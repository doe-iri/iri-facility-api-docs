# 1. Taxonomy

The following compute taxonomy defines the resource types and controlled attribute vocabularies used to model compute resources within an IRI facility.

```text
urn:doe-iri
│
├── resource
│   └── compute
│       ├── system  - "What managed computing environment can I use?"
│       ├── node    - "What individual computing host participates in the system?"
│       ├── cpu     - "What general-purpose processing resource is available?"
│       └── gpu     - "What accelerated or highly parallel processing resource is available?"
│
└── compute         - The compute controlled attribute vocabulary
    │
    │   SYSTEM ATTRIBUTES
    │
    ├── system-capability
    │   ├── batch-scheduling
    │   ├── interactive-access
    │   ├── container-execution
    │   └── accelerator-support
    │
    │   NODE ATTRIBUTES
    │
    ├── node-role
    │   ├── compute
    │   ├── login
    │   └── service
    │
    │   CPU ATTRIBUTES
    │
    ├── cpu-architecture
    │   ├── x86-64
    │   ├── arm64
    │   ├── ppc64le
    │   └── riscv64
    │
    │   GPU ATTRIBUTES
    │
    └── gpu-programming-interface
        ├── cuda
        ├── hip
        ├── opencl
        └── sycl
```

# 2. Compute URN Definitions

| URN | Short name | Description | Status |
|---|---|---|---|
| [`urn:doe-iri:resource:compute:system`](./urn-registry-attributes-compute-system.md) | Compute System | This namespace collects compute-system-related type definitions. | `provisional` |
| [`urn:doe-iri:resource:compute:node`](./urn-registry-attributes-compute-node.md) | Compute Node | This namespace collects compute-node-related type definitions. | `provisional` |
| [`urn:doe-iri:resource:compute:cpu`](./urn-registry-attributes-compute-cpu.md) | CPU | This namespace collects CPU-related type definitions. | `provisional` |
| [`urn:doe-iri:resource:compute:gpu`](./urn-registry-attributes-compute-gpu.md) | GPU | This namespace collects GPU-related type definitions. | `provisional` |
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

# 3. Compute Resource Relationships

Relationships between compute resources, and incoming relationships from other resource domains, are represented using registered IRI link relations. These relationships describe topology and containment without embedding one resource definition inside another.

| Relationship | Source | Target | Cardinality | Target Stability | Authorization Affects Visibility | Description |
|---|---|---|---|---|---|---|
| [`iri:hasNode`](./link-profile-has-node.md) | Compute System | Compute Node | `0..*` | Static | Yes | Indicates that the identified compute node participates in or is managed as part of the compute system. |
| [`iri:hasCPU`](./link-profile-has-cpu.md) | Compute Node | CPU | `0..*` | Static | Yes | Indicates that the compute node contains, provides, or is associated with the identified CPU resource. |
| [`iri:hasGPU`](./link-profile-has-gpu.md) | Compute Node | GPU | `0..*` | Static | Yes | Indicates that the compute node contains, provides, or is associated with the identified GPU resource. |
| [`iri:hostedOn`](./link-profile-hosted-on.md) | DTN Service or Inference Service | Compute System or Compute Node | `0..*` targets from a service | Static resource representation. The target identifies hosting infrastructure independently of current routing, live replica placement, health, or availability. | Yes | Incoming cross-domain relationship indicating that the target provides hosting infrastructure for the source service. |
| [`iri:locatedAt`](./link-profile-located-at.md) | Any DOE-IRI Resource | Facility API Site representation | `1` semantic target | Relatively stable Site representation | No; `site_uri` already discloses Site identity | Indicates the relatively stable physical and administrative Site associated with the source Resource. |
