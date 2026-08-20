# Decision 0003: Use HAL links for navigable relationships and operation affordances

**Status:** Accepted  
**Date:** 2026-08-14  
**Scope:** IRI hypermedia and URI-property migration

> **Non-normative:** This record explains architectural rationale. `rfc/rfc-hal-links.md`, the Link Relation Registry, and OpenAPI define current behavior.

## Context

IRI clients operate across independently implemented facilities. A client that discovers a Resource should not need to guess facility-specific URL templates for related Resources, monitoring targets, or operation entry points.

Existing representations also contain URI-valued properties that already identify navigable targets. A hypermedia model needs to coexist with those properties during an additive migration.

## Decision

Use HAL `_links` to advertise navigable relationships and applicable operation entry points.

Keep these responsibilities distinct:

```text
resource_type
    identifies what kind of Resource is represented

ordinary representation properties
    carry representation data

_links
    identifies related targets and applicable operation entry points

OpenAPI
    defines how an operation is invoked
```

Use standard Web Linking relations when their established semantics apply, including `self`, `help`, `monitor`, and `service-desc`. Use registered `iri:*` relations for DOE-IRI-specific relationship semantics.

During additive migration, retained URI properties and their mapped HAL links identify the same target. Null optional URI properties produce an omitted relation, never a null `href`.

An operation-affordance relation such as `iri:submit-job` targets an operation entry point, not the representation returned by that operation. OpenAPI remains authoritative for method, request/response schemas, authentication, authorization, and error handling.

### HAL Link Object four-layer distinction

Documentation and implementations should preserve this distinction:

```text
relation name
    WHY the target is linked

href
    WHERE the target is located

type
    HOW the target is represented

profile
    WHAT semantic representation profile applies to the target
```

A Link Object `profile` describes the target representation. It does not identify the relation, the source representation, or an operation contract.

## Rationale

This model reduces hard-coded path construction and makes traversal usable by conventional clients, workflow engines, and agentic tooling without making the LLM or client infer server routing conventions.

Separating relation semantics from target representation semantics prevents a profile URI from becoming an implicit relation registry and prevents a relation URI from being mistaken for a representation contract.

Keeping OpenAPI authoritative for invocation semantics allows hypermedia to advertise applicability and location without duplicating operation contracts.

## Consequences and tradeoffs

Existing URI-valued properties remain part of the current OpenAPI contract until a separately approved schema revision removes them.

Link visibility may be authorization-sensitive where the applicable relation definition says so; absence of a visible link is not automatically semantic absence.

Clients should not infer a target URL from a Resource identifier or Resource Type when the representation can advertise that target directly.

## Normative and current sources

- `rfc/rfc-hal-links.md`
- `registry/relations/README.md`
- `registry/relations/*.md`
- `registry/profiles/`
- `specification-v2/openapi/`

## Historical notes

This record distills durable rationale from an earlier HAL design note retained in Git history. File creation lists and one-time migration mechanics are intentionally omitted.
