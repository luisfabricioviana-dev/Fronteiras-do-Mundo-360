# Caso de regressão — Presença dos Estados Unidos na América do Sul

## Papel

Fixture real para validar Geo Motion, truth locks, semantic binding, câmera, labels, anchors, captions e pós-render do FDM360.

## Histórico resumido

- v37 — BLOCK: labels deslocados; Iquitos/Callao sem âncora; uso problemático de “infraestrutura”.
- v38 — CANDIDATE: sequência corrigida; termo removido.
- v39.1 — BLOCK: contornos de Equador/Peru/Brasil desalinhados do basemap.
- v39.4 — melhoria de sincronização; ainda exige validação geoespacial final.

## Invariantes derivados

- labels devem estar ancorados ao território correto;
- cidades/pontos só podem aparecer com âncora geográfica válida;
- overlays territoriais não podem divergir do basemap;
- a câmera deve preservar significado geográfico durante zoom/pan;
- o mapa deve ser um fluxo contínuo, não frames independentes;
- linguagem deve distinguir presença/atividade observada de inferência estratégica;
- o payoff não pode afirmar que a evidência prova um plano para cercar o Brasil.

## Uso

Este caso deve ser reutilizado como fixture de regressão sempre que houver alteração em Geo Motion, anchors, labels, truth locks ou pós-render semântico.
