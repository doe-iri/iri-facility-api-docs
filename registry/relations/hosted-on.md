# IRI Link Relation: `hosted-on`

**Relation URI:** `https://iri.science/rels/hosted-on`<br>
**CURIE:** `iri:hosted-on`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference`<br>
**Source resource type:** `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference`<br>
**Target representation type:** `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node`<br>
**Target resource type:** `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node`

This document defines the `iri:hosted-on` relationship used by the DOE-IRI service resource model.

The canonical relation URI is `https://iri.science/rels/hosted-on`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:hosted-on`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:hosted-on` |
| Relation URI | `https://iri.science/rels/hosted-on` |
| Status | `provisional` |
| Semantic meaning | Indicates that the identified compute system or compute node provides hosting infrastructure for the source service. |
| Source representation type | `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference` |
| Target representation type | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` |
| Cardinality | `0..*` targets from a service resource. |
| Target stability | Static resource representation. The target identifies hosting infrastructure independently of current routing, live replica placement, health, or availability. |
| Authorization affects visibility | Yes. The relationship or individual targets MAY be omitted when the requester is not authorized to discover service-hosting topology. |
| Target classification | Resource |
| Relationship volatility | Relatively static hosting topology. Changes when represented hosting infrastructure changes, not merely when service or infrastructure conditions change. |

## 2. Semantic Meaning

The `iri:hosted-on` relationship indicates that the target compute system or compute node provides hosting infrastructure for the source DTN or inference service.

The relationship separates consumable service identity from the identity of the infrastructure on which the service is hosted. A DTN service does not identify an individual host or compute node, and an inference service does not identify a deployment, endpoint, replica, or accelerator.

The relationship MUST NOT be interpreted as indicating current request routing, live replica placement, health, availability, or that a target is currently serving requests.

## 3. Source and Target Representation

The relationship MUST originate from a resource whose `resource_type` is one of:

```text
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

The relationship MUST target a resource whose `resource_type` is one of:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
```

The target is a compute Resource representation, not an operation entry point, relationship resource, endpoint, deployment, or live replica.

## 4. Cardinality

A service MAY identify zero, one, or multiple hosting infrastructure resources:

```text
Service  -- iri:hosted-on -->  Compute System or Compute Node
   1                0..*
```

The use of `0..*` permits facilities to represent services without exposing hosting topology and to represent services hosted across multiple systems or nodes.

This link-relation definition imposes no inverse-cardinality requirement.

## 5. Static and Dynamic Semantics

`iri:hosted-on` describes relatively static hosting topology. The relationship SHOULD remain present across ordinary operational state changes such as service degradation, infrastructure maintenance, node failure, temporary unavailability, routing changes, or replica changes.

Current health, availability, request routing, replica placement, workload activity, and endpoint reachability are outside the semantics of this relation. When represented, they are governed by the applicable IRI API contract and Resource Definition Profile.

## 6. Authorization and Visibility

Authorization MAY affect visibility of service-hosting topology. A provider MAY expose a service while omitting individual `iri:hosted-on` targets for requesters that are not permitted to discover the relevant compute infrastructure.

The absence of visible targets MUST NOT be interpreted as proof that the service has no hosting infrastructure.

## 7. HAL Representation

A service hosted on one compute system can use a singular link object:

```json
{
  "_links": {
    "iri:hosted-on": {
      "href": "/api/v2/status/resources/perlmutter",
      "profile": "https://iri.science/profiles/resource-definition/compute/system"
    }
  }
}
```

A service hosted across multiple compute nodes can use an array of link objects:

```json
{
  "_links": {
    "iri:hosted-on": [
      { "href": "/api/v2/status/resources/node-001", "profile": "https://iri.science/profiles/resource-definition/compute/node" },
      { "href": "/api/v2/status/resources/node-002", "profile": "https://iri.science/profiles/resource-definition/compute/node" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: hosted-on*
