# IRI Link Relation: `change-file-owner`

**Relation URI:** `https://iri.science/rels/change-file-owner`<br>
**CURIE:** `iri:change-file-owner`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Change controller:** IRI technical subcommittee<br>
**Source representation type:** Eligible DOE-IRI `Resource` representation with an explicit filesystem operation context<br>
**Source resource type:** One of the exact Resource Types enumerated in Section 3<br>
**Target representation type:** Resource-specific asynchronous file-ownership-change operation entry point<br>
**OpenAPI operation:** `POST /api/v2/filesystem/chown/{resource_id}` (`operationId: chown`)

This document defines the `iri:change-file-owner` operation-affordance
relationship used by eligible DOE-IRI Resource representations.

The canonical relation URI is
`https://iri.science/rels/change-file-owner`. With the canonical IRI CURIE
template `https://iri.science/rels/{rel}`, `iri:change-file-owner` expands to
that URI. The relation URI identifies the link-relation semantics and is
distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:change-file-owner` |
| Relation URI | `https://iri.science/rels/change-file-owner` |
| Status and version | `provisional`, version `1.0.0` |
| Change controller | IRI technical subcommittee |
| Semantic meaning | Identifies the applicable operation entry point for requesting a file ownership change in the source Resource's filesystem context. |
| Source representation type | DOE-IRI `Resource` representation with one of the exact Resource Types in Section 3 and an explicit, unambiguous filesystem adapter and path context. |
| Target representation type | Resource-specific asynchronous file-ownership-change operation entry point. |
| Cardinality | `0..1` link from each eligible source Resource representation. |
| Applicability | The adapter implements the mapped operation for the represented Resource and establishes its filesystem namespace and execution/access context. |
| Target stability | Configured operation affordance, not a current ownership, reachability, or successful-change assertion. |
| Relationship volatility | Changes when the facility configures or withdraws the applicable adapter operation or changes requester-visible discovery, not solely because operational conditions change. |
| Authorization affects visibility | Yes. The relation MAY be omitted when the requester is not authorized to discover or invoke the entry point. Presence grants no permission. |
| Omission semantics | Not advertised in this representation; omission does not prove that ownership changes are unsupported everywhere or permanently unavailable. |
| Target classification | Operation entry point; not an API resource, DOE-IRI typed Resource, relationship Resource, result representation, or representation profile. |
| OpenAPI operation | `POST /api/v2/filesystem/chown/{resource_id}` with `operationId: chown`; success returns `TaskSubmitResponse`. |
| OpenAPI binding | `x-iri-relation: ["https://iri.science/rels/change-file-owner"]` on that Operation Object. |

## 2. Semantic Meaning

The `iri:change-file-owner` relationship advertises the operation entry point
through which a client may request an ownership change for a file in the
source Resource's configured filesystem context. File operands and ownership
values remain in the OpenAPI-defined request body.

The relation identifies an applicable operation, not a current ownership state
or completed change. It does not grant authorization, prove that the identified
path or principal exists, or guarantee that the requested ownership change is
valid or will be applied.

## 3. Source, Target, and Operation Context

The relationship MAY originate only from a Resource whose exact
`resource_type` is one of:

```text
urn:doe-iri:resource:compute
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:storage
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:storage:mount
urn:doe-iri:resource:service:dtn
```

Eligibility is exact-type-based and is not inherited by other Resource Type
descendants. For every eligible type, the adapter MUST establish the path
namespace and one unambiguous execution/access context for the source
Resource. Type classification, topology links, mount relationships, and
`supported_endpoints` alone do not establish applicability.

In particular, a mount does not inherit operations from its filesystem or
consuming system, and a DTN's hosting or mount-access links do not imply a
filesystem execution context. Generic compute and storage Resources are
eligible only when their actual adapter semantics are known. If one source
cannot identify an unambiguous context, the producer MUST expose separate
Resources and use registered topology relations; it MUST NOT silently choose a
host or add an undocumented context selector.

The producer MUST bind `resource_id` to the represented Resource's adapter
context. Because it is the only path variable, the advertised operation link
is concrete rather than templated. If the operation belongs to a different
Resource, the producer MUST expose the appropriate Resource relationship
rather than advertise the operation as belonging to this source.

When `supported_endpoints` is present on the source Resource, advertising
`iri:change-file-owner` requires `"filesystem"` in that array. The reverse
implication does not apply, and authorization-suppressed omission does not make
a retained `"filesystem"` category inconsistent.

A representation advertising `iri:change-file-owner` MUST also advertise at
least one applicable `service-desc` link whose deployed OpenAPI description
contains the binding in Section 8. The operation link MUST NOT carry an IRI
representation `profile`.

## 4. Cardinality

Each eligible Resource MAY advertise zero or one applicable operation entry
point:

```text
Resource  -- iri:change-file-owner -->  File-ownership-change operation entry point
   1                     0..1
```

The HAL relation uses a singular link object when supplied.

## 5. Asynchronous Invocation Semantics

The mapped operation remains `POST` and returns `TaskSubmitResponse`. Following
the relation submits asynchronous work; it does not synchronously return the
changed file, its metadata, or proof that the change completed. Clients use the
existing Task monitoring flow and the governing OpenAPI contract to determine
the outcome.

## 6. Stability and Availability

The relationship describes a configured applicable operation affordance. Its
presence SHOULD remain stable across ordinary changes in load, health,
reachability, or filesystem contents. It may change when the facility
configures or withdraws the adapter operation or changes visibility for the
requester.

The relation does not prove that the target is currently healthy, reachable,
or available. Clients MUST handle ordinary invocation and Task failures.

## 7. Authorization, Visibility, and Omission

Authorization MAY affect visibility of the operation affordance. A provider
MAY omit `iri:change-file-owner` when the requester is not authorized to
discover or use the entry point. Presence grants no permission and guarantees
no successful ownership change.

Omission means only that the affordance is not advertised in this
representation. It does not prove that ownership changes are unsupported
everywhere or permanently unavailable. Links MUST NOT contain credentials or
secrets. A client MUST NOT automatically forward credentials to an unrelated
origin solely because an operation link or service description names it.

## 8. OpenAPI Contract and Binding

The current operation mapping is:

```text
POST /api/v2/filesystem/chown/{resource_id}
operationId: chown
success schema: TaskSubmitResponse
x-iri-relation: ["https://iri.science/rels/change-file-owner"]
```

OpenAPI remains authoritative for the bound path parameter,
`PutFileChownRequest` request body, responses, errors, Task submission, and
security behavior. Clients MUST follow the advertised target and the
applicable deployed OpenAPI description; they MUST NOT construct a URL or
infer an HTTP method from the relation name. The canonical relation URI,
rather than `operationId`, is the machine-readable binding key.

## 9. HAL Representation

```json
{
  "id": "scratch",
  "resource_type": "urn:doe-iri:resource:storage:filesystem",
  "supported_endpoints": ["filesystem"],
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:change-file-owner": {
      "href": "https://api.example.org/api/v2/filesystem/chown/scratch"
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
- [IRI v2 filesystem OpenAPI](../../specification-v2/openapi/production/filesystem.yaml)
- [Common Resource profile](../profiles/status/resource.md)
- [Compute-system Resource Definition Profile](../profiles/resource-definition/compute/system.md)
- [Compute-node Resource Definition Profile](../profiles/resource-definition/compute/node.md)
- [Filesystem Resource Definition Profile](../profiles/resource-definition/storage/filesystem.md)
- [Mount Resource Definition Profile](../profiles/resource-definition/storage/mount.md)
- [DTN service Resource Definition Profile](../profiles/resource-definition/service/dtn.md)

---

*DOE Integrated Research Infrastructure — Link Relation: change-file-owner*
