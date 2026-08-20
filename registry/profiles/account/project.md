# IRI Account Project Profile

**Profile URI:** `https://iri.science/profiles/account/project`  
**OpenAPI type:** `Project`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Account Project representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/project
```

An IRI Project represents a Facility-scoped project and the users associated with that project.

A Project provides the organizational and accounting context within which users may receive access to Facility capabilities through Project Allocations and User Allocations.

A Project is distinct from:

- a Facility, which represents the organization providing the IRI Facility API;
- a Capability, which represents an allocatable or otherwise distinguishable aspect of a Resource;
- a Project Allocation, which represents an allocation granted to a Project for a Capability;
- a User Allocation, which represents a user's allocation within a Project Allocation;
- a Resource, which represents compute, storage, network, service, or other infrastructure.

The normative structural definition of a Project representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with application-level semantics, identity rules, membership conventions, authorization considerations, and interoperability requirements.

## 2. Profile Semantics

An IRI Project represents a project known to a particular Facility.

A Project provides a grouping context for users and allocations.

A Project MAY have:

- one or more participating users;
- one or more Project Allocations;
- allocations associated with different Capabilities;
- User Allocations derived from its Project Allocations.

The existence of a Project MUST NOT itself be interpreted as:

- granting a user access to a Facility Resource;
- granting an allocation;
- proving that an allocation remains available;
- establishing current authorization to consume a Capability;
- indicating that any particular Resource is currently operational.

Those concerns are represented through the appropriate allocation, authorization, Capability, Resource, and operational-state representations.

## 3. Structural Contract

The structural definition of the Project representation is defined by the IRI Facility API OpenAPI `Project` schema.

The current Project schema defines the following properties:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Project within the Facility context. |
| `name` | Yes | Human-readable name of the Project. |
| `description` | Yes | Human-readable description of the Project. |
| `user_ids` | Yes | Identifiers of users participating in the Project. |
| `last_modified` | Yes | Time at which the Project representation was last modified. |
| `self_uri` | Yes | Canonical API URI of the Project representation. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- formats;
- structural validation;
- read-only properties.

This profile is authoritative for additional semantic and interoperability conventions associated with the Project representation.

## 4. Project Identity

The `id` property identifies the Project within the applicable Facility context.

For example:

```json
{
  "id": "proj-abc123"
}
```

The Project identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless another IRI specification explicitly defines additional semantics for that identifier.

A Project identifier is not an API path.

For example, a client discovering:

```json
{
  "id": "proj-abc123"
}
```

MUST NOT infer that the Project can necessarily be retrieved by constructing:

```text
/api/v2/account/projects/proj-abc123
```

The canonical API location of the Project MUST instead be obtained from `self_uri` or the corresponding advertised hypermedia link.

## 5. Project Naming and Description

### 5.1 `name`

`name` provides the human-readable name of the Project.

For example:

```json
{
  "name": "Climate Simulation"
}
```

The name is descriptive and MUST NOT be treated as the stable identity of the Project.

Different Facilities MAY use the same Project name.

### 5.2 `description`

`description` provides a human-readable description of the Project's purpose or activity.

For example:

```json
{
  "description": "Research project studying atmospheric dynamics."
}
```

The description MAY change over the lifetime of the Project without changing Project identity.

## 6. Project Membership

The `user_ids` property identifies users participating in the Project.

For example:

```json
{
  "user_ids": [
    "user-123",
    "user-456"
  ]
}
```

Each value in `user_ids` is a user identifier.

A `user_ids` value MUST NOT be assumed to be:

- an email address;
- a login name;
- a globally unique identifier;
- a dereferenceable URI;
- an authorization credential.

unless another governing IRI specification explicitly defines those semantics.

Membership in `user_ids` indicates that the user is associated with the Project according to the Facility's Project model.

Project membership MUST NOT by itself be interpreted as proof that the user:

- has a particular allocation;
- can consume every Capability associated with the Project;
- can access every Resource associated with the Facility;
- is currently authorized for a particular operation.

Authorization and allocation semantics remain separate.

## 7. Facility Scope

A Project exists within the context of a Facility.

Project identifiers SHOULD therefore be interpreted within the Facility scope unless another IRI specification establishes a broader identifier scope.

For example:

```text
Facility A
    └── Project id: climate

Facility B
    └── Project id: climate
```

does not necessarily identify the same Project.

Clients requiring globally stable Project references SHOULD use the canonical Project URI rather than relying on the Project `id` alone.

The Project representation currently does not contain an explicit Facility URI property.

This profile therefore does not define a Facility relationship that is absent from the current representation contract.

## 8. Project and Allocation Semantics

A Project MAY have one or more Project Allocations.

A Project Allocation represents a portion of a Capability allocation associated with the Project.

Conceptually:

```text
Project
   │
   └── ProjectAllocation
             │
             ├── Capability
             │
             └── AllocationEntry(s)
```

The V2 Account API exposes Project Allocations within the Project context.

However, the current `Project` OpenAPI representation does not contain a `project_allocation_uris` property or another direct link from the Project representation to its Project Allocations.

Accordingly, this profile does **not** define or assign a Project-to-ProjectAllocation HAL relation.

Clients MUST NOT assume that the nested API path structure itself defines a registered hypermedia relationship.

A future IRI specification MAY register an appropriate Project-to-ProjectAllocation relation. If such a relation is defined, the Project representation SHOULD use that registered relation rather than requiring clients to construct Project Allocation paths.

## 9. Hypermedia Representation

When represented using HAL, a Project SHOULD advertise its canonical identity through `_links.self`.

For example:

```json
{
  "id": "proj-abc123",
  "name": "Climate Simulation",
  "description": "Research project studying atmospheric dynamics.",
  "user_ids": [
    "user-123",
    "user-456"
  ],
  "last_modified": "2026-08-18T14:30:00Z",

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/account/projects/proj-abc123",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/account/project"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ]
  }
}
```

In this representation:

- `self` identifies the Project representation;
- `href` identifies the canonical Project API resource;
- `type` identifies the expected representation media type;
- `profile` identifies the IRI Account Project semantic profile.

The profile URI identifies the representation contract.

It does not identify the Project instance.

## 10. Relationship URIs

IRI-specific hypermedia relationships use registered IRI link relations.

For example, when applicable:

```json
{
  "name": "iri",
  "href": "https://iri.science/rels/{rel}",
  "templated": true
}
```

expands an IRI CURIE to its canonical relation URI.

This Project profile does not itself define new link relations.

The semantics, source representation types, target representation types, cardinality, authorization behavior, and stability of an `iri:*` relation MUST be defined by the applicable canonical relation document.

Representation profiles and link-relation identifiers serve different purposes and MUST NOT be treated as interchangeable.

## 11. Relationship to Existing URI Properties

The current Project schema defines:

```text
self_uri
```

as the canonical URI of the Project representation.

When the HAL hypermedia model is used:

```text
self_uri
    ↓
_links.self
```

For example:

```json
{
  "self_uri":
    "https://api.example.org/api/v2/account/projects/proj-abc123",

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/account/projects/proj-abc123",
      "profile": "https://iri.science/profiles/account/project"
    }
  }
}
```

During the compatibility period:

1. Producers retain the required `self_uri` property.
2. Producers MAY additionally expose `_links.self`.
3. Whenever both forms are present, `_links.self.href` MUST exactly equal `self_uri`.
4. Consumers SHOULD prefer the advertised HAL relation and MAY fall back to `self_uri`.
5. Removing or changing `self_uri` requires a separate OpenAPI schema revision.

The current Project schema has no other URI-valued relationship properties requiring HAL migration.

## 12. Media Type

This profile identifies the semantics of the Project representation independently of a particular serialization.

When a Project is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/account/project
```

The media type and profile URI have different roles:

```text
application/hal+json
    ↓
HOW the representation is encoded

https://iri.science/profiles/account/project
    ↓
WHAT semantic representation contract applies
```

The Project instance identifier, representation profile, and media type MUST NOT be treated as interchangeable.

## 13. Static and Dynamic Semantics

A Project representation primarily describes relatively stable organizational and accounting context.

Relatively stable information includes:

```text
id
name
description
user_ids
```

`last_modified` identifies the modification time of the Project representation.

Changes to Project membership or descriptive information SHOULD result in an appropriate update to `last_modified` according to the governing API contract.

The existence of a Project representation MUST NOT be interpreted as evidence that:

- the Project has an active allocation;
- the Project has remaining allocation;
- every listed user is currently authorized;
- a Facility Resource is currently available;
- a Capability can currently be consumed.

Those conditions require the applicable current allocation, authorization, Resource, and Capability information.

## 14. Authorization and Visibility

Project representations are authorization-sensitive.

The V2 Project collection represents Projects available to the currently authenticated user.

A provider MAY therefore expose different Project sets to different requesters according to authorization policy.

Visibility of a Project MUST NOT itself be interpreted as permission to:

- modify the Project;
- consume a Capability;
- submit work;
- access every Project allocation;
- inspect every User Allocation;
- act on behalf of another Project member.

Authorization MAY also affect Project-related representations accessible through other Account API operations.

Clients SHOULD treat the returned Project representation as the information visible within the current authenticated requester context.

The absence of a Project from a requester's visible Project collection MUST NOT necessarily be interpreted as proof that the Project does not exist.

## 15. Conformance

A representation conforms to the IRI Account Project Profile when:

1. it conforms to the applicable IRI Facility API `Project` schema;
2. its properties are interpreted according to the IRI Facility API and this profile;
3. `id` is treated as a Project identifier rather than a URL template;
4. Project identity is interpreted within its applicable Facility scope;
5. `user_ids` identifies Project membership and is not interpreted as authorization or allocation;
6. user identifiers are not assigned semantics beyond those defined by the governing identity specification;
7. Project visibility is not interpreted as a Capability-use or allocation grant;
8. `self_uri` identifies the canonical Project API representation;
9. when both `self_uri` and `_links.self` are present, they identify the same target;
10. profile URIs identify representation semantics and are not used as instance identifiers or link-relation identifiers;
11. clients are not required to infer or construct Project URLs from Project identifiers;
12. no Project-to-ProjectAllocation hypermedia relation is inferred from API path nesting without a registered relation definition.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/project
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, Project identifiers, Project instance URLs, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Adding new Project instances, Project members, allocation types, or registered relationships does not by itself require a new Project profile URI.

Changes that materially alter the interpretation or processing semantics of the common Project representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Account Project Profile*
