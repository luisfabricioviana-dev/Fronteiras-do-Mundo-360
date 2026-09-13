# FDM360 — Migration Registry

Registro de migração de conhecimento do projeto para o repositório canônico.

## Status

- `CANONICAL_IMPLEMENTED` — persistido e validado no repositório.
- `CANONICAL_SPEC` — persistido como especificação, ainda sem implementação/testes completos.
- `NEEDS_PORTING` — conhecido no projeto, ainda não materializado aqui.
- `SHARED_CORE` — pertence ao `agente-youtube`; aqui deve existir apenas configuração/extensão.

## Estado — 2026-09-13

| Capability / Contract | Target | Status |
|---|---|---|
| FDM360 channel profile | FDM360 | CANONICAL_SPEC |
| Visual Bible | FDM360 | CANONICAL_SPEC |
| Narrative rules | FDM360 | CANONICAL_SPEC |
| Production preferences | FDM360 | CANONICAL_SPEC |
| US Presence South America regression case | FDM360 | CANONICAL_IMPLEMENTED |
| Geo Motion profile configuration | FDM360 | CANONICAL_IMPLEMENTED |
| Geospatial Truth Lock config/fixtures | FDM360 | CANONICAL_IMPLEMENTED |
| Military Event Truth Lock config/fixtures | FDM360 | CANONICAL_IMPLEMENTED |
| Geo Asset Registry | FDM360 | CANONICAL_IMPLEMENTED |
| Motion Coherence + Geo Anchor QA profile rules | FDM360 | CANONICAL_IMPLEMENTED |
| Disputed Territory Gate profile rules | FDM360 | CANONICAL_IMPLEMENTED |
| Geo Repair Router profile rules | FDM360 | CANONICAL_IMPLEMENTED |
| STRAIT_REVEAL | FDM360 | CANONICAL_SPEC |
| MILITARY_BASE_REVEAL | FDM360 | CANONICAL_SPEC |
| RESOURCE_CORRIDOR | FDM360 | CANONICAL_SPEC |
| PORT_PROJECTION | FDM360 | CANONICAL_SPEC |
| SUBMARINE_CABLE_ROUTE | FDM360 | CANONICAL_SPEC |
| DISPUTED_BORDER | FDM360 | CANONICAL_SPEC |
| ISLAND_STRATEGIC_REVEAL | FDM360 | CANONICAL_SPEC |
| Reference Style Library entries | FDM360 | CANONICAL_IMPLEMENTED |
| Performance Memory | FDM360 | CANONICAL_IMPLEMENTED |
| POST_RENDER_SEMANTIC_INTEGRITY | agente-youtube | SHARED_CORE |
| Render Observation Adapter | agente-youtube | SHARED_CORE |
| SEMANTIC_BINDING_INTEGRITY_v1 | agente-youtube | SHARED_CORE |
| Camera-Meaning Integrity | agente-youtube | SHARED_CORE |
| Iconography Truth Gate | agente-youtube | SHARED_CORE |
| CROSS_AGENT_LEARNING_CORE_v1 | shared ecosystem | SHARED_CORE |
| THEME_TO_FINAL_VIDEO_RUNTIME_v1 | agente-youtube | SHARED_CORE |
| AGENT_CAPABILITY_RUNTIME_v1 | shared ecosystem | SHARED_CORE |

## Implemented artifacts

- `geo/motion/fdm360_geo_motion_profile.py`
- `geo/truth_locks/fdm360_truth_locks.py`
- `geo/asset_registry/fdm360_geo_asset_registry.py`
- `geo/qa/fdm360_geo_qa.py`
- `geo/repair/repair_router.py`
- `regressions/fixtures/us_presence_south_america_v1.json`
- `tests/test_geo_motion_truth_stack.py`
- `.github/workflows/geo-regression.yml`
- `references/style_library/README.md`
- `references/style_library/FDM360_REF_STYLE_001.yaml`
- `references/style_library/FDM360_REF_STYLE_002.yaml`
- `references/style_library/FDM360_REF_STYLE_015.yaml`
- `references/style_library/UNRECOVERED_REFERENCES.yaml`
- `performance/PERFORMANCE_MEMORY.md`
- `tests/test_reference_memory_integrity.py`

## Notes

The semantic template family remains specification-level because the connector blocked the consolidated template manifest write. Do not mark those templates implemented until a persisted machine-readable registry and regression coverage exist.

Reference styles 003–014 are registered as `UNRECOVERED`; their missing metadata must not be fabricated.

GitHub Actions workflow/status was not exposed for the latest commits at the time of this update. Therefore repository persistence and test definitions are confirmed, but CI pass status is not yet claimed.

## Promotion rule

Nenhum item `NEEDS_PORTING` muda para `CANONICAL_IMPLEMENTED` sem fixture/teste correspondente quando o comportamento for executável ou verificável.
