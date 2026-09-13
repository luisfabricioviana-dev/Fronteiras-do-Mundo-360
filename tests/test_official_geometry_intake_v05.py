import json
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str):
    return json.loads(read_text(path))


def test_all_four_official_geometries_are_loaded_and_hashed():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "status: PASS" in text
    assert "pre_render_geo_truth: PASS" in text
    assert text.count("geometry_loaded: true") == 4
    assert text.count("geometry_valid: true") == 4
    assert "raw_file_sha256: null" not in text
    assert "normalized_geometry_sha256: null" not in text
    hashes = re.findall(r"(?:raw_file_sha256|normalized_geometry_sha256): ([0-9a-f]{64})", text)
    assert len(hashes) >= 8


def test_operational_sources_match_validated_bundle():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "authority: IBGE" in text
    assert "DANE — Marco Geoestadístico Nacional 2025" in text
    assert "Serv_DIVIPOLA_MGN_2025/FeatureServer/319" in text
    assert "Instituto Geografico Nacional / IDEP" in text
    assert "Instituto Geografico Militar / IGM Ecuador" in text
    assert "OGC_WFS_GEOJSON_PROVINCES_DISSOLVED" in text
    assert "IGAC remains the sovereignty/border reference" in text


def test_exact_country_hashes_are_locked():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    for expected in (
        "e84c4d4ab199e646b5a180e0f5b7a991fe4c3d424dff8ae3dcf4495992c128d5",
        "ef57940d055ee4b7647a2b0d85e9f9e3fac5eeb40966dae50dea9824e730240f",
        "c018afcf84038be7e88b91430c3bf98fc027c1d6fe5722ff0e9372630649b5e3",
        "f6aefb92519563b3ec20a0e8265e178950a716269f038953a21097db9da5eb77",
        "7e32825a15d664bb37711265abe17b28506a96d48530aaa3590179317e0c6bd3",
        "cde8aeea3f3ce869f56f474e2c8678c989607080e5e2855ef3f01100be9ab04e",
        "2e78f40bb83dc0d11a74e6abc056166a51b4b4478f2ecfcacddfd16bdeb67808",
        "f21a2f9d40130f4073cbe54f1477a7712aa6558c0b6681aa7d7f96f2c17c7feb",
        "b9f2cb04a3e43e8308d7acf7174eb6c1bb3f503049ddf790bce608ffe0293c0b",
    ):
        assert expected in text


def test_callao_and_iquitos_are_verified_unique_official_anchors():
    text = read_text("geo/asset_registry/peru_anchor_intake_v05.yaml")
    assert "status: VERIFIED" in text
    assert text.count("feature_status: VERIFIED_UNIQUE") == 2
    assert text.count("anchor_verified: true") == 2
    assert text.count("candidate_count: 1") == 2
    assert "longitude: -77.11477973299998" in text
    assert "latitude: -12.047523470999977" in text
    assert "longitude: -73.25946289099994" in text
    assert "latitude: -3.749269530999925" in text
    assert "containment_in_peru: PASS" in text
    assert "02e45f4af4f28181818c8c57ab8d9fef5c9adaa629528798a7d18b835292b202" in text


def test_canonical_evidence_bundle_is_pass_but_not_publication_ready():
    bundle = read_json("geo/evidence/GEO_TRUTH_REFERENCE_BUNDLE_v05.json")
    assert bundle["status"] == "PASS"
    assert bundle["pre_render_geo_truth"] == "PASS"
    assert bundle["post_render_geo_truth"] == "NOT_RUN"
    assert bundle["publication_ready"] is False
    assert bundle["errors"] == []
    assert all(bundle["checks"][k] is True for k in (
        "countries_complete",
        "all_country_geometries_valid",
        "hashes_complete",
        "anchors_verified_exactly_once",
        "anchors_contained_in_peru",
    ))
    assert bundle["workflow_evidence"]["run_id"] == 34774202581
    assert bundle["workflow_evidence"]["artifact_digest"] == "sha256:83ad29718259efdba20308e55e5c7fcacf95bba4dcde8886c78ae707e15d32ff"


def test_post_render_and_publication_gates_remain_closed():
    text = read_text("geo/asset_registry/official_geometry_intake_v05.yaml")
    assert "post_render_geo_truth: NOT_RUN" in text
    assert "publication_ready: false" in text
