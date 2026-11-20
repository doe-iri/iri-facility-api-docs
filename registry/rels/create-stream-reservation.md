# IRI Link Relation: `create-stream-reservation`

**Relation URI:** `https://iri.science/rels/create-stream-reservation`<br>
**CURIE:** `iri:create-stream-reservation`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Change controller:** IRI technical subcommittee<br>
**Source representation type:** DOE-IRI `Resource` representation<br>
**Source resource type:** `urn:doe-iri:resource:service:streaming-transport`<br>
**Target representation type:** Reservation-creation operation entry point<br>
**OpenAPI operation:** Planned: `POST /api/v2/streaming/{resource_id}/reservations` (`operationId: createStreamReservation`); not yet in the IRI v2 OpenAPI

This document defines the `iri:create-stream-reservation` operation-affordance relationship proposed by [RFC: Streaming Data Transport Reservations](../../rfc/rfc-streaming-data-transport.md).

The canonical relation URI is `https://iri.science/rels/create-stream-reservation`. With the canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:create-stream-reservation` expands to that URI. The relation URI identifies the link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:create-stream-reservation` |
| Relation URI | `https://iri.science/rels/create-stream-reservation` |
| Status and version | `provisional`, version `1.0.0` |
| Change controller | IRI technical subcommittee |
| Semantic meaning | Identifies the applicable operation entry point for reserving a load balancer instance of the source streaming transport service against a project allocation. |
| Source representation type | DOE-IRI `Resource` representation whose exact `resource_type` is `urn:doe-iri:resource:service:streaming-transport`. |
| Target representation type | Reservation-creation operation entry point. |
| Cardinality | `0..1` link from each eligible streaming transport Resource representation. |
| Applicability | The adapter implements the mapped operation for the represented streaming transport service. |
| Target stability | Configured operation affordance, not a claim that a load balancer instance is free, that the control plane is reachable, or that the requester's allocation suffices. |
| Relationship volatility | Changes when the facility configures or withdraws the adapter operation or changes requester-visible discovery, not solely because operational conditions change. |
| Authorization affects visibility | Yes. The relation MAY be omitted when the requester is not authorized to discover or use the entry point. Presence grants no permission. |
| Omission semantics | Not advertised in this representation; omission does not prove that reservation creation is unsupported everywhere or that the requester can never use it. |
| Target classification | Operation entry point; not an API resource, DOE-IRI typed Resource, relationship Resource, or representation profile. |
| OpenAPI operation | Planned: `POST /api/v2/streaming/{resource_id}/reservations` with `operationId: createStreamReservation`. |
| OpenAPI binding | `x-iri-relation: ["https://iri.science/rels/create-stream-reservation"]` on that Operation Object, once the operation is added to the IRI v2 OpenAPI. |

## 2. Semantic Meaning

Identifies the applicable operation entry point for reserving a load balancer instance of the source streaming transport service against a project allocation. The relation identifies navigation to an applicable affordance. It does not itself specify the HTTP method or request contract, grant permission, prove current capacity, or replace the governing OpenAPI operation contract.

## 3. Source, Target, and Operation Context

The relationship MAY originate only from a Resource whose exact `resource_type` is `urn:doe-iri:resource:service:streaming-transport`. Eligibility is not inherited by the generic `urn:doe-iri:resource:service` type or by other service types.

The target is an operation entry point, not a Resource representation or relationship Resource. The producer MUST bind `resource_id` to the represented streaming transport service's adapter context. Because `resource_id` is the operation's only path variable, the advertised link is concrete rather than templated.

A representation advertising `iri:create-stream-reservation` MUST also advertise at least one applicable `service-desc` link whose deployed OpenAPI description contains the binding in Section 7. The operation link MUST NOT carry an IRI representation `profile`.

## 4. Cardinality

```text
Streaming Transport Service  -- iri:create-stream-reservation -->  Reservation-creation operation entry point
       1                    0..1
```

The HAL relation uses a singular link object when supplied.

## 5. Stability and Availability

The relationship describes a configured applicable operation affordance. Its presence SHOULD remain stable across ordinary changes in free instances, allocation balance, and control-plane health. The relation does not prove that the target is currently healthy, reachable, or available. Clients MUST use the governing OpenAPI contract and handle ordinary invocation failures, including allocation and capacity errors.

## 6. Authorization, Visibility, and Omission

Authorization MAY affect visibility of the operation affordance. A provider MAY omit `iri:create-stream-reservation` when the requester is not authorized to discover or use the entry point. Link visibility does not grant permission.

Omission means only that the affordance is not advertised in this representation.

Links MUST NOT contain credentials or secrets. A client MUST NOT automatically forward credentials to an unrelated origin solely because an operation link or service description names it.

## 7. OpenAPI Contract and Binding

The planned operation mapping is:

```text
POST /api/v2/streaming/{resource_id}/reservations
operationId: createStreamReservation
x-iri-relation: ["https://iri.science/rels/create-stream-reservation"]
```

The operation is not yet part of the IRI v2 OpenAPI. Until it is, and until the deployed OpenAPI carries this binding, producers MUST NOT advertise `iri:create-stream-reservation`. Once added, OpenAPI is authoritative for the method, path parameters, `StreamReservationRequest` request body, admission errors, the one-time credential in the response, responses, errors, and security behavior. Clients MUST follow the advertised target and the applicable deployed OpenAPI description; they MUST NOT construct a URL or infer an HTTP method from the relation name.

## 8. HAL Representation

```json
{
  "id": "ejfat-lb",
  "resource_type": "urn:doe-iri:resource:service:streaming-transport",
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:create-stream-reservation": {
      "href": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

## 9. Governing Sources

- [RFC: Streaming Data Transport Reservations](../../rfc/rfc-streaming-data-transport.md)
- [Resource operation-affordance RFC](../../rfc/rfc-resource-operation-affordances.md)
- [Streaming Transport Service Resource Definition Profile](../profiles/resource-definition/service/streaming-transport.md)

---

*DOE Integrated Research Infrastructure — Link Relation: create-stream-reservation*
