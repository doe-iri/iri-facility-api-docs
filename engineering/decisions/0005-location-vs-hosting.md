# Decision 0005: Distinguish Resource location from service hosting

**Status:** Accepted  
**Date:** 2026-08-14  
**Scope:** `iri:located-at` and `iri:hosted-on`

> **Non-normative:** This record explains why the two relationships are distinct. Their current semantics are defined by the corresponding relation definitions and HAL RFC.

## Context

A Resource's association with an IRI Site and a service's association with compute infrastructure answer different questions.

Treating both as one relation would blur administrative/physical Site placement with compute hosting topology and could encourage clients to infer runtime behavior from a stable relationship.

## Decision

Use `iri:located-at` from any DOE-IRI Resource to the associated Facility API `Site` representation.

Use `iri:hosted-on` from DTN or inference service Resources to the compute system or compute node that provides hosting infrastructure.

The relationships are intentionally independent:

```text
Resource -- iri:located-at --> Site

Service Resource -- iri:hosted-on --> Compute System or Compute Node
```

`iri:located-at` maps the current `Resource.site_uri` navigation semantics during the additive HAL migration. When both are present, the link target and retained `site_uri` agree according to the HAL RFC and relation definition.

Neither relation asserts current health, availability, endpoint reachability, request routing, live replica placement, or operation permission.

## Rationale

A Site is an administrative and physical facility concept. A compute system or node is infrastructure that may host a service. A service can remain associated with a Site while its hosting topology changes, and it may be hosted across more than one compute target.

Separate relations therefore preserve semantic precision and avoid encoding deployment topology in Resource Type URNs or location fields.

## Consequences and tradeoffs

Consumers that need only Site placement can use `iri:located-at` without learning service-host topology.

Consumers that are authorized to discover hosting topology can use `iri:hosted-on`; absence of visible hosting targets does not necessarily prove that no hosts exist.

## Normative and current sources

- `registry/relations/located-at.md`
- `registry/relations/hosted-on.md`
- `rfc/rfc-hal-links.md`
- `registry/profiles/facility/site.md`
- `registry/profiles/resource-definition/compute/system.md`
- `registry/profiles/resource-definition/compute/node.md`

## Historical notes

This record preserves the durable rationale from an earlier location-relation design note retained in Git history. Current relation documents remain authoritative for exact cardinality, visibility, compatibility, and target-profile rules.
