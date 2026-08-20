# Decision 0001: Model DTN and inference capabilities as service Resources

**Status:** Accepted  
**Date:** 2026-08-13  
**Scope:** Service Resource taxonomy and boundaries

> **Non-normative:** This record explains architectural rationale. The Resource Type registry, Resource Definition Profiles, relation definitions, and governing RFCs define current semantics.

## Context

IRI needs to describe consumable data-transfer and model-invocation services while keeping service identity distinct from the infrastructure and implementation details that support those services.

Several concepts could have been modeled as Resource subtypes: DTN hosts, inference endpoints, model artifacts, model deployments, replicas, and accelerators. Doing so without an independent interoperability need would make the Resource taxonomy mirror implementation topology rather than stable semantic identity.

## Decision

Use these refined service Resource Types:

```text
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

Keep service Resource Types under `urn:doe-iri:resource:service:*` and keep controlled service technologies, protocols, and API identifiers under `urn:doe-iri:service:*`.

A DTN Resource represents a consumable data-transfer service, not an individual host or compute node.

An inference Resource represents a consumable model-invocation service, not a model artifact, deployment, endpoint, replica, host, or accelerator.

Endpoint descriptors and served-model catalog entries remain type-specific attributes unless a future use case requires independent identity, lifecycle, authorization, or relationships.

Hosting topology is expressed with `iri:hosted-on`. A DTN's configured access through a filesystem mount is expressed with `iri:accesses-mount`.

IRI v2 does not require a separate Resource Definition / Resource State representation model. Time-varying values, when represented, are governed by the applicable API contract and Resource Definition Profile.

## Rationale

This model separates four questions that otherwise become conflated:

- what consumable service is being offered;
- what technology implements it;
- what protocol or API a consumer can use;
- what infrastructure hosts or supports it.

It also prevents vendor/product names from becoming Resource subtypes merely because the same name may describe a technology or protocol.

Using link relations for hosting and storage-access topology keeps the semantic Resource Type hierarchy independent of physical deployment topology.

## Consequences and tradeoffs

Facilities can expose a stable service identity even when hosting infrastructure, endpoints, or runtime placement changes.

The model deliberately does not make every internal service component independently addressable through IRI. If a future interoperability requirement needs independent identity for a model, endpoint, deployment, replica, or accelerator, that concept requires separate architectural review.

## Normative and current sources

- `registry/urns/resource-types.md`
- `registry/urns/attributes.md`
- `registry/profiles/resource-definition/service/dtn.md`
- `registry/profiles/resource-definition/service/inference.md`
- `registry/relations/hosted-on.md`
- `registry/relations/accesses-mount.md`
- `rfc/rfc-type-specific-attributes.md`

## Historical notes

This record distills durable rationale from an earlier design note retained in Git history. That note also contained implementation paths and a now-superseded v2 definition/state proposal; those details are intentionally not preserved here.
