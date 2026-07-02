#!/usr/bin/env python3
""" Create a single OpenAPI spec from modular YAML files. """

import argparse
import yaml
from pathlib import Path
import os

BASE = Path(".")

OUTPUT_ALL = "all_spec.yaml"

ORDER = ["production", "beta", "in_development", "planned", "prototype", "retired"]


def collect_yaml_files(directory):
    """Collect all YAML files in a directory and its subdirectories."""
    files = []
    for root, _, filenames in os.walk(directory):
        for name in filenames:
            if name.endswith(".yaml") or name.endswith(".yml"):
                files.append(Path(root) / name)
    return sorted(files)


def deep_merge(target, source):
    """
    Merge source into target.
    Existing keys in target are never overridden.
    """
    for key, value in source.items():
        if key not in target:
            target[key] = value
            continue
        if isinstance(target[key], dict) and isinstance(value, dict):
            deep_merge(target[key], value)
        elif isinstance(target[key], list) and isinstance(value, list):
            target[key].extend(value)
        else:
            pass


def load_yaml_file(path):
    """Load YAML file and return its content as a dictionary."""
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_all(stage_dirs=None, output_path=OUTPUT_ALL):
    """Build the final OpenAPI spec by merging all modular YAML files."""
    result = {}

    ordered_dirs = stage_dirs or ORDER

    for stage in ordered_dirs:
        stage_dir = BASE / stage
        if not stage_dir.exists():
            continue

        for file in collect_yaml_files(stage_dir):
            data = load_yaml_file(file)
            deep_merge(result, data)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(result, f, sort_keys=False)

    print(f"created {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dirs",
        nargs="+",
        help="Explicit directories to merge in order. Defaults to the lifecycle stages.",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_ALL,
        help="Output OpenAPI YAML file path.",
    )
    args = parser.parse_args()

    build_all(stage_dirs=args.dirs, output_path=args.output)
