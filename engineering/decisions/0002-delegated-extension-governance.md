# Decision 0002: Use explicit `ext` authority segments for delegated DOE-IRI extensions

**Status:** Accepted  
**Date:** 2026-08-14  
**Scope:** DOE-IRI URN extension governance

> **Non-normative:** This record explains architectural rationale. The governing DOE-IRI URN specification and URN registry define the current grammar, registration, and delegation rules.

## Context

Facilities and projects need to assign local DOE-IRI identifiers without colliding with future shared registry values or forcing every local leaf through central registration.

A direct facility-code segment could be confused with a future shared semantic child. The extension mechanism also needs to distinguish namespace governance from semantic classification.

## Decision

Use an explicit reserved delegation marker with the conceptual form:

```text
<registered-parent>:ext:<authority>:<local-path>
```

For example:

```text
urn:doe-iri:resource:compute:ext:nersc:fpga
```

Segments before `ext` form the shared DOE-IRI semantic hierarchy. `ext` switches into delegated administration, and the authority segment identifies governance rather than Resource classification.

Keep authority-code reservation separate from scope delegation. Reserving an authority code does not grant that authority every possible extension scope.

A scope applies to the exact delegated parent and grants the nonempty local suffix subtree beneath the assigned prefix. It does not grant adjacent, ancestor, or sibling scopes.

Hierarchy-aware generic processing may fall back to the registered shared semantic parent before `ext`; it must not treat `:ext` or `:ext:<authority>` as semantic Resource Types or controlled values.

Do not heuristically rewrite older direct-form identifiers into `ext` form. Any proven legacy identifiers require explicit compatibility or deprecation records.

## Rationale

The explicit marker creates a stable boundary between centrally governed semantics and delegated local naming. It avoids consuming shared semantic namespace positions merely to encode an organization's identity.

Separating authority reservation from scope delegation supports least-authority governance: an organization can be recognized without implicitly receiving every namespace branch.

Shared-parent fallback remains possible because the semantic parent remains visible before the delegation marker.

## Consequences and tradeoffs

Delegated authorities must document their local suffix semantics. Individual local leaves do not need central registration when the authority has an active scope and follows the governing rules.

Root-scope delegation remains possible but should be exceptional because it provides no domain-specific shared semantic parent for unfamiliar clients.

## Normative and current sources

- `rfc/rfc-iri-urn-structure-and-registry.md`
- `registry/urns/README.md`
- `registry/urns/resource-types.md`

## Historical notes

This record distills the rationale from an earlier design note retained in Git history without preserving one-time implementation instructions.
