# IRI Account User Allocation Profile

**Profile URI:** `https://iri.science/profiles/account/user-allocation`  
**OpenAPI type:** `UserAllocation`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Account User Allocation representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/user-allocation
```

An IRI User Allocation represents the allocation assigned to a particular user within a Project Allocation.

A User Allocation identifies:

- the user to whom the allocation applies;
- the Project Allocation of which the User Allocation is a part;
- one or more allocation entries describing quantities allocated to and consumed by the user.

A User Allocation is distinct from:

- a Project, which represents the project context;
- a Project Allocation, which represents an allocation granted to a Project for a Capability;
- a Capability, which represents the allocatable aspect of a Resource;
- a Resource, which represents compute, storage, network, service, or other infrastructure;
- an Allocation Entry, which expresses a quantity, usage value, and allocation unit within the User Allocation.

The normative structural definition of a User Allocation representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with application-level semantics, accounting relationships, user-association semantics, authorization considerations, and interoperability requirements.

## 2. Profile Semantics

An IRI User Allocation represents a user's allocation within exactly one Project Allocation under the current V2 model.

Conceptually:

```text
Project
   │
   ▼
ProjectAllocation
   │
   ├── applies to ───────────► Capability
   │
   ▼
UserAllocation
   │
   └── assigned to ──────────► user_id
```

A Project Allocation describes allocation at the Project level.

A User Allocation describes the portion or accounting assignment associated with one user within that Project Allocation.

The User Allocation does not itself represent:

- the Project;
- the Capability;
- the underlying Resource;
- the user as an independently addressable API resource;
- current Resource availability;
- authorization to invoke an operation;
- a guarantee that unused allocation can currently be consumed.

Those concepts are represented separately.

## 3. Structural Contract

The structural definition of the User Allocation representation is defined by the IRI Facility API OpenAPI `UserAllocation` schema.

The current User Allocation schema defines:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the User Allocation. |
| `user_id` | Yes | Identifier of the user receiving the allocation. |
| `entries` | Yes | Allocation entries describing allocation quantities and usage for the user. |
| `project_allocation_uri` | Yes | URI identifying the Project Allocation of which this User Allocation is a part. |

Each element of `entries` conforms to the OpenAPI `AllocationEntry` schema.

An Allocation Entry contains:

| Property | Required | Semantic purpose |
|---|---:|---|
| `allocation` | Yes | Total allocation amount assigned in this entry. |
| `usage` | Yes | Amount of the allocation consumed. |
| `unit` | Yes | Unit in which `allocation` and `usage` are expressed. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- formats;
- structural validation;
- Allocation Entry structure;
- allocation-unit representation.

This profile is authoritative for additional semantic and interoperability conventions associated with the User Allocation representation.

## 4. User Allocation Identity

The `id` property identifies the User Allocation instance.

For example:

```json
{
  "id": "user-alloc-42"
}
```

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless another IRI specification explicitly defines additional semantics for that identifier.

A User Allocation identifier is not an API path.

For example, a client discovering:

```json
{
  "id": "user-alloc-42"
}
```

MUST NOT infer that the representation is located at:

```text
/api/v2/account/user-allocations/user-alloc-42
```

The actual representation URI MUST be obtained through the governing API contract or an advertised hypermedia link.

## 5. User Association

The `user_id` property identifies the user to whom the User Allocation applies.

For example:

```json
{
  "user_id": "user-123"
}
```

The `user_id` value is an identifier.

Unless another governing IRI identity specification defines additional semantics, clients MUST NOT assume that `user_id` is:

- an email address;
- a Facility login name;
- an OIDC `sub` claim;
- a globally unique identifier;
- a URI;
- a dereferenceable API resource;
- an authorization credential.

The presence of:

```json
{
  "user_id": "user-123"
}
```

means that the User Allocation is associated with the user identified as `user-123` within the applicable Facility identity context.

It does not independently establish how that identifier maps to an external identity system.

### 5.1 No User Hypermedia Relation

The current V2 model does not define an independently addressable `User` representation or a URI-valued user relationship on `UserAllocation`.

Accordingly, this profile does not invent a User link relation such as:

```text
iri:has-user
```

or:

```text
iri:assigned-to
```

A future IRI identity specification MAY introduce a User representation or a registered relationship to one.

Until such a relationship is defined, `user_id` remains the authoritative structural mechanism for identifying the user associated with the User Allocation.

## 6. Project Allocation Relationship

Every User Allocation belongs to exactly one Project Allocation under the current V2 contract.

The existing representation identifies that Project Allocation through:

```text
project_allocation_uri
```

The registered IRI hypermedia relation is:

```text
iri:has-project-allocation
```

with canonical relation URI:

```text
https://iri.science/rels/has-project-allocation
```

Conceptually:

```text
UserAllocation
      │
      │ iri:has-project-allocation
      ▼
ProjectAllocation
```

with semantic cardinality:

```text
UserAllocation  -- iri:has-project-allocation -->  ProjectAllocation
      1                       1
```

The relationship identifies the Project Allocation of which the User Allocation is a part.

It describes a stable accounting hierarchy association.

It does not assert:

- that the Project Allocation has remaining capacity;
- that the Project remains active;
- that the user is currently authorized to consume the allocation;
- that the associated Capability is currently available;
- that the underlying Resource is schedulable or operational.

The target Project Allocation representation SHOULD identify:

```text
https://iri.science/profiles/account/project-allocation
```

as its representation profile when profile information is advertised.

## 7. Allocation Entries

The `entries` property describes allocation and usage quantities assigned to the user within the Project Allocation.

For example:

```json
{
  "entries": [
    {
      "allocation": 10000,
      "usage": 4250,
      "unit": "node_hours"
    }
  ]
}
```

Conceptually:

```text
UserAllocation
      │
      └── entries
             │
             ├── allocation
             ├── usage
             └── unit
```

### 7.1 `allocation`

`allocation` represents the quantity assigned to the user for the applicable Allocation Entry.

For example:

```json
{
  "allocation": 10000
}
```

The value MUST be interpreted together with its corresponding `unit`.

The numeric value by itself does not have complete allocation semantics.

### 7.2 `usage`

`usage` represents the amount of the corresponding user allocation that has been consumed according to Facility accounting data.

For example:

```json
{
  "usage": 4250
}
```

`usage` and `allocation` within an Allocation Entry MUST be interpreted using the same `unit`.

### 7.3 `unit`

`unit` identifies the unit used to express the `allocation` and `usage` values.

For example:

```json
{
  "unit": "node_hours"
}
```

The syntax and permitted values for the allocation unit are defined by the governing IRI Facility API and applicable DOE-IRI controlled-vocabulary specifications.

This profile does not independently redefine the allocation-unit vocabulary.

## 8. Allocation Hierarchy

The User Allocation participates in an accounting hierarchy:

```text
Project
   │
   ▼
ProjectAllocation
   │
   ▼
UserAllocation
```

The Project Allocation establishes the Project-level allocation for a Capability.

The User Allocation represents an allocation or accounting assignment for one user within that Project Allocation.

For example:

```text
Project: Climate Simulation

    ProjectAllocation:
        Capability: GPU compute
        Allocation: 100,000 node-hours

            UserAllocation: user-123
                Allocation: 10,000 node-hours

            UserAllocation: user-456
                Allocation: 20,000 node-hours
```

The accounting hierarchy does not imply that the sum of visible User Allocations MUST equal the corresponding Project Allocation.

A Facility MAY:

- leave some Project allocation unassigned to individual users;
- expose only User Allocations visible to the requester;
- apply Facility-specific accounting policies;
- modify User Allocations independently over time.

Clients MUST NOT infer accounting invariants beyond those explicitly established by the governing IRI specification.

## 9. Allocation Semantics

A User Allocation represents accounting allocation, not physical Resource capacity.

For example:

```json
{
  "entries": [
    {
      "allocation": 10000,
      "usage": 4250,
      "unit": "node_hours"
    }
  ]
}
```

indicates that the user has an allocation entry of 10,000 node-hours and that the Facility reports 4,250 node-hours of usage for that entry.

A client MAY calculate:

```text
allocation - usage
```

for presentation or analysis when applicable accounting semantics permit such a calculation.

However, a positive arithmetic remainder MUST NOT by itself be interpreted as proof that:

- the Capability is currently available;
- a compute system can currently schedule a job;
- the user is currently authorized;
- the allocation remains valid;
- the Project remains active;
- an applicable Resource is operational.

Accounting quantity, authorization, policy, allocation validity, and operational availability are separate concerns.

## 10. Hypermedia Representation

When represented using HAL, a User Allocation SHOULD advertise its Project Allocation relationship through `_links`.

For example:

```json
{
  "id": "user-alloc-42",
  "user_id": "user-123",

  "entries": [
    {
      "allocation": 10000,
      "usage": 4250,
      "unit": "node_hours"
    }
  ],

  "project_allocation_uri":
    "https://api.example.org/api/v2/account/projects/climate-simulation/project_allocations/alloc-001",

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/account/projects/climate-simulation/project_allocations/alloc-001/user_allocations/user-alloc-42",
      "type": "application/hal+json",
      "profile":
        "https://iri.science/profiles/account/user-allocation"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:has-project-allocation": {
      "href":
        "https://api.example.org/api/v2/account/projects/climate-simulation/project_allocations/alloc-001",
      "type": "application/hal+json",
      "profile":
        "https://iri.science/profiles/account/project-allocation"
    }
  }
}
```

In this representation:

- `self` identifies the User Allocation representation;
- `iri:has-project-allocation` identifies the Project Allocation of which the User Allocation is a part;
- `profile` identifies the semantic contract of a target representation;
- the relation name identifies why the target is related.

The relation URI, target URI, representation profile, instance identifier, and user identifier serve different purposes and MUST NOT be treated as interchangeable identifiers.

## 11. Relationship to Existing URI Properties

The current User Allocation schema defines:

```text
project_allocation_uri
```

as a direct URI-valued relationship property.

When the IRI HAL hypermedia model is used:

```text
project_allocation_uri
        ↓
_links["iri:has-project-allocation"]
```

During the compatibility period:

1. Producers retain the required `project_allocation_uri` property.
2. Producers MAY additionally expose `_links["iri:has-project-allocation"]`.
3. Whenever both forms are present, the link `href` MUST exactly equal `project_allocation_uri`.
4. Consumers SHOULD prefer the advertised hypermedia relationship and MAY fall back to `project_allocation_uri`.
5. Removing or changing `project_allocation_uri` requires a separate OpenAPI schema revision.

The current User Allocation schema does not define a `self_uri` property.

A HAL-enabled producer SHOULD nevertheless advertise a canonical `self` link when the User Allocation has an independently addressable representation.

Clients MUST use the advertised `self` link rather than infer the User Allocation URI from:

- `id`;
- `user_id`;
- `project_allocation_uri`;
- Project identifiers;
- API path conventions.

## 12. Media Type

This profile identifies the semantics of the User Allocation representation independently of a particular serialization.

When a User Allocation is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/account/user-allocation
```

The media type and profile URI have different roles:

```text
application/hal+json
    ↓
HOW the representation is encoded


https://iri.science/profiles/account/user-allocation
    ↓
WHAT semantic representation contract applies
```

They MUST NOT be treated as interchangeable.

## 13. Static and Dynamic Semantics

A User Allocation combines relatively stable accounting relationships with dynamic accounting quantities.

Relatively stable information includes:

```text
id
user_id
project_allocation_uri
```

The following value commonly changes as allocation is consumed:

```text
entries[].usage
```

Depending on Facility allocation policy, the following MAY also change:

```text
entries[].allocation
entries
```

The User-to-UserAllocation association and UserAllocation-to-ProjectAllocation association SHOULD normally remain stable for the lifetime of the represented User Allocation.

If either association changes, an implementation SHOULD consider whether that represents modification of the same allocation or creation of a new User Allocation identity according to the governing API contract.

This profile does not independently define a complete User Allocation lifecycle or state-transition model.

## 14. Authorization and Visibility

User Allocation representations are authorization-sensitive.

The V2 Account API exposes User Allocations within the context of an authenticated user's accessible Projects and Project Allocations.

A provider MAY restrict:

- which User Allocations are visible;
- allocation quantities;
- usage quantities;
- Project Allocation discoverability;
- related accounting information

according to Facility authorization policy.

The visibility of a User Allocation MUST NOT itself be interpreted as permission to consume the allocation.

Likewise, the presence of:

```text
iri:has-project-allocation
```

does not establish:

- user authorization;
- Project activity;
- remaining allocation;
- Capability availability;
- Resource availability.

The absence of another user's User Allocation MUST NOT be interpreted as proof that no such allocation exists.

Where `project_allocation_uri` and its corresponding HAL relation are both returned, they MUST remain consistent.

Clients SHOULD treat the representation as the allocation information visible within the current authenticated requester context.

## 15. Conformance

A representation conforms to the IRI Account User Allocation Profile when:

1. it conforms to the applicable IRI Facility API `UserAllocation` schema;
2. its properties are interpreted according to the IRI Facility API and this profile;
3. `id` is treated as a User Allocation identifier rather than a URL template;
4. `user_id` identifies the associated user but is not assigned URI, login, email, or global-identity semantics unless defined elsewhere;
5. no User hypermedia relationship is inferred solely from `user_id`;
6. `entries` are interpreted as accounting quantities rather than Resource availability;
7. each Allocation Entry interprets `allocation` and `usage` using its corresponding `unit`;
8. `project_allocation_uri` identifies exactly one Project Allocation association;
9. `iri:has-project-allocation` is used for the UserAllocation-to-ProjectAllocation relationship when represented through HAL;
10. IRI-specific link relations use the canonical IRI relation namespace;
11. representation profile URIs are not used as substitutes for relation identifiers, user identifiers, or instance identifiers;
12. when both `project_allocation_uri` and `_links["iri:has-project-allocation"]` are present, they identify the same target;
13. clients do not infer User Allocation or Project Allocation URLs from identifiers or path conventions;
14. visibility of a User Allocation is not interpreted as authorization to consume it.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/user-allocation
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, User Allocation identifiers, user identifiers, allocation-unit identifiers, instance URLs, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes to individual:

- User Allocations;
- user assignments;
- allocation amounts;
- usage amounts;
- allocation-unit values;
- Project Allocations

do not themselves require a new User Allocation profile URI.

Changes that materially alter the interpretation or processing semantics of the common User Allocation representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Account User Allocation Profile*