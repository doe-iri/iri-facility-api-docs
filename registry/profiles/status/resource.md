# IRI Status Resource Profile

**Profile URI:** `https://iri.science/profiles/status/resource`  
**OpenAPI type:** `Resource`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Status Resource representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/status/resource
```

An IRI Resource represents physical, logical, virtual, or service-oriented infrastructure exposed through an IRI Facility API.

Resources may represent, for example:

- compute systems;
- compute nodes;
- CPUs or GPUs;
- storage systems;
- filesystems;
- network infrastructure;
- facility-hosted services;
- data-transfer services;
- inference services;
- websites or portals;
- other registered IRI resource types.

A Resource is distinct from:

- a Facility, which represents the organization providing the IRI Facility API;
- a Site, which represents the physical site associated with Resources;
- an Event, which records a timestamped occurrence involving a Resource;
- an Incident, which groups related Events and identifies Resources that may be affected;
- a Capability, which identifies an allocatable or otherwise distinguished capability associated with a Resource.

The normative structural definition of a Resource representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with application-level semantics, resource-type interpretation rules, relationship conventions, and interoperability requirements.

## 2. Profile Semantics

An IRI Resource is an independently identifiable entity exposed by a participating Facility.

A Resource representation describes:

- the identity of the Resource;
- the semantic type of the Resource;
- relatively stable descriptive attributes;
- the Site associated with the Resource;
- current reported status when available;
- Capabilities associated with the Resource;
- type-specific attributes where applicable;
- relationships to other IRI Resources;
- applicable operation entry points when advertised.

A Resource representation SHOULD provide sufficient hypermedia information for clients to discover related resources and applicable operations without requiring clients to infer API paths.

Clients MUST NOT infer related-resource URLs or operation entry points from:

- Resource identifiers;
- Resource Type URNs;
- Site identifiers;
- naming conventions;
- known Facility routing conventions;
- previously observed API paths.

When a relationship or operation entry point is advertised through `_links`, clients SHOULD use the advertised target.

## 3. Structural Contract

The structural definition of the Resource representation is defined by the IRI Facility API OpenAPI `Resource` schema.

The V2 Resource schema defines the following conceptual properties:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Resource. |
| `name` | No | Human-readable long name of the Resource. |
| `description` | No | Human-readable description of the Resource. |
| `last_modified` | Yes | Time at which the Resource representation was last modified. |
| `group` | No | Logical grouping associated with the Resource. |
| `current_status` | No | Current status reported for the Resource. |
| `resource_type` | Yes | IRI Resource Type URN identifying the semantic type of the Resource. |
| `supported_endpoints` | No | Broad endpoint categories supported by the Resource. |
| `self_uri` | Yes | Canonical API URI of the Resource representation. |
| `site_uri` | Yes | URI identifying the authoritative Site associated with the Resource. |
| `capability_uris` | Yes | URIs identifying Capabilities associated with the Resource. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- nullable properties;
- formats;
- structural validation;
- read-only properties.

The DOE-IRI URN specification and DOE-IRI URN Registry are authoritative for:

- Resource Type URN syntax;
- registered Resource Type values;
- Resource Type hierarchy;
- registered parent-child relationships;
- delegated extension rules.

This profile is authoritative for additional semantic and interoperability conventions associated with the Resource representation.

## 4. Resource Identity

The `id` property identifies the Resource instance.

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque Resource identifier unless another IRI specification explicitly defines additional semantics for that identifier.

The Resource instance identifier and the Resource Type URN serve different purposes.

For example:

```json
{
  "id": "pioneer-compute",
  "resource_type": "urn:doe-iri:resource:compute:system"
}
```

means:

```text
pioneer-compute
    ↓
identifies WHICH Resource instance

urn:doe-iri:resource:compute:system
    ↓
identifies WHAT KIND of Resource it is
```

Clients MUST NOT construct API URLs by combining the Resource identifier with assumed path templates.

For example, a client discovering:

```json
{
  "id": "pioneer-compute"
}
```

MUST NOT assume the Resource is available at:

```text
/api/v2/status/resources/pioneer-compute
```

or that job submission is available at:

```text
/api/v2/compute/job/pioneer-compute
```

The canonical Resource URI and applicable operation entry points MUST instead be obtained from advertised URIs or hypermedia links.

## 5. Resource Classification

The `resource_type` property identifies the semantic type of the Resource.

The V2 `resource_type` property is structurally a string.

Its value MUST be an IRI Resource Type URN conforming to the DOE-IRI URN specification.

For example:

```json
{
  "resource_type": "urn:doe-iri:resource:compute:system"
}
```

Resource types are not defined as a closed OpenAPI enumeration.

This allows the Resource taxonomy to evolve through the DOE-IRI URN Registry without requiring an OpenAPI schema revision whenever a new Resource subtype is introduced.

### 5.1 Resource Type Namespace

Shared Resource Type URNs are rooted at:

```text
urn:doe-iri:resource
```

Examples include:

```text
urn:doe-iri:resource:website
urn:doe-iri:resource:service
urn:doe-iri:resource:compute
urn:doe-iri:resource:system
urn:doe-iri:resource:storage
urn:doe-iri:resource:network
urn:doe-iri:resource:unknown
```

More-specific registered types narrow these classifications.

Examples include:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu

urn:doe-iri:resource:storage:system
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:storage:filesystem:scratch

urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

### 5.2 Hierarchical Semantics

Each additional semantic segment in a Resource Type URN narrows the meaning of the Resource type.

For example:

```text
urn:doe-iri:resource:storage
        │
        └── filesystem
              │
              └── scratch
```

corresponds to:

```text
urn:doe-iri:resource:storage

urn:doe-iri:resource:storage:filesystem

urn:doe-iri:resource:storage:filesystem:scratch
```

A Resource classified as:

```text
urn:doe-iri:resource:storage:filesystem:scratch
```

is therefore also within the semantic hierarchy rooted at:

```text
urn:doe-iri:resource:storage:filesystem
```

and:

```text
urn:doe-iri:resource:storage
```

when those intermediate hierarchy levels are registered and semantically defined.

### 5.3 Producer Requirements

A producer SHOULD emit the most specific registered Resource Type URN that accurately describes the Resource.

For example, a scratch filesystem SHOULD normally use:

```text
urn:doe-iri:resource:storage:filesystem:scratch
```

rather than only:

```text
urn:doe-iri:resource:storage
```

when the more-specific classification is known and appropriate to disclose.

A producer MAY emit a recognized parent Resource Type when:

- a more-specific subtype is unavailable;
- a more-specific subtype is not applicable;
- disclosure of the subtype is restricted;
- the implementation intentionally exposes only a broader classification.

A producer MUST NOT invent an unregistered shared Resource Type URN and present it as a canonical DOE-IRI type.

Facility- or project-specific Resource types MUST use the DOE-IRI delegated-extension mechanism when an appropriate delegated scope exists.

### 5.4 Consumer Requirements

A generic client MUST NOT reject an otherwise syntactically valid IRI Resource Type URN solely because the specific type is not known to the client's local implementation.

A hierarchy-aware client SHOULD fall back to the nearest recognized semantic parent.

For example, if a client does not understand:

```text
urn:doe-iri:resource:storage:filesystem:scratch
```

but understands:

```text
urn:doe-iri:resource:storage:filesystem
```

it SHOULD process the Resource using its known filesystem behavior where that behavior is applicable.

If the client understands only:

```text
urn:doe-iri:resource:storage
```

it MAY fall back to generic storage behavior.

A client that does not implement DOE-IRI hierarchy parsing MUST treat an unfamiliar Resource Type URN as an opaque semantic identifier.

### 5.5 Hierarchy Matching

Hierarchy-aware matching MUST operate on complete colon-delimited semantic segments.

For example:

```text
urn:doe-iri:resource:storage
```

is a semantic parent of:

```text
urn:doe-iri:resource:storage:filesystem:scratch
```

but:

```text
urn:doe-iri:resource:stor
```

is not a semantic parent.

Clients MUST NOT use arbitrary string-prefix comparison as a substitute for DOE-IRI hierarchy-aware matching.

### 5.6 Extension Resource Types

DOE-IRI extension Resource Type URNs use the explicit `ext` delegation form.

For example:

```text
urn:doe-iri:resource:compute:ext:nersc:fpga
```

An extension marker and authority code express delegation structure rather than additional shared semantic hierarchy.

For hierarchy-aware fallback, clients stop at the nearest recognized shared semantic parent before `ext`.

For example:

```text
urn:doe-iri:resource:compute:ext:nersc:fpga
```

may fall back to:

```text
urn:doe-iri:resource:compute
```

A producer claiming an assigned DOE-IRI extension MUST satisfy the applicable syntax, scope-authorization, and local-definition requirements of the DOE-IRI URN specification.

## 6. Current Status

The `current_status` property represents the current status reported for the Resource.

The IRI Status model defines the following status values:

```text
up
down
degraded
unknown
```

For example:

```json
{
  "current_status": "degraded"
}
```

`current_status` provides a current-state summary associated with the Resource.

It is distinct from Event history.

An Event records a Resource condition at the Event's `occurred_at` time, while `current_status` describes the current reported condition of the Resource representation.

The existence of:

```json
{
  "current_status": "up"
}
```

does not imply that:

- the Resource has never experienced an Incident;
- every operation associated with the Resource is currently usable;
- every dependent Resource is available;
- every endpoint associated with the Resource is reachable.

Clients requiring historical information SHOULD inspect applicable Event and Incident representations.

## 7. Site Association

Each Resource has one authoritative Site association under the current V2 contract.

The representation exposes this relationship through:

```text
site_uri
```

The registered IRI hypermedia relation is:

```text
iri:located-at
```

with canonical relation URI:

```text
https://iri.science/rels/located-at
```

Conceptually:

```text
Resource  -- iri:located-at -->  Site
   1                1
```

`iri:located-at` identifies the relatively stable physical and administrative Site associated with the Resource.

It MUST NOT be interpreted as asserting:

- current process placement;
- compute hosting;
- service reachability;
- operational health;
- current availability;
- ownership;
- live network routing.

The target Site representation MAY advertise:

```text
https://iri.science/profiles/facility/site
```

as its representation profile.

## 8. Capabilities and Type-Specific Behavior

### 8.1 Capabilities

The Resource representation exposes associated Capabilities through:

```text
capability_uris
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
Resource  -- iri:has-capability -->  Capability
   1                  0..*
```

A Capability identifies a capability associated with the Resource.

The existence of a Capability relationship MUST NOT itself be interpreted as:

- an authorization grant;
- an allocation;
- current availability;
- permission to invoke an operation;
- a guarantee that the Capability can currently be consumed.

### 8.2 Type-Specific Attributes

The `resource_type` value determines the semantic Resource class and MAY identify additional type-specific attributes defined by the applicable IRI registry specifications.

For example:

```json
{
  "resource_type":
    "urn:doe-iri:resource:storage:filesystem:scratch"
}
```

identifies the representation as a scratch-filesystem Resource and permits clients that understand that registered type to interpret applicable storage/filesystem-specific attributes.

A generic client MUST remain capable of processing the common Resource representation even when it does not understand the Resource's most-specific type.

### 8.3 Resource Type Does Not Define URLs

A Resource Type URN identifies what the Resource is.

It does not identify where related resources or operations are located.

For example:

```text
urn:doe-iri:resource:compute:system
```

does not imply that job submission is located at:

```text
/api/v2/compute/job/{resource_id}
```

The applicable operation MUST be discovered through an advertised operation relation when such a relation is available.

## 9. Hypermedia Representation

When represented using HAL, a Resource SHOULD advertise its identity, relationships, and applicable operation entry points through `_links`.

For example:

```json
{
  "id": "pioneer-compute",
  "name": "Pioneer Compute System",
  "last_modified": "2026-08-17T18:12:00Z",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "current_status": "up",

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/status/resources/pioneer-compute",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/status/resource"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:located-at": {
      "href":
        "https://api.example.org/api/v2/facility/sites/example-site",
      "title": "Example Facility Site",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/facility/site"
    },

    "iri:has-capability": [
      {
        "href":
          "https://api.example.org/api/v2/account/capabilities/pioneer-gpu",
        "title": "Pioneer GPU Capability",
        "type": "application/hal+json"
      }
    ],

    "iri:submit-job": {
      "href":
        "https://api.example.org/api/v2/compute/job/pioneer-compute"
    },

    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

In this representation:

- `resource_type` identifies **what the Resource is**;
- `self` identifies the Resource representation;
- `iri:located-at` identifies the associated Site;
- `iri:has-capability` identifies associated Capabilities;
- `iri:submit-job` identifies an applicable operation entry point;
- `service-desc` identifies a machine-readable service description defining how operations are invoked;
- `profile` identifies the semantic profile of a target representation.

These identifiers serve different purposes and MUST NOT be treated as interchangeable.

## 10. Relationship URIs and Operation Affordances

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
iri:located-at
```

expands to:

```text
https://iri.science/rels/located-at
```

and:

```text
iri:has-capability
```

expands to:

```text
https://iri.science/rels/has-capability
```

The applicable canonical relation documents define the normative semantics of those relationships.

This Resource profile MUST NOT redefine those link-relation semantics.

### 10.1 Operation Discovery

A Resource MAY advertise operation entry points applicable to that Resource.

For example, a Resource classified as:

```text
urn:doe-iri:resource:compute:system
```

may advertise:

```json
{
  "_links": {
    "iri:submit-job": {
      "href":
        "https://api.example.org/api/v2/compute/job/pioneer-compute"
    }
  }
}
```

The Resource Type URN and operation relation answer different questions:

```text
resource_type
    ↓
WHAT is this Resource?

urn:doe-iri:resource:compute:system


iri:submit-job
    ↓
WHAT operation is applicable and WHERE?


service-desc
    ↓
HOW is that operation invoked?
```

An operation link does not itself define:

- HTTP method;
- request body;
- response body;
- authentication;
- authorization;
- scheduling policy;
- operational success.

Those invocation semantics remain defined by the applicable machine-readable API contract, such as OpenAPI.

Clients MUST NOT infer an operation URI solely from `resource_type`.

## 11. Relationship to Existing URI Properties

The current V2 Resource schema defines:

```text
self_uri
site_uri
capability_uris
```

These properties expose Resource and related-resource URIs directly.

When the IRI HAL hypermedia model is used, the corresponding relationships SHOULD be represented through `_links`:

```text
self_uri
    ↓
_links.self

site_uri
    ↓
_links["iri:located-at"]

capability_uris
    ↓
_links["iri:has-capability"]
```

For example:

```json
{
  "self_uri":
    "https://api.example.org/api/v2/status/resources/pioneer-compute",

  "site_uri":
    "https://api.example.org/api/v2/facility/sites/example-site",

  "capability_uris": [
    "https://api.example.org/api/v2/account/capabilities/pioneer-gpu"
  ],

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/status/resources/pioneer-compute"
    },

    "iri:located-at": {
      "href":
        "https://api.example.org/api/v2/facility/sites/example-site"
    },

    "iri:has-capability": [
      {
        "href":
          "https://api.example.org/api/v2/account/capabilities/pioneer-gpu"
      }
    ]
  }
}
```

During the compatibility period:

1. Producers retain the required `self_uri`, `site_uri`, and `capability_uris` properties.
2. Producers MAY additionally expose corresponding HAL relationships.
3. Whenever `site_uri` and `_links["iri:located-at"]` are both present, the link `href` MUST exactly equal `site_uri`.
4. Whenever `capability_uris` and `_links["iri:has-capability"]` are both present, they MUST identify the same targets, disregarding order.
5. Consumers SHOULD prefer advertised hypermedia relations and MAY fall back to corresponding URI-valued properties.
6. Removing or changing existing URI properties requires a separate OpenAPI schema revision.
7. `self_uri` remains authoritative under the current OpenAPI contract until changed by an approved schema revision.

Clients implementing the HAL representation SHOULD use advertised `_links` for navigation rather than constructing URLs from identifiers or Resource Type URNs.

## 12. Media Type

This profile identifies the semantics of the Resource representation independently of a particular serialization.

When a Resource is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/status/resource
```

The profile URI does not replace the media type or Resource Type URN.

The three identifiers have distinct roles:

```text
application/hal+json
    ↓
HOW the representation is encoded

https://iri.science/profiles/status/resource
    ↓
WHAT semantic representation contract applies

urn:doe-iri:resource:storage:filesystem:scratch
    ↓
WHAT KIND of IRI Resource is represented
```

These identifiers MUST NOT be treated as interchangeable.

## 13. Static and Dynamic Semantics

A Resource representation may contain both relatively stable descriptive information and dynamic status information.

Relatively stable information typically includes:

```text
id
name
description
group
resource_type
site_uri
capability_uris
supported_endpoints
```

Dynamic information includes:

```text
current_status
last_modified
```

Relationships such as:

```text
iri:located-at
iri:has-capability
```

generally describe relatively stable topology or administrative association.

Their existence MUST NOT be interpreted as proof of current availability or operational health.

Operation affordances MAY be more dynamic.

The presence of an operation link indicates that the operation is applicable and discoverable in the current representation context.

It does not guarantee that invocation will succeed.

Clients SHOULD consult the current Resource representation before acting on an operation affordance rather than relying on cached, indexed, or previously observed links.

## 14. Authorization and Visibility

Authorization MAY affect information and relationships visible through a Resource representation.

A provider MAY omit:

- Capabilities;
- operation affordances;
- topology relationships;
- type-specific attributes;
- descriptive information;
- other optional links

when the requester is not authorized to discover that information, subject to requirements imposed by the applicable OpenAPI schema and relation definitions.

A producer MAY expose a broader parent Resource Type when disclosure of a more-specific subtype is intentionally restricted.

For example:

```text
urn:doe-iri:resource:storage
```

may be exposed instead of:

```text
urn:doe-iri:resource:storage:filesystem:scratch
```

when policy permits disclosure of the broad Resource class but not the more-specific subtype.

The absence of an operation link MUST NOT necessarily be interpreted as proof that the underlying Resource has no such operation.

It indicates only that the operation is not advertised in the current representation context.

Where legacy URI properties and corresponding HAL relationships are both returned, they MUST remain consistent.

## 15. Conformance

A representation conforms to the IRI Status Resource Profile when:

1. it conforms to the applicable IRI Facility API `Resource` schema;
2. its properties are interpreted according to the IRI Facility API and this profile;
3. `resource_type` is structurally represented as a string;
4. `resource_type` contains a Resource Type URN conforming to the DOE-IRI URN specification;
5. Resource Type URNs are interpreted according to the applicable DOE-IRI registry semantics;
6. unfamiliar but syntactically valid Resource Type URNs are not rejected solely because they are absent from local client code or generated models;
7. hierarchy-aware Resource Type matching operates on complete semantic segments;
8. clients use nearest-recognized-parent or opaque fallback behavior where appropriate;
9. Resource identifiers are treated as identifiers rather than URL templates;
10. Resource Type URNs are treated as semantic classifications rather than URL or operation templates;
11. `current_status` is distinguished from historical Event state;
12. the authoritative Site is discoverable through `site_uri` or `iri:located-at`;
13. associated Capabilities are discoverable through `capability_uris` or `iri:has-capability`;
14. IRI-specific link relations use the canonical IRI relation namespace;
15. representation profile URIs are not used as substitutes for Resource Type URNs or link-relation identifiers;
16. when both `site_uri` and `_links["iri:located-at"]` are present, they identify the same target;
17. when both `capability_uris` and `_links["iri:has-capability"]` are present, they identify the same targets;
18. applicable operation entry points are discovered through advertised links rather than inferred from Resource identifiers or Resource Type URNs;
19. clients are not required to infer or construct related-resource or operation URLs.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/status/resource
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, Resource Type URNs, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications, new registered Resource Type URNs, and backward-compatible semantic additions MAY retain the same profile URI.

Adding a new Resource Type URN to the DOE-IRI URN Registry does **not** require a new version of this Resource representation profile merely because the taxonomy has expanded.

Changes that materially alter the interpretation or processing semantics of the common Resource representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Status Resource Profile*