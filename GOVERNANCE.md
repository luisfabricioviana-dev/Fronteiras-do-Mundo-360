# Governance — Fronteiras do Mundo 360

## Princípios canônicos

- `CORE SHARED != PROFILE-SPECIFIC`
- `NEW VIDEO != NEW RULE`
- `REFERENCE LIBRARY / STYLE MEMORY / PERFORMANCE MEMORY = PROFILE-SPECIFIC`
- `CROSS-CHANNEL CONTAMINATION = BLOCKED`
- `MEMORY_ONLY != CANONICAL_IMPLEMENTED`
- `ONE FAILURE -> FIXTURE FIRST -> RULE ONLY IF GENERALIZABLE`

## Fonte de verdade

Este repositório é a fonte canônica para comportamento durável específico do Fronteiras do Mundo 360.

A memória do ChatGPT, conversas, notas e análises são fontes de candidatos a melhoria. Elas só se tornam canônicas após materialização neste repositório e validação adequada.

## Critérios de promoção

Uma melhoria específica do canal deve seguir:

1. evidência ou falha observada;
2. especificação explícita;
3. fixture ou caso de regressão;
4. implementação/configuração versionada;
5. teste/regressão;
6. revisão de fronteira com o core compartilhado;
7. merge no `main`.

## Regra de não duplicação

Se uma capacidade for generalizável para outros canais, ela deve ser implementada no `agente-youtube` e apenas configurada ou especializada aqui.

## Isolamento de profile

Identidade visual, performance memory, reference style library, preferências editoriais e regras específicas do FDM360 não devem ser promovidas automaticamente para outros canais.
