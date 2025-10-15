# 7. Resource

## Overview
A *Resource* is an entity that either directly delivers a service to an end user or application 
(e.g., a compute node, virtual machine, network endpoint, storage instance), or indirectly supports 
the delivery of such a service by enabling, hosting, or connecting other resources (e.g., authentication 
server, routers, switches, power supplies).  *Resources* are typed, managed, and monitored objects that 
represent the components making up a system’s operational fabric. They are central to service modeling, 
observability, and incident response. A *Resource* will have an associated operational state, events, 
and incidents.

A *Resource* represents a facility component surfaced by a status API so clients can discover and monitor
its identity, description, and last modification timestamp. This document standardizes the representation
and endpoints using OpenAPI 3.1 aligned with JSON Schema 2020-12. 

OpenAPI 3.1 was chosen because it is fully compatible with JSON Schema 2020-12, which improves interoperability
and validation in tooling. ([OpenAPI Initiative Publications][1])

## Attributes
A `resource` is defined with the following attributes:

| Attribute             | Type         | Description                                                                                                                                                                           | Required | Example                                                                                                                                       |
|:----------------------|:-------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                  | string       | The unique identifier for the Resource.  Typically a UUID or URN to provide global uniqueness across facilities.                                                                      | True     | "09a22593-2be8-46f6-ae54-2904b04e13a4"                                                                                                        |
| `self_uri`            | string(uri)  | A hyperlink reference (URI) to this Resource (self).                                                                                                                                  | True     | "https://iri.example.com/api/v1/status/resources/09a22593-2be8-46f6-ae54-2904b04e13a4"                                                            |
| `name`                | string       | The long name of the Resource.                                                                                                                                                        | False    | "Data Transfer Nodes"                                                                                                                         |
| `description`         | string       | A description of the Resource.                                                                                                                                                        | False    | "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS." |
| `last_modified`       | string       | The date this Resource was last modified.  ISO 8601 standard with timezone offsets.                                                                                                   | False    | "2025-07-24T02:31:13.000Z"                                                                                                                    |
| `resource_type`       | ResourceType | The type of Resource based on string ENUM values.                                                                                                                                     | True     | "compute"                                                                                                                                     |
| `capability_uris`     | array[string] | Hyperlink references (URIs) to capabilities this Resource provides (hasCapability).                                                                                                   | False    | ["https://iri.example.com/api/v1/account/capabilities/b1ce8cd1-e8b8-4f77-b2ab-152084c70281"]                                                      |
| `group`               | string        | The member resource group.                                                                                                                                                            | False    | "storage"                                                                                                                                     |
| `current_status`      | StatusType    | The current status of this Resource at time of query based on string ENUM values. If there is no last Event associated with the resource to indicate a current status, then currentStatus defaults to "unknown". | True     | "up"                                                                                                                                          |
| `impacted_by_uri`     | string(uri)   | A hyperlink reference (URI) to the last event impacting this Resource (impactedBy).                                                                                                   | False    | "https://iri.example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171"                                                               |
| `located_at_uri`      | string(uri)   | A hyperlink reference (URI) to the Site containing this Resource (locatedAt).                                                                                                         | False    | "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                              |
| `member_of_uri`       | string(uri)   | A hyperlink reference (URI) to facility managing this Resource (memberOf).                                                                                                            | False    | "https://iri.example.com/api/v1/facility"                                                                                                         |
| `depends_on_uris`     | array[string] | A hyperlink reference (URI) a Resource that this Resource depends on (dependsOn).                                                                                                     | False    | ["https://iri.example.com/api/v1/status/resources/b1ce8cd1-e8b8-4f77-b2ab-152084c70281"]                                                          |
| `has_dependent_uris`  | array[string] | A hyperlink reference (URI) to a Resource that depend on this Resource (hasDependent).                                                                                                | False    | ["https://iri.example.com/api/v1/status/resources/8b61b346-b53c-4a8e-83b4-776eaa14cc67"]                                                          |

### ENUM ResourceType

The type of Resource based on its role at the Facility.
```yaml
    "resource_type": {
      "type": "string",
      "description": "The type of resource.",
      "enum": [
        "website",
        "service",
        "compute",
        "system",
        "storage",
        "network",
        "unknown"
      ],
      "example": "system"
    }
```

### ENUM StatusType

The possible status values for a resource.  If there is no last Event associated with the resource to indicate a current status, then currentStatus defaults to "unknown".
```yaml
    "current_status": {
      "type": "string",
      "description": "The current status of this resource at time of query.",
      "enum": [
        "up",
        "degraded",
        "down",
        "unknown"
      ],
      "example": "up"
    },
```

## Relationships to other resources

The `resource` has a set of well-defined relationships that allows for navigation between objects based on 
relationship type.  In this model the type relationship is represented by the attribute name, and the 
target object of the relationship is represented by a URI (`*_uri`).  Relationships with 1-to-many 
cardinalities are represented as lists of URI (`*_uris`). 

The following table describes the relationships contained in `resource` and their destination object type.

| Attribute            | Source   | Relationship   | Destination  | Description                                                                        |
|:---------------------|:---------|:---------------|:-------------|:-----------------------------------------------------------------------------------|
| `self_uri`           | Resource | self           | Resource     | A Resource has a mandatory reference to itself.                                    |
| `impacted_by_uri`    | Resource | impactedBy     | Event        | A Resource is impacted by the last applicable Events.                              |
| `member_of_uri`      | Resource | memberOf       | Facility     | A Resource is a member of one of more Facilities (allowing for a shared resource). |
| `located_at_uri`     | Resource | locatedAt      | Site         | A Resource is located at one Site.                                                 |
| `depends_on_uris`    | Resource | dependsOn      | Resource     | A Resource can depend on zero or more Resources.                                   |
| `has_dependent_uris` | Resource | hasDependent   | Resource     | A Resource can have zero or more dependent Resources.                              |

## Endpoints
The following REST endpoints provide access to Resources available under the Status model:

| Method | Path                                        | Description                                                                                   | Idempotency |
|-------:|:--------------------------------------------|:----------------------------------------------------------------------------------------------|:------------|
|    GET | `/api/v1/status/resources`                  | Retrieve a collection of resources (paginated and filterable). Supports conditional requests. | Yes (safe)  |
|    GET | `/api/v1/status/resources/{resource_id}`    | Retrieve a single resource by ID. Supports conditional requests.                              | Yes (safe)  |

The following REST endpoints provide access to Resources available under the Facility model:

| Method | Path                                        | Description                                                                                   | Idempotency |
|-------:|:--------------------------------------------|:----------------------------------------------------------------------------------------------|:------------|
|    GET | `/api/v1/facility/resources`                | Retrieve a collection of resources (paginated and filterable). Supports conditional requests. | Yes (safe)  |
|    GET | `/api/v1/facility/resources/{resource_id}`  | Retrieve a single resource by ID. Supports conditional requests.                              | Yes (safe)  |

## Request & Response Semantics

### Headers
**`Authorization` (request, string):**
Sends credentials so the user agent can authenticate to the origin server; its value is scheme-specific 
credentials for the realm of the requested resource. It can be sent pre-emptively or after a 
`401 Unauthorized`; proxies MUST NOT modify it. For OAuth 2.0 bearer tokens, use the Bearer scheme: 
`Authorization: Bearer <token>`. ([RFC Editor][6])

**`If-Modified-Since` (request, HTTP-date):**
Makes a `GET`/`HEAD` conditional on the selected representation being newer than the given date; if not newer, 
the server SHOULD return `304 Not Modified` with just useful metadata. Recipients MUST ignore it if the date is
invalid, if there are multiple values, if the method isn’t `GET`/`HEAD`, or if the resource lacks a modification 
date. Caches typically derive it from a prior `Last-Modified`. ([RFC Editor][6])

**`Last-Modified` (response, HTTP-date):**
Provides the server’s timestamp for when the **selected representation** was last modified, to support conditional 
requests and cache freshness evaluation. Servers SHOULD send it whenever they can determine a consistent 
modification time, SHOULD generate it as close as possible to the response `Date`, and MUST NOT set a future time 
relative to the server’s clock. ([RFC Editor][6])

**`Content-Location` (response, URI):**
Gives a URI that identifies a specific resource corresponding to the representation in the response body—i.e., 
a `GET` on that URI (at response time) would yield the same representation. If it equals the target URI, treat 
the body as a current representation of that resource; if it differs, the server asserts the body represents
that other URI (commonly the more specific, negotiated variant for `GET`/`HEAD`). It’s representation metadata, 
not a redirect target. ([RFC Editor][6])

| Header              | Direction | Type      | Required | Notes                                                                                                                                                                                                                       |
|---------------------| --------- |-----------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Authorization`     | request   | string    | no       | `Bearer <token>`; RFC 6750. ([IETF Datatracker][3]).  Unauthenticated access may be allowed by provider.                                                                                                                    |
| `If-Modified-Since` | request   | HTTP-date | no       | Conditional GET; on no change server returns **304** with no body. ([MDN Web Docs][4])                                                                                                                                      |
| `Last-Modified`     | response  | HTTP-date | n/a      | Timestamp of last modification of the selected representation. ([RFC Editor][6])                                                                                                                                            |
| `Content-Location`  | response  | URI       | n/a      | Identifies the specific resource for the representation you just returned. It provides a URI that, at the time the response was generated, would return the same representation if dereferenced with GET. ([RFC Editor][6]) |

### Path params
When a GET operation targets a single resource it can do this through use of path params.  The URL 
template `/api/v1/status/resources/{resource_id}` is used to focus the GET operation to return a 
single `resource` object identified by `{resource_id}`.

  | Name          | In   | Type          | Required | Description                 |
  | ------------- | ---- | ------------- | -------- | --------------------------- |
  | `resource_id` | path | string (UUID) | yes      | Identifier of the resource. |

### Query params (collection)
All query parameters are optional, however, paging is automatically enforced using the `limit` and `offset`
query parameter defaults.  This will restrict any unparameterized GET operation to return the first 100
`resource` objects sorted by `id`. 

The endpoint also supports the `Accept` header and optional `If-Modified-Since` header (RFC 1123 format) for conditional requests as described in the *Headers* section.

| Parameter | Description                                                | Type/Format                                                                       | Default | Required |
|-----------|------------------------------------------------------------|-----------------------------------------------------------------------------------|---------|----------|
| `name` | Filter by resource name.                                      | string                                                                            | - | No |
| `group` | Filter by group name.                                        | string                                                                            | - | No |
| `resource_type` | Filter by resource type.                             | enum: `website`, `service`, `compute`, `system`, `storage`, `network`, `unknown`  | - | No |
| `capability` | Filter by capability names.                             | array of strings                                                                  | - | No |
| `current_status` | Filter by current status.                           | array of enum: `up`, `degraded`, `down`, `unknown`                                | - | No |
| `modified_since` | Filter resources modified since timestamp.          | ISO 8601 timestamp                                                                | - | No |
| `offset` | Number of records to skip for pagination.  Defaults to 0.   | integer                                                                           | `0` | No |
| `limit` | Maximum number of records to return.  Defaults to 100.       | integer                                                                           | `100` | No |

### Security model (authN/authZ).
Endpoints use OAuth 2.0 Bearer access tokens (`Authorization: Bearer …`).  Unauthenticated requests 
yield **401** with `WWW-Authenticate: Bearer`, and authenticated callers without the necessary role 
receive **403**. This follows RFC 6750 and HTTP semantics for 401/403. ([IETF Datatracker][3])

### State transitions / invariants

  * The Facility and Status Endpoints are currently read-only (`GET` only).
  * `id` is immutable; `self_uri` is a stable dereference to this item.
  * Conditional requests MUST follow RFC 9110 semantics: **200** when modified; **304** with no body when not modified. ([RFC Editor][6])

## Examples

THis section contains a set of example `GET` operations on `resource` collections and individual items.
Common errors are also presented.

### Successful response example(s)

----

#### _`resource` Collection GET `/api/v1/status/resources`_

Request:

`% curl -sS -H "Accept: application/json" -i "https://iri.example.com/api/v1/status/resources?limit=1"`

Response **200 OK**:

```json
HTTP/1.1 200
Last-Modified: Tue, 14 Oct 2025 10:08:39 GMT
Content-Location: https://iri.example.com/api/v1/status/resources
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Tue, 14 Oct 2025 15:22:37 GMT
Server: DOE IRI Demo Server

[ {
"id" : "057c3750-4ba1-4b51-accf-b160be683d80",
"self_uri" : "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
"name" : "Data Transfer Nodes",
"description" : "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS.",
"last_modified" : "2025-10-14T03:00:48.000Z",
"resource_type" : "compute",
"group" : "storage",
"current_status" : "up",
"impacted_by_uri" : "https://iri.example.com/api/v1/status/events/6364a479-400c-481f-9980-6c1dd2947958",
"member_of_uri" : "https://iri.example.com/api/v1/facility"
} ]
```

----

#### _`resource` Item GET `/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80`_

Request:

`% curl -sS -H "Accept: application/json" -i "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80"`

Response **200 OK**:

```json
HTTP/1.1 200
Last-Modified: Tue, 14 Oct 2025 03:00:48 GMT
Content-Location: https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Tue, 14 Oct 2025 15:31:15 GMT
Server: DOE IRI Demo Server

{
  "id" : "057c3750-4ba1-4b51-accf-b160be683d80",
  "self_uri" : "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
  "name" : "Data Transfer Nodes",
  "description" : "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS.",
  "last_modified" : "2025-10-14T03:00:48.000Z",
  "resource_type" : "compute",
  "group" : "storage",
  "current_status" : "up",
  "impacted_by_uri" : "https://iri.example.com/api/v1/status/events/6364a479-400c-481f-9980-6c1dd2947958",
  "member_of_uri" : "https://iri.example.com/api/v1/facility"
}
```

----

#### _`resource` Item GET (conditional GET via `If-Modified-Since`)_

Using `If-Modified-Since` on a `GET` makes the request conditional: the server only sends the full representation 
if it has changed since the supplied date; otherwise it replies 304 Not Modified with no message body. The 
practical advantages are (a) less bandwidth and typically lower latency because unchanged resources aren’t 
retransmitted, and (b) efficient cache revalidation because clients/caches can refresh metadata/validators without 
downloading the body. Specs also note that caches commonly derive `If-Modified-Since` from a prior `Last-Modified`, 
and that widespread use of these validators “can substantially reduce unnecessary transfers and improve service 
availability and scalability.”

Request:

```json
% curl -sS -H "Accept: application/json" -H "If-Modified-Since: Tue, 14 Oct 2025 03:00:48 GMT" -v -i "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80"

GET /api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80 HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
If-Modified-Since: Tue, 14 Oct 2025 03:00:48 GMT
```

Response **304 Not Modified**:

```json
HTTP/1.1 304 
Content-Location: https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80
Last-Modified: Tue, 14 Oct 2025 03:00:48 GMT
Date: Tue, 14 Oct 2025 16:12:58 GMT
Server: DOE IRI Demo Server
```

No response body is sent for **304**, per RFC 9110; `If-Modified-Since` behavior is specified by HTTP
semantics and MDN’s reference. ([RFC Editor][6])

----

#### _`resource` Item GET (conditional GET via `modified_since` query parameter)_

Using `modified_since` on a `GET` makes the request conditional similar to the `If-Modified-Since`.  
The only difference is that `modified_since` specifies the date format as ISO 8601 standard date
time.  Each `resource` contains a property named `last_modified` that is also in ISO 8601 standard
date time format and mimics the `Last-Modified` functionality for that `resource`.

Request:

```json
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80?modified_since=2025-10-13T23:00:48-04:00"

GET /api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80?modified_since=2025-10-13T23:00:48-04:00 HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```

Response **200 OK**:

```json
HTTP/1.1 200
Last-Modified: Tue, 14 Oct 2025 18:54:50 GMT
Content-Location: https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Tue, 14 Oct 2025 23:29:30 GMT
Server: DOE IRI Demo Server

{
"id" : "057c3750-4ba1-4b51-accf-b160be683d80",
"self_uri" : "http://localhost:8081/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
"name" : "Data Transfer Nodes",
"description" : "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS.",
"last_modified" : "2025-10-14T18:54:50.000Z",
"resource_type" : "compute",
"group" : "storage",
"current_status" : "up",
"impacted_by_uri" : "http://localhost:8081/api/v1/status/events/68326d6d-16ec-4e14-81b0-52eaf12d8a34",
"member_of_uri" : "http://localhost:8081/api/v1/facility"
}
```

In this case we get a `200 OK` response 

----

### Error examples (Problem Details, RFC 9457)

All error responses use media type `application/problem+json` and fields per RFC 9457 (`type`, `title`, 
`status`, `detail`, `instance`, plus optional extensions). ([RFC Editor][8])

* **400 validation error** (invalid `resource_type`):

```json
{
  "type": "https://iri.example.com/problems/invalid-parameter",
  "title": "Invalid parameter",
  "status": 400,
  "detail": "resource_type must be from defined ENUM set.",
  "instance": "/api/v1/status/resources?resource_type=car",
  "invalid_params": [
    { "name": "size", "reason": "resource_type must be from defined ENUM set." }
  ]
}
```

* **401 unauthorized** (missing or bad token):

```json
{
  "type": "https://iri.example.com/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Bearer token is missing or invalid.",
  "instance": "/api/v1/status/resources"
}
```

The server also includes `WWW-Authenticate: Bearer …` per RFC 6750. ([IETF Datatracker][3])

* **403 forbidden** (authenticated but lacks role):

```json
{
  "type": "https://iri.example.com/problems/forbidden",
  "title": "Forbidden",
  "status": 403,
  "detail": "Caller is authenticated but lacks required role.",
  "instance": "/api/v1/status/resources"
}
```

Use 403 when authentication succeeded but authorization failed, per HTTP guidance. ([MDN Web Docs][9])

* **404 not found** (unknown `resource_id`):

```json
{
  "type": "https://iri.example.com/problems/not-found",
  "title": "Not Found",
  "status": 404,
  "detail": "No resource with id '2c6f4e08-4b0e-4c55-9313-4f4e0a93e111' exists.",
  "instance": "/api/v1/status/resources/2c6f4e08-4b0e-4c55-9313-4f4e0a93e111"
}
```

404 indicates the target resource is not present. ([MDN Web Docs][10])

* **409 conflict** (generic example shown for consistency across resources; not expected from `GET`):

```json
{
  "type": "https://iri.example.com/problems/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "The request conflicts with the current state of the target resource.",
  "instance": "/api/v1/status/resources"
}
```

Conflict indicates a state conflict (typical for write operations), defined by HTTP semantics. ([MDN Web Docs][11])

* **500 internal server error**:

```json
{
  "type": "https://iri.example.com/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred.",
  "instance": "/api/v1/status/resources"
}
```

Represents an unexpected condition preventing the server from fulfilling the request. ([Wikipedia][12])

## OpenAPI 3.1 Snippet (YAML)

A minimal, valid OAS 3.1 description **scoped to this resource**. Uses JSON Schema 2020-12 style and examples; error
responses follow RFC 9457 `application/problem+json`. ([OpenAPI Initiative Publications][1])

```yaml
openapi: 3.1.0
info:
  title: IRI Facility API
  description: This API implements the standard integrated research infrastructure
    specification for facility status.
  termsOfService: "IRI Facility API Copyright (c) 2025. The Regents of the University\
    \ of California, through Lawrence Berkeley National Laboratory (subject to receipt\
    \ of any required approvals from the U.S. Dept. of Energy).  All rights reserved."
  contact:
    name: The IRI Interfaces Subcommittee
    url: https://iri.science/ts/interfaces/
    email: software@es.net
  license:
    name: The 3-Clause BSD License
    url: https://opensource.org/license/bsd-3-clause/
  version: v1
servers:
  - url: http://localhost:8081
    description: Generated server url
tags:
  - name: IRI Status API
    description: |-
      The Status API offers users programmatic access to information on the operational status of various resources within a facility, scheduled maintenance/outage events, and a limited historical record of these events. Designed for quick and efficient status checks of current and future (scheduled) operational status, this API allows developers to integrate facility information into applications or workflows, providing a streamlined way to programmatically access data without manual intervention.

      It should be noted that the operational status of a resource is not an indication of a commitment to provide service, only that the resource is in the described operational state.

      The Facility and Status API is not intended for reporting or monitoring purposes; it does not support asynchronous logging or alerting capabilities, and should not be used to derive any type of up or downtime metrics. Instead, its primary focus is on delivering simple, on-demand access to facility resource status, and scheduled maintenance events.
paths:
  /api/v1/status/resources:
    get:
      tags:
        - getResources
        - IRI Status API
      summary: Get a collection of IRI resources.
      description: Returns a list of IRI resources matching the query.
      operationId: getResources
      parameters:
        - name: Accept
          in: header
          description: Provides media types that are acceptable for the response. At
            the moment application/json is the supported response encoding.
          required: false
          schema:
            type: string
            default: application/json
        - name: If-Modified-Since
          in: header
          description: The HTTP request may contain the If-Modified-Since header requesting
            all models with a last modified time after the specified date. The date
            must be specified in RFC 1123 format.
          required: false
          schema:
            type: string
        - name: modified_since
          in: query
          description: A query parameter imitating the If-Modified-Since header requesting
            all models with a last modified time after the specified date. The date
            must be specified in ISO 8601 format.
          required: false
          schema:
            type: string
            format: date-time
        - name: name
          in: query
          description: The name of the resource.
          required: false
          schema:
            type: string
        - name: offset
          in: query
          description: "An integer value specifying the starting number of resource\
          \ to return, where 0 is the first resource based on identifier sorted order."
          required: false
          schema:
            type: integer
            default: 0
        - name: limit
          in: query
          description: "An integer value specifying the maximum number of resources\
          \ to return, where 100 is the default limit.  Use offset query parameter\
          \ to navigate retrieval of complete set."
          required: false
          schema:
            type: integer
            default: 100
        - name: group
          in: query
          description: The group parameter will filter resources based on group membership.  If
            group is specified then only resources that are a member of the specified
            group will be returned.
          required: false
          schema:
            type: string
        - name: resource_type
          in: query
          description: Return only resources of this type.
          required: false
          schema:
            type: string
        - name: capability
          in: query
          description: Return only resources with this capability.
          required: false
          schema:
            type: array
            items:
              type: string
        - name: current_status
          in: query
          description: Return only resources with these status values.
          required: false
          schema:
            type: array
            items:
              type: string
      responses:
        "200":
          description: OK - Returns a list of available IRI resources matching the
            request criteria.
          headers:
            Content-Location:
              description: "Identifies the specific resource for the representation\
                \ you just returned. It provides a URI that, at the time the response\
                \ was generated, would return the same representation if dereferenced\
                \ with GET."
              style: simple
              schema:
                type: string
            Last-Modified:
              description: The HTTP response should contain the Last-Modified header
                with the date set to the RFC 1123 format of the resource's last modified
                time.
              style: simple
              schema:
                type: string
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Resource"
        "304":
          description: Not Modified - The requested resource was not modified.
          headers:
            Last-Modified:
              description: The HTTP response should contain the Last-Modified header
                with the date set to the RFC 1123 format of the resource's last modified
                time.
              style: simple
              schema:
                type: string
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
        "400":
          description: Bad Request - The server due to malformed syntax or invalid
            query parameters could not understand the client’s request.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "401":
          description: Unauthorized - Requester is not authorized to access the requested
            resource.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "403":
          description: Forbidden - Requester is not authorized to access the requested
            resource.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "500":
          description: Internal Server Error - A generic error message given when
            an unexpected condition was encountered and a more specific message is
            not available.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
  /api/v1/status/resources/{resource_id}:
    get:
      tags:
        - getResource
        - IRI Status API
      summary: Get the IRI resource associated with the specified id.
      description: Returns the matching IRI resource.
      operationId: getResource_1
      parameters:
        - name: Accept
          in: header
          description: Provides media types that are acceptable for the response. At
            the moment application/json is the supported response encoding.
          required: false
          schema:
            type: string
            default: application/json
        - name: If-Modified-Since
          in: header
          description: The HTTP request may contain the If-Modified-Since header requesting
            all models with a last modified time after the specified date. The date
            must be specified in RFC 1123 format.
          required: false
          schema:
            type: string
        - name: modified_since
          in: query
          description: A query parameter imitating the If-Modified-Since header requesting
            all models with a last modified time after the specified date. The date
            must be specified in ISO 8601 format.
          required: false
          schema:
            type: string
            format: date-time
        - name: resource_id
          in: path
          description: resource_id
          required: true
          schema:
            type: string
      responses:
        "200":
          description: OK - Returns a list of available IRI resources matching the
            request criteria.
          headers:
            Content-Location:
              description: "Identifies the specific resource for the representation\
                \ you just returned. It provides a URI that, at the time the response\
                \ was generated, would return the same representation if dereferenced\
                \ with GET."
              style: simple
              schema:
                type: string
            Last-Modified:
              description: The HTTP response should contain the Last-Modified header
                with the date set to the RFC 1123 format of the resource's last modified
                time.
              style: simple
              schema:
                type: string
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Resource"
        "304":
          description: Not Modified - The requested resource was not modified.
          headers:
            Last-Modified:
              description: The HTTP response should contain the Last-Modified header
                with the date set to the RFC 1123 format of the resource's last modified
                time.
              style: simple
              schema:
                type: string
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
        "404":
          description: Not Found - The provider is not currently capable of serving
            resource models.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "400":
          description: Bad Request - The server due to malformed syntax or invalid
            query parameters could not understand the client’s request.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "401":
          description: Unauthorized - Requester is not authorized to access the requested
            resource.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "403":
          description: Forbidden - Requester is not authorized to access the requested
            resource.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
        "500":
          description: Internal Server Error - A generic error message given when
            an unexpected condition was encountered and a more specific message is
            not available.
          headers:
            Content-Type:
              description: Provides media type used to encode the result of the operation
                based on those values provided in the Accept request header. At the
                moment application/json is the only supported Content-Type encoding.
              style: simple
              schema:
                type: string
          content:
            application/problem+json:
              schema:
                $ref: "#/components/schemas/Error"
components:
  schemas:
    Error:
      type: object
      description: "Error structure for REST interface based on RFC 9457, \"Problem\
        \ Details for HTTP APIs.\""
      properties:
        type:
          type: string
          format: uri
          default: about:blank
          description: A URI reference that identifies the problem type.
          example: https://iri.example.com/notFound
        title:
          type: string
          description: "A short, human-readable summary of the problem type."
          example: Not Found
        status:
          type: integer
          format: int32
          description: The HTTP status code generated by the origin server for this
            occurrence of the problem.
          example: 404
          maximum: 599
          minimum: 100
        detail:
          type: string
          description: A human-readable explanation specific to this occurrence of
            the problem.
          example: Descriptive text.
        instance:
          type: string
          format: uri
          description: A URI reference that identifies the specific occurrence of
            the problem.
          example: http://localhost:8081/api/v1/status/events/f9d6e700-1807-45bd-9a52-e81c32d40c5a
      required:
        - instance
        - status
        - type
    Resource:
      type: object
      description: "A Resource is an object that either offers a service to the end\
        \ user, or supports a resource that offers a service to the end user.  This\
        \ resource will have an associated operational state, events, and incidents."
      properties:
        id:
          type: string
          description: The unique identifier for the object.  Typically a UUID or
            URN to provide global uniqueness across facilities.
          example: 09a22593-2be8-46f6-ae54-2904b04e13a4
        self_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to this resource (self)
          example: https://iri.example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171
        name:
          type: string
          description: The long name of the resource.
          example: Lawrence Berkeley National Laboratory
        description:
          type: string
          description: A description of the resource.
          example: Lawrence Berkeley National Laboratory is charged with conducting
            unclassified research across a wide range of scientific disciplines.
        last_modified:
          type: string
          format: date-time
          description: The date this resource was last modified. Format follows the
            ISO 8601 standard with timezone offsets.
          example: 2025-03-11T07:28:24.000−00:00
        resource_type:
          type: string
          description: The type of resource.
          enum:
            - website
            - service
            - compute
            - system
            - storage
            - network
            - unknown
          example: system
        capability_uris:
          type: array
          items:
            type: string
            format: uri
            description: Hyperlink references (URIs) to capabilities this resource
              provides (hasCapability).
            example: https://iri.example.com/api/v1/account/capabilities/b1ce8cd1-e8b8-4f77-b2ab-152084c70281
        group:
          type: string
          description: The member resource group.
          example: PERLMUTTER
        current_status:
          type: string
          description: The current status of this resource at time of query.
          enum:
            - up
            - degraded
            - down
            - unknown
          example: up
        impacted_by_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to the last event impacting this
            Resource (impactedBy).
          example: https://iri.example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171
        located_at_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to the Site containing this Resource
            (locatedAt).
          example: https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45
        member_of_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to facility managing this Resource
            (memberOf).
          example: https://iri.example.com/api/v1/facility
        depends_on_uris:
          type: array
          items:
            type: string
            format: uri
            description: A hyperlink reference (URI) a Resource that this Resource
              depends on (dependsOn).
            example: https://iri.example.com/api/v1/status/resources/b1ce8cd1-e8b8-4f77-b2ab-152084c70281
        has_dependent_uris:
          type: array
          items:
            type: string
            format: uri
            description: A hyperlink reference (URI) to a Resource that depend on
              this Resource (hasDependent).
            example: https://iri.example.com/api/v1/status/resources/8b61b346-b53c-4a8e-83b4-776eaa14cc67
      required:
        - current_status
        - id
        - impacted_by_uri
        - last_modified
        - name
        - resource_type
        - self_uri
```

## Notes & Decisions

* **Versioning rationale.** The API is versioned under `/api/v1` to allow additive, backward-compatible evolution following common REST versioning practices while keeping path stability. (OpenAPI 3.1 is used to describe the interface.) ([OpenAPI Initiative Publications][1])
* **Pagination/filtering rules.** Page-based query parameters (`offset`, `limit`) are provided so clients can traverse pages by relation rather than by constructing URLs. ([IETF Datatracker][2])
* **Sorting rules.** `sort` uses `<field>,<direction>`; unrecognized fields are rejected with **400**.
* **Cachingvrules.** Clients may send `If-Modified-Since` on no changes the server responds **304** with no body. ([RFC Editor][6])

## Changelog

* 2025-10-05 – Initial draft.

---

### Standards referenced

* OpenAPI 3.1.0 (alignment with JSON Schema 2020-12). ([OpenAPI Initiative Publications][1])
* JSON Schema 2020-12. ([JSON Schema][13])
* Problem Details for HTTP APIs (RFC 9457). ([RFC Editor][8])
* HTTP Semantics and conditional requests (RFC 9110); 304 rules. ([RFC Editor][6])
* `If-Modified-Since` reference and behavior; caching overview and ETag precedence. ([MDN Web Docs][4])
* Pagination links via HTTP `Link` header (RFC 8288). ([IETF Datatracker][2])
* OAuth 2.0 Bearer token usage (RFC 6750). ([IETF Datatracker][3])

> **Transparency note.** Where exact deployment behaviors are not mandated by Internet standards (e.g., which fields are indexed for filtering), this document states explicit choices to ensure a precise, executable contract, and cites relevant standards for the underlying semantics. I cannot confirm site-specific policies beyond those standards.

[1]: https://spec.openapis.org/oas/v3.1.0.html?utm_source=chatgpt.com "OpenAPI Specification v3.1.0"
[2]: https://datatracker.ietf.org/doc/html/rfc8288?utm_source=chatgpt.com "RFC 8288 - Web Linking"
[3]: https://datatracker.ietf.org/doc/html/rfc6750?utm_source=chatgpt.com "RFC 6750 - The OAuth 2.0 Authorization Framework"
[4]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Modified-Since?utm_source=chatgpt.com "If-Modified-Since header - HTTP - MDN"
[5]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching?utm_source=chatgpt.com "HTTP caching - MDN - Mozilla"
[6]: https://www.rfc-editor.org/rfc/rfc9110.html?utm_source=chatgpt.com "RFC 9110: HTTP Semantics"
[7]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag?utm_source=chatgpt.com "ETag header - HTTP | MDN - Mozilla"
[8]: https://www.rfc-editor.org/rfc/rfc9457.html?utm_source=chatgpt.com "RFC 9457: Problem Details for HTTP APIs"
[9]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401?utm_source=chatgpt.com "401 Unauthorized - HTTP - MDN - Mozilla"
[10]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/404?utm_source=chatgpt.com "404 Not Found - HTTP - MDN - Mozilla"
[11]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/409?utm_source=chatgpt.com "409 Conflict - HTTP - MDN - Mozilla"
[12]: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes?utm_source=chatgpt.com "List of HTTP status codes"
[13]: https://json-schema.org/specification?utm_source=chatgpt.com "JSON Schema - Specification [#section]"
