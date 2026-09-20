---
layout: default
title: IRI API URL Structure
parent: IRI Architecture
nav_order: 2
permalink: /api-url-structure/
---

# IRI API URL Structure

This page describes how the IRI Facility API v2 HTTP namespace is organized and
how URL organization differs from the semantic Resource model.

The OpenAPI specification remains authoritative for exact paths, methods,
parameters, request bodies, and responses.

---

## 1. Base API Namespace

IRI v2 endpoints are organized beneath:

```text
/api/v2/
```

The first path segment after the version identifies the functional API domain.

Conceptually:

```text
/api/v2/<domain>/...
```

The current production OpenAPI is modularized into the following functional
areas:

```text
facility
status
account
compute
filesystem
storage
task
```

with shared schemas maintained in `_components.yaml`.

---

## 2. General URL Pattern

Many IRI resources follow the familiar collection/item pattern:

```text
/api/v2/<domain>/<collection>
/api/v2/<domain>/<collection>/<identifier>
```

For example:

```text
GET /api/v2/status/resources
GET /api/v2/status/resources/{resource_id}
```

Some representations are singleton resources.

For example:

```text
GET /api/v2/facility
```

The Facility API also exposes Sites as a collection:

```text
GET /api/v2/facility/sites
GET /api/v2/facility/sites/{site_id}
```

---

## 3. Functional Domains

| Domain | URL namespace | Architectural purpose |
|---|---|---|
| Facility | `/api/v2/facility/...` | Facility identity, metadata, and Site discovery. |
| Status | `/api/v2/status/...` | Resource discovery, status, incidents, and events. |
| Account | `/api/v2/account/...` | Capabilities, projects, project allocations, and user allocations. |
| Compute | `/api/v2/compute/...` | Compute-oriented operations such as job submission and job access. |
| Filesystem | `/api/v2/filesystem/...` | Filesystem operation endpoints and related request/response contracts. |
| Storage | `/api/v2/storage/...` | Storage-oriented operations and contracts. |
| Task | `/api/v2/task/...` | Asynchronous task monitoring and retrieval. |

The exact endpoints within each namespace MUST be obtained from the current
OpenAPI specification.

---

## 4. URL Structure Is Not the Resource Taxonomy

This distinction is fundamental.

```text
HTTP path
    organizes an API implementation

Resource Type URN
    identifies semantic classification
```

For example:

```text
/api/v2/status/resources/frontier
```

may return:

```json
{
  "id": "frontier",
  "resource_type": "urn:doe-iri:resource:compute:system"
}
```

The fact that the Resource is a compute system does not require its
representation to be located under:

```text
/api/v2/compute/system/...
```

The status Resource endpoint and the compute operation namespace serve
different architectural purposes.

---

## 5. Do Not Construct URLs from `resource_type`

A Resource Type URN MUST NOT be treated as a path template.

This is incorrect:

```text
resource_type =
urn:doe-iri:resource:compute:system

therefore job submission must be:
/api/v2/compute/jobs/{id}
```

Instead, the Resource advertises the applicable operation:

```json
{
  "_links": {
    "iri:submit-job": {
      "href": "https://api.example.org/api/v2/compute/job/frontier"
    }
  }
}
```

The client uses:

```text
resource_type
    to understand what kind of Resource it discovered

_links
    to discover the applicable target URI

OpenAPI
    to understand how to invoke the target
```

---

## 6. Collection and Object Identity

The URL path identifies the retrievable API representation.

The object's semantic identity is expressed by the representation itself and
its `self` link when HAL links are present.

Example:

```json
{
  "id": "frontier",
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/frontier",
      "profile": "https://iri.science/profiles/resource-definition/compute/system"
    }
  }
}
```

The `self` URI answers:

```text
WHERE is this representation?
```

The target profile answers:

```text
WHAT semantic representation contract applies?
```

---

## 7. Operation URLs

Operation URLs are not Resource Type identifiers and should not be inferred from
Resource identifiers.

Operation-affordance relations explicitly advertise applicable entry points.

For example:

```text
iri:submit-job
```

means that the target is an applicable job-submission entry point for the
source compute Resource.

Its relation definition determines the semantic meaning.

The OpenAPI specification determines:

- HTTP method;
- path parameters;
- request body;
- response body;
- authentication/security;
- error model.

---

## 8. `service-desc`

A representation may advertise:

```text
service-desc
```

to identify the machine-readable description applicable to the API context.

Example:

```json
{
  "_links": {
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/json"
    }
  }
}
```

This provides an important separation:

```text
operation link
    WHICH operation is applicable and WHERE?

service-desc
    WHERE is the operation contract?

OpenAPI
    HOW is the operation invoked?
```

---

## 9. Why This Matters for Multi-Facility IRI

Different facilities can expose equivalent IRI semantics while using different
deployment routing.

For example:

```text
Facility A
https://facility-a.example/api/v2/compute/job/frontier

Facility B
https://iri.facility-b.example/actions/job-submit/system-42
```

Both can advertise the same semantic relation:

```text
iri:submit-job
```

A generic client therefore does not need facility-specific path templates.

---

## 10. Architectural Summary

```text
/api/v2/...
    organizes HTTP functionality

Resource identifier
    identifies an instance

resource_type
    classifies the Resource

_links
    provides navigable targets

link relation
    explains WHY a target is related/applicable

service-desc
    locates machine-readable API description

OpenAPI
    defines the exact invocation contract
```

---

## Authoritative Source

Current v2 OpenAPI:

https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi

See also:

- [IRI Architecture](architecture.md)
- [IRI Object Model Reference](object-model-reference.md)
- [IRI Agentic Discovery](agentic-discovery.md)
