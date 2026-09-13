from pathlib import Path


def read_text(path: str) -> str:
    return (Path(__file__).parents[1] / path).read_text(encoding="utf-8")


def test_reference_library_governance_defaults_to_reference_only():
    text = read_text("references/style_library/README.md")
    assert "REFERENCE_ONLY" in text
    assert "uma referência isolada não altera automaticamente a identidade do canal" in text


def test_ref_015_is_profile_specific_and_not_auto_promoted():
    text = read_text("references/style_library/FDM360_REF_STYLE_015.yaml")
    assert "profile_specific: true" in text
    assert "promote_to_identity_automatically: false" in text
    assert "status: REFERENCE_ONLY" in text


def test_ref_001_preserves_continuous_spatial_sequence_lock():
    text = read_text("references/style_library/FDM360_REF_STYLE_001.yaml")
    assert "continuous_spatial_sequence" in text
    assert "semantic_camera_motion" in text


def test_unrecovered_references_are_not_fabricated():
    text = read_text("references/style_library/UNRECOVERED_REFERENCES.yaml")
    for number in range(3, 15):
        assert f"FDM360_REF_STYLE_{number:03d}" in text
    assert text.count("provenance_status: UNRECOVERED") == 12


def test_performance_memory_is_profile_specific_and_requires_promotion():
    text = read_text("performance/PERFORMANCE_MEMORY.md")
    assert "PROFILE-SPECIFIC" in text
    assert "CANDIDATE -> VALIDATED -> PROMOTED" in text
    assert "Um único vídeo" in text


def test_continuous_camera_rule_is_persistent():
    text = read_text("performance/PERFORMANCE_MEMORY.md")
    assert "movimento de câmera contínuo" in text
