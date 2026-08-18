# IRI Link Relation: `has-cpu`

**Relation URI:** `https://iri.science/rels/has-cpu`\
**CURIE:** `iri:has-cpu`\
**Status:** Draft\
**Version:** 1.0.0<br>
**Source representation type:** `urn:doe-iri:resource:compute:node`<br>
**Source resource type:** `urn:doe-iri:resource:compute:node`<br>
**Target representation type:** `urn:doe-iri:resource:compute:cpu`<br>
**Target resource type:** `urn:doe-iri:resource:compute:cpu`

This document defines the `iri:has-cpu` relationship used by the DOE-IRI compute resource model.

The canonical relation URI is `https://iri.science/rels/has-cpu`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:has-cpu`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-cpu` |
| Relation URI | `https://iri.science/rels/has-cpu` |
| Semantic meaning | Indicates that the compute node contains, provides, or is associated with the identified CPU resource. |
| Source representation type | `urn:doe-iri:resource:compute:node` |
| Target representation type | `urn:doe-iri:resource:compute:cpu` |
| Cardinality | `0..*` targets from a compute-node resource. |
| Target stability | Static resource representation. The target identifies a CPU resource independent of current utilization, frequency, health, or allocation. |
| Authorization affects visibility | Yes. CPU-level topology MAY be omitted when the requester is not authorized to discover processor-level details. |
| Target classification | Resource |
| Relationship volatility | Relatively static hardware/topology relationship. Operational CPU state is separate. |

## 2. Semantic Meaning

The `iri:has-cpu` relationship identifies CPU resources associated with the source compute node.

CPU-specific characteristics such as processor architecture, core count, thread count, clock characteristics, vendor, and model belong to the target CPU resource rather than being embedded into the link relationship.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:compute:node
```

and MUST target:

```text
urn:doe-iri:resource:compute:cpu
```

The target is a resource representation, not a state object, operation entry point, or relationship resource.

## 4. Cardinality

A compute node MAY expose zero, one, or multiple CPU resources:

```text
Compute Node  -- iri:has-cpu -->  CPU
     1                0..*
```

A facility MAY expose aggregate CPU counts on the node without exposing individual CPU resources, so zero visible CPU targets does not necessarily mean that the node has no processors.

## 5. Static and Dynamic Semantics

The relationship describes relatively stable processor topology. It SHOULD NOT change solely because CPU cores are allocated, idle, unavailable to a particular user, frequency-throttled, or otherwise affected by dynamic operational conditions.

Current utilization, frequency, health, temperature, allocation, or availability belongs in state.

## 6. Authorization and Visibility

Authorization MAY affect visibility of CPU-level topology. A provider MAY omit CPU targets while still exposing aggregate processor counts on the node resource.

Absence of visible CPU targets MUST NOT be interpreted as evidence that the node lacks CPUs.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:has-cpu": [
      {
        "href": "/api/v2/status/resources/node-001-cpu-0"
      },
      {
        "href": "/api/v2/status/resources/node-001-cpu-1"
      }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: has-cpu*
