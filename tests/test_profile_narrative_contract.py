from pathlib import Path

PROFILE = Path(__file__).parents[1] / "profile"


def test_narrative_contract_preserves_geo_truth_and_continuity():
    text = (PROFILE / "narrative_rules.yaml").read_text(encoding="utf-8")
    assert "narrative_mode: GEO_DOCUMENTARY" in text
    assert "voiceover_first: true" in text
    assert "map_as_narrative: true" in text
    assert "geography_must_not_be_invented" in text
    assert "disputed_territory_requires_explicit_gate" in text
    assert "camera_motion_must_preserve_semantic_meaning" in text
    assert "payoff_must_not_overclaim_evidence" in text
    assert "map_video_mode: CONTINUOUS_CAMERA_PATH" in text
    assert "disconnected_scene_frames: BLOCKED" in text
