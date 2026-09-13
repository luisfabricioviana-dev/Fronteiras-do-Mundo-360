from contracts.v05_publication_gate import (
    V05GateState,
    enrichment_allowed,
    publication_ready,
    render_v05_allowed,
)


def test_render_requires_official_geometry_and_pre_render_geo_truth():
    assert not render_v05_allowed(V05GateState())
    assert not render_v05_allowed(V05GateState(official_geometries_loaded=True))
    assert render_v05_allowed(
        V05GateState(
            official_geometries_loaded=True,
            pre_render_geo_truth_pass=True,
        )
    )


def test_proxy_voice_is_hard_block_for_enrichment():
    state = V05GateState(
        post_render_geo_truth_pass=True,
        final_voice_selected=True,
        proxy_voice_used=True,
    )
    assert not enrichment_allowed(state)


def test_publication_requires_exact_final_hash_and_all_gates():
    base = dict(
        official_geometries_loaded=True,
        pre_render_geo_truth_pass=True,
        post_render_geo_truth_pass=True,
        final_voice_selected=True,
        proxy_voice_used=False,
        rights_provenance_pass=True,
        semantic_qa_pass=True,
        audio_qa_pass=True,
        mobile_qa_pass=True,
        profile_fit_pass=True,
    )
    assert not publication_ready(V05GateState(**base))
    assert publication_ready(
        V05GateState(
            **base,
            final_render_sha256="a" * 64,
        )
    )


def test_any_failed_final_gate_blocks_publication():
    state = V05GateState(
        official_geometries_loaded=True,
        pre_render_geo_truth_pass=True,
        post_render_geo_truth_pass=False,
        final_voice_selected=True,
        rights_provenance_pass=True,
        semantic_qa_pass=True,
        audio_qa_pass=True,
        mobile_qa_pass=True,
        profile_fit_pass=True,
        final_render_sha256="b" * 64,
    )
    assert not publication_ready(state)
