# IRI Link Relation: `submit-job`

**Relation URI:** `https://iri.science/rels/submit-job`<br>
**CURIE:** `iri:submit-job`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Change controller:** IRI technical subcommittee<br>
**Source representation type:** DOE-IRI `Resource` representation<br>
**Source resource type:** `urn:doe-iri:resource:compute:system`<br>
**Target representation type:** Resource-specific job-submission operation entry point<br>
**OpenAPI operation:** `POST /api/v2/compute/job/{resource_id}` (`operationId: launchJob`)

This document defines the `iri:submit-job` operation-affordance relationship
used by DOE-IRI compute-system Resource representations.

The canonical relation URI is `https://iri.science/rels/submit-job`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:submit-job`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:submit-job` |
| Relation URI | `https://iri.science/rels/submit-job` |
| Status and version | `provisional`, version `1.0.0` |
| Change controller | IRI technical subcommittee |
| Semantic meaning | Identifies the applicable job-submission operation entry point for the source compute system. |
| Source representation type | DOE-IRI `Resource` representation whose exact `resource_type` is `urn:doe-iri:resource:compute:system`. |
| Target representation type | Resource-specific job-submission operation entry point. |
| Cardinality | `0..1` link from each eligible compute-system Resource representation. |
| Applicability | The adapter implements the mapped operation for the represented compute-system context. |
| Target stability | Configured operation affordance, not a live capacity, queue, health, or schedulability assertion. |
| Relationship volatility | Changes when the facility configures or withdraws the adapter operation or changes requester-visible discovery, not solely because operational conditions change. |
| Authorization affects visibility | Yes. The relation MAY be omitted when the requester is not authorized to discover or use the entry point. Presence grants no permission. |
| Omission semantics | Not advertised in this representation; omission does not prove that submission is unsupported everywhere or that the requester can never submit a job. |
| Target classification | Operation entry point; not an API resource, DOE-IRI typed Resource, relationship Resource, or representation profile. |
| OpenAPI operation | `POST /api/v2/compute/job/{resource_id}` with `operationId: launchJob`. |
| OpenAPI binding | `x-iri-relation: ["https://iri.science/rels/submit-job"]` on that Operation Object. |

## 2. Semantic Meaning

The `iri:submit-job` relationship advertises the operation entry point through
which a client may submit a job for the source compute system. The source MUST
be a DOE-IRI Resource whose exact `resource_type` is
`urn:doe-iri:resource:compute:system`. Eligibility is not inherited by generic
compute, compute-node, CPU, or GPU Resource types.

The relation identifies navigation to an applicable affordance. It does not
itself specify the HTTP method or request contract, grant permission, prove
current capacity, guarantee schedulability, or replace the governing OpenAPI
operation contract.

## 3. Source, Target, and Operation Context

The relationship MAY originate only from:

```text
urn:doe-iri:resource:compute:system
```

The target is a Resource-specific operation entry point, not a Resource
representation or relationship Resource. The producer MUST bind `resource_id`
to the represented compute system's adapter context. Because `resource_id` is
the operation's only path variable, the advertised link is concrete rather
than templated.

The adapter MUST implement the mapped operation for that context. A producer
MUST NOT synthesize this link solely because `"compute"` appears in
`supported_endpoints`. When `supported_endpoints` is present on the source
Resource, advertising `iri:submit-job` requires `"compute"` in that array; the
reverse implication does not apply. Authorization-suppressed omission does not
make a retained `"compute"` category inconsistent.

A representation advertising `iri:submit-job` MUST also advertise at least
one applicable `service-desc` link whose deployed OpenAPI description contains
the binding in Section 7. The operation link MUST NOT carry an IRI
representation `profile`.

## 4. Cardinality

A compute-system Resource MAY advertise zero or one applicable job-submission
entry point:

```text
Compute System  -- iri:submit-job -->  Job-submission operation entry point
       1                    0..1
```

The HAL relation uses a singular link object when supplied.

## 5. Stability and Availability

The relationship describes a configured applicable operation affordance. Its
presence SHOULD remain stable across ordinary changes in capacity, queue
state, health, allocation balance, and schedulability. It may change when the
facility configures or withdraws the adapter operation or changes what is
visible to the requester.

The relation does not prove that the target is currently healthy, reachable,
or available. Clients MUST use the governing OpenAPI contract and handle
ordinary invocation failures.

## 6. Authorization, Visibility, and Omission

Authorization MAY affect visibility of the operation affordance. A provider
MAY omit `iri:submit-job` when the requester is not authorized to discover or
use the entry point. Conversely, link visibility does not grant permission and
does not guarantee that a submission will be accepted.

Omission means only that the affordance is not advertised in this
representation. It does not prove that the compute system has no
job-submission operation, that the operation is unsupported by every adapter,
or that the requester can never become authorized.

Links MUST NOT contain credentials or secrets. A client MUST NOT automatically
forward credentials to an unrelated origin solely because an operation link or
service description names it.

## 7. OpenAPI Contract and Binding

The current operation mapping is:

```text
POST /api/v2/compute/job/{resource_id}
operationId: launchJob
x-iri-relation: ["https://iri.science/rels/submit-job"]
```

OpenAPI remains authoritative for the method, path parameter semantics,
`JobSpec` request body, responses, errors, and security behavior. Clients MUST
follow the advertised target and the applicable deployed OpenAPI description;
they MUST NOT construct a URL or infer an HTTP method from the relation name.
The canonical relation URI, rather than `operationId`, is the machine-readable
binding key.

## 8. HAL Representation

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
    "iri:submit-job": {
      "href": "https://api.example.org/api/v2/compute/job/system-a"
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

---

*DOE Integrated Research Infrastructure — Link Relation: submit-job*
