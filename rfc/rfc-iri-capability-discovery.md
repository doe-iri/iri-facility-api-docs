# RFC: IRI Facility API Root Discovery and Implementation Conformance

## Abstract

The DOE Integrated Research Infrastructure (IRI) Facility API is implemented by independently operated facilities that may support different subsets of the IRI 2.0 contract. This RFC defines a HAL API root that combines:

- a `conforms_to` declaration identifying the standardized IRI behavior implemented by a deployment;
- typed `_links` identifying the deployed entry point for each IRI API area; and
- `service-desc` identifying the deployment-specific OpenAPI description.

The mechanism allows a client to discover supported behavior and authoritative entry-point URIs without constructing facility URLs or using `501 Not Implemented` as its primary capability-discovery mechanism.

## Status of This Memo

**Status:** Draft for discussion  
**Target:** IRI 2.0 additive extension  
**Revision:** 0.3  
**Date:** 2026-09-10

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

This revision was reviewed against the IRI documentation repository at commit [`896be8af387e`](https://github.com/doe-iri/iri-facility-api-docs/commit/896be8af387ebc8c0837a8fcea4f0b61cd7a0176).

The nine `https://iri.science/conformance/2.0/...` identifiers and the seven API-area relations proposed by this RFC are not currently assigned by the reviewed IRI registries. They become canonical only if this RFC is adopted and the corresponding conformance and relation registrations are published. This RFC does not itself modify the production OpenAPI or registry files.

The OLCF URIs used below are illustrative deployment examples. This document does not assert that OLCF currently serves these resources.

## 1. Scope and Semantic Model

This RFC defines deployment-level API discovery. It keeps the following concepts distinct:

```text
conforms_to
    WHAT standardized IRI behavior the deployment claims to implement

root API-area relation
    WHY a linked target is the entry point for an IRI API area

href
    WHERE that deployed API-area entry point is located

Resource- or representation-level relation
    WHICH related resource or operation is applicable in that context

service-desc / OpenAPI
    HOW operations are invoked and representations are structured
```

An Account `Capability` remains an allocatable or distinguishable aspect of an IRI Resource. Resource Definition Profile capability attributes such as `system_capabilities` and `filesystem_capabilities` remain characteristics of a Resource. Neither is an API implementation conformance class.

This RFC does not repurpose `Capability`, `capability_uris`, `iri:has-capability`, Resource Type URNs, or Representation Profile URIs. It introduces no separate Resource Definition or Resource State representation.

The migration from `Resource.supported_endpoints` to Resource-specific operation affordances is governed by the companion [Resource Operation Affordances RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/rfc/rfc-resource-operation-affordances.md). The present RFC supplies deployment-level conformance and API-area discovery; it does not duplicate that operation-relation catalog.

## 2. API Root

An adopting deployment MUST expose a read-only API root discoverable from a configured deployment URI. For the IRI 2.0 reference path layout, the root is:

```text
GET /api/v2
Accept: application/hal+json
```

A successful response MUST use `Content-Type: application/hal+json` and MUST be a HAL Resource Object.

The API root MUST contain:

| Element | Requirement |
| --- | --- |
| `conforms_to` | REQUIRED non-null array of unique absolute URI strings identifying every IRI conformance class claimed for this deployment and API version. |
| `_links.self` | REQUIRED canonical URI of the API root. |
| `_links.service-desc` | REQUIRED machine-readable description of the deployed API applicable to this root. |
| `_links.curies` | REQUIRED whenever a compact `iri:*` relation occurs. |
| API-area links | Conditionally required by §5 when the deployment claims a class belonging to that API area. |

`conforms_to` is ordinary resource data, not a HAL link relation. The snake_case name follows the prevailing IRI JSON property convention; it is an IRI adaptation of the conformance-declaration pattern and is not the OGC `conformsTo` wire property.

The API root URI and every advertised `href` MUST be treated as opaque by clients. A client MUST NOT append path segments, substitute identifiers, or derive another API URI from the example path layout.

## 3. Example Root Representation

The following response describes a deployment claiming the nine initial classes defined in §4 while advertising entry points for seven IRI API areas:

```json
{
  "conforms_to": [
    "https://iri.science/conformance/2.0/core",
    "https://iri.science/conformance/2.0/facility/read",
    "https://iri.science/conformance/2.0/facility/site-read",
    "https://iri.science/conformance/2.0/status/resource-read",
    "https://iri.science/conformance/2.0/status/incident-read",
    "https://iri.science/conformance/2.0/status/event-read",
    "https://iri.science/conformance/2.0/compute/resource-discovery",
    "https://iri.science/conformance/2.0/compute/job-read",
    "https://iri.science/conformance/2.0/compute/job-submit"
  ],
  "_links": {
    "self": {
      "href": "https://api.olcf.ornl.gov/api/v2"
    },
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:account": {
      "href": "https://api.olcf.ornl.gov/api/v2/account",
      "title": "OLCF account API",
      "type": "application/hal+json"
    },
    "iri:compute": {
      "href": "https://api.olcf.ornl.gov/api/v2/compute",
      "title": "OLCF compute API",
      "type": "application/hal+json"
    },
    "iri:facility": {
      "href": "https://api.olcf.ornl.gov/api/v2/facility",
      "title": "OLCF facility API",
      "type": "application/hal+json"
    },
    "iri:filesystem": {
      "href": "https://api.olcf.ornl.gov/api/v2/filesystem",
      "title": "OLCF filesystem API",
      "type": "application/hal+json"
    },
    "iri:status": {
      "href": "https://api.olcf.ornl.gov/api/v2/status",
      "title": "OLCF status API",
      "type": "application/hal+json"
    },
    "iri:storage": {
      "href": "https://api.olcf.ornl.gov/api/v2/storage",
      "title": "OLCF storage API",
      "type": "application/hal+json"
    },
    "iri:task": {
      "href": "https://api.olcf.ornl.gov/api/v2/task",
      "title": "OLCF task API",
      "type": "application/hal+json"
    },
    "service-desc": {
      "href": "https://api.olcf.ornl.gov/openapi.json",
      "title": "OLCF's IRI Facility API OpenAPI description",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

The example claims conformance only for `core`, Facility, Status, and the listed Compute behaviors. The `iri:account`, `iri:filesystem`, `iri:storage`, and `iri:task` links advertise navigable API-area entry points but do not, by themselves, make a standardized conformance claim for operations in those areas. Additional conformance classes may be registered later without changing the root representation schema.

## 4. Initial Conformance Classes

Canonical class identifiers use:

```text
https://iri.science/conformance/2.0/<class>
```

A class identifier is distinct from a DOE-IRI URN, a Representation Profile URI, a link-relation URI, an API endpoint, and an OpenAPI document URI. Matching is by exact identifier. Path hierarchy within the identifier is organizational and MUST NOT imply unregistered inheritance.

Every non-core class defined below depends on `https://iri.science/conformance/2.0/core`. Additional dependencies are listed explicitly.

| Class | Required IRI behavior | Current OpenAPI operations | Additional dependency |
| --- | --- | --- | --- |
| `core` | Provide the API root, complete `conforms_to`, HAL link processing, `self`, canonical IRI CURIE processing, API-area-link consistency, and deployed `service-desc` behavior defined by this RFC. | Proposed `GET /api/v2`; not present in the reviewed OpenAPI. | None |
| `facility/read` | Retrieve the Facility representation, including the defined `modified_since` processing and response/error contract. | `GET /api/v2/facility`; `getFacility` | `core` |
| `facility/site-read` | List Sites with defined filtering and pagination, retrieve a Site by identifier, and preserve the registered `iri:has-site` semantics when links are advertised. | `GET /api/v2/facility/sites`; `getSites`. `GET /api/v2/facility/sites/{site_id}`; `getSite` | `facility/read` |
| `status/resource-read` | List and filter Resources, including Resource Type URN prefix matching, and retrieve a Resource by identifier. | `GET /api/v2/status/resources`; `getResources`. `GET /api/v2/status/resources/{resource_id}`; `getResource` | `core` |
| `status/incident-read` | List and filter Incidents without their Events and retrieve an Incident with its Events by identifier. | `GET /api/v2/status/incidents`; `getIncidents`. `GET /api/v2/status/incidents/{incident_id}`; `getIncident` | `core` |
| `status/event-read` | List and filter Events and retrieve an Event by identifier. | `GET /api/v2/status/events`; `getEventsByIncident`. `GET /api/v2/status/events/{event_id}`; `getEventByIncident` | `core` |
| `compute/resource-discovery` | List Resources accepted by the deployment's Compute API. This is deployment operation support, not a guarantee that every returned Resource supports every compute operation. | `GET /api/v2/compute/resources`; `getComputeResources` | `core` |
| `compute/job-read` | Retrieve one Job and its status and query multiple Job statuses, including the defined historical, specification-inclusion, filtering, and pagination behavior. The multi-Job query remains `POST`. | `GET /api/v2/compute/status/{resource_id}/{job_id}`; `getJob`. `POST /api/v2/compute/status/{resource_id}`; `getJobs` | `compute/resource-discovery` |
| `compute/job-submit` | Submit an OpenAPI `JobSpec`, enforce the defined project/account selection rule, implement the defined optional `Idempotency-Key` behavior, and return the defined `Job` representation. | `POST /api/v2/compute/job/{resource_id}`; `launchJob` | `compute/resource-discovery` and `compute/job-read` |

A producer MUST claim a class only when it satisfies every requirement in the class definition, including applicable validation, response, error, and security behavior. Exposing a route or returning a successful response in one case is insufficient.

A class claim applies to deployment support. It does not state that the caller is authorized, that an allocation exists, that every Resource supports the behavior, or that the service is presently healthy.

The class registry created by adoption of this RFC MUST record, for each class:

- canonical identifier and version applicability;
- required operations and semantic behavior;
- explicit dependencies;
- applicable profiles and registered relations;
- lifecycle status and change controller; and
- conformance tests.

Published requirements MUST NOT change incompatibly under an existing class identifier.

## 5. API-Area Entry-Point Relations

This RFC requests registration of the following API-area link relations. Until their individual definitions are added to the DOE-IRI Link Relation Index, they MUST be treated as proposals rather than registered `iri:*` relations.

| Relation | Proposed canonical relation URI | Target meaning | Required by claims |
| --- | --- | --- | --- |
| `iri:account` | `https://iri.science/rels/account` | GET-able HAL entry point for the deployed Account API area. | Any future `account/*` class |
| `iri:compute` | `https://iri.science/rels/compute` | GET-able HAL entry point for the deployed Compute API area. | Any `compute/*` class |
| `iri:facility` | `https://iri.science/rels/facility` | GET-able HAL entry point for the deployed Facility API area. | Any `facility/*` class |
| `iri:filesystem` | `https://iri.science/rels/filesystem` | GET-able HAL entry point for the deployed Filesystem API area. | Any future `filesystem/*` class |
| `iri:status` | `https://iri.science/rels/status` | GET-able HAL entry point for the deployed Status API area. | Any `status/*` class |
| `iri:storage` | `https://iri.science/rels/storage` | GET-able HAL entry point for the deployed Storage API area. | Any future `storage/*` class |
| `iri:task` | `https://iri.science/rels/task` | GET-able HAL entry point for the deployed Task API area. | Any future `task/*` class |

Each relation has a singular `0..1` cardinality at the API root. Its target is an API-area entry-point resource, not a Resource Type, Representation Profile, conformance document, or assertion that every operation in the area is implemented.

If a deployment claims any conformance class mapped to an API area, the corresponding root relation MUST be present. A root relation MAY be present without a conformance claim when the deployment provides a navigable API area but makes no claim against an adopted IRI class for that behavior. A client MUST use `conforms_to`, not link presence alone, to decide whether standardized behavior is guaranteed.

An API-area link:

- identifies where to begin navigation for that area;
- does not specify an HTTP method other than the relation's required safe GET traversal;
- does not grant authorization;
- does not assert current availability; and
- does not replace Resource-specific or operation-specific relations.

The optional HAL `title` is a human-readable label. The `type` member is a target representation hint and MUST be `application/hal+json` only when the target actually offers that representation.

On successful retrieval, an API-area entry point MUST provide `self` and an applicable `service-desc`, and SHOULD expose further standard or registered relations relevant to that area. Clients MUST continue traversal or use the deployed OpenAPI contract; they MUST NOT construct subordinate paths from the area URI.

## 6. Relationship Between Conformance and Links

The initial class-to-root-link requirements are:

| Claimed class | Required root links |
| --- | --- |
| `core` | `self`, `service-desc`, and `curies` when any `iri:*` relation is present |
| `facility/read` | `iri:facility` |
| `facility/site-read` | `iri:facility` |
| `status/resource-read` | `iri:status` |
| `status/incident-read` | `iri:status` |
| `status/event-read` | `iri:status` |
| `compute/resource-discovery` | `iri:compute` |
| `compute/job-read` | `iri:compute` |
| `compute/job-submit` | `iri:compute` |

The three discovery layers have different scopes:

1. `conforms_to` states deployment-level support independently of the caller.
2. API-area links identify stable entry points into that deployed API.
3. Resource- and representation-level links identify context-specific relationships and operation affordances and MAY be authorization-filtered under their registered semantics.

For example, `compute/job-submit` claims that the deployment implements the standardized job-submission behavior. On a compute-system Resource where submission is applicable and visible, `iri:submit-job` identifies the actual operation entry point. The current registered `iri:submit-job` relation may be omitted based on authorization; its absence in one representation does not contradict the deployment-level class claim.

The deployed OpenAPI description advertised through `service-desc` supplies the HTTP method, parameters, request body, responses, errors, security requirements, and server resolution. For operation affordances governed by the companion RFC, the OpenAPI Operation Object uses `x-iri-relation` to bind the canonical relation URI to that operation.

A `service-desc` link describes the deployed service; it does not assert IRI conformance. The canonical IRI OpenAPI is an appropriate target only when it accurately describes the deployed service applicable to the link context.

## 7. Proposed URL Structure and Compatibility

The reviewed IRI 2.0 OpenAPI does not currently define `GET /api/v2` or exact GET operations at `/api/v2/account`, `/api/v2/compute`, `/api/v2/filesystem`, `/api/v2/status`, or `/api/v2/storage`. It currently defines `GET /api/v2/facility` as `getFacility` and `GET /api/v2/task` as `getTasks`, whose successful response is an `application/json` array.

Consequently, the example URL structure requires the following additive work:

| Example path | Current reviewed contract | Proposed HAL behavior |
| --- | --- | --- |
| `/api/v2` | No exact path operation | Add the API root defined in §2. |
| `/api/v2/account` | No exact path operation | Add a GET-able Account API-area entry point. |
| `/api/v2/compute` | No exact path operation | Add a GET-able Compute API-area entry point. |
| `/api/v2/facility` | Existing `getFacility` | Add an `application/hal+json` Facility representation carrying applicable links while preserving the existing contract during migration. |
| `/api/v2/filesystem` | No exact path operation | Add a GET-able Filesystem API-area entry point. |
| `/api/v2/status` | No exact path operation | Add a GET-able Status API-area entry point. |
| `/api/v2/storage` | No exact path operation | Add a GET-able Storage API-area entry point. |
| `/api/v2/task` | Existing `getTasks` returns an `application/json` array | Add an `application/hal+json` alternative selected through content negotiation, or advertise a distinct HAL entry-point URI. The existing JSON response MUST remain available during the compatibility period. |

When one URI supplies both `application/json` and `application/hal+json`, the server MUST perform HTTP content negotiation and SHOULD emit `Vary: Accept`. The applicable OpenAPI description MUST document both representations.

A deployment MAY use different URIs from the example. Conformance depends on advertised relation semantics and behavior, not path spelling. A producer MUST NOT advertise an API-area link with `type: application/hal+json` until that target representation is implemented.

## 8. OpenAPI Additions

Adoption requires an OpenAPI operation for the API root. The following fragment is illustrative; the production OpenAPI remains authoritative after an approved change:

```yaml
paths:
  /api/v2:
    get:
      operationId: getApiRoot
      summary: Discover IRI API conformance and entry points
      responses:
        '200':
          description: IRI API root
          content:
            application/hal+json:
              schema:
                $ref: '#/components/schemas/IriApiRoot'

components:
  schemas:
    IriApiRoot:
      type: object
      required:
        - conforms_to
        - _links
      properties:
        conforms_to:
          type: array
          uniqueItems: true
          items:
            type: string
            format: uri
        _links:
          $ref: '#/components/schemas/HalLinks'
      additionalProperties: true
```

The generic `HalLinks` schema is insufficient by itself to express all root semantics. The OpenAPI description for `IriApiRoot` MUST additionally document the required `self`, `service-desc`, conditional CURIE, class-to-area-link consistency, and singular API-area relation rules.

Deployment OpenAPI documents MUST describe only implemented operations and representations. A conformance claim, advertised area link, and deployed OpenAPI description MUST NOT contradict one another.

## 9. Producer and Consumer Requirements

A producer:

- MUST publish a complete `conforms_to` declaration for the represented deployment and IRI version;
- MUST NOT filter deployment-level class claims based on the caller's permissions;
- MUST provide every root link required by its claims;
- MUST ensure each advertised target and media-type hint is accurate;
- MUST update the root representation when implementation support or entry-point locations change; and
- MUST NOT include credentials, bearer tokens, private keys, or other secrets in links.

A provider MAY require authentication before returning the API root. If it cannot disclose a complete declaration to a caller, it SHOULD deny access rather than return a partial list that appears complete.

A consumer:

- MUST compare class identifiers exactly;
- MUST tolerate and ignore unknown class identifiers unless they are required for its workflow;
- MUST treat a missing `conforms_to` property as unknown support from a non-adopting or nonconforming deployment;
- SHOULD treat omission of a required class as absence of an interoperable support guarantee and avoid depending on that behavior;
- MUST follow advertised links instead of constructing facility URLs;
- MUST consult the applicable deployed OpenAPI before invoking an operation; and
- MUST still handle normal authentication, authorization, validation, conflict, availability, and execution failures.

## 10. Authorization, Availability, and Caching

A conformance claim is not an authorization or allocation grant. An API-area link is not evidence that the caller can invoke every operation in that area.

Temporary outages, queue state, capacity, schedulability, Resource status, or allocation balance MUST NOT alter deployment conformance claims. Temporary conditions are reported through the relevant status and error mechanisms. Stable API-area links SHOULD remain advertised during temporary outages.

The root representation SHOULD be cacheable and SHOULD expose a validator such as `ETag`. A producer MUST change the validator when `conforms_to` or `_links` changes. Caller-independent root representations are preferred. If representation content varies by authorization, the server MUST apply appropriate cache controls and the response no longer satisfies this RFC's requirement for a complete, caller-independent conformance declaration.

Clients MUST NOT automatically forward credentials to a different origin merely because an advertised link names it.

## 11. Adoption and Verification

Adoption requires coordinated changes:

1. Add `GET /api/v2` and `IriApiRoot` to IRI 2.0 OpenAPI.
2. Establish a governed conformance-class registry and publish the nine definitions and their tests.
3. Register `iri:account`, `iri:compute`, `iri:facility`, `iri:filesystem`, `iri:status`, `iri:storage`, and `iri:task` through individual relation definitions and add them to the Link Relation Index.
4. Add or negotiate HAL representations for the advertised API-area entry points.
5. Ensure the deployment-specific OpenAPI describes the actual root, area representations, operations, media types, and security.
6. Coordinate Resource operation discovery with the Resource Operation Affordances RFC rather than duplicating its relation mappings.
7. Test completeness, exact identifier matching, class dependencies, link requirements, URL opacity, media-type accuracy, authorization separation, and OpenAPI consistency.

An implementation MUST NOT claim one of these classes or emit one of the proposed `iri:*` API-area relations as a registered IRI semantic until its governing definition has been adopted.

## References

Repository references are pinned to the reviewed commit.

1. [IRI 2.0 OpenAPI](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/specification-v2/openapi/all_spec_v2.yaml).
2. [HAL `_links` for the IRI Facility API](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/rfc/rfc-hal-links.md).
3. [Migrating `Resource.supported_endpoints` to HAL Operation Affordances](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/rfc/rfc-resource-operation-affordances.md).
4. [DOE-IRI Link Relation Index](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/registry/relations/README.md) and [`iri:submit-job`](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/registry/relations/submit-job.md).
5. [IRI Representation Profiles](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/registry/profiles/README.md) and [Type-Specific Attributes RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/896be8af387ebc8c0837a8fcea4f0b61cd7a0176/rfc/rfc-type-specific-attributes.md).
6. [OGC API Common, Part 1: Core, §9.3](https://docs.ogc.org/is/19-072/19-072.html) — conformance-declaration design precedent.
7. [RFC 8631](https://www.rfc-editor.org/rfc/rfc8631.html) — `service-desc`.
8. [JSON Hypertext Application Language, draft-kelly-json-hal-11](https://datatracker.ietf.org/doc/html/draft-kelly-json-hal-11) — HAL representation conventions; expired Internet-Draft.
9. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) and [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html) — HTTP semantics and caching.
10. [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html) — requirements language.
