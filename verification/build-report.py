#!/usr/bin/env python3
"""
Build a report from validation outputs.
"""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import yaml

OUTPUT_DIR = Path(__file__).parent / "output"
REPORT_FILE = OUTPUT_DIR / "full-report.md"


def load_official_operations(schema_path):
    """Load official operations from the OpenAPI schema."""
    with open(schema_path, encoding="utf-8") as fd:
        try:
            schema = json.load(fd)
        except json.JSONDecodeError:
            fd.seek(0)
            schema = yaml.safe_load(fd)

    ops = set()
    for path, methods in schema.get("paths", {}).items():
        for method in methods:
            ops.add(f"{method.upper()} {path}")
    return ops


def parse_junit(xml_file):
    """ Parse JUnit XML results and return a mapping of operationId to PASS/FAIL status. """
    results = {}
    if not xml_file.exists():
        return results

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for testcase in root.iter("testcase"):
        name = testcase.attrib.get("name", "")
        if "[" in name and "]" in name:
            op = name.split("[", 1)[1].rsplit("]", 1)[0]
        else:
            continue

        if testcase.find("failure") is not None:
            results[op] = "FAIL"
        else:
            results[op] = "PASS"

    return results


def parse_spec_json(json_file):
    """Parse spec compliance JSON results."""
    if not json_file.exists():
        return {"present": [], "missing": [], "extra": []}
    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


def badge(status: str):
    """Return a markdown badge for the given status."""
    mapping = {
        "PASS": "badge-pass",
        "FAIL": "badge-fail",
        "MISSING": "badge-missing",
        "EXTRA": "badge-extra",
        "EXTRA-PASS": "badge-extra-pass",
        "EXTRA-FAIL": "badge-extra-fail",
    }
    return f"![][{mapping.get(status, '')}]" if status in mapping else status


def main():
    """Main function to build the report."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--official-schema", required=True)
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    official_ops = load_official_operations(args.official_schema)
    sites = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]

    local_results = {}
    official_results = {}
    spec_results = {}
    missing_ops = {}
    extra_ops_all = {}

    for site_dir in sites:
        host = site_dir.name
        local_results[host] = parse_junit(site_dir / "local.xml")
        official_results[host] = parse_junit(site_dir / "official.xml")
        spec_results[host] = parse_spec_json(site_dir / "spec.compliance.json")
        missing_ops[site_dir.name] = {f"{item['method']} {item['path']}" for item in spec_results[host].get("missing", [])}
        extra_ops_all[site_dir.name] = {f"{item['method']} {item['path']}" for item in spec_results[site_dir.name].get("extra", [])}


    lines = []

    def write(line=""):
        """Write a line to the report."""
        print(line)
        lines.append(line)

    # Header
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    write("# API Endpoints Report\n")
    write(f"**Generated at:** {now}\n")
    write(f"**Sites tested:** {', '.join(s.name for s in sites)}\n")
    write(f"**Official endpoints defined in spec:** {len(official_ops)}\n")
    write("")

    headers = ["operationId"] + [s.name for s in sites]

    # 1. Spec Compliance
    write("## Spec Compliance (OperationId and API available at site from official spec)\n")
    write("| " + " | ".join(headers) + " |")
    write("|" + "|".join(["---"] * len(headers)) + "|")

    for op in sorted(official_ops):
        row = [op]
        for site in sites:
            host = site.name
            extra_ops = {f"{item['method']} {item['path']}" for item in spec_results[host].get("extra", [])}

            if op in missing_ops[host]:
                status = "MISSING"
            elif op in extra_ops:
                status = "EXTRA"
            else:
                status = "PASS"

            row.append(badge(status))
        write("| " + " | ".join(row) + " |")

    write("\n## Official Spec Schemathesis Test\n")
    write("| " + " | ".join(headers) + " |")
    write("|" + "|".join(["---"] * len(headers)) + "|")

    for op in sorted(official_ops):
        row = [op]
        for site in sites:
            host = site.name
            if op in missing_ops[host]:
                status = "MISSING"
            else:
                status = official_results[host].get(op, "MISSING")

            row.append(badge(status))


        write("| " + " | ".join(row) + " |")

    # 3. Local Behavioral
    all_local_ops = set()
    for results in local_results.values():
        all_local_ops |= set(results)


    write("\n## Local Site Schemathesis Test\n")
    write(f"\n**Total endpoints discovered across local schemas:** {len(all_local_ops)}\n")

    write("| " + " | ".join(headers) + " |")
    write("|" + "|".join(["---"] * len(headers)) + "|")

    for op in sorted(all_local_ops):
        row = [op]

        for site in sites:
            host = site.name
            local_status = local_results[host].get(op)

            extras = extra_ops_all.get(host, set())
            missing = missing_ops.get(host, set())

            if op in extras:
                if local_status == "PASS":
                    status = "EXTRA-PASS"
                elif local_status == "FAIL":
                    status = "EXTRA-FAIL"
                else:
                    status = "EXTRA"

            elif op in missing:
                status = "MISSING"

            else:
                status = local_status if local_status else "—"

            row.append(badge(status))

        write("| " + " | ".join(row) + " |")

    write("\n---\n")
    write("<!-- Badge references -->")
    write("[badge-pass]: https://img.shields.io/badge/PASS-brightgreen")
    write("[badge-fail]: https://img.shields.io/badge/FAIL-red")
    write("[badge-missing]: https://img.shields.io/badge/MISSING-red")
    write("[badge-extra]: https://img.shields.io/badge/EXTRA-orange")
    write("[badge-extra-pass]: https://img.shields.io/badge/EXTRA--PASS-blue")
    write("[badge-extra-fail]: https://img.shields.io/badge/EXTRA--FAIL-purple")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
