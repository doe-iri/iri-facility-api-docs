# API Verification with Schemathesis + Pytest

This repository provides a **minimal, self-contained API verification harness** built on top of:

- **Schemathesis** for OpenAPI-driven test generation
- **Pytest** as the execution engine
- **pytest-html** for a portable HTML report

The goal is simple:  
**given an OpenAPI schema, automatically exercise all endpoints and validate that the API behaves sanely** — without writing hand-crafted tests.

This is intentionally lightweight and script-driven rather than a full test framework.

---

## What This Does

- Loads an OpenAPI schema (from a URL or a local file)
- Generates test cases for every operation defined in the schema
- Sends real HTTP requests to the API
- Validates responses against the OpenAPI contract
- Produces a single self-contained HTML report
- In addition to runtime API validation, the validator can perform a specification compliance check (see Compliance verification)

---

## Bootstrap

Create and populate a virtual environment:

```bash
./bootstrap.sh
```

This will:
- Create a `.venv` directory if missing
- Install all required dependencies from requirements.txt

Activate it manually with:

```bash
source .venv/bin/activate
```

## How to pass Auth token

Tool expects environment variable `IRI_API_TOKEN`, that will be used by Schemathesis `curl -H 'Authorization: Bearer <IRI_API_TOKEN>` ...

---

## Running the Validator

The validator is a **standalone Python script** that internally runs pytest.

### Default (local API)

```bash
python api-validator.py
```

Defaults:
- Base URL: `http://localhost:8000/`
- Schema URL: `http://localhost:8000/openapi.json`
- Report Name: `schemathesis-report`

---

### Custom Base URL

```bash
python api-validator.py --baseurl https://iri.example.org
```

This automatically resolves the schema as:
```
https://example.org/openapi.json
```

---

### Compliance verification

```bash
python api-validator.py --checkspeccompliance --official-schema ../specification/openapi/openapi_iri_facility_api_v1.yaml
```

The validator will do:

- Loads the official IRI OpenAPI spec (as file yaml/json)
- Fetches the facility’s live OpenAPI spec (localhost:8000)
- Compares operations by operationId
- Generate and print the report

Report states:

- **PASSED** - Operation exists in official and facility specs
- **FAILED** - Operation exists in official spec but is missing in facility spec
- **WARNING** - Operation exists in facility spec but not in official spec (extension, custom apis)

Example output:

```text
Found in facility spec:
-------------------------------------------------
spec_compliance::[GET /api/v1/account/capabilities] PASSED
spec_compliance::[GET /api/v1/account/capabilities/{capability_id}] PASSED
spec_compliance::[GET /api/v1/facility] PASSED
spec_compliance::[GET /api/v1/status/incidents/{incident_id}] PASSED
-------------------------------------------------

Not found in facility spec:
-------------------------------------------------
spec_compliance::[GET /api/v1/status/events/{event_id}] FAILED (missing operationId: getEvent)
spec_compliance::[GET /api/v1/status/events] FAILED (missing operationId: getEvents)
-------------------------------------------------

Extra operationIds in facility spec not found in official spec:
-------------------------------------------------
spec_compliance::[DELETE /api/v1/compute/cancel/{resource_id}/{job_id}] WARNING (extra operationId: cancelJob)
spec_compliance::[GET /api/v1/filesystem/checksum/{resource_id}] WARNING (extra operationId: checksum)
```

---

### Explicit Schema URL

```bash
python api-validator.py \
  --baseurl https://iri.example.org \
  --schema-url https://schemas.iri..example.org/openapi.json
```

---

### Local Schema File

```bash
python api-validator.py --schema-path ./openapi.json
```

Useful when validating an API against a local or in-progress schema.

---

### Custom Report Name

```bash
python api-validator.py --report-name custom-report-name
```

The report will produce two files:
* **self-contained HTML file** with ending `.html`.
* **XML file** with ending `.html`.

---

## What Is Being Checked

For each OpenAPI operation, Schemathesis automatically:
- Generates valid inputs based on Spec
- Generates invalid requests and methods not defined in Spec
- Sends HTTP requests
- Verifies response status codes and structure

---

## Header Sanitization (Remove non ansi characters)

Before each request, generated headers are sanitized to ensure:
- Header names are RFC-compliant tokens
- Header values are printable and safe

This keeps failures focused on **API behavior**, not HTTP encoding issues.
