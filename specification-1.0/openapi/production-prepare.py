#!/usr/bin/env python3
"""
Split an OpenAPI spec into modular files.
"""

import argparse
import json
from pathlib import Path
from urllib.request import urlopen

import yaml
import re

VERSION_RE = re.compile(r"^v\d+$")


def load_spec(source: str):
    """Load OpenAPI spec from URL or local file (JSON or YAML)."""
    if source.startswith(("http://", "https://", "file://")):
        with urlopen(source) as resp:
            data = resp.read().decode("utf-8")
    else:
        data = Path(source).read_text(encoding="utf-8")

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return yaml.safe_load(data)


def extract_group(path: str, api_version: str) -> str | None:
    """
    Extract group name from path.
    /api/v1/account/foo -> account
    /api/v1/status/bar  -> status
    """

    parts = path.strip("/").split("/")

    if len(parts) >= 3 and parts[0] == "api" and parts[1] == api_version and VERSION_RE.fullmatch(parts[1]):
        return parts[2]

    return None


def write_yaml(path: Path, data):
    """Write YAML with nice formatting."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def split_spec(spec: dict, outdir: Path, api_version: str):
    """ Split the spec into components, top info, and grouped paths. """
    outdir.mkdir(parents=True, exist_ok=True)

    if "components" in spec:
        write_yaml(outdir / "_components.yaml", {"components": spec["components"]})

    topinfo = {
        k: v
        for k, v in spec.items()
        if k not in ("paths", "components")
    }

    write_yaml(outdir / "_topinfo.yaml", topinfo)

    grouped_paths: dict[str, dict] = {}

    for path, item in spec.get("paths", {}).items():
        group = extract_group(path, api_version)
        if not group:
            group = "_misc"
        grouped_paths.setdefault(group, {})[path] = item

    for group, paths in grouped_paths.items():
        data = {
            "paths": paths
        }
        write_yaml(outdir / f"{group}.yaml", data)


def main():
    """ Main entry point for the split script. """
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="URL or local file containing the OpenAPI schema")
    parser.add_argument(
        "--outdir",
        default="production",
        help="Output directory",
    )
    parser.add_argument(
        "--api-version",
        default="v1",
        help="API version segment to split on, for example v1 or v2.",
    )

    args = parser.parse_args()
    spec = load_spec(args.source)
    split_spec(spec, Path(args.outdir), args.api_version)
    print(f"Split complete → {args.outdir}")


if __name__ == "__main__":
    main()
