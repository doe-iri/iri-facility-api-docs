# IRI Link Relation: `accesses-mount`

**Relation URI:** `https://iri.science/rels/accesses-mount`<br>
**CURIE:** `iri:accesses-mount`<br>
**Status:** Provisional<br>
**Version:** 1.1.0<br>
**Source representation type:** `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:compute:system`<br>
**Target representation type:** `urn:doe-iri:resource:storage:mount`<br>
**Target representation profile:** `https://iri.science/profiles/resource-definition/storage/mount`

This document defines the `iri:accesses-mount` relationship used by the DOE-IRI service and compute resource models.

The canonical relation URI is `https://iri.science/rels/accesses-mount`. With
the canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:accesses-mount` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from the target mount representation
profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:accesses-mount` |
| Relation URI | `https://iri.science/rels/accesses-mount` |
| Status | `provisional` |
| Semantic meaning | Indicates that the source DTN service or compute system is configured to access a filesystem through the identified mount relationship resource. |
| Source representation type | `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:compute:system` |
| Target representation type | `urn:doe-iri:resource:storage:mount` |
| Target representation profile | `https://iri.science/profiles/resource-definition/storage/mount` |
| Cardinality | `0..*` targets from a DTN service or compute system resource. |
| Inverse relation | [`iri:mounted-on`](./mounted-on.md) |
| Target stability | Relatively static relationship resource. The target identifies configured filesystem access topology, not current mount availability, endpoint reachability, credential validity, unrestricted access, or transfer activity. |
| Authorization affects visibility | Yes. The relationship or individual mount targets MAY be omitted when the requester is not authorized to discover the configured access topology. |
| Target classification | Relationship resource |
| Relationship volatility | Relatively static configured access topology. Changes when the source's access configuration changes, not merely when mount or transfer conditions change. |

## 2. Semantic Meaning

The `iri:accesses-mount` relationship indicates that the source resource is configured to access a filesystem through the identified mount relationship resource. A DTN service uses the mount for transfer operations; a compute system makes the mount available to workloads that run on it.

The target is a mount rather than a direct filesystem because the mount identifies the particular filesystem exposure and configuration through which the filesystem is accessed. It can carry information such as the mount path, access mode, protocol, mount options, and consuming-system relationship that does not belong solely to the filesystem resource.

The relationship MUST NOT be interpreted as indicating current mount availability, endpoint reachability, credential validity, unrestricted read or write access, or active transfer activity.

## 3. Source and Target Representation

The relationship MUST originate from a resource whose `resource_type` is one of:

```text
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:compute:system
```

The relationship MUST target a resource whose `resource_type` is:

```text
urn:doe-iri:resource:storage:mount
```

The mount target is a relationship resource representing configured filesystem exposure. It is not a direct filesystem target, operation entry point, or endpoint.

A representation of the target mount resource MAY advertise the profile
`https://iri.science/profiles/resource-definition/storage/mount`. That profile identifies the
semantic contract of the target representation; it does not define the
semantics of `iri:accesses-mount`, which are identified by
`https://iri.science/rels/accesses-mount`.

## 4. Cardinality

A DTN service or compute system MAY identify zero, one, or multiple mount resources:

```text
DTN Service or Compute System  -- iri:accesses-mount -->  Filesystem Mount
              1                          0..*
```

The use of `0..*` permits facilities to represent a source resource without exposing configured mount access and to represent access to multiple filesystem exposures.

## 5. Static and Dynamic Semantics

`iri:accesses-mount` describes relatively static configured access topology. The relationship SHOULD remain present across ordinary operational state changes such as temporary mount unavailability, endpoint failure, credential expiration, authorization changes, or periods without transfer activity.

Current mount status, endpoint reachability, credential validity, authorization outcomes, and active transfer activity are outside the semantics of this relation. When represented, they are governed by the applicable IRI API, security, and Resource Definition Profile contracts.

## 6. Authorization and Visibility

Authorization MAY affect visibility of configured access topology. A provider MAY expose a DTN service or compute system while omitting individual `iri:accesses-mount` targets for requesters that are not permitted to discover the relevant mount or access configuration.

The absence of visible targets MUST NOT be interpreted as proof that the source resource has no configured mount access.

## 7. Cross-Relation Guidance

`iri:mounted-on` is the inverse of this relation: `Consumer -- iri:accesses-mount --> Mount` and `Mount -- iri:mounted-on --> Consumer` state the same configured relationship. Providers SHOULD publish both directions so that clients can start from either resource.

A link in either direction is sufficient to establish the relationship. A missing inverse link MUST NOT be interpreted as denying it, because the provider may not publish it or authorization may hide it.

Clients MUST use one of these two relations to discover configured DTN access to a filesystem exposure. The combination of `iri:hosted-on` and a mount resource's `iri:mounted-on` link to the hosting compute system MUST NOT be used to infer that a DTN service can access the mount, even when the service and mount are associated with the same compute infrastructure.

The mount target is more precise than a direct filesystem target because it identifies the particular exposure through which the DTN is configured to access the filesystem. A filesystem can have multiple mount relationship resources with different paths, protocols, access modes, or consuming systems.

## 8. HAL Representation

```json
{
  "_links": {
    "iri:accesses-mount": [
      { "href": "/api/v2/status/resources/perlmutter-scratch-mount", "profile": "https://iri.science/profiles/resource-definition/storage/mount" },
      { "href": "/api/v2/status/resources/analysis-home-mount", "profile": "https://iri.science/profiles/resource-definition/storage/mount" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: accesses-mount*
