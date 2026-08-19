# RFC: Type-Specific Attributes and Resource Definition Profiles for IRI Resource Objects

## Abstract

The DOE Integrated Research Infrastructure (IRI) Facility API represents heterogeneous facility resources through a common `Resource` representation. Facilities also need to describe characteristics that are meaningful only for particular Resource types without continually expanding the common `Resource` schema.

This RFC defines the semantic use of the optional `attributes` property on an IRI `Resource` representation and defines how a registered `resource_type` selects an applicable IRI Resource Definition Profile.

The model separates four concerns:

```text
OpenAPI Resource schema
    defines the common JSON structure

Resource Type URN
    identifies what kind of Resource is represented

Resource Definition Profile
    defines additional semantics that apply to that Resource type

attributes
    carries type-specific data defined by the applicable Resource Definition Profile
```

Registered DOE-IRI URNs remain authoritative in the DOE-IRI URN Registry. Registered IRI link relations remain authoritative in the IRI Link Relation Registry. Resource Definition Profiles reference those registries rather than redefining them.

This RFC does not introduce a separate Resource Definition API object or a separate Resource State API object in IRI v2. It defines an extensible semantic specialization mechanism for the existing IRI v2 `Resource` representation.

## Status of This Memo

This document is an IRI Facility API RFC intended for use with DOE IRI specification version 2.0 and reference implementations.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

| Revision | Author | Date | Notes |
|---|---|---|---|
| 0.1 | ChatGPT | Jun 24, 2026 | Initial version. |
| 0.2 | John MacAuley | Jun 24, 2026 | Revised based on initial review. |
| 0.3 | John MacAuley | Jul 22, 2026 | Final revisions before subcommittee discussions. |
| 1.0 | John MacAuley | Aug 7, 2026 | Comments addressed; issued version 1.0 for publication. |
| 1.1 | John MacAuley | Aug 19, 2026 | Aligned with Resource Definition Profiles, current URN registries, and current IRI v2 Resource schema. |

# 1. Introduction

The IRI Facility API `Resource` representation provides a common model for physical, logical, virtual, and service-oriented infrastructure exposed by participating facilities.

Common Resource properties include concepts such as:

```text
id
name
description
last_modified
group
current_status
resource_type
supported_endpoints
self_uri
site_uri
capability_uris
attributes
```

The common representation cannot reasonably define every property needed to describe every kind of compute, storage, network, service, or future IRI Resource.

Examples of type-specific information include:

- compute-system architecture and capabilities;
- compute-node role and configured hardware;
- CPU architecture and processor characteristics;
- GPU programming interfaces and accelerator characteristics;
- storage-system technology and architecture;
- filesystem technology, protocol, and usage tier;
- block-storage access and provisioning characteristics;
- object-storage APIs and consistency characteristics;
- data-transfer service technology and transfer protocols;
- inference-service implementation and API characteristics.

Adding all such properties to the top-level `Resource` schema would create an ever-expanding common model and would couple OpenAPI evolution to the Resource Type taxonomy.

IRI therefore uses:

```text
resource_type
```

to identify the semantic Resource class and:

```text
attributes
```

as the designated container for type-specific Resource data.

The semantics of `attributes` are supplied by the Resource Definition Profile registered for the Resource's `resource_type`.

## 1.1. Architectural Roles

The following concepts are distinct:

```text
Resource instance identifier
    WHICH Resource is this?

Resource Type URN
    WHAT KIND of Resource is this?

Resource Definition Profile
    WHAT ADDITIONAL SEMANTICS apply to Resources of this type?

attributes
    WHAT TYPE-SPECIFIC DATA does this Resource representation contain?

link relation
    WHY is another target related or applicable?
```

For example:

```json
{
  "id": "orion",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "attributes": {
    "schema_version": "1.0.0",
    "storage_technology": "urn:doe-iri:storage:system-technology:lustre"
  }
}
```

uses:

```text
orion
    Resource instance identifier

urn:doe-iri:resource:storage:system
    Resource Type URN

https://iri.science/profiles/resource-definition/storage/system
    Resource Definition Profile

storage_technology
    property defined by the Resource Definition Profile

urn:doe-iri:storage:system-technology:lustre
    registered controlled attribute value
```

These identifiers and concepts MUST NOT be treated as interchangeable.

# 2. Scope

This RFC defines:

1. the semantic role of the `attributes` property on IRI `Resource` representations;
2. the use of `resource_type` as the selector for Resource Definition semantics;
3. the relationship between the common IRI Status Resource Profile and type-specific Resource Definition Profiles;
4. requirements for canonical Resource Definition Profiles;
5. processing requirements for producers and consumers;
6. use of registered DOE-IRI controlled attribute URNs within Resource Definition Profiles;
7. compatibility behavior for unknown Resource types, unknown profiles, and unfamiliar attributes;
8. requirements for facility- or project-specific Resource Definition Profiles associated with delegated DOE-IRI extension URNs.

This RFC does not:

1. define every Resource Type;
2. register Resource Type URNs;
3. register controlled attribute URNs;
4. register IRI link relations;
5. define arbitrary filtering over `attributes`;
6. define write operations for Resource attributes;
7. define authorization policy from Resource attributes;
8. require runtime profile dereferencing;
9. define a separate Resource Definition API representation;
10. define a separate Resource State API representation;
11. replace the IRI Facility API OpenAPI specification.

The authoritative registries are:

```text
../registry/urns/resource-types.md
    assigned Resource Type URNs

../registry/urns/attributes.md
    assigned controlled attribute URNs

../registry/relations/README.md
    registered IRI link relations

../registry/profiles/resource-definition/
    canonical Resource Definition Profiles
```

# 3. Semantic Model

## 3.1. Common Resource Representation

The common semantic profile for an IRI Resource representation is:

```text
https://iri.science/profiles/status/resource
```

That profile applies to every IRI Resource representation.

A more-specific Resource Definition Profile supplements the common profile when one is registered for the Resource's exact `resource_type`.

Conceptually:

```text
IRI Facility API OpenAPI Resource schema
        │
        ▼
IRI Status Resource Profile
https://iri.science/profiles/status/resource
        │
        │ resource_type
        ▼
registered Resource Type URN
        │
        ▼
optional Resource Definition Profile
https://iri.science/profiles/resource-definition/<domain>/<type>
        │
        ▼
semantics of Resource.attributes and type-specific behavior
```

A Resource Definition Profile specializes the existing Resource representation. It does not replace the common Resource profile.

## 3.2. Resource Type Registration

A Resource Type URN is a semantic identifier such as:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu

urn:doe-iri:resource:storage:system
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:storage:mount
urn:doe-iri:resource:storage:block
urn:doe-iri:resource:storage:object

urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

The DOE-IRI Resource Type Registry is authoritative for assigned Resource Type URNs, their hierarchy, lifecycle status, and associated Resource Definition Profile when one exists.

The Resource Definition Profile MUST NOT become an independent authoritative registration record for the Resource Type URN.

## 3.3. No URL or Profile-URI Construction from Resource Type

A Resource Type URN identifies semantic classification. It does not encode an API path.

A client MUST NOT derive an API path from `resource_type`.

Similarly, a client MUST NOT assume that a Resource Definition Profile URI can be constructed mechanically from a Resource Type URN.

For example, although the registry may associate:

```text
urn:doe-iri:resource:compute:system
```

with:

```text
https://iri.science/profiles/resource-definition/compute/system
```

the registry association is authoritative.

Clients SHOULD use known registry mappings or locally recognized profile identifiers rather than inventing profile URIs by string transformation.

# 4. The `attributes` Property

## 4.1. Structural Contract

The IRI v2 OpenAPI `Resource` schema is authoritative for the structural definition of `attributes`.

Under the current IRI v2 schema, `attributes` is:

- optional;
- represented as an object when populated;
- nullable;
- open to additional properties.

This RFC does not narrow that wire-level contract.

A producer SHOULD omit `attributes` when it has no type-specific attribute data to report.

A producer MAY emit:

```json
{
  "attributes": null
}
```

when permitted by the governing OpenAPI contract, but omission is preferred when no attribute data is being reported.

Consumers MUST tolerate both `attributes` being absent and `attributes` being `null` when allowed by the governing OpenAPI schema.

When `attributes` contains data, it MUST be a JSON object.

## 4.2. Semantic Contract

The semantic meaning of members within `attributes` is determined by the Resource Definition Profile applicable to the Resource's `resource_type`.

A Resource Definition Profile may define:

- permitted property names;
- property semantics;
- JSON value types;
- required properties within `attributes`;
- controlled vocabulary requirements;
- units and encoding conventions;
- constraints between attributes;
- extension behavior;
- examples;
- type-specific relationships;
- type-specific operation affordances.

The profile MUST remain compatible with the structural contract defined by OpenAPI.

## 4.3. Common-Field Precedence

The `attributes` object MUST NOT redefine or override common top-level Resource properties.

For example, a Resource Definition Profile MUST NOT redefine:

```text
id
last_modified
current_status
resource_type
self_uri
site_uri
capability_uris
```

inside `attributes` with competing semantics.

For example:

```json
{
  "current_status": "up",
  "attributes": {
    "current_status": "down"
  }
}
```

MUST NOT be defined as a valid profile pattern.

When the common Resource representation already defines a concept, the common property is authoritative.

## 4.4. Attribute Names

Ordinary JSON attribute names are defined by the applicable Resource Definition Profile.

Examples include:

```text
schema_version
storage_technology
storage_architecture
capacity_gib
vendor
product
cpu_architecture
configured_memory_gib
supported_apis
```

Ordinary JSON property names are not DOE-IRI URNs.

Where a property requires a controlled machine-readable value, the applicable Resource Definition Profile SHOULD use a registered DOE-IRI controlled attribute URN when an appropriate vocabulary exists.

## 4.5. Controlled Attribute Values

Controlled DOE-IRI attribute values are registered separately from Resource Definition Profiles.

For example:

```json
{
  "storage_technology": "urn:doe-iri:storage:system-technology:lustre"
}
```

The Resource Definition Profile defines the `storage_technology` property semantics and allowed value domain, while the DOE-IRI Controlled Attribute URN Registry defines the registered controlled value.

A Resource Definition Profile MAY enumerate registered values for readability, but the central URN registry remains authoritative for registration and lifecycle status.


# 5. Resource Type as Profile Selector

## 5.1. Exact Resource Type Selection

The full `resource_type` value selects the applicable Resource Definition semantics.

For example:

```text
resource_type = urn:doe-iri:resource:storage:system
```

is currently associated with:

```text
https://iri.science/profiles/resource-definition/storage/system
```

A Resource conforming to that Resource Definition Profile also conforms to the common:

```text
https://iri.science/profiles/status/resource
```

profile.

## 5.2. Generic Resource Types

Not every registered Resource Type requires a Resource Definition Profile.

A broad Resource Type may be fully usable using only the common Resource profile.

For example, the Resource Type registry may register:

```text
urn:doe-iri:resource:compute
urn:doe-iri:resource:storage
urn:doe-iri:resource:service
urn:doe-iri:resource:network
```

without requiring a type-specific Resource Definition Profile for each broad parent.

The Resource Type Registry MUST indicate the applicable Resource Definition Profile when a canonical one exists.

## 5.3. Hierarchical Fallback

The DOE-IRI URN specification defines hierarchy-aware handling of Resource Type URNs.

A consumer MAY use a recognized semantic parent for generic classification or fallback behavior.

However, hierarchy fallback MUST NOT be treated as implicit profile inheritance.

Recognizing `urn:doe-iri:resource:storage` does not by itself authorize a consumer to validate the `attributes` of `urn:doe-iri:resource:storage:filesystem` against an inferred schema.

Profile inheritance MUST be explicitly defined by the applicable profile or registry metadata.

## 5.4. Unknown Resource Types

A generic consumer MUST NOT reject an otherwise valid Resource solely because the specific `resource_type` is unfamiliar to its implementation.

A consumer that does not recognize the exact Resource Definition Profile:

- MUST still process the common Resource representation when possible;
- MAY treat `attributes` as opaque JSON data;
- SHOULD ignore unfamiliar attributes that are not needed for its operation;
- MUST NOT infer unsupported semantics from unfamiliar fields;
- MUST NOT require network dereferencing of a profile in order to process the common Resource representation.
- 

# 6. Resource Definition Profiles

## 6.1. Purpose

A Resource Definition Profile defines additional semantics that apply to the current IRI v2 `Resource` representation because of its `resource_type`.

Canonical shared Resource Definition Profiles use identifiers under:

```text
https://iri.science/profiles/resource-definition/
```

Examples include:

```text
https://iri.science/profiles/resource-definition/compute/system
https://iri.science/profiles/resource-definition/compute/node
https://iri.science/profiles/resource-definition/compute/cpu
https://iri.science/profiles/resource-definition/compute/gpu

https://iri.science/profiles/resource-definition/storage/system
https://iri.science/profiles/resource-definition/storage/filesystem
https://iri.science/profiles/resource-definition/storage/mount
https://iri.science/profiles/resource-definition/storage/block
https://iri.science/profiles/resource-definition/storage/object

https://iri.science/profiles/resource-definition/service/dtn
https://iri.science/profiles/resource-definition/service/inference
```

## 6.2. Required Profile Identification

A canonical Resource Definition Profile SHOULD identify at least:

```text
Profile URI
Base Profile
Resource Type
Status
Version
```

For example:

```markdown
**Profile URI:** `https://iri.science/profiles/resource-definition/compute/system`
**Base Profile:** `https://iri.science/profiles/status/resource`
**Resource Type:** `urn:doe-iri:resource:compute:system`
**Status:** Draft
**Version:** 1.0.0
```

The Resource Type URN and Profile URI are different identifiers and MUST NOT be used interchangeably.

## 6.3. Profile Responsibilities

A Resource Definition Profile SHOULD document, as applicable:

- applicability;
- type-specific semantic model;
- type-specific attributes;
- controlled DOE-IRI vocabularies used by those attributes;
- relationships applicable to the Resource type;
- operation affordances applicable to the Resource type;
- attribute extension policy;
- security or visibility considerations;
- examples;
- conformance requirements.

A Resource Definition Profile MUST NOT:

- redefine the DOE-IRI URN grammar;
- independently register controlled DOE-IRI URNs;
- invent unregistered `iri:*` link relations and use them normatively;
- replace the OpenAPI structural contract;
- redefine common Resource properties;
- require a separate IRI v2 Resource Definition endpoint;
- require a separate IRI v2 Resource State endpoint.

## 6.4. `schema_version`

Canonical Resource Definition Profiles SHOULD define a `schema_version` attribute for the version of the type-specific `attributes` contract.

When a Resource Definition Profile declares `schema_version` mandatory, a producer using non-null `attributes` under that profile MUST provide it.

For example:

```json
{
  "attributes": {
    "schema_version": "1.0.0"
  }
}
```

`schema_version` identifies the version of the Resource Definition Profile's type-specific attribute contract. It is not the IRI Facility API version, the OpenAPI version, the Resource Type URN version, or the version of the Resource instance.

## 6.5. Relationships

Resource Definition Profiles may state which registered link relations are applicable to a Resource type.

For example, a storage-system Resource Definition Profile may use:

```text
iri:provides-filesystem
iri:provides-block
iri:provides-object
```

The corresponding definitions under `../registry/relations/` remain authoritative for relation semantics, cardinality, source and target classification, visibility, and volatility.

A Resource Definition Profile MUST NOT redefine a registered link relation with different semantics.

## 6.6. Operation Affordances

A Resource Definition Profile may identify registered operation-affordance relations applicable to the type.

For example:

```text
iri:submit-job
```

may apply to:

```text
urn:doe-iri:resource:compute:system
```

The relation identifies that the operation is applicable and where the entry point is located.

The governing OpenAPI contract remains authoritative for HTTP method, request schema, response schema, parameters, authentication, authorization, and error handling.


# 7. Current IRI v2 Modeling Scope

This RFC does not define a separate Resource Definition representation or Resource State representation for IRI v2.

The term **Resource Definition Profile** means a type-specific semantic specialization of the existing IRI v2 `Resource` representation.

The current Resource representation may contain both common properties and type-specific attributes according to the governing OpenAPI schema and applicable profiles.

A Resource Definition Profile SHOULD clearly describe the semantics of each attribute, including whether a value represents configuration, capability, descriptive metadata, a measured or quantitative value, a time-varying observation, or another type-specific concept.

A profile MUST NOT duplicate or override `current_status`, which remains a common top-level Resource property.

If an attribute can change over time, its profile SHOULD define the meaning of the value and any relevant update semantics.

This RFC intentionally does not prescribe a future IRI v3 decomposition of Resource definition and Resource state.


# 8. Canonical Example: Storage System

The Resource Type registry associates:

```text
urn:doe-iri:resource:storage:system
```

with:

```text
https://iri.science/profiles/resource-definition/storage/system
```

A representation may therefore contain type-specific attributes such as:

```json
{
  "id": "orion",
  "name": "Orion",
  "description": "Facility storage system",
  "last_modified": "2026-08-19T15:00:00Z",
  "current_status": "up",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "self_uri": "https://api.example.org/api/v2/status/resources/orion",
  "site_uri": "https://api.example.org/api/v2/facility/sites/example-site",
  "capability_uris": [],
  "attributes": {
    "schema_version": "1.0.0",
    "storage_technology": "urn:doe-iri:storage:system-technology:lustre",
    "storage_architecture": [
      "urn:doe-iri:storage:system-architecture:distributed",
      "urn:doe-iri:storage:system-architecture:clustered"
    ],
    "storage_capabilities": [
      "urn:doe-iri:storage:system-capability:replication",
      "urn:doe-iri:storage:system-capability:snapshot"
    ],
    "media_types": [
      "urn:doe-iri:storage:media-type:solid-state",
      "urn:doe-iri:storage:media-type:magnetic-disk"
    ],
    "capacity_gib": 10485760,
    "vendor": "Example Vendor",
    "product": "Example Platform",
    "version": "1.0"
  },
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/orion",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/system"
    },
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:located-at": {
      "href": "https://api.example.org/api/v2/facility/sites/example-site"
    },
    "iri:provides-filesystem": [
      {
        "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
        "type": "application/hal+json",
        "profile": "https://iri.science/profiles/resource-definition/storage/filesystem"
      }
    ]
  }
}
```

The example illustrates separate semantic responsibilities:

```text
resource_type
    identifies Storage System classification

Resource Definition Profile
    defines the Storage System attribute contract

storage_technology / storage_architecture / ...
    ordinary JSON properties defined by that profile

urn:doe-iri:storage:...
    registered controlled values

iri:located-at / iri:provides-filesystem
    registered link relations
```

The example is illustrative. The governing OpenAPI specification is authoritative for the complete JSON structure and the relation definitions are authoritative for link semantics.


# 9. Delegated Extension Resource Types

The DOE-IRI URN specification defines the canonical `ext` mechanism for delegated facility- or project-controlled Resource Type extensions.

For example:

```text
urn:doe-iri:resource:compute:ext:nersc:fpga
```

is syntactically an extension Resource Type under the shared:

```text
urn:doe-iri:resource:compute
```

semantic parent.

A producer MUST NOT claim an extension as an assigned DOE-IRI extension unless the syntax, scope-authorization, and local-definition requirements of the DOE-IRI URN specification are satisfied.

A delegated authority MAY publish a Resource Definition Profile for an assigned local Resource Type.

The delegated authority's local definition SHOULD identify:

- the exact extension Resource Type URN;
- the Resource Definition Profile URI;
- the shared base Resource profile;
- the profile version;
- the type-specific attribute semantics;
- controlled values used by the profile;
- applicable registered link relations;
- extension-property policy.

The profile URI need not be under `iri.science` unless the profile becomes part of the shared DOE-IRI profile registry.

A consumer MUST NOT require automatic network retrieval of a facility-local profile in order to process the common Resource representation.


# 10. OpenAPI and API Behavior

## 10.1. OpenAPI Authority

The IRI Facility API OpenAPI specification is authoritative for the structural definition of the `Resource` representation.

This RFC does not duplicate or replace that schema.

The current IRI v2 Resource contract already includes an optional `attributes` property. Therefore this revision does not require adding a new `ResourceAttributes` component merely to implement the semantic model described here.

If the OpenAPI structure changes, the OpenAPI specification controls the wire contract and this RFC/profile set MUST be reviewed for semantic consistency.

## 10.2. Applicable Endpoints

No new endpoint is required by this RFC.

Resource Definition semantics apply wherever the API returns a `Resource` representation, including Resource collections and individually addressable Resources.

## 10.3. Filtering

This RFC does not define filtering over arbitrary members of `attributes`.

Resource filtering by `resource_type`, when supported by the governing API, SHOULD use canonical DOE-IRI Resource Type URNs according to the applicable OpenAPI contract.

A future specification MAY define profile-aware filtering after query semantics, authorization behavior, indexing requirements, and performance expectations are defined.

## 10.4. Modification Semantics

Changes to type-specific attributes are changes to the Resource representation.

When a material change to reported `attributes` occurs, the producer MUST update `last_modified` consistently with the governing Resource modification semantics.

A Resource Definition Profile MAY provide more specific guidance for attributes whose values change frequently.


# 11. Producer Requirements

A producer conforming to this RFC:

1. MUST conform to the governing IRI v2 OpenAPI `Resource` schema.
2. MUST use a registered or valid delegated DOE-IRI Resource Type URN according to the governing URN specification and applicable API requirements.
3. SHOULD emit the most-specific accurate registered Resource Type that is appropriate to disclose.
4. MAY omit `attributes`.
5. MAY emit `attributes: null` when permitted by OpenAPI, although omission is preferred when no attribute data is reported.
6. MUST emit `attributes` as an object when type-specific attribute data is present.
7. MUST interpret that object according to the applicable Resource Definition Profile when one is claimed or registered.
8. MUST NOT use `attributes` to override common Resource properties.
9. MUST use registered controlled DOE-IRI attribute URNs where the applicable Resource Definition Profile requires them.
10. MUST NOT claim an unregistered shared URN as a canonical DOE-IRI value.
11. MUST NOT use unregistered `iri:*` relation names normatively.
12. MUST NOT place credentials, access tokens, secrets, private keys, or other sensitive authentication material in `attributes`.
13. MUST update `last_modified` when required by the governing Resource modification semantics.
14. SHOULD publish documentation for delegated facility-local Resource Definition Profiles.
15. SHOULD use canonical shared Resource Definition Profiles when available.


# 12. Consumer Requirements

A consumer conforming to this RFC:

1. MUST process the common Resource representation independently of whether it understands the most-specific Resource Definition Profile.
2. MUST tolerate absence of `attributes`.
3. MUST tolerate `attributes: null` when permitted by the governing OpenAPI contract.
4. MUST treat an unfamiliar Resource Definition Profile as non-fatal.
5. MUST NOT reject a Resource solely because it contains unfamiliar attribute names.
6. SHOULD use the exact `resource_type` to select locally known Resource Definition semantics.
7. MAY use Resource Type hierarchy-aware fallback for generic classification.
8. MUST NOT infer a complete attribute-validation contract solely from URN prefix matching.
9. MUST NOT infer a Resource Definition Profile URI by mechanically rewriting the Resource Type URN.
10. MAY treat unfamiliar `attributes` content as opaque JSON.
11. SHOULD ignore attributes not relevant to the consumer's purpose.
12. MUST NOT rely on Resource Type or attributes alone as authorization, entitlement, availability, or trust assertions.
13. MUST NOT automatically execute or instantiate code based on attribute values, Resource Type URNs, or profile identifiers.


# 13. Compatibility and Versioning

## 13.1. API Compatibility

The IRI v2 Resource schema already provides an extensible `attributes` container.

This RFC defines interoperable semantic use of that container. It does not require clients to understand every Resource Definition Profile.

A generic consumer remains interoperable by processing the common Resource properties and ignoring unfamiliar type-specific data.

## 13.2. Resource Type Evolution

New shared Resource Types are registered through the DOE-IRI URN governance process.

Adding a new registered Resource Type does not by itself require an OpenAPI schema revision when `resource_type` remains an extensible string.

A new Resource Type MAY have a new Resource Definition Profile.

## 13.3. Resource Definition Profile Evolution

Compatible changes MAY retain the same canonical profile URI according to the profile's versioning policy.

Changes requiring compatibility review include:

- removing a previously supported attribute;
- materially changing an attribute's meaning;
- changing units;
- narrowing accepted values;
- changing a required attribute to have incompatible semantics;
- changing controlled vocabulary semantics;
- changing relationship requirements.

A new descendant Resource Type MUST NOT be created merely as a substitute for ordinary profile versioning unless the Resource itself represents a meaningfully different semantic type.

## 13.4. `schema_version`

When a Resource Definition Profile uses `schema_version`, its value versions the type-specific attribute contract for that profile.

Consumers MUST interpret `schema_version` only in the context of the Resource Definition Profile selected for the Resource.


# 14. Security Considerations

Resource attributes are descriptive or operational data. They are not, by themselves:

- authorization credentials;
- proof of entitlement;
- proof of allocation;
- proof of trust;
- proof of current availability;
- permission to invoke an operation.

Implementations MUST treat attribute values, URNs, profile identifiers, and link targets as data rather than executable instructions.

Implementations MUST NOT deserialize Resource attributes into arbitrary executable classes or otherwise evaluate attribute content as code.

Implementations SHOULD:

1. validate externally sourced data before publishing it;
2. apply appropriate size and nesting-depth limits;
3. safely escape displayed values;
4. avoid exposing sensitive topology or operational information when disclosure is not authorized;
5. avoid automatic schema retrieval or code loading solely because a Resource contains an unfamiliar `resource_type` or profile;
6. avoid exposing credentials, tokens, secrets, private keys, or protected personal information;
7. apply authorization before revealing relationships or attributes whose disclosure is sensitive.


# 15. IANA Considerations

This document requires no IANA action.

The DOE-IRI URN namespace specification separately discusses potential future IANA registration of the `doe-iri` URN namespace.


# 16. References

1. RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*.
2. RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.
3. RFC 8141, *Uniform Resource Names (URNs)*.
4. RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*.
5. RFC 6906, *The 'profile' Link Relation Type*.
6. OpenAPI Specification 3.1.
7. [A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md).
8. [HAL `_links` for the IRI Facility API](./rfc-hal-links.md).
9. [DOE-IRI URN Registry](../registry/urns/README.md).
10. [DOE-IRI Resource Type URNs](../registry/urns/resource-types.md).
11. [DOE-IRI Controlled Attribute URNs](../registry/urns/attributes.md).
12. [DOE-IRI Link Relation Index](../registry/relations/README.md).
13. [IRI Status Resource Profile](../registry/profiles/status/resource.md).
14. [IRI Resource Definition Profiles](../registry/profiles/resource-definition/).
15. [IRI Facility API OpenAPI v2](../specification-v2/openapi/all_spec_v2.yaml).


# Appendix A. Current Shared Resource Definition Profiles

At the time of this revision, the Resource Type registry associates the following refined shared Resource Types with Resource Definition Profiles:

| Resource Type URN | Resource Definition Profile |
|---|---|
| `urn:doe-iri:resource:compute:system` | `https://iri.science/profiles/resource-definition/compute/system` |
| `urn:doe-iri:resource:compute:node` | `https://iri.science/profiles/resource-definition/compute/node` |
| `urn:doe-iri:resource:compute:cpu` | `https://iri.science/profiles/resource-definition/compute/cpu` |
| `urn:doe-iri:resource:compute:gpu` | `https://iri.science/profiles/resource-definition/compute/gpu` |
| `urn:doe-iri:resource:storage:system` | `https://iri.science/profiles/resource-definition/storage/system` |
| `urn:doe-iri:resource:storage:filesystem` | `https://iri.science/profiles/resource-definition/storage/filesystem` |
| `urn:doe-iri:resource:storage:mount` | `https://iri.science/profiles/resource-definition/storage/mount` |
| `urn:doe-iri:resource:storage:block` | `https://iri.science/profiles/resource-definition/storage/block` |
| `urn:doe-iri:resource:storage:object` | `https://iri.science/profiles/resource-definition/storage/object` |
| `urn:doe-iri:resource:service:dtn` | `https://iri.science/profiles/resource-definition/service/dtn` |
| `urn:doe-iri:resource:service:inference` | `https://iri.science/profiles/resource-definition/service/inference` |

This appendix is informational. The DOE-IRI Resource Type Registry is authoritative for the current set of registrations.


# Appendix B. Processing Example

Given:

```json
{
  "resource_type": "urn:doe-iri:resource:compute:system",
  "attributes": {
    "schema_version": "1.0.0",
    "system_capabilities": [
      "urn:doe-iri:compute:system-capability:batch-scheduling",
      "urn:doe-iri:compute:system-capability:accelerator-support"
    ]
  }
}
```

a profile-aware client can process the representation as:

```text
1. Parse the common Resource representation according to OpenAPI.

2. Apply:
   https://iri.science/profiles/status/resource

3. Recognize:
   urn:doe-iri:resource:compute:system

4. Consult the known registry mapping to:
   https://iri.science/profiles/resource-definition/compute/system

5. Interpret `attributes` using that Resource Definition Profile.

6. Interpret controlled values using:
   registry/urns/attributes.md

7. Interpret any `iri:*` links using:
   registry/relations/README.md and the linked relation definition.
```

A generic client that does not know step 4 can still process the common Resource representation and safely treat the `attributes` object as unfamiliar type-specific data.