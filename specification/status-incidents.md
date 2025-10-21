# 6.3. Incidents

## Overview
An **Incident** represents a discrete occurrence, planned or unplanned, that actually or potentially affects
the availability, performance, integrity, or security of one or more **Resources** at a given **Facility**.
**Incidents** serves as a high-level grouping construct for aggregating and tracking related **Events** over 
time and across multiple system components acting as higher-level status records for users and operators.

An Incident represents a discrete occurrence, planned or unplanned, that actually or potentially affects 
the availability, performance, integrity, or security of one or more Resources at a given Facility. It 
serves as a high-level grouping construct for aggregating and tracking related Events over time and 
across multiple system components.

[TODO: Need to document the behaviour of Incident across the lifetime of an instance.]

## Attributes
An `incident` is defined with the following attributes:

| Attribute       | Type           | Description                                                                                                                                                                                                      | Required | Example                                                                                                                                       |
|:----------------|:---------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| `id`            | string         | The unique identifier for the Incident.  Typically a UUID or URN to provide global uniqueness across facilities.                                                                                                 | True     | "09a22593-2be8-46f6-ae54-2904b04e13a4"                                                                                                        |
| `self_uri`      | URI            | A hyperlink reference (URI) to this Incident (self).                                                                                                                                                             | True     | "https://iri.example.com/api/v1/status/resources/09a22593-2be8-46f6-ae54-2904b04e13a4"                                                            |
| `name`          | string         | The long name of the Incident.                                                                                                                                                                                   | False    | "Data Transfer Nodes"                                                                                                                         |
| `description`   | string         | A description of the Incident.                                                                                                                                                                                   | False    | "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS." |
| `last_modified` | string         | The date this Incident was last modified.  ISO 8601 standard with timezone offsets.                                                                                                                              | False    | "2025-07-24T02:31:13.000Z"                                                                                                                    |
| `status`        | StatusType     | The status of the Resource associated with this Incident. | no | `down` |
| `type`          | IncidentType   | The type of Incident based on string ENUM values. | yes | `down` |
| `start`         | date-time      | When the incident started (ISO 8601). | yes | `2023-10-17T11:02:31.690-00:00` |
| `end`           | date-time      | When the incident was resolved (ISO 8601). | no | `2023-10-19T11:02:31.690-00:00` |
| `resolution`    | ResolutionType | The resolution for this Incident. | yes | `pending` |
| `resource_uris` | URI[]          | A hyperlink reference (URI) to the Resources impacted by this Incident (mayImpact). | no | `[ "https://example.com/api/v1/status/resources/03bdbf77-6f29-4f66-9809-7f4f77098171" ]` |
| `events_uris`   | URI[]          | A hyperlink reference (URI) to the Event associated with this Incident (hasEvent). | no | `[ "https://example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171" ]` |

### ENUM StatusType

The possible status values for an `incident`.

```yaml
    StatusType:
      type: string
      description: The current status of this resource at time of query.
      enum:
        - up
        - degraded
        - down
        - unknown
      example: up
```

### ENUM IncidentType

The possible types for an `incident`.

```yaml
    IncidentType:
      type: string
      description: The type of incident.
      enum:
      - planned
      - unplanned
      - reservation
      example: planned
```

### ENUM ResolutionType

The current state of the `incident` resolution.

```yaml
        ResolutionType:
          type: string
          default: pending
          description: The resolution for this incident.
          enum:
          - unresolved
          - cancelled
          - completed
          - extended
          - pending
          example: pending
```

## Relationships to other resources

The `incident` has a set of well-defined relationships that allows for navigation between objects based on
relationship type.  In this model the type relationship is represented by the attribute name, and the
target object of the relationship is represented by a URI (`*_uri`) or URIs (`*_uris`) when a 1-to-many
relationship is modelled.

The following table describes the relationships contained in `incident` and their destination object type.

| Attribute       | Source   | Relationship | Destination | Description                                    |
|-----------------|----------|--------------|-------------|------------------------------------------------|
| `self_uri`      | Incident | self         | Incident    | Self-reference.                                |
| `resource_uris` | Incident | mayImpact    | Resource    | An Incident may impact one or more Resources.  |
| `events_uris`   | Incident | hasEvent     | Event       | An Incident has one or more associated Events. |

## Endpoints

| Method | Path                                               | Description                                                         | Idempotency |
|--------|----------------------------------------------------|---------------------------------------------------------------------|-------------|
| GET    | `/api/v1/status/incidents`                         | Retrieve a collection of `incident`.                                | Yes (safe)  |
| GET    | `/api/v1/status/incidents/{incident_id}`           | Retrieve a single `incident` by ID.                                 | Yes (safe)  |
| GET    | `/api/v1/status/incidents/{incident_id}/events`    | Retrieve list of `event` associated with this `incident`.           | Yes (safe)  |
| GET    | `/api/v1/status/incidents/{incident_id}/resources` | Retrieve list of `resource` that maybe impacted by this `incident`. | Yes (safe)  |

## Request & Response Semantics

### Path params
When a GET operation targets a single `incident` it can do this through use of path params.  The URL
template `/api/v1/status/incidents/{incident_id}` is used to focus the GET operation to return a
single `incident` object identified by `{incident_id}`.

| Name          | In   | Type          | Required | Description                        |
| ------------- | ---- | ------------- | -------- |------------------------------------|
| `incident_id` | path | string (UUID) | yes      | Identifier of the target Incident. |

### Query params (collection)

All query parameters are optional, however, paging is automatically enforced using the `limit` and `offset`
query parameter defaults.  This will restrict any unparameterized GET operation to return the first 100
`incident` objects sorted by `id`.

| Parameter        | Description                                                                                                         | Type/Format                                                                      | Default | Required |
|------------------|---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|---------|----------|
| `name`           | Filter by `incident` name.                                                                                          | string                                                                           | -       | No       |
| `modified_since` | Filter resources modified since timestamp (ISO 8601).                                                               | date-time                                                                        | -       | No       |
| `status`         | A list of StatusType used to filter matching `incident`.                                                            | array of StatusType enum: `up`, `degraded`, `down`, `unknown`                    | -       | No       |
| `type`           | A list of IncidentType used to filter matching `incident`.                                                          | array of IncidentType enum: `planned`, `unplanned`, `reservation`, | -       | No       |
| `resolution`     | A list of ResolutionType used to filter matching `incident`.                                                        | array of ResolutionType enum: `unresolved`, `cancelled`, `completed`, `extended`, `pending`. | -       | No       |
| `offset`         | Number of records to skip for pagination.  Defaults to 0.                                                           | integer         | `0`     | No       |
| `limit`          | Maximum number of records to return.  Defaults to 100.                                                              | integer         | `100`   | No       |
| `time`           | Search for incidents overlapping with this timestamp (ISO 8601), where `start <= time <= end`.                      | date-time       | -       | No       |
| `from`           | Return incidents with `start >=` this timestamp (ISO 8601).                                                         | date-time       | -       | No       |
| `to`             | Return incidents with `end <=` this timestamp (ISO 8601).                                                           | date-time       | -       | No       |
| `resource_uris`  | A list of `resource` URI to match as impacted by the `incident`.  Only one URI need match to include an `incident`. | array of URI    | -       | No       |
| `event_uris`     | A list of `event` URI to match as generated by the `incident`.  Only one URI need match to include an `incident`.   | array of URI    | -       | No       |

### Security model (authN/authZ)

- OAuth 2.0 bearer tokens; `401` if unauthenticated, `403` if not authorized.

### State transitions / invariants

* The Facility and Status Endpoints are currently read-only (`GET` only).
* `id` is immutable; `self_uri` is a stable dereference to this item.
* Conditional requests MUST follow RFC 9110 semantics: **200** when modified; **304** with no body when not modified. ([RFC Editor][6])

## Examples

This section contains a set of example `GET` operations on `incident` collections and individual items.
Common errors are also presented.

| Operation                                               | HTTP Request                                                   | Description                                                                                         
|:--------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|
| getIncidents()                                          | GET `/api/v1/status/incidents`                                 | Retrieve a collection of `incident` items.                                                          |
| getIncidents(modified_since)                            | GET `/api/v1/status/incidents?modified_since={date-time}`      | Retrieve a collection of `incident` items that have been modified since `modified_since`.           |
| getIncidentsByName(name)                                | GET `/api/v1/status/incidents?name={string}`                   | Retrieve a collection of `incident` items with the specified `name`.                                |
| getIncidentsByStatus(status[])                          | GET `/api/v1/status/incidents?status={StatusType[]}`           | Retrieve a collection of `incident` items with one of the specified `status`.                       |
| getIncidentsByType(type[])                              | GET `/api/v1/status/incidents?type={IncidentType[]}`           | Retrieve a collection of `incident` items with one of the specified `type`.                         |
| getIncidentsByResolution(resolution[])                  | GET `/api/v1/status/incidents?resolution={ResolutionType[]}`   | Retrieve a collection of `incident` items with one of the specified `resolution`.                   |
| getIncidentsConflicting(time)                           | GET `/api/v1/status/incidents?time={date-time}`                | Retrieve a collection of `incident` items where `start <= time <= end`.                             |
| getIncidentsOverlapping(from, to)                       | GET `/api/v1/status/incidents?from={start-date}&to={end-date}` | Retrieve a collection of `incident` items where `from <= end` and `to >= start` time.               |
| getIncidentsByResource(resource_uri[])                  | GET `/api/v1/status/incidents?resource_uris={URI[]}`           | Retrieve a collection of `incident` items that maybe impacting the list of `resource_uris`. |
| getIncident(incident_id)                                | GET `/api/v1/status/incidents/{incident_id}`                   | Retrieve a single `incident` item by `incident_id`.                                                 |
| getEventsByIncident(incident_id)                        | GET `/api/v1/status/incidents/{incident_id}/events`            | Retrieve a collection of `event` items generated by this incident.                                  |
| getResourcesByIncident(incident_id)                     | GET `/api/v1/status/incidents/{incident_id}/resources`         | Retrieve a collection of `resource` items that maybe impacted by this incident.                     |

Application developers can also build more complex and specialized queries that better meet their
workflow needs. For example, combining the getIncidentsByResource(resource_uri[]) and 
getIncidentsOverlapping(from, to) queries to get all `incident` items that could impact a target 
`resource` during their experimental runtime.

GET `/api/v1/status/incidents?resource_uris={URI{}}&from={start-date}&to={end-date}`

Many different query optimizations can be performed to simplify interactions with the IRI API.

### Successful response example(s)

This section provides a list of example `GET` operations and associated responses.

-----

#### Operation: _getIncidents()_
* GET `/api/v1/status/incidents` (paginated)
* Returns: `resource` Collection

This operation returns a collection of `incident` items filtered by query parameters.  In this specific example
paging query parameters are used to get the first two `incident`.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?limit=2"

GET /api/v1/status/incidents?limit=2 HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```

Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Sun, 19 Oct 2025 21:04:01 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sun, 19 Oct 2025 22:10:10 GMT
Server: DOE IRI Demo Server
```
```json
[
  {
    "id": "05dcf051-8e9f-4806-8af0-125782ec2799",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/05dcf051-8e9f-4806-8af0-125782ec2799",
    "name": "unplanned outage on group websites",
    "description": "Auto-generated incident of type unplanned",
    "last_modified": "2025-06-29T02:34:25.000Z",
    "status": "down",
    "type": "unplanned",
    "start": "2025-06-28T18:34:25.272Z",
    "end": "2025-06-29T02:34:25.278Z",
    "resolution": "completed",
    "resource_uris": [
      "https://iri.example.com/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
      "https://iri.example.com/api/v1/status/resources/b951a092-7f0a-4263-bc9a-700c7ceed415",
      "https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc",
      "https://iri.example.com/api/v1/status/resources/d3c52e3c-dd2a-47a4-91e7-f06e00cf486d"
    ],
    "event_uris": [
      "https://iri.example.com/api/v1/status/events/ae6176f5-5cea-4e3c-8e0f-b5fa1f4d77bd",
      "https://iri.example.com/api/v1/status/events/93376f06-3754-4084-b083-8199ae2eb9e7",
      "https://iri.example.com/api/v1/status/events/9a4cbda5-f3cb-4251-af08-3308e72ee840",
      "https://iri.example.com/api/v1/status/events/f662e367-e038-4a8b-8522-3bbd3a08eb6d",
      "https://iri.example.com/api/v1/status/events/7fd99a90-2f22-4412-9285-036f0d366d7b",
      "https://iri.example.com/api/v1/status/events/489508ab-bbc7-4ed7-93f5-42fc9e66d083",
      "https://iri.example.com/api/v1/status/events/ae61f377-7f3f-4bcc-9060-9be15341131b",
      "https://iri.example.com/api/v1/status/events/d686e8df-9bea-4677-b885-816ed4b0f6a7"
    ]
  },
  {
    "id": "0c7d7cf6-9c5b-4c94-8caf-a4ada9f0597d",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/0c7d7cf6-9c5b-4c94-8caf-a4ada9f0597d",
    "name": "unplanned outage on group services",
    "description": "Auto-generated incident of type unplanned",
    "last_modified": "2025-07-24T02:31:08.000Z",
    "status": "down",
    "type": "unplanned",
    "start": "2025-06-29T15:04:25.272Z",
    "end": "2025-06-30T00:04:25.272Z",
    "resolution": "completed",
    "resource_uris": [
      "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
      "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
      "https://iri.example.com/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6",
      "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e",
      "https://iri.example.com/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc"
    ],
    "event_uris": [
      "https://iri.example.com/api/v1/status/events/2db874b1-f6af-4c0e-916d-835b42b67fc6",
      "https://iri.example.com/api/v1/status/events/024176f3-07d5-4209-ac86-ed6d69764fbd",
      "https://iri.example.com/api/v1/status/events/bdb546fe-d37e-4d17-b289-504c91435729",
      "https://iri.example.com/api/v1/status/events/e1ff4cd0-2bff-4e0e-b481-5061e8203bb7",
      "https://iri.example.com/api/v1/status/events/ac0b3980-0d2b-4475-b4cd-b4a998f1156c",
      "https://iri.example.com/api/v1/status/events/805ee514-2bb8-4f68-92c8-1c8103ddf43f",
      "https://iri.example.com/api/v1/status/events/e84ece59-2c1e-4410-9df0-1632490aa569",
      "https://iri.example.com/api/v1/status/events/a8b1c94d-93ad-408f-a3ae-e92a3c6612df",
      "https://iri.example.com/api/v1/status/events/6493546d-6136-4e16-96a4-48885365bb0e",
      "https://iri.example.com/api/v1/status/events/c1f9185a-a0b4-4224-ac26-ebdafe988ba0"
    ]
  }
]
```
-----

#### Operation: _getIncidents(modified_since)_
* GET `/api/v1/status/incidents?modified_since={date-time}` (paginated)
* Returns: `incident` Collection

Using `modified_since` on a `GET` makes the request conditional similar to the standard `If-Modified-Since`
header: the server only sends the full representation if it has changed since the supplied date; otherwise
it replies 304 Not Modified with no message body. The only difference is that `modified_since` specifies
the date format as ISO 8601 standard date time.  Each `event` contains a property named `last_modified`
that is also in ISO 8601 standard date time format and mimics the standard `Last-Modified` header
functionality for that `incident`. ([RFC Editor][6])

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?modified_since=2025-10-19T20:04:01.000Z"

GET /api/v1/status/incidents?modified_since=2025-10-19T20:04:01.000Z HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```

Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Sun, 19 Oct 2025 22:04:01 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sun, 19 Oct 2025 22:45:15 GMT
Server: DOE IRI Demo Server
```
```json
[
  {
        "id": "42252068-be61-4941-bc77-3482ea840429",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/42252068-be61-4941-bc77-3482ea840429",
        "name": "unplanned outage on resourceType storage",
        "description": "Auto-generated incident of type unplanned",
        "last_modified": "2025-10-19T21:03:31.000Z",
        "status": "down",
        "type": "unplanned",
        "start": "2025-10-19T21:03:31.307Z",
        "end": "2025-10-20T01:03:31.307Z",
        "resolution": "unresolved",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/303a692d-c52b-47f0-8699-045f962650e2",
            "https://iri.example.com/api/v1/status/resources/be85a1f4-292e-44d7-804d-68a7ca3e0a1e",
            "https://iri.example.com/api/v1/status/resources/29ea05ad-86de-4df8-b208-f0691aafbaa2",
            "https://iri.example.com/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6",
            "https://iri.example.com/api/v1/status/resources/b06f8043-f96b-4279-8f0a-0e128a73cc32",
            "https://iri.example.com/api/v1/status/resources/ff415c87-6596-41c7-93fd-b772994a92d4",
            "https://iri.example.com/api/v1/status/resources/43b698c6-ed4a-4c1c-90b6-f8829daa9e96",
            "https://iri.example.com/api/v1/status/resources/097c3750-4ba1-4b51-accf-b160be683d55"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/30f11532-8d7f-4db5-af23-9a4a39b37955",
            "https://iri.example.com/api/v1/status/events/bef59800-7745-4c39-9149-164b732a629b",
            "https://iri.example.com/api/v1/status/events/effa9c9c-9394-4357-9962-8e4b333033ef",
            "https://iri.example.com/api/v1/status/events/927e2a0d-a2cf-43e5-bae8-919d8e855962",
            "https://iri.example.com/api/v1/status/events/41f51b81-c401-456c-9401-1d7294bc56db",
            "https://iri.example.com/api/v1/status/events/46f175ed-336d-4a94-b853-ec8ac34e89f9",
            "https://iri.example.com/api/v1/status/events/adbc158b-584e-4ac3-aa41-df5e02e98e7c",
            "https://iri.example.com/api/v1/status/events/ead769f5-7bcd-4011-b5a6-878800149370"
        ]
    },
    {
        "id": "4c03e9c9-a338-47ba-ae89-a2ba90ed83f6",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/4c03e9c9-a338-47ba-ae89-a2ba90ed83f6",
        "name": "planned outage on group websites",
        "description": "Auto-generated incident of type planned",
        "last_modified": "2025-10-19T21:04:01.000Z",
        "status": "down",
        "type": "planned",
        "start": "2025-07-24T11:31:08.519Z",
        "end": "2025-07-24T17:31:08.519Z",
        "resolution": "completed",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
            "https://iri.example.com/api/v1/status/resources/b951a092-7f0a-4263-bc9a-700c7ceed415",
            "https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc",
            "https://iri.example.com/api/v1/status/resources/d3c52e3c-dd2a-47a4-91e7-f06e00cf486d"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/21e9c6cb-a845-4fb5-afd4-d272dd30702a",
            "https://iri.example.com/api/v1/status/events/25ff85ca-66df-439e-9ad7-9a72dcf6c9ba",
            "https://iri.example.com/api/v1/status/events/b54b638c-2107-43b8-8656-b80a4e6dfd44",
            "https://iri.example.com/api/v1/status/events/2731b8ff-5c10-4341-9a1a-034a836604b4",
            "https://iri.example.com/api/v1/status/events/2772dbf7-a2d9-4836-9605-a054a0ee26b2",
            "https://iri.example.com/api/v1/status/events/e954224c-db32-43e5-88ad-a30afbb1eb18",
            "https://iri.example.com/api/v1/status/events/571128b4-20e1-47e2-a779-d2c62b513b8a",
            "https://iri.example.com/api/v1/status/events/5e69ab21-f07f-4242-a5ba-a738bc39c578"
        ]
    }
]
```

There were two `incident` items modified since the specified `2025-10-19T20:04:01.000Z` timestamp, 
and so a response body was returned with a **200** status code per RFC 9110. ([RFC Editor][6])

#### Operation: _getIncidentsByName(name)_
* GET `/api/v1/status/incidents?name={string}` (paginated)
* Returns: `incident` Collection

This operation returns the all `incident` items with a matching `name` string if it exists.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?name=System%20startup"

GET /api/v1/status/incidents?name=System%20startup HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```

Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Sun, 19 Oct 2025 22:04:01 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sun, 19 Oct 2025 22:53:36 GMT
Server: DOE IRI Demo Server
```
```json
[
    {
        "id": "837d19d2-459c-4c06-96dc-ca1bd1e22344",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/837d19d2-459c-4c06-96dc-ca1bd1e22344",
        "name": "System startup",
        "description": "The system has been started.",
        "last_modified": "2025-10-19T21:03:31.000Z",
        "status": "up",
        "type": "unplanned",
        "start": "2025-10-19T21:03:31.054Z",
        "end": "2025-10-19T21:03:31.054Z",
        "resolution": "completed",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
            "https://iri.example.com/api/v1/status/resources/f8a06086-b79b-4f45-beec-abb8bee38fa1",
            "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
            "https://iri.example.com/api/v1/status/resources/303a692d-c52b-47f0-8699-045f962650e2",
            "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
            "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
            "https://iri.example.com/api/v1/status/resources/be85a1f4-292e-44d7-804d-68a7ca3e0a1e",
            "https://iri.example.com/api/v1/status/resources/29ea05ad-86de-4df8-b208-f0691aafbaa2",
            "https://iri.example.com/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6",
            "https://iri.example.com/api/v1/status/resources/b1ce8cd1-e8b8-4f77-b2ab-152084c70281",
            "https://iri.example.com/api/v1/status/resources/b06f8043-f96b-4279-8f0a-0e128a73cc32",
            "https://iri.example.com/api/v1/status/resources/8b61b346-b53c-4a8e-83b4-776eaa14cc67",
            "https://iri.example.com/api/v1/status/resources/b951a092-7f0a-4263-bc9a-700c7ceed415",
            "https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc",
            "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e",
            "https://iri.example.com/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc",
            "https://iri.example.com/api/v1/status/resources/ff415c87-6596-41c7-93fd-b772994a92d4",
            "https://iri.example.com/api/v1/status/resources/43b698c6-ed4a-4c1c-90b6-f8829daa9e96",
            "https://iri.example.com/api/v1/status/resources/d3c52e3c-dd2a-47a4-91e7-f06e00cf486d",
            "https://iri.example.com/api/v1/status/resources/097c3750-4ba1-4b51-accf-b160be683d55"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/354f984e-3933-40ff-8268-590513100635",
            "https://iri.example.com/api/v1/status/events/157642f5-1286-415a-8e5a-674f6e0c7a19",
            "https://iri.example.com/api/v1/status/events/9e09b1ce-7fc8-4a95-b617-f67667999fc6",
            "https://iri.example.com/api/v1/status/events/6218dccf-4699-4f1e-9f40-2c04ea2d95de",
            "https://iri.example.com/api/v1/status/events/d0a56869-779a-4024-bcd0-cd4197fcc98c",
            "https://iri.example.com/api/v1/status/events/471a9b4b-b514-496d-8eed-06a3e9853765",
            "https://iri.example.com/api/v1/status/events/42082b6f-2892-4ed8-8c82-e4dc2d4b1991",
            "https://iri.example.com/api/v1/status/events/efd37a5d-2132-4589-8626-4f6fe0f494cc",
            "https://iri.example.com/api/v1/status/events/c90626df-fb35-486f-ad93-60c30d82baab",
            "https://iri.example.com/api/v1/status/events/34ac8628-bdc1-4536-b1bb-fab2ec5e7f61",
            "https://iri.example.com/api/v1/status/events/48b08313-d932-439d-9aa8-0d0e9e9d8f18",
            "https://iri.example.com/api/v1/status/events/52673dcd-eb3b-4039-bb45-6c94fc8f6ee7",
            "https://iri.example.com/api/v1/status/events/655f065b-544b-4f32-a406-665ef52bd10a",
            "https://iri.example.com/api/v1/status/events/38d080a0-5e0f-4713-b8f1-c4546004376d",
            "https://iri.example.com/api/v1/status/events/fb481a12-e821-40c7-a208-4a3c813ed4b4",
            "https://iri.example.com/api/v1/status/events/59cdfe3e-5046-47ad-87eb-13cdbe9e5675",
            "https://iri.example.com/api/v1/status/events/5821bb4b-e121-44f7-a880-63205d7cc692",
            "https://iri.example.com/api/v1/status/events/cddff518-1206-44b9-a8a7-c8bd3e40d8c7",
            "https://iri.example.com/api/v1/status/events/d9ee3755-f18b-470b-b798-9971c7611bb5",
            "https://iri.example.com/api/v1/status/events/f3286af4-a01c-47ba-abf9-23861d7b3763"
        ]
    }
]
```

-----

#### Operation: _getIncidentsByStatus(status[])_
* GET `/api/v1/status/incidents?status={StatusType[]}` (paginated)
* Returns: `incident` Collection

This operation returns all `incident` items with a matching `status` string if it exists.  The parameter 
accepts a list of StatusType ENUM to allow for matching on multiple values.  For example, if you would 
like to find all `incident` items that degrade the system or worst, we would want to use the following 
query string: `?status=degraded,down,unknown`

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?status=degraded,down,unknown"

GET /api/v1/status/incidents?status=degraded,down,unknown HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```

Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Sun, 19 Oct 2025 22:04:01 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sun, 19 Oct 2025 23:16:45 GMT
Server: DOE IRI Demo Server
```
```json
[
    {
        "id": "05dcf051-8e9f-4806-8af0-125782ec2799",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/05dcf051-8e9f-4806-8af0-125782ec2799",
        "name": "unplanned outage on group websites",
        "description": "Auto-generated incident of type unplanned",
        "last_modified": "2025-06-29T02:34:25.000Z",
        "status": "down",
        "type": "unplanned",
        "start": "2025-06-28T18:34:25.272Z",
        "end": "2025-06-29T02:34:25.278Z",
        "resolution": "completed",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
            "https://iri.example.com/api/v1/status/resources/b951a092-7f0a-4263-bc9a-700c7ceed415",
            "https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc",
            "https://iri.example.com/api/v1/status/resources/d3c52e3c-dd2a-47a4-91e7-f06e00cf486d"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/ae6176f5-5cea-4e3c-8e0f-b5fa1f4d77bd",
            "https://iri.example.com/api/v1/status/events/93376f06-3754-4084-b083-8199ae2eb9e7",
            "https://iri.example.com/api/v1/status/events/9a4cbda5-f3cb-4251-af08-3308e72ee840",
            "https://iri.example.com/api/v1/status/events/f662e367-e038-4a8b-8522-3bbd3a08eb6d",
            "https://iri.example.com/api/v1/status/events/7fd99a90-2f22-4412-9285-036f0d366d7b",
            "https://iri.example.com/api/v1/status/events/489508ab-bbc7-4ed7-93f5-42fc9e66d083",
            "https://iri.example.com/api/v1/status/events/ae61f377-7f3f-4bcc-9060-9be15341131b",
            "https://iri.example.com/api/v1/status/events/d686e8df-9bea-4677-b885-816ed4b0f6a7"
        ]
    },
    {
        "id": "0c7d7cf6-9c5b-4c94-8caf-a4ada9f0597d",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/0c7d7cf6-9c5b-4c94-8caf-a4ada9f0597d",
        "name": "unplanned outage on group services",
        "description": "Auto-generated incident of type unplanned",
        "last_modified": "2025-07-24T02:31:08.000Z",
        "status": "down",
        "type": "unplanned",
        "start": "2025-06-29T15:04:25.272Z",
        "end": "2025-06-30T00:04:25.272Z",
        "resolution": "completed",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
            "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
            "https://iri.example.com/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6",
            "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e",
            "https://iri.example.com/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/2db874b1-f6af-4c0e-916d-835b42b67fc6",
            "https://iri.example.com/api/v1/status/events/024176f3-07d5-4209-ac86-ed6d69764fbd",
            "https://iri.example.com/api/v1/status/events/bdb546fe-d37e-4d17-b289-504c91435729",
            "https://iri.example.com/api/v1/status/events/e1ff4cd0-2bff-4e0e-b481-5061e8203bb7",
            "https://iri.example.com/api/v1/status/events/ac0b3980-0d2b-4475-b4cd-b4a998f1156c",
            "https://iri.example.com/api/v1/status/events/805ee514-2bb8-4f68-92c8-1c8103ddf43f",
            "https://iri.example.com/api/v1/status/events/e84ece59-2c1e-4410-9df0-1632490aa569",
            "https://iri.example.com/api/v1/status/events/a8b1c94d-93ad-408f-a3ae-e92a3c6612df",
            "https://iri.example.com/api/v1/status/events/6493546d-6136-4e16-96a4-48885365bb0e",
            "https://iri.example.com/api/v1/status/events/c1f9185a-a0b4-4224-ac26-ebdafe988ba0"
        ]
    },
    {"more":  "...."}
]
```
-----

#### Operation: _getIncidentsByType(type[])_
* GET `/api/v1/status/incidents?type={IncidentType[]}` (paginated)
* Returns: `incident` Collection

This operation returns all `incident` items with a matching `type` string if it exists.  The parameter
accepts a list of IncidentType ENUM to allow for matching on multiple values.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?type=planned"

GET /api/v1/status/incidents?type=planned HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```

Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Sun, 19 Oct 2025 22:04:01 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Mon, 20 Oct 2025 00:14:37 GMT
Server: DOE IRI Demo Server
```
```json
[
    {
        "id": "1340b8c6-66b3-495c-a0a3-e90cff0d0b9d",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/1340b8c6-66b3-495c-a0a3-e90cff0d0b9d",
        "name": "planned outage on group storage",
        "description": "Auto-generated incident of type planned",
        "last_modified": "2025-06-28T21:04:25.000Z",
        "status": "down",
        "type": "planned",
        "start": "2025-06-28T16:04:25.273Z",
        "end": "2025-06-28T21:04:25.273Z",
        "resolution": "completed",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/303a692d-c52b-47f0-8699-045f962650e2",
            "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
            "https://iri.example.com/api/v1/status/resources/be85a1f4-292e-44d7-804d-68a7ca3e0a1e",
            "https://iri.example.com/api/v1/status/resources/b06f8043-f96b-4279-8f0a-0e128a73cc32",
            "https://iri.example.com/api/v1/status/resources/ff415c87-6596-41c7-93fd-b772994a92d4",
            "https://iri.example.com/api/v1/status/resources/43b698c6-ed4a-4c1c-90b6-f8829daa9e96",
            "https://iri.example.com/api/v1/status/resources/097c3750-4ba1-4b51-accf-b160be683d55"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/907014d0-a9ad-443a-a691-584fb7c76d9a",
            "https://iri.example.com/api/v1/status/events/728e65cd-13fd-4c0b-a687-2477d5c7a1a1",
            "https://iri.example.com/api/v1/status/events/83c0b0de-d3f3-4a7f-953f-221a2c038ff3",
            "https://iri.example.com/api/v1/status/events/a02ea1f6-2841-48d7-b505-2ad871536f00",
            "https://iri.example.com/api/v1/status/events/7dd9cd97-ea20-4824-8b01-c6cbae6b6470",
            "https://iri.example.com/api/v1/status/events/8eb443c1-130f-4fe7-a591-3a18e8c84818",
            "https://iri.example.com/api/v1/status/events/d7da77e0-df98-4268-8d2f-4050ecdaf420",
            "https://iri.example.com/api/v1/status/events/a288a80f-0813-44e8-926d-71a54c8ccc2b",
            "https://iri.example.com/api/v1/status/events/329a6bed-08f1-40bd-a24b-7f05dc62dd59",
            "https://iri.example.com/api/v1/status/events/7ece3a71-ff91-4ad7-b0d5-5efa9e5f56a2",
            "https://iri.example.com/api/v1/status/events/3d13702b-101b-4f4d-b6e8-b741b1a5d4cb",
            "https://iri.example.com/api/v1/status/events/e90b7948-5f18-436f-bdd9-ffd973a73d67",
            "https://iri.example.com/api/v1/status/events/69108809-595c-4078-973d-e78260b2b229",
            "https://iri.example.com/api/v1/status/events/1fbd3925-6802-478e-8c49-0bcbb37a6f21"
        ]
    },
    {
        "id": "21b6351d-3d99-43d4-860b-afdfac87f38b",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/21b6351d-3d99-43d4-860b-afdfac87f38b",
        "name": "planned outage on group storage",
        "description": "Auto-generated incident of type planned",
        "last_modified": "2025-07-24T02:31:13.000Z",
        "status": "down",
        "type": "planned",
        "start": "2025-06-30T04:34:25.273Z",
        "end": "2025-06-30T10:34:25.273Z",
        "resolution": "completed",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/303a692d-c52b-47f0-8699-045f962650e2",
            "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
            "https://iri.example.com/api/v1/status/resources/be85a1f4-292e-44d7-804d-68a7ca3e0a1e",
            "https://iri.example.com/api/v1/status/resources/b06f8043-f96b-4279-8f0a-0e128a73cc32",
            "https://iri.example.com/api/v1/status/resources/ff415c87-6596-41c7-93fd-b772994a92d4",
            "https://iri.example.com/api/v1/status/resources/43b698c6-ed4a-4c1c-90b6-f8829daa9e96",
            "https://iri.example.com/api/v1/status/resources/097c3750-4ba1-4b51-accf-b160be683d55"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/8584eae9-317e-4b0f-8052-f6f4fadef0ef",
            "https://iri.example.com/api/v1/status/events/60691eaa-bde0-4044-b21d-8179d73e0968",
            "https://iri.example.com/api/v1/status/events/ab5a8dcb-9d7b-451a-9d02-ef771acb8cec",
            "https://iri.example.com/api/v1/status/events/b58d29f1-e677-40be-9e48-778790bd833a",
            "https://iri.example.com/api/v1/status/events/a4458313-e940-4de6-9141-043945355c20",
            "https://iri.example.com/api/v1/status/events/dec4a0d6-5483-4ee9-b434-bade87468b7b",
            "https://iri.example.com/api/v1/status/events/a184a7f8-b1f6-4c3e-8c52-ef78b9a6277b",
            "https://iri.example.com/api/v1/status/events/0108be78-8771-4507-abfd-5823f265708d",
            "https://iri.example.com/api/v1/status/events/7449fa2f-a039-4cf5-9ea3-5c0319defe5c",
            "https://iri.example.com/api/v1/status/events/0f698072-8b77-4f9e-a963-38997def00e7",
            "https://iri.example.com/api/v1/status/events/fd83882f-757d-4647-b117-da2a988d0c11",
            "https://iri.example.com/api/v1/status/events/6062adad-4f0e-4d8b-bb92-790b07f29a8a",
            "https://iri.example.com/api/v1/status/events/3dbb25d7-3739-4cf6-85ba-4a34b8656285",
            "https://iri.example.com/api/v1/status/events/c606595d-f4f5-4bbe-9600-4aab0eebd931"
        ]
    }
]
```

-----

#### Operation: _getIncidentsByResolution(resolution[])_
* GET `/api/v1/status/incidents?resolution={ResolutionType[]}` (paginated)
* Returns: `incident` Collection

This operation returns all `incident` items with a matching `resolution` string if it exists.  The parameter
accepts a list of ResolutionType ENUM (`unresolved`, `cancelled`, `completed`, `extended`, `pending`) to 
allow for matching on multiple values.  In this example we look for all `unresolved` incidents.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?resolution=unresolved"

GET /api/v1/status/incidents?resolution=unresolved HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```
Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Mon, 20 Oct 2025 16:02:59 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Mon, 20 Oct 2025 16:10:51 GMT
Server: DOE IRI Demo Server
```
```json
[
  {
    "id": "b4532892-7516-473e-b914-1c42a32960a5",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/b4532892-7516-473e-b914-1c42a32960a5",
    "name": "unplanned outage on resourceType service",
    "description": "Auto-generated incident of type unplanned",
    "last_modified": "2025-10-20T15:31:59.000Z",
    "status": "down",
    "type": "unplanned",
    "start": "2025-10-20T15:31:59.249Z",
    "end": "2025-10-20T22:31:59.249Z",
    "resolution": "unresolved",
    "resource_uris": [
      "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
      "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
      "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e"
    ],
    "event_uris": [
      "https://iri.example.com/api/v1/status/events/861ad5d9-545d-4395-bc15-9493bf2cee2c",
      "https://iri.example.com/api/v1/status/events/bb96e071-06e1-4a33-b5be-59ff05af74d5",
      "https://iri.example.com/api/v1/status/events/b1e06782-22b1-42fd-81dd-b2e3cc1acc32"
    ]
  },
  {
    "id": "c64d3450-f909-489e-8e44-8fd0b02e1c23",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/c64d3450-f909-489e-8e44-8fd0b02e1c23",
    "name": "planned outage on resourceType system",
    "description": "Auto-generated incident of type planned",
    "last_modified": "2025-10-20T16:02:59.000Z",
    "status": "down",
    "type": "planned",
    "start": "2025-10-20T16:02:31.156Z",
    "end": "2025-10-20T21:02:31.156Z",
    "resolution": "unresolved"
  }
]          
```
-----

#### Operation: _getIncidentsConflicting(time)_
* GET `/api/v1/status/incidents?time={date-time}` (paginated)
* Returns: `incident` Collection

This operation returns all `incident` items where `start <= time <= endtime`, allowing the user to determine 
which `incident` were active, are active, or will be active, at a specific point in time.  This capability
can be used to troubleshoot issues after the fact if a workflow failed at a specific time.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?time=2025-10-20T16:02:59.000Z"

GET /api/v1/status/incidents?time=2025-10-20T16:02:59.000Z HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```
Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Mon, 20 Oct 2025 16:02:59 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Mon, 20 Oct 2025 16:10:51 GMT
Server: DOE IRI Demo Server
```
```json
[
  {
    "id": "b4532892-7516-473e-b914-1c42a32960a5",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/b4532892-7516-473e-b914-1c42a32960a5",
    "name": "unplanned outage on resourceType service",
    "description": "Auto-generated incident of type unplanned",
    "last_modified": "2025-10-20T15:31:59.000Z",
    "status": "down",
    "type": "unplanned",
    "start": "2025-10-20T15:31:59.249Z",
    "end": "2025-10-20T22:31:59.249Z",
    "resolution": "unresolved",
    "resource_uris": [
      "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
      "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
      "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e"
    ],
    "event_uris": [
      "https://iri.example.com/api/v1/status/events/861ad5d9-545d-4395-bc15-9493bf2cee2c",
      "https://iri.example.com/api/v1/status/events/bb96e071-06e1-4a33-b5be-59ff05af74d5",
      "https://iri.example.com/api/v1/status/events/b1e06782-22b1-42fd-81dd-b2e3cc1acc32"
    ]
  },
  {
    "id": "c64d3450-f909-489e-8e44-8fd0b02e1c23",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/c64d3450-f909-489e-8e44-8fd0b02e1c23",
    "name": "planned outage on resourceType system",
    "description": "Auto-generated incident of type planned",
    "last_modified": "2025-10-20T16:02:59.000Z",
    "status": "down",
    "type": "planned",
    "start": "2025-10-20T16:02:31.156Z",
    "end": "2025-10-20T21:02:31.156Z",
    "resolution": "unresolved"
  }
]       
```

-----
#### Operation: _getIncidentsOverlapping(from, to))_
* GET `/api/v1/status/incidents?time={date-time}` (paginated)
* Returns: `incident` Collection

This operation returns all `incident` items where `from <= end` and `to >= start` , allowing the user to 
determine which `incident` items were or could be impactful during a specific period in time. This could 
be used for both planning and troubleshooting workflow failures.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "https://iri.example.com/api/v1/status/incidents?from=2025-10-20T16:00:00.000Z&to=2025-10-20T18:00:00.000Z"

GET /api/v1/status/incidents?from=2025-10-20T16:00:00.000Z&to=2025-10-20T18:00:00.000Z HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```
Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Mon, 20 Oct 2025 17:39:04 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Mon, 20 Oct 2025 17:58:47 GMT
Server: DOE IRI Demo Server
```
```json
[
    {
        "id": "b4532892-7516-473e-b914-1c42a32960a5",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/b4532892-7516-473e-b914-1c42a32960a5",
        "name": "unplanned outage on resourceType service",
        "description": "Auto-generated incident of type unplanned",
        "last_modified": "2025-10-20T15:31:59.000Z",
        "status": "down",
        "type": "unplanned",
        "start": "2025-10-20T15:31:59.249Z",
        "end": "2025-10-20T22:31:59.249Z",
        "resolution": "unresolved",
        "resource_uris": [
            "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
            "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
            "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e"
        ],
        "event_uris": [
            "https://iri.example.com/api/v1/status/events/861ad5d9-545d-4395-bc15-9493bf2cee2c",
            "https://iri.example.com/api/v1/status/events/bb96e071-06e1-4a33-b5be-59ff05af74d5",
            "https://iri.example.com/api/v1/status/events/b1e06782-22b1-42fd-81dd-b2e3cc1acc32"
        ]
    },
    {
        "id": "fe61cf3f-7703-4e83-a1da-fa466708227e",
        "self_uri": "https://iri.example.com/api/v1/status/incidents/fe61cf3f-7703-4e83-a1da-fa466708227e",
        "name": "unplanned outage on resourceType network",
        "description": "Auto-generated incident of type unplanned",
        "last_modified": "2025-10-20T17:39:04.000Z",
        "status": "down",
        "type": "unplanned",
        "start": "2025-10-20T17:39:04.054Z",
        "end": "2025-10-20T19:39:04.054Z",
        "resolution": "unresolved",
        "resource_uris": ["https://iri.example.com/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc"],
        "event_uris": ["https://iri.example.com/api/v1/status/events/26d35769-c12e-46df-a7d3-df64943d48d8"]
    }
]
```
-----

#### Operation: _getIncidentsByResource(from, to))_
* GET `/api/v1/status/incidents?resource_uris={URI[]}` (paginated)
* Returns: `incident` Collection

This operation returns all `incident` items where the impacted `resource_uris` property contains at least 
one of the resources listed in the `resource_uris` query parameter. This could be used for both planning 
and troubleshooting workflow failures.

Request:

```http
% curl -sS -H "Accept: application/json" -v -i "http//iri.example.com/api/v1/status/incidents?resource_uris=http//iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80"

GET /api/v1/status/incidents?resource_uris= HTTP/1.1
Host: iri.example.com
User-Agent: curl/8.1.2
Accept: application/json
```
Response **200 OK**:

```http
HTTP/1.1 200 
Last-Modified: Mon, 20 Oct 2025 17:39:04 GMT
Content-Location: https://iri.example.com/api/v1/status/incidents
vary: accept-encoding
Content-Type: application/json
Transfer-Encoding: chunked
Date: Mon, 20 Oct 2025 17:58:47 GMT
Server: DOE IRI Demo Server
```
```json
[
  {
    "id": "60821fd9-7c52-46c3-ae9b-ff1a8248a63e",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/60821fd9-7c52-46c3-ae9b-ff1a8248a63e",
    "name": "System startup",
    "description": "The system has been started.",
    "last_modified": "2025-10-20T02:02:31.000Z",
    "status": "up",
    "type": "unplanned",
    "start": "2025-10-20T02:02:31.154Z",
    "end": "2025-10-20T02:02:31.154Z",
    "resolution": "completed",
    "resource_uris": [
      "https://iri.example.com/api/v1/status/resources/29989783-bc70-4cc8-880f-f2176d6cec20",
      "https://iri.example.com/api/v1/status/resources/f8a06086-b79b-4f45-beec-abb8bee38fa1",
      "https://iri.example.com/api/v1/status/resources/72c11ef6-ff6b-409e-adfd-2f3763daac4f",
      "https://iri.example.com/api/v1/status/resources/303a692d-c52b-47f0-8699-045f962650e2",
      "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
      "https://iri.example.com/api/v1/status/resources/0918ad2e-b318-4fd1-ac8f-56a55abf8e8d",
      "https://iri.example.com/api/v1/status/resources/be85a1f4-292e-44d7-804d-68a7ca3e0a1e",
      "https://iri.example.com/api/v1/status/resources/29ea05ad-86de-4df8-b208-f0691aafbaa2",
      "https://iri.example.com/api/v1/status/resources/13f886ac-6cc2-47c0-a5d4-d82daf3cf5c6",
      "https://iri.example.com/api/v1/status/resources/b1ce8cd1-e8b8-4f77-b2ab-152084c70281",
      "https://iri.example.com/api/v1/status/resources/b06f8043-f96b-4279-8f0a-0e128a73cc32",
      "https://iri.example.com/api/v1/status/resources/8b61b346-b53c-4a8e-83b4-776eaa14cc67",
      "https://iri.example.com/api/v1/status/resources/b951a092-7f0a-4263-bc9a-700c7ceed415",
      "https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc",
      "https://iri.example.com/api/v1/status/resources/a0d96526-6fd3-413e-8f9e-ff12d602539e",
      "https://iri.example.com/api/v1/status/resources/3594b493-f811-43b9-9c14-a3dd23542ffc",
      "https://iri.example.com/api/v1/status/resources/ff415c87-6596-41c7-93fd-b772994a92d4",
      "https://iri.example.com/api/v1/status/resources/43b698c6-ed4a-4c1c-90b6-f8829daa9e96",
      "https://iri.example.com/api/v1/status/resources/d3c52e3c-dd2a-47a4-91e7-f06e00cf486d",
      "https://iri.example.com/api/v1/status/resources/097c3750-4ba1-4b51-accf-b160be683d55"
    ],
    "event_uris": [
      "https://iri.example.com/api/v1/status/events/3c6d4fea-72e0-4c33-b637-7c505e72be59",
      "https://iri.example.com/api/v1/status/events/2cb705b1-5940-4595-a67d-3263f4045c60",
      "https://iri.example.com/api/v1/status/events/c205670d-1090-478c-a7d2-0e0db6b91311",
      "https://iri.example.com/api/v1/status/events/0f5dcc20-8b07-4e37-b09f-902fbb2b1842",
      "https://iri.example.com/api/v1/status/events/8d4be0a2-fd2a-4a43-a3c0-191b5137fe3d",
      "https://iri.example.com/api/v1/status/events/16434347-a589-4812-b8d2-da4a3aa0a891",
      "https://iri.example.com/api/v1/status/events/92c90bbe-f6b0-4dbf-af6d-f87b8cb5c5b9",
      "https://iri.example.com/api/v1/status/events/42aa2a66-4b72-4636-8a76-30fc42187b52",
      "https://iri.example.com/api/v1/status/events/f5447eaf-0077-49c0-b75b-92d4c2baed03",
      "https://iri.example.com/api/v1/status/events/35a57162-94a1-4101-9492-561c61464341",
      "https://iri.example.com/api/v1/status/events/1ae5ad86-4514-442e-8245-86d6e6e58766",
      "https://iri.example.com/api/v1/status/events/be2c5511-e602-4c1a-ba27-ca9d072f996b",
      "https://iri.example.com/api/v1/status/events/3c7c3776-5aa7-4d2e-a247-864b44bcdd66",
      "https://iri.example.com/api/v1/status/events/61a4ac3c-5bb6-48ce-9003-6a06790e6af9",
      "https://iri.example.com/api/v1/status/events/74cb6a75-7d84-48e3-92ed-64817964028a",
      "https://iri.example.com/api/v1/status/events/4f94264e-8cba-4a64-868b-b0a5d0cd0666",
      "https://iri.example.com/api/v1/status/events/af2cffce-45e7-45a1-91aa-f432a24bee32",
      "https://iri.example.com/api/v1/status/events/90a3d184-99df-4da4-a2f3-f55d449e7aad",
      "https://iri.example.com/api/v1/status/events/de8fd34d-07ef-4c8a-9375-4ffc632b8b9a",
      "https://iri.example.com/api/v1/status/events/9b49ad29-22ae-4802-ba50-2c291f278d10"
    ]
  },
  {
    "id": "c990a71a-2066-468a-9155-aff5955c5c3f",
    "self_uri": "https://iri.example.com/api/v1/status/incidents/c990a71a-2066-468a-9155-aff5955c5c3f",
    "name": "unplanned outage on resourceType compute",
    "description": "Auto-generated incident of type unplanned",
    "last_modified": "2025-10-20T13:20:27.000Z",
    "status": "down",
    "type": "unplanned",
    "start": "2025-10-20T08:09:13.212Z",
    "end": "2025-10-20T13:09:13.212Z",
    "resolution": "completed",
    "resource_uris": [
      "https://iri.example.com/api/v1/status/resources/f8a06086-b79b-4f45-beec-abb8bee38fa1",
      "https://iri.example.com/api/v1/status/resources/057c3750-4ba1-4b51-accf-b160be683d80",
      "https://iri.example.com/api/v1/status/resources/b1ce8cd1-e8b8-4f77-b2ab-152084c70281",
      "https://iri.example.com/api/v1/status/resources/8b61b346-b53c-4a8e-83b4-776eaa14cc67"
    ],
    "event_uris": [
      "https://iri.example.com/api/v1/status/events/98113566-0766-4061-b8d8-947e7d3b1e5f",
      "https://iri.example.com/api/v1/status/events/fbb0aa14-8090-43dd-ac40-b6381d23f6c9",
      "https://iri.example.com/api/v1/status/events/7a54f754-247a-4582-9902-a1330e5ca78c",
      "https://iri.example.com/api/v1/status/events/1768c252-53b7-40ab-8deb-c364353cb39f",
      "https://iri.example.com/api/v1/status/events/0b7aad17-dd4e-45a6-9b17-525cf2ba8845",
      "https://iri.example.com/api/v1/status/events/3dbae387-ec52-4c04-ac36-6fb088476713",
      "https://iri.example.com/api/v1/status/events/17cb4594-9c07-4fc9-baa7-391d88b44d59",
      "https://iri.example.com/api/v1/status/events/e77f846c-3a4f-44af-963d-8a7509ffc9f7"
    ]
  }
]
```

-----

TODO: Complete adding of examples.

| getIncident(incident_id)               | GET `/api/v1/status/incidents/{incident_id}`                   | Retrieve a single `incident` item by `incident_id`.                                                 |
| getEventsByIncident(incident_id)       | GET `/api/v1/status/incidents/{incident_id}/events`            | Retrieve a collection of `event` items generated by this incident.                                  |
| getResourcesByIncident(incident_id)    | GET `/api/v1/status/incidents/{incident_id}/resources`         | Retrieve a collection of `resource` items that maybe impacted by this incident.                     |

-----

### Error examples (Problem Details, RFC 9457)

All error responses use media type `application/problem+json` and fields per RFC 9457 (`type`, `title`,
`status`, `detail`, `instance`, plus optional extensions). ([RFC Editor][8])

- **400 Bad Request** — invalid parameter:
```http
HTTP/1.1 400 Bad Request
Content-Type: application/problem+json
```
```json
{
  "type": "https://example.com/problems/invalid-parameter",
  "title": "Invalid request parameter",
  "status": 400,
  "detail": "Parameter 'status' must be one of: up, degraded, down, unknown",
  "instance": "https://iri.example.com/api/v1/status/events?status=bogus"
}
```

* **401 unauthorized** (missing or bad token):

```json
{
  "type": "https://example.com/problems/unauthorized",
  "title": "Missing or invalid token",
  "status": 401,
  "detail": "Bearer token is missing, expired, or invalid",
  "instance": "https://iri.example.com/api/v1/status/incidents"
}
```

The server also includes `WWW-Authenticate: Bearer …` per RFC 6750. ([IETF Datatracker][3])

* **403 forbidden** (authenticated but lacks role):

```json
{
  "type": "https://example.com/problems/forbidden",
  "title": "Insufficient permissions",
  "status": 403,
  "detail": "The authenticated principal is not authorized to access this resource",
  "instance": "https://iri.example.com/api/v1/status/incidents"
}
```

Use 403 when authentication succeeded but authorization failed, per HTTP guidance. ([MDN Web Docs][9])

* **404 not found** (unknown `incident_id`):

```json
{
  "type": "https://example.com/problems/not-found",
  "title": "Incident not found",
  "status": 404,
  "detail": "No incident found with id 'deadbeef-0000-0000-0000-000000000000'",
  "instance": "https://iri.example.com/api/v1/status/incidents/deadbeef-0000-0000-0000-000000000000"
}
```

404 indicates the target resource is not present. ([MDN Web Docs][10])

* **409 conflict** (generic example shown for consistency across resources; not expected from `GET`):

```json
{
  "type": "https://example.com/problems/conflict",
  "title": "Conflicting parameters",
  "status": 409,
  "detail": "Only one of 'from' and 'modified_since' may be used for time filtering",
  "instance": "https://iri.example.com/api/v1/status/incidents?from=2025-05-01T00:00:00Z&modified_since=2025-05-02T00:00:00Z"
}
```

Conflict indicates a state conflict (typical for write operations), defined by HTTP semantics. ([MDN Web Docs][11])

* **500 internal server error**:

```json
{
  "type": "about:blank",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred",
  "instance": "https://iri.example.com/api/v1/status/incidents"
}
```

## OpenAPI 3.1 Snippet (YAML)
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
  - url: http://iri.example.com
    description: Generated server url
tags:
  - name: IRI Status API
    description: |-
      The Status API offers users programmatic access to information on the operational status of various resources within a facility, scheduled maintenance/outage events, and a limited historical record of these events. Designed for quick and efficient status checks of current and future (scheduled) operational status, this API allows developers to integrate facility information into applications or workflows, providing a streamlined way to programmatically access data without manual intervention.

      It should be noted that the operational status of a resource is not an indication of a commitment to provide service, only that the resource is in the described operational state.

      The Facility Status API is not intended for reporting or monitoring purposes; it does not support asynchronous logging or alerting capabilities, and should not be used to derive any type of up or downtime metrics. Instead, its primary focus is on delivering simple, on-demand access to facility resource status, and scheduled maintenance events.
paths:
  /api/v1/status/incidents:
    get:
      tags:
        - IRI Status API
        - getIncidents
      summary: Get a list of available incident resources.
      description: Returns a list of incident resources matching the specified query
      operationId: getIncidents
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
        - name: status
          in: query
          description: The status of a resource.
          required: false
          schema:
            type: string
            description: The status of a resource.
            enum:
              - up
              - degraded
              - down
              - unknown
        - name: type
          in: query
          description: The type of incident.
          required: false
          schema:
            type: string
            description: The type of incident.
            enum:
              - planned
              - unplanned
              - reservation
        - name: resolution
          in: query
          description: The type of resolution to the incident.
          required: false
          schema:
            type: string
            description: The current state of the incident resolution.
            enum:
              - unresolved
              - cancelled
              - completed
              - extended
              - pending
        - name: time
          in: query
          description: "Search for incidents overlapping with time, where start <= time\
          \ <= end.  The time query parameter must be in ISO 8601 format with timezone\
          \ offsets."
          required: false
          schema:
            type: string
            format: date-time
        - name: from
          in: query
          description: Search for incidents/events that are active after (and including)
            the specified from time.  The from query parameter must be in ISO 8601 format
            with timezone offsets.
          required: false
          schema:
            type: string
            format: date-time
        - name: to
          in: query
          description: Search for incidents/events that are active before (and including)
            the specified 'to' time.  The from query parameter must be in ISO 8601 format
            with timezone offsets.
          required: false
          schema:
            type: string
            format: date-time
        - name: resource_uris
          in: query
          description: A list of resources to match.
          required: false
          schema:
            type: array
            items:
              type: string
        - name: event_uris
          in: query
          description: A list of event to match.
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
                  $ref: "#/components/schemas/Incident"
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
  /api/v1/status/incidents/{incident_id}:
    get:
      tags:
        - getIncident
        - IRI Status API
      summary: Get the incident resource associated with the specified id.
      description: Returns the matching incident resource.
      operationId: getIncident
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
        - name: incident_id
          in: path
          description: incident_id
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
                $ref: "#/components/schemas/Incident"
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
  /api/v1/status/incidents/{incident_id}/resources:
    get:
      tags:
        - IRI Status API
        - getResourcesByIncident
      summary: Get the resources associated with the specified incident.
      description: Returns the resources associated with the specified incident.
      operationId: getResourceByIncident
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
        - name: incident_id
          in: path
          description: incident_id
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
          example: https://example.com/notFound
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
          example: https://iri.example.com/api/v1/status/events/f9d6e700-1807-45bd-9a52-e81c32d40c5a
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
          example: https://example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171
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
            example: https://example.com/api/v1/account/capabilities/b1ce8cd1-e8b8-4f77-b2ab-152084c70281
        current_status:
          type: string
          description: The current status of this resource at time of query.
          enum:
            - up
            - degraded
            - down
            - unknown
          example: up
        located_at_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to the Site containing this Resource
            (locatedAt).
          example: https://example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45
        member_of_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to facility managing this Resource
            (memberOf).
          example: https://example.com/api/v1/facility
      required:
        - current_status
        - id
        - last_modified
        - name
        - resource_type
        - self_uri
    Incident:
      type: object
      description: "An Incident represents a discrete occurrence, planned or unplanned,\
        \ that actually or potentially affects the availability, performance, integrity,\
        \ or security of one or more Resources at a given Facility. It serves as a\
        \ high-level grouping construct for aggregating and tracking related Events\
        \ over time and across multiple system components."
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
          example: https://example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171
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
        status:
          type: string
          description: The status of the Resource associated with this Incident.
          enum:
            - up
            - degraded
            - down
            - unknown
          example: down
        type:
          type: string
          description: The type of Incident.
          enum:
            - planned
            - unplanned
            - reservation
          example: planned
        start:
          type: string
          format: date-time
          description: "The date this Incident started, or is predicted to start.\
            \ Format follows the ISO 8601 standard with timezone offsets."
          example: 2023-10-17T11:02:31.690-00:00
        end:
          type: string
          format: date-time
          description: "The date this Incident ended, or is predicted to end.  Format\
            \ follows the ISO 8601 standard with timezone offsets."
          example: 2023-10-19T11:02:31.690-00:00
        resolution:
          type: string
          default: pending
          description: The resolution for this Incident.
          enum:
            - unresolved
            - cancelled
            - completed
            - extended
            - pending
          example: pending
        resource_uris:
          type: array
          items:
            type: string
            format: uri
            description: A hyperlink reference (URI) to the Resources impacted by
              this Incident (mayImpact).
            example: https://example.com/api/v1/status/resources/03bdbf77-6f29-4f66-9809-7f4f77098171
        event_uris:
          type: array
          items:
            type: string
            format: uri
            description: A hyperlink reference (URI) to the Event associated with
              this Incident (hasEvent).
            example: https://example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171
      required:
        - id
        - last_modified
        - name
        - self_uri
        - start
        - type
    Event:
      type: object
      description: "An Event represents a discrete, timestamped occurrence that reflects\
        \ a change in state, condition, or behavior of a Resource, typically within\
        \ the context of an ongoing Incident. Events provide the fine-grained details\
        \ necessary to understand the progression and impact of an Incident, serving\
        \ as both diagnostic data and a lightweight status log of relevant activity."
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
          example: https://example.com/api/v1/status/events/03bdbf77-6f29-4f66-9809-7f4f77098171
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
        status:
          type: string
          description: The status of the resource associated with this event.
          enum:
            - up
            - degraded
            - down
            - unknown
          example: down
        occurred_at:
          type: string
          format: date-time
          description: The date this event occurred.  Format follows the ISO 8601
            standard with timezone offsets.
          example: 2025-03-11T07:28:24.000−00:00
        resource_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to the Resource associated with
            this Event (impacts).
          example: https://example.com/api/v1/status/resources/03bdbf77-6f29-4f66-9809-7f4f77098171
        incident_uri:
          type: string
          format: uri
          description: A hyperlink reference (URI) to the Incident associated with
            this Event (generatedBy).
          example: https://example.com/api/v1/status/incidents/03bdbf77-6f29-4f66-9809-7f4f77098171
      required:
        - id
        - last_modified
        - name
        - self_uri
```

## Notes & Decisions
* **Versioning rationale.** The API is versioned under `/api/v1` to allow additive, backward-compatible evolution following common REST versioning practices while keeping path stability. (OpenAPI 3.1 is used to describe the interface.) ([OpenAPI Initiative Publications][1])
- **Pagination.** Page-based query parameters (`offset`, `limit`) are provided so clients can traverse pages by relation rather than by constructing URLs. Results sorted deterministically (by id) before slicing per controller pattern. ([IETF Datatracker][2])
- **Filtering.** `status` applies to incident’s status; `from`/`to` filter by `started_at`/`resolved_at`; `modified_since` filters by `last_modified`.

## Changelog
- 2025-10-15 — Initial draft for Incidents based on `StatusController.java` and existing docs style.

## Sources (from attached repo)
- `docs/status-resources.md`
- `src/main/java/net/es/iri/api/facility/StatusController.java`
- `src/main/java/net/es/iri/api/facility/schema/Incident.java`
- `src/main/java/net/es/iri/api/facility/schema/NamedObject.java`
- `examples/incidents.json`