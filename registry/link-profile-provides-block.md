# Link Profile: `iri:provides-block`

This document defines the `iri:provides-block` relationship used by the DOE-IRI storage resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:provides-block` |
| Semantic meaning | Indicates that a storage system provides the identified logical block-storage resource. |
| Source representation type | `urn:doe-iri:resource:storage:system` |
| Target representation type | `urn:doe-iri:resource:storage:block` |
| Cardinality | `0..*` targets from a storage-system resource. |
| Target stability | Static resource representation. The target identifies a logical block resource whose identity is independent of its current attachment or operational state. |
| Authorization affects visibility | Yes. The relationship or individual targets MAY be omitted when the requester is not authorized to discover the target resource. |
| Target classification | Resource |
| Relationship volatility | Relatively static topology/configuration. Changes when the logical block resources provided by the storage system change. |

## 2. Semantic Meaning

The `iri:provides-block` relationship indicates that the source storage system provides the identified logical block-storage resource.

The relationship separates the infrastructure that implements storage from the logical volume presented for consumption. Storage-system characteristics belong to the source resource, while block-specific characteristics such as protocol, provisioning model, access mode, capabilities, logical capacity, tier, and backing media belong to the target block resource.

The relationship does not indicate that the block resource is currently attached to a host or compute system.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:system
```

and MUST target:

```text
urn:doe-iri:resource:storage:block
```

The target represents the logical block-storage resource itself, not an attachment, device path, state object, or operation endpoint.

## 4. Cardinality

A storage system MAY provide zero, one, or multiple block-storage resources:

```text
Storage System  -- iri:provides-block -->  Block Storage
      1                      0..*
```

No inverse-cardinality requirement is imposed by this link profile.

## 5. Static and Dynamic Semantics

`iri:provides-block` describes relatively stable provider topology.

Current attachment, I/O activity, path health, utilization, and availability are dynamic concerns and SHOULD NOT be encoded by adding or removing this relationship solely because operational state changes.

## 6. Authorization and Visibility

Authorization MAY affect relationship visibility. A provider MAY omit block resources that the requester is not authorized to discover.

An omitted target MUST NOT be interpreted as evidence that the storage system provides no additional block resources.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:provides-block": [
      { "href": "/api/v2/status/resources/project-volume-001" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: provides-block*
