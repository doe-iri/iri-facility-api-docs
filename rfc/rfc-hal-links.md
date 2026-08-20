# RFC: HAL `_links` for the IRI Facility API

## Abstract

The DOE Integrated Research Infrastructure (IRI) requires APIs that can describe
heterogeneous resources across facilities, services, storage systems, compute
systems, networks, workflow engines, data-transfer services, and scientific user
environments.

This RFC defines an additive HAL `_links` convention for IRI 2.0
resource-oriented JSON representations. The convention makes related resources,
dynamic state resources, operation entry points, and topology relationships
explicit and navigable. It also defines migration of existing navigable
URI-valued properties to standard or registered DOE-IRI link relations and
advertises an initial job-submission affordance. It does not change the
production OpenAPI schemas.

## Status of This Memo

This document is a proposed IRI Facility API RFC. The key words **MUST**,
**MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as
described in BCP 14 when, and only when, they appear in all capitals. The
authoritative source for DOE-IRI resource-type and controlled-value URNs is
the [DOE-IRI URN Registry](../registry/urns/README.md). The
[DOE-IRI Link Relation Index](../registry/relations/README.md) is the
authoritative navigation index for registered `iri:*` names; each linked
definition is authoritative for that relation's complete semantics.

This document proposes an IRI Facility API extension and is intended for adoption
in the DOE IRI specification version 2.0 and reference implementations.

| Revision | Author | Date | Notes |
|---|---|---|---|
| 0.1 | ChatGPT | Jul 31, 2026 | Initial version from John’s dank prompt. |
| 0.2 | John MacAuley | Jul 31, 2026 | Revised based on initial thoughts. |
| 0.3 | John MacAuley | Aug 14, 2026 | Revising for consistency. |
| 0.4 | John MacAuley | Aug 14, 2026 | Added problem statement and layered hypermedia/service-description discovery model. |


## 1. Scope and Semantic Model

For an existing API `Resource` representation:

```text
resource_type identifies what the Resource is.
ordinary properties describe the representation.
_links identifies related resources, dynamic state resources, topology
       relationships, and applicable operation entry points.
link relations identify why a target is related or applicable.
OpenAPI defines how to invoke an operation.
```

This RFC covers HAL link objects, migration of URI-valued properties, standard
relations, registered DOE-IRI relations, topology relationships, discovery of
machine-readable service descriptions, and operations such as `iri:submit-job`.
It does not assign URNs or link-relation names, alter production OpenAPI v1 or
v2, define operational telemetry, or define other operation affordances.

The JSON below is registry-aligned HAL migration material: it uses canonical
registry URNs and illustrates representation shapes, rather than claiming to
be complete instances conformant with the current production OpenAPI. In
particular, migration from the current v2 `ResourceType` legacy enum is outside
this RFC and requires later OpenAPI work.

## 2. Problem Statement

IRI APIs describe heterogeneous resources implemented across independently
operated facilities and services. Those resources expose relationships to other
resources, capabilities, dynamic state, topology, and operation entry points.
Because facilities may implement these APIs using different internal routing
structures, clients cannot safely infer a target URI from a resource identifier
or resource type.

Without a standard hypermedia model, clients must instead rely on hard-coded
path construction, SDK-specific conventions, or out-of-band documentation.

### 2.1. Hand-Constructed URLs

IRI clients, workflow engines, and AI tools SHOULD NOT need advance knowledge of
how an individual facility structures its URLs. Depending on the resource and
API, a client may need to discover questions such as:

```text
Which related resource represents a filesystem?
Which resource exposes current state or capacity information?
Which incidents or events affect the resource?
Which mount relationship connects a compute resource to a filesystem?
Which operation entry point applies to the resource?
```

Requiring a client to derive those targets from identifiers and known path
templates couples the client to server-side routing conventions. A client that
discovers a storage resource, for example, SHOULD NOT need to construct a
filesystem API URL from resource identifiers when the representation can
advertise the relationship directly.

### 2.2. Operation Discovery

Different resource types may expose different operation entry points. For
example:

```text
A compute system may support job submission.
A filesystem may support file operations.
A storage resource may expose dynamic capacity state.
A network resource may expose topology relationships.
A data-transfer resource may expose transfer operations.
```

Without typed links, a client must infer applicable operations from static
documentation, resource type, SDK-specific logic, or facility-specific routing
knowledge.

An advertised operation relation identifies that an operation is applicable and
where its entry point is located. It does not define the HTTP method, request
body, response, error model, or security requirements. Those invocation
semantics remain the responsibility of the governing OpenAPI contract.

### 2.3. AI and MCP URL Speculation

AI agents and MCP-enabled clients SHOULD NOT speculate about API paths. For
example, an agent that discovers a compute resource SHOULD NOT guess that job
submission is located at:

```text
/api/v2/compute/jobs/{resource_id}
```

Instead, the current representation SHOULD advertise the applicable operation
entry point when it is available to that client:

```json
{
  "_links": {
    "iri:submit-job": {
      "href": "https://api.example.org/api/v2/compute/job/pioneer-compute"
    }
  }
}
```

This reduces path speculation and facility-specific routing knowledge by
allowing traversal to be based on information advertised by the current
representation.

RAG systems MAY index relation names and linked resource context to improve
discovery, but an agent MUST consult the current representation and governing
OpenAPI contract before invoking an operation. Indexed, cached, or previously
observed links do not prove current authorization, availability, applicability,
or permission.

## 3. HAL Links, Link Objects, Metadata, Arrays, and CURIEs

A HAL-enabled representation places relations in `_links`. Each relation value
is either one link object or an array of link objects. A link object MUST have
`href`; a producer MUST NOT emit `"href": null`. Relation-specific cardinality,
target classification, volatility, authorization behavior, and omission
semantics are defined by the applicable registered link-relation definition.

Use a singular object for a singular relation and an array for a plural
relation. A representation with its own canonical identity MUST expose `self`.
A transient `TaskSubmitResponse` has no such requirement. Its `monitor` link
identifies the Task resource used to monitor the asynchronous operation that
the response represents.

HAL link information has distinct semantic roles:

- The relation name identifies why the target is related or applicable.
- `href` identifies where the target is located.
- `type` MAY provide a media-type hint for the target representation.
- `profile` MAY identify the profile of the target representation.
- `title` MAY provide a human-readable label for the link.
- A `service-desc` relation MAY identify a machine-readable service description
  applicable to the link context, such as an OpenAPI description.

The HAL Link Object `profile` property and a DOE-IRI link-relation URI serve
different purposes. The HAL `profile` property identifies the profile of the
target representation. The DOE-IRI Link Relation Index and linked definitions
define the semantics of an `iri:*` relation itself. A producer MUST NOT use the
HAL `profile` property to redefine or replace the registered semantics of a
link relation.

RFC 6906 explicitly describes profiles as a mechanism for signaling additional 
semantics beyond those defined by the media type, and should be primarily treated
as identifiers.  A client must recognize a profile from the URI alone. The URI may 
be dereferenceable and provide human- or machine-readable documentation, and 
RFC 6906 recommends making it dereferenceable when clients may encounter unknown 
profiles, but the protocol does not require dereferencing.

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch filesystem",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/json",
      "title": "IRI Facility API OpenAPI description"
    }
  }
}
```

Similarly, `service-desc` is a link relation, not Link Object metadata. It can
identify the machine-readable contract that describes how API operations are
invoked, while the other advertised relations identify which resources or
operation entry points are relevant. A `service-desc` link does not redefine
those relations or grant authorization to invoke the described operations.

HAL CURIEs MAY abbreviate registered DOE-IRI relation identifiers. The
canonical IRI CURIE declaration is:

```json
{
  "_links": {
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

The template expands `iri:<relation>` to
`https://iri.science/rels/<relation>`. CURIE expansion does not assign or
redefine a relation; the Link Relation Index and linked definitions remain
authoritative.

## 4. Authoritative Relation Sources

Use standard Web Linking relations when their established semantics apply:

| Relation | Use |
|---|---|
| `self` | Canonical URI of the current representation. |
| `help` | Facility help or support portal. |
| `monitor` | Task resource used to monitor an asynchronous result. |
| `service-desc` | Machine-readable service description applicable to the context, such as an OpenAPI description. |

For every `iri:*` relation, a producer and consumer MUST use the exact
registered name in the Link Relation Index and the complete semantics in its
linked definition. Link relations are not DOE-IRI URNs, and this RFC does not
create another relation registry. Relevant registered topology relations, such
as `iri:provides-filesystem`, retain the meanings specified by their linked
definitions.

DOE-IRI custom link relation identifiers MUST use lowercase ASCII letters,
digits, and hyphens. Multiword relation identifiers MUST separate words with
a hyphen (`-`). DOE-IRI custom relation identifiers MUST NOT use camelCase,
PascalCase, underscores, or whitespace.

This rule does not apply to JSON property names, DOE-IRI URNs, OpenAPI
`operationId` values, API paths, programming-language symbols, or standard
registered Web Linking relations.

## 5. Legacy URI-Property Mapping

Mapping depends on the source representation's semantics, not merely on the
property spelling. For example, `Event.resource_uri`, `Incident.resource_uris`,
and `Site.resource_uris` map to three different relations.

| Source representation | Existing property | HAL relation | Form and semantic cardinality |
|---|---|---|---|
| Any representation with canonical identity | `self_uri` | `self` | Singular; exactly one canonical target. |
| `Resource` | `site_uri` | `iri:located-at` | Singular; exactly one under the required field contract. |
| `Facility` | `support_uri` | `help` | Singular when the optional, nullable URI is supplied (`0..1`). |
| `Facility` | `site_uris` | `iri:has-site` | Array; `0..*`. |
| `Event` | `incident_uri` | `iri:generated-by` | Singular; `0..1`. |
| `Incident` | `event_uris` | `iri:has-event` | Array; `0..*`. |
| `Event` | `resource_uri` | `iri:impacts` | Singular; exactly one under the required field contract. |
| `Incident` | `resource_uris` | `iri:may-impact` | Array; `0..*`. |
| `Site` | `resource_uris` | `iri:has-resource` | Array; `0..*`. |
| `ProjectAllocation` | `project_uri` | `iri:has-project` | Singular; exactly one under the required field contract. |
| `ProjectAllocation` | `capability_uri` | `iri:has-capability` | Singular; exactly one under the required field contract. |
| `Resource` | `capability_uris` | `iri:has-capability` | Array; `0..*`. |
| `UserAllocation` | `project_allocation_uri` | `iri:has-project-allocation` | Singular; exactly one under the required field contract. |
| `TaskSubmitResponse` | `task_uri` | `monitor` | Singular; exactly one under the required field contract. |

`Event.incident_uri` is required but nullable. A null value maps to an omitted
`iri:generated-by` relation, never a null `href`. `iri:has-capability` has one
general meaning: a Resource provides the Capability, while a
ProjectAllocation applies to it. For full source, target, cardinality, target
classification, visibility, and volatility rules, consult the registered
profile for each `iri:*` relation.

## 6. Operation Affordance: `iri:submit-job`

`iri:submit-job` is the registered provisional relation for the applicable
job-submission entry point of a Resource whose `resource_type` is
`urn:doe-iri:resource:compute:system`. It has cardinality `0..1`; the target
is an operation entry point, not an API resource.

The current operation is `POST /api/v2/compute/job/{resource_id}` with
`operationId: launchJob`. The link identifies where job submission is defined;
it does not specify the HTTP method or request body, grant permission,
guarantee schedulability, or replace the OpenAPI `JobSpec`, response, error,
or security contracts. The current `launchJob` operation returns `Job`.
Visibility MAY be filtered by authorization.

A representation MAY advertise a `service-desc` link to allow a client to
discover the machine-readable service description governing the operation.
When that target is an OpenAPI description, the operation relation identifies
which entry point is applicable and the OpenAPI description defines how to
invoke it.

## 7. OpenAPI 3.1 Schema

The following reusable components describe the HAL wire shape. The generic
schema permits a singular object or an array; relation definitions remain
authoritative for semantic cardinality. `curies` is permitted as an array of
`HalLink` objects. Standard relations such as `service-desc` require no
relation-specific schema property because they are represented as keys within
`HalLinks`.

```yaml
HalLink:
  type: object
  required:
    - href
  properties:
    href:
      type: string
      format: uri-reference
    templated:
      type: boolean
      default: false
    type:
      type: string
      description: Media-type hint for the target representation.
    deprecation:
      type: string
      format: uri
    name:
      type: string
    profile:
      type: string
      format: uri
      description: URI that identifies or hints at the profile of the target representation.
    title:
      type: string
      description: Human-readable label for the link.
    hreflang:
      type: string
  additionalProperties: true

HalLinkValue:
  oneOf:
    - $ref: '#/components/schemas/HalLink'
    - type: array
      items:
        $ref: '#/components/schemas/HalLink'

HalLinks:
  type: object
  additionalProperties:
    $ref: '#/components/schemas/HalLinkValue'
```

An existing representation adopts the components with this property fragment:

```yaml
_links:
  $ref: '#/components/schemas/HalLinks'
  readOnly: true
```

## 8. Compatibility and Migration

This is an additive migration; it does not modify current OpenAPI conformance.

1. Existing URI properties retain their current required and nullable rules
   until a later OpenAPI revision.
2. A producer MAY add the mapped HAL relation during the transition.
3. When both forms are present, their targets MUST agree: a scalar URI equals
   the link `href`; URI and link arrays name the same targets disregarding
   order.
4. A null or absent optional URI maps to an omitted relation, never a null
   `href`.
5. Consumers SHOULD prefer an advertised relation and MAY fall back to the
   legacy URI property.
6. Removing a URI property requires a subsequent OpenAPI change.
7. The existing `site_uri` / `iri:located-at` contract remains unchanged:
   while `site_uri` is returned, a supplied relation MUST have the same `href`
   and MUST NOT be independently hidden.

For relations backed by current required fields, exact-one is the semantic
cardinality after the relation is supplied or becomes the replacement
contract. `_links` remains optional during the additive transition.

## 9. Producer, Consumer, Authorization, and Security Rules

Producers:

- MUST include `self` on a HAL representation with canonical identity.
- MUST use standard relations where applicable and registered relations for
  every `iri:*` link.
- MUST enforce the mapping equivalence rules when retaining legacy fields.
- MAY advertise `service-desc` when a machine-readable service description is
  applicable to the represented resource or service context.
- MAY omit authorization-sensitive links where the relevant profile permits;
  an omission is not proof that the relationship or affordance is absent.
- MUST NOT expose credentials, tokens, secrets, private keys, or protected
  information in a link or its metadata.

Consumers:

- MUST tolerate unknown relations and missing optional links.
- SHOULD follow advertised links instead of constructing facility URLs when a
  suitable relation is present.
- MAY use an advertised `service-desc` link to discover the machine-readable
  service contract applicable to the context.
- MUST consult the applicable relation profile and governing OpenAPI contract
  before invoking an operation, and MUST NOT treat an operation link or
  `service-desc` link as authorization.
- MUST treat link targets as data and avoid automatically following arbitrary
  links from untrusted sources.

## 10. Examples

### 10.1 Storage-system Resource

```json
{
  "id": "pioneer-storage",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "self_uri": "/api/v2/status/resources/pioneer-storage",
  "site_uri": "/api/v2/facility/sites/pioneer",
  "capability_uris": [],
  "_links": {
    "self": { "href": "/api/v2/status/resources/pioneer-storage" },
    "iri:located-at": { "href": "/api/v2/facility/sites/pioneer" },
    "iri:provides-filesystem": [
      { "href": "/api/v2/status/resources/pioneer-scratch" }
    ]
  }
}
```

### 10.2 Event migration

```json
{
  "id": "event-001",
  "self_uri": "/api/v2/status/events/event-001",
  "resource_uri": "/api/v2/status/resources/pioneer-storage",
  "incident_uri": "/api/v2/status/incidents/incident-001",
  "_links": {
    "self": { "href": "/api/v2/status/events/event-001" },
    "iri:impacts": { "href": "/api/v2/status/resources/pioneer-storage" },
    "iri:generated-by": { "href": "/api/v2/status/incidents/incident-001" }
  }
}
```

### 10.3 Compute-system job submission and task monitoring

The first object advertises the `launchJob` entry point, whose current OpenAPI
response is `Job`. The second, independent object illustrates a
`TaskSubmitResponse` for an asynchronous filesystem operation; it is not a
`launchJob` response. Its `monitor` link identifies the Task to monitor.

```json
[
  {
    "id": "pioneer-compute",
    "resource_type": "urn:doe-iri:resource:compute:system",
    "self_uri": "/api/v2/status/resources/pioneer-compute",
    "site_uri": "/api/v2/facility/sites/pioneer",
    "capability_uris": [],
    "_links": {
      "self": { "href": "/api/v2/status/resources/pioneer-compute" },
      "iri:submit-job": { "href": "/api/v2/compute/job/pioneer-compute" },
      "service-desc": {
        "href": "/openapi.json",
        "type": "application/json",
        "title": "IRI Facility API OpenAPI description"
      }
    }
  },
  {
    "task_id": "task-001",
    "task_uri": "/api/v2/task/task-001",
    "_links": {
      "monitor": { "href": "/api/v2/task/task-001" }
    }
  }
]
```

### 10.4 Topology relationship with target profile and service description

The following example illustrates the layered discovery model. It assumes that
`iri:has-mount` is a registered DOE-IRI relation whose definition permits the
source resource to link to a resource representing a mount relationship. The HAL
`profile` property describes the target representation; it does not define the
semantics of `iri:has-mount` itself.  

RFC 6906 explicitly describes profiles as a mechanism for signaling additional 
semantics beyond those defined by the media type, and should be primarily treated
as identifiers.  A client must recognize a profile from the URI alone. The URI may 
be dereferenceable and provide human- or machine-readable documentation, and 
RFC 6906 recommends making it dereferenceable when clients may encounter unknown 
profiles, but the protocol does not require dereferencing.

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch filesystem",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/json",
      "title": "IRI Facility API OpenAPI description"
    }
  }
}
```

A client can interpret the representation in layers: `iri:has-mount` identifies
why the target is relevant, `href` identifies where the relationship resource
is located, `type` and `profile` provide hints about the target representation,
and `service-desc` identifies a machine-readable description of the service
context. The governing OpenAPI description remains authoritative for operation
invocation semantics.

| Field           | Meaning                                                                     |
| --------------- | --------------------------------------------------------------------------- |
| `iri:has-mount` | **What relationship exists**: the current resource has a mount relationship.|
| `href`          | **Where to get the target resource** representing that relationship.        |
| `type`          | **Serialization/media type expected** when retrieving it: HAL JSON.         |
| `profile`       | **The more-specific semantic contract that HAL resource follows**.          |
| `title`         | A human-readable description for the relationship.                          |


## 11. References

1. RFC 2119 and RFC 8174, requirements-language conventions.
2. RFC 8288, *Web Linking*.
3. RFC 8631, *Link Relation Types for Web Services*.
4. JSON Hypertext Application Language, `draft-kelly-json-hal`.
5. OpenAPI Specification 3.1.
6. [DOE-IRI Link Relation Index](../registry/relations/README.md).
7. [IRI Facility API OpenAPI v2](../specification-v2/openapi/all_spec_v2.yaml).
