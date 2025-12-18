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
- Report: `schemathesis-report.html`

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

### Custom Report Path

```bash
python api-validator.py --report-path reports/api-report.html
```

The report is a **single self-contained HTML file**.

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
