# OpenAPI Specification Workflow

This repository maintains the OpenAPI specification in a modular format. The specification is split into multiple YAML files organized by lifecycle stage.

Three helper scripts are provided to manage the specification lifecycle.

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

- `split_spec.py`	Convert a single OpenAPI spec into modular YAML files
- `diff_spec.py`	Generate differences between a new spec and the production baseline
- `build_spec.py`	Merge all modular YAML files into a single OpenAPI spec

These scripts allow to prepare all specification from an HTTP Endpoint (or local files).

### Split Specification (split_spec.py)

Split a full OpenAPI specification into modular YAML files for production directory.
This allows to take production OpenAPI URL and automatically prepare specification.

Usage
```
python split_spec.py <openapi_url> --outdir production
```

### Spec difference (diff_spec.py)

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
python diff_spec.py <openapi_url> --outdir prototype/testfeature/
```

### Build specification (build_spec.py)

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
python build_spec.py
```

