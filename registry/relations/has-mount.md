# IRI Link Relation: `has-mount`

**Relation URI:** `https://iri.science/rels/has-mount`<br>
**CURIE:** `iri:has-mount`<br>
**Status:** Draft<br>
**Version:** 1.0.0<br>
**Source representation type:** `urn:doe-iri:resource:storage:filesystem`<br>
**Target representation type:** `urn:doe-iri:resource:storage:mount`<br>
**Target resource type:** `urn:doe-iri:resource:storage:mount`<br>
**Target representation profile:** `https://iri.science/profiles/resource-definition/storage/mount`

## 1. Link Relation Definition

This document defines the `iri:has-mount` link relation used by the DOE-IRI
storage resource model. Its canonical relation URI is:

```text
https://iri.science/rels/has-mount
```

When a HAL representation declares the IRI CURIE as:

```json
{
  "name": "iri",
  "href": "https://iri.science/rels/{rel}",
  "templated": true
}
```

the relation:

```text
iri:has-mount
```

expands to:

```text
https://iri.science/rels/has-mount
```

The relation URI identifies the semantics of the link relation. It is distinct
from the profile URI associated with a target mount representation.

## 2. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-mount` |
| Relation URI | `https://iri.science/rels/has-mount` |
| Semantic meaning | Indicates that a filesystem is exposed through the identified mount relationship resource. |
| Source representation type | `urn:doe-iri:resource:storage:filesystem` |
| Target representation type | `urn:doe-iri:resource:storage:mount` |
| Target representation profile | `https://iri.science/profiles/resource-definition/storage/mount` |
| Cardinality | `0..*` targets from a filesystem resource. |
| Target stability | Relatively static relationship resource. The target represents configured filesystem exposure, not current mount health or availability. |
| Authorization affects visibility | Yes. Mount resources MAY be omitted when the requester is not authorized to discover the mount or its associated consuming system. |
| Target classification | Relationship resource |
| Relationship volatility | Configuration/topology. Mount definitions may be added or removed as filesystem exposure changes, but operational mounted/unmounted state belongs in state. |

## 3. Semantic Meaning

The `iri:has-mount` relationship indicates that the source filesystem is
exposed through the identified mount resource.

A mount is modeled as a relationship resource because it carries information
that belongs neither solely to the filesystem nor solely to the consuming
compute system. Typical mount-specific characteristics include the namespace
location, access mode, filesystem protocol, and implementation-specific mount
options.

The mount resource allows one filesystem to be exposed differently on multiple
consuming systems without duplicating the filesystem resource.

## 4. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:filesystem
```

and MUST target:

```text
urn:doe-iri:resource:storage:mount
```

The mount target represents the relationship/configuration through which the
filesystem is exposed. It is not a second filesystem representation and is not
itself the consuming compute system.

The consuming system is identified by the mount resource's `iri:mounted-on`
relationship.

A representation of the target mount resource MAY advertise the profile:

`https://iri.science/profiles/resource-definition/storage/mount`

The profile identifies the semantic contract of the target mount
representation. It does not define the semantics of the `iri:has-mount`
relation itself; those semantics are identified by
`https://iri.science/rels/has-mount`.

## 5. Cardinality

A filesystem MAY have zero, one, or multiple mount resources:

```text
Filesystem  -- iri:has-mount -->  Mount
    1                0..*
```

Multiple mount targets allow the same filesystem to be exposed at different
paths, through different protocols, with different access modes, or on
different consuming systems.

Each mount resource SHOULD describe one filesystem-to-consuming-system
exposure. A mount resource therefore SHOULD normally be referenced by one
filesystem.

## 6. Static and Dynamic Semantics

The mount target represents a relatively stable exposure configuration.

The existence of `iri:has-mount` MUST NOT be interpreted as proof that the
mount is currently active, reachable, healthy, or usable. Current mount status
belongs in the mount resource's state representation.

## 7. Authorization and Visibility

Authorization MAY affect mount visibility because a mount can reveal both
filesystem topology and the identity of consuming systems.

A provider MAY omit a mount target when the requester is not authorized to
discover the mount or related compute topology.

The absence of visible mount targets MUST NOT be interpreted as proof that the
filesystem is not exposed elsewhere.

## 8. HAL Representation

```json
{
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch filesystem",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    }
  }
}
```

- `iri:has-mount` identifies the link relation and expands through the IRI
  CURIE to `https://iri.science/rels/has-mount`.
- `href` identifies the actual target mount resource instance.
- `type` identifies the expected representation media type.
- `profile` identifies the semantic profile of the target mount
  representation.

The relation URI and profile URI serve different purposes and MUST NOT be
treated as interchangeable identifiers.

---

*DOE Integrated Research Infrastructure — Link Relation: has-mount*
