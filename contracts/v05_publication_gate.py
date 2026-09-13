from dataclasses import dataclass


@dataclass(frozen=True)
class V05GateState:
    official_geometries_loaded: bool = False
    pre_render_geo_truth_pass: bool = False
    post_render_geo_truth_pass: bool = False
    final_voice_selected: bool = False
    proxy_voice_used: bool = False
    rights_provenance_pass: bool = False
    semantic_qa_pass: bool = False
    audio_qa_pass: bool = False
    mobile_qa_pass: bool = False
    profile_fit_pass: bool = False
    final_render_sha256: str | None = None


def publication_ready(state: V05GateState) -> bool:
    if state.proxy_voice_used:
        return False
    if not state.final_render_sha256:
        return False
    required = (
        state.official_geometries_loaded,
        state.pre_render_geo_truth_pass,
        state.post_render_geo_truth_pass,
        state.final_voice_selected,
        state.rights_provenance_pass,
        state.semantic_qa_pass,
        state.audio_qa_pass,
        state.mobile_qa_pass,
        state.profile_fit_pass,
    )
    return all(required)


def render_v05_allowed(state: V05GateState) -> bool:
    return state.official_geometries_loaded and state.pre_render_geo_truth_pass


def enrichment_allowed(state: V05GateState) -> bool:
    return (
        state.post_render_geo_truth_pass
        and state.final_voice_selected
        and not state.proxy_voice_used
    )
