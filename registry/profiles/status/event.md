# IRI Status Event Profile

**Profile URI:** `https://iri.science/profiles/status/event`  
**OpenAPI type:** `Event`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Status Event representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/status/event
```

An IRI Event represents a discrete, timestamped occurrence associated with an IRI Resource.

An Event records the state, condition, or behavior of the associated Resource at the time represented by the Event. Events provide fine-grained historical information that can be used to understand changes in Resource state and the progression of an Incident.

An Event is distinct from:

- a Resource, which represents compute, storage, network, service, or other infrastructure;
- an Incident, which groups one or more related Events and may apply to multiple Resources;
- current Resource state, which represents the Resource's operational condition at the time it is queried.

The normative structural definition of an Event representation is provided by the IRI Facility API OpenAPI specification. This profile supplements that schema with application-level semantics and interoperability requirements.

## 2. Profile Semantics

An IRI Event describes an occurrence involving exactly one Resource under the current IRI Facility API data model.

Each Event:

- identifies the Resource associated with the occurrence;
- records when the occurrence occurred;
- records the Resource status represented by the occurrence;
- MAY be associated with an Incident.

An Event represents historical information about a Resource at a specific time.

The status recorded by an Event MUST NOT be interpreted as necessarily representing the current status of the associated Resource.

Events associated with an Incident provide fine-grained information about the progression or effects of that Incident.

Clients SHOULD use advertised hypermedia relationships to discover the Resource and Incident associated with an Event rather than constructing API paths from Event, Resource, or Incident identifiers.

## 3. Structural Contract

The structural definition of the Event representation is defined by the IRI Facility API OpenAPI `Event` schema.

The current Event schema defines the following properties:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Event. |
| `name` | No | Human-readable name or title of the Event. |
| `description` | No | Human-readable description of the Event. |
| `last_modified` | Yes | Time at which the Event representation was last modified. |
| `occurred_at` | Yes | Time at which the represented occurrence happened. |
| `status` | Yes | Status of the associated Resource at the time of the Event. |
| `self_uri` | Yes | Canonical API URI of the Event representation. |
| `resource_uri` | Yes | URI identifying the Resource associated with the Event. |
| `incident_uri` | Yes | URI identifying the Incident associated with the Event, or `null` when the Event is not associated with an Incident. |

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

## 4. Event Identity

The `id` property identifies the Event.

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless a separate IRI specification explicitly defines internal semantics for that identifier.

Clients MUST NOT construct API URLs by combining the Event identifier with assumed path templates.

For example, a client MUST NOT assume that an Event having:

```json
{
  "id": "event-1234"
}
```

can necessarily be retrieved by constructing:

```text
/api/v2/status/events/event-1234
```

The canonical API location of an Event representation MUST instead be determined from an advertised URI or hypermedia link.

## 5. Temporal Semantics

### 5.1 `occurred_at`

`occurred_at` identifies the time at which the represented occurrence happened.

For example:

```json
{
  "occurred_at": "2026-08-17T14:32:18Z"
}
```

The `status` carried by the Event describes the Resource status associated with this occurrence time.

Clients MUST NOT interpret `occurred_at` as the time at which the Event representation was last modified.

### 5.2 `last_modified`

`last_modified` identifies when the Event representation was last modified according to the IRI Facility API contract.

For example:

```json
{
  "last_modified": "2026-08-17T14:32:20Z"
}
```

`occurred_at` and `last_modified` have different semantics:

```text
occurred_at
    ↓
When the represented occurrence happened

last_modified
    ↓
When the Event representation was last modified
```

Clients MUST NOT assume that these timestamps are identical.

## 6. Status Semantics

The `status` property records the status of the associated Resource represented by the Event.

The current IRI Facility API defines:

```text
up
down
degraded
unknown
```

For example:

```json
{
  "status": "degraded",
  "occurred_at": "2026-08-17T14:32:18Z"
}
```

indicates that the Event represents the associated Resource as `degraded` at the time of the occurrence.

The Event status is historical.

It MUST NOT be interpreted as authoritative current Resource status unless the governing IRI API explicitly establishes that the Event remains the current state source.

Clients requiring current Resource status SHOULD retrieve the associated Resource and applicable current-state representation.

## 7. Event-to-Resource Relationship

Every Event identifies exactly one associated Resource under the current OpenAPI contract.

The existing representation exposes this relationship through:

```text
resource_uri
```

The registered IRI hypermedia relation is:

```text
iri:impacts
```

with canonical relation URI:

```text
https://iri.science/rels/impacts
```

Conceptually:

```text
Event  -- iri:impacts -->  Resource
  1             1
```

`iri:impacts` identifies the Resource associated with the Event occurrence.

The relationship is intentionally stronger than the Incident relation:

```text
iri:may-impact
```

An Event records an occurrence associated with a specific Resource, whereas an Incident may identify Resources that are potentially affected.

The existence of `iri:impacts` MUST NOT be interpreted as indicating the Resource's current operational state.

The Event's `status` describes the represented Resource condition at `occurred_at`.

## 8. Event-to-Incident Relationship

An Event MAY be associated with an Incident.

The existing representation exposes this relationship through:

```text
incident_uri
```

The current OpenAPI contract requires the `incident_uri` property to be present but permits its value to be `null`.

The registered IRI hypermedia relation is:

```text
iri:generated-by
```

with canonical relation URI:

```text
https://iri.science/rels/generated-by
```

Conceptually:

```text
Event  -- iri:generated-by -->  Incident
  1               0..1
```

When `incident_uri` contains a URI, `iri:generated-by` identifies the Incident associated with the Event.

When `incident_uri` is `null`, the HAL representation MUST omit the `iri:generated-by` relation.

A producer MUST NOT emit:

```json
{
  "iri:generated-by": {
    "href": null
  }
}
```

The absence of `iri:generated-by` therefore indicates that no Incident target is represented for that Event.

## 9. Hypermedia Representation

When represented using HAL, an Event SHOULD advertise its associated Resource and, when applicable, its associated Incident through `_links`.

For example:

```json
{
  "id": "event-1234",
  "name": "Scratch filesystem degraded",
  "description": "Filesystem entered a degraded state.",
  "last_modified": "2026-08-17T14:32:20Z",
  "occurred_at": "2026-08-17T14:32:18Z",
  "status": "degraded",

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/events/event-1234",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/status/event"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:impacts": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
      "title": "Orion Scratch Filesystem",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/status/resource"
    },

    "iri:generated-by": {
      "href": "https://api.example.org/api/v2/status/incidents/inc-1234",
      "title": "Scheduled filesystem maintenance",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/status/incident"
    }
  }
}
```

In this representation:

- `self` identifies the Event representation itself;
- the `profile` on `self` identifies the IRI Status Event Profile;
- `iri:impacts` identifies the Resource associated with the Event;
- `iri:generated-by` identifies the Incident associated with the Event;
- each `href` identifies the actual target representation;
- `type` identifies the expected media type of the target representation;
- the `profile` on `iri:generated-by` identifies the semantic profile of the target Incident representation.

A Resource link MAY additionally include a `profile` when a registered IRI representation profile exists for the target Resource representation.

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
iri:impacts
```

expands to:

```text
https://iri.science/rels/impacts
```

and:

```text
iri:generated-by
```

expands to:

```text
https://iri.science/rels/generated-by
```

The canonical relation documents define the normative semantics of those relationships.

This Event profile MUST NOT redefine those link-relation semantics.

## 11. Relationship to Existing URI Properties

The current IRI Facility API OpenAPI schema defines:

```text
self_uri
resource_uri
incident_uri
```

These properties expose related-resource URIs directly in the Event representation.

When the IRI HAL hypermedia model is used, the corresponding relationships SHOULD be represented through `_links`:

```text
self_uri
    ↓
_links.self

resource_uri
    ↓
_links["iri:impacts"]

incident_uri
    ↓
_links["iri:generated-by"]
```

For example:

```json
{
  "self_uri": "https://api.example.org/api/v2/status/events/event-1234",

  "resource_uri":
    "https://api.example.org/api/v2/status/resources/orion-scratch",

  "incident_uri":
    "https://api.example.org/api/v2/status/incidents/inc-1234",

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/events/event-1234",
      "profile": "https://iri.science/profiles/status/event"
    },

    "iri:impacts": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
      "profile": "https://iri.science/profiles/status/resource"
    },

    "iri:generated-by": {
      "href": "https://api.example.org/api/v2/status/incidents/inc-1234",
      "profile": "https://iri.science/profiles/status/incident"
    }
  }
}
```

During the compatibility period:

1. Producers retain the required `resource_uri` property.
2. Producers retain the required but nullable `incident_uri` property.
3. Producers MAY additionally expose `_links["iri:impacts"]`.
4. Producers MAY additionally expose `_links["iri:generated-by"]` when `incident_uri` is non-null.
5. Whenever `resource_uri` and `_links["iri:impacts"]` are both present, the link `href` MUST exactly equal `resource_uri`.
6. Whenever non-null `incident_uri` and `_links["iri:generated-by"]` are both present, the link `href` MUST exactly equal `incident_uri`.
7. When `incident_uri` is `null`, `_links["iri:generated-by"]` MUST be omitted.
8. Consumers SHOULD prefer advertised hypermedia relations and MAY fall back to the corresponding URI-valued properties.
9. Removing or changing the existing URI properties requires a separate OpenAPI schema revision.
10. `self_uri` remains authoritative under the current OpenAPI contract until changed by an approved schema revision.

Clients implementing the HAL representation SHOULD use advertised `_links` for navigation rather than constructing URLs from identifiers.

## 12. Media Type

This profile identifies the semantics of the Event representation independently of a particular serialization.

When an Event is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/status/event
```

The profile URI does not replace the media type.

The media type identifies how the representation is encoded; the profile identifies the additional IRI Event semantics applied to that representation.

## 13. Static and Dynamic Semantics

An Event represents a historical occurrence at a specific point in time.

The Event's:

```text
occurred_at
status
resource_uri
```

describe the occurrence and its associated Resource.

The existing IRI Event model characterizes Events as historical records useful for audit and timeline reconstruction.

An Event MUST NOT be interpreted as a continuously updated representation of current Resource state.

For example, an Event:

```json
{
  "occurred_at": "2026-08-17T14:32:18Z",
  "status": "down"
}
```

records a `down` condition at that time.

It does not establish that the Resource remains `down` when the Event is retrieved later.

Clients requiring current Resource status SHOULD retrieve the applicable current Resource or state representation.

An associated Incident MAY continue to evolve after an Event occurs.

The Event's relationship to an Incident does not imply that the Incident's current status or resolution is identical to the Event's recorded status.

## 14. Authorization and Visibility

Authorization MAY affect Event discoverability or the information visible through an Event representation.

A provider MAY omit an Event from a collection or deny access to an Event when the requester is not authorized to discover it.

Where an Event representation is returned, treatment of required properties remains subject to the applicable OpenAPI schema.

The absence of an `iri:generated-by` relationship MUST NOT be interpreted independently as proof that no related Incident exists when authorization or representation filtering may affect visibility, except where the governing API contract guarantees complete visibility.

Where legacy URI properties and corresponding HAL relationships are both returned, they MUST remain consistent with each other.

Clients SHOULD treat the representation as the set of Event information visible to the authenticated requester.

## 15. Conformance

A representation conforms to the IRI Status Event Profile when:

1. it conforms to the applicable IRI Facility API `Event` schema;
2. its properties are interpreted according to the semantics defined by the IRI Facility API and this profile;
3. Event identifiers are treated as identifiers rather than URL templates;
4. `occurred_at` identifies the time of the represented occurrence;
5. `status` represents the Resource status associated with that occurrence and is not assumed to be current Resource state;
6. the associated Resource is discoverable through `resource_uri` or `iri:impacts`;
7. an associated Incident, when represented, is discoverable through non-null `incident_uri` or `iri:generated-by`;
8. `iri:impacts` is used for the Event-to-Resource relationship;
9. `iri:generated-by` is used for the Event-to-Incident relationship;
10. IRI-specific link relations use the canonical IRI relation namespace;
11. profile URIs identify representation semantics and are not used as substitutes for link-relation identifiers;
12. when both `resource_uri` and `_links["iri:impacts"]` are present, they identify the same target;
13. when both non-null `incident_uri` and `_links["iri:generated-by"]` are present, they identify the same target;
14. a null `incident_uri` is represented by omission of `iri:generated-by`, not by a null `href`;
15. clients are not required to infer or construct related-resource URLs.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/status/event
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes that materially alter the interpretation or processing semantics of the Event representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Status Event Profile*
