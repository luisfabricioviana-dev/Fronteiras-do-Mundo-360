from __future__ import annotations

import json
import sys

from shapely.geometry import shape
from shapely.ops import unary_union
from shapely.validation import explain_validity

import build_geo_truth_reference_bundle_v05 as b

# Use the lighter official IGAC political-administrative department layer.
b.SOURCES["colombia"]["service"] = (
    "https://mapas.igac.gov.co/server/rest/services/atlas/"
    "politicoadministrativo/MapServer/5"
)


def wfs_geojson(type_name: str, raw_name: str):
    endpoint = "https://www.geoportaligm.gob.ec/nacional/wfs"
    params = {
        "service": "WFS",
        "version": "1.1.0",
        "request": "GetFeature",
        "typeName": type_name,
        "outputFormat": "application/json",
        "srsName": "EPSG:4326",
    }
    data, final_url = b.get_bytes(endpoint, params=params)
    (b.RAW / raw_name).write_bytes(data)
    obj = json.loads(data.decode("utf-8"))
    if obj.get("type") != "FeatureCollection":
        raise ValueError(f"Unexpected WFS response for {type_name}: {str(obj)[:300]}")
    return obj, data, final_url


def ingest_ecuador_wfs():
    provinces_obj, provinces_bytes, provinces_url = wfs_geojson(
        "igm:provincias", "ecuador_provincias_wfs.geojson"
    )
    boundary_obj, boundary_bytes, boundary_url = wfs_geojson(
        "igm:limite", "ecuador_limite_wfs.geojson"
    )
    geoms = [
        shape(f["geometry"])
        for f in provinces_obj.get("features", [])
        if f.get("geometry")
    ]
    if not geoms:
        raise ValueError("No official IGM province polygons returned by WFS")
    geom = b.ensure_polygonal(unary_union(geoms))
    b.write_geojson(
        "ecuador",
        geom,
        {"authority": "IGM Ecuador", "source_url": provinces_url},
    )
    return geom, {
        "authority": "IGM Ecuador",
        "source_url": provinces_url,
        "verification_boundary_url": boundary_url,
        "source_format": "OGC_WFS_GEOJSON_PROVINCES_DISSOLVED",
        "raw_file_sha256": b.sha256(provinces_bytes),
        "verification_boundary_raw_sha256": b.sha256(boundary_bytes),
        "native_crs": "EPSG:4326",
        "normalized_crs": "EPSG:4326",
        "normalized_geometry_sha256": b.canonical_geometry_hash(geom),
        "geometry_loaded": True,
        "valid": geom.is_valid,
        "validity": explain_validity(geom),
        "feature_count_raw": len(geoms),
        "verification_boundary_feature_count": len(boundary_obj.get("features", [])),
        "derivation": "dissolve_official_igm_province_polygons",
    }


b.ingest_ecuador = ingest_ecuador_wfs

if __name__ == "__main__":
    sys.exit(b.main())
