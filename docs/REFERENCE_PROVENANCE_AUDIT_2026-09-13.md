# FDM360 — Reference Provenance Audit — 2026-09-13

## Scope

Audit of `FDM360_REF_STYLE_003` through `FDM360_REF_STYLE_014`.

## Result

No explicit prior record was recovered for these IDs with enough evidence to restore canonical names, source files/URLs, technical metadata, style fingerprints or hard locks.

The available project history confirmed only the channel-level governance and visual rules already represented elsewhere in this repository. Those general rules must not be backfilled into individual reference records as if they were source-specific observations.

## Decision

Keep `FDM360_REF_STYLE_003` through `FDM360_REF_STYLE_014` as:

- `status: REFERENCE_ONLY`
- `provenance_status: UNRECOVERED`

Do not fabricate names, sources, metrics or fingerprints.

## Recovery rule

A reference may leave `UNRECOVERED` only when at least one explicit source is recovered, such as:

1. original video/file or URL;
2. prior analysis with unambiguous reference ID mapping;
3. prior canonical registry entry with source-specific metadata.

Any recovered record must preserve profile isolation and must not promote a single reference into channel identity automatically.
