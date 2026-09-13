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
    beats: List[GeoBeat]


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
        beats=beats,
    )
