# Link Profile: `iri:provides-object`

This document defines the `iri:provides-object` relationship used by the DOE-IRI storage resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:provides-object` |
| Semantic meaning | Indicates that a storage system provides the identified logical object-storage resource. |
| Source representation type | `urn:doe-iri:resource:storage:system` |
| Target representation type | `urn:doe-iri:resource:storage:object` |
| Cardinality | `0..*` targets from a storage-system resource. |
| Target stability | Static resource representation. The target identifies a logical object-storage resource independent of current endpoint health or service state. |
| Authorization affects visibility | Yes. The relationship or individual targets MAY be omitted when the requester is not authorized to discover the target resource. |
| Target classification | Resource |
| Relationship volatility | Relatively static topology/configuration. Changes when the set of logical object-storage resources provided by the storage system changes. |

## 2. Semantic Meaning

The `iri:provides-object` relationship indicates that the source storage system provides the identified logical object-storage resource.

The relationship separates storage infrastructure from the logical object service or namespace consumed through object-storage APIs. Object-specific characteristics such as supported APIs, access endpoints, implementation technology, consistency semantics, capabilities, tier, and backing media belong to the target object resource.

Service endpoints are not the target of `iri:provides-object`; they are access characteristics of the object-storage resource unless separately modeled as resources by a future profile.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:system
```

and MUST target:

```text
urn:doe-iri:resource:storage:object
```

The target is the logical object-storage resource, not an individual bucket, object, endpoint URL, state object, or operation entry point.

## 4. Cardinality

A storage system MAY provide zero, one, or multiple object-storage resources:

```text
Storage System  -- iri:provides-object -->  Object Storage
      1                       0..*
```

No inverse-cardinality requirement is imposed by this link profile.

## 5. Static and Dynamic Semantics

The relationship describes relatively stable storage topology.

Endpoint reachability, request latency, utilization, capacity availability, and service health are dynamic characteristics and SHOULD be represented through the relevant state mechanisms rather than by treating `iri:provides-object` as an availability indicator.

## 6. Authorization and Visibility

Authorization MAY affect relationship visibility. A provider MAY omit target object resources that the requester is not authorized to discover.

Absence of the link or a particular target MUST NOT be interpreted as proof that no additional object-storage resources exist.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:provides-object": [
      { "href": "/api/v2/status/resources/science-object-store" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: providesObject*
