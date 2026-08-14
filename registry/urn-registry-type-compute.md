# Type Registry: `urn:doe-iri:resource:compute`

This document defines the `urn:doe-iri:resource:compute` resource type hierarchy and serves as the entry point for the DOE-IRI compute resource model.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:compute` |
| Short name | Compute |
| Description | This namespace collects compute-related resource type definitions. |
| Parent URN | `urn:doe-iri:resource` |
| Status | `active` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | Proposed type extensions for compute resources. |
| Legacy value | `compute` enumeration. |
| Examples | `urn:doe-iri:resource:compute:system` |
| Notes | This namespace defines the provisional child resource types used to refine the generic `compute` resource type. Type-specific characteristics are defined by the corresponding attribute profiles. |

## 2. Introduction

The purpose of the IRI compute model is to provide a consistent, implementation-independent way to describe computational infrastructure and the processing resources made available by an IRI facility.

This document defines the top-level compute resource taxonomy and the relationships between its primary resource types. Detailed characteristics and controlled vocabularies applicable to each resource type are defined by the corresponding attribute profiles referenced in Section 4. This document therefore serves as the entry point for the IRI compute model rather than defining all characteristics of each compute resource.

The compute model separates the managed **compute system** from the **compute nodes** that participate in that system and from processing devices, such as CPUs and GPUs, associated with those nodes.

A primary goal of this separation is to avoid embedding physical containment, system topology, implementation details, or operational state directly into a single generic compute resource. Independently meaningful components are represented as resources with their own identities and characteristics, while relationships between those resources are expressed explicitly using IRI link relations.

The compute model follows the broader IRI separation between resource identity, resource characteristics, resource relationships, and operational state:

```text
Resource Type
    "What kind of compute resource is this?"

Attributes
    "What relatively stable characteristics does this resource have?"

Relationships
    "How is this resource related to other resources?"

State
    "What is happening with this resource now?"
```

Resource type URNs identify what kind of resource is being described. Attribute profiles describe relatively stable characteristics of that resource. IRI link relations describe topology and relationships between independently identifiable resources. Dynamic information such as current utilization, free memory, workload activity, health, or availability is represented separately through the appropriate resource-state mechanisms.

### 2.1. Compute Resource Model

The compute model defines a **Compute System** as a managed computing environment composed of one or more compute nodes and supporting infrastructure, presented as a cohesive computational resource.

The general model is:

```text
Compute System
urn:doe-iri:resource:compute:system
        │
        │ iri:hasNode
        ▼
Compute Node
urn:doe-iri:resource:compute:node
        │
        ├── iri:hasCPU ──> CPU
        │                  urn:doe-iri:resource:compute:cpu
        │
        └── iri:hasGPU ──> GPU
                           urn:doe-iri:resource:compute:gpu
```

A **Compute System** represents a managed computing environment presented to users, applications, or workflows as a cohesive computational resource. A system may consist of many compute nodes and supporting scheduling, networking, storage, and management infrastructure.

A **Compute Node** represents an individual computing host within a compute system. A node provides processing, memory, and other local resources used to execute workloads or support operation of the compute environment.

A **CPU** represents a central processing unit or processor package associated with a compute node and provides general-purpose instruction processing.

A **GPU** represents a graphics processing unit or similar highly parallel accelerator associated with a compute node and used to accelerate computational workloads.

A facility is not required to expose every individual node, CPU, or GPU resource. Facilities MAY expose only the level of topology necessary to support discovery, workflow planning, allocation, or other IRI use cases.

### 2.2. Example Compute Topology

The following theoretical example illustrates a compute system containing two nodes with CPU and GPU resources:

```text
Compute System
resource_type = urn:doe-iri:resource:compute:system

        │ iri:hasNode
        │
        ├───────────────────────────────┐
        ▼                               ▼

Compute Node 001                  Compute Node 002
resource_type =                  resource_type =
  urn:doe-iri:resource:            urn:doe-iri:resource:
  compute:node                     compute:node

        │                               │
        ├── iri:hasCPU                  ├── iri:hasCPU
        │       │                       │       │
        │       ▼                       │       ▼
        │      CPU                     CPU
        │
        └── iri:hasGPU                  └── iri:hasGPU
                │                               │
                ▼                               ▼
               GPU                             GPU
```

The example illustrates an important property of the model: the type hierarchy classifies resources, while the IRI link relations express the actual topology between those resources.

## 3. Taxonomy

The following taxonomy defines the resource types registered beneath `urn:doe-iri:resource:compute`.

The hierarchy represents **resource type refinement only**. It does not represent physical containment, membership, allocation, scheduling, or other topology relationships between compute resources. Those relationships are represented using IRI link relations.

```text
urn:doe-iri:resource:compute
│
├── system
│   └── "What managed computing environment can I use?"
│
├── node
│   └── "What individual computing host participates in the system?"
│
├── cpu
│   └── "What general-purpose processing resource is available?"
│
└── gpu
    └── "What accelerated or highly parallel processing resource is available?"
```

Although these resource types appear as siblings in the taxonomy, their topology relationships are expressed separately. For example, a compute node may contain CPU and GPU resources, but `cpu` and `gpu` are not subtypes of `node`; all three are refinements of the generic compute resource type.

## 4. Compute Resource Types

The following URNs are registered as child resource types of `urn:doe-iri:resource:compute`. Each type refines the generic compute resource into a more specific resource abstraction and links to an attribute profile defining the characteristics applicable to that resource type.

| URN | Short name | Description | Status |
|---|---|---|---|
| [`urn:doe-iri:resource:compute:system`](./urn-registry-attributes-compute-system.md) | Compute System | A managed computing environment composed of one or more compute nodes and supporting infrastructure, presented as a cohesive computational resource. | `provisional` |
| [`urn:doe-iri:resource:compute:node`](./urn-registry-attributes-compute-node.md) | Compute Node | An individual computing host within a compute system that provides processing, memory, and other local resources for executing workloads. | `provisional` |
| [`urn:doe-iri:resource:compute:cpu`](./urn-registry-attributes-compute-cpu.md) | CPU | A central processing unit or processor package associated with a compute node that provides general-purpose instruction processing. | `provisional` |
| [`urn:doe-iri:resource:compute:gpu`](./urn-registry-attributes-compute-gpu.md) | GPU | A graphics processing unit or similar highly parallel accelerator associated with a compute node and used to accelerate computational workloads. | `provisional` |

The linked attribute profiles define resource-specific characteristics and controlled DOE-IRI vocabularies applicable to each compute resource type.

## 5. Compute Controlled Attribute Vocabulary

The compute attribute profiles define controlled DOE-IRI URN vocabularies for characteristics that require consistent, machine-readable semantics across IRI facilities. These URNs are used as attribute values when describing compute-system, node, CPU, and GPU resources.

Controlled attribute URNs are distinct from the resource type URNs defined in Section 4. A resource type URN identifies **what kind of compute resource is being represented**, while a controlled attribute URN identifies a standardized **characteristic, capability, architecture, role, or programming interface of that resource**.

Only attributes that require a registered controlled vocabulary are represented by URNs in this section. Quantitative or descriptive attributes such as configured counts, memory capacity, vendor, product, model, version, or clock frequency use their corresponding JSON scalar types.

| URN | Short name | Description | Status |
|---|---|---|---|
| [`urn:doe-iri:compute:system-capability:batch-scheduling`](./urn-registry-attributes-compute-system.md) | Batch scheduling | The compute system supports submission and execution of workloads through a batch scheduling environment. | `provisional` |
| [`urn:doe-iri:compute:system-capability:interactive-access`](./urn-registry-attributes-compute-system.md) | Interactive access | The compute system supports interactive user or workflow access for executing or preparing computational work. | `provisional` |
| [`urn:doe-iri:compute:system-capability:container-execution`](./urn-registry-attributes-compute-system.md) | Container execution | The compute system supports execution of containerized workloads through an available container runtime or execution environment. | `provisional` |
| [`urn:doe-iri:compute:system-capability:accelerator-support`](./urn-registry-attributes-compute-system.md) | Accelerator support | The compute system provides or supports access to computational accelerators such as GPUs. | `provisional` |
| [`urn:doe-iri:compute:node-role:compute`](./urn-registry-attributes-compute-node.md) | Compute | The node is primarily intended to execute computational workloads. | `provisional` |
| [`urn:doe-iri:compute:node-role:login`](./urn-registry-attributes-compute-node.md) | Login | The node provides interactive access to a compute environment for tasks such as job preparation, submission, and management. | `provisional` |
| [`urn:doe-iri:compute:node-role:service`](./urn-registry-attributes-compute-node.md) | Service | The node primarily provides supporting services used by the compute environment. | `provisional` |
| [`urn:doe-iri:compute:cpu-architecture:x86-64`](./urn-registry-attributes-compute-cpu.md) | x86-64 | A 64-bit processor architecture compatible with the x86-64 instruction-set architecture. | `provisional` |
| [`urn:doe-iri:compute:cpu-architecture:arm64`](./urn-registry-attributes-compute-cpu.md) | Arm64 | A 64-bit processor architecture compatible with the AArch64 execution state of the Arm architecture. | `provisional` |
| [`urn:doe-iri:compute:cpu-architecture:ppc64le`](./urn-registry-attributes-compute-cpu.md) | ppc64le | A 64-bit little-endian Power Architecture processor environment. | `provisional` |
| [`urn:doe-iri:compute:cpu-architecture:riscv64`](./urn-registry-attributes-compute-cpu.md) | RISC-V 64 | A 64-bit processor architecture based on the RISC-V instruction-set architecture. | `provisional` |
| [`urn:doe-iri:compute:gpu-programming-interface:cuda`](./urn-registry-attributes-compute-gpu.md) | CUDA | The GPU is usable through a CUDA programming environment when supported by the facility software stack. | `provisional` |
| [`urn:doe-iri:compute:gpu-programming-interface:hip`](./urn-registry-attributes-compute-gpu.md) | HIP | The GPU is usable through a HIP programming environment when supported by the facility software stack. | `provisional` |
| [`urn:doe-iri:compute:gpu-programming-interface:opencl`](./urn-registry-attributes-compute-gpu.md) | OpenCL | The GPU is usable through an OpenCL programming environment when supported by the facility software stack. | `provisional` |
| [`urn:doe-iri:compute:gpu-programming-interface:sycl`](./urn-registry-attributes-compute-gpu.md) | SYCL | The GPU is usable through a SYCL programming environment when supported by the facility software stack. | `provisional` |

## 6. Compute Resource Relationships

Relationships between compute resources, and incoming relationships from other resource domains, are represented using registered IRI link relations. These relationships describe topology and containment without embedding one resource definition inside another.

| Relationship | Source | Target | Cardinality | Target Stability | Authorization Affects Visibility | Description |
|---|---|---|---|---|---|---|
| [`iri:hasNode`](./link-profile-has-node.md) | Compute System | Compute Node | `0..*` | Static | Yes | Indicates that the identified compute node participates in or is managed as part of the compute system. |
| [`iri:hasCPU`](./link-profile-has-cpu.md) | Compute Node | CPU | `0..*` | Static | Yes | Indicates that the compute node contains or provides the identified CPU resource. |
| [`iri:hasGPU`](./link-profile-has-gpu.md) | Compute Node | GPU | `0..*` | Static | Yes | Indicates that the compute node contains or provides the identified GPU resource. |
| [`iri:hostedOn`](./link-profile-hosted-on.md) | DTN Service or Inference Service | Compute System or Compute Node | `0..*` targets from a service | Static resource representation. The target identifies hosting infrastructure independently of current routing, live replica placement, health, or availability. | Yes | Incoming cross-domain relationship indicating that the target provides hosting infrastructure for the source service. |
| [`iri:locatedAt`](./link-profile-located-at.md) | Any DOE-IRI Resource | Facility API Site representation | `1` semantic target | Relatively stable Site representation | No; `site_uri` already discloses Site identity | Indicates the relatively stable physical and administrative Site associated with the source Resource. |

These relationships describe relatively stable resource topology and SHOULD NOT be interpreted as operational availability indicators. Current utilization, health, allocation, and availability belong in the corresponding resource-state representations.

Authorization MAY affect relationship visibility. A facility MAY expose aggregate compute-system information while withholding individual node or processor topology from clients that do not require or are not authorized to discover that level of infrastructure detail.

Relationships describe independently identifiable resources and SHOULD NOT be duplicated as ordinary attributes when an IRI link relation is defined for the relationship.

---

*DOE Integrated Research Infrastructure — URN Registry: Compute*
