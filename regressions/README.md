# Regressions — FDM360

Este diretório concentra fixtures, resultados esperados e relatórios de regressão específicos do Fronteiras do Mundo 360.

## Regra

`ONE FAILURE -> FIXTURE FIRST -> RULE ONLY IF GENERALIZABLE`

## Categorias mínimas

- GEO_ALIGNMENT
- GEO_ANCHOR
- LABEL_BINDING
- CAMERA_MEANING
- CAMERA_CONTINUITY
- SEMANTIC_BINDING
- MILITARY_EVENT_TRUTH
- DISPUTED_TERRITORY
- CAPTION_SAFE_AREA
- AUDIO_VISUAL_SYNC
- POST_RENDER_INTEGRITY

## CAMERA_CONTINUITY

Para vídeos de mapa animado do FDM360, a unidade visual canônica é uma única cena geográfica contínua. Beats sucessivos devem ser ligados por movimento de câmera, mudança de escala, recentering, target lock ou evidence return. Frames cartográficos independentes, substituição do mapa entre beats e crossfade entre estados cartográficos incompatíveis são regressões mesmo quando cada frame isolado está correto.

## Estados

- PASS
- CANDIDATE
- BLOCK
- REJECTED

Uma versão de vídeo aprovada visualmente não invalida automaticamente regressões anteriores; o histórico deve permanecer auditável.
