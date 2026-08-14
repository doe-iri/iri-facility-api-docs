# RFC: HAL `_links` for IRI 2.0

---

**Status:** Draft / Proposed  
**Target API Version:** IRI Facility API 2.0  
**Related RFCs:**   
RFC: IRI URN Structure and Registry  
RFC: Type-Specific Attributes for IRI Resource Objects  
RFC: Separating ResourceDefinition from ResourceState in the IRI Facility API  
RFC: Facility Physical and Logical Topology API Using HAL Links

---

Abstract

This RFC defines the use of HAL `_links` in IRI 2.0 JSON representations for modelling relationships between resource descriptions and resource state \[12\], both physical and logical relationships between resources \[13\], and to allow for URL discovery \[14\] in support of more friendly agentic workflow support.

The goal of URL discovery is to reduce client dependence on hand-constructed URLs, hard-coded endpoint paths, and out-of-band knowledge of which operations apply to a given IRI resource. Instead, resource representations SHOULD expose typed link relations that identify related resources, dynamic state resources, operation entry points, service descriptions, and topology relationships.

This RFC is complementary to the separate `ResourceDefinition` / `ResourceState` separation RFC \[12\]. That RFC defines the architectural separation between stable resource descriptions and dynamic operational state. This RFC defines how HAL `_links` support that model by allowing stable resource descriptions to link to current state, capacity, incidents, events, metrics, filesystem APIs, job APIs, and relationship resources.

The proposal defines a three-layer semantic contract:

1. HAL `_links` identify where a client can navigate.  
2. Relation and profile documentation define what each link means.  
3. OpenAPI and JSON Schema define how to invoke operation targets safely.

This model supports traditional clients, SDKs, workflow engines, MCP tools, and AI-assisted orchestration systems by making resource-specific affordances discoverable from the resource representation itself.

## **Status of This Memo**

This document is a proposed IRI Facility API extension and is intended for adoption within the DOE IRI specification version 2.0 and reference implementations.

| Revision | Author | Date | Notes |
| :---- | :---- | :---- | :---- |
| 0.1 | ChatGPT | Jul 31, 2026 | Initial version from John’s dank prompt. |
| 0.2 | John MacAuley | Jul 31, 2026 | Revised based on initial thoughts. |
| 0.3 | John MacAuley | Aug 14, 2026 | Revising for consistency. |

# 1\. Introduction

The DOE Integrated Research Infrastructure requires APIs that can describe heterogeneous resources across facilities, services, storage systems, compute systems, networks, workflow engines, data-transfer services, and scientific user environments.

IRI clients SHOULD NOT need to know in advance how every facility structures every URL. A client that discovers a compute resource SHOULD NOT need to guess which path is used for job submission. A client that discovers a storage resource SHOULD NOT need to construct a filesystem API URL from resource identifiers. An AI or MCP agent SHOULD NOT need to infer operational paths from static documentation when those paths can be advertised directly by the resource representation.

This RFC proposes that IRI 2.0 resource-oriented JSON representations include HAL-style `_links` to make related resources, dynamic state resources, operation entry points, and topology relationships explicit and navigable.

This RFC does not define the separation of `ResourceDefinition` and `ResourceState`; that separation is handled by a companion RFC \[12\]. However, this RFC provides the link model needed to make that separation operational.

For example, a `ResourceDefinition` can link to its dynamic `ResourceState`:

```json
{
  "id": "orion-scratch",
  "name": "Orion Scratch Filesystem",
  "resource_type": "urn:doe-iri:resource:storage:filesystem:scratch",
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    },
    "iri:capacity": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity"
    }
  }
}
```

The separation RFC \[12\] defines what belongs in the definition versus the state. This RFC defines how the definition points to the state and other related resources.

# 2\. Requirements Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

# 3\. Problem Statement

IRI resources expose relationships, capabilities, dynamic state, and operation entry points. Without a standard hypermedia model, clients often need to rely on hard-coded path construction or out-of-band documentation.

This creates several problems.

## 3.1. Hand-Constructed URLs

Clients, workflow engines, and AI tools may need to construct URLs manually from known path templates.  For example, given a storage resource, a client may need out-of-band knowledge to determine:

```
Which endpoint exposes filesystem operations?
Which endpoint exposes current capacity?
Which endpoint exposes incidents?
Which endpoint exposes events?
Which endpoint exposes mounted access from a compute resource?
```

This couples clients to server-side routing conventions.

## 3.2. Operation Discovery

Different resource types support different operations.

Examples:

```
A compute system may support job submission.
A filesystem may support file operations.
A storage resource may expose capacity state.
A network resource may expose topology relationships.
A data-transfer resource may expose transfer operations.
```

Without typed links, a client must infer available operations from documentation, resource type, or SDK-specific logic.

## 3.3. AI and MCP URL Speculation

AI systems and MCP servers SHOULD NOT speculate about API paths.  For example, an agent SHOULD NOT guess that job submission for a resource is located at:

```
/api/v2/compute/jobs/{resource_id}
```

Instead, the resource SHOULD advertise the applicable operation entry point:

```json
{
  "_links": {
    "iri:jobApi": {
      "href": "https://api.example.org/api/v2/compute/resources/frontier/jobs"
    }
  }
}
```

This makes tool selection and traversal more deterministic.

## 3.4. ResourceDefinition and ResourceState Navigation

The companion ResourceDefinition / ResourceState RFC \[12\] defines how stable resource descriptions are separated from dynamic operational state.

This RFC does not justify or redefine that separation. It defines the link mechanism that allows a stable resource description to reference dynamic state resources.

For example:

```json
{
  "_links": {
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    },
    "iri:capacity": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity"
    },
    "iri:events": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/events?resource_id=orion-scratch"
    },
    "iri:incidents": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/incidents?resource_id=orion-scratch"
    }
  }
}
```

## 3.5. Relationship Modeling

IRI needs to model physical and logical relationships, including:

```
connectedTo
locatedAt
providesFilesystem 
providesBlock 
providesObject 
hasMount 
mountedOn 
attachedTo 
hasNode 
hasCPU 
hasGPU
hostedOn 
accessesMount
```

A standard `_links` model allows these relationships to be represented consistently and navigated by clients, SDKs, MCP tools, and AI systems.

# 4\. Goals

This RFC has the following goals:

1. Define a common HAL `_links` convention for IRI 2.0 resource-oriented JSON representations.  
2. Reduce the need for clients to hand-construct URLs.  
3. Allow resources to advertise applicable operation entry points.  
4. Support navigation from `ResourceDefinition` to `ResourceState` as defined by the companion RFC.  
5. Support physical and logical topology relationship modeling.  
6. Provide a consistent traversal model for clients, SDKs, MCP tools, and AI agents.  
7. Support RAG indexing of stable resource definitions by allowing links to dynamic resources to be represented explicitly.  
8. Preserve server-side freedom to evolve URL structures.  
9. Support facility-local extension relations without namespace collisions.  
10. Provide a migration path from legacy URI fields to HAL links.

# 5\. Non-Goals

This RFC does not:

1. Define the `ResourceDefinition` / `ResourceState` separation.  
2. Justify which fields belong in `ResourceDefinition` versus `ResourceState`.  
3. Require every IRI response to use HAL.  
4. Replace OpenAPI.  
5. Define every possible IRI link relation.  
6. Define every possible resource relationship type.  
7. Define a complete topology ontology.  
8. Require clients to follow every link.  
9. Require dynamic dereferencing of schema or profile documents at runtime.  
10. Define authorization policy for all link targets.  
11. Require all facilities to expose identical operation endpoints.  
12. Remove existing URI fields immediately.

# 6\. Scope of HAL Usage

## 6.1. Resource-Oriented JSON Representations

IRI 2.0 resource-oriented JSON representations SHOULD support HAL-compatible `_links`.

This includes, but is not limited to:

```
ResourceDefinition
ResourceState
ResourceCapacityState
ResourceRelationship
Facility
Site
Capability
Incident
Event
```

## 6.2. Specialized Representations

Not every response needs to be HAL.

The following MAY use other media types or representation formats:

```
Problem Details
OpenAPI documents
binary file downloads
event streams
metrics streams
logs
bulk data transfer payloads
non-JSON representations
```

When a response is represented as HAL JSON, the media type SHOULD be:

```
application/hal+json
```

An implementation MAY support content negotiation between `application/json` and `application/hal+json` during migration.

# 7\. Architectural Model

This RFC defines a three-layer semantic contract.

## 7.1. Layer 1: HAL `_links` — Where Can I Go?

The `_links` object identifies related resources, state objects, operation entry points, documentation, and topology relationships.

Example:

```json
{
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/resource-definitions/frontier"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/frontier"
    },
    "iri:jobApi": {
      "href": "https://api.example.org/api/v2/compute/resources/frontier/jobs"
    }
  }
}
```

HAL tells the client where to navigate. HAL does not, by itself, define the complete invocation contract for unsafe or payload-bearing operations.

## 7.2. Layer 2: Relation and Profile Documentation — What Does It Mean?

Each IRI-specific link relation SHOULD have documentation that defines:

```
semantic meaning
source representation type
target representation type
cardinality
whether the target is static or dynamic
whether authorization affects visibility
whether the target represents a resource, state object, operation entry point, or relationship resource
```

Where additional schema or semantic documentation is useful, link objects SHOULD include a `profile` URI.

Example:

```json
{
  "iri:capacity": {
    "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity",
    "profile": "https://iri.science/profiles/resource-capacity-state"
  }
}
```

## 7.3. Layer 3: OpenAPI and JSON Schema — How Do I Use It?

When a link target represents an operation entry point, the operation MUST be described by OpenAPI or equivalent machine-readable service description.

Examples include:

```
job submission
file upload
file deletion
reservation creation
workflow launch
state mutation
administrative action
```

The link target documentation SHOULD define:

```
allowed HTTP methods
required headers
request schema
response schema
authorization requirements
idempotency behavior
error responses
rate limits
side effects
```

The registered `service-desc` link relation SHOULD be used when linking to machine-readable API descriptions.

Example:

```json
{
  "_links": {
    "iri:jobApi": {
      "href": "https://api.example.org/api/v2/compute/resources/frontier/jobs",
      "profile": "https://iri.science/profiles/job-api"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

# 8\. HAL Schema Requirements

## 8.1. HalLink

IRI implementations SHOULD support the following HAL link schema.

```
HalLink:
  type: object
  required:
    - href
  properties:
    href:
      type: string
      format: uri-reference
      description: Link target. May be absolute or relative.
    templated:
      type: boolean
      default: false
      description: Whether href is a URI template.
    type:
      type: string
      description: Expected media type of the target representation.
    deprecation:
      type: string
      format: uri
      description: URI documenting deprecation of the link target or relation.
    name:
      type: string
      description: Secondary key for selecting among links with the same relation.
    profile:
      type: string
      format: uri
      description: URI identifying semantic or schema profile for the target.
    title:
      type: string
      description: Human-readable link title.
    hreflang:
      type: string
      description: Language of the target resource.
  additionalProperties: true
```

The `href` property is REQUIRED.

IRI-specific extension properties MAY be added, but clients MUST NOT require non-standard link properties for basic navigation unless the applicable relation profile explicitly requires them.

## 8.2. HalLinks

```
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

A relation MAY resolve to a single link or an array of links.

## 8.3. CURIEs

IRI-specific relations SHOULD use HAL CURIEs.

Example:

```json
{
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    }
  }
}
```

The expanded CURIE URI SHOULD provide human-readable documentation and MAY provide machine-readable documentation for the relation.

# 9\. Link Relation Naming

## 9.1. Registered Relations

Registered link relations SHOULD be used where applicable.

Examples:

```
self
service-desc
service-doc
describedby
collection
item
next
prev
```

## 9.2. IRI-Specific Relations

IRI-specific relations SHOULD use the `iri:` CURIE prefix.

Recommended naming convention:

```
lowerCamelCase
```

Examples:

```
iri:state
iri:definition
iri:capacity
iri:events
iri:incidents
iri:metrics
iri:facility
iri:site
iri:jobApi
iri:filesystemApi
iri:connectedTo
iri:hasDirectConnection
iri:hasRoutedConnection
iri:providesFilesystem
iri:hasMountedFilesystem
iri:relationship
iri:source
iri:target
```

The IRI specification SHOULD NOT mix naming styles such as `connected-to`, `connectedTo`, and `connected_to` for the same semantic relation.

## **9.3. Relation Registry Requirements**

Each standard IRI relation SHOULD be registered in an IRI link relation registry.

A registry entry SHOULD include:

| Field | Description |
| ----- | ----- |
| Relation | Compact relation name, such as `iri:state`. |
| Expanded URI | Full documentation URI. |
| Description | Human-readable meaning. |
| Source type | Expected source representation type. |
| Target type | Expected target representation type. |
| Cardinality | Single, array, or either. |
| Static or dynamic | Whether the target is stable or dynamic. |
| Operation or resource | Whether the target is an operation entry point or a retrievable resource. |
| Authorization sensitivity | Whether visibility may depend on user, project, or facility context. |
| Profile | Optional profile URI. |
| Status | Active, experimental, deprecated, or replaced. |
| Replacement | Replacement relation if deprecated. |

# 10\. Required and Recommended Relations

## 10.1. Required for HAL-Enabled Representations

Every HAL-enabled representation MUST include:

| Relation | Target | Meaning |
| ----- | ----- | ----- |
| `self` | Current representation | Canonical URI for the representation. |

## 10.2. Recommended for ResourceDefinition

The ResourceDefinition / ResourceState separation is defined in a companion RFC. When a `ResourceDefinition` supports HAL and dynamic state is available, it SHOULD include:

| Relation | Target | Meaning |
| ----- | ----- | ----- |
| `iri:state` | `ResourceState` | Current or recent dynamic state for this resource. |

A `ResourceDefinition` SHOULD also include the following where applicable:

| Relation | Target | Meaning |
| ----- | ----- | ----- |
| `iri:facility` | `Facility` | Facility responsible for the resource. |
| `iri:site` | `Site` | Site where the resource is located. |
| `service-desc` | OpenAPI or service description | Machine-readable service description. |
| `service-doc` | Human-readable documentation | Human-readable API or service documentation. |

## 10.3. Dynamic State Relations

A `ResourceDefinition` or `ResourceState` MAY include:

| Relation | Target | Meaning |
| ----- | ----- | ----- |
| `iri:capacity` | `ResourceCapacityState` | Current or recent capacity information. |
| `iri:metrics` | Metrics endpoint or resource | Current or historical metrics. |
| `iri:events` | Event collection | Events associated with the resource. |
| `iri:incidents` | Incident collection | Incidents affecting the resource. |
| `iri:health` | Health state | Health details beyond summary status. |

## 10.4. Operation Entry Relations

A resource MAY include operation links where the operation is applicable.

| Relation | Source | Target | Meaning |
| ----- | ----- | ----- | ----- |
| `iri:jobApi` | Compute resource | Job API entry point | Submit, inspect, or manage jobs. |
| `iri:filesystemApi` | Filesystem or storage resource | Filesystem API entry point | Perform filesystem operations. |
| `iri:reservationApi` | Allocatable resource | Reservation API entry point | Create or inspect reservations. |
| `iri:transferApi` | Data-transfer resource | Transfer API entry point | Initiate or inspect data transfers. |

Operation links MUST be accompanied by sufficient documentation through `profile`, `service-desc`, OpenAPI, or relation documentation.

## 10.5. Topology and Relationship Relations

A resource MAY include topology or logical relationship links.

| Relation | Meaning |
| ----- | ----- |
| `iri:connectedTo` | Resource has a general connection to another resource. |
| `iri:hasDirectConnection` | Resource has a direct physical or logical connection to another resource. |
| `iri:hasRoutedConnection` | Resource can reach another resource through a routed path. |
| `iri:providesFilesystem` | Storage system provides a filesystem resource. |
| `iri:hasMountedFilesystem` | Compute or execution environment has mounted access to a filesystem. |
| `iri:relationship` | Link to a first-class relationship resource. |

# 11\. Support for ResourceDefinition and ResourceState

The companion ResourceDefinition / ResourceState RFC defines the architectural separation between stable resource descriptions and dynamic operational state.

This RFC only defines how HAL links support traversal between those representations.

## 11.1. ResourceDefinition Link Example

A `ResourceDefinition` MAY link to dynamic state resources:

```json
{
  "id": "orion-scratch",
  "name": "Orion Scratch Filesystem",
  "resource_type": "urn:doe-iri:resource:storage:filesystem:scratch",
  "attributes": {
    "filesystem_technology": "lustre",
    "namespace_root": "/lustre/orion",
    "persistence_class": "scratch"
  },
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "self": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
      "profile": "https://iri.science/profiles/resource-state"
    },
    "iri:capacity": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity",
      "profile": "https://iri.science/profiles/resource-capacity-state"
    },
    "iri:events": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/events"
    },
    "iri:incidents": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/incidents"
    }
  }
}
```

## 11.2. ResourceState Link Example

A `ResourceState` MAY link back to the `ResourceDefinition`:

```json
{
  "resource_id": "orion-scratch",
  "observed_at": "2026-07-31T21:00:00Z",
  "status": "up",
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    },
    "iri:definition": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    },
    "iri:capacity": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity"
    }
  }
}
```

The detailed schema and field classification rules for `ResourceDefinition` and `ResourceState` are out of scope for this RFC.

# 12\. Capacity Link Example

A `ResourceDefinition` MAY link to capacity state:

```json
{
  "_links": {
    "iri:capacity": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity",
      "title": "Current capacity state for Orion Scratch",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-capacity-state"
    }
  }
}
```

The target MAY look like:

```json
{
  "resource_id": "orion-scratch",
  "resource_type": "urn:doe-iri:resource:storage:filesystem:scratch",
  "observed_at": "2026-07-31T21:00:00Z",
  "state_valid_until": "2026-07-31T21:05:00Z",
  "capacity": {
    "total_bytes": "679000000000000000",
    "available_bytes": "600000000000000000",
    "used_bytes": "79000000000000000"
  },
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity"
    },
    "iri:definition": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    }
  }
}
```

Byte values SHOULD be represented as decimal integer strings to avoid precision loss in clients whose JSON number handling cannot safely represent large integers.

# 13\. ResourceRelationship

## 13.1. Purpose

Some relationships have meaningful attributes of their own.

Examples:

```
mount path
access mode
visibility
filesystem semantics
bandwidth
latency
directionality
routing policy
administrative domain
lifecycle state
authorization scope
```

These values are not simply properties of the source resource or the target resource. They are properties of the relationship between them.

## 13.2. Preferred Modeling Rule

HAL `_links` SHOULD be used for navigation.

A first-class `ResourceRelationship` object SHOULD be used when the relationship has meaningful attributes, lifecycle, state, authorization rules, provenance, or independent query value.

Inline link metadata MAY be used only for small, stable, non-authoritative hints.

## 13.3. Relationship Link Example

From a compute resource:

```json
{
  "_links": {
    "iri:hasMountedFilesystem": {
      "href": "https://api.example.org/api/v2/resource-relationships/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch filesystem",
      "profile": "https://iri.science/profiles/mounted-filesystem-relationship"
    }
  }
}
```

Target relationship resource:

```json
{
  "id": "frontier-orion-scratch-mount",
  "relationship_type": "urn:doe-iri:relationship:has-mounted-filesystem",
  "source_resource_id": "frontier",
  "target_resource_id": "orion-scratch",
  "attributes": {
    "mount_path": "/lustre/orion",
    "access_mode": "read-write",
    "visibility": "compute-nodes",
    "filesystem_semantics": "posix",
    "intended_use": "scratch"
  },
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/resource-relationships/frontier-orion-scratch-mount"
    },
    "iri:source": {
      "href": "https://api.example.org/api/v2/resource-definitions/frontier"
    },
    "iri:target": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    }
  }
}
```

## 13.4. Inline Link Metadata

Inline metadata MAY be used for simple stable hints.

Example:

```json
{
  "_links": {
    "iri:hasMountedFilesystem": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch",
      "title": "Orion scratch filesystem",
      "profile": "https://iri.science/profiles/mounted-filesystem",
      "mount_path": "/lustre/orion",
      "access_mode": "read-write"
    }
  }
}
```

Clients SHOULD NOT assume that inline relationship metadata is complete or authoritative unless the relation profile explicitly states that it is.

# 14\. Operation Entry Points

A HAL link MAY identify an operation entry point.

Examples:

```json
{
  "_links": {
    "iri:jobApi": {
      "href": "https://api.example.org/api/v2/compute/resources/frontier/jobs",
      "profile": "https://iri.science/profiles/job-api",
      "type": "application/hal+json",
      "title": "Job operations for Frontier"
    },
    "iri:filesystemApi": {
      "href": "https://api.example.org/api/v2/filesystems/orion-scratch",
      "profile": "https://iri.science/profiles/filesystem-api",
      "type": "application/hal+json",
      "title": "Filesystem operations for Orion Scratch"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

A link to an operation entry point MUST NOT be interpreted as permission to perform the operation.

Authorization, request validation, policy checks, and audit requirements still apply.

# 15\. AI, RAG, and MCP Usage Pattern

This RFC supports AI-assisted workflow systems by making traversal targets explicit.

## 15.1. Static Discovery Query

User request:

```
Which resources provide filesystems?
```

Expected AI behavior:

1. Search indexed resource descriptions.  
2. Identify resources with `iri:providesFilesystem`, `iri:filesystemApi`, or storage-filesystem resource types.  
3. Answer from stable resource descriptions.  
4. Do not call dynamic state endpoints unless current availability is requested.

## 15.2. Dynamic State Query

User request:

```
How much space is available on Orion Scratch right now?
```

Expected AI behavior:

1. Retrieve the indexed description for `orion-scratch`.  
2. Follow `_links.iri:capacity`.  
3. Retrieve capacity state.  
4. Answer using `available_bytes` and `observed_at`.

## 15.3. Operation Query

User request:

```
Submit this workflow to Frontier.
```

Expected AI behavior:

1. Retrieve the description for Frontier.  
2. Locate `_links.iri:jobApi`.  
3. Retrieve or consult `service-desc` / OpenAPI.  
4. Validate required payload and authorization.  
5. Invoke the operation through an MCP tool or API client.

## 15.4. Topology Query

User request:

```
Can Frontier write output to Orion Scratch?
```

Expected AI behavior:

1. Retrieve the description for Frontier.  
2. Follow or inspect `iri:hasMountedFilesystem`.  
3. Retrieve the relationship resource if present.  
4. Confirm mount path, access mode, and visibility.  
5. Retrieve current state only if the user asks whether the filesystem is currently available.

# 16\. Producer Requirements

An IRI producer that supports this RFC:

1. MUST include `_links` in HAL-enabled resource-oriented representations.  
2. MUST include `self` in every HAL-enabled resource representation.  
3. SHOULD include `iri:state` in `ResourceDefinition` representations where dynamic state is available.  
4. SHOULD use registered link relations where applicable.  
5. SHOULD use IRI CURIE relations for IRI-specific semantics.  
6. SHOULD publish relation documentation for every standard or facility-local relation.  
7. SHOULD include `service-desc` where operation links require machine-readable invocation details.  
8. SHOULD use `ResourceRelationship` for metadata-rich relationships.  
9. SHOULD include `observed_at` or equivalent freshness metadata in dynamic state representations.  
10. MUST NOT expose credentials, secrets, access tokens, private keys, or protected information through links or link metadata.  
11. MUST apply authorization policy before exposing sensitive links.  
12. SHOULD document which links may be omitted due to authorization or facility policy.

# 17\. Consumer Requirements

An IRI consumer that supports this RFC:

1. MUST tolerate unknown link relations.  
2. MUST tolerate missing optional links.  
3. MUST NOT assume that a missing link proves that a relationship or capability does not exist.  
4. SHOULD use links instead of constructing URLs when an appropriate relation is available.  
5. SHOULD inspect `profile`, `type`, and relation documentation before invoking operation links.  
6. SHOULD treat dynamic state links as time-sensitive.  
7. SHOULD inspect `observed_at` or equivalent freshness metadata before using dynamic state values.  
8. MUST NOT treat the presence of an operation link as authorization to perform the operation.  
9. SHOULD ignore inline link metadata it does not understand.  
10. SHOULD prefer first-class `ResourceRelationship` resources for authoritative relationship attributes where available.

# 18\. Authorization and Link Visibility

Link visibility MAY depend on:

```
authenticated identity
project context
facility policy
resource sensitivity
operation authorization
network security policy
incident status
maintenance mode
```

A producer MAY omit links that the caller is not authorized to see.

A consumer MUST NOT assume that an omitted link means the relationship, operation, or state resource does not exist.

If appropriate, a producer MAY include a redacted or limited link relation that points to documentation explaining access requirements.

# 19\. Caching and Freshness

This RFC does not define the caching rules for `ResourceDefinition` or `ResourceState`; those rules are addressed by the companion separation RFC.

However, HAL links SHOULD preserve enough information for clients to reason about freshness expectations.

For dynamic link targets, producers SHOULD include freshness metadata in the target representation, such as:

```
observed_at
state_valid_until
ETag
Last-Modified
Cache-Control
```

Clients SHOULD treat dynamic state targets as time-sensitive unless the target representation states otherwise.

# 20\. Security Considerations

HAL links can expose information about:

```
resource topology
operation entry points
filesystem access
network connectivity
incident endpoints
metrics endpoints
facility structure
authorization-sensitive capabilities
```

Implementations MUST apply authorization and redaction policies before returning HAL links.

Implementations SHOULD avoid exposing internal-only topology, hostnames, administrative endpoints, or sensitive operational paths to unauthorized users.

Clients MUST treat link targets as data, not executable instructions.

Clients SHOULD NOT automatically follow arbitrary links from untrusted sources.

Operation links MUST still enforce authentication, authorization, validation, policy checks, and audit logging.

A link relation MUST NOT be used as the sole basis for an access-control decision.

# 21\. Migration Strategy

## 21.1. Phase 1: Add `_links` Alongside Legacy URI Fields

Existing fields such as:

```
self_uri
site_uri
capability_uris
resource_uris
event_uris
incident_uris
```

MAY continue to be returned.

Equivalent `_links` SHOULD be added.

Example:

```json
{
  "self_uri": "https://api.example.org/api/v2/status/resources/orion-scratch",
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    }
  }
}
```

## 21.2. Phase 2: Update Clients and SDKs

IRI client SDKs and MCP tools SHOULD prefer `_links` when available.

Hard-coded URL construction SHOULD be treated as a fallback.

## 21.3. Phase 3: Align With ResourceDefinition and ResourceState

As the companion ResourceDefinition / ResourceState RFC is adopted, facilities SHOULD expose links between stable resource descriptions and dynamic state representations.

Example:

```json
{
  "_links": {
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    }
  }
}
```

## 21.4. Phase 4: Deprecate Legacy URI Fields

After equivalent `_links` are available and documented, legacy URI fields MAY be marked deprecated.

Deprecation SHOULD include:

```
replacement link relation
target API version
migration guidance
expected removal timeline, if any
```

## 21.5. Phase 5: Remove Legacy URI Fields in a Major Version

Legacy URI fields SHOULD only be removed in a future major API version after a documented migration period.

# 22\. OpenAPI Integration

OpenAPI schemas SHOULD include `_links` on HAL-enabled resource representations.

Example:

```
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
    type:
      type: string
    deprecation:
      type: string
      format: uri
    name:
      type: string
    profile:
      type: string
      format: uri
    title:
      type: string
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

Example resource schema fragment:

```
ResourceDefinition:
  type: object
  required:
    - id
    - resource_type
    - _links
  properties:
    id:
      type: string
    name:
      type:
        - string
        - "null"
    description:
      type:
        - string
        - "null"
    resource_type:
      $ref: '#/components/schemas/ResourceType'
    attributes:
      type: object
      additionalProperties: true
    _links:
      $ref: '#/components/schemas/HalLinks'
```

Operation links SHOULD be supported by OpenAPI operation definitions.

Where an operation entry point is advertised through a link relation, the corresponding relation documentation SHOULD identify the relevant OpenAPI operation or service description.

# 23\. Relationship to IRI Type URNs

IRI Type URNs and HAL link relations serve different purposes.

```
resource_type identifies what a resource is.
link relation identifies how one representation relates to another.
profile identifies the semantic or schema profile of the linked representation.
service-desc identifies a machine-readable service description.
```

Example:

```json
{
  "resource_type": "urn:doe-iri:resource:storage:filesystem:scratch",
  "_links": {
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch",
      "profile": "https://iri.science/profiles/resource-state"
    }
  }
}
```

A resource type URN SHOULD NOT be confused with a HAL relation name.

# 24\. Governance

The IRI Interfaces Technical Subcommittee SHOULD govern the standard IRI relation registry.

Governance SHOULD include:

1. Review of new standard relation names.  
2. Review of relation semantics.  
3. Review of source and target type expectations.  
4. Review of facility-local relation promotion to standard relations.  
5. Deprecation and replacement guidance.  
6. Versioning of relation documentation.  
7. Publication of examples.  
8. Alignment with IRI Type URN governance.  
9. Coordination with the ResourceDefinition / ResourceState RFC where a relation targets state resources.

Facility-local relations MAY be used, but they SHOULD be documented and namespaced to avoid collision.

# 25\. IANA Considerations

This document does not require IANA action.

Where existing registered link relations apply, IRI SHOULD use them rather than defining duplicate IRI-specific relations.

IRI-specific relations SHOULD be documented in the IRI relation registry and exposed through CURIE expansion.

# 26\. References

1. RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*.  
2. RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.  
3. RFC 8288, *Web Linking*.  
4. RFC 8631, *Link Relation Types for Web Services*.  
5. RFC 8259, *The JavaScript Object Notation Data Interchange Format*.  
6. JSON Hypertext Application Language, draft-kelly-json-hal.  
7. OpenAPI Specification 3.1.  
8. IANA Link Relations Registry.  
9. IRI Facility API OpenAPI Specification.  
10. RFC: IRI URN Structure and Registry.  
11.       RFC: Type-Specific Attributes for IRI Resource Objects.  
12. RFC: Separating ResourceDefinition from ResourceState in the IRI Facility API.  
13. RFC: Facility Physical and Logical Topology API Using HAL Links.  
14. RFC: JSON Hypertext Application Language, https://datatracker.ietf.org/doc/html/draft-kelly-json-hal-06.  
    ---

# Appendix A. Complete Example: Frontier, Orion, and Orion Scratch

## A.1. Frontier ResourceDefinition

```json
{
  "id": "frontier",
  "name": "Frontier",
  "description": "OLCF Frontier compute system",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "attributes": {
    "scheduler_type": "slurm"
  },
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "self": {
      "href": "https://api.example.org/api/v2/resource-definitions/frontier"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/frontier"
    },
    "iri:jobApi": {
      "href": "https://api.example.org/api/v2/compute/resources/frontier/jobs",
      "profile": "https://iri.science/profiles/job-api"
    },
    "iri:hasMountedFilesystem": {
      "href": "https://api.example.org/api/v2/resource-relationships/frontier-orion-scratch-mount",
      "profile": "https://iri.science/profiles/mounted-filesystem-relationship"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

## A.2. Orion Storage ResourceDefinition

```json
{
  "id": "orion-storage",
  "name": "Orion",
  "description": "Storage system providing the Orion filesystem namespace",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "attributes": {
    "storage_type": "urn:doe-iri:resource:storage:filesystem",
    "filesystem_technology": "lustre"
  },
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-storage"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-storage"
    },
    "iri:providesFilesystem": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    }
  }
}
```

## A.3. Orion Scratch Filesystem ResourceDefinition

```json
{
  "id": "orion-scratch",
  "name": "Orion Scratch Filesystem",
  "description": "Scratch filesystem namespace provided by Orion",
  "resource_type": "urn:doe-iri:resource:storage:filesystem:scratch",
  "attributes": {
    "filesystem_technology": "lustre",
    "namespace_root": "/lustre/orion",
    "persistence_class": "scratch"
  },
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    },
    "iri:state": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch"
    },
    "iri:capacity": {
      "href": "https://api.example.org/api/v2/status/resources/orion-scratch/capacity",
      "profile": "https://iri.science/profiles/resource-capacity-state"
    },
    "iri:filesystemApi": {
      "href": "https://api.example.org/api/v2/filesystems/orion-scratch",
      "profile": "https://iri.science/profiles/filesystem-api"
    },
    "iri:providedBy": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-storage"
    }
  }
}
```

## **A.4. Frontier to Orion Scratch Mount Relationship**

```json
{
  "id": "frontier-orion-scratch-mount",
  "relationship_type": "urn:doe-iri:relationship:has-mounted-filesystem",
  "source_resource_id": "frontier",
  "target_resource_id": "orion-scratch",
  "attributes": {
    "mount_path": "/lustre/orion",
    "access_mode": "read-write",
    "visibility": "compute-nodes",
    "filesystem_semantics": "posix",
    "intended_use": "scratch"
  },
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/resource-relationships/frontier-orion-scratch-mount"
    },
    "iri:source": {
      "href": "https://api.example.org/api/v2/resource-definitions/frontier"
    },
    "iri:target": {
      "href": "https://api.example.org/api/v2/resource-definitions/orion-scratch"
    }
  }
}
```

# Appendix B. Summary of Architectural Benefits

This RFC provides the following architectural benefits:

1. **Reduced URL construction**: Clients follow advertised links instead of constructing paths.  
2. **Better operation discovery**: Resources advertise applicable operation entry points.  
3. **AI-safe traversal**: MCP tools and AI agents use explicit relation names instead of speculative URLs.  
4. **Support for resource/state separation**: Resource descriptions can link to dynamic state resources defined by the companion RFC.  
5. **Topology modeling**: Physical and logical relationships become explicit and navigable.  
6. **Cleaner schema evolution**: New links and relations can be added without expanding every resource schema.  
7. **Facility flexibility**: Servers can evolve internal routing while preserving relation semantics.  
8. **Authorization-aware discovery**: Producers can expose only links appropriate to the caller.  
9. **Incremental migration**: Legacy URI fields can coexist with `_links` during transition.

