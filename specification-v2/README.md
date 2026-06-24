![Department of Energy - Office of Science](../specification-v1/images/doe-logo.jpg)

**IRI Facility Interface Design Document -- Specification 2.0**
---

**Draft**

# OpenAPI specification for the Facility API suite **[openapi/](./openapi/)**

This directory holds the **v2** OpenAPI specification for the IRI Facility API. v2 evolves
independently from v1 (see **[IRI Specification 1.0](../specification-v1/README.md)**).

OpenAPI 3.1 was chosen for documentation of the REST API because it is fully compatible with
JSON Schema 2020-12, which improves interoperability and validation in tooling.

Maintained OpenAPI definitions:
- all_spec_v2.yaml **[YAML](./openapi/all_spec_v2.yaml)** - versioned v2 artifact prepared from the `/api/v2` implementation line

The modular sources and build scripts live under **[openapi/](./openapi/)**; see
**[openapi/README.MD](./openapi/README.MD)** for the lifecycle layout and build workflow.

# Design Documentation

The conceptual model and design documentation are currently shared with v1 and maintained in
**[specification-v1](../specification-v1/README.md)**. v2-specific design documents will be added
here as they diverge.
