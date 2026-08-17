# Link Profile: `iri:has-mount`

This document defines the `iri:has-mount` relationship used by the DOE-IRI storage resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-mount` |
| Semantic meaning | Indicates that a filesystem is exposed through the identified mount relationship resource. |
| Source representation type | `urn:doe-iri:resource:storage:filesystem` |
| Target representation type | `urn:doe-iri:resource:storage:mount` |
| Cardinality | `0..*` targets from a filesystem resource. |
| Target stability | Relatively static relationship resource. The target represents configured filesystem exposure, not current mount health or availability. |
| Authorization affects visibility | Yes. Mount resources MAY be omitted when the requester is not authorized to discover the mount or its associated consuming system. |
| Target classification | Relationship resource |
| Relationship volatility | Configuration/topology. Mount definitions may be added or removed as filesystem exposure changes, but operational mounted/unmounted state belongs in state. |

## 2. Semantic Meaning

The `iri:has-mount` relationship indicates that the source filesystem is exposed through the identified mount resource.

A mount is modeled as a relationship resource because it carries information that belongs neither solely to the filesystem nor solely to the consuming compute system. Typical mount-specific characteristics include the namespace location, access mode, filesystem protocol, and implementation-specific mount options.

The mount resource allows one filesystem to be exposed differently on multiple consuming systems without duplicating the filesystem resource.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:filesystem
```

and MUST target:

```text
urn:doe-iri:resource:storage:mount
```

The mount target represents the relationship/configuration through which the filesystem is exposed. It is not a second filesystem representation and is not itself the consuming compute system.

The consuming system is identified by the mount resource's `iri:mounted-on` relationship.

## 4. Cardinality

A filesystem MAY have zero, one, or multiple mount resources:

```text
Filesystem  -- iri:has-mount -->  Mount
    1                0..*
```

Multiple mount targets allow the same filesystem to be exposed at different paths, through different protocols, with different access modes, or on different consuming systems.

Each mount resource SHOULD describe one filesystem-to-consuming-system exposure. A mount resource therefore SHOULD normally be referenced by one filesystem.

## 5. Static and Dynamic Semantics

The mount target represents a relatively stable exposure configuration.

The existence of `iri:has-mount` MUST NOT be interpreted as proof that the mount is currently active, reachable, healthy, or usable. Current mount status belongs in the mount resource's state representation.

## 6. Authorization and Visibility

Authorization MAY affect mount visibility because a mount can reveal both filesystem topology and the identity of consuming systems.

A provider MAY omit a mount target when the requester is not authorized to discover the mount or related compute topology.

The absence of visible mount targets MUST NOT be interpreted as proof that the filesystem is not exposed elsewhere.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:has-mount": [
      { "href": "/api/v2/status/resources/perlmutter-scratch-mount" },
      { "href": "/api/v2/status/resources/analysis-scratch-mount" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: has-mount*
