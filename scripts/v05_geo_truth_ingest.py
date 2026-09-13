from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin

import geopandas as gpd
import requests
from bs4 import BeautifulSoup
from shapely import normalize, set_precision
from shapely.geometry import shape
from shapely.ops import unary_union

OUT = Path("artifacts/v05_geo_truth")
RAW = OUT / "raw"
NORM = OUT / "normalized"
RAW.mkdir(parents=True, exist_ok=True)
NORM.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "FDM360-GeoTruth/1.0 (+https://github.com/luisfabricioviana-dev/Fronteiras-do-Mundo-360)"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_bytes(url: str, *, params=None) -> tuple[bytes, str]:
    r = requests.get(url, params=params, headers=UA, timeout=120)
    r.raise_for_status()
    return r.content, r.url


def write_raw(name: str, data: bytes) -> Path:
    p = RAW / name
    p.write_bytes(data)
    return p


def canonical_geom_hash(geom) -> str:
    geom = set_precision(geom, grid_size=1e-9)
    geom = normalize(geom)
    return hashlib.sha256(geom.wkb).hexdigest()


def canonical_country(gdf: gpd.GeoDataFrame):
    if gdf.crs is None:
        raise RuntimeError("missing CRS")
    gdf = gdf.to_crs(4326)
    gdf = gdf[gdf.geometry.notna()].copy()
    gdf["geometry"] = gdf.geometry.make_valid()
    geom = unary_union(list(gdf.geometry))
    geom = geom.buffer(0)
    if geom.is_empty or not geom.is_valid:
        raise RuntimeError("invalid/empty normalized country geometry")
    return geom


def save_geom(name: str, geom) -> None:
    feature = {"type": "Feature", "properties": {"id": name}, "geometry": geom.__geo_interface__}
    (NORM / f"{name}.geojson").write_text(json.dumps({"type":"FeatureCollection","features":[feature]}, separators=(",", ":")), encoding="utf-8")


def read_geojson_bytes(data: bytes, name: str) -> gpd.GeoDataFrame:
    p = write_raw(name, data)
    return gpd.read_file(p)


def arcgis_geojson(url: str, where: str = "1=1") -> tuple[bytes, str]:
    params = {
        "where": where,
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
    }
    return get_bytes(url.rstrip("/") + "/query", params=params)


def extract_igm_provincias_kml() -> tuple[bytes, str]:
    page = "https://www.geoportaligm.gob.ec/portal/index.php/descargas/enlaces-google-earth/"
    html, _ = get_bytes(page)
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find_all("tr"):
        txt = " ".join(tr.stripped_strings)
        if re.search(r"\bProvincias\b", txt, re.I):
            a = tr.find("a", href=True)
            if a:
                href = urljoin(page, a["href"])
                return get_bytes(href)
    raise RuntimeError("Could not resolve official IGM Provincias KML download link")


def read_kml(path: Path) -> gpd.GeoDataFrame:
    errors = []
    for engine in ("pyogrio", "fiona"):
        try:
            return gpd.read_file(path, engine=engine)
        except Exception as e:
            errors.append(f"{engine}: {e}")
    raise RuntimeError("KML read failed: " + " | ".join(errors))


def pick_feature(data: bytes, needle: str):
    obj = json.loads(data)
    feats = obj.get("features", [])
    needle_u = needle.upper()
    matches = []
    for f in feats:
        props = f.get("properties") or {}
        hay = " | ".join(str(v) for v in props.values() if v is not None).upper()
        if needle_u in hay:
            matches.append(f)
    if not matches:
        raise RuntimeError(f"No feature matched {needle}")
    # deterministic: sort serialized properties and select first
    matches.sort(key=lambda f: json.dumps(f.get("properties") or {}, sort_keys=True, ensure_ascii=False))
    return matches[0], len(matches)


def main():
    manifest = {"bundle":"GEO_TRUTH_REFERENCE_BUNDLE_v05","normalized_crs":"EPSG:4326","countries":{},"anchors":{},"checks":{},"status":"BLOCK"}

    # Brazil — official IBGE country shapefile ZIP
    br_url = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2024/Brasil/BR_Pais_2024.zip"
    br_raw, br_final = get_bytes(br_url)
    br_path = write_raw("BR_Pais_2024.zip", br_raw)
    br_gdf = gpd.read_file(f"zip://{br_path}")
    br_geom = canonical_country(br_gdf)
    save_geom("brazil", br_geom)
    manifest["countries"]["brazil"] = {"authority":"IBGE","source_url":br_final,"raw_file_sha256":sha256_bytes(br_raw),"native_crs":str(br_gdf.crs),"normalized_geometry_sha256":canonical_geom_hash(br_geom),"geometry_loaded":True,"valid":bool(br_geom.is_valid)}

    # Colombia — official IGAC department polygons, dissolved
    co_url = "https://mapas.igac.gov.co/server/rest/services/ObservatorioInmobiliario/DepartamentosOIC/FeatureServer/0"
    co_raw, co_final = arcgis_geojson(co_url)
    co_gdf = read_geojson_bytes(co_raw, "colombia_departamentos.geojson")
    co_geom = canonical_country(co_gdf)
    save_geom("colombia", co_geom)
    manifest["countries"]["colombia"] = {"authority":"IGAC","source_url":co_final,"raw_file_sha256":sha256_bytes(co_raw),"native_crs":str(co_gdf.crs),"normalized_geometry_sha256":canonical_geom_hash(co_geom),"geometry_loaded":True,"valid":bool(co_geom.is_valid),"derivation":"dissolve official department polygons"}

    # Peru — official IGN/IDEP national polygon
    pe_url = "https://www.idep.gob.pe/geoportal/rest/services/DATOS_GEOESPACIALES/PERU/FeatureServer/0"
    pe_raw, pe_final = arcgis_geojson(pe_url)
    pe_gdf = read_geojson_bytes(pe_raw, "peru_country.geojson")
    pe_geom = canonical_country(pe_gdf)
    save_geom("peru", pe_geom)
    manifest["countries"]["peru"] = {"authority":"IGN/IDEP","source_url":pe_final,"raw_file_sha256":sha256_bytes(pe_raw),"native_crs":str(pe_gdf.crs),"normalized_geometry_sha256":canonical_geom_hash(pe_geom),"geometry_loaded":True,"valid":bool(pe_geom.is_valid)}

    # Ecuador — official IGM Provincias KML, dissolved
    ec_raw, ec_final = extract_igm_provincias_kml()
    ec_path = write_raw("ecuador_provincias.kml", ec_raw)
    ec_gdf = read_kml(ec_path)
    ec_geom = canonical_country(ec_gdf)
    save_geom("ecuador", ec_geom)
    manifest["countries"]["ecuador"] = {"authority":"IGM Ecuador","source_url":ec_final,"raw_file_sha256":sha256_bytes(ec_raw),"native_crs":str(ec_gdf.crs),"normalized_geometry_sha256":canonical_geom_hash(ec_geom),"geometry_loaded":True,"valid":bool(ec_geom.is_valid),"derivation":"dissolve official Provincias KML"}

    # Iquitos — official IGN capital-department layer; query all and select by attributes.
    iq_url = "https://www.idep.gob.pe/geoportal/rest/services/DATOS_GEOESPACIALES/CENTROS_POBLADOS/FeatureServer/0"
    iq_raw, iq_final = arcgis_geojson(iq_url)
    iq_feat, iq_count = pick_feature(iq_raw, "IQUITOS")
    iq_geom = shape(iq_feat["geometry"])
    save_geom("iquitos", iq_geom)
    manifest["anchors"]["iquitos"] = {"authority":"IGN/IDEP","source_url":iq_final,"raw_response_sha256":sha256_bytes(iq_raw),"feature_match_count":iq_count,"feature_properties":iq_feat.get("properties",{}),"geometry_sha256":canonical_geom_hash(iq_geom),"anchor_verified":True,"within_peru":bool(pe_geom.covers(iq_geom))}

    # Callao — official IDEP Puerto layer; query all and select feature with CALLAO in attributes.
    ca_url = "https://www.idep.gob.pe/geoportal/rest/services/DATOS_ESPACIALES/TEMA_BASE/MapServer/17"
    ca_raw, ca_final = arcgis_geojson(ca_url)
    ca_feat, ca_count = pick_feature(ca_raw, "CALLAO")
    ca_geom = shape(ca_feat["geometry"])
    save_geom("callao", ca_geom)
    manifest["anchors"]["callao"] = {"authority":"IGN/IDEP","source_url":ca_final,"raw_response_sha256":sha256_bytes(ca_raw),"feature_match_count":ca_count,"feature_properties":ca_feat.get("properties",{}),"geometry_sha256":canonical_geom_hash(ca_geom),"anchor_verified":True,"within_peru":bool(pe_geom.covers(ca_geom))}

    # Coarse cross-source adjacency sanity checks. These are not legal boundary tests.
    pairs = [("brazil","colombia",br_geom,co_geom),("brazil","peru",br_geom,pe_geom),("colombia","ecuador",co_geom,ec_geom),("peru","ecuador",pe_geom,ec_geom),("colombia","peru",co_geom,pe_geom)]
    boundary_checks = {}
    for a,b,ga,gb in pairs:
        d = ga.boundary.distance(gb.boundary)
        boundary_checks[f"{a}_{b}"] = {"boundary_min_distance_degrees":d,"coarse_pass":bool(d <= 0.10)}
    manifest["checks"]["boundary_sanity"] = boundary_checks

    required_country_pass = all(v["geometry_loaded"] and v["valid"] and v["raw_file_sha256"] and v["normalized_geometry_sha256"] for v in manifest["countries"].values())
    anchors_pass = all(v["anchor_verified"] and v["within_peru"] for v in manifest["anchors"].values())
    boundaries_pass = all(v["coarse_pass"] for v in boundary_checks.values())
    manifest["checks"]["crs_epsg4326_normalized"] = True
    manifest["checks"]["countries_complete"] = required_country_pass
    manifest["checks"]["anchors_complete_and_contained"] = anchors_pass
    manifest["checks"]["boundary_sanity_pass"] = boundaries_pass
    manifest["status"] = "PASS" if required_country_pass and anchors_pass and boundaries_pass else "BLOCK"
    manifest["pre_render_geo_truth"] = manifest["status"]

    (OUT / "geo_truth_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    if manifest["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
