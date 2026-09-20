# IRI Link Relation: `get-job`

**Relation URI:** `https://iri.science/rels/get-job`<br>
**CURIE:** `iri:get-job`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Change controller:** IRI technical subcommittee<br>
**Source representation type:** DOE-IRI compute-system `Resource` representation or IRI v2 `Job` representation<br>
**Source resource type:** `urn:doe-iri:resource:compute:system` when the source is a Resource; not applicable when the source is a Job<br>
**Target representation type:** Selected-job retrieval operation entry point<br>
**OpenAPI operation:** `GET /api/v2/compute/status/{resource_id}/{job_id}` (`operationId: getJob`)

This document defines the `iri:get-job` operation-affordance relationship used
by DOE-IRI compute-system Resource and IRI v2 Job representations.

The canonical relation URI is `https://iri.science/rels/get-job`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:get-job`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:get-job` |
| Relation URI | `https://iri.science/rels/get-job` |
| Status and version | `provisional`, version `1.0.0` |
| Change controller | IRI technical subcommittee |
| Semantic meaning | Identifies the applicable operation entry point for retrieving a selected job and its current status in the compute-system context. |
| Source representation type | DOE-IRI `Resource` representation whose exact `resource_type` is `urn:doe-iri:resource:compute:system`, or an IRI v2 `Job` representation. |
| Target representation type | Selected-job retrieval operation entry point. |
| Cardinality | Resource source: `0..1`; Job source: `0..1`. |
| Applicability | The adapter implements the mapped retrieval operation for the represented compute system; a Job-source link is fully bound to that selected job. |
| Target stability | Configured Resource affordance; on a Job, the fully bound target remains associated with that job while the operation context is retained. |
| Relationship volatility | Changes with adapter configuration or requester visibility and, on a Job source, when the producer no longer retains the bound operation context. |
| Authorization affects visibility | Yes. The relation MAY be omitted based on discovery or retrieval authorization. Presence grants no permission. |
| Omission semantics | Not advertised in this representation; omission does not prove that job retrieval is unsupported everywhere or permanently unavailable. |
| Target classification | Operation entry point; not an API resource, DOE-IRI typed Resource, relationship Resource, or representation profile. |
| OpenAPI operation | `GET /api/v2/compute/status/{resource_id}/{job_id}` with `operationId: getJob`. |
| OpenAPI binding | `x-iri-relation: ["https://iri.science/rels/get-job"]` on that Operation Object. |

## 2. Semantic Meaning

The `iri:get-job` relationship advertises the operation entry point through
which a client may retrieve a selected job and its current status. It is an
operation affordance, not the identity relation for a Job representation.
Standard `self` remains a Job's canonical retrieval relation;
`iri:get-job` is optional on a Job source.

The relation does not grant permission, assert that every job identifier is
visible, or replace the governing OpenAPI response and security contract.

## 3. Source, Target, and Operation Context

The relationship MAY originate from either:

1. a DOE-IRI Resource whose exact `resource_type` is
   `urn:doe-iri:resource:compute:system`; or
2. an IRI v2 Job representation for one selected job.

On a compute-system Resource, the producer MUST bind `resource_id` to the
represented Resource's adapter context. It MAY leave only `job_id` as a URI
template variable, in which case the link MUST set `templated` to `true`.
Expansion identifies a selected job in that Resource context and grants no
permission to retrieve arbitrary job identifiers.

On a Job representation, the producer MUST bind both `resource_id` and
`job_id`. The producer MUST retain the compute-system operation context because
a client cannot infer `resource_id` from `job_id`. A Job-source link MUST be a
concrete URI, not a template with either identifier unresolved.

The adapter MUST implement the mapped operation for the applicable context.
Resource Type hierarchy alone does not make generic compute, node, CPU, or GPU
Resources eligible. When `supported_endpoints` is present on a Resource source,
advertising `iri:get-job` requires `"compute"` in that array; the rule does not
apply to Job representations, and the reverse implication does not apply.
Authorization-suppressed omission does not make a retained `"compute"`
category inconsistent.

A representation advertising `iri:get-job` MUST also advertise at least one
applicable `service-desc` link whose deployed OpenAPI description contains the
binding in Section 7. The operation link MUST NOT carry an IRI representation
`profile`.

## 4. Cardinality

Each eligible source representation MAY advertise zero or one retrieval entry
point:

```text
Compute System  -- iri:get-job -->  Selected-job retrieval operation
       1                   0..1

Job             -- iri:get-job -->  Selected-job retrieval operation
 1                          0..1
```

The HAL relation uses a singular link object when supplied.

## 5. Stability and Availability

On a compute-system Resource, the relation describes a configured operation
affordance and SHOULD remain stable across ordinary changes in load, capacity,
queue state, or health. On a Job, the target is bound to that selected job and
may cease to be advertised when the producer no longer retains its operation
context or changes visibility for the requester.

The relation does not prove that the target is currently healthy, reachable,
or available. Clients MUST use the governing OpenAPI contract and handle
ordinary invocation failures.

## 6. Authorization, Visibility, and Omission

Authorization MAY affect visibility of the operation affordance. A provider
MAY omit `iri:get-job` when the requester is not authorized to discover or use
the entry point. Presence grants no permission and does not guarantee that a
retrieval request will succeed.

Omission means only that the affordance is not advertised in this
representation. It does not prove that retrieving jobs is unsupported
everywhere or permanently unavailable. On a Job, `self` remains the canonical
retrieval relation even when `iri:get-job` is omitted.

Links MUST NOT contain credentials or secrets. A client MUST NOT automatically
forward credentials to an unrelated origin solely because an operation link or
service description names it.

## 7. OpenAPI Contract and Binding

The current operation mapping is:

```text
GET /api/v2/compute/status/{resource_id}/{job_id}
operationId: getJob
x-iri-relation: ["https://iri.science/rels/get-job"]
```

OpenAPI remains authoritative for path parameters, the `Job` response,
responses, errors, and security behavior. Clients MUST follow the advertised
target and the applicable deployed OpenAPI description; they MUST NOT
construct a URL or infer an HTTP method from the relation name. The canonical
relation URI, rather than `operationId`, is the machine-readable binding key.

## 8. HAL Representation

Compute-system Resource with producer-bound `resource_id` and templated
`job_id`:

```json
{
  "id": "system-a",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "supported_endpoints": ["compute"],
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:get-job": {
      "href": "https://api.example.org/api/v2/compute/status/system-a/{job_id}",
      "templated": true
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

Job with both identifiers bound and standard `self` retained:

```json
{
  "id": "job-42",
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "self": {
      "href": "https://api.example.org/api/v2/compute/status/system-a/job-42"
    },
    "iri:get-job": {
      "href": "https://api.example.org/api/v2/compute/status/system-a/job-42"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

## 9. Governing Sources

- [Resource operation-affordance RFC](../../rfc/rfc-resource-operation-affordances.md)
- [IRI v2 compute OpenAPI](../../specification-v2/openapi/production/compute.yaml)
- [Common Resource profile](../profiles/status/resource.md)
- [Compute-system Resource Definition Profile](../profiles/resource-definition/compute/system.md)
- [Job profile](../profiles/compute/job.md)

---

*DOE Integrated Research Infrastructure — Link Relation: get-job*
