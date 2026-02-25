# Tool Reference

Complete parameter documentation for all K01 MCP server tools.

## generate_synthetic_cohort

Generate synthetic patient cohorts with demographic and clinical constraints. Returns a FHIR Bundle containing Patient, Condition, MedicationStatement, Procedure, and Observation resources.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `count` | integer | `1` | Number of patients to generate (1-1000) |
| `age_min` | integer | — | Minimum patient age (0-120) |
| `age_max` | integer | — | Maximum patient age (0-120) |
| `gender` | string | — | Patient gender: `male`, `female`, `other`, `unknown` |
| `condition` | string | — | Required ICD-10 codes, comma-separated (e.g., `"E11.9,I10"`) |
| `seed` | integer | — | Random seed for reproducible results |
| `forceEdgeCases` | boolean | — | Generate edge case patients for boundary testing |
| `numberOfConditionTypesFrom` | integer | — | Minimum number of condition types (use with `forceEdgeCases`) |
| `numberOfConditionTypesTo` | integer | — | Maximum number of condition types (use with `forceEdgeCases`) |
| `locale` | string | — | Patient locale: `is` (Iceland), `dk` (Denmark), `no` (Norway), `us` (USA), `gb` (UK) |
| `managingOrganization` | string | — | Managing organization code in `RAxx-xxxx` format |
| `fhir_version` | string | `"R4"` | FHIR version: `R4` or `R5` |

### Returns

```json
{
  "fhir_bundle": { "resourceType": "Bundle", "type": "collection", "entry": [...] },
  "patient_count": 50,
  "seed_used": 42
}
```

### Examples

```
# 50 diabetic patients aged 40-60
generate_synthetic_cohort(count=50, age_min=40, age_max=60, condition="E11.9")

# 10 patients with COPD and hypertension, Danish locale
generate_synthetic_cohort(count=10, condition="J44.9,I10", locale="dk")

# Edge case patients with exactly 1 condition type
generate_synthetic_cohort(count=5, forceEdgeCases=true, numberOfConditionTypesFrom=1, numberOfConditionTypesTo=1)
```

---

## search_patients

Search a virtual patient database with advanced healthcare filters. Generates a deterministic patient pool and filters by demographics, medication counts, condition types, and clinical complexity.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `count` | integer | `10` | Maximum results to return |
| `total` | integer | `1000` | Size of the virtual patient pool |
| `gender` | string | — | Gender filter: `male`, `female`, `other`, `unknown` |
| `birthdate` | string | — | Birth date filter with HL7 prefix (e.g., `"ge1980-01-01"`, `"le1990-12-31"`) |
| `numberOfMedicines` | integer | — | Exact medication count |
| `numberOfMedicinesFrom` | integer | — | Minimum medication count |
| `numberOfMedicinesTo` | integer | — | Maximum medication count |
| `numberOfConditions` | integer | — | Minimum condition count |
| `numberOfConditionTypesFrom` | integer | — | Minimum distinct condition types |
| `numberOfConditionTypesTo` | integer | — | Maximum distinct condition types |
| `conditionTypes` | string | — | Filter by chronicity: `chronic`, `acute`, `unknown` |
| `forceEdgeCases` | boolean | — | Generate edge case patients |
| `locale` | string | — | Locale: `is` or `en` |
| `managingOrganization` | string | — | Managing organization code in `RAxx-xxxx` format |
| `fhir_version` | string | `"R4"` | FHIR version: `R4` or `R5` |

### Returns

```json
{
  "fhir_bundle": { "resourceType": "Bundle", "type": "searchset", "total": 150, "entry": [...] },
  "total_matches": 150,
  "returned_count": 10
}
```

### Examples

```
# Female patients with chronic conditions
search_patients(gender="female", conditionTypes="chronic")

# Patients born 1980-1990 with 2-4 medications
search_patients(birthdate="ge1980-01-01", numberOfMedicinesFrom=2, numberOfMedicinesTo=4)

# Complex patients from a large pool
search_patients(total=5000, numberOfConditions=3, count=20)
```

---

## get_patient_record

Retrieve a complete patient record with demographic data and clinical summaries. Returns a FHIR Patient resource with extensions containing medication and condition summary counts.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `patient_id` | string | **required** | Patient ID or kennitala (10-digit Icelandic national ID) |
| `fhir_version` | string | `"R4"` | FHIR version: `R4` or `R5` |

### Returns

```json
{
  "fhir_resource": { "resourceType": "Patient", "id": "0101302989", ... },
  "patient_id": "0101302989",
  "medication_summary": { "url": "...", "extension": [...] },
  "condition_summary": { "url": "...", "extension": [...] }
}
```

The summary extensions include:
- **Medication summary**: total count, counts by category (permanent, as_needed, course, institutional)
- **Condition summary**: total count, counts by type (chronic, acute, unknown)

### Examples

```
# Get patient record
get_patient_record(patient_id="0101302989")

# Get patient record in R5 format
get_patient_record(patient_id="0101302989", fhir_version="R5")
```

---

## get_patient_medications

Get detailed medication records for a patient. Returns MedicationStatement (R4) or MedicationUsage (R5) resources with ATC codes, therapeutic indications, and dosage information.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `patient_id` | string | **required** | Patient ID or kennitala |
| `seed` | integer | — | Random seed for reproducible results |
| `fhir_version` | string | `"R4"` | FHIR version: `R4` or `R5` |

### Returns

```json
{
  "fhir_bundle": { "resourceType": "Bundle", "entry": [...] },
  "medication_count": 3,
  "fhir_version": "R4",
  "resource_type": "MedicationStatement",
  "seed_used": 12345
}
```

Each medication resource includes:
- ATC codes with localized display names
- Therapeutic indications (localized for Icelandic patients)
- Dosage instructions and routes
- Internal categorization (permanent, as_needed, course, institutional)

### Examples

```
# Get medications for a patient
get_patient_medications(patient_id="0101302989")

# Reproducible medication list
get_patient_medications(patient_id="0101302989", seed=12345)

# R5 format (returns MedicationUsage instead of MedicationStatement)
get_patient_medications(patient_id="0101302989", fhir_version="R5")
```

---

## get_patient_conditions

Retrieve all conditions (diagnoses) for a patient. Returns Condition resources with ICD-10 codes, clinical status, and localized names.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `patient_id` | string | **required** | Patient ID or kennitala |
| `seed` | integer | — | Random seed for reproducible results |
| `fhir_version` | string | `"R4"` | FHIR version: `R4` or `R5` |

### Returns

```json
{
  "fhir_bundle": { "resourceType": "Bundle", "entry": [...] },
  "condition_count": 2,
  "seed_used": 12345
}
```

Each condition resource includes:
- ICD-10 codes
- Clinical status (active, resolved, etc.)
- Verification status
- Onset dates
- Localized condition names for Icelandic patients

### Examples

```
# Get conditions for a patient
get_patient_conditions(patient_id="0101302989")

# Reproducible conditions
get_patient_conditions(patient_id="0101302989", seed=12345)
```

---

## compare_fhir_versions

Compare the same patient data across FHIR R4 and R5 versions. Useful for understanding version differences and planning migrations.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `patient_id` | string | **required** | Patient ID or kennitala |
| `resource_type` | string | `"Patient"` | Resource to compare: `Patient`, `Medication`, or `Condition` |

### Returns

```json
{
  "patient_id": "0101302989",
  "resource_type": "Medication",
  "r4_data": { ... },
  "r5_data": { ... },
  "key_differences": [
    "R4 uses 'MedicationStatement', R5 uses 'MedicationUsage'",
    "Resource structure and status codes may differ"
  ]
}
```

### Key Differences by Resource Type

| Resource | R4 | R5 |
|----------|-----|-----|
| Medications | `MedicationStatement` | `MedicationUsage` |
| Status codes | Standard | Enhanced |
| Patient | Same structure | Same structure |

### Examples

```
# Compare patient record across versions
compare_fhir_versions(patient_id="0101302989", resource_type="Patient")

# Compare medication representation
compare_fhir_versions(patient_id="0101302989", resource_type="Medication")

# Compare condition resources
compare_fhir_versions(patient_id="0101302989", resource_type="Condition")
```
