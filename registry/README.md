# DOE IRI Registry

> Registry documentation for the resource types, controlled attribute vocabularies, attribute profiles, and hypermedia relationships used by the Department of Energy Integrated Research Infrastructure (IRI) Facility API.

The DOE IRI Registry provides the registered semantic identifiers used to describe IRI resources while keeping the core API representation implementation-independent. It separates **resource classification**, **type-specific characteristics**, and **resource relationships** so that each area can evolve without requiring every registry change to modify the core OpenAPI schema.

At a high level:

```text
Resource Type  →  Attributes  →  Relationships
```

Operational state is modeled separately from these relatively stable resource definitions.

## 1. What Is the DOE IRI Registry?

The registry records the identifiers and semantic definitions used by the IRI Facility API.

It is intentionally separate from the specifications that define how those identifiers are structured and registered:

```text
Specifications
    Define the rules.

Registries
    Record the values assigned under those rules.
```

The governing specifications define matters such as URN syntax, registration procedures, extension rules, HAL relationship semantics, and conformance requirements. The registry records the resource types, controlled vocabulary values, and link relations assigned under those rules.

The root of the registered URN namespace is:

```text
urn:doe-iri:
```

The [DOE-IRI URN Root Registry](urn-registry-root.md) is the authoritative entry point for the registered namespace hierarchy.

## 2. Resource Model

IRI resource representations use three independently extensible semantic layers.

| Layer | Answers | Representation |
|---|---|---|
| **Resource Type** | What kind of resource is this? | `resource_type` containing a registered `urn:doe-iri:resource:*` URN |
| **Attributes** | What relatively stable characteristics does the resource have? | Type-specific `attributes`, including registered controlled URN values where appropriate. |
| **Relationships** | How is the resource related to other resources? | Registered HAL `_links` relations. |

Conceptually:

```text
Resource Definition
│
├── resource_type ──> What kind of resource is this?
│
├── attributes ─────> What characteristics does it have?
│
└── _links ─────────> How is it related to other resources?
```

This separation allows:

- New resource types to be registered without changing the core resource schema.
- Type-specific attribute profiles to evolve independently.
- Controlled attribute vocabularies to grow without introducing new JSON property names.
- New link relations to be registered without embedding topology into resource definitions.

## 3. Registry Structure

The registry is organized hierarchically by semantic domain.

```text
DOE-IRI Registry
│
├── Root URN Registry
│
├── Resource Type Registries
│   │
│   ├── Storage
│   │   ├── Storage System
│   │   ├── Filesystem
│   │   ├── Filesystem Mount
│   │   ├── Block Storage
│   │   └── Object Storage
│   │
│   ├── Compute
│   │   ├── Compute System
│   │   ├── Compute Node
│   │   ├── CPU
│   │   └── GPU
│   │
│   └── Service
│   │   ├── DTN Service
│   │   └── Inference Service
│
├── Controlled Attribute Vocabularies
│   ├── Storage
│   ├── Compute
│   └── Service
│
└── Link Profiles
    ├── Storage relationships
    ├── Compute relationships
    └── Service relationships
```

The URN hierarchy is a **semantic classification hierarchy**. It does not imply physical containment, ownership, deployment topology, or runtime relationships between resources.

For example:

```text
urn:doe-iri:resource:compute:node
```

classifies a resource as a compute node. Its membership in a compute system is represented separately through a registered link relation such as `iri:hasNode`.

## 4. Root Registry

| Document | Purpose |
|---|---|
| [DOE-IRI URN Root Registry](urn-registry-root.md) | Defines the registered top-level `urn:doe-iri:` semantic branches, base resource-type URNs, allocation units, compression identifiers, and delegated extension authorities. |

The Root Registry is the starting point for discovering registered DOE-IRI identifiers.

The governing URN specification, rather than the Root Registry, defines namespace syntax, matching and equivalence rules, registration procedures, and extension rules.

## 5. Resource Type Registries

Resource Type Registries define the registered type hierarchy for a resource domain and provide navigation to the applicable attribute and relationship documentation.

### 5.1. Storage

The Storage registry defines the resource types used to represent storage infrastructure and logical storage resources.

**Entry points**

| Document | Purpose |
|---|---|
| [Storage Type Registry](urn-registry-type-storage.md) | Defines the `urn:doe-iri:resource:storage` resource hierarchy and the storage resource model. |
| [Storage Taxonomy and URN Index](urn-registry-type-storage-taxonomy.md) | Consolidated taxonomy, storage controlled attribute URNs, and storage resource relationships. |

**Resource attribute profiles**

| Resource Type | Attribute Profile |
|---|---|
| Storage System | [urn-registry-attributes-storage-system.md](urn-registry-attributes-storage-system.md) |
| Filesystem | [urn-registry-attributes-storage-filesystem.md](urn-registry-attributes-storage-filesystem.md) |
| Filesystem Mount | [urn-registry-attributes-storage-mount.md](urn-registry-attributes-storage-mount.md) |
| Block Storage | [urn-registry-attributes-storage-block.md](urn-registry-attributes-storage-block.md) |
| Object Storage | [urn-registry-attributes-storage-object.md](urn-registry-attributes-storage-object.md) |

**Storage relationship profiles**

| Relationship | Source | Target | Link Profile |
|---|---|---|---|
| `iri:providesFilesystem` | Storage System | Filesystem | [link-profile-provides-filesystem.md](link-profile-provides-filesystem.md) |
| `iri:providesBlock` | Storage System | Block Storage | [link-profile-provides-block.md](link-profile-provides-block.md) |
| `iri:providesObject` | Storage System | Object Storage | [link-profile-provides-object.md](link-profile-provides-object.md) |
| `iri:hasMount` | Filesystem | Filesystem Mount | [link-profile-has-mount.md](link-profile-has-mount.md) |
| `iri:mountedOn` | Filesystem Mount | Compute System | [link-profile-mounted-on.md](link-profile-mounted-on.md) |
| `iri:attachedTo` | Block Storage | Compute System or Compute Node | [link-profile-attached-to.md](link-profile-attached-to.md) |

### 5.2. Compute

The Compute registry defines the resource types used to represent managed compute systems, individual nodes, and processing devices.

**Entry points**

| Document | Purpose |
|---|---|
| [Compute Type Registry](urn-registry-type-compute.md) | Defines the `urn:doe-iri:resource:compute` resource hierarchy and the compute resource model. |
| [Compute Taxonomy and URN Index](urn-registry-type-compute-taxonomy.md) | Consolidated taxonomy, compute controlled attribute URNs, and compute resource relationships. |

**Resource attribute profiles**

| Resource Type | Attribute Profile |
|---|---|
| Compute System | [urn-registry-attributes-compute-system.md](urn-registry-attributes-compute-system.md) |
| Compute Node | [urn-registry-attributes-compute-node.md](urn-registry-attributes-compute-node.md) |
| CPU | [urn-registry-attributes-compute-cpu.md](urn-registry-attributes-compute-cpu.md) |
| GPU | [urn-registry-attributes-compute-gpu.md](urn-registry-attributes-compute-gpu.md) |

**Compute relationship profiles**

| Relationship | Source | Target | Link Profile |
|---|---|---|---|
| `iri:hasNode` | Compute System | Compute Node | [link-profile-has-node.md](link-profile-has-node.md) |
| `iri:hasCPU` | Compute Node | CPU | [link-profile-has-cpu.md](link-profile-has-cpu.md) |
| `iri:hasGPU` | Compute Node | GPU | [link-profile-has-gpu.md](link-profile-has-gpu.md) |

### 5.3. Service

The Service registry defines consumable data-transfer and model-invocation services and the relatively stable infrastructure relationships used to describe their hosting and configured filesystem access.

**Entry points**

| Document | Purpose |
|---|---|
| [Service Type Registry](urn-registry-type-service.md) | Defines the `urn:doe-iri:resource:service` resource hierarchy, the `urn:doe-iri:service` controlled-vocabulary branch, and the service resource model. |
| [Service Taxonomy and URN Index](urn-registry-type-service-taxonomy.md) | Consolidated taxonomy, service controlled attribute URNs, and service resource relationships. |

**Resource attribute profiles**

| Resource Type | Attribute Profile |
|---|---|
| DTN Service | [urn-registry-attributes-service-dtn.md](urn-registry-attributes-service-dtn.md) |
| Inference Service | [urn-registry-attributes-service-inference.md](urn-registry-attributes-service-inference.md) |

**Service relationship profiles**

| Relationship | Source | Target | Link Profile |
|---|---|---|---|
| `iri:hostedOn` | DTN Service or Inference Service | Compute System or Compute Node | [link-profile-hosted-on.md](link-profile-hosted-on.md) |
| `iri:accessesMount` | DTN Service | Filesystem Mount | [link-profile-accesses-mount.md](link-profile-accesses-mount.md) |

### 5.4. Additional Resource Domains

Additional resource domains MAY be introduced beneath `urn:doe-iri:resource` as their refinement models are defined.

Base resource types currently registered by the Root Registry include domains such as:

```text
urn:doe-iri:resource:network
urn:doe-iri:resource:system
urn:doe-iri:resource:website
urn:doe-iri:resource:service
```

When a domain requires subtype refinement, controlled attributes, or relationship profiles, it SHOULD follow the same documentation structure used by Storage and Compute.

## 6. Controlled Attribute Vocabularies

Some resource attributes use registered URNs rather than unrestricted strings.

A controlled attribute URN identifies a standardized characteristic of a resource; it does not identify the resource itself.

For example:

```text
Resource type:
    urn:doe-iri:resource:storage:filesystem

Attribute:
    tier

Controlled value:
    urn:doe-iri:storage:tier:scratch
```

Compare this with:

```text
Resource type:
    urn:doe-iri:resource:compute:cpu

Attribute:
    cpu_architecture

Controlled value:
    urn:doe-iri:compute:cpu-architecture:x86-64
```

Controlled vocabulary namespaces are separate from resource-type namespaces:

```text
urn:doe-iri:resource:...
    Resource classification

urn:doe-iri:storage:...
    Storage controlled attribute vocabulary

urn:doe-iri:compute:...
    Compute controlled attribute vocabulary

urn:doe-iri:service:...
    Service controlled attribute vocabulary
```

Each resource's attribute profile defines which controlled vocabularies apply and whether an attribute is singular, multi-valued, optional, or required.

## 7. Link Profiles

Link profiles define the semantics of registered HAL relationships between IRI resources.

Each relationship profile documents, at minimum:

- Semantic meaning.
- Source representation type.
- Target representation type.
- Cardinality.
- Whether the target represents static topology or dynamic state.
- Whether authorization may affect relationship visibility.
- Whether the target is a resource, state object, operation entry point, or relationship resource.
- Example HAL representation.

Relationships describe topology or navigation and SHOULD NOT be duplicated as ordinary attributes when a registered link relation exists for the same semantic relationship.

For example:

```text
Storage System
    │
    │ iri:providesFilesystem
    ▼
Filesystem
    │
    │ iri:hasMount
    ▼
Filesystem Mount
    │
    │ iri:mountedOn
    ▼
Compute System
```

and:

```text
Compute System
    │
    │ iri:hasNode
    ▼
Compute Node
    │
    ├── iri:hasCPU ──> CPU
    │
    └── iri:hasGPU ──> GPU
```

## 8. How the Documents Relate

The following example shows how the registry documentation for a filesystem resource connects.

```text
urn:doe-iri:resource:storage
        │
        └── urn:doe-iri:resource:storage:filesystem
                    │
                    ├── Attribute Profile
                    │     urn-registry-attributes-storage-filesystem.md
                    │
                    ├── Controlled Attributes
                    │     urn:doe-iri:storage:filesystem-technology:lustre
                    │     urn:doe-iri:storage:tier:scratch
                    │     urn:doe-iri:storage:media-type:solid-state
                    │     ...
                    │
                    └── Relationships
                          iri:hasMount
                              │
                              └── link-profile-has-mount.md
```

The resource type selects the applicable semantic profile. The profile defines the characteristics of that type, including any controlled URN values. Link profiles define how instances of that type relate to other IRI resources.

## 9. Where Do I Start?

| I want to... | Start here |
|---|---|
| Understand the DOE-IRI URN namespace | [Root Registry](urn-registry-root.md) |
| Find a registered resource type | [Root Registry](urn-registry-root.md) → applicable Resource Type Registry |
| Describe a storage resource | [Storage Type Registry](urn-registry-type-storage.md) |
| Describe a compute resource | [Compute Type Registry](urn-registry-type-compute.md) |
| Describe a DTN or inference service | [Service Type Registry](urn-registry-type-service.md) |
| Find service controlled attribute values | [Service Taxonomy and URN Index](urn-registry-type-service-taxonomy.md) |
| Understand service hosting or configured mount access | [Service relationship profiles](urn-registry-type-service.md#6-service-resource-relationships) |
| Determine which attributes apply to a resource | The resource's Attribute Profile |
| Find valid controlled attribute values | Applicable taxonomy/index or Attribute Profile |
| Understand how two resources relate | Applicable Link Profile |
| Determine whether information belongs in definition or state | Resource model guidance and applicable Attribute/Link Profile |
| Register a new DOE-IRI URN | Governing DOE-IRI URN specification |
| Define a facility-specific extension | Root Registry extension-authority section and governing URN specification |

## 10. Registry Conventions

### 10.1. File Naming

Registry documentation follows a predictable naming convention:

```text
urn-registry-root.md
    Root DOE-IRI namespace registry

urn-registry-type-<domain>.md
    Resource-type registry and model for a domain

urn-registry-type-<domain>-taxonomy.md
    Consolidated taxonomy and URN index for a domain

urn-registry-attributes-<domain>-<type>.md
    Attribute profile for a specific resource type

link-profile-<relation>.md
    Semantic definition of an IRI link relation
```

Examples:

```text
urn-registry-type-storage.md
urn-registry-type-compute.md

urn-registry-attributes-storage-filesystem.md
urn-registry-attributes-compute-node.md

link-profile-has-mount.md
link-profile-has-node.md
```

### 10.2. Registry Status

Registry entries use lifecycle status values such as:

| Status | Meaning |
|---|---|
| `active` | Assigned and approved for current use. |
| `provisional` | Assigned for evaluation or refinement and subject to change. |
| `deprecated` | Retained for compatibility but no longer preferred for new use. |

A deprecated value SHOULD identify its preferred replacement when one exists.

### 10.3. URNs and Link Relations

DOE-IRI URNs and IRI link relations serve different purposes.

```text
URN
    Identifies a registered semantic value.

Link relation
    Identifies the semantic relationship between representations.
```

For example:

```text
urn:doe-iri:resource:storage:filesystem
```

classifies a resource, while:

```text
iri:hasMount
```

describes a relationship from that filesystem to a mount resource.

### 10.4. Definition and State

Registry attribute profiles SHOULD describe relatively stable resource characteristics.

Examples of definition information include:

- Resource type.
- Technology.
- Architecture.
- Capabilities.
- Configured capacity.
- Topology relationships.

Examples of operational state include:

- Current availability.
- Health.
- Utilization.
- Free or used capacity.
- Current throughput.
- Current attachment or mount status.

Dynamic state SHOULD NOT be encoded by changing relatively stable type or topology semantics solely because current operating conditions change.

## 11. Governing Specifications

The registry is governed by specifications that define the syntax, semantics, and registration rules under which registry values are assigned.

| Specification | Purpose |
|---|---|
| [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md) | Defines the DOE-IRI URN namespace structure, registration model, extension rules, and conformance requirements. |
| [Type-Specific Attributes for IRI Resource Objects](../rfc/rfc-type-specific-attributes.md) | Defines the model for type-specific resource attributes. |
| HAL `_links` Integration for IRI 2.0 | Defines the use of HAL links for resource relationships. |
| Facility Physical and Logical Topology API Using HAL Links | Defines topology representation using resource relationships. |
| Separating ResourceDefinition from ResourceState | Defines the separation between relatively stable resource definition and dynamic operational state. |

Where a registry document and a governing specification appear to conflict, the governing specification defines the registration and conformance rules; the registry defines the currently assigned values.

---

*IRI specification — DOE Integrated Research Infrastructure*
