from dataclasses import dataclass
from enum import Enum
from typing import Iterable, List


class MotionFamily(str, Enum):
    SCALE_MOTION = "SCALE_MOTION"
    TARGET_MOTION = "TARGET_MOTION"
    RELATION_MOTION = "RELATION_MOTION"
    CONTEXTUAL_REVEAL = "CONTEXTUAL_REVEAL"
    TERRITORIAL_TRANSFORMATION = "TERRITORIAL_TRANSFORMATION"
    EVIDENCE_RETURN = "EVIDENCE_RETURN"


class RenderRoute(str, Enum):
    QUICK_MOBILE_GEO = "QUICK_MOBILE_GEO"
    AI_GEO_MOTION = "AI_GEO_MOTION"
    HYBRID_GEO = "HYBRID_GEO"
    PREMIUM_TRACKED_GEO = "PREMIUM_TRACKED_GEO"


class GeoSceneContinuity(str, Enum):
    CONTINUOUS = "CONTINUOUS"
    DISCONNECTED = "DISCONNECTED"


@dataclass(frozen=True)
class GeoBeat:
    target_id: str
    family: MotionFamily
    precision: str = "NORMAL"
    disputed_territory: bool = False
    geo_tracking_required: bool = False


@dataclass(frozen=True)
class MotionPlan:
    route: RenderRoute
    continuous_camera: bool
    scene_continuity: GeoSceneContinuity
    beats: List[GeoBeat]
    allow_independent_map_frames: bool = False
    allow_map_replacement_between_beats: bool = False


class GeoMotionContinuityError(ValueError):
    pass


def select_route(beats: Iterable[GeoBeat], prototype_quality: str = "NORMAL") -> RenderRoute:
    beats = list(beats)
    if any(b.disputed_territory or b.precision == "CRITICAL" or b.geo_tracking_required for b in beats):
        return RenderRoute.PREMIUM_TRACKED_GEO
    if prototype_quality == "LOW":
        return RenderRoute.QUICK_MOBILE_GEO
    if any(b.family in {MotionFamily.RELATION_MOTION, MotionFamily.TERRITORIAL_TRANSFORMATION} for b in beats):
        return RenderRoute.HYBRID_GEO
    return RenderRoute.AI_GEO_MOTION


def compile_motion_plan(beats: Iterable[GeoBeat], prototype_quality: str = "NORMAL") -> MotionPlan:
    beats = list(beats)
    if not beats:
        raise ValueError("At least one geo beat is required")
    return MotionPlan(
        route=select_route(beats, prototype_quality=prototype_quality),
        continuous_camera=True,
        scene_continuity=GeoSceneContinuity.CONTINUOUS,
        beats=beats,
        allow_independent_map_frames=False,
        allow_map_replacement_between_beats=False,
    )


def validate_continuous_geo_motion(
    plan: MotionPlan,
    *,
    independent_map_frames_used: bool = False,
    map_replacement_between_beats: bool = False,
    mismatched_map_crossfade: bool = False,
) -> None:
    """Block map-video implementations that break the single continuous geo scene.

    FDM360 map videos must preserve spatial continuity through camera motion over one
    coherent geographic scene. Independent map frames, map replacement between beats,
    or crossfades between incompatible map states are regressions even when each frame
    is geographically correct in isolation.
    """
    failures = []
    if plan.scene_continuity != GeoSceneContinuity.CONTINUOUS or not plan.continuous_camera:
        failures.append("continuous_camera_not_enforced")
    if independent_map_frames_used or plan.allow_independent_map_frames:
        failures.append("independent_map_frames_forbidden")
    if map_replacement_between_beats or plan.allow_map_replacement_between_beats:
        failures.append("map_replacement_between_beats_forbidden")
    if mismatched_map_crossfade:
        failures.append("mismatched_map_crossfade_forbidden")
    if failures:
        raise GeoMotionContinuityError(",".join(failures))
