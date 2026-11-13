# IRI Link Relation: `accesses-mount`

**Relation URI:** `https://iri.science/rels/accesses-mount`<br>
**CURIE:** `iri:accesses-mount`<br>
**Status:** Provisional<br>
**Version:** 1.1.0<br>
**Source representation type:** DOE-IRI `Resource` representing a configured filesystem consumer<br>
**Source resource type:** Any conforming Resource Type, subject to the consumer-role requirement below<br>
**Target representation type:** DOE-IRI `Resource`<br>
**Target resource type:** `urn:doe-iri:resource:storage:mount`<br>
**Target representation profile:** `https://iri.science/profiles/resource-definition/storage/mount`

This document defines the `iri:accesses-mount` configured filesystem-access
relationship and its inverse, [`iri:accessed-by`](./accessed-by.md).

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
| Version | `1.1.0` |
| Semantic meaning | Indicates that the source Resource is configured to access a filesystem through the identified mount relationship resource. |
| Source representation type | DOE-IRI `Resource` representing an actual configured filesystem consumer. |
| Source resource type | Any conforming Resource Type, subject to the consumer-role requirement in Section 3. |
| Target representation type | DOE-IRI `Resource`. |
| Target resource type | Exactly `urn:doe-iri:resource:storage:mount`. |
| Target representation profile | `https://iri.science/profiles/resource-definition/storage/mount` |
| Cardinality | `0..*` mount targets from a consumer Resource. |
| Inverse relation | [`iri:accessed-by`](./accessed-by.md). Each direction is independently optional. |
| Target stability | Relatively static relationship resource. The target identifies configured filesystem access topology, not current mount availability, endpoint reachability, credential validity, unrestricted access, or transfer activity. |
| Authorization affects visibility | Yes. The relationship or individual mount targets MAY be omitted when the requester is not authorized to discover the configured access topology. |
| Target classification | Relationship resource |
| Relationship volatility | Relatively static configured access topology. Changes when consumer access configuration changes, not merely when mount or operational conditions change. |

## 2. Semantic Meaning

The `iri:accesses-mount` relationship indicates that the source Resource is
configured to access a filesystem through the identified mount relationship
resource. For example, a DTN service can use that exposure for transfer
operations, while a compute node or another service can use it for its own
configured filesystem access.

The target is a mount rather than a direct filesystem because the mount identifies the particular filesystem exposure and configuration through which the filesystem is accessed. It can carry information such as the mount path, access mode, protocol, mount options, and consuming-system relationship that does not belong solely to the filesystem resource.

The relationship MUST NOT be interpreted as indicating current mount
availability, endpoint reachability, credential validity, unrestricted read or
write access, or current filesystem use or transfer activity. It does not grant
authorization or establish eligibility for any operation-affordance relation.

## 3. Source and Target Representation

The relationship MUST originate from a conforming DOE-IRI `Resource` that
represents an actual configured filesystem consumer through the target mount.
The consumer's Resource Type MUST be valid under the governing registration or
delegation rules. A valid Resource Type alone is insufficient: the represented
Resource MUST have the configured consumer role for that mount.

Illustrative source Resource Types include:

```text
urn:doe-iri:resource:compute
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:service
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

These examples are not a closed whitelist. Other properly registered or
delegated Resource Types MAY be used when the represented Resource satisfies
the same configured-consumer requirement.

The relationship MUST target a Resource whose `resource_type` is exactly:

```text
urn:doe-iri:resource:storage:mount
```

The mount target is a relationship resource representing configured filesystem exposure. It is not a direct filesystem target, operation entry point, or endpoint.

The mount's `mount_path` remains in the filesystem namespace of the exactly one
`urn:doe-iri:resource:compute:system` identified by the mount's
[`iri:mounted-on`](./mounted-on.md) relation. An `iri:accesses-mount` link from a
service, node, or other consumer does not relocate that path into the source
Resource's own namespace or change the mount's consuming-system identity.

A representation of the target mount resource MAY advertise the profile
`https://iri.science/profiles/resource-definition/storage/mount`. That profile identifies the
semantic contract of the target representation; it does not define the
semantics of `iri:accesses-mount`, which are identified by
`https://iri.science/rels/accesses-mount`.

## 4. Cardinality

A consumer Resource MAY identify zero, one, or multiple mount resources:

```text
Consumer Resource  -- iri:accesses-mount -->  Filesystem Mount
        1                      0..*
```

The use of `0..*` permits facilities to represent a consumer without exposing
configured mount access and to represent access to multiple filesystem
exposures.

`iri:accesses-mount` and [`iri:accessed-by`](./accessed-by.md) describe the same
configured consumer–mount association in opposite directions. Advertisement
of either direction is independently optional; a provider is not required to
publish a reciprocal link or an exhaustive list of consumers or mounts. When
both relations describe the same configuration, they MUST agree about the
consumer–mount association. This consistency requirement does not require
matching or exhaustive visible link sets.

## 5. Static and Dynamic Semantics

`iri:accesses-mount` describes relatively static configured access topology.
Subject to authorization-sensitive visibility, the relationship SHOULD remain
present across ordinary operational state changes such as temporary mount
unavailability, endpoint failure, credential expiration, authorization outcome
changes, or periods without filesystem use or transfer activity.

Current mount status, endpoint reachability, credential validity, authorization outcomes, and active transfer activity are outside the semantics of this relation. When represented, they are governed by the applicable IRI API, security, and Resource Definition Profile contracts.

## 6. Authorization and Visibility

Authorization MAY affect visibility of configured access topology. A provider
MAY expose a consumer Resource while omitting individual `iri:accesses-mount`
targets for requesters that are not permitted to discover the relevant mount or
access configuration.

The absence of visible targets MUST NOT be interpreted as proof that the
consumer has no configured mount access. Omission of either direction can
reflect optional advertisement, partial publication, or authorization
filtering; absence is not a negative assertion about the association or proof
that the inverse is inconsistent.

## 7. Cross-Relation Guidance

Clients MAY discover a configured association from a consumer's advertised
`iri:accesses-mount` link or a mount's advertised
[`iri:accessed-by`](./accessed-by.md) link. Clients MUST NOT infer configured
access solely from a Resource Type, hosting, containment, or a mount's
`iri:mounted-on` relation. In particular, the combination of `iri:hosted-on`
and `iri:mounted-on` does not establish access even when the service and mount
are associated with the same compute infrastructure.

The mount target identifies the particular exposure through which the consumer
is configured to access the filesystem. A filesystem can have multiple mount
relationship resources with different paths, protocols, access modes, or
consuming systems. Neither direction changes operation-affordance source-type
or applicability restrictions.

## 8. HAL Representation

These illustrative partial Resource representations show a compute node and a
DTN service configured to use the same mount. Other required Resource fields
are omitted for clarity. The mount's `mount_path` is interpreted in its
`iri:mounted-on` compute-system namespace, not a namespace inferred from either
source.

```json
[
  {
    "id": "pioneer-login01",
    "resource_type": "urn:doe-iri:resource:compute:node",
    "_links": {
      "curies": [
        { "name": "iri", "href": "https://iri.science/rels/{rel}", "templated": true }
      ],
      "self": { "href": "/api/v2/status/resources/pioneer-login01", "profile": "https://iri.science/profiles/resource-definition/compute/node" },
      "iri:accesses-mount": [
        { "href": "/api/v2/status/resources/pioneer-scratch-mount", "profile": "https://iri.science/profiles/resource-definition/storage/mount" }
      ]
    }
  },
  {
    "id": "pioneer-dtn",
    "resource_type": "urn:doe-iri:resource:service:dtn",
    "_links": {
      "curies": [
        { "name": "iri", "href": "https://iri.science/rels/{rel}", "templated": true }
      ],
      "self": { "href": "/api/v2/status/resources/pioneer-dtn", "profile": "https://iri.science/profiles/resource-definition/service/dtn" },
      "iri:accesses-mount": [
        { "href": "/api/v2/status/resources/pioneer-scratch-mount", "profile": "https://iri.science/profiles/resource-definition/storage/mount" },
        { "href": "/api/v2/status/resources/analysis-home-mount", "profile": "https://iri.science/profiles/resource-definition/storage/mount" }
      ]
    }
  }
]
```

---

*DOE Integrated Research Infrastructure — Link Relation: accesses-mount*
