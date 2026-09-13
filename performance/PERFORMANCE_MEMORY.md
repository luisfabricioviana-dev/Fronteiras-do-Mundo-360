# FDM360 Performance Memory

Escopo: PROFILE-SPECIFIC.

## Princípios de governança
- Um único vídeo, uma única referência ou um único resultado não cria regra permanente.
- Aprendizados persistentes devem vir de evidência repetida, regressões ou instrução explícita.
- Falha observada deve virar fixture antes de virar regra geral, quando possível.
- Performance Memory é isolada por canal; não compartilhar identidade com outros perfis.

## Regras atualmente promovidas
- map-first quando localização for causal;
- linguagem Geo Documentary / Geo Motion;
- mapa como narrativa, não decoração;
- movimento de câmera contínuo em sequências cartográficas;
- evitar mapa preto e branco incompatível com a identidade aprovada;
- evitar zoom único estático;
- captions curtas em área segura;
- voiceover PT-BR claro;
- footage real pontual quando acrescenta evidência;
- preservar verdade geoespacial e semântica após render.

## Estados de aprendizado
`CANDIDATE -> VALIDATED -> PROMOTED`

A promoção exige evidência suficiente para evitar overfitting a um único vídeo.

## Ciclo de evolução
`FIXTURE -> HYPOTHESIS -> RENDER OBSERVATION -> QA -> RESULT -> LEARNING CANDIDATE -> REGRESSION -> VALIDATION`

Regras:
- uma observação isolada permanece `CANDIDATE`;
- validação exige recorrência e regressão verde;
- promoção exige validação e evidência repetida ou aprovação explícita;
- falha nova vira fixture antes de virar regra geral;
- QA de render, performance, referência de estilo e identidade do canal são camadas distintas.
