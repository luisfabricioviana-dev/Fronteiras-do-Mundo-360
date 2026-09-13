from audiovisual.post_render.fdm360_post_render_profile import (
    PostRenderObservation,
    evaluate_fdm360_post_render,
    publication_gate,
)
from geo.repair.repair_router import route_repairs


def test_clean_render_passes_publication_gate():
    result = evaluate_fdm360_post_render([
        PostRenderObservation(
            element_id="peru_label",
            semantic_target="peru",
            rendered_target="peru",
            geo_anchor_expected="peru",
            geo_anchor_rendered="peru",
            moves_with_map=True,
            outline_matches_basemap=True,
            iconography_verified=True,
        )
    ])
    assert result.passed is True
    assert publication_gate(result) == "PASS"


def test_semantic_target_mismatch_blocks_release():
    result = evaluate_fdm360_post_render([
        PostRenderObservation(
            element_id="camera_beat_04",
            semantic_target="ecuador",
            rendered_target="peru",
        )
    ])
    assert result.passed is False
    assert "camera_beat_04:semantic_binding_mismatch" in result.failures
    assert "camera_beat_04:camera_semantic_target_mismatch" in result.failures
    assert publication_gate(result) == "BLOCK_REPAIR_REQUIRED"


def test_label_drift_routes_to_reanchor():
    result = evaluate_fdm360_post_render([
        PostRenderObservation(
            element_id="ecuador_label",
            semantic_target="ecuador",
            rendered_target="ecuador",
            geo_anchor_expected="ecuador",
            geo_anchor_rendered="colombia",
            moves_with_map=False,
        )
    ])
    plan = route_repairs(result.failures)
    assert "REANCHOR" in plan.actions


def test_outline_misalignment_routes_to_basemap_repair():
    result = evaluate_fdm360_post_render([
        PostRenderObservation(
            element_id="brazil_outline",
            semantic_target="brazil",
            rendered_target="brazil",
            outline_matches_basemap=False,
        )
    ])
    plan = route_repairs(result.failures)
    assert "REALIGN_BASEMAP" in plan.actions


def test_unverified_iconography_holds_release():
    result = evaluate_fdm360_post_render([
        PostRenderObservation(
            element_id="military_icon",
            semantic_target="verified_site",
            rendered_target="verified_site",
            iconography_verified=False,
        )
    ])
    plan = route_repairs(result.failures)
    assert "REPLACE_ASSET" in plan.actions
    assert plan.hold_release is True


def test_profile_preserves_map_binding_requirement():
    result = evaluate_fdm360_post_render([
        PostRenderObservation(
            element_id="callao_label",
            semantic_target="callao",
            rendered_target="callao",
            geo_anchor_expected="callao",
            geo_anchor_rendered="callao",
            moves_with_map=False,
        )
    ])
    assert "callao_label:screen_space_drift" in result.failures
