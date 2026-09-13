import json
from pathlib import Path


MANIFEST = Path(__file__).parents[1] / "integration" / "shared_core_compatibility.json"


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_shared_core_lock_is_pinned_to_green_ci():
    data = load_manifest()
    assert data["verified_core_commit"] == "97fb894e61d93e75270f3b9c95cb69e257616ed2"
    assert data["verified_ci_run"] == 34
    assert data["verified_ci_result"] == "SUCCESS"


def test_all_required_shared_core_capabilities_are_resolved():
    data = load_manifest()
    capabilities = data["capabilities"]
    required = [
        "POST_RENDER_SEMANTIC_INTEGRITY",
        "Render Observation Adapter",
        "SEMANTIC_BINDING_INTEGRITY_v1",
        "Camera-Meaning Integrity",
        "Iconography Truth Gate",
        "AGENT_CAPABILITY_RUNTIME_v1",
        "THEME_TO_FINAL_VIDEO_RUNTIME_v1",
        "CROSS_AGENT_LEARNING_CORE_v1",
    ]
    for capability in required:
        item = capabilities[capability]
        assert item["status"] == "RESOLVED_SHARED_CORE"
        assert item["path"].startswith("contracts/")


def test_no_unresolved_shared_core_remains():
    data = load_manifest()
    statuses = {item["status"] for item in data["capabilities"].values()}
    assert "UNRESOLVED_SHARED_CORE" not in statuses


def test_governance_blocks_local_duplication():
    data = load_manifest()
    rules = data["rules"]
    assert rules["profile_must_not_duplicate_resolved_shared_core"] is True
    assert rules["unresolved_shared_core_must_not_be_marked_implemented_locally"] is True
    assert rules["compatibility_lock_requires_green_core_ci"] is True
