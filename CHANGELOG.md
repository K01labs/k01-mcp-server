# Changelog

## 1.7.1 — 2025-02-25

Initial public release of the K01 MCP server registry listing.

### Tools

- `generate_synthetic_cohort` — Generate synthetic patient cohorts with demographic and clinical constraints
- `search_patients` — Search virtual patient database with advanced healthcare filters
- `get_patient_record` — Retrieve complete patient record with clinical summaries
- `get_patient_medications` — Get detailed medication records with ATC codes
- `get_patient_conditions` — Retrieve patient conditions with ICD-10 codes
- `compare_fhir_versions` — Compare patient data across FHIR R4 and R5

### Features

- FHIR R4 and R5 dual version support
- Deterministic seed-based reproducibility
- Icelandic localization (kennitala, condition names, therapeutic indications)
- Multi-locale support (IS, DK, NO, US, GB)
- Edge case generation for boundary testing
