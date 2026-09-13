from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class RepairPlan:
    actions: List[str]
    hold_release: bool


def route_repairs(failures: Iterable[str]) -> RepairPlan:
    actions: List[str] = []
    hold_release = False

    for failure in failures:
        if "anchor_mismatch" in failure or "screen_space_drift" in failure:
            actions.append("REANCHOR")
        elif "disconnected_geo_frames" in failure or "camera_semantic_target_mismatch" in failure or "semantic_binding_mismatch" in failure:
            actions.append("RECOMPILE_CAMERA_PATH")
        elif "outline_basemap_misalignment" in failure:
            actions.append("REALIGN_BASEMAP")
        elif "unverified" in failure or "truth_lock" in failure:
            actions.append("REPLACE_ASSET")
            hold_release = True
        else:
            actions.append("MANUAL_REVIEW")
            hold_release = True

    return RepairPlan(list(dict.fromkeys(actions)), hold_release)
