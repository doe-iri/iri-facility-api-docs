# Link Profile: `iri:hasGPU`

This document defines the `iri:hasGPU` relationship used by the DOE-IRI compute resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:hasGPU` |
| Semantic meaning | Indicates that the compute node contains, provides, or is associated with the identified GPU resource. |
| Source representation type | `urn:doe-iri:resource:compute:node` |
| Target representation type | `urn:doe-iri:resource:compute:gpu` |
| Cardinality | `0..*` targets from a compute-node resource. |
| Target stability | Static resource representation. The target identifies a GPU resource independent of current utilization, memory consumption, health, or allocation. |
| Authorization affects visibility | Yes. GPU-level topology MAY be omitted when the requester is not authorized to discover accelerator-level details. |
| Target classification | Resource |
| Relationship volatility | Relatively static hardware/topology relationship. Operational GPU state is separate. |

## 2. Semantic Meaning

The `iri:hasGPU` relationship identifies GPU or accelerator resources associated with the source compute node.

GPU-specific characteristics such as device memory, programming interfaces, vendor, model, and vendor-defined architecture belong to the target GPU resource rather than being embedded into the relationship.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:compute:node
```

and MUST target:

```text
urn:doe-iri:resource:compute:gpu
```

The target is a resource representation, not a state object, operation entry point, or relationship resource.

## 4. Cardinality

A compute node MAY expose zero, one, or multiple GPU resources:

```text
Compute Node  -- iri:hasGPU -->  GPU
     1                0..*
```

A node with no GPU targets may be CPU-only, or the facility may have chosen not to expose individual accelerator topology. Clients SHOULD use the node's `gpu_count` attribute, when present, to distinguish these cases where necessary.

## 5. Static and Dynamic Semantics

The relationship describes relatively stable accelerator topology. It SHOULD NOT be added or removed solely because a GPU is allocated, idle, unhealthy, or temporarily unavailable.

Current utilization, allocated memory, temperature, health, workload assignment, and availability belong in state.

## 6. Authorization and Visibility

Authorization MAY affect visibility of GPU-level topology. A provider MAY omit GPU targets while still exposing aggregate accelerator counts on the node or compute-system resource.

Absence of visible GPU targets MUST NOT be interpreted as evidence that no accelerators exist unless the applicable aggregate attributes also indicate zero.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:hasGPU": [
      {
        "href": "/api/v2/status/resources/node-001-gpu-0"
      },
      {
        "href": "/api/v2/status/resources/node-001-gpu-1"
      }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: hasGPU*
