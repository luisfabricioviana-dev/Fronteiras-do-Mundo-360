# Geo — FDM360

Camada específica de geografia e cartografia do Fronteiras do Mundo 360.

## Capacidades a persistir neste domínio

- Geo Motion System — configuração/extensão FDM360
- Geospatial Truth Lock
- Military Event Truth Lock
- Geo Asset Registry
- Geo Visual Beat Mapper — especialização do profile
- Camera Path rules do canal
- Motion Coherence + Geo Anchor QA
- Disputed Territory Gate
- Geo Repair Router

## Templates semânticos do profile

- STRAIT_REVEAL
- MILITARY_BASE_REVEAL
- RESOURCE_CORRIDOR
- PORT_PROJECTION
- SUBMARINE_CABLE_ROUTE
- DISPUTED_BORDER
- ISLAND_STRATEGIC_REVEAL

## Regra de fronteira

Algoritmos genéricos de motion/routing pertencem ao `agente-youtube`. Este diretório guarda configuração, locks, fixtures, templates e extensões específicas do FDM360.

## Invariante principal

`MAP_ANIMATION = CONTINUOUS_CAMERA_PATH`, não sequência de frames cartográficos independentes.
