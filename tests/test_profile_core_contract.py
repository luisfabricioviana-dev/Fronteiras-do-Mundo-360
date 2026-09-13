from pathlib import Path

PROFILE = Path(__file__).parents[1] / "profile"


def read(name):
    return (PROFILE / name).read_text(encoding="utf-8")


def test_channel_profile_core_contract():
    text = read("channel_profile.yaml")
    assert "profile_id: FDM360" in text
    assert "style_isolation: true" in text
    assert "performance_memory_scope: PROFILE_SPECIFIC" in text
    assert "reference_library_scope: PROFILE_SPECIFIC" in text
    assert "cross_channel_contamination: BLOCKED" in text
    assert "core_dependency: agente-youtube" in text


def test_visual_bible_core_contract():
    text = read("visual_bible.yaml")
    assert "monochrome_black_white: REJECTED" in text
    assert "continuous_camera_motion: REQUIRED" in text
    assert "disconnected_static_frames: REJECTED" in text
    assert "geo_anchor_integrity: REQUIRED" in text
    assert "blurry_assets: REJECTED" in text


def test_production_motion_contract():
    text = read("production_preferences.yaml")
    assert "mode: CONTINUOUS" in text
    assert "static_single_zoom: REJECTED" in text
    assert "disconnected_frames: REJECTED" in text
    assert "static_only: REJECTED" in text
