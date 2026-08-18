# IRI Account Project Allocation Profile

**Profile URI:** `https://iri.science/profiles/account/project-allocation`  
**OpenAPI type:** `ProjectAllocation`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Account Project Allocation representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/project-allocation
```

An IRI Project Allocation represents an allocation granted to a Project for a specific Capability.

A Project Allocation identifies:

- the Project receiving the allocation;
- the Capability to which the allocation applies;
- one or more allocation entries describing quantities granted and consumed.

A Project Allocation is distinct from:

- a Project, which represents the project receiving the allocation;
- a Capability, which represents the allocatable aspect of an IRI Resource;
- a User Allocation, which represents a user's allocation within a Project Allocation;
- a Resource, which represents the underlying compute, storage, network, service, or other infrastructure;
- an Allocation Entry, which expresses a quantity, usage value, and allocation unit within the Project Allocation.

The normative structural definition of a Project Allocation representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with application-level semantics, accounting relationships, authorization considerations, and interoperability requirements.

## 2. Profile Semantics

An IRI Project Allocation represents an accounting relationship between exactly one Project and exactly one Capability under the current V2 model.

Conceptually:

```text
                   Project
                      ▲
                      │
                iri:has-project
                      │
                      │
             ProjectAllocation
                      │
                iri:has-capability
                      │
                      ▼
                  Capability
```

The Project Allocation contains one or more allocation entries that describe the quantities granted and consumed using applicable allocation units.

A Project Allocation does not itself represent:

- the underlying Resource;
- current Resource availability;
- authorization to invoke an operation;
- a guarantee that unused allocation can currently be consumed;
- an individual user's share of the Project Allocation.

Those concepts are represented separately.

## 3. Structural Contract

The structural definition of the Project Allocation representation is defined by the IRI Facility API OpenAPI `ProjectAllocation` schema.

The current Project Allocation schema defines:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Project Allocation. |
| `entries` | Yes | Allocation entries describing granted quantities and usage. |
| `project_uri` | Yes | URI identifying the Project to which the allocation belongs. |
| `capability_uri` | Yes | URI identifying the Capability to which the allocation applies. |

Each element of `entries` conforms to the OpenAPI `AllocationEntry` schema.

An Allocation Entry contains:

| Property | Required | Semantic purpose |
|---|---:|---|
| `allocation` | Yes | Total allocation amount granted. |
| `usage` | Yes | Amount of the allocation consumed. |
| `unit` | Yes | Unit in which `allocation` and `usage` are expressed. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- formats;
- structural validation;
- allocation-entry structure;
- allocation-unit representation.

This profile is authoritative for additional semantic and interoperability conventions associated with the Project Allocation representation.

## 4. Project Allocation Identity

The `id` property identifies the Project Allocation.

For example:

```json
{
  "id": "alloc-001"
}
```

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless another IRI specification explicitly defines additional semantics for that identifier.

A Project Allocation identifier is not an API path.

For example, a client discovering:

```json
{
  "id": "alloc-001"
}
```

MUST NOT infer that the representation can necessarily be retrieved using a constructed path such as:

```text
/api/v2/account/project-allocations/alloc-001
```

The actual representation URI MUST be obtained through the governing API contract or an advertised hypermedia link.

## 5. Project Relationship

Every Project Allocation belongs to exactly one Project under the current V2 contract.

The existing representation identifies that Project through:

```text
project_uri
```

The registered IRI hypermedia relation is:

```text
iri:has-project
```

with canonical relation URI:

```text
https://iri.science/rels/has-project
```

Conceptually:

```text
ProjectAllocation  -- iri:has-project -->  Project
       1                    1
```

The relationship identifies the Project to which the Project Allocation belongs.

It describes a stable accounting association.

It does not assert that:

- the Project is currently active;
- the Project has active users;
- the allocation has remaining capacity;
- any particular user is authorized to consume the allocation;
- the associated Resource is currently available.

Those conditions require the appropriate current representations and authorization context.

The target Project representation SHOULD identify the profile:

```text
https://iri.science/profiles/account/project
```

when profile information is advertised.

## 6. Capability Relationship

Every Project Allocation applies to exactly one Capability under the current V2 contract.

The existing representation identifies that Capability through:

```text
capability_uri
```

The registered IRI hypermedia relation is:

```text
iri:has-capability
```

with canonical relation URI:

```text
https://iri.science/rels/has-capability
```

Conceptually:

```text
ProjectAllocation  -- iri:has-capability -->  Capability
       1                      1
```

For a Project Allocation, `iri:has-capability` means that the allocation applies to the target Capability.

This is source-context-specific use of the general `iri:has-capability` relation.

On a Resource:

```text
Resource
    -- iri:has-capability -->
Capability
```

means that the Resource provides the Capability.

On a Project Allocation:

```text
ProjectAllocation
    -- iri:has-capability -->
Capability
```

means that the allocation applies to that Capability.

The relation does not assert:

- current Capability availability;
- remaining allocation;
- enabled state;
- user permission;
- schedulability.

The target Capability representation SHOULD identify the profile:

```text
https://iri.science/profiles/account/capability
```

when profile information is advertised.

## 7. Allocation Entries

The `entries` property describes allocation and usage quantities associated with the Project Allocation.

For example:

```json
{
  "entries": [
    {
      "allocation": 100000,
      "usage": 52342.5,
      "unit": "node_hours"
    }
  ]
}
```

Each Allocation Entry represents quantities within one measurement unit.

Conceptually:

```text
ProjectAllocation
       │
       └── entries
              │
              ├── allocation
              ├── usage
              └── unit
```

### 7.1 `allocation`

`allocation` represents the total quantity granted for that Allocation Entry.

For example:

```json
{
  "allocation": 100000
}
```

The value MUST be interpreted in conjunction with the corresponding `unit`.

The numeric value alone has no complete allocation meaning.

### 7.2 `usage`

`usage` represents the amount of the corresponding allocation that has been consumed according to the Facility's accounting data.

For example:

```json
{
  "usage": 52342.5
}
```

`usage` and `allocation` MUST be interpreted using the same `unit` within an Allocation Entry.

### 7.3 `unit`

`unit` identifies the unit used to express the `allocation` and `usage` values.

For example:

```json
{
  "unit": "node_hours"
}
```

The set and syntax of valid allocation-unit values are defined by the governing IRI Facility API and applicable DOE-IRI controlled-vocabulary specifications.

This profile does not independently redefine the allocation-unit vocabulary.

## 8. Allocation Semantics

A Project Allocation represents a Facility accounting allocation, not physical Resource capacity.

For example:

```json
{
  "entries": [
    {
      "allocation": 100000,
      "usage": 52342.5,
      "unit": "node_hours"
    }
  ]
}
```

indicates that 100,000 node-hours have been allocated and that the Facility reports 52,342.5 node-hours of usage for that Allocation Entry.

A client MAY calculate:

```text
allocation - usage
```

for display or analysis when the applicable accounting semantics permit such a calculation.

However, an arithmetically positive remainder MUST NOT by itself be interpreted as proof that:

- the Capability is currently available;
- a Resource is currently schedulable;
- the Project remains authorized;
- the allocation has not expired;
- the requesting user may consume the remaining quantity.

Accounting quantity, authorization, policy, and operational availability are separate concerns.

## 9. Hypermedia Representation

When represented using HAL, a Project Allocation SHOULD advertise its Project and Capability relationships through `_links`.

For example:

```json
{
  "id": "alloc-001",

  "entries": [
    {
      "allocation": 100000,
      "usage": 52342.5,
      "unit": "node_hours"
    }
  ],

  "project_uri":
    "https://api.example.org/api/v2/account/projects/climate-simulation",

  "capability_uri":
    "https://api.example.org/api/v2/account/capabilities/gpu-node-hours",

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/account/projects/climate-simulation/project_allocations/alloc-001",
      "type": "application/hal+json",
      "profile":
        "https://iri.science/profiles/account/project-allocation"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:has-project": {
      "href":
        "https://api.example.org/api/v2/account/projects/climate-simulation",
      "type": "application/hal+json",
      "profile":
        "https://iri.science/profiles/account/project"
    },

    "iri:has-capability": {
      "href":
        "https://api.example.org/api/v2/account/capabilities/gpu-node-hours",
      "type": "application/hal+json",
      "profile":
        "https://iri.science/profiles/account/capability"
    }
  }
}
```

In this representation:

- `self` identifies the Project Allocation representation;
- `iri:has-project` identifies the Project to which the allocation belongs;
- `iri:has-capability` identifies the Capability to which the allocation applies;
- `profile` identifies the semantic contract of a target representation;
- the relation names identify why the targets are related.

The relation URI, target URI, media type, and profile URI serve different purposes and MUST NOT be treated as interchangeable identifiers.

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
iri:has-project
```

expands to:

```text
https://iri.science/rels/has-project
```

and:

```text
iri:has-capability
```

expands to:

```text
https://iri.science/rels/has-capability
```

The canonical relation documents define the normative semantics of those relationships.

This Project Allocation profile MUST NOT redefine those relation semantics.

## 11. Relationship to Existing URI Properties

The current Project Allocation schema defines:

```text
project_uri
capability_uri
```

as direct URI-valued relationship properties.

When the IRI HAL hypermedia model is used, the corresponding relationships SHOULD be represented through `_links`:

```text
project_uri
    ↓
_links["iri:has-project"]


capability_uri
    ↓
_links["iri:has-capability"]
```

During the compatibility period:

1. Producers retain the required `project_uri` property.
2. Producers retain the required `capability_uri` property.
3. Producers MAY additionally expose `_links["iri:has-project"]`.
4. Producers MAY additionally expose `_links["iri:has-capability"]`.
5. Whenever both `project_uri` and `_links["iri:has-project"]` are present, the link `href` MUST exactly equal `project_uri`.
6. Whenever both `capability_uri` and `_links["iri:has-capability"]` are present, the link `href` MUST exactly equal `capability_uri`.
7. Consumers SHOULD prefer advertised hypermedia relationships and MAY fall back to the URI-valued properties.
8. Removing or changing either URI-valued property requires a separate OpenAPI schema revision.

Unlike several other IRI representations, the current Project Allocation schema does not define a `self_uri` property.

A HAL-enabled producer SHOULD nevertheless advertise a canonical `self` link when the Project Allocation has an independently addressable representation.

Clients MUST use the advertised `self` link rather than infer the Project Allocation URI from `id`, `project_uri`, or API path conventions.

## 12. Media Type

This profile identifies the semantics of the Project Allocation representation independently of a particular serialization.

When a Project Allocation is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/account/project-allocation
```

The media type and profile URI have different roles:

```text
application/hal+json
    ↓
HOW the representation is encoded


https://iri.science/profiles/account/project-allocation
    ↓
WHAT semantic representation contract applies
```

They MUST NOT be treated as interchangeable.

## 13. Static and Dynamic Semantics

A Project Allocation combines relatively stable accounting relationships with dynamic accounting quantities.

Relatively stable information includes:

```text
id
project_uri
capability_uri
```

The following values may change as usage is recorded:

```text
entries[].usage
```

Depending on Facility allocation policy, the following may also change over the allocation lifetime:

```text
entries[].allocation
entries
```

The Project and Capability relationships SHOULD remain stable for the lifetime of the represented Project Allocation.

If the allocation is reassigned to another Project or Capability, an implementation SHOULD consider whether that represents modification of the same allocation or creation of a new Project Allocation identity according to the governing API contract.

This profile does not independently define a Project Allocation lifecycle or state-transition model.

## 14. Authorization and Visibility

Project Allocation representations are authorization-sensitive.

A provider MAY expose only Project Allocations visible to the authenticated requester according to Facility policy.

Authorization MAY affect:

- whether a Project Allocation is discoverable;
- whether its Project is discoverable;
- whether its Capability is discoverable;
- whether usage information is visible;
- whether associated User Allocations are visible.

The visibility of a Project Allocation MUST NOT itself be interpreted as permission to consume the allocation.

Likewise, the presence of:

```text
iri:has-capability
```

does not grant access to the Capability.

Where URI-valued properties and corresponding HAL relationships are both returned, they MUST remain consistent.

Clients SHOULD treat the returned representation as the allocation information visible within the current authenticated requester context.

## 15. Conformance

A representation conforms to the IRI Account Project Allocation Profile when:

1. it conforms to the applicable IRI Facility API `ProjectAllocation` schema;
2. its properties are interpreted according to the IRI Facility API and this profile;
3. `id` is treated as an allocation identifier rather than a URL template;
4. `entries` are interpreted as accounting quantities rather than Resource availability;
5. each Allocation Entry interprets `allocation` and `usage` using its corresponding `unit`;
6. `project_uri` identifies exactly one Project association;
7. `capability_uri` identifies exactly one Capability association;
8. `iri:has-project` is used for the Project Allocation-to-Project relationship when represented through HAL;
9. `iri:has-capability` is used for the Project Allocation-to-Capability relationship when represented through HAL;
10. IRI-specific link relations use the canonical IRI relation namespace;
11. profile URIs identify representation semantics and are not used as substitutes for relation identifiers or instance identifiers;
12. when both `project_uri` and `_links["iri:has-project"]` are present, they identify the same target;
13. when both `capability_uri` and `_links["iri:has-capability"]` are present, they identify the same target;
14. clients do not infer Project, Capability, or Project Allocation URLs from identifiers or path conventions;
15. visibility of an allocation is not interpreted as authorization to consume it.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/project-allocation
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, Project Allocation identifiers, Project Allocation instance URLs, allocation-unit identifiers, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes to individual:

- Project Allocations;
- allocation amounts;
- usage amounts;
- allocation-unit values;
- Projects;
- Capabilities

do not themselves require a new Project Allocation profile URI.

Changes that materially alter the interpretation or processing semantics of the common Project Allocation representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Account Project Allocation Profile*