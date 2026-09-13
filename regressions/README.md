# Regressions — FDM360

Este diretório concentra fixtures, resultados esperados e relatórios de regressão específicos do Fronteiras do Mundo 360.

## Regra

`ONE FAILURE -> FIXTURE FIRST -> RULE ONLY IF GENERALIZABLE`

## Categorias mínimas

- GEO_ALIGNMENT
- GEO_ANCHOR
- LABEL_BINDING
- CAMERA_MEANING
- SEMANTIC_BINDING
- MILITARY_EVENT_TRUTH
- DISPUTED_TERRITORY
- CAPTION_SAFE_AREA
- AUDIO_VISUAL_SYNC
- POST_RENDER_INTEGRITY

## Estados

- PASS
- CANDIDATE
- BLOCK
- REJECTED

Uma versão de vídeo aprovada visualmente não invalida automaticamente regressões anteriores; o histórico deve permanecer auditável.
