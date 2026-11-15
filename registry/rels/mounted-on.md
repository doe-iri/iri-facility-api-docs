# IRI Link Relation: `mounted-on`

**Relation URI:** `https://iri.science/rels/mounted-on`<br>
**CURIE:** `iri:mounted-on`<br>
**Status:** Draft<br>
**Version:** 2.0.0<br>
**Source representation type:** `urn:doe-iri:resource:storage:mount`<br>
**Source resource type:** `urn:doe-iri:resource:storage:mount`<br>
**Target representation type:** `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:service:dtn`<br>
**Target resource type:** `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:service:dtn`

This document defines the `iri:mounted-on` relationship used by the DOE-IRI storage resource model.

The canonical relation URI is `https://iri.science/rels/mounted-on`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:mounted-on` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:mounted-on` |
| Relation URI | `https://iri.science/rels/mounted-on` |
| Semantic meaning | Identifies a consuming compute system or DTN service to which the filesystem represented by the mount resource is exposed. |
| Source representation type | `urn:doe-iri:resource:storage:mount` |
| Target representation type | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:service:dtn` |
| Cardinality | `1..*` targets for a valid mount resource. |
| Inverse relation | [`iri:accesses-mount`](./accesses-mount.md) |
| Target stability | Static resource representation. Each target identifies a consumer of the exposure; current mount condition is outside the semantics of this relation. |
| Authorization affects visibility | Yes. A target MAY be hidden when the requester is not authorized to discover that consumer or topology. |
| Target classification | Resource |
| Relationship volatility | Relatively static configuration/topology. It changes when the mount's consumers change, not when mount health changes. |

## 2. Semantic Meaning

The `iri:mounted-on` relationship identifies a consumer of the exposure represented by the source mount resource: a compute system whose filesystem namespace contains that exposure, or a DTN service configured to use it for transfer operations.

The mount's own attributes describe how the filesystem is exposed—for example, `mount_path`, access mode, or filesystem protocol—while `iri:mounted-on` identifies the consumers to which those characteristics apply. The [Filesystem Mount profile](../profiles/resource-definition/storage/mount.md) defines how `mount_path` applies to each kind of consumer.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:mount
```

and MUST target a resource of one of these types:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:service:dtn
```

The target is the consumer's Resource representation, not an operation endpoint. A DTN target identifies the data-transfer service, not a host or node; where the service runs is represented separately by `iri:hosted-on`.

The target type varies, so a `profile` on a link object identifies that target's own representation.

## 4. Cardinality

A mount resource represents one configured filesystem exposure, which one or more consumers can share. A valid mount resource therefore MUST identify at least one `iri:mounted-on` target:

```text
Mount  -- iri:mounted-on -->  Compute System or DTN Service
  1              1..*
```

The relation is plural, so its value is always an array of link objects, including when the mount has one target.

A mount MAY name several consumers only when its attributes describe the exposure for all of them, as the [Filesystem Mount profile](../profiles/resource-definition/storage/mount.md) defines. When they do not, for example when compute systems see the filesystem at different paths or consumers use different access modes, separate mount resources MUST be used.

## 5. Static and Dynamic Semantics

The relationship describes configured topology, not current operational state.

The presence of `iri:mounted-on` means that the mount resource is defined in relation to the identified consumer. It does not mean that the mount is currently active or usable.

Mounted/unmounted status, accessibility, errors, or degradation are outside the semantics of this relation and, when represented, are governed by the applicable IRI API contract and Resource Definition Profile.

## 6. Authorization and Visibility

Authorization MAY affect visibility of any target.

When the source mount is visible but a consumer is not discoverable by the requester, the provider MAY omit that target or otherwise restrict the relationship according to facility authorization policy. The absence of a visible target MUST NOT be interpreted as proof that a resource does not consume the mount.

Because at least one `iri:mounted-on` target is required for the semantic completeness of a mount resource, implementations SHOULD prefer to hide the mount resource itself when exposing it without any visible target would produce an unusable or misleading representation.

## 7. Cross-Relation Guidance

`iri:accesses-mount` is the inverse of this relation: `Mount -- iri:mounted-on --> Consumer` and `Consumer -- iri:accesses-mount --> Mount` state the same configured relationship. Providers SHOULD publish both directions so that clients can start from either resource.

A link in either direction is sufficient to establish the relationship. A missing inverse link MUST NOT be interpreted as denying it, because the provider may not publish it or authorization may hide it.

## 8. HAL Representation

```json
{
  "_links": {
    "iri:mounted-on": [
      {
        "href": "/api/v2/status/resources/perlmutter",
        "profile": "https://iri.science/profiles/resource-definition/compute/system"
      },
      {
        "href": "/api/v2/status/resources/perlmutter-dtn",
        "profile": "https://iri.science/profiles/resource-definition/service/dtn"
      }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: mounted-on*
