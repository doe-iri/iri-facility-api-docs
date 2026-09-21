#!/usr/bin/env python3
"""Validate the adopted DOE-IRI operation-relation OpenAPI bindings.

The mapping below is a regression assertion for the approved Phase 1 package.
It does not register relations or replace the relation registry, profiles, or
OpenAPI documents as the authorities for their respective concerns.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

import yaml


OPENAPI_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = OPENAPI_DIR.parents[1]
PRODUCTION_DIR = OPENAPI_DIR / "production"
GENERATED_SPEC = OPENAPI_DIR / "all_spec_v2.yaml"
RELATION_DIR = REPOSITORY_ROOT / "registry" / "relations"
RELATION_INDEX = RELATION_DIR / "README.md"

CANONICAL_PREFIX = "https://iri.science/rels/"
HTTP_METHODS = {
    "get",
    "put",
    "post",
    "delete",
    "options",
    "head",
    "patch",
    "trace",
}

# Canonical relation URI -> (path, method, operationId).
EXPECTED_BINDINGS = {
    f"{CANONICAL_PREFIX}submit-job": (
        "/api/v2/compute/job/{resource_id}",
        "post",
        "launchJob",
    ),
    f"{CANONICAL_PREFIX}update-job": (
        "/api/v2/compute/job/{resource_id}/{job_id}",
        "put",
        "updateJob",
    ),
    f"{CANONICAL_PREFIX}get-job": (
        "/api/v2/compute/status/{resource_id}/{job_id}",
        "get",
        "getJob",
    ),
    f"{CANONICAL_PREFIX}query-jobs": (
        "/api/v2/compute/status/{resource_id}",
        "post",
        "getJobs",
    ),
    f"{CANONICAL_PREFIX}cancel-job": (
        "/api/v2/compute/cancel/{resource_id}/{job_id}",
        "delete",
        "cancelJob",
    ),
    f"{CANONICAL_PREFIX}change-file-mode": (
        "/api/v2/filesystem/chmod/{resource_id}",
        "post",
        "chmod",
    ),
    f"{CANONICAL_PREFIX}change-file-owner": (
        "/api/v2/filesystem/chown/{resource_id}",
        "post",
        "chown",
    ),
    f"{CANONICAL_PREFIX}identify-file": (
        "/api/v2/filesystem/file/{resource_id}",
        "post",
        "file",
    ),
    f"{CANONICAL_PREFIX}stat-file": (
        "/api/v2/filesystem/stat/{resource_id}",
        "post",
        "stat",
    ),
    f"{CANONICAL_PREFIX}create-directory": (
        "/api/v2/filesystem/mkdir/{resource_id}",
        "post",
        "mkdir",
    ),
    f"{CANONICAL_PREFIX}create-symlink": (
        "/api/v2/filesystem/symlink/{resource_id}",
        "post",
        "symlink",
    ),
    f"{CANONICAL_PREFIX}list-directory": (
        "/api/v2/filesystem/ls/{resource_id}",
        "post",
        "ls",
    ),
    f"{CANONICAL_PREFIX}read-file-head": (
        "/api/v2/filesystem/head/{resource_id}",
        "post",
        "head",
    ),
    f"{CANONICAL_PREFIX}view-file": (
        "/api/v2/filesystem/view/{resource_id}",
        "post",
        "view",
    ),
    f"{CANONICAL_PREFIX}read-file-tail": (
        "/api/v2/filesystem/tail/{resource_id}",
        "post",
        "tail",
    ),
    f"{CANONICAL_PREFIX}checksum-file": (
        "/api/v2/filesystem/checksum/{resource_id}",
        "post",
        "checksum",
    ),
    f"{CANONICAL_PREFIX}remove-path": (
        "/api/v2/filesystem/rm/{resource_id}",
        "post",
        "rm",
    ),
    f"{CANONICAL_PREFIX}compress-paths": (
        "/api/v2/filesystem/compress/{resource_id}",
        "post",
        "compress",
    ),
    f"{CANONICAL_PREFIX}extract-archive": (
        "/api/v2/filesystem/extract/{resource_id}",
        "post",
        "extract",
    ),
    f"{CANONICAL_PREFIX}move-path": (
        "/api/v2/filesystem/mv/{resource_id}",
        "post",
        "mv",
    ),
    f"{CANONICAL_PREFIX}copy-path": (
        "/api/v2/filesystem/cp/{resource_id}",
        "post",
        "cp",
    ),
    f"{CANONICAL_PREFIX}download-file": (
        "/api/v2/filesystem/download/{resource_id}",
        "post",
        "download",
    ),
    f"{CANONICAL_PREFIX}upload-file": (
        "/api/v2/filesystem/upload/{resource_id}",
        "post",
        "upload",
    ),
    f"{CANONICAL_PREFIX}resolve-storage-locations": (
        "/api/v2/storage/locations/{resource_id}",
        "get",
        "getStorageLocations",
    ),
    f"{CANONICAL_PREFIX}get-storage-access-endpoints": (
        "/api/v2/storage/access-endpoints/{resource_id}",
        "get",
        "getStorageAccessEndpoints",
    ),
}


def load_yaml(path: Path) -> dict:
    """Load one YAML mapping, failing clearly on an invalid document."""
    with path.open(encoding="utf-8") as stream:
        document = yaml.safe_load(stream) or {}
    if not isinstance(document, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return document


def collect_production_spec() -> dict:
    """Reproduce build-final-spec.py's production-only merge in memory."""
    result: dict = {}
    files = sorted(
        path
        for path in PRODUCTION_DIR.rglob("*")
        if path.suffix in {".yaml", ".yml"}
    )
    for path in files:
        deep_merge(result, load_yaml(path))
    return result


def deep_merge(target: dict, source: dict) -> None:
    """Match build-final-spec.py: merge without overriding existing scalars."""
    for key, value in source.items():
        if key not in target:
            target[key] = value
        elif isinstance(target[key], dict) and isinstance(value, dict):
            deep_merge(target[key], value)
        elif isinstance(target[key], list) and isinstance(value, list):
            target[key].extend(value)


def operation_bindings(document: dict, label: str, errors: list[str]) -> dict:
    """Collect and validate all x-iri-relation occurrences in a document."""
    occurrences: dict[str, list[tuple[str, str, str | None]]] = {}
    for path, path_item in document.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if (
                not isinstance(method, str)
                or method.lower() not in HTTP_METHODS
                or not isinstance(operation, dict)
            ):
                continue
            if "x-iri-relation" not in operation:
                continue

            relations = operation["x-iri-relation"]
            location = f"{label}: {method.upper()} {path}"
            if not isinstance(relations, list) or not relations:
                errors.append(f"{location}: x-iri-relation must be a non-empty array")
                continue
            string_relations = [
                relation for relation in relations if isinstance(relation, str)
            ]
            if len(string_relations) != len(relations):
                errors.append(f"{location}: relation values must be strings")
            if len(string_relations) != len(set(string_relations)):
                errors.append(f"{location}: x-iri-relation values must be unique")

            for relation in string_relations:
                parsed = urlsplit(relation)
                canonical = (
                    parsed.scheme == "https"
                    and parsed.netloc == "iri.science"
                    and parsed.path.startswith("/rels/")
                    and bool(parsed.path.removeprefix("/rels/"))
                    and not parsed.query
                    and not parsed.fragment
                )
                if not canonical:
                    errors.append(
                        f"{location}: {relation!r} is not an absolute canonical "
                        "DOE-IRI relation URI"
                    )
                occurrences.setdefault(relation, []).append(
                    (path, method.lower(), operation.get("operationId"))
                )
    return occurrences


def validate_mapping(document: dict, label: str, errors: list[str]) -> None:
    """Validate exact one-to-one relation and Operation Object mappings."""
    occurrences = operation_bindings(document, label, errors)
    unexpected = set(occurrences) - set(EXPECTED_BINDINGS)
    missing = set(EXPECTED_BINDINGS) - set(occurrences)
    for relation in sorted(unexpected):
        errors.append(f"{label}: unexpected operation relation {relation}")
    for relation in sorted(missing):
        errors.append(f"{label}: missing operation relation {relation}")

    for relation, expected in EXPECTED_BINDINGS.items():
        actual = occurrences.get(relation, [])
        if actual != [expected]:
            errors.append(
                f"{label}: {relation} must occur exactly once as {expected}; "
                f"found {actual}"
            )


def validate_relation_registry(errors: list[str]) -> None:
    """Check registry files, lifecycle metadata, and index links."""
    index_text = RELATION_INDEX.read_text(encoding="utf-8")
    new_relations = set(EXPECTED_BINDINGS) - {f"{CANONICAL_PREFIX}submit-job"}
    if len(new_relations) != 24:
        errors.append(
            f"regression mapping must contain 24 new relations; found {len(new_relations)}"
        )

    for relation in EXPECTED_BINDINGS:
        slug = relation.removeprefix(CANONICAL_PREFIX)
        definition = RELATION_DIR / f"{slug}.md"
        if not definition.is_file():
            errors.append(f"missing relation definition: {definition}")
            continue

        text = definition.read_text(encoding="utf-8")
        required_fragments = {
            "canonical URI": f"**Relation URI:** `{relation}`",
            "provisional status": "**Status:** Provisional<br>",
            "version 1.0.0": "**Version:** 1.0.0<br>",
            "change controller": (
                "**Change controller:** IRI technical subcommittee<br>"
            ),
        }
        for description, fragment in required_fragments.items():
            if fragment not in text:
                errors.append(f"{definition}: missing {description}")

        index_link = f"[`iri:{slug}`](./{slug}.md)"
        if index_link not in index_text:
            errors.append(f"{RELATION_INDEX}: missing index link for iri:{slug}")


def validate_hal_schemas(document: dict, label: str, errors: list[str]) -> None:
    """Validate reusable HAL schemas and their four approved attachments."""
    schemas = document.get("components", {}).get("schemas", {})
    hal_link = schemas.get("HalLink")
    hal_value = schemas.get("HalLinkValue")
    hal_links = schemas.get("HalLinks")

    if not isinstance(hal_link, dict):
        errors.append(f"{label}: missing HalLink schema")
    else:
        if hal_link.get("type") != "object":
            errors.append(f"{label}: HalLink must be an object schema")
        if hal_link.get("required") != ["href"]:
            errors.append(f"{label}: HalLink must require only href")
        href = hal_link.get("properties", {}).get("href", {})
        if href.get("type") != "string":
            errors.append(f"{label}: HalLink.href must be a string")
        if href.get("format") == "uri-reference":
            errors.append(
                f"{label}: HalLink.href must not declare format: uri-reference -- "
                "templated hrefs are RFC 6570 URI Templates, not plain URI-references"
            )

    expected_value = [
        {"$ref": "#/components/schemas/HalLink"},
        {
            "type": "array",
            "items": {"$ref": "#/components/schemas/HalLink"},
        },
    ]
    if not isinstance(hal_value, dict) or hal_value.get("oneOf") != expected_value:
        errors.append(f"{label}: HalLinkValue must allow one HalLink or an array")

    if not isinstance(hal_links, dict) or hal_links.get("additionalProperties") != {
        "$ref": "#/components/schemas/HalLinkValue"
    }:
        errors.append(f"{label}: HalLinks values must reference HalLinkValue")

    attached = set()
    for schema_name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        properties = schema.get("properties", {})
        if "_links" not in properties:
            continue
        attached.add(schema_name)
        link_property = properties["_links"]
        if link_property != {
            "$ref": "#/components/schemas/HalLinks",
            "readOnly": True,
        }:
            errors.append(f"{label}: {schema_name}._links has an unexpected schema")
        if "_links" in schema.get("required", []):
            errors.append(f"{label}: {schema_name}._links must remain optional")

    expected_attachments = {"Resource", "Job", "Task", "TaskSubmitResponse"}
    if attached != expected_attachments:
        errors.append(
            f"{label}: _links must be attached exactly to "
            f"{sorted(expected_attachments)}; found {sorted(attached)}"
        )

    resource = schemas.get("Resource", {})
    supported = resource.get("properties", {}).get("supported_endpoints")
    if not isinstance(supported, dict):
        errors.append(f"{label}: Resource.supported_endpoints must remain present")
    elif supported.get("deprecated") is True:
        errors.append(f"{label}: Resource.supported_endpoints must not be deprecated")


def main() -> int:
    errors: list[str] = []
    try:
        modular = collect_production_spec()
        generated = load_yaml(GENERATED_SPEC)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}")
        return 1

    validate_mapping(modular, "modular production OpenAPI", errors)
    validate_mapping(generated, "generated OpenAPI", errors)
    validate_relation_registry(errors)
    validate_hal_schemas(modular, "modular production OpenAPI", errors)
    validate_hal_schemas(generated, "generated OpenAPI", errors)

    if modular != generated:
        errors.append(
            "all_spec_v2.yaml does not match the production-only modular merge; "
            "regenerate it with build-final-spec.py"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"operation-relation validation failed with {len(errors)} error(s)")
        return 1

    print(
        "operation-relation validation passed: 25 canonical bindings, "
        "25 indexed provisional relation definitions, 4 optional HAL attachments, "
        "and matching modular/generated OpenAPI"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
