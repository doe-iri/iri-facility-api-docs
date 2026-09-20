---
layout: default
title: IRI 2.0
nav_order: 5
has_children: true
permalink: /iri-2.0/
---

# IRI 2.0

IRI Facility API Specification 2.0 is the current v2 development line in the documentation repository.

The repository currently labels the v2 specification as **Draft**.

## Authoritative sources

- [Specification 2.0 README](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/README.md)
- [v2 OpenAPI directory](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi)
- [Combined v2 OpenAPI YAML](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/all_spec_v2.yaml)
- [IRI Registry](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/README.md)
- [IRI RFCs](https://github.com/doe-iri/iri-facility-api-docs/tree/main/rfc)

## OpenAPI version

The v2 documentation uses OpenAPI 3.1. The repository identifies compatibility with JSON Schema 2020-12 as a reason for that choice.

## Canonical IRI v2 OpenAPI

The authoritative repository artifact for the canonical IRI v2 API contract is
[`specification-v2/openapi/all_spec_v2.yaml`](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/all_spec_v2.yaml).

Its intended canonical publication URI is:

```text
https://iri.science/api/v2/openapi.json
```

This is the canonical IRI contract, not a description of every facility's
operational deployment. Implementations publish deployment-specific OpenAPI
documents containing their actual servers, security requirements, implemented
operations, and other applicable details. Their `service-desc` links normally
identify those deployed documents.

## Relationship to v1

The repository maintains v1 and v2 independently:

- [Specification 1.0](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v1)
- [Specification 2.0](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2)

The v2 README currently notes that some conceptual and design documentation remains shared with v1 until v2-specific documents diverge.

## Important v2 design areas

Current v2 design work includes several complementary areas:

### Resource classification

Resources use registered Resource Type identifiers.

See:

- [Resource Type URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md)
- [IRI Registry](registry.md)

### Type-specific semantics

Resource Definition Profiles provide type-specific semantics associated with `resource_type`.

See:

- [Resource Definition Profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles/resource-definition)
- [Type-Specific Attributes RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-type-specific-attributes.md)

### Hypermedia relationships

HAL-style links provide a mechanism for advertising relationships and navigation.

See:

- [HAL Links RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-hal-links.md)
- [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations)
- [Hypermedia and Discovery](hypermedia-and-discovery.md)

### Resource operation affordances

The approved Phase 1 operation-affordance migration maps all 25
Resource-scoped Compute, Filesystem, and Storage operations in the reviewed v2
contract to registered `iri:*` relations. Applicable links identify operation
entry points; the deployed OpenAPI Operation Objects bind those relations with
`x-iri-relation` and define methods, inputs, responses, errors, and security.

Phase 1 is additive. `Resource.supported_endpoints` remains in the v2 schema
and has not been deprecated or removed.

See:

- [Resource Operation Affordances RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md)
- [Operation relation validation](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/validate-operation-relations.py)

### Container execution capability discovery

The approved container-capability RFC adds optional `container_runtimes` data
to the Compute System Resource Definition Profile. It describes configured
runtime, image-format, acquisition, registry, privilege, accelerator, MPI,
build, and architecture behavior. It adds no image-acquisition endpoint and
does not change the existing job `Container` schema.

For `container_runtimes`, omission means structured capability information is
unknown, an empty array explicitly means container execution is unsupported,
and a non-empty array describes supported execution paths.

See the [Container Execution Capability Discovery RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-container-capability-discovery.md).

### IRI identifier governance

IRI URNs are governed through a registry model rather than being embedded as closed OpenAPI enumerations that must be revised for every taxonomy change.

See:

- [IRI URN Structure and Registry RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-iri-urn-structure-and-registry.md)
- [URN Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/urns)

### Proposals still under review

The [Normalized Queueing Policy Discovery RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-normalized-queue-atttributes.md)
proposes queue information in Resource `attributes`. The
[API Root Discovery and Implementation Conformance RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-iri-capability-discovery.md)
proposes a HAL API root, deployment-level conformance identifiers, and API-area
entry-point relations. Both remain Draft / Proposed; their identifiers and
behaviors are not canonical until the required registry and OpenAPI work is
adopted.

## How to use this site with v2

Use this site to understand the model and implementation flow. Use the repository sources above whenever exact schema, requirement language, registered identifiers, or conformance behavior matters.
