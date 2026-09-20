---
layout: default
title: Hypermedia and Discovery
parent: IRI 2.0
nav_order: 2
permalink: /hypermedia-and-discovery/
---

# Hypermedia and Discovery

A central IRI design goal is that clients should be able to discover relationships and applicable entry points from resource representations instead of constructing facility-specific URLs from assumptions.

The normative design is maintained in the [HAL links RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-hal-links.md), the approved [Resource Operation Affordances RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md), and the [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations). This page provides the conceptual model.

## Why discovery matters

Facilities may expose the same conceptual capability using different internal services and routing structures.

Without discoverable links, a client might need to know that one facility uses:

```text
/api/v2/compute/jobs/{resource_id}
```

while another uses:

```text
/services/scheduler/{resource_id}/jobs
```

That routing knowledge couples the client to individual facility implementations.

The preferred IRI pattern is for the representation to advertise the applicable target.

## Basic traversal model

```text
Discover Resource
       │
       ▼
Read representation
       │
       ├──── resource_type
       │          │
       │          ▼
       │   Resource Definition semantics
       │
       └──── _links
                  │
                  ├── related resources
                  ├── topology
                  ├── state resources
                  ├── operation entry points
                  └── service descriptions
```

## Example representation

The following is illustrative rather than normative:

```json
{
  "resource_id": "frontier",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "_links": {
    "self": {
      "href": "https://facility.example/api/v2/status/resources/frontier"
    },
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:has-node": {
      "href": "https://facility.example/api/v2/status/resources/frontier-node-1",
      "title": "Frontier node 1",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/compute/node"
    },
    "iri:submit-job": {
      "href": "https://facility.example/api/v2/compute/job/frontier"
    },
    "service-desc": {
      "href": "https://facility.example/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

A client can determine:

- what the resource represents from `resource_type`,
- where the canonical representation is from `self`,
- how the `iri` CURIE expands to canonical relation URIs,
- that a node relationship exists from the registered `iri:has-node` relation,
- that job submission is applicable from `iri:submit-job`,
- the target of that relationship from `href`,
- the target representation semantics from `profile`, when supplied, and
- where to obtain a machine-readable API description from `service-desc`.

## Relation semantics

A relation name should communicate the semantics of the relationship independently of the target URL.

Conceptually:

```text
iri:has-mount ─────► "this resource has the referenced mount relationship"
href          ─────► "the target can be found here"
profile       ─────► "interpret the target according to this profile"
```

Canonical IRI-specific relation names and their semantics are maintained in the [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations).

## Do not infer paths

Clients, workflow engines, MCP servers, and AI agents should prefer advertised links over path speculation.

Avoid:

```text
resource_id = frontier
therefore submit URL = /api/v2/jobs/frontier
```

Prefer:

```text
resource representation
        │
        ▼
registered operation relation
        │
        ▼
advertised href
```

The server remains free to change its internal routing as long as the representation continues to advertise the correct target.

## Link relation vs target profile

These solve different problems:

| Element | Question answered |
|---|---|
| Relation name | Why is this target linked from the current representation? |
| `href` | Where is the target? |
| `type` | What media type should the client expect? |
| `profile` | What additional representation semantics apply to the target? |

A relation definition should not be used as a substitute for the target representation profile.

## Operation affordances and OpenAPI binding

IRI v2 Phase 1 defines 25 operation-affordance mappings: five Compute,
18 Filesystem, and two Storage discovery operations. Each operation link has
zero-or-one cardinality in a source representation and means that the operation
is configured, applicable, and visible in that Resource context. Presence is
not an authorization grant, and absence does not prove that the deployment
lacks the operation.

HAL links do not carry methods or request schemas. An operation-affordance link
must not add a `method` or `operationId` member, and it must not use a
representation `profile` merely because the operation returns that kind of
object. Instead, the applicable deployed OpenAPI description binds the
canonical relation URI on an Operation Object:

```yaml
paths:
  /api/v2/compute/job/{resource_id}:
    post:
      operationId: launchJob
      x-iri-relation:
        - https://iri.science/rels/submit-job
```

The relation URI is the stable lookup key; `operationId` can differ or change.
The approved migration is additive, so broad `Resource.supported_endpoints`
categories may coexist with operation links. A producer must not infer that
all operations apply merely because the broad category is present.

## Service discovery

A `service-desc` link can advertise an OpenAPI description:

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

This supports a two-level discovery pattern:

```text
IRI representation
      │
      ├── semantic links ───► resources / operations
      │
      └── service-desc ─────► OpenAPI contract
```

When a client discovers an operation such as `iri:submit-job`, the operation
link identifies that the operation applies and where its entry point is. The
`service-desc` from the applicable deployed service tells the client how to
invoke it, including the HTTP method, parameters, request body, response schema,
authentication and security requirements, and errors.

A client SHOULD NOT assume that the canonical `iri.science` OpenAPI fully
describes the operational details of the facility it is currently interacting
with when a deployed `service-desc` is available.

```text
current representation + deployed OpenAPI
    beats
guessed facility routing or stale static assumptions
```

See [Understanding `service-desc`](service-desc.md) for a detailed explanation of how this registered relation differs from operation links, IRI relation definitions, and representation profiles.

## Client algorithm

A generic IRI client can follow this sequence:

1. Obtain an IRI representation through a configured or previously discovered entry point.
2. Validate the representation against the applicable structural contract.
3. Inspect `resource_type`.
4. Apply registered Resource Definition semantics as needed.
5. Enumerate `_links`.
6. Match a link relation to the desired relationship or operation and expand
   an applicable CURIE to its canonical relation URI.
7. For an operation, retrieve the applicable deployed OpenAPI through
   `service-desc` and find the single Operation Object whose
   `x-iri-relation` contains that canonical URI.
8. Verify that the advertised `href` matches that operation after server
   resolution and producer-bound path variables; do not guess when the binding
   is missing, duplicated, or inconsistent.
9. Invoke the operation according to OpenAPI, or follow the advertised `href`
   for an ordinary navigational relation.
10. Honor `type`, `profile`, and URI-template metadata when applicable.

This model is especially useful for portable orchestration and agentic systems because it replaces URL guessing with explicit, registered semantics.
