from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GeoClaim:
    target_id: str
    source_anchor: Optional[str]
    precision: str = "NORMAL"
    disputed: bool = False
    military_event: bool = False
    evidence_strength: str = "SUPPORTED"


@dataclass(frozen=True)
class TruthLockResult:
    allowed: bool
    reason: str


def geospatial_truth_lock(claim: GeoClaim) -> TruthLockResult:
    if not claim.source_anchor:
        return TruthLockResult(False, "missing_geo_anchor")
    if claim.precision == "CRITICAL" and claim.evidence_strength != "VERIFIED":
        return TruthLockResult(False, "critical_precision_requires_verified_evidence")
    if claim.disputed and claim.evidence_strength != "VERIFIED":
        return TruthLockResult(False, "disputed_territory_requires_verified_evidence")
    return TruthLockResult(True, "geo_claim_allowed")


def military_event_truth_lock(claim: GeoClaim) -> TruthLockResult:
    base = geospatial_truth_lock(claim)
    if not base.allowed:
        return base
    if claim.military_event and claim.evidence_strength != "VERIFIED":
        return TruthLockResult(False, "military_event_requires_verified_evidence")
    return TruthLockResult(True, "military_claim_allowed")
