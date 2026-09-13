from __future__ import annotations

import hashlib
import io
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

import rarfile
import requests
import shapefile
from bs4 import BeautifulSoup
from pyproj import CRS, Transformer
from shapely import normalize, set_precision, to_wkb
from shapely.geometry import Point, Polygon, mapping, shape
from shapely.ops import transform, unary_union
from shapely.validation import explain_validity

OUT = Path("build/geo_truth_v05")
RAW = OUT / "raw"
NORM = OUT / "normalized"
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
NORM.mkdir(parents=True, exist_ok=True)

TIMEOUT = 60
UA = {"User-Agent": "FDM360-GeoTruth/1.0 (+https://github.com/luisfabricioviana-dev/Fronteiras-do-Mundo-360)"}

SOURCES = {
    "brazil": {
        "authority": "IBGE",
        "url": "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2024/Brasil/BR_Pais_2024.zip",
    },
    "colombia": {
        "authority": "IGAC",
        "service": "https://mapas.igac.gov.co/server/rest/services/ObservatorioInmobiliario/DepartamentosOIC/FeatureServer/0",
    },
    "peru": {
        "authority": "IGN / IDEP",
        "service": "https://www.idep.gob.pe/geoportal/rest/services/DATOS_GEOESPACIALES/PERU/FeatureServer/0",
    },
    "ecuador": {
        "authority": "IGM Ecuador",
        "catalog": "https://www.geoportaligm.gob.ec/portal/index.php/descargas/enlaces-google-earth/",
    },
}

CAPITALS_SERVICE = "https://www.idep.gob.pe/geoportal/rest/services/DATOS_GEOESPACIALES/CENTROS_POBLADOS/FeatureServer/0"
ANCHORS = {
    "iquitos": {"service": CAPITALS_SERVICE, "match": "IQUITOS"},
    "callao": {"service": CAPITALS_SERVICE, "match": "CALLAO"},
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_bytes(url: str, *, params: dict[str, Any] | None = None) -> tuple[bytes, str]:
    r = requests.get(url, params=params, timeout=TIMEOUT, headers=UA)
    r.raise_for_status()
    return r.content, r.url


def canonical_geometry_hash(geom) -> str:
    g = normalize(set_precision(geom, grid_size=1e-9))
    return sha256(to_wkb(g, byte_order=1, output_dimension=2))


def write_geojson(name: str, geom, properties: dict[str, Any]) -> Path:
    p = NORM / f"{name}.geojson"
    obj = {
        "type": "FeatureCollection",
        "name": name,
        "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
        "features": [{"type": "Feature", "properties": properties, "geometry": mapping(geom)}],
    }
    p.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    return p


def ensure_polygonal(geom):
    if geom.geom_type in {"Polygon", "MultiPolygon"}:
        return geom
    polys = [g for g in getattr(geom, "geoms", []) if g.geom_type in {"Polygon", "MultiPolygon"}]
    if not polys:
        raise ValueError(f"Expected polygonal geometry, got {geom.geom_type}")
    merged = unary_union(polys)
    if merged.geom_type not in {"Polygon", "MultiPolygon"}:
        raise ValueError(f"Polygon union produced {merged.geom_type}")
    return merged


def deterministic_zip(entries: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, entries[name])
    return buf.getvalue()


def arcgis_geojson(service: str, raw_name: str) -> tuple[dict[str, Any], bytes, str]:
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
    }
    data, final_url = get_bytes(f"{service}/query", params=params)
    (RAW / raw_name).write_bytes(data)
    obj = json.loads(data.decode("utf-8"))
    if obj.get("type") != "FeatureCollection":
        raise ValueError(f"Unexpected ArcGIS GeoJSON response from {service}: {str(obj)[:500]}")
    return obj, data, final_url


def arcgis_geojson_chunked(service: str, raw_name: str, chunk_size: int = 4) -> tuple[dict[str, Any], bytes, str]:
    ids_bytes, ids_url = get_bytes(
        f"{service}/query",
        params={"where": "1=1", "returnIdsOnly": "true", "f": "json"},
    )
    ids_obj = json.loads(ids_bytes.decode("utf-8"))
    object_ids = ids_obj.get("objectIds") or []
    if not object_ids:
        raise ValueError(f"No object IDs returned from {service}")
    entries: dict[str, bytes] = {"object_ids.json": ids_bytes}
    features: list[dict[str, Any]] = []
    for i in range(0, len(object_ids), chunk_size):
        batch = object_ids[i : i + chunk_size]
        data, _ = get_bytes(
            f"{service}/query",
            params={
                "objectIds": ",".join(str(v) for v in batch),
                "outFields": "*",
                "returnGeometry": "true",
                "outSR": "4326",
                "f": "geojson",
            },
        )
        obj = json.loads(data.decode("utf-8"))
        if obj.get("type") != "FeatureCollection":
            raise ValueError(f"Unexpected chunk response from {service}: {str(obj)[:300]}")
        features.extend(obj.get("features", []))
        entries[f"chunk_{i // chunk_size:03d}.geojson"] = data
    package = deterministic_zip(entries)
    (RAW / raw_name).write_bytes(package)
    return {"type": "FeatureCollection", "features": features}, package, ids_url


def service_metadata(service: str) -> dict[str, Any]:
    data, _ = get_bytes(service, params={"f": "json"})
    return json.loads(data.decode("utf-8"))


def ingest_brazil() -> tuple[Any, dict[str, Any]]:
    cfg = SOURCES["brazil"]
    data, final_url = get_bytes(cfg["url"])
    (RAW / "BR_Pais_2024.zip").write_bytes(data)
    extract_dir = RAW / "brazil_unzipped"
    extract_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(extract_dir)
    shp_files = list(extract_dir.rglob("*.shp"))
    if len(shp_files) != 1:
        raise ValueError(f"Expected one Brazil shapefile, found {len(shp_files)}")
    shp = shp_files[0]
    prj = shp.with_suffix(".prj")
    if not prj.exists():
        raise ValueError("Brazil shapefile missing .prj")
    native_crs = CRS.from_wkt(prj.read_text(encoding="utf-8", errors="ignore"))
    transformer = Transformer.from_crs(native_crs, CRS.from_epsg(4326), always_xy=True)
    reader = shapefile.Reader(str(shp))
    geoms = [shape(s.__geo_interface__) for s in reader.shapes()]
    geom = ensure_polygonal(unary_union([transform(transformer.transform, g) for g in geoms]))
    write_geojson("brazil", geom, {"authority": cfg["authority"], "source_url": final_url})
    return geom, {
        "authority": cfg["authority"],
        "source_url": final_url,
        "source_format": "ZIP_SHAPEFILE",
        "raw_file_sha256": sha256(data),
        "native_crs": native_crs.to_string(),
        "normalized_crs": "EPSG:4326",
        "normalized_geometry_sha256": canonical_geometry_hash(geom),
        "geometry_loaded": True,
        "valid": geom.is_valid,
        "validity": explain_validity(geom),
        "feature_count_raw": len(geoms),
    }


def ingest_arcgis_country(name: str, service: str, authority: str) -> tuple[Any, dict[str, Any]]:
    meta = service_metadata(service)
    spatial_ref = (meta.get("extent") or {}).get("spatialReference") or {}
    wkid = spatial_ref.get("latestWkid") or spatial_ref.get("wkid")
    native = f"EPSG:{wkid}" if wkid else None
    if name == "colombia":
        obj, raw_bytes, final_url = arcgis_geojson_chunked(service, "colombia_official_export.zip")
        source_format = "ARCGIS_FEATURE_SERVICE_CHUNKED_GEOJSON_EXPORT_ZIP"
    else:
        obj, raw_bytes, final_url = arcgis_geojson(service, f"{name}_official_export.geojson")
        source_format = "ARCGIS_FEATURE_SERVICE_GEOJSON_EXPORT"
    geoms = [shape(f["geometry"]) for f in obj.get("features", []) if f.get("geometry")]
    if not geoms:
        raise ValueError(f"No polygon features returned for {name}")
    geom = ensure_polygonal(unary_union(geoms))
    write_geojson(name, geom, {"authority": authority, "source_url": final_url})
    return geom, {
        "authority": authority,
        "source_url": final_url,
        "source_service": service,
        "source_format": source_format,
        "raw_file_sha256": sha256(raw_bytes),
        "native_crs": native,
        "normalized_crs": "EPSG:4326",
        "normalized_geometry_sha256": canonical_geometry_hash(geom),
        "geometry_loaded": True,
        "valid": geom.is_valid,
        "validity": explain_validity(geom),
        "feature_count_raw": len(geoms),
        "derivation": "dissolve_all_official_polygons" if len(geoms) > 1 else "official_country_polygon",
    }


def find_igm_kml_link(label: str) -> str:
    catalog = SOURCES["ecuador"]["catalog"]
    html, _ = get_bytes(catalog)
    soup = BeautifulSoup(html, "html.parser")
    target = label.casefold()
    for row in soup.find_all("tr"):
        text = " ".join(row.stripped_strings).casefold()
        if target in text:
            a = row.find("a", href=True)
            if a:
                return requests.compat.urljoin(catalog, a["href"])
    for a in soup.find_all("a", href=True):
        text = " ".join(a.stripped_strings).casefold()
        title = (a.get("title") or "").casefold()
        if target in text or target in title:
            return requests.compat.urljoin(catalog, a["href"])
    raise ValueError(f"Could not resolve IGM download link for {label}")


def unwrap_kml(data: bytes) -> bytes:
    if not data.startswith(b"Rar!"):
        return data
    with rarfile.RarFile(io.BytesIO(data)) as rf:
        names = [n for n in rf.namelist() if n.lower().endswith(".kml")]
        if len(names) != 1:
            raise ValueError(f"Expected exactly one KML inside IGM RAR, found {names}")
        return rf.read(names[0])


def parse_kml_polygons(data: bytes) -> list[Polygon]:
    root = ET.fromstring(data)
    ns = {"k": "http://www.opengis.net/kml/2.2"}
    polygons: list[Polygon] = []

    def parse_ring(text: str):
        coords = []
        for token in text.split():
            parts = token.split(",")
            if len(parts) >= 2:
                coords.append((float(parts[0]), float(parts[1])))
        return coords

    for poly in root.findall(".//k:Polygon", ns):
        outer_node = poly.find("./k:outerBoundaryIs/k:LinearRing/k:coordinates", ns)
        if outer_node is None or not (outer_node.text or "").strip():
            continue
        outer = parse_ring(outer_node.text or "")
        inners = []
        for inner_node in poly.findall("./k:innerBoundaryIs/k:LinearRing/k:coordinates", ns):
            ring = parse_ring(inner_node.text or "")
            if ring:
                inners.append(ring)
        if len(outer) >= 4:
            polygons.append(Polygon(outer, inners))
    return polygons


def ingest_ecuador() -> tuple[Any, dict[str, Any]]:
    provinces_url = find_igm_kml_link("Provincias")
    boundary_url = find_igm_kml_link("Limite Internacional")
    provinces_archive, provinces_final = get_bytes(provinces_url)
    boundary_archive, boundary_final = get_bytes(boundary_url)
    provinces_kml = unwrap_kml(provinces_archive)
    boundary_kml = unwrap_kml(boundary_archive)
    (RAW / "ecuador_provincias_download.bin").write_bytes(provinces_archive)
    (RAW / "ecuador_limite_internacional_download.bin").write_bytes(boundary_archive)
    (RAW / "ecuador_provincias.kml").write_bytes(provinces_kml)
    (RAW / "ecuador_limite_internacional.kml").write_bytes(boundary_kml)
    polys = parse_kml_polygons(provinces_kml)
    if not polys:
        raise ValueError("No province polygons parsed from official Ecuador IGM KML")
    geom = ensure_polygonal(unary_union(polys))
    write_geojson("ecuador", geom, {"authority": "IGM Ecuador", "source_url": provinces_final})
    return geom, {
        "authority": "IGM Ecuador",
        "source_url": provinces_final,
        "verification_boundary_url": boundary_final,
        "source_format": "RAR_CONTAINING_KML_PROVINCES_DISSOLVED",
        "source_year": 2013,
        "source_scale": "1:2000000",
        "raw_file_sha256": sha256(provinces_archive),
        "verification_boundary_raw_sha256": sha256(boundary_archive),
        "native_crs": "EPSG:4326",
        "normalized_crs": "EPSG:4326",
        "normalized_geometry_sha256": canonical_geometry_hash(geom),
        "geometry_loaded": True,
        "valid": geom.is_valid,
        "validity": explain_validity(geom),
        "feature_count_raw": len(polys),
        "derivation": "dissolve_official_province_polygons",
    }


def find_anchor(name: str, cfg: dict[str, str]) -> dict[str, Any]:
    obj, raw_bytes, final_url = arcgis_geojson(cfg["service"], f"anchor_{name}_source.geojson")
    needle = cfg["match"].casefold()
    candidates = []
    for f in obj.get("features", []):
        props = f.get("properties") or {}
        hay = " | ".join(str(v) for v in props.values() if v is not None).casefold()
        if needle in hay and f.get("geometry"):
            g = shape(f["geometry"])
            if g.geom_type == "Point":
                candidates.append((props, g))
    result: dict[str, Any] = {
        "source_url": final_url,
        "raw_file_sha256": sha256(raw_bytes),
        "candidate_count": len(candidates),
        "anchor_verified": False,
        "candidates": [],
    }
    for props, g in candidates:
        result["candidates"].append({"properties": props, "lon": g.x, "lat": g.y})
    if len(candidates) == 1:
        props, g = candidates[0]
        result.update({"anchor_verified": True, "lon": g.x, "lat": g.y, "properties": props})
    return result


def main() -> int:
    report: dict[str, Any] = {
        "bundle": "GEO_TRUTH_REFERENCE_BUNDLE_v05",
        "normalized_crs": "EPSG:4326",
        "countries": {},
        "anchors": {},
        "checks": {},
        "status": "BLOCK",
        "pre_render_geo_truth": "BLOCK",
    }
    errors: list[str] = []
    geoms: dict[str, Any] = {}

    for name, loader in (
        ("brazil", lambda: ingest_brazil()),
        ("colombia", lambda: ingest_arcgis_country("colombia", SOURCES["colombia"]["service"], SOURCES["colombia"]["authority"])),
        ("peru", lambda: ingest_arcgis_country("peru", SOURCES["peru"]["service"], SOURCES["peru"]["authority"])),
        ("ecuador", lambda: ingest_ecuador()),
    ):
        try:
            geoms[name], report["countries"][name] = loader()
        except Exception as e:
            errors.append(f"{name}: {e}")

    for anchor_name, cfg in ANCHORS.items():
        try:
            report["anchors"][anchor_name] = find_anchor(anchor_name, cfg)
        except Exception as e:
            errors.append(f"anchor {anchor_name}: {e}")

    countries_complete = set(geoms) == {"brazil", "colombia", "peru", "ecuador"}
    all_valid = countries_complete and all(g.is_valid and not g.is_empty for g in geoms.values())
    anchors_verified = all(report["anchors"].get(k, {}).get("anchor_verified") is True for k in ("iquitos", "callao"))
    containment = False
    if "peru" in geoms and anchors_verified:
        peru = geoms["peru"]
        containment = all(
            peru.covers(Point(report["anchors"][k]["lon"], report["anchors"][k]["lat"]))
            for k in ("iquitos", "callao")
        )

    hashes_complete = countries_complete and all(
        report["countries"][k].get("raw_file_sha256") and report["countries"][k].get("normalized_geometry_sha256")
        for k in ("brazil", "colombia", "peru", "ecuador")
    )

    report["checks"] = {
        "countries_complete": countries_complete,
        "all_country_geometries_valid": all_valid,
        "hashes_complete": bool(hashes_complete),
        "anchors_verified_exactly_once": anchors_verified,
        "anchors_contained_in_peru": containment,
        "normalized_crs": "EPSG:4326",
    }
    report["errors"] = errors

    passed = countries_complete and all_valid and hashes_complete and anchors_verified and containment and not errors
    if passed:
        report["status"] = "PASS"
        report["pre_render_geo_truth"] = "PASS"

    (OUT / "geo_truth_reference_bundle_v05.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
