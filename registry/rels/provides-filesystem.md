# IRI Link Relation: `provides-filesystem`

**Relation URI:** `https://iri.science/rels/provides-filesystem`<br>
**CURIE:** `iri:provides-filesystem`<br>
**Status:** Draft<br>
**Version:** 1.0.0<br>
**Source representation type:** `urn:doe-iri:resource:storage:system`<br>
**Source resource type:** `urn:doe-iri:resource:storage:system`<br>
**Target representation type:** `urn:doe-iri:resource:storage:filesystem`<br>
**Target resource type:** `urn:doe-iri:resource:storage:filesystem`

This document defines the `iri:provides-filesystem` relationship used by the DOE-IRI storage resource model.

The canonical relation URI is `https://iri.science/rels/provides-filesystem`.
With the canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:provides-filesystem` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:provides-filesystem` |
| Relation URI | `https://iri.science/rels/provides-filesystem` |
| Semantic meaning | Indicates that a storage system provides the identified logical filesystem resource. |
| Source representation type | `urn:doe-iri:resource:storage:system` |
| Target representation type | `urn:doe-iri:resource:storage:filesystem` |
| Cardinality | `0..*` targets from a storage-system resource. |
| Target stability | Static resource representation. The target identifies a logical filesystem resource whose identity is expected to remain stable across ordinary operational state changes. |
| Authorization affects visibility | Yes. The relationship or individual targets MAY be omitted when the requester is not authorized to discover the target resource. |
| Target classification | Resource |
| Relationship volatility | Relatively static topology/configuration. Changes when the set of filesystems provided by the storage system changes; it is not intended to represent current filesystem health or availability. |

## 2. Semantic Meaning

The `iri:provides-filesystem` relationship indicates that the source storage system provides, hosts, or otherwise makes available the identified logical filesystem resource.

The relationship separates infrastructure identity from logical storage identity. Characteristics of the storage infrastructure belong to the source `urn:doe-iri:resource:storage:system` resource, while characteristics of the logical filesystem belong to the target `urn:doe-iri:resource:storage:filesystem` resource.

A client SHOULD NOT infer filesystem characteristics such as tier, filesystem technology, protocols, capabilities, capacity, media type, health, or current availability solely from the presence of this relationship. Those characteristics SHOULD be obtained from the target filesystem Resource according to the applicable IRI API contract and Resource Definition Profile.

## 3. Source and Target Representation

The relationship MUST originate from a resource whose `resource_type` is:

```text
urn:doe-iri:resource:storage:system
```

The relationship MUST target a resource whose `resource_type` is:

```text
urn:doe-iri:resource:storage:filesystem
```

The target is a logical storage Resource, not a mount, operation endpoint, or embedded filesystem description.

## 4. Cardinality

A storage system MAY provide zero, one, or multiple filesystem resources. The forward cardinality is therefore:

```text
Storage System  -- iri:provides-filesystem -->  Filesystem
      1                          0..*
```

No inverse-cardinality requirement is imposed by this link-relation definition.

## 5. Static and Dynamic Semantics

The relationship represents a relatively stable storage topology. It describes which logical filesystem resources a storage system provides.

The relationship MUST NOT be used to indicate whether the filesystem is currently healthy, reachable, writable, mounted, or available for new work. Those conditions are outside the semantics of this relation and, when represented, are governed by the applicable IRI API contract and Resource Definition Profile.

## 6. Authorization and Visibility

Authorization MAY affect whether a requester can see the relationship or an individual target.

If the source storage system is visible but the requester cannot discover a target filesystem, the provider MAY omit that target from the relationship. The absence of a target MUST NOT be interpreted as proof that no additional filesystem resources exist.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:provides-filesystem": [
      { "href": "/api/v2/status/resources/scratch", "profile": "https://iri.science/profiles/resource-definition/storage/filesystem" },
      { "href": "/api/v2/status/resources/home", "profile": "https://iri.science/profiles/resource-definition/storage/filesystem" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: provides-filesystem*
