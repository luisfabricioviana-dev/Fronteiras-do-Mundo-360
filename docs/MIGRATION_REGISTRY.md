# FDM360 — Migration Registry

Registro de migração de conhecimento do projeto para o repositório canônico.

## Status

- `CANONICAL_IMPLEMENTED` — persistido e validado no repositório.
- `CANONICAL_SPEC` — persistido como especificação, ainda sem implementação/testes completos.
- `NEEDS_PORTING` — conhecido no projeto, ainda não materializado aqui.
- `SHARED_CORE_RESOLVED` — pertence ao `agente-youtube`, já materializado e validado no core compartilhado.
- `SHARED_CORE_UNRESOLVED` — pertence ao core compartilhado, mas ainda não foi materializado/validado.

## Estado — 2026-09-13

| Capability / Contract | Target | Status |
|---|---|---|
| FDM360 channel profile | FDM360 | CANONICAL_IMPLEMENTED |
| Visual Bible | FDM360 | CANONICAL_IMPLEMENTED |
| Narrative rules | FDM360 | CANONICAL_IMPLEMENTED |
| Production preferences | FDM360 | CANONICAL_IMPLEMENTED |
| US Presence South America regression case | FDM360 | CANONICAL_IMPLEMENTED |
| Geo Motion profile configuration | FDM360 | CANONICAL_IMPLEMENTED |
| Geospatial Truth Lock config/fixtures | FDM360 | CANONICAL_IMPLEMENTED |
| Military Event Truth Lock config/fixtures | FDM360 | CANONICAL_IMPLEMENTED |
| Geo Asset Registry | FDM360 | CANONICAL_IMPLEMENTED |
| Motion Coherence + Geo Anchor QA profile rules | FDM360 | CANONICAL_IMPLEMENTED |
| Disputed Territory Gate profile rules | FDM360 | CANONICAL_IMPLEMENTED |
| Geo Repair Router profile rules | FDM360 | CANONICAL_IMPLEMENTED |
| STRAIT_REVEAL | FDM360 | CANONICAL_IMPLEMENTED |
| MILITARY_BASE_REVEAL | FDM360 | CANONICAL_IMPLEMENTED |
| RESOURCE_CORRIDOR | FDM360 | CANONICAL_IMPLEMENTED |
| PORT_PROJECTION | FDM360 | CANONICAL_IMPLEMENTED |
| SUBMARINE_CABLE_ROUTE | FDM360 | CANONICAL_IMPLEMENTED |
| DISPUTED_BORDER | FDM360 | CANONICAL_IMPLEMENTED |
| ISLAND_STRATEGIC_REVEAL | FDM360 | CANONICAL_IMPLEMENTED |
| Reference Style Library entries | FDM360 | CANONICAL_IMPLEMENTED |
| Performance Memory | FDM360 | CANONICAL_IMPLEMENTED |
| FDM360 post-render semantic integrity profile | FDM360 | CANONICAL_IMPLEMENTED |
| FDM360 publication gate + repair binding | FDM360 | CANONICAL_IMPLEMENTED |
| Shared-core compatibility lock | FDM360 | CANONICAL_IMPLEMENTED |
| POST_RENDER_SEMANTIC_INTEGRITY | agente-youtube | SHARED_CORE_RESOLVED |
| Render Observation Adapter | agente-youtube | SHARED_CORE_RESOLVED |
| SEMANTIC_BINDING_INTEGRITY_v1 | agente-youtube | SHARED_CORE_RESOLVED |
| Camera-Meaning Integrity | agente-youtube | SHARED_CORE_RESOLVED |
| Iconography Truth Gate | agente-youtube | SHARED_CORE_RESOLVED |
| AGENT_CAPABILITY_RUNTIME_v1 | agente-youtube | SHARED_CORE_RESOLVED |
| CROSS_AGENT_LEARNING_CORE_v1 | agente-youtube | SHARED_CORE_UNRESOLVED |
| THEME_TO_FINAL_VIDEO_RUNTIME_v1 | agente-youtube | SHARED_CORE_UNRESOLVED |

## Implemented artifacts

- `profile/channel_profile.yaml`
- `profile/visual_bible.yaml`
- `profile/narrative_rules.yaml`
- `profile/production_preferences.yaml`
- `tests/test_profile_core_contract.py`
- `tests/test_profile_narrative_contract.py`
- `geo/motion/fdm360_geo_motion_profile.py`
- `geo/truth_locks/fdm360_truth_locks.py`
- `geo/asset_registry/fdm360_geo_asset_registry.py`
- `geo/qa/fdm360_geo_qa.py`
- `geo/repair/repair_router.py`
- `geo/templates/template_registry.py`
- `audiovisual/post_render/fdm360_post_render_profile.py`
- `regressions/fixtures/us_presence_south_america_v1.json`
- `tests/test_geo_motion_truth_stack.py`
- `tests/test_semantic_geo_templates.py`
- `tests/test_fdm360_post_render_profile.py`
- `.github/workflows/geo-regression.yml`
- `references/style_library/README.md`
- `references/style_library/FDM360_REF_STYLE_001.yaml`
- `references/style_library/FDM360_REF_STYLE_002.yaml`
- `references/style_library/FDM360_REF_STYLE_015.yaml`
- `references/style_library/UNRECOVERED_REFERENCES.yaml`
- `performance/PERFORMANCE_MEMORY.md`
- `tests/test_reference_memory_integrity.py`
- `integration/shared_core_compatibility.json`
- `tests/test_shared_core_compatibility_manifest.py`

## CI evidence

### FDM360
- Workflow: `FDM360 Geo Regression`
- Run: `26`
- Commit: `cfb1d0d52a891d72dcdf5a1d46aba08e159f0808`
- Result: `SUCCESS`
- `pytest -q`: `SUCCESS`

### Shared core (`agente-youtube`)
- Workflow: `reference-regression`
- Run: `28`
- Commit: `e5163cb932ac1bf6128ca00988babfb06e3c2abf`
- Result: `SUCCESS`
- Complete contract regression suite: `SUCCESS`

## Notes

The profile specification files are covered by regression tests, so changes to style isolation, map continuity, visual language and narrative continuity are no longer documentation-only.

The semantic template family is machine-readable and covered by regression tests. Templates cannot bypass verified geo anchors, Truth Locks or Geo QA.

The FDM360 post-render layer is a profile-specific specialization over shared audiovisual integrity concepts. Generic mechanisms remain in `agente-youtube`; this repository stores only FDM360 bindings, gates and regression behavior.

`integration/shared_core_compatibility.json` pins the profile to a known-green shared-core commit and explicitly distinguishes resolved from unresolved shared capabilities.

Reference styles 003–014 are registered as `UNRECOVERED`; their missing metadata must not be fabricated.

## Promotion rule

Nenhum item `NEEDS_PORTING` ou `SHARED_CORE_UNRESOLVED` muda para implementado/resolvido sem fixture/teste correspondente e evidência de CI quando o comportamento for executável ou verificável.
