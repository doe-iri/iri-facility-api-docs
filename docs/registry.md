---
layout: default
title: IRI Registry
nav_order: 6
has_children: true
permalink: /registry/
---

# IRI Registry

The DOE IRI Registry records semantic identifiers and representation conventions used by the IRI Facility APIs.

The authoritative registry is maintained under [`registry/`](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry).

## Why the registry exists

IRI interfaces need shared identifiers that can evolve independently of individual facility implementations.

The registry keeps several concerns distinct:

```text
Resource classification
        │
        ▼
Resource Type URN
        │
        ▼
Resource Definition semantics
        │
        └────────► relationships expressed with registered links
```

## Registry areas

| Registry area | Purpose |
|---|---|
| [URN Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/urns) | Assigned IRI URNs and controlled identifiers |
| [Resource Type URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md) | Canonical resource classifications |
| [Controlled Attribute URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/attributes.md) | Registered controlled attribute values |
| [Resource Profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles) | Common and type-specific representation semantics |
| [Resource Definition Profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles/resource-definition) | Type-specific Resource semantics |
| [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations) | Registered relation names and their semantics |

## Resource Type vs Resource Definition Profile

These identifiers have different roles.

Example Resource Type:

```text
urn:doe-iri:resource:compute:system
```

Example profile URI pattern:

```text
https://iri.science/profiles/resource-definition/compute/system
```

The Resource Type classifies the resource. The Resource Definition Profile provides additional semantics for that resource type.

Do not treat the Resource Type URN as if it were the profile URI.

## Common resource semantics

The registry contains common semantics that apply to IRI Resource representations, with additional Resource Definition semantics selected according to `resource_type`.

This allows shared structure and type-specific meaning to evolve without creating a separate API object for every resource subtype.

## Relationships

Topology, navigational relationships, and applicable Resource operations are
represented through registered link relations.

For example, a compute resource can link to another resource through an IRI relation whose authoritative meaning is defined in the Link Relation Registry.

The relation identifier should be interpreted according to its registry definition rather than inferred from the target URL.

The approved IRI v2 Phase 1 mapping adds 25 provisional operation-affordance
relations for Resource-scoped Compute, Filesystem, and Storage operations. An
operation relation identifies why its entry point is applicable and where it
is; the deployed OpenAPI contract remains authoritative for the method,
parameters, payloads, responses, errors, and security. OpenAPI binds the
canonical relation URI to an Operation Object through `x-iri-relation`.

The mapping is additive. The broad `Resource.supported_endpoints` property
remains available during Phase 1 and cannot be used by itself to infer all
operation links. See the [Resource Operation Affordances RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md).

## Registering new semantics

Before introducing a new IRI identifier:

1. Check the existing registry.
2. Determine whether the concept is a Resource Type, controlled value, profile, or relationship.
3. Avoid creating a new identifier when an existing registered semantic already applies.
4. Use an issue or RFC when the change introduces a new architectural concept.
5. Submit the registry change through the main repository's pull-request process.

See [RFC Process](rfc-process.md) and [Contributing](contributing.md).

## Authoritative registry overview

See the repository's [DOE IRI Registry README](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/README.md) for the current registry structure and rules.
