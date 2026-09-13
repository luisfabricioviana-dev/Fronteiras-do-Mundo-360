from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Tuple


class TemplateId(str, Enum):
    STRAIT_REVEAL = "STRAIT_REVEAL"
    MILITARY_BASE_REVEAL = "MILITARY_BASE_REVEAL"
    RESOURCE_CORRIDOR = "RESOURCE_CORRIDOR"
    PORT_PROJECTION = "PORT_PROJECTION"
    SUBMARINE_CABLE_ROUTE = "SUBMARINE_CABLE_ROUTE"
    DISPUTED_BORDER = "DISPUTED_BORDER"
    ISLAND_STRATEGIC_REVEAL = "ISLAND_STRATEGIC_REVEAL"


@dataclass(frozen=True)
class SemanticTemplate:
    template_id: TemplateId
    purpose: str
    required_geo_relations: FrozenSet[str]
    preferred_motion_families: Tuple[str, ...]
    requires_continuous_camera: bool = True
    requires_verified_geo_anchor: bool = True
    requires_truth_lock: bool = True
    requires_geo_qa: bool = True
    disputed_territory_gate: bool = False
    military_event_truth_lock: bool = False


TEMPLATES = {
    TemplateId.STRAIT_REVEAL: SemanticTemplate(
        TemplateId.STRAIT_REVEAL,
        "Reveal a narrow maritime passage by moving from regional context to the constrained waterway.",
        frozenset({"regional_context", "waterway", "adjacent_landmasses"}),
        ("CONTEXTUAL_REVEAL", "TARGET_MOTION"),
    ),
    TemplateId.MILITARY_BASE_REVEAL: SemanticTemplate(
        TemplateId.MILITARY_BASE_REVEAL,
        "Reveal a verified installation from regional context without inferring operational intent.",
        frozenset({"regional_context", "verified_site_anchor"}),
        ("CONTEXTUAL_REVEAL", "TARGET_MOTION", "EVIDENCE_RETURN"),
        military_event_truth_lock=True,
    ),
    TemplateId.RESOURCE_CORRIDOR: SemanticTemplate(
        TemplateId.RESOURCE_CORRIDOR,
        "Explain a resource-linked geographic corridor using verified origin, route and destination anchors.",
        frozenset({"origin", "route", "destination"}),
        ("RELATION_MOTION", "TARGET_MOTION"),
    ),
    TemplateId.PORT_PROJECTION: SemanticTemplate(
        TemplateId.PORT_PROJECTION,
        "Reveal a port and its geographic connectivity without implying unsupported strategic conclusions.",
        frozenset({"port_anchor", "regional_context"}),
        ("CONTEXTUAL_REVEAL", "RELATION_MOTION"),
    ),
    TemplateId.SUBMARINE_CABLE_ROUTE: SemanticTemplate(
        TemplateId.SUBMARINE_CABLE_ROUTE,
        "Trace a verified submarine cable route between confirmed landing points.",
        frozenset({"landing_point_a", "route", "landing_point_b"}),
        ("RELATION_MOTION", "TARGET_MOTION"),
    ),
    TemplateId.DISPUTED_BORDER: SemanticTemplate(
        TemplateId.DISPUTED_BORDER,
        "Explain a disputed boundary while preserving source attribution and territorial uncertainty.",
        frozenset({"claimant_a", "claimant_b", "disputed_geometry"}),
        ("CONTEXTUAL_REVEAL", "TERRITORIAL_TRANSFORMATION", "EVIDENCE_RETURN"),
        disputed_territory_gate=True,
    ),
    TemplateId.ISLAND_STRATEGIC_REVEAL: SemanticTemplate(
        TemplateId.ISLAND_STRATEGIC_REVEAL,
        "Move from regional context to a verified island anchor and explain only supported geographic relationships.",
        frozenset({"regional_context", "island_anchor"}),
        ("CONTEXTUAL_REVEAL", "TARGET_MOTION", "RELATION_MOTION"),
    ),
}


def get_template(template_id: TemplateId) -> SemanticTemplate:
    return TEMPLATES[template_id]


def validate_template(template: SemanticTemplate) -> None:
    if not template.requires_continuous_camera:
        raise ValueError("FDM360 semantic templates must require continuous camera motion")
    if not template.requires_verified_geo_anchor:
        raise ValueError("FDM360 semantic templates must require verified geo anchors")
    if not template.requires_truth_lock or not template.requires_geo_qa:
        raise ValueError("FDM360 semantic templates cannot bypass truth locks or geo QA")
    if not template.required_geo_relations:
        raise ValueError("Semantic template must define required geographic relations")
