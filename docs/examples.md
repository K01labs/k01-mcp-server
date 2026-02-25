# Usage Examples

Practical workflows showing how to use K01's MCP tools in real scenarios.

## Research Cohort Design

### Generate a diabetes study cohort

```
You: Generate 200 patients aged 40-70 with Type 2 diabetes for a medication adherence study.

Claude: [Uses generate_synthetic_cohort]
        count=200, age_min=40, age_max=70, condition="E11.9", seed=42

Generated 200 patients. The cohort includes:
- 200 Patient resources with demographics
- 200+ Condition resources (E11.9 plus comorbidities)
- MedicationStatement resources (antidiabetics, statins, antihypertensives)
- Procedure and Observation resources
```

### Build a multi-morbidity cohort

```
You: I need elderly patients with both COPD and hypertension.

Claude: [Uses generate_synthetic_cohort]
        count=50, age_min=65, condition="J44.9,I10"

Generated 50 patients aged 65+ with both J44.9 (COPD) and I10 (hypertension),
plus clinically correlated comorbidities and medications.
```

## Patient-Level Analysis

### Explore a patient's full record

```
You: Show me everything about patient 0101302989.

Claude: [Uses get_patient_record]
        patient_id="0101302989"

This is a 35-year-old male patient with:
- 4 active medications (2 permanent, 1 as-needed, 1 course)
- 3 conditions (2 chronic, 1 acute)

You: What medications are they taking?

Claude: [Uses get_patient_medications]
        patient_id="0101302989"

3 active medications:
1. Metformin 500mg (ATC: A10BA02) — for Sykursýki tegund 2
2. Lisinopril 10mg (ATC: C09AA03) — for Háþrýstingur
3. Ibuprofen 400mg (ATC: M01AE01) — as needed
```

### Get reproducible results for testing

```
You: Generate medications for patient 0101302989 with seed 100, then do it again.

Claude: [Uses get_patient_medications twice with seed=100]

Both calls return identical results — same medications, same ATC codes,
same dosages. Useful for integration tests and regression suites.
```

## FHIR Version Comparison

### Compare R4 vs R5 medication representation

```
You: How do medications look in R4 vs R5 for patient 0101302989?

Claude: [Uses compare_fhir_versions]
        patient_id="0101302989", resource_type="Medication"

Key differences:
- R4 uses "MedicationStatement", R5 uses "MedicationUsage"
- Status codes differ between versions
- R5 includes enhanced metadata fields
```

## Filtering and Search

### Find patients by clinical complexity

```
You: Find patients with at least 3 medications and chronic conditions.

Claude: [Uses search_patients]
        numberOfMedicinesFrom=3, conditionTypes="chronic", _count=15

Found 150 matching patients in the pool, returning first 15.
These patients have complex medication regimens and at least one chronic condition.
```

### Age-based cohort search

```
You: Show me young adult patients born between 1990 and 2000.

Claude: [Uses search_patients]
        birthdate="ge1990-01-01", birthdate="le2000-12-31", _count=20

Found 120 patients in the specified age range.
```

## Edge Case Testing

### Generate boundary condition patients

```
You: I need patients with exactly 1 condition type for testing our minimum-data path.

Claude: [Uses generate_synthetic_cohort]
        count=10, forceEdgeCases=true, numberOfConditionTypesFrom=1, numberOfConditionTypesTo=1

Generated 10 patients, each with exactly 1 condition type.
Useful for testing systems that handle minimal clinical data.
```

## Multi-Locale Generation

### Generate Icelandic patients

```
You: Generate 20 Icelandic patients with hypertension.

Claude: [Uses generate_synthetic_cohort]
        count=20, condition="I10", locale="is"

Generated 20 patients with:
- Icelandic kennitala identifiers
- Condition names in Icelandic (Háþrýstingur)
- Therapeutic indications in Icelandic
- Icelandic demographic data
```

### Generate Danish patients

```
You: Create 10 patients for our Danish deployment test.

Claude: [Uses generate_synthetic_cohort]
        count=10, locale="dk"

Generated 10 patients with Danish demographics and locale-specific data.
```
