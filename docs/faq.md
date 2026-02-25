# FAQ

## General

### What is this?

K01's MCP server lets AI assistants generate and query synthetic health data through the Model Context Protocol. Instead of writing API calls by hand, you describe what you need in natural language and the AI handles the rest.

### Is any real patient data involved?

No. All data is fully synthetic, generated from published clinical statistics and pharmacological references. No real patient records are used in generation, training, or output.

### What FHIR versions are supported?

Both R4 and R5. All tools accept a `fhir_version` parameter. The key difference is that R4 uses `MedicationStatement` while R5 uses `MedicationUsage`.

### What locales are available?

Iceland (`is`), Denmark (`dk`), Norway (`no`), United States (`us`), and United Kingdom (`gb`). Icelandic patients automatically get kennitala identifiers and localized condition/medication names.

## Setup

### How do I get an API key?

Contact K01 at [k01.is](https://k01.is). Self-service key provisioning is coming soon.

### Which MCP clients work with this?

Any client that supports Streamable HTTP transport. This includes Claude Desktop, Cursor, and other MCP-compatible tools. See [authentication.md](authentication.md) for configuration examples.

### I added the config but don't see the tools

- Make sure you restarted the application after editing the config
- Check that the config file is valid JSON
- Verify your API key is correct
- Confirm you can reach `https://mcp.k01.is/mcp` from your network

### I get "Authentication Failed"

- Check that your API key is correct and hasn't expired
- Make sure the `Authorization` header includes the `Bearer ` prefix
- Contact K01 if you need a new key

## Usage

### Can I get reproducible results?

Yes. Pass a `seed` parameter to any tool that supports it. The same parameters + seed will always produce identical output. Note that cohort seeds and patient-level seeds are independent — the same patient can have different medications in different contexts.

### How many patients can I generate at once?

Up to 1,000 per call via `generate_synthetic_cohort`. For larger datasets, make multiple seeded calls.

### What ICD-10 codes can I use?

The system supports standard ICD-10 codes. Common examples:
- `E11.9` — Type 2 diabetes
- `I10` — Essential hypertension
- `J44.9` — COPD
- `F32.9` — Major depressive disorder
- `M54.5` — Low back pain

Multiple codes can be comma-separated: `"E11.9,I10"`.

### What's the difference between `generate_synthetic_cohort` and `search_patients`?

`generate_synthetic_cohort` creates new patients matching your criteria. `search_patients` generates a large deterministic pool and filters it — useful when you want to explore a population and find patients matching complex criteria.

## Privacy and Compliance

### Can the synthetic data be traced back to real patients?

No. The data is generated using statistical models built from aggregate clinical references, not individual patient records. Differential privacy mechanisms add noise to ensure generated distributions cannot be reversed.

### Can I use this data for regulatory submissions?

The synthetic data is intended for development, testing, and research. For regulatory contexts, consult with your compliance team about the specific use case.

### Is the data HIPAA/GDPR relevant?

Since no real patient data is involved, synthetic data from K01 does not constitute protected health information (PHI) under HIPAA or personal data under GDPR. However, consult your own legal and compliance teams for your specific use case.
