# IRI Status Incident Profile

**Profile URI:** `https://iri.science/profiles/status/incident`  
**OpenAPI type:** `Incident`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Status Incident representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/status/incident
```

An IRI Incident represents a discrete occurrence, planned or unplanned, that actually or potentially affects the availability, performance, integrity, security, or usability of one or more IRI Resources.

An Incident provides a higher-level status record that can group related Events over time and across multiple Resources.

An Incident is distinct from:

- a Resource, which represents compute, storage, network, service, or other infrastructure;
- an Event, which represents an occurrence associated with a Resource at a particular point in time;
- dynamic Resource state, which represents the current operational condition of a Resource.

The normative structural definition of an Incident representation is provided by the IRI Facility API OpenAPI specification. This profile supplements that schema with application-level semantics and interoperability requirements.

## 2. Profile Semantics

An IRI Incident represents a condition, activity, maintenance period, outage, reservation, or other occurrence that may affect one or more Resources.

An Incident MAY:

- apply to one Resource or multiple Resources;
- contain zero or more associated Events;
- represent planned or unplanned activity;
- describe an occurrence that has ended or one for which no end time has yet been recorded.

The existence of an Incident does not necessarily mean that every associated Resource is unavailable.

The `status`, temporal properties, associated Events, affected Resources, and resolution information together describe the Incident.

Clients SHOULD use the relationships advertised by the Incident representation to discover associated Events and potentially impacted Resources rather than constructing API paths from Incident or Resource identifiers.

## 3. Structural Contract

The structural definition of the Incident representation is defined by the IRI Facility API OpenAPI `Incident` schema.

The current Incident schema defines the following properties:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Incident. |
| `name` | No | Human-readable name of the Incident. |
| `description` | No | Human-readable description of the Incident. |
| `last_modified` | Yes | Time at which the Incident representation was last modified. |
| `status` | Yes | Current status associated with the Incident. |
| `start` | Yes | Time at which the Incident began or is scheduled to begin. |
| `end` | No | Time at which the Incident ended or is scheduled to end. |
| `type` | Yes | Classification of the Incident. |
| `resolution` | Yes | Current resolution state of the Incident. |
| `self_uri` | Yes | Canonical API URI of the Incident representation. |
| `event_uris` | Yes | URIs identifying Events associated with the Incident. |
| `resource_uris` | Yes | URIs identifying Resources that may be impacted by the Incident. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- nullable properties;
- formats;
- enumerated values;
- structural validation;
- read-only properties.

This profile is authoritative for additional semantic and interoperability conventions associated with those properties and their corresponding hypermedia relationships.

## 4. Incident Identity

The `id` property identifies the Incident.

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless a separate IRI specification explicitly defines internal semantics for that identifier.

Clients MUST NOT construct API URLs by combining the Incident identifier with assumed path templates.

For example, a client MUST NOT assume that an Incident having:

```json
{
  "id": "maintenance-1234"
}
```

can necessarily be retrieved by constructing:

```text
/api/v2/status/incidents/maintenance-1234
```

The canonical API location of an Incident representation MUST instead be determined from an advertised URI or hypermedia link.

## 5. Incident Type

The `type` property classifies the nature of the Incident.

The current IRI Facility API defines the following values:

| Value | Meaning |
|---|---|
| `planned` | The Incident represents planned activity. |
| `unplanned` | The Incident represents unplanned activity. |
| `reservation` | The Incident represents a reservation-related occurrence. |

The Incident type describes the nature of the occurrence and MUST NOT by itself be interpreted as indicating Resource availability or Incident resolution state.

For example:

```json
{
  "type": "planned"
}
```

indicates planned activity but does not establish whether associated Resources are currently available, degraded, or unavailable.

## 6. Status and Resolution

### 6.1 `status`

The `status` property represents the current status associated with the Incident.

The current IRI Facility API defines:

```text
up
down
degraded
unknown
```

The Incident status characterizes the Incident's current operational effect or represented status condition.

The status of an Incident MUST NOT automatically be interpreted as the status of every Resource identified by the Incident.

For example, an Incident affecting multiple Resources MAY represent an overall degraded condition even when individual Resources have different current states.

Clients requiring authoritative current Resource status SHOULD retrieve the affected Resource representations and their applicable state information.

### 6.2 `resolution`

The `resolution` property identifies the current resolution state of the Incident.

The current IRI Facility API defines:

```text
unresolved
cancelled
completed
extended
pending
```

The resolution state describes the disposition or resolution progress of the Incident.

`status` and `resolution` represent different concepts.

For example:

```json
{
  "status": "degraded",
  "resolution": "pending"
}
```

indicates an Incident whose represented operational condition is degraded and whose resolution is pending.

Clients MUST NOT derive one property solely from the value of the other.

## 7. Temporal Semantics

### 7.1 `start`

`start` identifies when the Incident began or is scheduled to begin.

The property is required.

For example:

```json
{
  "start": "2026-08-17T14:00:00Z"
}
```

### 7.2 `end`

`end` identifies when the Incident ended or is scheduled to end.

The property is optional and nullable.

For example:

```json
{
  "end": "2026-08-17T18:00:00Z"
}
```

An absent or `null` `end` value indicates only that an end time is not represented.

Clients MUST NOT infer solely from a missing or `null` `end` value that an Incident is currently active.

Likewise, the presence of an `end` value MUST NOT independently determine the Incident's current `status` or `resolution`.

### 7.3 Incident Lifetime

The combination of:

```text
start
end
status
resolution
type
```

provides temporal and lifecycle information about an Incident.

This profile does not currently define a complete state-transition model between `status`, `resolution`, `start`, and `end`.

Implementations MUST NOT invent additional mandatory lifecycle transitions that are not defined by the applicable IRI specification.

A future revision of this profile MAY define additional lifecycle invariants if adopted by IRI.

## 8. Incident Relationships

An Incident has two principal relationships represented by the current OpenAPI model:

```text
event_uris
resource_uris
```

These relationships have different semantics.

### 8.1 Incident to Event

`event_uris` identifies Events associated with the Incident.

The registered IRI hypermedia relation is:

```text
iri:has-event
```

with canonical relation URI:

```text
https://iri.science/rels/has-event
```

Conceptually:

```text
Incident  -- iri:has-event -->  Event
   1               0..*
```

An Event linked through `iri:has-event` is part of the represented Incident's event history or grouping.

### 8.2 Incident to Resource

`resource_uris` identifies Resources that may be impacted by the Incident.

The registered IRI hypermedia relation is:

```text
iri:may-impact
```

with canonical relation URI:

```text
https://iri.science/rels/may-impact
```

Conceptually:

```text
Incident  -- iri:may-impact -->  Resource
   1                0..*
```

The `may-impact` semantics are intentional.

The existence of the relationship MUST NOT be interpreted as proof that the target Resource:

- is currently unavailable;
- is currently degraded;
- has experienced an outage;
- will necessarily be affected;
- has the same status as the Incident.

Clients requiring authoritative Resource state SHOULD follow the Resource relationship and inspect the applicable Resource and state representations.

## 9. Hypermedia Representation

When represented using HAL, an Incident SHOULD advertise its associated Events and potentially impacted Resources through `_links`.

For example:

```json
{
  "id": "inc-1234",
  "name": "Scheduled filesystem maintenance",
  "description": "Maintenance affecting access to the scratch filesystem.",
  "last_modified": "2026-08-17T15:30:00Z",
  "status": "degraded",
  "type": "planned",
  "start": "2026-08-17T14:00:00Z",
  "end": "2026-08-17T18:00:00Z",
  "resolution": "pending",

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/incidents/inc-1234",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/status/incident"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:has-event": [
      {
        "href": "https://api.example.org/api/v2/status/events/event-101",
        "title": "Maintenance started",
        "type": "application/hal+json",
        "profile": "https://iri.science/profiles/status/event"
      },
      {
        "href": "https://api.example.org/api/v2/status/events/event-102",
        "title": "Filesystem entered degraded state",
        "type": "application/hal+json",
        "profile": "https://iri.science/profiles/status/event"
      }
    ],

    "iri:may-impact": [
      {
        "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
        "title": "Orion Scratch Filesystem",
        "type": "application/hal+json",
        "profile": "https://iri.science/profiles/status/resource"
      }
    ]
  }
}
```

In this representation:

- `self` identifies the Incident representation itself;
- the `profile` on `self` identifies the IRI Status Incident Profile;
- `iri:has-event` identifies Events associated with the Incident;
- `iri:may-impact` identifies Resources that may be impacted by the Incident;
- each `href` identifies an actual target representation;
- `type` identifies the expected media type of the target representation.

A target link MAY additionally include a `profile` when a registered IRI representation profile exists for that target representation.

The relation URI and representation profile URI serve different purposes and MUST NOT be treated as interchangeable identifiers.

## 10. Relationship URIs

IRI-specific relations use the IRI CURIE namespace.

For example:

```json
{
  "name": "iri",
  "href": "https://iri.science/rels/{rel}",
  "templated": true
}
```

The CURIE:

```text
iri:has-event
```

expands to:

```text
https://iri.science/rels/has-event
```

and:

```text
iri:may-impact
```

expands to:

```text
https://iri.science/rels/may-impact
```

The canonical relation documents define the normative semantics of those relationships.

This Incident profile MUST NOT redefine those link-relation semantics.

## 11. Relationship to Existing URI Properties

The current IRI Facility API OpenAPI schema defines:

```text
self_uri
event_uris
resource_uris
```

These properties expose resource URIs directly in the Incident representation.

When the IRI HAL hypermedia model is used, the corresponding relationships SHOULD be represented through `_links`:

```text
self_uri
    ↓
_links.self

event_uris
    ↓
_links["iri:has-event"]

resource_uris
    ↓
_links["iri:may-impact"]
```

For example:

```json
{
  "self_uri": "https://api.example.org/api/v2/status/incidents/inc-1234",

  "event_uris": [
    "https://api.example.org/api/v2/status/events/event-101",
    "https://api.example.org/api/v2/status/events/event-102"
  ],

  "resource_uris": [
    "https://api.example.org/api/v2/status/resources/orion-scratch"
  ],

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/incidents/inc-1234",
      "profile": "https://iri.science/profiles/status/incident"
    },

    "iri:has-event": [
      {
        "href": "https://api.example.org/api/v2/status/events/event-101",
        "profile": "https://iri.science/profiles/status/event"
      },
      {
        "href": "https://api.example.org/api/v2/status/events/event-102",
        "profile": "https://iri.science/profiles/status/event"
      }
    ],

    "iri:may-impact": [
      {
        "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
        "profile": "https://iri.science/profiles/status/resource"
      }
    ]
  }
}
```

During the compatibility period:

1. Producers retain the required `event_uris` and `resource_uris` properties.
2. Producers MAY additionally expose `_links["iri:has-event"]` and `_links["iri:may-impact"]`.
3. Whenever both forms are present, `event_uris` and `_links["iri:has-event"]` MUST identify the same targets, disregarding order.
4. Whenever both forms are present, `resource_uris` and `_links["iri:may-impact"]` MUST identify the same targets, disregarding order.
5. Consumers SHOULD prefer advertised hypermedia relations and MAY fall back to the corresponding URI-valued properties.
6. Removing or changing the existing URI properties requires a separate OpenAPI schema revision.
7. `self_uri` remains authoritative under the current OpenAPI contract until changed by an approved schema revision.

Clients implementing the HAL representation SHOULD use advertised `_links` for navigation rather than constructing URLs from identifiers.

## 12. Media Type

This profile identifies the semantics of the Incident representation independently of a particular serialization.

When an Incident is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/status/incident
```

The profile URI does not replace the media type.

The media type identifies how the representation is encoded; the profile identifies the additional IRI Incident semantics applied to that representation.

## 13. Static and Dynamic Semantics

An Incident is a dynamic status-domain representation whose properties MAY change during its lifetime.

Properties that may change include:

```text
last_modified
status
end
resolution
event_uris
resource_uris
```

Changes to associated Events or potentially impacted Resources MAY cause the Incident representation to change.

Clients SHOULD NOT assume that an Incident representation retrieved previously still represents current Incident state.

The Incident's `last_modified` property provides the representation's modification timestamp according to the IRI Facility API contract.

The existence of an Incident relationship MUST NOT be treated as proof of current Resource availability or unavailability.

Current Resource state SHOULD be obtained from the applicable Resource or state representation.

## 14. Authorization and Visibility

Authorization MAY affect information visible through an Incident representation.

A provider MAY omit:

- Events;
- impacted Resources;
- descriptive information;
- relationships;
- other information

when the requester is not authorized to discover that information, subject to the requirements of the applicable OpenAPI schema.

The absence of an Event or Resource relationship MUST NOT necessarily be interpreted as proof that the relationship does not exist.

Where legacy URI properties and corresponding HAL relationships are both returned, they MUST remain consistent with each other.

Clients SHOULD treat the representation as the set of Incident information visible to the authenticated requester.

## 15. Conformance

A representation conforms to the IRI Status Incident Profile when:

1. it conforms to the applicable IRI Facility API `Incident` schema;
2. its properties are interpreted according to the semantics defined by the IRI Facility API and this profile;
3. Incident identifiers are treated as identifiers rather than URL templates;
4. associated Events are discoverable through `event_uris` or `iri:has-event`;
5. potentially impacted Resources are discoverable through `resource_uris` or `iri:may-impact`;
6. IRI-specific link relations use the canonical IRI relation namespace;
7. profile URIs identify representation semantics and are not used as substitutes for link-relation identifiers;
8. when both `event_uris` and `_links["iri:has-event"]` are present, they identify the same targets;
9. when both `resource_uris` and `_links["iri:may-impact"]` are present, they identify the same targets;
10. clients are not required to infer or construct related-resource URLs.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/status/incident
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes that materially alter the interpretation or processing semantics of the Incident representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Status Incident Profile*
