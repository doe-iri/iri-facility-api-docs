# Link Profile: `iri:has-node`

This document defines the `iri:has-node` relationship used by the DOE-IRI compute resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-node` |
| Semantic meaning | Indicates that the identified compute node participates in or is managed as part of the source compute system. |
| Source representation type | `urn:doe-iri:resource:compute:system` |
| Target representation type | `urn:doe-iri:resource:compute:node` |
| Cardinality | `0..*` targets from a compute-system resource. |
| Target stability | Static resource representation. The target identifies a compute-node resource whose identity is independent of current health, allocation, or availability. |
| Authorization affects visibility | Yes. The relationship or individual node targets MAY be omitted when the requester is not authorized to discover node-level topology. |
| Target classification | Resource |
| Relationship volatility | Relatively static topology/configuration. Changes when system membership or represented topology changes; operational node state is separate. |

## 2. Semantic Meaning

The `iri:has-node` relationship indicates that the source compute system contains, manages, or otherwise presents the identified compute node as part of the system's represented topology.

The relationship separates system identity from node identity. System-level characteristics belong to the source compute-system resource, while node-specific characteristics belong to the target compute-node resource.

The relationship MUST NOT be interpreted as indicating that the node is currently available for workload execution.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:compute:system
```

and MUST target:

```text
urn:doe-iri:resource:compute:node
```

The target is a resource representation, not a state object, operation entry point, or relationship resource.

## 4. Cardinality

A compute system MAY expose zero, one, or multiple node resources:

```text
Compute System  -- iri:has-node -->  Compute Node
      1                  0..*
```

The use of `0..*` permits facilities to expose aggregate system information without exposing individual node topology.

No inverse-cardinality requirement is imposed by this link profile.

## 5. Static and Dynamic Semantics

`iri:has-node` describes relatively stable compute topology. The relationship SHOULD remain present across ordinary operational state changes such as node allocation, maintenance, drain, failure, or temporary unavailability.

Current node health, workload activity, allocation state, and availability SHOULD be represented through the node's state resource.

## 6. Authorization and Visibility

Authorization MAY affect visibility of node topology. A provider MAY expose a compute system while omitting individual `iri:has-node` targets for requesters that are not permitted to discover node-level infrastructure details.

The absence of visible node targets MUST NOT be interpreted as proof that the compute system contains no nodes.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:has-node": [
      {
        "href": "/api/v2/status/resources/node-001"
      },
      {
        "href": "/api/v2/status/resources/node-002"
      }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: hasNode*
