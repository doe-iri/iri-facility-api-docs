---
layout: default
title: Resource Architecture Overview
parent: IRI 2.0
nav_order: 1
permalink: /resource-architecture-overview/
---

# Making IRI Facility Capabilities Discoverable

The IRI Facility API must describe heterogeneous compute, storage, service,
and other infrastructure across independently operated facilities. It must do
so without forcing every resource-specific concept into one common schema or
requiring clients to understand facility-specific URL conventions. The revised
architecture addresses this challenge through three complementary parts:
`resource_type`, type-specific `attributes`, and HAL `_links`.

This document explains the limitations of the IRI 1.0 resource model and the
reasoning behind this architecture change. Readers will learn:

- how Resource Type URNs provide extensible, governed classification;
- how Resource Definition Profiles give type-specific `attributes` shared
  semantics without replacing the common Resource representation;
- how registered link relations and `_links` describe topology, related
  Resources, and applicable operation entry points;
- how the URN registry, profile documentation, relation documentation, and
  OpenAPI divide responsibility; and
- how these conventions help conventional clients and agentic workflows
  discover facility capabilities without guessing semantics or URLs.

By the end, readers should understand both how a facility publishes this
information and how a consumer can use it to interpret and traverse an IRI
facility as a machine-understandable capability graph.



## 1. IRI 1.0 identified resources but left important meaning implicit

IRI 1.0 established a common Resource representation, but broad resource types
such as `compute`, `storage`, and `service` could not precisely describe
heterogeneous infrastructure.

- Adding every domain property to the common schema would make it continually
  expand.
- Closed type enumerations required schema and client changes for each new
  resource class.
- URI properties and facility-specific routing conventions made relationships
  difficult to discover.
- Clients and agents had to infer topology, capabilities, and operation URLs.
- Similar concepts could be represented differently by different facilities.

The architecture needed extensibility without sacrificing shared meaning.



## 2. The new architecture separates three kinds of information

Every IRI Resource retains the same common representation while adding three
complementary extension points:

| Element | Responsibility |
|---|---|
| `resource_type` | Classifies what kind of Resource this is |
| `attributes` | Describes facts specific to that Resource type |
| `_links` | Advertises relationships and applicable operations |

OpenAPI continues to define the structural API contract: properties, types,
required fields, operations, request bodies, responses, and security.

This separation lets each concern evolve under the appropriate governance
mechanism.



## 3. Each identifier answers a different question

| Concept | Question answered | Example |
|---|---|---|
| Resource ID | Which Resource is this? | `pioneer-compute` |
| Resource Type URN | What kind of Resource is it? | `urn:doe-iri:resource:compute:system` |
| Profile URI | What semantic contract applies? | `…/resource-definition/compute/system` |
| Link relation | Why is the target relevant? | `iri:has-node` |
| `href` | Where is the target? | `/status/resources/node-001` |
| OpenAPI | How is an operation invoked? | `POST /api/v2/compute/job/{resource_id}` |

These identifiers are complementary—not interchangeable.



## 4. One Resource schema supports many specialized resource types

All Resources conform to the common OpenAPI `Resource` schema and the common
Resource profile.

```text
OpenAPI Resource schema
        ↓
Common Resource semantics
        ↓
resource_type
        ↓
Registered Resource Type URN
        ↓
Mapped Resource Definition Profile
        ↓
Meaning of attributes and applicable relationships
```

A Resource Definition Profile specializes the existing Resource
representation. It does not create a separate Resource Definition object,
state object, or endpoint.



## 5. The URN registry provides extensible, governed classification

Resource Type URNs replace a closed enumeration with persistent semantic
identifiers.

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:service:dtn
```

The registry records:

- canonical identifier and meaning;
- semantic parent;
- lifecycle status;
- legacy mapping;
- associated Resource Definition Profile.

The hierarchy supports graceful fallback: a client unfamiliar with a specific
compute subtype can still recognize it as a compute Resource.



## 6. The URN hierarchy classifies meaning, not topology

Additional URN segments narrow semantic classification. They do not mean that
one Resource physically contains another.

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:gpu
```

Systems, nodes, and GPUs are independently identifiable resource types. Their
topology is expressed through links:

```text
Compute System ── iri:has-node ──▶ Compute Node
Compute Node   ── iri:has-gpu  ──▶ GPU
```

This keeps classification stable when facility topology changes.



## 7. `attributes` carries type-specific facts without expanding the common schema

```json
{
  "resource_type": "urn:doe-iri:resource:compute:system",
  "attributes": {
    "schema_version": "1.0.0",
    "system_capabilities": [
      "urn:doe-iri:compute:system-capability:batch-scheduling",
      "urn:doe-iri:compute:system-capability:accelerator-support"
    ],
    "configured_node_count": 512,
    "configured_gpu_count": 2048,
    "vendor": "Example Computing"
  }
}
```

Controlled URNs are used where governed vocabulary improves interoperability.
Counts, capacities, versions, names, paths, and other ordinary values remain
normal JSON scalars.



## 8. Profiles turn an open JSON object into a shared semantic contract

A Resource Definition Profile defines the meaning of `attributes` for one
Resource type.

It documents:

- attribute names, types, units, and interpretation;
- controlled vocabularies;
- profile versioning through `schema_version`;
- applicable relationships and operation affordances;
- extension and conformance rules;
- representative Resource examples.

A profile supplements OpenAPI rather than overriding it. Clients use the
registry's explicit Resource Type-to-profile mapping; they do not construct
profile URIs from URNs.



## 9. `_links` makes facility topology and operations discoverable

```json
{
  "_links": {
    "iri:has-node": {
      "href": "/api/v2/status/resources/node-001",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/compute/node"
    }
  }
}
```

The four link layers remain distinct:

- Relation: **why** the target is relevant.
- `href`: **where** the target is.
- `type`: **how** the target is represented.
- `profile`: **what semantic contract applies to the target**.

Clients traverse advertised links instead of constructing facility-specific
URLs.



## 10. Relation documentation makes every link predictable

Each registered `iri:*` relation defines more than a name:

- semantic meaning;
- permitted source and target types;
- cardinality;
- target classification;
- expected stability or volatility;
- authorization-sensitive visibility;
- meaning of an omitted link.

For example, `iri:has-node` describes relatively stable topology. It does not
assert that the node is healthy, available, or schedulable.

A missing link may reflect authorization filtering rather than semantic
absence.



## 11. Links advertise operations; OpenAPI defines how to invoke them

A compute system can advertise job submission without requiring clients to
know its URL structure:

```json
{
  "_links": {
    "iri:submit-job": {
      "href": "/api/v2/compute/job/pioneer-compute"
    },
    "service-desc": {
      "href": "/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

`iri:submit-job` says the operation is applicable and identifies its entry
point. OpenAPI defines the HTTP method, parameters, request body, responses,
errors, and security requirements.

An operation link identifies an affordance—it does not grant authorization or
guarantee capacity.



## 12. A Pioneer Resource combines classification, description, and navigation

```json
{
  "id": "pioneer-storage",
  "current_status": "up",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "attributes": {
    "schema_version": "1.0.0",
    "storage_technology":
      "urn:doe-iri:storage:system-technology:lustre",
    "capacity_gib": 25165824
  },
  "_links": {
    "self": {
      "href": "/status/resources/pioneer-storage",
      "profile": "…/resource-definition/storage/system"
    },
    "iri:provides-filesystem": [{
      "href": "/status/resources/pioneer-scratch",
      "profile": "…/resource-definition/storage/filesystem"
    }]
  }
}
```

A generic client can process the common fields. A profile-aware client can
interpret the attributes. A hypermedia client can traverse the facility graph.



## 13. A facility becomes a traversable capability graph

```text
Storage System
  └─ iri:provides-filesystem ─▶ Filesystem
                                 └─ iri:has-mount ─▶ Mount
                                                     └─ iri:mounted-on ─▶ Compute System
                                                                           ├─ iri:has-node ─▶ Node
                                                                           └─ iri:submit-job ─▶ Operation

DTN Service
  └─ iri:accesses-mount ────────────────────────────▶ Mount
```

Resources carry their own type and attributes. Relations connect independently
meaningful Resources without duplicating their descriptions.

The public NERSC prototype demonstrates how the same model can describe
Perlmutter, node classes, scratch storage, filesystems, and DTN services.



## 14. Agentic workflows can discover capabilities without guessing

An agent can now follow a deterministic process:

1. Retrieve the facility and its advertised Resources.
2. Classify each Resource using `resource_type`.
3. Apply the registered profile when recognized.
4. Interpret controlled attributes and tolerate unfamiliar extensions.
5. Traverse registered relations to discover topology and capabilities.
6. Follow operation links rather than inventing paths.
7. Consult OpenAPI before invoking an operation.
8. Recheck current status, authorization, and advertised links at execution
   time.

Facilities that publish accurate types, profile-conformant attributes, and
registered links expose a portable, machine-understandable capability
graph—not merely a collection of endpoints.



## 15. Source Material

- IRI v2 OpenAPI specification
- DOE-IRI URN structure and registry specification
- DOE-IRI Resource Type and controlled-attribute registries
- IRI Resource Definition Profiles
- IRI Link Relation Registry
- HAL `_links` RFC
- Public NERSC metadata prototype:
  <https://github.com/gabor-lbl/iri-metadata-nersc>
