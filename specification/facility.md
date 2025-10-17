# Facility

## Overview
The **Facility** endpoint returns metadata about the facility itself and discovery links to related resources
(Sites, Locations, Resources, Events, Incidents, Capabilities, Projects, Allocations).

- **Endpoint:** `GET /api/v1/facility`  
- **Produces:** `application/json` (and `application/problem+json` for errors)

## Attributes
| Attribute | Type | Description | Required | Example                                                                                             |
|---|---|---|---|-----------------------------------------------------------------------------------------------------|
| `id` | string | Unique identifier (UUID). | yes | `09a22593-2be8-46f6-ae54-2904b04e13a4`                                                              |
| `self_uri` | URI | Canonical hyperlink to this Facility. | yes | `https://iri.example.com/api/v1/facility`                                                           |
| `name` | string | Long name of the Facility. | yes | `National Energy Research Scientific Computing Center`                                              |
| `description` | string | Human‑readable description. | no | `NERSC is the mission scientific computing facility for the U…`                                     |
| `last_modified` | date-time | Timestamp (ISO 8601) when this Facility was last modified. | yes | `2025-10-15T01:00:50.000Z`                                                                          |
| `short_name` | string | Common/short name of the facility. | no | `NERSC`                                                                                             |
| `organization_name` | string | Operating organization’s name. | no | `Lawrence Berkeley National Laboratory`                                                             |
| `support_uri` | URI | Link to facility support portal. | no | `https://help.nersc.gov/`                                                                           |
| `site_uris` | URI[] | URIs of associated Sites (hasSite). | no | [`https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45`]              |
| `location_uris` | URI[] | URIs of associated Locations (hasLocation). | no | [`https://iri.example.com/api/v1/facility/locations/b1c7773f-4624-4787-b1e9-46e1c78c3320`]          |
| `resource_uris` | URI[] | URIs of contained Resources (hasResource). | no | [`https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc`]            |
| `event_uris` | URI[] | URIs of Events in this Facility (hasEvent). | no | [`https://iri.example.com/api/v1/status/events/f9d6e700-1807-45bd-9a52-e81c32d40c5a`]               |
| `incident_uris` | URI[] | URIs of Incidents in this Facility (hasIncident). | no | [`https://iri.example.com/api/v1/status/incidents/686efb0a-0f85-4cc9-86a3-f5713ee6ea44`]            |
| `capability_uris` | URI[] | URIs of Capabilities offered by the Facility. | no | [`https://iri.example.com/api/v1/account/capabilities/9b930fc2-7840-47b2-9268-42362b6fe9ee`]        |
| `project_uris` | URI[] | URIs of Projects associated to this Facility. | no | [`https://iri.example.com/api/v1/account/projects/d6bdb597-8393-4747-8f90-6db08ae018ac`]            |
| `project_allocation_uris` | URI[] | URIs of Project Allocations. | no | [`https://iri.example.com/api/v1/account/project_allocations/46dcde57-e88a-49a9-bf7a-c2120cf5a86b`] |
| `user_allocation_uris` | URI[] | URIs of User Allocations. | no | [`https://iri.example.com/api/v1/account/user_allocations/be91d9c1-99bc-47c1-aaa9-3ee82bb8a7d0`]    |


## Endpoint

| Method | Path | Description | Idempotency |
|---|---|---|---|
| GET | `/api/v1/facility` | Retrieve the facility resource | Yes (safe) |

### Request & Response Semantics

**Headers**
- `Accept` — preferred media type (default `application/json`).
- `If-Modified-Since` — conditional GET on `last_modified`; server returns **304 Not Modified** if unchanged.

**Query Parameters**
- `modified_since` — when provided, filters by `last_modified` like `If-Modified-Since` (controller honors either).

**Responses**
- **200 OK** — returns a Facility object.  
  Headers: `Content-Location` (request URI), `Last-Modified` (facility `last_modified`, truncated to seconds).  
- **304 Not Modified** — if `If-Modified-Since` (or `modified_since`) is not earlier than the facility’s `last_modified`.  
- **500 Internal Server Error** — Problem Details.

### Examples

**Request**
```http
GET /api/v1/facility HTTP/1.1
Accept: application/json
If-Modified-Since: 2025-10-15T00:59:00Z
```

**Response (200)**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Location: https://iri.example.com/api/v1/facility
Last-Modified: 2025-10-15T01:00:50.000Z
```

```json
{
  "id": "09a22593-2be8-46f6-ae54-2904b04e13a4",
  "self_uri": "https://iri.example.com/api/v1/facility",
  "name": "National Energy Research Scientific Computing Center",
  "description": "NERSC is the mission scientific computing facility for the U.S. Department of Energy Office of Science, the nation’s single largest supporter of basic research in the physical sciences.",
  "last_modified": "2025-10-15T01:00:50.000Z",
  "short_name": "NERSC",
  "organization_name": "Lawrence Berkeley National Laboratory",
  "support_uri": "https://help.nersc.gov/",
  "site_uris": [
    "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"
  ],
  "location_uris": [
    "https://iri.example.com/api/v1/facility/locations/b1c7773f-4624-4787-b1e9-46e1c78c3320"
  ],
  "resource_uris": [
    "https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc",
    "https://iri.example.com/api/v1/status/resources/29ea05ad-86de-4df8-b208-f0691aafbaa2",
    "https://iri.example.com/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
    "https://iri.example.com/api/v1/status/resources/303a692d-c52b-47f0-8699-045f962650e2",
    "https://iri.example.com/api/v1/status/resources/b06f8043-f96b-4279-8f0a-0e128a73cc32"
  ],
  "event_uris": [
    "https://iri.example.com/api/v1/status/events/f9d6e700-1807-45bd-9a52-e81c32d40c5a",
    "https://iri.example.com/api/v1/status/events/a867806a-f130-40b3-93f3-a2aa05ec7cda",
    "https://iri.example.com/api/v1/status/events/b1313a09-caa0-4755-b9a1-00d5cff59ac7",
    "https://iri.example.com/api/v1/status/events/83a8cf0f-e85b-4f32-acbe-031af26b234a",
    "https://iri.example.com/api/v1/status/events/633b476e-9a5a-45a6-9e5a-3b099d879596",
    "https://iri.example.com/api/v1/status/events/7732bce6-bc6a-4f25-9aa7-2885a0792eb7",
    "https://iri.example.com/api/v1/status/events/10040ca5-86ae-411f-b39d-ef6a629edd0f",
    "https://iri.example.com/api/v1/status/events/200f9b94-58fd-4eef-862d-e41680f4f275",
    "https://iri.example.com/api/v1/status/events/80136146-b571-49ac-8c9f-ef6ea810cf1f",
    "https://iri.example.com/api/v1/status/events/bbb3b05a-3bd7-449f-92f2-a98ebbfccd94",
    "https://iri.example.com/api/v1/status/events/1e0228ea-63b9-4ea9-9c9c-fd090f1e8b9f",
    "https://iri.example.com/api/v1/status/events/0e1bdcf2-122b-4f11-bf9e-c1f8bc916cf3"
  ],
  "incident_uris": [
    "https://iri.example.com/api/v1/status/incidents/686efb0a-0f85-4cc9-86a3-f5713ee6ea44",
    "https://iri.example.com/api/v1/status/incidents/a585fd0f-62b8-4eb3-a751-bf60dc5e8101",
    "https://iri.example.com/api/v1/status/incidents/878573ff-6522-4a39-8b17-3d3cc9cd5e4e",
    "https://iri.example.com/api/v1/status/incidents/c456a2a5-8983-4a2a-99ac-d48c84b81356",
    "https://iri.example.com/api/v1/status/incidents/33816884-3f2d-420d-a627-60f749d8f7d6",
    "https://iri.example.com/api/v1/status/incidents/d8bac71e-46d2-4319-ba10-575fb3ca0747",
    "https://iri.example.com/api/v1/status/incidents/222de383-8d18-4c03-b852-50ac85565779",
    "https://iri.example.com/api/v1/status/incidents/4cc0c46d-5813-4fe2-abbe-4af789e99674",
    "https://iri.example.com/api/v1/status/incidents/b4d9aac4-9f91-4167-9302-2fc29814a30e",
    "https://iri.example.com/api/v1/status/incidents/22dbe91f-939b-4543-a27f-cc2061296d99",
    "https://iri.example.com/api/v1/status/incidents/28f3c398-3f14-4113-8e2b-2ae16a33e792",
    "https://iri.example.com/api/v1/status/incidents/b12295d6-6a1a-476b-b233-c30c0a151f3a"
  ],
  "capability_uris": [
    "https://iri.example.com/api/v1/account/capabilities/9b930fc2-7840-47b2-9268-42362b6fe9ee",
    "https://iri.example.com/api/v1/account/capabilities/dfa2eca9-bec0-47f3-9e1e-c15fc122ea25",
    "https://iri.example.com/api/v1/account/capabilities/87b7692f-8793-447f-ba75-bb0b9c37d9d9",
    "https://iri.example.com/api/v1/account/capabilities/80db7b6e-5746-4d63-8d87-84396a8c29ab"
  ],
  "project_uris": [
    "https://iri.example.com/api/v1/account/projects/d6bdb597-8393-4747-8f90-6db08ae018ac",
    "https://iri.example.com/api/v1/account/projects/863a48f9-447e-4c22-82fb-72bcc6686d4c"
  ],
  "project_allocation_uris": [
    "https://iri.example.com/api/v1/account/project_allocations/46dcde57-e88a-49a9-bf7a-c2120cf5a86b",
    "https://iri.example.com/api/v1/account/project_allocations/237e42bf-62f0-40ea-99af-55a8d518b413",
    "https://iri.example.com/api/v1/account/project_allocations/5053d076-2e12-40f2-a098-71164629131a",
    "https://iri.example.com/api/v1/account/project_allocations/c5eea9d4-c20b-438b-b8f2-df0199bad3bb",
    "https://iri.example.com/api/v1/account/project_allocations/3a2c9d4c-180c-44c7-a59d-df21f963d83d",
    "https://iri.example.com/api/v1/account/project_allocations/43076d5e-a23e-440a-a02f-aca936262dc8",
    "https://iri.example.com/api/v1/account/project_allocations/6ddbd7c4-1872-4490-9313-f0d7090449ac",
    "https://iri.example.com/api/v1/account/project_allocations/1308fbef-b29a-411f-86c1-c471154108ed"
  ],
  "user_allocation_uris": [
    "https://iri.example.com/api/v1/account/user_allocations/be91d9c1-99bc-47c1-aaa9-3ee82bb8a7d0",
    "https://iri.example.com/api/v1/account/user_allocations/a98005a7-a7c0-46de-b64c-950fbc50b6fc",
    "https://iri.example.com/api/v1/account/user_allocations/85c8a6be-a220-4c0c-84ce-e454c9abcd16",
    "https://iri.example.com/api/v1/account/user_allocations/d2bb025c-5ecf-4245-9fee-6e8f4a228cdc",
    "https://iri.example.com/api/v1/account/user_allocations/a8d3c5f7-fb01-4134-9cb3-bb51e68458eb",
    "https://iri.example.com/api/v1/account/user_allocations/8e2b256e-b5f5-4195-80e3-92335499ad09",
    "https://iri.example.com/api/v1/account/user_allocations/c2c6e8f7-2504-4861-b9e1-37e96b3b55b0",
    "https://iri.example.com/api/v1/account/user_allocations/6f74f68d-07ae-4a11-b97d-4e6d57b6e62f"
  ]
}
```

**Response (304)**
```http
HTTP/1.1 304 Not Modified
Last-Modified: Tue, 14 Oct 2025 10:08:39 GMT
```


### Error examples (Problem Details, RFC 9457)

All error responses use media type `application/problem+json` and fields per RFC 9457 (`type`, `title`,
`status`, `detail`, `instance`, plus optional extensions). ([RFC Editor][8])

* **400 validation error** (invalid `modfied_since`):

```json
{
  "type": "https://iri.example.com/problems/invalid-parameter",
  "title": "Invalid parameter",
  "status": 400,
  "detail": "modfied_since must be a date in ISO 8601 standard with timezone offsets.",
  "instance": "/api/v1/facility?modfied_since=Tue, 14 Oct 2025 10:08:39 GMT",
  "invalid_params": [
    { "name": "modfied_since", "reason": "modfied_since must be a date in ISO 8601 standard with timezone offsets." }
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









## OpenAPI 3.1 Snippet
```yaml

```

## Notes
- `Last-Modified` header is computed from the facility model and truncated to seconds (per controller).
- `Content-Location` is set to the request URI.
- No authentication is enforced by this controller method in the reference implementation (read-only discovery).

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
