#!/usr/bin/env python3
"""
Run full API validation suite for IRI facilities.
Outputs per-site artifacts into: output/<hostname>/
"""

import argparse
import subprocess
from pathlib import Path
from urllib.parse import urlparse
import sys

OUTPUT_DIR = Path(__file__).parent / "output"


def hostname_from_url(url: str) -> str:
    """ Convert a URL to a filesystem-friendly hostname string. """
    return urlparse(url).netloc.replace(":", "_")


def run_cmd(cmd, cwd=None):
    """ Run a command and print it. """
    print(" ".join(cmd))
    subprocess.run(cmd, check=False, cwd=cwd)


def run_for_site(site, official_schema, validator_script):
    """ Run all validation steps for a single site. """
    host = hostname_from_url(site)
    site_dir = OUTPUT_DIR / host
    site_dir.mkdir(parents=True, exist_ok=True)

    # 1. Local schema validation
    run_cmd([
        sys.executable, str(validator_script),
        "--baseurl", site,
        "--schema-url", f"{site.rstrip('/')}/openapi.json",
        "--report-name", str(site_dir / "local")
    ])

    # 2. Official schema validation
    run_cmd([
        sys.executable, str(validator_script),
        "--baseurl", site,
        "--schema-path", official_schema,
        "--report-name", str(site_dir / "official")
    ])

    # 3. Spec compliance
    run_cmd([
        sys.executable, str(validator_script),
        "--baseurl", site,
        "--checkspeccompliance",
        "--official-schema", official_schema,
        "--report-name", str(site_dir / "spec"),
        "--compliance-json", str(site_dir / "spec.compliance.json")
    ])


def main():
    """ Main entry point for the site validation script. """
    parser = argparse.ArgumentParser()
    parser.add_argument("--official-schema", required=True)
    parser.add_argument("--sites", nargs="+", required=True)

    parser.add_argument(
        "--validator-script",
        default=Path(__file__).parent / "api-validator.py",
        help="Path to api-validator.py (default: same directory as this script)"
    )

    args = parser.parse_args()

    validator_script = Path(args.validator_script).resolve()

    if not validator_script.exists():
        print(f"ERROR: validator script not found: {validator_script}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for site in args.sites:
        print(f"\n=== Running validation for {site} ===")
        run_for_site(site, args.official_schema, validator_script)


if __name__ == "__main__":
    main()