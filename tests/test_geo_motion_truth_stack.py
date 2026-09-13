import json
from pathlib import Path

import pytest

from geo.asset_registry.fdm360_geo_asset_registry import GeoAsset, GeoAssetRegistry
from geo.motion.fdm360_geo_motion_profile import (
    GeoBeat,
    GeoMotionContinuityError,
    GeoSceneContinuity,
    MotionFamily,
    RenderRoute,
    compile_motion_plan,
    validate_continuous_geo_motion,
)
from geo.qa.fdm360_geo_qa import VisualGeoElement, camera_meaning_integrity, motion_coherence_and_anchor_qa
from geo.repair.repair_router import route_repairs
from geo.truth_locks.fdm360_truth_locks import GeoClaim, geospatial_truth_lock, military_event_truth_lock


def test_continuous_camera_is_mandatory():
    plan = compile_motion_plan([GeoBeat("brazil", MotionFamily.CONTEXTUAL_REVEAL)])
    assert plan.continuous_camera is True
    assert plan.scene_continuity == GeoSceneContinuity.CONTINUOUS
    assert plan.allow_independent_map_frames is False
    assert plan.allow_map_replacement_between_beats is False


def test_critical_precision_routes_to_premium_tracking():
    plan = compile_motion_plan([GeoBeat("callao", MotionFamily.TARGET_MOTION, precision="CRITICAL")])
    assert plan.route == RenderRoute.PREMIUM_TRACKED_GEO


def test_relation_motion_routes_to_hybrid_when_not_critical():
    plan = compile_motion_plan([GeoBeat("corridor", MotionFamily.RELATION_MOTION)])
    assert plan.route == RenderRoute.HYBRID_GEO


def test_independent_map_frames_are_blocked():
    plan = compile_motion_plan([
        GeoBeat("colombia", MotionFamily.TARGET_MOTION),
        GeoBeat("ecuador", MotionFamily.TARGET_MOTION),
    ])
    with pytest.raises(GeoMotionContinuityError, match="independent_map_frames_forbidden"):
        validate_continuous_geo_motion(plan, independent_map_frames_used=True)


def test_map_replacement_between_beats_is_blocked():
    plan = compile_motion_plan([
        GeoBeat("peru", MotionFamily.TARGET_MOTION),
        GeoBeat("brazil", MotionFamily.TARGET_MOTION),
    ])
    with pytest.raises(GeoMotionContinuityError, match="map_replacement_between_beats_forbidden"):
        validate_continuous_geo_motion(plan, map_replacement_between_beats=True)


def test_crossfade_between_mismatched_map_states_is_blocked():
    plan = compile_motion_plan([GeoBeat("peru", MotionFamily.CONTEXTUAL_REVEAL)])
    with pytest.raises(GeoMotionContinuityError, match="mismatched_map_crossfade_forbidden"):
        validate_continuous_geo_motion(plan, mismatched_map_crossfade=True)


def test_clean_continuous_camera_path_passes():
    plan = compile_motion_plan([
        GeoBeat("south_america", MotionFamily.CONTEXTUAL_REVEAL),
        GeoBeat("colombia", MotionFamily.TARGET_MOTION),
        GeoBeat("ecuador", MotionFamily.TARGET_MOTION),
        GeoBeat("peru", MotionFamily.TARGET_MOTION),
        GeoBeat("callao", MotionFamily.SCALE_MOTION, precision="CRITICAL"),
        GeoBeat("iquitos", MotionFamily.TARGET_MOTION, precision="CRITICAL"),
        GeoBeat("brazil", MotionFamily.TARGET_MOTION),
        GeoBeat("south_america", MotionFamily.EVIDENCE_RETURN),
    ])
    validate_continuous_geo_motion(plan)


def test_missing_anchor_is_blocked():
    result = geospatial_truth_lock(GeoClaim("iquitos", None))
    assert result.allowed is False
    assert result.reason == "missing_geo_anchor"


def test_critical_geo_claim_requires_verified_evidence():
    result = geospatial_truth_lock(GeoClaim("callao", "callao_peru", precision="CRITICAL", evidence_strength="SUPPORTED"))
    assert result.allowed is False


def test_verified_military_event_is_allowed():
    result = military_event_truth_lock(
        GeoClaim("exercise", "official_source", military_event=True, evidence_strength="VERIFIED")
    )
    assert result.allowed is True


def test_anchor_mismatch_and_screen_drift_fail_qa():
    result = motion_coherence_and_anchor_qa(
        [VisualGeoElement("label_ecuador", "colombia", "ecuador", moves_with_map=False)],
        continuous_camera=True,
    )
    assert result.passed is False
    assert "label_ecuador:anchor_mismatch" in result.failures
    assert "label_ecuador:screen_space_drift" in result.failures


def test_disconnected_frames_fail_qa():
    result = motion_coherence_and_anchor_qa([], continuous_camera=False)
    assert result.passed is False
    assert "disconnected_geo_frames" in result.failures


def test_camera_meaning_integrity():
    assert camera_meaning_integrity("peru", "peru").passed is True
    assert camera_meaning_integrity("ecuador", "peru").passed is False


def test_geo_asset_registry_rejects_unverified_disputed_asset():
    registry = GeoAssetRegistry()
    try:
        registry.register(GeoAsset("border_x", "Border X", "border", "source", verified=False, disputed=True))
    except ValueError as exc:
        assert "must be verified" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_repair_router_reanchors_and_recompiles():
    plan = route_repairs(["label_ecuador:anchor_mismatch", "camera_semantic_target_mismatch"])
    assert "REANCHOR" in plan.actions
    assert "RECOMPILE_CAMERA_PATH" in plan.actions
    assert plan.hold_release is False


def test_repair_router_holds_release_for_unverified_asset():
    plan = route_repairs(["unverified_asset"])
    assert "REPLACE_ASSET" in plan.actions
    assert plan.hold_release is True


def test_regression_fixture_preserves_editorial_lock():
    fixture_path = Path(__file__).parents[1] / "regressions" / "fixtures" / "us_presence_south_america_v1.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert fixture["continuous_camera_required"] is True
    assert fixture["single_geo_scene_required"] is True
    assert "surround Brazil" in fixture["editorial_lock"]
