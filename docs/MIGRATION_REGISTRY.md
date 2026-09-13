# FDM360 — Migration Registry

Registro de migração de conhecimento do projeto para o repositório canônico.

## Status

- `CANONICAL_IMPLEMENTED` — persistido e validado no repositório.
- `CANONICAL_SPEC` — persistido como especificação, ainda sem implementação/testes completos.
- `NEEDS_PORTING` — conhecido no projeto, ainda não materializado aqui.
- `SHARED_CORE` — pertence ao `agente-youtube`; aqui deve existir apenas configuração/extensão.

## Estado inicial — 2026-09-13

| Capability / Contract | Target | Status |
|---|---|---|
| FDM360 channel profile | FDM360 | CANONICAL_SPEC |
| Visual Bible | FDM360 | CANONICAL_SPEC |
| Narrative rules | FDM360 | CANONICAL_SPEC |
| Production preferences | FDM360 | CANONICAL_SPEC |
| US Presence South America regression case | FDM360 | CANONICAL_SPEC |
| Geo Motion profile configuration | FDM360 | NEEDS_PORTING |
| Geospatial Truth Lock config/fixtures | FDM360 | NEEDS_PORTING |
| Military Event Truth Lock config/fixtures | FDM360 | NEEDS_PORTING |
| Geo Asset Registry | FDM360 | NEEDS_PORTING |
| Motion Coherence + Geo Anchor QA profile rules | FDM360 | NEEDS_PORTING |
| Disputed Territory Gate profile rules | FDM360 | NEEDS_PORTING |
| Geo Repair Router profile rules | FDM360 | NEEDS_PORTING |
| STRAIT_REVEAL | FDM360 | NEEDS_PORTING |
| MILITARY_BASE_REVEAL | FDM360 | NEEDS_PORTING |
| RESOURCE_CORRIDOR | FDM360 | NEEDS_PORTING |
| PORT_PROJECTION | FDM360 | NEEDS_PORTING |
| SUBMARINE_CABLE_ROUTE | FDM360 | NEEDS_PORTING |
| DISPUTED_BORDER | FDM360 | NEEDS_PORTING |
| ISLAND_STRATEGIC_REVEAL | FDM360 | NEEDS_PORTING |
| Reference Style Library entries | FDM360 | NEEDS_PORTING |
| Performance Memory | FDM360 | NEEDS_PORTING |
| POST_RENDER_SEMANTIC_INTEGRITY | agente-youtube | SHARED_CORE |
| Render Observation Adapter | agente-youtube | SHARED_CORE |
| SEMANTIC_BINDING_INTEGRITY_v1 | agente-youtube | SHARED_CORE |
| Camera-Meaning Integrity | agente-youtube | SHARED_CORE |
| Iconography Truth Gate | agente-youtube | SHARED_CORE |
| CROSS_AGENT_LEARNING_CORE_v1 | shared ecosystem | SHARED_CORE |
| THEME_TO_FINAL_VIDEO_RUNTIME_v1 | agente-youtube | SHARED_CORE |
| AGENT_CAPABILITY_RUNTIME_v1 | shared ecosystem | SHARED_CORE |

## Promotion rule

Nenhum item `NEEDS_PORTING` muda para `CANONICAL_IMPLEMENTED` sem fixture/teste correspondente quando o comportamento for executável ou verificável.
