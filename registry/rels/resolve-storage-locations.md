# IRI Link Relation: `resolve-storage-locations`

**Relation URI:** `https://iri.science/rels/resolve-storage-locations`<br>
**CURIE:** `iri:resolve-storage-locations`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Change controller:** IRI technical subcommittee<br>
**Source representation type:** Eligible DOE-IRI `Resource` representation with an applicable storage-location-resolution context<br>
**Source resource type:** One of the exact Resource Types and conditions enumerated in Section 3<br>
**Target representation type:** Resource-specific storage-location-resolution operation entry point<br>
**OpenAPI operation:** `GET /api/v2/storage/locations/{resource_id}` (`operationId: getStorageLocations`)

This document defines the `iri:resolve-storage-locations` operation-affordance
relationship used by eligible DOE-IRI Resource representations.

The canonical relation URI is
`https://iri.science/rels/resolve-storage-locations`. With the canonical IRI
CURIE template `https://iri.science/rels/{rel}`,
`iri:resolve-storage-locations` expands to that URI. The relation URI
identifies the link-relation semantics and is distinct from any target
representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:resolve-storage-locations` |
| Relation URI | `https://iri.science/rels/resolve-storage-locations` |
| Status and version | `provisional`, version `1.0.0` |
| Change controller | IRI technical subcommittee |
| Semantic meaning | Identifies the applicable operation entry point for resolving storage locations in the source Resource's context. |
| Source representation type | DOE-IRI `Resource` representation with one of the exact Resource Types and all applicable context conditions in Section 3. |
| Target representation type | Resource-specific storage-location-resolution operation entry point. |
| Cardinality | `0..1` link from each eligible source Resource representation. |
| Applicability | The adapter implements the mapped operation for the represented Resource and can apply the operation's existing `StorageInstance` response semantics to that Resource context. |
| Target stability | Configured discovery affordance, not a topology, current-location, accessibility, reachability, or successful-resolution assertion. |
| Relationship volatility | Changes when the facility configures or withdraws the applicable adapter operation or changes requester-visible discovery, not solely because returned locations or operational conditions change. |
| Authorization affects visibility | Yes. The relation MAY be omitted when the requester is not authorized to discover or invoke the entry point. Presence grants no permission. |
| Omission semantics | Not advertised in this representation; omission does not prove that location resolution is unsupported everywhere or permanently unavailable. |
| Target classification | Operation entry point; not an API resource, DOE-IRI typed Resource, topology relationship, `StorageInstance` result, or representation profile. |
| OpenAPI operation | `GET /api/v2/storage/locations/{resource_id}` with `operationId: getStorageLocations`; success returns an array of `StorageInstance`. |
| OpenAPI binding | `x-iri-relation: ["https://iri.science/rels/resolve-storage-locations"]` on that Operation Object. |

## 2. Semantic Meaning

The `iri:resolve-storage-locations` relationship advertises the operation entry
point through which a client may resolve `StorageInstance` entries in the
source Resource's context. The current operation supports optional
`logicalpath`, `project`, `allocation`, and `intent` query filters.

This relation describes context-sensitive resolution, not configured storage
topology. It does not replace relations such as `iri:has-mount`, assert that a
returned location is mounted on or contained by the source, grant access, or
guarantee that a returned location is currently reachable or usable.

## 3. Source, Target, and Operation Context

The relationship MAY originate only from a Resource whose exact
`resource_type` is one of the following and only under the stated conditions:

| Exact Resource Type | Required applicability condition |
|---|---|
| `urn:doe-iri:resource:compute` | Actual adapter semantics for location resolution are explicitly known and unambiguous. |
| `urn:doe-iri:resource:compute:system` | Location resolution is implemented for that configured system context. |
| `urn:doe-iri:resource:compute:node` | Location resolution is explicitly configured for that node. |
| `urn:doe-iri:resource:storage` | Actual adapter semantics for location resolution are explicitly known and unambiguous. |
| `urn:doe-iri:resource:storage:system` | The operation's existing response semantics apply to that storage system. |
| `urn:doe-iri:resource:storage:filesystem` | The adapter accepts that filesystem identifier and defines its path and resolution context. |
| `urn:doe-iri:resource:storage:mount` | The adapter supports that mount identifier and its mount-specific context; eligibility is not inherited from its filesystem or consuming system. |
| `urn:doe-iri:resource:storage:block` | The operation's existing response semantics apply to that block-storage Resource. |
| `urn:doe-iri:resource:storage:object` | The operation's existing response semantics apply to that object-storage Resource. |
| `urn:doe-iri:resource:service:dtn` | The DTN itself is the explicit adapter context; hosting and mount-access links alone do not imply applicability. |

Eligibility is exact-type-based and is not inherited by other Resource Type
descendants. Classification or topology alone does not establish
applicability. If a source cannot identify one unambiguous operation context,
the producer MUST expose separate Resources using the existing model and link
them through registered topology relations; it MUST NOT silently choose a host
or add an undocumented context selector.

The producer MUST bind `resource_id` to the represented Resource's adapter
context. The advertised example is concrete; clients supply any optional query
filters according to OpenAPI. If the operation belongs to a different
Resource, the producer MUST expose the appropriate Resource relationship
rather than advertise the operation as belonging to this source.

This storage-discovery relation has no legacy `supported_endpoints` category
mapping. Its presence requires neither `"compute"` nor `"filesystem"`, and a
retained category does not imply this relation.

A representation advertising `iri:resolve-storage-locations` MUST also
advertise at least one applicable `service-desc` link whose deployed OpenAPI
description contains the binding in Section 8. The operation link MUST NOT
carry an IRI representation `profile`.

## 4. Cardinality

Each eligible Resource MAY advertise zero or one applicable operation entry
point:

```text
Resource  -- iri:resolve-storage-locations -->  Location-resolution operation entry point
   1                          0..1
```

The HAL relation uses a singular link object when supplied.

## 5. Discovery and Result Semantics

The mapped operation remains `GET` and returns an array of `StorageInstance`
values. Query filters and requester context may change the returned entries
without changing the configured operation-affordance relationship.

The operation response does not establish topology, health, protocol
availability, authorization to use a location, or successful future access.
Clients interpret the response according to the governing OpenAPI contract and
applicable Resource profiles.

## 6. Stability and Availability

The relationship describes a configured applicable discovery affordance. Its
presence SHOULD remain stable across ordinary changes in returned locations,
load, health, reachability, or storage contents. It may change when the
facility configures or withdraws the adapter operation or changes visibility
for the requester.

The relation does not prove that the target or any returned location is
currently healthy, reachable, or available. Clients MUST handle ordinary
invocation failures and changing results.

## 7. Authorization, Visibility, and Omission

Authorization MAY affect visibility of the operation affordance and the
locations returned by the operation. A provider MAY omit
`iri:resolve-storage-locations` when the requester is not authorized to
discover or use the entry point. Presence grants no permission and guarantees
no particular result.

Omission means only that the affordance is not advertised in this
representation. It does not prove that location resolution is unsupported
everywhere or permanently unavailable. Links MUST NOT contain credentials or
secrets. A client MUST NOT automatically forward credentials to an unrelated
origin solely because an operation link or service description names it.

## 8. OpenAPI Contract and Binding

The current operation mapping is:

```text
GET /api/v2/storage/locations/{resource_id}
operationId: getStorageLocations
required path parameter: resource_id
optional query parameters: logicalpath, project, allocation, intent
success status: 200
success schema: array of StorageInstance
x-iri-relation: ["https://iri.science/rels/resolve-storage-locations"]
```

OpenAPI remains authoritative for path and query parameters, serialization,
responses, errors, and security behavior. Clients MUST follow the advertised
target and the applicable deployed OpenAPI description; they MUST NOT
construct a URL or infer invocation details from the relation name. The
canonical relation URI, rather than `operationId`, is the machine-readable
binding key.

## 9. HAL Representation

```json
{
  "id": "scratch",
  "resource_type": "urn:doe-iri:resource:storage:filesystem",
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:resolve-storage-locations": {
      "href": "https://api.example.org/api/v2/storage/locations/scratch"
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
- [Compute-system Resource Definition Profile](../profiles/resource-definition/compute/system.md)
- [Compute-node Resource Definition Profile](../profiles/resource-definition/compute/node.md)
- [Storage-system Resource Definition Profile](../profiles/resource-definition/storage/system.md)
- [Filesystem Resource Definition Profile](../profiles/resource-definition/storage/filesystem.md)
- [Mount Resource Definition Profile](../profiles/resource-definition/storage/mount.md)
- [Block-storage Resource Definition Profile](../profiles/resource-definition/storage/block.md)
- [Object-storage Resource Definition Profile](../profiles/resource-definition/storage/object.md)
- [DTN service Resource Definition Profile](../profiles/resource-definition/service/dtn.md)

---

*DOE Integrated Research Infrastructure — Link Relation: resolve-storage-locations*
