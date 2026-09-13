# v05.1 — Post-Render Geo Truth QA

Status: `POST_RENDER_GEO_TRUTH = PASS`

Scope: geo-only visual master; this is not a publication-ready master.

## Render identity

- file: `FDM360_US_PRESENCE_v05_1_GEO_MASTER_1080x1920.mp4`
- SHA-256: `eb508e4f0bb74fc1c0cd16a7afbc0a7c5b40a88c58aa8a07787bdeccff1f3066`
- duration: 30.0 s
- raster: 1080x1920
- codec: H.264
- frame rate: 30 fps
- audio: none

## Geo provenance

The render was generated from the approved `GEO_TRUTH_REFERENCE_BUNDLE_v05` normalized geometries in EPSG:4326 and the verified IGN/IDEP anchors for Callao and Iquitos.

Approved pre-render bundle evidence:
- workflow run: `34774202581`
- artifact id: `10322718276`
- artifact digest: `sha256:83ad29718259efdba20308e55e5c7fcacf95bba4dcde8886c78ae707e15d32ff`
- `PRE_RENDER_GEO_TRUTH = PASS`

## Observed MP4 QA

Critical and transition frames were extracted from the encoded MP4, including overview, Colombia, Ecuador, Peru, Callao, Iquitos, Brazil and final synthesis, with additional samples across the Callao -> Iquitos -> Brazil camera transitions.

Checks:
- country outlines remain bound to the same normalized geometry throughout camera movement: PASS;
- country labels remain geographically bound during pan/zoom: PASS;
- Callao marker uses the verified Callao anchor: PASS;
- Iquitos marker uses the verified Iquitos anchor: PASS;
- no country is represented by a point marker resembling a military base: PASS;
- no line connects countries: PASS;
- map remains one continuous spatial scene: PASS;
- camera target and caption change together after v05 -> v05.1 semantic-sync repair: PASS;
- final synthesis preserves the editorial lock that the evidence does not prove a plan to surround Brazil: PASS.

## Regression found and repaired

The first v05 render was blocked because during one transition the visual target had already changed to Iquitos while the caption still read Callao. v05.1 synchronizes target selection and caption selection on the same temporal transition boundary. The repaired MP4 was re-observed at intermediate timestamps.

## Gate result

`POST_RENDER_GEO_TRUTH = PASS` applies only to the exact SHA-256 above.

Remaining publication blocks:
- final PT-BR voice not selected/rendered;
- `PROXY VOICE = HARD BLOCK` remains in force;
- audio QA not run;
- rights/provenance QA for documentary inserts not run;
- final mobile/branding QA not run;
- final master hash not approved.

Therefore: `PUBLICATION_READY = FALSE`.
