---
layout: default
title: Core Concepts
nav_order: 3
permalink: /core-concepts/
---

# Core Concepts

This page introduces the vocabulary used throughout the IRI Facility API documentation.

For a visual explanation of how these concepts relate to one another, see
[IRI Resource Model](resource-model.md).

## Resource

A **Resource** is an IRI representation of a facility resource.

Resources may represent heterogeneous infrastructure such as compute systems, storage systems, network-related resources, or other facility capabilities defined by the specification and registry.

The structural representation is governed by the applicable IRI specification and OpenAPI schema.

## Resource Type

`resource_type` classifies an IRI Resource using a registered IRI Resource Type identifier.

Example:

```text
urn:doe-iri:resource:compute:system
```

The canonical assignments are maintained in the [Resource Type URN registry](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md).

A Resource Type URN is an identifier. It is **not** a Resource Definition Profile URI.

## Resource Definition Profile

A **Resource Definition Profile** defines additional semantics associated with a particular Resource Type.

The repository's registry explicitly separates Resource Type URNs from Resource Definition Profile URIs. A resource conforms to the common Resource representation and may also be interpreted according to the Resource Definition Profile selected by its `resource_type`.

See the [Resource Definition Profile registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles/resource-definition).

## Controlled IRI URNs

IRI uses registered URNs for controlled semantic identifiers.

The [URN registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/urns) contains the authoritative assignments.

Clients should compare registered identifiers as identifiers rather than attempting to derive unregistered semantics from string fragments.

## Link Relation

A **link relation** identifies the meaning of a link between the current representation and a target.

IRI-specific relation names are registered in the [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations).

Conceptually:

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://facility.example/api/v2/status/resources/example-mount"
    }
  }
}
```

The relation tells the client **why the link exists**. The `href` tells the client **where the target is**.

## Operation-affordance relation

An **operation-affordance relation** is a registered link relation whose target
is an operation entry point applicable to the source Resource. IRI v2 Phase 1
defines 25 such mappings across the Compute, Filesystem, and Storage APIs.

For example, `iri:submit-job` says that job submission is applicable in the
source Resource's context and identifies the entry point in `href`. It does not
grant authorization, encode an HTTP method, or describe the request body.

The deployed OpenAPI document advertised through `service-desc` supplies the
invocation contract. Its matching Operation Object carries an
`x-iri-relation` array containing the operation relation's absolute canonical
URI, such as `https://iri.science/rels/submit-job`. The canonical relation URI,
not `operationId`, is the binding key.

Phase 1 is additive: the existing optional `Resource.supported_endpoints`
property remains in the v2 schema and is not deprecated by the approved RFC.
Producers must not manufacture operation links solely from a broad
`supported_endpoints` category.

See the approved [Resource Operation Affordances RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md)
and the [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations).

## `profile`

A link may carry a `profile` value when the target representation has a defined representation profile.

Conceptually:

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://facility.example/api/v2/status/resources/example-mount",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    }
  }
}
```

The authoritative semantics of an IRI profile belong in the registry, not in this explanatory documentation.

## `service-desc`

`service-desc` is used to advertise a service description such as an OpenAPI document.

Example:

```json
{
  "_links": {
    "service-desc": {
      "href": "https://facility.example/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

This lets a client discover a machine-readable API description rather than depending exclusively on out-of-band configuration.

See [Understanding `service-desc`](service-desc.md) for its relationship to operation links, IRI relation definitions, and representation profiles.

## OpenAPI

OpenAPI defines the machine-readable structural contract for IRI APIs.

The v2 documentation uses OpenAPI 3.1. The maintained v2 sources are under [specification-v2/openapi](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi).

## RFC

An **IRI Request for Comments (RFC)** is a version-controlled design proposal used to evolve shared IRI technical standards.

See [RFC Process](rfc-process.md).

## Normative vs explanatory documentation

| Source | Role |
|---|---|
| Versioned specification | Normative API requirements |
| OpenAPI | Machine-readable API structure |
| Registry | Assigned identifiers and registered semantics |
| RFC | Proposed or adopted design rationale and governance |
| Documentation site | Explanation, onboarding, and implementation guidance |

When this site and a normative source differ, the normative source controls.
