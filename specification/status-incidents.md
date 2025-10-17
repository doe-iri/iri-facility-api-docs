# 9. Incidents

## Overview
An **Incident** represents a period of impaired behavior or outage affecting a **Resource**.
Incidents often aggregate multiple **Events** and have a lifecycle (started/resolved). They serve as higher-level status records for users and operators.

## Attributes
| Attribute | Type | Description | Required | Example |
|---|---|---|---|---|
| `id` | string | Unique identifier (UUID). | yes | `0048907a-8569-4f76-aff0-c6c852f5e331` |
| `self_uri` | URI | Canonical hyperlink to this Incident. | yes | `http://localhost:8081/api/v1/status/incidents/0048907a-8569-4f76-aff0-c6c852f5e331` |
| `name` | string | Short, human-readable title. | yes | `unplanned outage on group services` |
| `description` | string | Detailed description of the incident. | no | `Auto-generated incident of type unplanned` |
| `last_modified` | date-time | When this Incident was last modified (ISO 8601). | yes | `2025-05-22T23:34:25.000Z` |
| `status` | StatusType | Current status. | yes | `down` |
| `started_at` | date-time | When the incident started (ISO 8601). | no | `` |
| `resolved_at` | date-time | When the incident was resolved (ISO 8601). | no | `` |
| `resource_uri` | URI | Impacted **Resource**. | yes | `` |

### ENUM StatusType
`up`, `degraded`, `down`, `unknown`

## Relationships to other resources
| Attribute | Source | Relationship | Destination | Description |
|---|---|---|---|---|
| `self_uri` | Incident | self | Incident | Self-reference. |
| `resource_uri` | Incident | impacts | Resource | Incident impacts a Resource. |
| _events_ | Incident | aggregates | Event | An incident aggregates one or more events. |

## Endpoints
| Method | Path | Description | Idempotency |
|---|---|---|---|
| GET | `/api/v1/status/incidents` | Retrieve a collection of incidents | Yes (safe) |
| GET | `/api/v1/status/incidents/{incident_id}` | Retrieve a single incident by ID | Yes (safe) |

## Request & Response Semantics

### Headers
- `Authorization: Bearer <token>` — OAuth 2.0 bearer token.
- `If-Modified-Since: <HTTP-date>` — Conditional GET on `last_modified`; `304 Not Modified` if unchanged (RFC 9110).
- `Last-Modified: <HTTP-date>` — Response header indicating most recent modification time.
- `Content-Location: <URI>` — Response header identifying the URI of the returned representation (RFC 9110).

### Path params
- `incident_id` — UUID of the target Incident.

### Query params (collection)
- `name` — filter by incident name.
- `status` — filter by `StatusType`.
- `from` — return incidents with `started_at >=` this timestamp (ISO 8601).
- `to` — return incidents with `resolved_at <=` this timestamp (ISO 8601).
- `modified_since` — return incidents with `last_modified >` this timestamp.
- `offset` (default `0`) — pagination start index.
- `limit` (default `100`) — page size.

### Security model (authN/authZ)
- OAuth 2.0 bearer tokens; `401` if unauthenticated, `403` if not authorized.

### State transitions / invariants
- Read-only `GET` operations.
- Conditional requests supported with `If-Modified-Since` → `304 Not Modified` when applicable.

## Examples

### Successful response example(s)

#### _`incident` Collection GET `/api/v1/status/incidents` (paginated)_
```http
GET /api/v1/status/incidents?limit=2&offset=0 HTTP/1.1
Accept: application/json
Authorization: Bearer <token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Location: http://localhost:8081/api/v1/status/incidents?limit=2&offset=0
Last-Modified: 2025-05-22T23:34:25.000Z
```

```json
{
  "items": [
    {
      "id": "0048907a-8569-4f76-aff0-c6c852f5e331",
      "self_uri": "http://localhost:8081/api/v1/status/incidents/0048907a-8569-4f76-aff0-c6c852f5e331",
      "name": "unplanned outage on group services",
      "description": "Auto-generated incident of type unplanned",
      "last_modified": "2025-05-22T23:34:25.000Z",
      "status": "down",
      "type": "unplanned",
      "start": "2025-05-22T20:34:25.277Z",
      "end": "2025-05-22T23:34:25.277Z",
      "resolution": "completed",
      "resource_uris": [
        "http://localhost:8081/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
        "http://localhost:8081/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
        "http://localhost:8081/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e",
        "http://localhost:8081/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc",
        "http://localhost:8081/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6"
      ],
      "event_uris": [
        "http://localhost:8081/api/v1/status/events/aa4ad0b9-4c9b-4973-b069-b420a7707930",
        "http://localhost:8081/api/v1/status/events/b874b6f8-c0ed-4daf-b89b-ed0ff6cee9bf",
        "http://localhost:8081/api/v1/status/events/0e253b16-8595-439b-b1fd-ff4d3866b90c",
        "http://localhost:8081/api/v1/status/events/9b7ce748-7076-4cf9-8734-df74f3f47b7f",
        "http://localhost:8081/api/v1/status/events/1e5462a5-cfb5-4970-a9fa-a83048be9ba5",
        "http://localhost:8081/api/v1/status/events/e1aa2c4d-90ab-420c-9fa8-0ca360413278",
        "http://localhost:8081/api/v1/status/events/16c6eb0a-a293-4b6c-ba3d-6f51425bf4a0",
        "http://localhost:8081/api/v1/status/events/cea90b03-0aad-422c-937f-6d9cff1ce67c",
        "http://localhost:8081/api/v1/status/events/d6050c39-e486-4bb6-a742-b0ea8868f0c1",
        "http://localhost:8081/api/v1/status/events/2b7bb153-71d3-4031-98e5-ffc757d06878"
      ]
    },
    {
      "id": "0240606e-0ebf-4159-9ce5-55580bb7e15c",
      "self_uri": "http://localhost:8081/api/v1/status/incidents/0240606e-0ebf-4159-9ce5-55580bb7e15c",
      "name": "unplanned outage on group websites",
      "description": "Auto-generated incident of type unplanned",
      "last_modified": "2025-05-02T15:04:25.000Z",
      "status": "down",
      "type": "unplanned",
      "start": "2025-05-02T15:04:25.379Z",
      "end": "2025-05-02T15:04:25.379Z",
      "resolution": "completed",
      "resource_uris": [
        "http://localhost:8081/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
        "http://localhost:8081/api/v1/status/resources/d3c52e3c-dd2a-47a4-91e7-f06e00cf486d",
        "http://localhost:8081/api/v1/status/resources/b951a092-7f0a-4263-bc9a-700c7ceed415",
        "http://localhost:8081/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc"
      ],
      "event_uris": [
        "http://localhost:8081/api/v1/status/events/445acd99-df4c-4ebb-9edc-5633e1645152",
        "http://localhost:8081/api/v1/status/events/606812f1-2451-4254-8ee5-694f03932587",
        "http://localhost:8081/api/v1/status/events/11951828-d1ce-4394-a1c1-e0e0e9b52499",
        "http://localhost:8081/api/v1/status/events/7411dff5-a0ba-4791-b9d8-74e59854c4b1",
        "http://localhost:8081/api/v1/status/events/2982dea6-4514-4d62-b1f4-76ac66f8deab",
        "http://localhost:8081/api/v1/status/events/1392e14a-bcf3-426d-a652-e8cfb1442653",
        "http://localhost:8081/api/v1/status/events/0111fc7d-f665-40cc-8d6f-d3af643f1a12",
        "http://localhost:8081/api/v1/status/events/34172179-3185-42ec-bb26-bcec993ea8e1"
      ]
    }
  ],
  "offset": 0,
  "limit": 2,
  "count": 2,
  "total": 2,
  "_links": {
    "self": {
      "href": "http://localhost:8081/api/v1/status/incidents?limit=2&offset=0"
    },
    "next": {
      "href": "http://localhost:8081/api/v1/status/incidents?limit=2&offset=2"
    }
  }
}
```

#### _`incident` Item GET `/api/v1/status/incidents/{incident_id}`_
```http
GET http://localhost:8081/api/v1/status/incidents/0048907a-8569-4f76-aff0-c6c852f5e331 HTTP/1.1
Accept: application/json
Authorization: Bearer <token>
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Location: http://localhost:8081/api/v1/status/incidents/0048907a-8569-4f76-aff0-c6c852f5e331
Last-Modified: 2025-05-22T23:34:25.000Z
```

```json
{
  "id": "0048907a-8569-4f76-aff0-c6c852f5e331",
  "self_uri": "http://localhost:8081/api/v1/status/incidents/0048907a-8569-4f76-aff0-c6c852f5e331",
  "name": "unplanned outage on group services",
  "description": "Auto-generated incident of type unplanned",
  "last_modified": "2025-05-22T23:34:25.000Z",
  "status": "down",
  "type": "unplanned",
  "start": "2025-05-22T20:34:25.277Z",
  "end": "2025-05-22T23:34:25.277Z",
  "resolution": "completed",
  "resource_uris": [
    "http://localhost:8081/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
    "http://localhost:8081/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
    "http://localhost:8081/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e",
    "http://localhost:8081/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc",
    "http://localhost:8081/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6"
  ],
  "event_uris": [
    "http://localhost:8081/api/v1/status/events/aa4ad0b9-4c9b-4973-b069-b420a7707930",
    "http://localhost:8081/api/v1/status/events/b874b6f8-c0ed-4daf-b89b-ed0ff6cee9bf",
    "http://localhost:8081/api/v1/status/events/0e253b16-8595-439b-b1fd-ff4d3866b90c",
    "http://localhost:8081/api/v1/status/events/9b7ce748-7076-4cf9-8734-df74f3f47b7f",
    "http://localhost:8081/api/v1/status/events/1e5462a5-cfb5-4970-a9fa-a83048be9ba5",
    "http://localhost:8081/api/v1/status/events/e1aa2c4d-90ab-420c-9fa8-0ca360413278",
    "http://localhost:8081/api/v1/status/events/16c6eb0a-a293-4b6c-ba3d-6f51425bf4a0",
    "http://localhost:8081/api/v1/status/events/cea90b03-0aad-422c-937f-6d9cff1ce67c",
    "http://localhost:8081/api/v1/status/events/d6050c39-e486-4bb6-a742-b0ea8868f0c1",
    "http://localhost:8081/api/v1/status/events/2b7bb153-71d3-4031-98e5-ffc757d06878"
  ]
}
```

#### _Conditional GET via `If-Modified-Since`_
```http
GET http://localhost:8081/api/v1/status/incidents/0048907a-8569-4f76-aff0-c6c852f5e331 HTTP/1.1
Accept: application/json
If-Modified-Since: 2025-06-01T00:00:00Z
```

```http
HTTP/1.1 304 Not Modified
Last-Modified: 2025-05-22T23:34:25.000Z
```

### Error examples (Problem Details, RFC 9457)
```json
{
  "type": "https://example.com/problems/invalid-parameter",
  "title": "Invalid request parameter",
  "status": 400,
  "detail": "Parameter 'status' must be one of: up, degraded, down, unknown",
  "instance": "http://localhost:8081/api/v1/status/incidents?status=bogus"
}
```
```json
{
  "type": "https://example.com/problems/unauthorized",
  "title": "Missing or invalid token",
  "status": 401,
  "detail": "Bearer token is missing, expired, or invalid",
  "instance": "http://localhost:8081/api/v1/status/incidents"
}
```
```json
{
  "type": "https://example.com/problems/forbidden",
  "title": "Insufficient permissions",
  "status": 403,
  "detail": "The authenticated principal is not authorized to access this resource",
  "instance": "http://localhost:8081/api/v1/status/incidents"
}
```
```json
{
  "type": "https://example.com/problems/not-found",
  "title": "Incident not found",
  "status": 404,
  "detail": "No incident found with id 'deadbeef-0000-0000-0000-000000000000'",
  "instance": "http://localhost:8081/api/v1/status/incidents/deadbeef-0000-0000-0000-000000000000"
}
```
```json
{
  "type": "https://example.com/problems/conflict",
  "title": "Conflicting parameters",
  "status": 409,
  "detail": "Only one of 'from' and 'modified_since' may be used for time filtering",
  "instance": "http://localhost:8081/api/v1/status/incidents?from=2025-05-01T00:00:00Z&modified_since=2025-05-02T00:00:00Z"
}
```
```json
{
  "type": "about:blank",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred",
  "instance": "http://localhost:8081/api/v1/status/incidents"
}
```

## OpenAPI 3.1 Snippet (YAML)
```yaml
openapi: 3.1.0
info:
  title: IRI Facility Status API
  version: v1
  description: Incident endpoints for the IRI Facility Status API.
servers:
- url: http://localhost:8081
paths:
  /api/v1/status/incidents:
    get:
      summary: Retrieve a collection of incidents
      operationId: getIncidents
      tags:
      - status
      - incidents
      parameters:
      - name: accept
        in: header
        required: false
        schema:
          type: string
          default: application/json
      - name: If-Modified-Since
        in: header
        required: false
        schema:
          type: string
          format: date-time
      - name: modified_since
        in: query
        required: false
        schema:
          type: string
          format: date-time
      - name: name
        in: query
        required: false
        schema:
          type: string
      - name: status
        in: query
        required: false
        schema:
          type: string
          enum:
          - up
          - degraded
          - down
          - unknown
      - name: from
        in: query
        required: false
        schema:
          type: string
          format: date-time
        description: Return incidents with started_at >= this timestamp.
      - name: to
        in: query
        required: false
        schema:
          type: string
          format: date-time
        description: Return incidents with resolved_at <= this timestamp (or current
          time if unresolved).
      - name: offset
        in: query
        required: false
        schema:
          type: integer
          minimum: 0
          default: 0
      - name: limit
        in: query
        required: false
        schema:
          type: integer
          minimum: 1
          default: 100
      responses:
        '200':
          description: Successful response
          headers:
            Content-Location:
              schema:
                type: string
                format: uri
            Last-Modified:
              schema:
                type: string
                format: date-time
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IncidentCollection'
        '304':
          description: Not Modified
          headers:
            Last-Modified:
              schema:
                type: string
                format: date-time
        '400':
          $ref: '#/components/responses/Problem400'
        '401':
          $ref: '#/components/responses/Problem401'
        '403':
          $ref: '#/components/responses/Problem403'
        '500':
          $ref: '#/components/responses/Problem500'
      security:
      - bearerAuth: []
  /api/v1/status/incidents/{incident_id}:
    get:
      summary: Retrieve a single incident by ID
      operationId: getIncident
      tags:
      - status
      - incidents
      parameters:
      - name: accept
        in: header
        required: false
        schema:
          type: string
          default: application/json
      - name: If-Modified-Since
        in: header
        required: false
        schema:
          type: string
          format: date-time
      - name: modified_since
        in: query
        required: false
        schema:
          type: string
          format: date-time
      - name: incident_id
        in: path
        required: true
        schema:
          type: string
      responses:
        '200':
          description: Successful response
          headers:
            Content-Location:
              schema:
                type: string
                format: uri
            Last-Modified:
              schema:
                type: string
                format: date-time
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Incident'
        '304':
          description: Not Modified
          headers:
            Last-Modified:
              schema:
                type: string
                format: date-time
        '401':
          $ref: '#/components/responses/Problem401'
        '403':
          $ref: '#/components/responses/Problem403'
        '404':
          $ref: '#/components/responses/Problem404'
        '500':
          $ref: '#/components/responses/Problem500'
      security:
      - bearerAuth: []
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Incident:
      type: object
      additionalProperties: false
      properties:
        id:
          type: string
          description: Unique identifier (UUID).
        self_uri:
          type: string
          format: uri
        name:
          type: string
        description:
          type: string
        last_modified:
          type: string
          format: date-time
        status:
          type: string
          enum:
          - up
          - degraded
          - down
          - unknown
        started_at:
          type: string
          format: date-time
        resolved_at:
          type: string
          format: date-time
        resource_uri:
          type: string
          format: uri
      required:
      - id
      - self_uri
      - name
      - last_modified
      - status
      - resource_uri
    IncidentCollection:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/Incident'
        offset:
          type: integer
          minimum: 0
        limit:
          type: integer
          minimum: 1
        count:
          type: integer
          minimum: 0
        total:
          type: integer
          minimum: 0
        _links:
          type: object
          additionalProperties: true
      required:
      - items
    Problem:
      type: object
      properties:
        type:
          type: string
          format: uri-reference
        title:
          type: string
        status:
          type: integer
          minimum: 100
          maximum: 599
        detail:
          type: string
        instance:
          type: string
          format: uri
      required:
      - type
      - title
      - status
  responses:
    Problem400:
      description: Bad Request
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/Problem'
    Problem401:
      description: Unauthorized
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/Problem'
    Problem403:
      description: Forbidden
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/Problem'
    Problem404:
      description: Not Found
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/Problem'
    Problem500:
      description: Internal Server Error
      content:
        application/problem+json:
          schema:
            $ref: '#/components/schemas/Problem'
```

## Notes & Decisions
- **Versioning.** Endpoints under `/api/v1/...`
- **Pagination.** `offset` + `limit` paging; results sorted deterministically (by id) before slicing per controller pattern.
- **Filtering.** `status` applies to incident’s status; `from`/`to` filter by `started_at`/`resolved_at`; `modified_since` filters by `last_modified`.
- **Caching.** Conditional GET support via `If-Modified-Since`; responses include `Last-Modified` & `Content-Location`.

## Changelog
- 2025-10-15 — Initial draft for Incidents based on `StatusController.java` and existing docs style.

## Sources (from attached repo)
- `docs/status-resources.md`
- `src/main/java/net/es/iri/api/facility/StatusController.java`
- `src/main/java/net/es/iri/api/facility/schema/Incident.java`
- `src/main/java/net/es/iri/api/facility/schema/NamedObject.java`
- `examples/incidents.json`