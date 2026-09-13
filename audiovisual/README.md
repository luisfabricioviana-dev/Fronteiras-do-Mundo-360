# Audiovisual — FDM360

Camada de regras audiovisuais específicas do Fronteiras do Mundo 360.

## Escopo

- Scene rules específicas do canal
- Camera-Meaning Integrity aplicado ao FDM360
- regras de captions e safe area
- Audio Cue Map específico por vídeo/perfil
- pós-render semântico aplicado ao canal
- critérios de aprovação visual do profile

## Dependências compartilhadas

Capacidades genéricas como `POST_RENDER_SEMANTIC_INTEGRITY`, `Render Observation Adapter`, `SEMANTIC_BINDING_INTEGRITY_v1`, `Camera-Meaning Integrity` e `Iconography Truth Gate` devem viver no `agente-youtube`; este repositório deve conter apenas configuração, especialização, fixtures e regressões FDM360.
