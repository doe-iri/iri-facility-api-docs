# IRI Account Capability Profile

**Profile URI:** `https://iri.science/profiles/account/capability`  
**OpenAPI type:** `Capability`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Account Capability representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/capability
```

An IRI Capability represents an allocatable or otherwise distinguishable aspect of an IRI Resource.

A Capability allows a Facility to describe a portion, class, or characteristic of a Resource against which allocations may be granted and usage may be accounted.

For example, a compute Resource may expose a Capability corresponding to GPU-enabled nodes, while another Capability may represent CPU-only capacity.

A Capability is distinct from:

- a Resource, which represents the underlying compute, storage, network, service, or other infrastructure;
- a Project Allocation, which grants a Project some quantity of a Capability;
- a User Allocation, which assigns some portion of a Project Allocation to a user;
- an allocation unit, which identifies how the quantity of a Capability is measured.

The normative structural definition of a Capability representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with application-level semantics, relationship conventions, and interoperability requirements.

## 2. Profile Semantics

An IRI Capability identifies an aspect of a Resource that can participate in the IRI allocation model.

A Capability MAY correspond:

- one-to-one with an underlying Resource;
- to a subset or partition of a Resource;
- to a particular class of Resource functionality;
- to an allocatable Resource characteristic.

For example, a compute system may expose:

```text
GPU nodes
CPU nodes
large-memory nodes
```

as separately allocatable Capabilities even though they belong to the same underlying compute Resource.

A Capability does not itself represent:

- an allocation;
- an authorization grant;
- current availability;
- an operation entry point;
- a guarantee that the Capability can presently be consumed.

Those concerns are represented independently.

## 3. Structural Contract

The structural definition of the Capability representation is defined by the IRI Facility API OpenAPI `Capability` schema.

The current Capability schema defines the following properties:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Capability. |
| `name` | No | Human-readable long name of the Capability. |
| `description` | No | Human-readable description of the Capability. |
| `last_modified` | No | Time at which the Capability representation was last modified. |
| `units` | Yes | Allocation units supported by the Capability. |
| `self_uri` | Yes | Canonical API URI of the Capability representation. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- nullable properties;
- formats;
- structural validation;
- read-only properties.

The applicable IRI controlled-vocabulary or URN specifications are authoritative for registered allocation-unit identifiers where those specifications are adopted.

This profile is authoritative for additional semantic and interoperability conventions associated with a Capability representation.

## 4. Capability Identity

The `id` property identifies the Capability instance.

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless another IRI specification explicitly defines additional semantics for that identifier.

For example:

```json
{
  "id": "perlmutter-gpu"
}
```

identifies a particular Capability.

Clients MUST NOT infer API paths from the Capability identifier.

For example, a client MUST NOT assume that:

```text
perlmutter-gpu
```

implies:

```text
/api/v2/account/capabilities/perlmutter-gpu
```

The canonical Capability URI MUST instead be obtained from `self_uri` or the corresponding advertised hypermedia link.

## 5. Capability Naming

### 5.1 `name`

`name` provides the human-readable name of the Capability.

For example:

```json
{
  "name": "Perlmutter GPU Nodes"
}
```

The name is descriptive and MUST NOT be treated as the stable identity of the Capability.

### 5.2 `description`

`description` provides additional human-readable information about the Capability.

For example:

```json
{
  "description": "GPU-enabled compute capacity available to allocated projects."
}
```

Descriptions MAY change without changing the identity of the Capability.

## 6. Allocation Units

The `units` property identifies the units in which allocations associated with the Capability may be expressed.

For example:

```json
{
  "units": [
    "node_hours"
  ]
}
```

A Capability MAY support more than one allocation unit when permitted by the governing API contract.

The presence of a unit on a Capability means that allocations for that Capability may be expressed using that unit.

It does not indicate:

- the amount allocated;
- the amount consumed;
- remaining capacity;
- Resource availability.

Those values belong to the applicable allocation representation.

Conceptually:

```text
Capability
    │
    └── supports allocation measurement in
             ↓
        Allocation Unit

ProjectAllocation
    │
    └── records
             ↓
        allocation + usage
```

If the IRI Allocation Unit vocabulary is represented using DOE-IRI URNs, producers and consumers SHOULD use the registered canonical URN values defined by the applicable IRI specification.

## 7. Capability and Resource Relationship

A Capability is associated with an IRI Resource.

The Resource representation exposes this association in the Resource-to-Capability direction through:

```text
capability_uris
```

The registered hypermedia relation is:

```text
iri:has-capability
```

with canonical relation URI:

```text
https://iri.science/rels/has-capability
```

Conceptually:

```text
Resource  -- iri:has-capability -->  Capability
   1                  0..*
```

A Capability linked through `iri:has-capability` represents an allocatable or otherwise distinguished aspect of the source Resource.

The existence of this relationship MUST NOT be interpreted as:

- granting an allocation;
- granting permission to use the Resource;
- indicating current availability;
- indicating remaining allocation;
- identifying an operation endpoint.

## 8. Capability and Allocation Relationship

A Project Allocation applies to a Capability.

The current Project Allocation representation exposes the target Capability through:

```text
capability_uri
```

which maps to:

```text
iri:has-capability
```

in the current HAL relationship model.

The same relation therefore appears in different representation contexts:

```text
Resource
   │
   └── iri:has-capability
              ↓
         Capability


ProjectAllocation
   │
   └── iri:has-capability
              ↓
         Capability
```

The source representation determines the specific contextual interpretation:

- from a Resource, the Capability is provided or associated with that Resource;
- from a Project Allocation, the allocation applies to that Capability.

The canonical `iri:has-capability` relation definition is authoritative for the complete cross-context semantics.

This Capability profile MUST NOT redefine the registered relation.

## 9. Hypermedia Representation

When represented using HAL, a Capability SHOULD advertise its canonical identity through `_links.self`.

For example:

```json
{
  "id": "perlmutter-gpu",
  "name": "Perlmutter GPU Nodes",
  "description": "GPU-enabled compute capacity available to allocated projects.",
  "units": [
    "node_hours"
  ],

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/account/capabilities/perlmutter-gpu",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/account/capability"
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

- `self` identifies the Capability representation;
- `href` identifies the target URI;
- `type` identifies the expected representation media type;
- `profile` identifies the IRI Account Capability semantic profile.

The representation profile URI is not a Capability identifier and MUST NOT be treated as one.

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
iri:has-capability
```

expands to:

```text
https://iri.science/rels/has-capability
```

The canonical relation document defines the normative semantics of the relationship.

The Capability profile MUST NOT redefine those link-relation semantics.

## 11. Relationship to Existing URI Properties

The current Capability schema defines:

```text
self_uri
```

as the canonical URI of the Capability representation.

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
    "https://api.example.org/api/v2/account/capabilities/perlmutter-gpu",

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/account/capabilities/perlmutter-gpu",
      "profile": "https://iri.science/profiles/account/capability"
    }
  }
}
```

During the compatibility period:

1. Producers retain the required `self_uri` property.
2. Producers MAY additionally expose `_links.self`.
3. Whenever both are present, `_links.self.href` MUST exactly equal `self_uri`.
4. Consumers SHOULD prefer the advertised HAL relation and MAY fall back to `self_uri`.
5. Removing or changing `self_uri` requires a separate OpenAPI schema revision.

Clients SHOULD use the advertised canonical URI rather than constructing Capability URLs from identifiers.

## 12. Media Type

This profile identifies the semantics of the Capability representation independently of a particular serialization.

When a Capability is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/account/capability
```

The media type and profile serve different purposes:

```text
application/hal+json
    ↓
HOW the representation is encoded

https://iri.science/profiles/account/capability
    ↓
WHAT semantic representation contract applies
```

They MUST NOT be treated as interchangeable.

## 13. Static and Dynamic Semantics

A Capability representation primarily describes relatively stable allocation and Resource-model information.

Relatively stable information includes:

```text
id
name
description
units
```

`last_modified` indicates when the Capability representation was most recently modified when that value is available.

The existence of a Capability MUST NOT be interpreted as indicating:

- that capacity is currently available;
- that an authenticated user has an allocation;
- that a Project is authorized to consume the Capability;
- that the underlying Resource is operational.

Those questions require the appropriate Resource status, allocation, authorization, or operational representations.

## 14. Authorization and Visibility

Authorization MAY affect which Capabilities are visible to a requester.

A Facility MAY expose only Capabilities the requester is permitted to discover, subject to the governing API contract.

The absence of a Capability from a Resource or Capability collection MUST NOT necessarily be interpreted as proof that the Capability does not exist.

Likewise, visibility of a Capability MUST NOT itself be interpreted as authorization to consume that Capability.

Allocation and authorization decisions remain separate from Capability discovery.

Clients SHOULD treat the returned representation as the Capability information visible in the current requester context.

## 15. Conformance

A representation conforms to the IRI Account Capability Profile when:

1. it conforms to the applicable IRI Facility API `Capability` schema;
2. its properties are interpreted according to the IRI Facility API and this profile;
3. `id` is treated as a Resource-local identifier rather than a URL template;
4. `units` identifies supported allocation measurement units rather than allocation quantities;
5. Capability visibility is not interpreted as an authorization or allocation grant;
6. associated Resource and allocation relationships use registered IRI link relations where advertised;
7. IRI-specific link relations use the canonical IRI relation namespace;
8. profile URIs identify representation semantics and are not used as substitutes for link-relation identifiers;
9. when both `self_uri` and `_links.self` are present, they identify the same target;
10. clients are not required to infer or construct Capability URLs.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/account/capability
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI locations, allocation-unit identifiers, Capability instance identifiers, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Adding new allocation units or new Capability instances does not itself require a new Capability profile URI.

Changes that materially alter the interpretation or processing semantics of the common Capability representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Account Capability Profile*
