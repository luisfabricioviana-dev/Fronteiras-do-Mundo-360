# FDM360 Reference Style Library

Biblioteca versionada das referências audiovisuais específicas do perfil Fronteiras do Mundo 360.

Governança:
- toda nova referência entra como `REFERENCE_ONLY`;
- uma referência isolada não altera automaticamente a identidade do canal;
- um novo vídeo não cria regra permanente por si só;
- cross-channel style contamination é bloqueada;
- metadados ausentes permanecem ausentes, sem preenchimento por inferência;
- referências só podem ser promovidas após validação explícita e regressão quando aplicável.

## Reference Learning Registry

Escopo: `PROFILE_SPECIFIC`.

Regras de aprendizagem:
- sinais ausentes não podem ser inferidos;
- referências `UNRECOVERED` não entram no denominador de frequência;
- caminho de promoção: `OBSERVED -> CANDIDATE -> VALIDATED -> PROMOTED`;
- nenhum aprendizado deste registry promove automaticamente identidade do canal.

Base de evidência atual:
- `FDM360_REF_STYLE_001`: possui sinais visuais/narrativos e hard locks recuperados;
- `FDM360_REF_STYLE_002`: provenance parcial, sem sinais de estilo recuperados;
- `FDM360_REF_STYLE_015`: possui metadados técnicos recuperados;
- `FDM360_REF_STYLE_003` a `014`: `UNRECOVERED`.

Aprendizados observados/candidatos:
- `REF_LEARN_001` — `continuous_satellite_map` — `OBSERVED` — evidência: `REF_STYLE_001`;
- `REF_LEARN_002` — `semantic_camera_motion` — `OBSERVED` — evidência: `REF_STYLE_001`;
- `REF_LEARN_003` — `documentary_evidence + return_to_map` — `OBSERVED` — evidência: `REF_STYLE_001`;
- `REF_LEARN_004` — `persistent_geo_labels` — `OBSERVED` — evidência: `REF_STYLE_001`;
- `REF_LEARN_005` — `vertical 720x1280 at 30 fps` — `CANDIDATE` — evidência: `REF_STYLE_001` + `REF_STYLE_015`;
- `REF_LEARN_006` — `integrated loudness near -14 LUFS` — `CANDIDATE` — evidência: `REF_STYLE_001` + `REF_STYLE_015`.

Targets possíveis após validação:
- `STYLE_MEMORY_CANDIDATE`;
- `NARRATIVE_PATTERN_CANDIDATE`;
- `PRODUCTION_CONVENTION_CANDIDATE`;
- `AUDIO_CONVENTION_CANDIDATE`.
