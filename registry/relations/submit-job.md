# IRI Link Relation: `submit-job`

**Relation URI:** `https://iri.science/rels/submit-job`<br>
**CURIE:** `iri:submit-job`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** `urn:doe-iri:resource:compute:system`<br>
**Source resource type:** `urn:doe-iri:resource:compute:system`<br>
**Target representation type:** Resource-specific job-submission operation entry point. The current OpenAPI operation is `POST /api/v2/compute/job/{resource_id}` with `operationId: launchJob`.

This document defines the `iri:submit-job` operation-affordance relationship used by DOE-IRI compute-system Resource representations.

The canonical relation URI is `https://iri.science/rels/submit-job`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:submit-job`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:submit-job` |
| Relation URI | `https://iri.science/rels/submit-job` |
| Status | `provisional` |
| Semantic meaning | Identifies the applicable job-submission operation entry point for the source compute system. |
| Source representation type | `urn:doe-iri:resource:compute:system` |
| Target representation type | Resource-specific job-submission operation entry point. The current OpenAPI operation is `POST /api/v2/compute/job/{resource_id}` with `operationId: launchJob`. |
| Cardinality | `0..1` target from a compute-system resource. |
| Target stability | Applicable configured affordance, not a live capacity assertion. |
| Authorization affects visibility | Yes. A provider MAY omit the relation when job submission is not visible to the requester; absence does not generally prove that the compute system has no job-submission operation. |
| Target classification | Operation entry point; not an API resource, DOE-IRI typed Resource, state object, or relationship resource. |
| Relationship volatility | Changes when the facility configures, withdraws, or changes the applicable job-submission affordance. It does not change solely because capacity, queue state, health, or schedulability changes. |

## 2. Semantic Meaning

The `iri:submit-job` relationship advertises the operation entry point through which a client may submit a job for the source compute system. The source MUST be a DOE-IRI Resource whose `resource_type` is `urn:doe-iri:resource:compute:system`.

The relation identifies navigation to an applicable affordance. It does not itself specify the HTTP method or request contract, grant permission, prove current capacity, guarantee schedulability, or replace the governing OpenAPI operation contract.

## 3. Source and Target Representation

The relationship MAY originate only from:

```text
urn:doe-iri:resource:compute:system
```

The target is a resource-specific operation entry point, not a Resource representation, state object, or relationship resource. The current operation is:

```text
POST /api/v2/compute/job/{resource_id}
operationId: launchJob
```

OpenAPI remains authoritative for the HTTP method, `JobSpec` request body, response, error, and security behavior.

## 4. Cardinality

A compute-system resource MAY advertise zero or one applicable job-submission entry point:

```text
Compute System  -- iri:submit-job -->  Job-submission operation entry point
       1                    0..1
```

The HAL relation uses a singular link object when it is supplied. Omission means that the entry point is not advertised to the requester; it does not grant a negative assertion about permission, capacity, or schedulability.

## 5. Static and Dynamic Semantics

The relationship describes a configured applicable operation affordance. Its presence does not assert that the compute system has current capacity, an available queue, a schedulable allocation, or a successful authorization outcome.

Live capacity, queue state, health, allocation balance, and schedulability are dynamic conditions outside this link relation. Clients MUST consult the current representation and the governing OpenAPI contract before invoking the operation.

## 6. Authorization and Visibility

Authorization MAY affect visibility of the operation affordance. A provider MAY omit `iri:submit-job` when the requester is not authorized to discover or use the entry point. Conversely, link visibility does not grant permission and does not guarantee that a submission will be accepted.

## 7. OpenAPI Contract

The relation is an additive navigation aid and does not replace OpenAPI. The current operation is `POST /api/v2/compute/job/{resource_id}` with `operationId: launchJob`.

OpenAPI remains authoritative for the method, path parameter semantics, `JobSpec` request body, responses, error handling, and security behavior. A client MUST follow that contract when invoking the advertised entry point.

## 8. HAL Representation

```json
{
  "resource_type": "urn:doe-iri:resource:compute:system",
  "_links": {
    "iri:submit-job": {
      "href": "/api/v2/compute/job/perlmutter"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: submit-job*
