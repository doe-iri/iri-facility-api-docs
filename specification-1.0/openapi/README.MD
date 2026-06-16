# OpenAPI Specification Workflow

This repository maintains the OpenAPI specification in a modular format. The specification is split into multiple YAML files organized by lifecycle stage.

Three helper scripts are provided to manage the specification lifecycle and versioned build artifacts.

## Directory Structure

```
openapi/
  production/
  beta/
  in_development/
  planned/
  prototype/
  retired/
  v2/
    production/
    beta/
    in_development/
    planned/
    prototype/
    retired/
```

Each directory contains modular YAML files such as:

```
_components.yaml
_topinfo.yaml
account.yaml
facility.yaml
status.yaml
compute.yaml
```

## Script helpers

- `production-prepare.py`	Convert a single OpenAPI spec into modular YAML files
- `diff-prepare.py`	Generate differences between a new spec and a modular baseline
- `build-final-spec.py`	Merge modular YAML files into a single OpenAPI spec

These scripts allow to prepare all specification from an HTTP Endpoint (or local files).

### Split Specification (`production-prepare.py`)

Split a full OpenAPI specification into modular YAML files for a target directory.
This allows taking an implementation OpenAPI URL or local file and preparing modular specification inputs for a specific API major version.

Usage
```
python production-prepare.py <openapi_source> --api-version v1 --outdir production
python production-prepare.py <openapi_source> --api-version v2 --outdir v2/production
```

`<openapi_source>` may be a URL, `file:///...` URL, or a local file path.

### Spec difference (`diff-prepare.py`)

Generate only the new API changes compared to the production specification. This is useful when new APIs are introduced and need to prepare spec change.
What it does? 

- Loads the new OpenAPI spec
- Compares it with the production baseline
- Extracts only:
  - new paths
  - new HTTP methods
  - new components
  - new top-level fields
  - Writes only the differences to the output directory.

Usage
```
python diff-prepare.py <openapi_source> --baseline production --api-version v1 --outdir planned/my-feature
python diff-prepare.py <openapi_source> --baseline v2/production --api-version v2 --outdir v2/in_development/my-feature
```

### Build specification (`build-final-spec.py`)

Merge all modular YAML files into a single OpenAPI specification. This produces the final OpenAPI document.

What it does? The script processes directories in lifecycle order:
```
production
beta
in_development
planned
prototype
retired
```

- Production loaded first
- Later stages may add new paths or components
- Existing definitions (path/components, etc) are never overridden

Usage:
```
python build-final-spec.py
python build-final-spec.py --dirs production --output all_spec_v1.yaml
python build-final-spec.py --dirs v2/production --output all_spec_v2.yaml
python build-final-spec.py --dirs v2/production v2/beta v2/in_development v2/planned v2/prototype v2/retired --output all_spec_v2.yaml
```

Recommended artifact flow:

- `all_spec_v1.yaml`: build from `production` after refreshing it from the `iri-facility-api-python` `1.1.0` implementation tag.
- `all_spec_v2.yaml`: build from the `v2/...` directory tree while v2 evolves independently.
- `all_spec.yaml`: optional combined lifecycle artifact for the current top-level lifecycle tree.
