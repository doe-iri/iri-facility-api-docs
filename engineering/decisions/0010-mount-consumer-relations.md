# Decision 0010: Shared mounts and two-way mount consumer relations

**Status:** Proposed  
**Date:** 2026-11-06  
**Scope:** `iri:mounted-on`, `iri:accesses-mount`, and the Filesystem Mount profile

> **Non-normative:** This record explains architectural rationale. Current OpenAPI, RFCs, registries, relation definitions, and representation profiles remain authoritative by concern.

## Context

`iri:mounted-on` ran only from a mount to exactly one compute system, and `iri:accesses-mount` ran only from a DTN service to a mount. A client starting at a compute system could not find its mounts, and a client starting at a mount could not find the DTN services that use it. The `iri:accesses-mount` definition deferred any inverse to a separate registration decision.

ESnet's EFS deployment shows the gap. One home mount and one project mount serve both a compute pool and a Globus DTN, and clients need to walk that topology from either end.

## Decision

- `iri:mounted-on` allows `1..*` targets, each a compute system or a DTN service.
- `iri:accesses-mount` allows a compute system as a source in addition to a DTN service.
- The two relations are registered as inverses. Providers SHOULD publish both directions, and a missing inverse link does not deny the relationship.
- Consumers MAY share one mount when its attributes describe the exposure for all of them. Compute systems that see different paths, and consumers that use different access modes, still require separate mounts.
- `mount_path` describes the location on compute systems. It does not describe the namespace a DTN service presents at its transfer endpoints.

## Rationale

Reusing the two registered relations gives clients both directions without adding new relation names.

A shared mount matches how a facility configures this storage: one configured exposure with several consumers. It avoids publishing duplicate mount resources whose only difference is the consumer they name.

One mount per consumer was the main alternative. It would have kept `iri:mounted-on` singular, kept the link format unchanged, and given each consumer its own `mount_path`. It was not chosen as the only model because of the duplicate resources, and it remains the required form when attributes differ between consumers.

## Consequences and tradeoffs

- `iri:mounted-on` changes from a single link object to an array of link objects for every facility, including mounts with one target. Clients that read `href` directly from the relation value must change.
- The target type of `iri:mounted-on` varies, so its link `profile` depends on the target. An implementation that cannot determine the target's profile can omit it, as with other polymorphic relations.
- A DTN consumer's transfer path cannot be derived from `mount_path`. Clients obtain it from the transfer service.
- Authorization can hide either direction of the relationship, so clients cannot treat the two directions as a consistency check.

## Normative and current sources

- `registry/rels/mounted-on.md`
- `registry/rels/accesses-mount.md`
- `registry/profiles/resource-definition/storage/mount.md`
- `registry/profiles/resource-definition/compute/system.md`
- `registry/profiles/resource-definition/service/dtn.md`

## Historical notes

Decision 0001 introduced `iri:accesses-mount` for DTN services. This record extends that relation to compute systems and does not change the service boundaries that decision describes.
