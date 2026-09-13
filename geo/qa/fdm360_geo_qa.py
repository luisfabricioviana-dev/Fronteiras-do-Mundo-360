from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class VisualGeoElement:
    element_id: str
    anchor_id: str | None
    expected_anchor_id: str | None
    moves_with_map: bool = True
    semantic_role: str = "generic"


@dataclass(frozen=True)
class QAResult:
    passed: bool
    failures: List[str]


def motion_coherence_and_anchor_qa(elements: Iterable[VisualGeoElement], continuous_camera: bool) -> QAResult:
    failures: List[str] = []
    if not continuous_camera:
        failures.append("disconnected_geo_frames")
    for element in elements:
        if not element.anchor_id:
            failures.append(f"{element.element_id}:missing_anchor")
        elif element.expected_anchor_id and element.anchor_id != element.expected_anchor_id:
            failures.append(f"{element.element_id}:anchor_mismatch")
        if not element.moves_with_map:
            failures.append(f"{element.element_id}:screen_space_drift")
    return QAResult(passed=not failures, failures=failures)


def camera_meaning_integrity(camera_target: str, narrated_target: str) -> QAResult:
    if camera_target != narrated_target:
        return QAResult(False, ["camera_semantic_target_mismatch"])
    return QAResult(True, [])
