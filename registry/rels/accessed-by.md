# IRI Link Relation: `accessed-by`

**Relation URI:** `https://iri.science/rels/accessed-by`<br>
**CURIE:** `iri:accessed-by`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** DOE-IRI `Resource`<br>
**Source resource type:** `urn:doe-iri:resource:storage:mount`<br>
**Target representation type:** DOE-IRI `Resource` representing a configured filesystem consumer<br>
**Target resource type:** Any conforming Resource Type, subject to the consumer-role requirement below<br>
**Target representation profile:** `https://iri.science/profiles/status/resource`, or the applicable established specialized target profile

This document defines the `iri:accessed-by` configured filesystem-access
relationship, the inverse of [`iri:accesses-mount`](./accesses-mount.md).

The canonical relation URI is `https://iri.science/rels/accessed-by`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:accessed-by` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:accessed-by` |
| Relation URI | `https://iri.science/rels/accessed-by` |
| Status | `provisional` |
| Version | `1.0.0` |
| Semantic meaning | Indicates that the identified consumer Resource is configured to access a filesystem through the source mount relationship resource. |
| Source representation type | DOE-IRI `Resource`. |
| Source resource type | Exactly `urn:doe-iri:resource:storage:mount`. |
| Target representation type | DOE-IRI `Resource` representing an actual configured filesystem consumer. |
| Target resource type | Any conforming Resource Type, subject to the consumer-role requirement in Section 3. |
| Target representation profile | `https://iri.science/profiles/status/resource`, or the applicable established specialized target profile. |
| Cardinality | `0..*` consumer targets from a mount Resource. |
| Inverse relation | [`iri:accesses-mount`](./accesses-mount.md). Each direction is independently optional. |
| Target stability | Relatively static Resource representation. The target identifies a configured filesystem consumer, not current mount availability, endpoint reachability, credential validity, unrestricted access, or transfer activity. |
| Authorization affects visibility | Yes. The relationship or individual consumer targets MAY be omitted when the requester is not authorized to discover the configured access topology. |
| Target classification | Resource |
| Relationship volatility | Relatively static configured access topology. Changes when consumer access configuration changes, not merely when mount or operational conditions change. |

## 2. Semantic Meaning

The `iri:accessed-by` relationship indicates that the identified consumer
Resource is configured to access a filesystem through the source mount
relationship resource. It describes the same configured consumer–mount
association as [`iri:accesses-mount`](./accesses-mount.md), viewed from the mount.

The mount identifies the particular filesystem exposure and configuration
through which the filesystem is accessed. It can carry information such as
the mount path, access mode, protocol, mount options, and consuming-system
relationship that does not belong solely to the filesystem Resource.

The relationship MUST NOT be interpreted as indicating current mount
availability, endpoint reachability, credential validity, unrestricted read or
write access, or current filesystem use or transfer activity. It does not grant
authorization or establish eligibility for any operation-affordance relation.

## 3. Source and Target Representation

The relationship MUST originate from a Resource whose `resource_type` is
exactly:

```text
urn:doe-iri:resource:storage:mount
```

The source is a mount relationship Resource representing configured filesystem
exposure. It is not a direct filesystem, operation entry point, or endpoint.

The relationship MUST target a conforming DOE-IRI `Resource` that represents
an actual configured filesystem consumer through the source mount. The
consumer's Resource Type MUST be valid under the governing registration or
delegation rules. A valid Resource Type alone is insufficient: the represented
Resource MUST have the configured consumer role for that mount.

Illustrative target Resource Types include:

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

The mount's `mount_path` remains in the filesystem namespace of the exactly one
`urn:doe-iri:resource:compute:system` identified by the mount's
[`iri:mounted-on`](./mounted-on.md) relation. An `iri:accessed-by` link to a
service, node, or other consumer does not relocate that path into the target
Resource's own namespace or change the mount's consuming-system identity.

The target is a Resource representation, not an operation entry point or
endpoint. A HAL target `profile`, when supplied, MUST describe that actual
target. Use the generic Resource profile,
`https://iri.science/profiles/status/resource`, unless the actual target's more
specific type and applicable specialized profile are established. For example,
a known DTN target can use
`https://iri.science/profiles/resource-definition/service/dtn`. Neither the
mount source profile nor the relation URI describes the consumer target.

## 4. Cardinality

A mount Resource MAY identify zero, one, or multiple configured consumer
Resources:

```text
Filesystem Mount  -- iri:accessed-by -->  Consumer Resource
        1                    0..*
```

The use of `0..*` permits facilities to represent a mount without exposing its
configured consumers and to represent multiple consumers of the same
filesystem exposure. This does not change the mount's exactly-one
`iri:mounted-on` compute-system target.

`iri:accessed-by` and [`iri:accesses-mount`](./accesses-mount.md) describe the
same configured consumer–mount association in opposite directions.
Advertisement of either direction is independently optional; a provider is
not required to publish a reciprocal link or an exhaustive list of consumers
or mounts. When both relations describe the same configuration, they MUST
agree about the consumer–mount association. This consistency requirement does
not require matching or exhaustive visible link sets.

## 5. Static and Dynamic Semantics

`iri:accessed-by` describes relatively static configured access topology.
Subject to authorization-sensitive visibility, the relationship SHOULD remain
present across ordinary operational state changes such as temporary mount
unavailability, endpoint failure, credential expiration, authorization outcome
changes, or periods without filesystem use or transfer activity.

Current mount status, endpoint reachability, credential validity,
authorization outcomes, and active transfer activity are outside the semantics
of this relation. When represented, they are governed by the applicable IRI
API, security, and Resource Definition Profile contracts.

## 6. Authorization and Visibility

Authorization MAY affect visibility of configured access topology. A provider
MAY expose a mount Resource while omitting individual `iri:accessed-by` targets
for requesters that are not permitted to discover the relevant consumer or
access configuration.

The absence of visible targets MUST NOT be interpreted as proof that the mount
has no configured consumers. Omission of either direction can reflect optional
advertisement, partial publication, or authorization filtering; absence is not
a negative assertion about the association or proof that the inverse is
inconsistent. A visible mount does not by itself identify every Resource
configured to access it.

## 7. Cross-Relation Guidance

Clients MAY discover a configured association from a mount's advertised
`iri:accessed-by` link or a consumer's advertised
[`iri:accesses-mount`](./accesses-mount.md) link. Clients MUST NOT infer
configured access solely from a Resource Type, hosting, containment, or a
mount's `iri:mounted-on` relation. In particular, the combination of
`iri:hosted-on` and `iri:mounted-on` does not establish access even when the
service and mount are associated with the same compute infrastructure.

The source mount identifies the particular exposure through which the consumer
is configured to access the filesystem. A filesystem can have multiple mount
relationship Resources with different paths, protocols, access modes, or
consuming systems. Neither direction changes operation-affordance source-type
or applicability restrictions.

## 8. HAL Representation

This illustrative partial mount Resource identifies a known compute-node
consumer, a known DTN consumer, and another consumer whose specialization is
not established here. The first two targets use their applicable specialized
profiles; the third uses the generic Resource profile. Other required Resource
fields are omitted for clarity. The `mount_path` belongs to the `pioneer`
compute-system namespace identified by `iri:mounted-on`.

```json
{
  "id": "pioneer-scratch-mount",
  "resource_type": "urn:doe-iri:resource:storage:mount",
  "attributes": {
    "mount_path": "/scratch"
  },
  "_links": {
    "curies": [
      { "name": "iri", "href": "https://iri.science/rels/{rel}", "templated": true }
    ],
    "self": { "href": "/api/v2/status/resources/pioneer-scratch-mount", "profile": "https://iri.science/profiles/resource-definition/storage/mount" },
    "iri:mounted-on": { "href": "/api/v2/status/resources/pioneer", "profile": "https://iri.science/profiles/resource-definition/compute/system" },
    "iri:accessed-by": [
      { "href": "/api/v2/status/resources/pioneer-login01", "profile": "https://iri.science/profiles/resource-definition/compute/node" },
      { "href": "/api/v2/status/resources/pioneer-dtn", "profile": "https://iri.science/profiles/resource-definition/service/dtn" },
      { "href": "/api/v2/status/resources/analysis-consumer", "profile": "https://iri.science/profiles/status/resource" }
    ]
  }
}
```

The example does not require any of these consumers to advertise a reciprocal
link and does not assert that all configured consumers are visible.

---

*DOE Integrated Research Infrastructure — Link Relation: accessed-by*
