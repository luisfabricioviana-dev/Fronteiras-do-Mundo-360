# FDM360 — v05 Production Gate Plan

## Principle
Do not advance audiovisual polish before geospatial truth is closed. Geo truth is a hard prerequisite, not a late QA step.

## P0 — Official geometry ingestion
For Brazil, Colombia, Peru and Ecuador, register only official vector sources. Each asset record must include:
- source_url
- source_date or retrieval_date
- native_crs
- raw_file_sha256
- normalized_crs = EPSG:4326
- normalized_geometry_sha256
- geometry_loaded

`geometry_loaded` may become `true` only after successful normalization and provenance capture.

## P0 — GEO_TRUTH_REFERENCE_BUNDLE
Required checks:
- CRS consistency
- geometry validity
- country containment
- border consistency
- Callao anchor
- Iquitos anchor
- entity ↔ geometry ↔ label_anchor binding
- regressions from v37, v03B and v04

Required result before render:
`PRE_RENDER_GEO_TRUTH = PASS`

Any pending critical geo issue keeps the pipeline in `BLOCK`.

## P0 — v05 recompilation
The v05 render must use only assets approved in the Geo Asset Registry.

Hard requirements:
- camera path derives from approved geometry
- country contours derive from the same approved geometry
- markers derive from approved anchors
- Callao and Iquitos use approved bundle anchors
- country markers must not visually imply military bases
- no lines between countries
- continuous camera motion for animated map sequences

## P0 — Post-render geospatial QA
QA must inspect the rendered MP4, not only source code or scene specifications.

Critical checkpoints:
- Colombia
- Ecuador
- Peru
- Callao
- Iquitos
- Brazil
- final synthesis

Intermediate camera states must also be inspected for pan/zoom drift of labels, contours and anchors.

Required result:
`POST_RENDER_GEO_TRUTH = PASS`

## P1 — Voice cast before enrichment
Run a short PT-BR voice cast with 2–3 candidate voices and score:
- intelligibility
- naturalness
- documentary identity

`PROXY_VOICE = HARD_BLOCK`

The visual must be recompiled around the selected final narration track.

## P1 — Controlled audiovisual enrichment
Only after final voice and Geo Truth PASS:
- 1–2 documentary inserts directly tied to claims
- semantic motion per country
- punctual SFX
- low music bed

No visual event is added merely to increase motion density. Each event must explain, prove or clarify something in the narration.

## P1 — Branding and mobile QA
Before final candidate:
- watermark/logo inside safe area
- approved FDM360 finish
- captions slightly higher in the frame
- small-screen legibility
- no UI collisions for Reels / Shorts / TikTok

## P0 final — FINAL_CANDIDATE_RENDER
Generate the final 1080×1920 master and calculate its exact SHA-256.

The exact final MP4 must pass:
- Geo QA
- Semantic QA
- Audio QA
- Rights / Provenance
- Mobile QA
- Profile Fit

Only the exact approved file hash may receive:
`PUBLICATION_READY = TRUE`

## Learning closure
After controlled publication, Performance Memory may ingest:
- scroll-stop
- retention
- completion
- rewatch
- other platform-available engagement signals

Performance evidence must be compared against the specific visual and editorial decisions used in that exact published render.

A single publication result remains a learning candidate; durable promotion requires recurrence, validation and regression.
