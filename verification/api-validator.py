#!/usr/bin/env python3
"""Schemathesis test script for the API."""
import os
import re
import json
import argparse
import schemathesis
import pytest

# ---------------------------------------------------------------------------
# Allow to pass tokens via environment variables
# ---------------------------------------------------------------------------
API_TOKEN = os.environ.get("IRI_API_TOKEN")

# ---------------------------------------------------------------------------
# Argument parsing (script-owned, not pytest)
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("--baseurl", help="Base URL of the API under test. Default: http://localhost:8000/")
parser.add_argument("--schema-url", help="URL to the OpenAPI schema. Cannot be used with --schema-path. Default: <baseurl>/openapi.json")
parser.add_argument("--schema-path", help="Path to the OpenAPI schema file. Cannot be used with --schema-url. Default: None")
parser.add_argument("--report-path", help="Path to output the HTML report. Default: schemathesis-report.html", default="schemathesis-report.html")

# parse_known_args so pytest flags are untouched
args, _ = parser.parse_known_args()

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
BASE_URL = args.baseurl or os.environ.get("BASE_URL") or "http://localhost:8000/"
SCHEMA_URL = None
SCHEMA_PATH = None
if args.schema_url and args.schema_path:
    raise ValueError("Cannot specify both --schema-url and --schema-path")
if args.schema_url:
    SCHEMA_URL = args.schema_url
if args.schema_path:
    SCHEMA_PATH = args.schema_path
if not args.schema_url and not args.schema_path:
    SCHEMA_URL = f"{BASE_URL}/openapi.json"

# ---------------------------------------------------------------------------
# Load schema BEFORE test definition
# ---------------------------------------------------------------------------
if SCHEMA_URL:
    print(f"Loading schema from URL: {SCHEMA_URL}")
    schema = schemathesis.openapi.from_url(SCHEMA_URL)
else:
    print(f"Loading schema from file: {SCHEMA_PATH}")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        raw_schema = json.load(f)
    schema = schemathesis.openapi.from_dict(raw_schema)

# ---------------------------------------------------------------------------
# Header sanitization (unchanged)
# ---------------------------------------------------------------------------
TOKEN = re.compile(r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$").fullmatch
VALUE = re.compile(r"^[\x20-\x7E\x80-\xFF]+$").fullmatch

@schemathesis.hook
def before_call(ctx, case, kwargs):
    headers = case.headers or {}
    clean = {}

    for k, v in headers.items():
        if not isinstance(k, str) or not TOKEN(k):
            continue
        if isinstance(v, str) and VALUE(v):
            clean[k] = v
        else:
            clean[k] = "X-Replaced"

    # ---- AUTH ----
    if API_TOKEN:
        clean["Authorization"] = f"Bearer {API_TOKEN}"

    case.headers = clean

# ---------------------------------------------------------------------------
# Test definition (unchanged)
# ---------------------------------------------------------------------------
@schema.parametrize()
def test_api(case):
    response = case.call(
        base_url=BASE_URL,
        timeout=60,
    )
    case.validate_response(
        response,
        excluded_checks=[
            schemathesis.checks.content_type_conformance,
            schemathesis.checks.response_schema_conformance,
            schemathesis.checks.unsupported_method,
        ],
    )

# ---------------------------------------------------------------------------
# Pytest runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pytest_args = [
        "-s",
        "-vv",
        "--maxfail=0",
        "--disable-warnings",
        "--continue-on-collection-errors",
        "--no-header", "--no-summary",
        "--html=" + args.report_path,
        "--self-contained-html",
        "--junitxml=schemathesis-report.xml",
        __file__,
    ]
    raise SystemExit(pytest.main(pytest_args))
