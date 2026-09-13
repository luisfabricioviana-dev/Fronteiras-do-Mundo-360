from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class PostRenderObservation:
    element_id: str
    semantic_target: Optional[str]
    rendered_target: Optional[str]
    geo_anchor_expected: Optional[str] = None
    geo_anchor_rendered: Optional[str] = None
    moves_with_map: bool = True
    outline_matches_basemap: bool = True
    iconography_verified: bool = True


@dataclass(frozen=True)
class PostRenderResult:
    passed: bool
    failures: List[str]


def evaluate_fdm360_post_render(observations: List[PostRenderObservation]) -> PostRenderResult:
    failures: List[str] = []

    for obs in observations:
        if obs.semantic_target and obs.rendered_target and obs.semantic_target != obs.rendered_target:
            failures.append(f"{obs.element_id}:semantic_binding_mismatch")
            failures.append(f"{obs.element_id}:camera_semantic_target_mismatch")

        if obs.geo_anchor_expected and obs.geo_anchor_rendered and obs.geo_anchor_expected != obs.geo_anchor_rendered:
            failures.append(f"{obs.element_id}:anchor_mismatch")

        if not obs.moves_with_map:
            failures.append(f"{obs.element_id}:screen_space_drift")

        if not obs.outline_matches_basemap:
            failures.append(f"{obs.element_id}:outline_basemap_misalignment")

        if not obs.iconography_verified:
            failures.append(f"{obs.element_id}:unverified_iconography")

    return PostRenderResult(passed=not failures, failures=failures)


def publication_gate(result: PostRenderResult) -> str:
    return "PASS" if result.passed else "BLOCK_REPAIR_REQUIRED"
