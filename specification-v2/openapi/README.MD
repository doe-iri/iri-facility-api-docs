# OpenAPI Specification Workflow (v2)

This directory holds the IRI Facility API **v2** OpenAPI specification in a modular format.
The specification is split into multiple YAML files organized by lifecycle stage. v2 evolves
independently from v1, which lives in `../../specification-v1/openapi/`.

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
```

Only `production/` exists today; the other lifecycle stages are created on demand.

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
They default to the `v2` API version.

### Split Specification (`production-prepare.py`)

Split a full OpenAPI specification into modular YAML files for a target directory.
This allows taking an implementation OpenAPI URL or local file and preparing modular specification inputs.

Usage
```
python production-prepare.py <openapi_source> --outdir production
python production-prepare.py <openapi_source> --api-version v2 --outdir production
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
python diff-prepare.py <openapi_source> --baseline production --outdir in_development/my-feature
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
python build-final-spec.py --dirs production --output all_spec_v2.yaml
python build-final-spec.py --dirs production beta in_development planned prototype retired --output all_spec_v2.yaml
```

Recommended artifact flow:

- `all_spec_v2.yaml`: build from the `production` directory (and any later lifecycle stages) as v2 evolves.
  This is the default output of `build-final-spec.py`.
