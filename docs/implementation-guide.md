---
layout: default
title: Implementation Guide
parent: IRI 2.0
nav_order: 4
permalink: /implementation-guide/
---

# Implementation Guide

This page provides a practical implementation path for facilities exposing IRI-compatible APIs.

It is guidance, not a substitute for the versioned specification or OpenAPI contract.

Use the [reference Python implementation](https://github.com/doe-iri/iri-facility-api-python) as a starting point for your implementation.

If you are interested in driving the reference implementation with some demo data, use the [iri-facility-api-demo-adapter](https://github.com/doe-iri/iri-facility-api-demo-adapter).

## 1. Select the target specification

For v2 development, begin with:

- [IRI Specification 2.0](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2)
- [v2 OpenAPI sources](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi)
- [Combined v2 OpenAPI YAML](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/all_spec_v2.yaml)

Confirm the exact version or commit against which your implementation is intended to conform.

## 2. Identify the resources your facility exposes

Map facility capabilities to registered IRI Resource Types.

Use:

- [Resource Type URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md)

Do not create facility-local variants of IRI Resource Type identifiers when an existing registered type already represents the concept.

## 3. Apply common and type-specific semantics

For each Resource Type:

1. implement the common Resource representation required by the specification,
2. identify the applicable Resource Definition Profile,
3. populate type-specific `attributes` according to the governing semantics, and
4. use registered controlled values where the profile requires them.

See:

- [Resource profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles)
- [Controlled Attribute URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/attributes.md)

## 4. Advertise relationships and operation affordances

Use registered IRI link relations for resource relationships and navigation.

```json
{
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:has-mount": {
      "href": "https://facility.example/api/v2/status/resources/example-mount"
    }
  }
}
```

Check the [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations) for the authoritative relation semantics.

Do not invent an unregistered IRI relation simply to match an internal database relationship.

For Resource-scoped Compute, Filesystem, and Storage operations, implement the
approved Phase 1 mappings in the [Resource Operation Affordances RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md).
Advertise an operation relation only when that operation is implemented,
applicable to the represented Resource context, and visible to the requester.
Do not infer every operation from a broad `supported_endpoints` value.

An operation link identifies the entry point but does not encode the HTTP
method or payload. In the deployed OpenAPI document, put the canonical relation
URI in the matching Operation Object's `x-iri-relation` array. Do not put
`x-iri-relation`, `method`, or `operationId` on the HAL Link Object, and do not
attach a Resource or Job representation profile to an operation entry point.

## 5. Advertise service descriptions when applicable

An IRI v2 facility implementation should:

1. implement the canonical IRI API contract;
2. publish an OpenAPI description of the actual deployment;
3. include its actual deployment servers, security configuration, and
   implemented operations; and
4. expose that document through `service-desc` where applicable; and
5. ensure every advertised Phase 1 operation relation has exactly one matching
   `x-iri-relation` binding in that deployed document.

Illustrative example:

```json
{
  "_links": {
    "service-desc": {
      "href": "https://iri.example.gov/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

`https://iri.science/api/v2/openapi.json` is the intended canonical publication
URI for the IRI v2 reference contract. It is not normally a facility's
`service-desc` target, because that link should describe the deployed service
in its actual context.

See [Understanding `service-desc`](service-desc.md) for placement, media-type, client-use, and security guidance.

## 6. Preserve URI opacity for clients

Facility implementations control their URI layout.

A client should not need to know how that layout was constructed. Therefore, links returned by the implementation should contain usable target URIs and should remain semantically stable according to the governing specification.

## 7. Implement HTTP behavior from the specification

HTTP method behavior, status codes, headers, conditional request behavior, error formats, pagination, and other protocol details should be implemented from the applicable specification and OpenAPI definition.

Do not rely on examples on this site as the source of truth for exact wire behavior.

## 8. Validate representations

Validation should include both:

- **structural validation** against the OpenAPI / JSON Schema contract, and
- **semantic validation** against applicable registry and profile rules.

Passing schema validation does not necessarily prove that a registered identifier has been used with the correct semantics.

For the adopted operation mappings, also run the repository's
[`validate-operation-relations.py`](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/validate-operation-relations.py)
regression check. It verifies the 25 relation-to-operation bindings, registry
entries, HAL declarations, and generated OpenAPI artifact.

## 9. Test discovery

Test the implementation as a generic client would use it:

```text
known entry point
      │
      ▼
retrieve representation
      │
      ▼
read resource_type
      │
      ▼
inspect links
      │
      ▼
follow advertised relation
      │
      ▼
retrieve target / operation description
```

A useful test is to verify that the client can complete the flow without being given facility-specific path templates.

## 10. Track specification evolution

IRI v2 is currently maintained as a draft development line. Implementations should pin validation and interoperability testing to a known specification revision or commit and explicitly update that baseline as the specification changes.

See [Contributing](contributing.md) for how to report implementation findings.
