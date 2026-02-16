#!/usr/bin/env python3
"""
Generate a diff between a new OpenAPI spec and a baseline
(graduated), then split into modular files.
"""

import argparse
import json
from pathlib import Path
from urllib.request import urlopen
import yaml

def load_spec(url: str):
    """ Load an OpenAPI spec from a URL, trying JSON first and falling back to YAML. """
    with urlopen(url) as resp:
        data = resp.read().decode("utf-8")

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return yaml.safe_load(data)


def load_yaml(path: Path):
    """ Load a YAML file, returning an empty dict if the file doesn't exist. """
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def extract_group(path: str) -> str | None:
    """ Extract a group name from the path, e.g. /api/v1/<group>/... """
    parts = path.strip("/").split("/")

    if len(parts) >= 3 and parts[0] == "api" and parts[1] == "v1":
        return parts[2]

    return None


def write_yaml(path: Path, data):
    """ Write data to a YAML file. """
    if not data:
        return

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def diff_paths(new_paths: dict, baseline_dir: Path):
    """ Compare new paths to baseline paths and return only the new ones. """
    baseline_paths = {}

    for file in baseline_dir.glob("*.yaml"):
        if file.name.startswith("_"):
            continue

        content = load_yaml(file)
        baseline_paths.update(content.get("paths", {}))

    diff = {}

    for path, item in new_paths.items():

        if path not in baseline_paths:
            diff[path] = item
            continue

        existing_methods = baseline_paths[path]

        new_methods = {
            m: v
            for m, v in item.items()
            if m not in existing_methods
        }

        if new_methods:
            diff[path] = new_methods

    return diff


def diff_components(new_components: dict, baseline_components: dict):
    """ Compare new components to baseline components and return only the new ones. """
    diff = {}

    for section, items in new_components.items():

        base_items = baseline_components.get(section, {})

        new_items = {
            k: v
            for k, v in items.items()
            if k not in base_items
        }

        if new_items:
            diff[section] = new_items

    return diff


def diff_topinfo(new_spec: dict, baseline_topinfo: dict):
    """ Compare top-level info (title, version, etc.) and return only the new/different fields. """
    diff = {}

    for k, v in new_spec.items():
        if k in ("paths", "components"):
            continue

        if k not in baseline_topinfo:
            diff[k] = v

    return diff


def split_paths(diff_paths: dict, outdir: Path):
    """ Split the diff paths into separate files based on their group. """
    grouped = {}

    for path, item in diff_paths.items():
        group = extract_group(path) or "_misc"
        grouped.setdefault(group, {})[path] = item

    for group, paths in grouped.items():
        write_yaml(outdir / f"{group}.yaml", {"paths": paths})


def main():
    """ Main entry point for the diff and split process. """
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--outdir", required=True)

    args = parser.parse_args()

    baseline_dir = Path(args.baseline)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    new_spec = load_spec(args.url)

    baseline_components = load_yaml(baseline_dir / "_components.yaml").get("components", {})
    baseline_topinfo = load_yaml(baseline_dir / "_topinfo.yaml")

    path_diff = diff_paths(new_spec.get("paths", {}), baseline_dir)
    component_diff = diff_components(new_spec.get("components", {}), baseline_components)
    topinfo_diff = diff_topinfo(new_spec, baseline_topinfo)

    write_yaml(outdir / "_components.yaml",
               {"components": component_diff} if component_diff else {})
    write_yaml(outdir / "_topinfo.yaml", topinfo_diff)

    split_paths(path_diff, outdir)

    print(f"Difference written to → {outdir}")

if __name__ == "__main__":
    main()

