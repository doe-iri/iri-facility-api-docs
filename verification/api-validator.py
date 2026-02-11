#!/usr/bin/env python3
"""Schemathesis test script for the API."""
import os
import re
import json
import argparse
import warnings
import yaml
import schemathesis
import pytest
from hypothesis import settings, HealthCheck

# Allow to pass tokens via environment variables
API_TOKEN = os.environ.get("IRI_API_TOKEN")

# Argument parsing (script-owned, not pytest)
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("--baseurl", help="Base URL of the API under test. Default: http://localhost:8000/")
parser.add_argument("--schema-url", help="URL to the OpenAPI schema. Cannot be used with --schema-path. Default: <baseurl>/openapi.json")
parser.add_argument("--schema-path", help="Path to the OpenAPI schema file. Cannot be used with --schema-url. Default: None")
parser.add_argument("--report-name", help="Name of the HTML/XML report file. Default: schemathesis-report", default="schemathesis-report")
parser.add_argument("--checkspeccompliance", action="store_true", help="Check facility spec compliance against official spec (operationIds)")
parser.add_argument("--official-schema", help="Path or URL to the official OpenAPI schema")
parser.add_argument("--compliance-json", help="Write spec compliance details (present/missing/extra) to this JSON file")
parser.add_argument("--max-examples", type=int, help="Maximum number of examples per endpoint. Default: 20. Setting to 100 is aggressive")
parser.add_argument("--deadline", type=int, help="Deadline for each test in milliseconds. Default: None (no deadline)")
args, _ = parser.parse_known_args()


# Schemathesis settings for CI mode
settings.register_profile("ci",
                          max_examples=args.max_examples or 20,
                          deadline=args.deadline or None,
                          suppress_health_check=[HealthCheck.too_slow])
settings.load_profile("ci")


# Defaults
BASE_URL = args.baseurl or os.environ.get("BASE_URL") or "http://localhost:8000/"
SCHEMA_URL = None
SCHEMA_PATH = None
if args.schema_url and args.schema_path:
    raise ValueError("Cannot specify both --schema-url and --schema-path")
if args.schema_url:
    SCHEMA_URL = args.schema_url
if args.schema_path:
    SCHEMA_PATH = args.schema_path
if not args.schema_url and not args.schema_path and not args.checkspeccompliance:
    SCHEMA_URL = f"{BASE_URL}/openapi.json"

# Load schema BEFORE test definition
schema = None
if not args.checkspeccompliance:
    if SCHEMA_URL:
        print(f"Loading schema from URL: {SCHEMA_URL}")
        schema = schemathesis.openapi.from_url(SCHEMA_URL)
    else:
        print(f"Loading schema from file: {SCHEMA_PATH}")
        with open(SCHEMA_PATH, encoding="utf-8") as fd:
            try:
                raw_schema = json.load(fd)
            except json.JSONDecodeError as exc:
                print(f"Failed to parse JSON, trying YAML load: {exc}")
                fd.seek(0)
                raw_schema = yaml.safe_load(fd)
        schema = schemathesis.openapi.from_dict(raw_schema)

# Header sanitization
TOKEN = re.compile(r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$").fullmatch
VALUE = re.compile(r"^[\x20-\x7E\x80-\xFF]+$").fullmatch
SAFE_PATH_RE = re.compile(r"^[A-Za-z0-9._~-]+$")

def safeascii(value: str) -> str:
    return "".join(c if 32 <= ord(c) <= 126 else "-" for c in value)

@schemathesis.hook
def before_call(ctx, case, kwargs):
    headers = case.headers or {}
    clean = {"Accept": "application/json"}

    if case.path_parameters:
        for k, v in case.path_parameters.items():
            if isinstance(v, str) and not SAFE_PATH_RE.fullmatch(v):
                case.path_parameters[k] = "1"

    for k, v in headers.items():
        if not isinstance(k, str):
            continue

        safe_k = safeascii(k)

        if isinstance(v, str):
            safe_v = safeascii(v)
        else:
            safe_v = str(v)

        clean[safe_k] = safe_v

    # ---- AUTH ----
    if API_TOKEN:
        clean["Authorization"] = f"Bearer {API_TOKEN}"

    case.headers = clean

# Spec compliance helpers
def _load_schema(source):
    if source.startswith("http://") or source.startswith("https://"):
        return schemathesis.openapi.from_url(source).raw_schema
    with open(source, encoding="utf-8") as fd:
        try:
            return json.load(fd)
        except json.JSONDecodeError:
            fd.seek(0)
            return yaml.safe_load(fd)

def _extract_operation_ids(schema_dict):
    ops = {}
    for path, methods in schema_dict.get("paths", {}).items():
        for method, op in methods.items():
            opid = op.get("operationId")
            if opid:
                ops[opid] = (path, method)
    return ops

# Spec compliance test
@pytest.mark.skipif(not args.checkspeccompliance, reason="Compliance mode not enabled")
def test_spec_compliance():
    if not args.official_schema:
        pytest.fail("--official-schema must be provided with --checkspeccompliance")

    official_schema = _load_schema(args.official_schema)
    facility_schema = schemathesis.openapi.from_url(f"{BASE_URL}/openapi.json").raw_schema

    official_ops = _extract_operation_ids(official_schema)
    facility_ops = _extract_operation_ids(facility_schema)

    missing = sorted(set(official_ops) - set(facility_ops))
    extra = sorted(set(facility_ops) - set(official_ops))
    present = sorted(set(official_ops) & set(facility_ops))

    GREEN = "\033[1;92m"
    RED = "\033[1;91m"
    YELLOW = "\033[1;93m"
    RESET = "\033[0m"

    print("\n================ SPEC COMPLIANCE ================\n")

    # PASSED
    print("Found in facility spec:")
    print("-------------------------------------------------")
    for op in present:
        path, method = official_ops[op]
        print(f"spec_compliance::[{method.upper()} {path}] {GREEN}PASSED{RESET}")
    print("-------------------------------------------------\n")
    # FAILED
    print("Not found in facility spec:")
    print("-------------------------------------------------")
    for op in missing:
        path, method = official_ops[op]
        print(f"spec_compliance::[{method.upper()} {path}] {RED}FAILED{RESET} (missing operationId: {op})")
    print("-------------------------------------------------\n")

    # WARNINGS (extra endpoints)
    print("Extra operationIds in facility spec not found in official spec:")
    print("-------------------------------------------------")
    for op in extra:
        path, method = facility_ops[op]
        print(f"spec_compliance::[{method.upper()} {path}] {YELLOW}WARNING{RESET} (extra operationId: {op})")
        warnings.warn(f"Extra operationId in facility spec not in official spec: {op} ({method.upper()} {path})")
    print("-------------------------------------------------\n")

    print("\n=================================================\n")

    # Optional structured artifact for report aggregation
    if args.compliance_json:
        payload = {
            "base_url": BASE_URL,
            "official_schema": args.official_schema,
            "facility_schema_url": f"{BASE_URL}/openapi.json",
            "present": [
                {"operationId": op, "method": official_ops[op][1].upper(), "path": official_ops[op][0]}
                for op in present
            ],
            "missing": [
                {"operationId": op, "method": official_ops[op][1].upper(), "path": official_ops[op][0]}
                for op in missing
            ],
            "extra": [
                {"operationId": op, "method": facility_ops[op][1].upper(), "path": facility_ops[op][0]}
                for op in extra
            ],
            "counts": {
                "present": len(present),
                "missing": len(missing),
                "extra": len(extra),
            },
        }
        with open(args.compliance_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)

    if missing:
        pytest.fail(f"{len(missing)} official operationIds are missing from the facility spec")


# API validation test
if schema is None and not args.checkspeccompliance:
    raise ValueError("Schema could not be loaded for API validation tests")
if schema is not None:
    @pytest.mark.skipif(args.checkspeccompliance, reason="Running spec compliance mode only")
    @schema.parametrize()
    def test_api(case):
        """API validation test generated by Schemathesis."""
        response = case.call(
            base_url=BASE_URL,
            timeout=60
        )
        case.validate_response(
            response,
            excluded_checks=[
                schemathesis.checks.content_type_conformance,
                schemathesis.checks.unsupported_method
            ],
        )
else:
    @pytest.mark.skip(reason="Schemathesis disabled in spec compliance mode")
    def test_api():
        """Dummy test when schemathesis is disabled."""
        pass

# Pytest runner
if __name__ == "__main__":
    pytest_args = [
        "-s",
        "-v",
        "--tb=no",
        "--maxfail=0",
        "--disable-warnings",
        "--continue-on-collection-errors",
        "--no-header", "--no-summary",
        "--html=" + args.report_name + ".html",
        "--self-contained-html",
        "--junitxml=" + args.report_name + ".xml",
        __file__,
    ]
    raise SystemExit(pytest.main(pytest_args))
