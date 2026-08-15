# Link Profile: `iri:provides-filesystem`

This document defines the `iri:provides-filesystem` relationship used by the DOE-IRI storage resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:provides-filesystem` |
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

A client SHOULD NOT infer filesystem characteristics such as tier, filesystem technology, protocols, capabilities, capacity, media type, health, or current availability solely from the presence of this relationship. Those characteristics SHOULD be obtained from the target filesystem resource or its corresponding state representation.

## 3. Source and Target Representation

The relationship MUST originate from a resource whose `resource_type` is:

```text
urn:doe-iri:resource:storage:system
```

The relationship MUST target a resource whose `resource_type` is:

```text
urn:doe-iri:resource:storage:filesystem
```

The target is a logical storage resource, not a mount, state object, operation endpoint, or embedded filesystem description.

## 4. Cardinality

A storage system MAY provide zero, one, or multiple filesystem resources. The forward cardinality is therefore:

```text
Storage System  -- iri:provides-filesystem -->  Filesystem
      1                          0..*
```

No inverse-cardinality requirement is imposed by this link profile.

## 5. Static and Dynamic Semantics

The relationship represents relatively stable storage topology. It describes which logical filesystem resources are provided by a storage system.

The relationship MUST NOT be used to indicate whether the filesystem is currently healthy, reachable, writable, mounted, or available for new work. Such information is operational state and SHOULD be represented through the applicable resource-state mechanism.

## 6. Authorization and Visibility

Authorization MAY affect whether the relationship or an individual target is visible to a requester.

If the source storage system is visible but a target filesystem is not discoverable by the requester, the provider MAY omit that target from the relationship. The absence of a target MUST NOT be interpreted as proof that no additional filesystem resources exist.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:provides-filesystem": [
      { "href": "/api/v2/status/resources/scratch" },
      { "href": "/api/v2/status/resources/home" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: providesFilesystem*
