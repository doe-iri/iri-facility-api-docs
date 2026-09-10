# Decision 0007: Bind operation-affordance relations to OpenAPI Operation Objects

**Status:** Accepted

**Date:** 2026-09-10

**Scope:** DOE-IRI operation relations, relation definitions, and OpenAPI discovery

> **Non-normative:** This record explains architectural rationale. The HAL RFC, operation-affordance RFC, link-relation registry, and checked-out OpenAPI remain authoritative by concern.

## Context

A HAL operation-affordance link such as `iri:submit-job` identifies why an operation target is applicable and where its entry point is located. HAL does not identify the HTTP method, parameters, request body, responses, errors, or security contract for that operation.

The relation definition can identify the operation's semantics and current OpenAPI mapping, but duplicating the complete invocation contract there would create a second structural authority. Conversely, a deployed OpenAPI description contains the invocation contract but needs a machine-readable way to state which registered DOE-IRI relation identifies each Operation Object.

An IRI representation profile is not that mapping mechanism. A HAL Link Object's `profile` describes a target representation, while an operation relation targets an operation entry point.

## Decision

Use three coordinated layers for DOE-IRI operation affordances.

### HAL operation relation

A Resource or other permitted source representation advertises an applicable operation with a registered `iri:*` relation and an `href`. For example:

```text
iri:submit-job
    → https://api.example.org/api/v2/compute/job/system-a
```

The relation answers why the operation is applicable, and `href` answers where its entry point is located. The HAL Link Object does not duplicate the HTTP method, `operationId`, request schema, or other OpenAPI fields. It does not carry a Job representation profile merely because the operation returns a Job.

An adopting representation also advertises `service-desc` for the applicable deployed OpenAPI description.

### Relation definition

Every DOE-IRI operation relation has an individual definition under `registry/relations/`, linked from the Link Relation Index. That document is authoritative for the relation URI and CURIE, semantic meaning, permitted source, operation-entry-point target classification, cardinality, applicability and stability, authorization-sensitive visibility, and omission semantics. It records the current OpenAPI mapping for navigation, while OpenAPI remains authoritative for the operation structure.

For `iri:submit-job`, the definition is `registry/relations/submit-job.md`, and its canonical relation URI is:

```text
https://iri.science/rels/submit-job
```

The relation definition does not replace OpenAPI and does not independently define the operation's structural invocation contract.

### OpenAPI binding

The applicable deployed OpenAPI description binds a canonical relation URI to an Operation Object with the `x-iri-relation` Specification Extension. Its value is a non-empty array of unique absolute canonical relation URI strings, not HAL CURIEs.

```yaml
paths:
  /api/v2/compute/job/{resource_id}:
    post:
      operationId: launchJob
      x-iri-relation:
        - https://iri.science/rels/submit-job
```

Within one applicable OpenAPI description, each operation relation maps to exactly one Operation Object. The extension does not register the relation or override either the relation definition or the OpenAPI operation contract.

OpenAPI remains authoritative for the method, path and parameter serialization, request content and schema, responses, errors, and security requirements.

### Client resolution

The discovery path is:

```text
HAL relation/CURIE
    ↓ expand
canonical relation URI
    ↓ match x-iri-relation
deployed OpenAPI Operation Object
    ↓ apply
method + parameters + request body + responses + security
```

A client expands the HAL CURIE, retrieves the OpenAPI description through `service-desc`, finds the Operation Object whose `x-iri-relation` contains the canonical URI, verifies that the advertised `href` corresponds to that operation's server and path template, and then follows the OpenAPI invocation contract.

The canonical relation URI—not `operationId`—is the stable binding key. Changing `launchJob` to `submitJob` therefore does not rename `iri:submit-job` or alter the `x-iri-relation` value.

## Rationale

This design preserves a single authority for each concern while supporting runtime discovery. HAL exposes applicability and location, the relation registry governs semantic meaning, and OpenAPI governs invocation structure.

Using the canonical relation URI in OpenAPI avoids dependence on a representation-local CURIE declaration and remains stable across deployed paths and `operationId` changes. Keeping method and schema information out of HAL prevents stale duplication and allows standard OpenAPI tooling to remain the source of invocation details.

## Consequences and tradeoffs

Relation registration and OpenAPI annotation require coordinated review. Adding `x-iri-relation` does not make an unregistered relation valid, and adding a relation document does not make an unannotated OpenAPI operation machine-discoverable.

Clients supporting generic operation discovery must understand `x-iri-relation`. A missing, duplicate, or target-inconsistent binding is an error; clients must not guess a method from the relation name or probe a mutation to discover its contract. Explicit version-specific mappings may remain a migration fallback for older service descriptions.

The extension uses OpenAPI's standard Specification Extension mechanism but is DOE-IRI-specific. Validators should check canonical URI syntax, uniqueness, relation registration, and correspondence between advertised `href` values and bound Operation Objects.

Operation-link visibility remains authorization-sensitive where the relation definition says so. Link presence does not grant permission, and OpenAPI security requirements remain authoritative at invocation.

The current production OpenAPI remains authoritative until the `x-iri-relation` annotations are adopted through the normal OpenAPI revision and generation workflow.

## Normative and current sources

- `rfc/rfc-resource-operation-affordances.md`
- `rfc/rfc-hal-links.md`
- `registry/relations/README.md`
- `registry/relations/submit-job.md`
- `specification-v2/openapi/production/compute.yaml`
- `specification-v2/openapi/all_spec_v2.yaml`

## Historical notes

This decision extends Decision 0003's use of HAL for operation affordances by recording the machine-readable OpenAPI binding. It is consistent with Decision 0006, which retains `iri:submit-job` while planning the `operationId` migration from `launchJob` to `submitJob`. Neither earlier decision is superseded.
