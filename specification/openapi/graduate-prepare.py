#!/usr/bin/env python3
"""
Split an OpenAPI spec into modular files.
"""

import argparse
import json
from pathlib import Path
from urllib.request import urlopen

import yaml

def load_spec(url: str):
    """Load OpenAPI spec from URL (JSON or YAML)."""
    with urlopen(url) as resp:
        data = resp.read().decode("utf-8")

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return yaml.safe_load(data)


def extract_group(path: str) -> str | None:
    """
    Extract group name from path.
    /api/v1/account/foo -> account
    /api/v1/status/bar  -> status
    """

    parts = path.strip("/").split("/")

    if len(parts) >= 3 and parts[0] == "api" and parts[1] == "v1":
        return parts[2]

    return None


def write_yaml(path: Path, data):
    """Write YAML with nice formatting."""
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def split_spec(spec: dict, outdir: Path):
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
        group = extract_group(path)
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
    parser.add_argument("url", help="URL to openapi.json")
    parser.add_argument(
        "--outdir",
        default="graduated",
        help="Output directory",
    )

    args = parser.parse_args()
    spec = load_spec(args.url)
    split_spec(spec, Path(args.outdir))
    print(f"Split complete → {args.outdir}")


if __name__ == "__main__":
    main()

