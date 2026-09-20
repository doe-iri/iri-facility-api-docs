# IRI Link Relation: `get-storage-access-endpoints`

**Relation URI:** `https://iri.science/rels/get-storage-access-endpoints`<br>
**CURIE:** `iri:get-storage-access-endpoints`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Change controller:** IRI technical subcommittee<br>
**Source representation type:** Eligible DOE-IRI storage `Resource` representation<br>
**Source resource type:** One of the exact storage Resource Types enumerated in Section 3<br>
**Target representation type:** Resource-specific storage-access-endpoint discovery operation entry point<br>
**OpenAPI operation:** `GET /api/v2/storage/access-endpoints/{resource_id}` (`operationId: getStorageAccessEndpoints`)

This document defines the `iri:get-storage-access-endpoints`
operation-affordance relationship used by eligible DOE-IRI storage Resource
representations.

The canonical relation URI is
`https://iri.science/rels/get-storage-access-endpoints`. With the canonical IRI
CURIE template `https://iri.science/rels/{rel}`,
`iri:get-storage-access-endpoints` expands to that URI. The relation URI
identifies the link-relation semantics and is distinct from any target
representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:get-storage-access-endpoints` |
| Relation URI | `https://iri.science/rels/get-storage-access-endpoints` |
| Status and version | `provisional`, version `1.0.0` |
| Change controller | IRI technical subcommittee |
| Semantic meaning | Identifies the applicable operation entry point for discovering access descriptions for the source storage Resource. |
| Source representation type | DOE-IRI `Resource` representation with one of the exact storage Resource Types and conditions in Section 3. |
| Target representation type | Resource-specific storage-access-endpoint discovery operation entry point. |
| Cardinality | `0..1` link from each eligible source Resource representation. |
| Applicability | The adapter implements the mapped discovery operation for the represented storage Resource. |
| Target stability | Configured discovery affordance, not a current endpoint-health, reachability, protocol-availability, or successful-access assertion. |
| Relationship volatility | Changes when the facility configures or withdraws the applicable discovery operation or changes requester-visible discovery, not solely because returned endpoint descriptions or operational conditions change. |
| Authorization affects visibility | Yes. The relation MAY be omitted when the requester is not authorized to discover or invoke the entry point. Presence grants no permission. |
| Omission semantics | Not advertised in this representation; omission does not prove that access-endpoint discovery is unsupported everywhere or permanently unavailable. |
| Target classification | Operation entry point; not an `AccessEndpoint` result, protocol operation, API resource, DOE-IRI typed Resource, or representation profile. |
| OpenAPI operation | `GET /api/v2/storage/access-endpoints/{resource_id}` with `operationId: getStorageAccessEndpoints`; success returns an array of `AccessEndpoint`. |
| OpenAPI binding | `x-iri-relation: ["https://iri.science/rels/get-storage-access-endpoints"]` on that Operation Object. |

## 2. Semantic Meaning

The `iri:get-storage-access-endpoints` relationship advertises the operation
entry point through which a client may retrieve `AccessEndpoint` descriptions
for the source storage Resource. The current operation supports optional
`protocol` and `endpoint_id` query filters.

This is a discovery relation. Invoking it does not execute a Globus transfer,
S3 request, XRootD request, or any other described protocol operation. Neither
the relation nor a returned descriptor guarantees endpoint health,
reachability, authorization, protocol support for a particular action, or
successful future access.

## 3. Source, Target, and Operation Context

The relationship MAY originate only from a Resource whose exact
`resource_type` is one of the following and only under the stated conditions:

| Exact Resource Type | Required applicability condition |
|---|---|
| `urn:doe-iri:resource:storage` | Actual adapter semantics for access-endpoint discovery are explicitly known. |
| `urn:doe-iri:resource:storage:system` | The adapter implements access-endpoint discovery for that storage system. |
| `urn:doe-iri:resource:storage:filesystem` | The adapter accepts that filesystem identifier, defines its path context, and implements access-endpoint discovery. |
| `urn:doe-iri:resource:storage:block` | The adapter implements access-endpoint discovery for that block-storage Resource. |
| `urn:doe-iri:resource:storage:object` | The adapter implements access-endpoint discovery for that object-storage Resource. |

Eligibility is exact-type-based and is not inherited by other Resource Type
descendants. In particular, `storage:mount`, compute, service, and hardware
Resources are not eligible merely because they are connected to or consume an
eligible storage Resource.

The producer MUST bind `resource_id` to the represented storage Resource's
adapter context. The advertised example is concrete; clients supply optional
`protocol` or `endpoint_id` filters according to OpenAPI. If the operation
belongs to a different Resource, the producer MUST expose the appropriate
Resource relationship rather than advertise the operation as belonging to
this source.

This storage-discovery relation has no legacy `supported_endpoints` category
mapping. Its presence requires neither `"compute"` nor `"filesystem"`, and a
retained category does not imply this relation.

A representation advertising `iri:get-storage-access-endpoints` MUST also
advertise at least one applicable `service-desc` link whose deployed OpenAPI
description contains the binding in Section 8. The operation link MUST NOT
carry an IRI representation `profile`.

## 4. Cardinality

Each eligible Resource MAY advertise zero or one applicable operation entry
point:

```text
Resource  -- iri:get-storage-access-endpoints -->  Access-endpoint discovery operation entry point
   1                              0..1
```

The HAL relation uses a singular link object when supplied.

## 5. Discovery and Result Semantics

The mapped operation remains `GET` and returns an array of `AccessEndpoint`
descriptions. Query filters and requester context may change the returned
entries without changing the configured operation-affordance relationship.

Returned `AccessEndpoint.capabilities` retain their existing descriptive
meaning. They do not convert this relation into a protocol invocation and do
not guarantee that every described operation is currently usable or authorized
for the requester.

## 6. Stability and Availability

The relationship describes a configured applicable discovery affordance. Its
presence SHOULD remain stable across ordinary changes in returned endpoints,
load, health, reachability, or protocol availability. It may change when the
facility configures or withdraws the adapter operation or changes visibility
for the requester.

The relation does not prove that the target or any returned access endpoint is
currently healthy, reachable, or available. Clients MUST handle ordinary
invocation failures and changing results.

## 7. Authorization, Visibility, and Omission

Authorization MAY affect visibility of the operation affordance and the
endpoint descriptions returned by the operation. A provider MAY omit
`iri:get-storage-access-endpoints` when the requester is not authorized to
discover or use the entry point. Presence grants no permission and guarantees
no particular result or protocol access.

Omission means only that the affordance is not advertised in this
representation. It does not prove that access-endpoint discovery is unsupported
everywhere or permanently unavailable. Links MUST NOT contain credentials or
secrets. A client MUST NOT automatically forward credentials to an unrelated
origin solely because an operation link, service description, or returned
access descriptor names it.

## 8. OpenAPI Contract and Binding

The current operation mapping is:

```text
GET /api/v2/storage/access-endpoints/{resource_id}
operationId: getStorageAccessEndpoints
required path parameter: resource_id
optional query parameters: protocol, endpoint_id
success status: 200
success schema: array of AccessEndpoint
x-iri-relation: ["https://iri.science/rels/get-storage-access-endpoints"]
```

OpenAPI remains authoritative for path and query parameters, serialization,
responses, errors, and security behavior. Clients MUST follow the advertised
target and the applicable deployed OpenAPI description; they MUST NOT
construct a URL, infer invocation details from the relation name, or treat the
discovery operation as a returned endpoint's protocol operation. The canonical
relation URI, rather than `operationId`, is the machine-readable binding key.

## 9. HAL Representation

```json
{
  "id": "storage-a",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:get-storage-access-endpoints": {
      "href": "https://api.example.org/api/v2/storage/access-endpoints/storage-a"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

## 10. Governing Sources

- [Resource operation-affordance RFC](../../rfc/rfc-resource-operation-affordances.md)
- [IRI v2 storage OpenAPI](../../specification-v2/openapi/production/storage.yaml)
- [Common Resource profile](../profiles/status/resource.md)
- [Storage-system Resource Definition Profile](../profiles/resource-definition/storage/system.md)
- [Filesystem Resource Definition Profile](../profiles/resource-definition/storage/filesystem.md)
- [Block-storage Resource Definition Profile](../profiles/resource-definition/storage/block.md)
- [Object-storage Resource Definition Profile](../profiles/resource-definition/storage/object.md)

---

*DOE Integrated Research Infrastructure — Link Relation: get-storage-access-endpoints*
