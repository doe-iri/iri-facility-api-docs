# Link Profile: `iri:hostedOn`

This document defines the `iri:hostedOn` relationship used by the DOE-IRI service resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:hostedOn` |
| Semantic meaning | Indicates that the identified compute system or compute node provides hosting infrastructure for the source service. |
| Source representation type | `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference` |
| Target representation type | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` |
| Cardinality | `0..*` targets from a service resource. |
| Target stability | Static resource representation. The target identifies hosting infrastructure independently of current routing, live replica placement, health, or availability. |
| Authorization affects visibility | Yes. The relationship or individual targets MAY be omitted when the requester is not authorized to discover service-hosting topology. |
| Target classification | Resource |
| Relationship volatility | Relatively static hosting topology. Changes when represented hosting infrastructure changes; operational service and infrastructure state is separate. |

## 2. Semantic Meaning

The `iri:hostedOn` relationship indicates that the target compute system or compute node provides hosting infrastructure for the source DTN or inference service.

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

The target is a compute resource representation, not a state object, operation entry point, relationship resource, endpoint, deployment, or live replica.

## 4. Cardinality

A service MAY identify zero, one, or multiple hosting infrastructure resources:

```text
Service  -- iri:hostedOn -->  Compute System or Compute Node
   1                0..*
```

The use of `0..*` permits facilities to represent services without exposing hosting topology and to represent services hosted across multiple systems or nodes.

No inverse-cardinality requirement is imposed by this link profile.

## 5. Static and Dynamic Semantics

`iri:hostedOn` describes relatively static hosting topology. The relationship SHOULD remain present across ordinary operational state changes such as service degradation, infrastructure maintenance, node failure, temporary unavailability, routing changes, or replica changes.

Current health, availability, request routing, replica placement, workload activity, and endpoint reachability SHOULD be represented through the applicable resource-state mechanisms.

## 6. Authorization and Visibility

Authorization MAY affect visibility of service-hosting topology. A provider MAY expose a service while omitting individual `iri:hostedOn` targets for requesters that are not permitted to discover the relevant compute infrastructure.

The absence of visible targets MUST NOT be interpreted as proof that the service has no hosting infrastructure.

## 7. HAL Representation

A service hosted on one compute system can use a singular link object:

```json
{
  "_links": {
    "iri:hostedOn": {
      "href": "/api/v2/status/resources/perlmutter"
    }
  }
}
```

A service hosted across multiple compute nodes can use an array of link objects:

```json
{
  "_links": {
    "iri:hostedOn": [
      { "href": "/api/v2/status/resources/node-001" },
      { "href": "/api/v2/status/resources/node-002" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: hostedOn*
