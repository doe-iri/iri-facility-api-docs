# IRI Compute System Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/compute/system`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:compute:system`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Profile Applicability

This profile applies to an IRI Resource representation whose `resource_type` is
`urn:doe-iri:resource:compute:system`. It specializes the [IRI Status Resource
Profile](../../status/resource.md); a conforming representation MUST also
satisfy that base profile. The authoritative registration record for this
Resource Type URN is in [Resource Type URNs](../../../urns/resource-types.md).

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of compute systems within the DOE Integrated Research Infrastructure (IRI). A compute system represents a managed computing environment composed of one or more compute nodes and supporting infrastructure, presented to users, applications, or workflows as a cohesive computational resource.

The compute model intentionally separates the system-level resource from individual nodes and processing devices. A `urn:doe-iri:resource:compute:system` resource describes system-level characteristics, while node, CPU, and GPU resources describe lower-level components when a facility chooses to expose that topology.

For example:

```text
Compute System
urn:doe-iri:resource:compute:system
        │
        │ iri:has-node
        ▼
Compute Node
urn:doe-iri:resource:compute:node
```

This separation allows a compute system to be defined once while nodes and processor resources are independently represented and related through IRI links.

The attributes in this profile describe configured characteristics of the compute system. This version of the profile does not define current utilization, available nodes, queue depth, free memory, job activity, health, or service availability. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by this Resource Definition Profile.

Only attributes represented using controlled DOE-IRI URNs appear in the taxonomy. Quantitative or descriptive attributes such as configured resource counts, memory capacity, vendor, product, and version are defined by the profile but are not represented as taxonomy branches.

```text
urn:doe-iri
│
├── resource
│   └── compute
│       └── system
│
└── compute
    ├── system-capability
    │   ├── batch-scheduling
    │   ├── interactive-access
    │   ├── container-execution
    │   └── accelerator-support
    ├── container-runtime
    │   ├── apptainer
    │   ├── singularity
    │   ├── podman
    │   ├── podman-hpc
    │   ├── shifter
    │   └── docker
    ├── container-image-format
    │   ├── oci-image
    │   ├── docker-v2-image
    │   ├── oci-image-layout
    │   ├── oci-archive
    │   ├── docker-archive
    │   ├── sif
    │   └── apptainer-sandbox
    ├── container-execution-format
    │   ├── sif
    │   ├── runtime-managed-image
    │   ├── oci-runtime-bundle
    │   └── rootfs-directory
    ├── container-acquisition
    │   ├── direct
    │   ├── pre-stage-required
    │   └── not-supported
    ├── container-registry-auth
    │   ├── none
    │   ├── anonymous
    │   ├── user-login
    │   ├── facility-managed
    │   └── pull-secret
    ├── container-uid-mode
    │   ├── host-user
    │   ├── userns
    │   ├── fakeroot
    │   └── setuid-helper
    ├── container-gpu-injection
    │   ├── automatic
    │   ├── module
    │   ├── runtime-hook
    │   └── host-library-bind
    ├── container-build
    │   ├── none
    │   ├── login-node
    │   ├── compute-node
    │   ├── batch
    │   └── ci-service
    ├── container-mpi-model
    │   ├── bind
    │   ├── hybrid
    │   ├── container-native
    │   └── none
    ├── container-mpi-host-transfer
    │   ├── bind-mount
    │   ├── library-injection
    │   ├── library-swap
    │   ├── launcher-only
    │   └── none
    ├── container-mpi-abi
    │   ├── mpich
    │   └── open-mpi
    ├── container-mpi-activation
    │   ├── automatic
    │   ├── flag
    │   ├── module
    │   ├── env
    │   └── none
    ├── cpu-architecture             (reused; registered by the CPU profile)
    └── gpu-programming-interface    (reused; registered by the GPU profile)
```

## 4. Compute System Attributes

The `container-*` vocabularies are used only by the `container_runtimes` attribute (Section 4.4). `cpu-architecture` and `gpu-programming-interface` are reused unchanged from the [CPU](cpu.md) and [GPU](gpu.md) profiles; the [Controlled Attribute URN Registry](../../../urns/attributes.md) remains authoritative for all of these values.


This Resource Definition Profile defines the set of attributes that MAY be used to describe resources of type `urn:doe-iri:resource:compute:system`.

Except for `schema_version`, attributes in this profile are optional. The absence of an optional attribute indicates that the information has not been provided and MUST NOT be interpreted as implying a particular value or capability.

Configured aggregate counts describe the capacity represented by the resource definition. They SHOULD NOT be interpreted as current available capacity.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition (e.g. `"1.0.0"`). | yes |
| `system_capabilities` | 1.0.0 | Array IRI URN string | Identifies capabilities exposed by the compute system. | no |
| `configured_node_count` | 1.0.0 | integer | Configured number of compute nodes represented by the system. | no |
| `configured_cpu_core_count` | 1.0.0 | integer | Configured aggregate number of CPU cores represented by the system. | no |
| `configured_gpu_count` | 1.0.0 | integer | Configured aggregate number of GPU devices represented by the system. | no |
| `configured_memory_gib` | 1.0.0 | integer | Configured aggregate system memory represented by the system in GiB (2³⁰ bytes). | no |
| `vendor` | 1.0.0 | string | Identifies the system vendor when relevant. | no |
| `product` | 1.0.0 | string | Identifies the system product or platform when relevant. | no |
| `version` | 1.0.0 | string | Identifies the deployed platform or system version when relevant. | no |
| `container_runtimes` | 1.0.0 | Array `ContainerRuntimeProfile` | Container execution capability discovery: one entry per facility container execution path (Section 4.4). Absent means container capability is not published (unknown); an empty array states that containerized execution is unsupported. | no |

### 4.1 Compute System Capabilities

The `system_capabilities` attribute identifies capabilities exposed by a `urn:doe-iri:resource:compute:system` resource. A compute system may expose multiple capabilities, so the attribute is represented as an array of registered DOE-IRI URNs from the `urn:doe-iri:compute:system-capability` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:compute:system-capability:batch-scheduling` | Batch scheduling | The compute system supports submission and execution of workloads through a batch scheduling environment. | `provisional` |
| `urn:doe-iri:compute:system-capability:interactive-access` | Interactive access | The compute system supports interactive user or workflow access for executing or preparing computational work. | `provisional` |
| `urn:doe-iri:compute:system-capability:container-execution` | Container execution | The compute system supports execution of containerized workloads through an available container runtime or execution environment. | `provisional` |
| `urn:doe-iri:compute:system-capability:accelerator-support` | Accelerator support | The compute system provides or supports access to computational accelerators such as GPUs. | `provisional` |

Example:

```json
{
  "system_capabilities": [
    "urn:doe-iri:compute:system-capability:batch-scheduling",
    "urn:doe-iri:compute:system-capability:container-execution",
    "urn:doe-iri:compute:system-capability:accelerator-support"
  ]
}
```

A capability indicates that the compute system supports the described function. It does not imply that the capability is currently available to a particular user, project, allocation, or workload. Authorization and current availability are separate concerns.

Capabilities SHOULD NOT be inferred solely from vendor or product information.

### 4.2 Configured Compute Capacity

The configured capacity attributes describe relatively stable aggregate capacity represented by the compute-system resource:

- `configured_node_count` identifies the number of configured nodes.
- `configured_cpu_core_count` identifies the aggregate configured CPU core count.
- `configured_gpu_count` identifies the aggregate configured GPU device count.
- `configured_memory_gib` identifies aggregate configured system memory in GiB.

For example:

```json
{
  "configured_node_count": 1024,
  "configured_cpu_core_count": 131072,
  "configured_gpu_count": 4096,
  "configured_memory_gib": 524288
}
```

These values represent configured capacity and MUST NOT be interpreted as currently idle, allocatable, or available capacity. If values such as available nodes, free memory, or idle GPUs are represented, their semantics and update behavior are governed by the applicable IRI API contract and Resource Definition Profile.

Where a facility exposes detailed node, CPU, or GPU resources, configured aggregate counts MAY be derivable from those resources. Facilities MAY still advertise aggregate values when doing so is useful for discovery or when lower-level topology is not exposed.

### 4.3 Vendor, Product, and Version

The optional `vendor`, `product`, and `version` attributes provide descriptive implementation information about the compute system.

These values are represented as strings rather than controlled DOE-IRI URNs unless a future interoperability requirement demonstrates a need for a controlled vendor or product vocabulary.

### 4.4 Container Runtimes

The `container_runtimes` attribute is an OPTIONAL addition to this draft profile. It lets a client discover, before job submission, how a compute system runs containerized workloads: which runtimes it accepts, which image formats, whether a registry image can be referenced directly or must be pre-staged and converted, which registries are permitted, how a private repository is authenticated, how GPUs and host libraries are integrated, whether rootless or unprivileged execution is required, whether a facility build environment exists, and which CPU architectures are supported. It carries no image-acquisition operation and does not change the `Container` job schema.

`container_runtimes` is an array of `ContainerRuntimeProfile` objects. Each object describes one facility container execution path. Array order is not significant.

- The attribute is OPTIONAL. Its absence means the facility has not published structured container information; container capability is then **unknown** and MUST NOT be read as unsupported.
- An empty array (`[]`) is an explicit statement that containerized execution is not supported. When it is empty, `urn:doe-iri:compute:system-capability:container-execution` MUST NOT appear in `system_capabilities`.
- A non-empty array MUST be accompanied by `urn:doe-iri:compute:system-capability:container-execution` in `system_capabilities`.
- When the array is non-empty, exactly one entry MUST have `default` set to `true`.
- Two entries MUST NOT share the same `runtime` value unless their `applies_to_queues` sets are disjoint.

The `ContainerRuntimeProfile` attributes are:

| Attribute | Type | Required | Description |
|---|---|---|---|
| `runtime` | IRI URN (`container-runtime`) | yes | Container runtime/engine for this path. |
| `runtime_version` | string | no | Deployed or default runtime version. Informational. |
| `default` | boolean | yes | Whether this is the default path among otherwise matching entries. Exactly one `true` per non-empty array. |
| `applies_to_queues` | array of string | no | Exact resource-local queue names this entry applies to, matching `JobAttributes.queue_name`. Absent means all queues. Non-empty and unique when present. |
| `accepted_image_formats` | array of IRI URN (`container-image-format`) | yes (≥ 1) | Input representations this path can consume. Unique. |
| `native_execution_format` | IRI URN (`container-image-format` or `container-execution-format`) | no | Representation actually executed. Differs from an accepted input when conversion occurs in this path. |
| `registry_pull` | IRI URN (`container-acquisition`) | yes | `direct`, `pre-stage-required`, or `not-supported`. |
| `pull_actor` | string enum: `user`, `facility`, `runtime` | no | Which actor performs the pull and any conversion. Informational. |
| `registry_policy_mode` | string enum: `any`, `allowlist`, `deny-all`, `unknown` | required when `registry_pull` is not `not-supported` | Outbound registry access state. |
| `allowed_registries` | array of string (HTTPS origin) | required and non-empty iff `registry_policy_mode` is `allowlist`; absent otherwise | Exact HTTPS origins (scheme and authority only). Informational discovery aid, not an authorization statement. |
| `private_registry_auth` | array of IRI URN (`container-registry-auth`) | no | Authentication methods available for private repositories. Unique. Names methods, never credential material. |
| `auth_docs_uri` | string (URI) | no | Human documentation for establishing private-registry access. |
| `rootless_required` | boolean | no | Whether containers must run rootless. |
| `privileged_allowed` | boolean | no | Whether `--privileged`-equivalent execution is permitted. |
| `uid_mode` | IRI URN (`container-uid-mode`) | no | In-container execution identity model. |
| `gpu_integration` | `GpuIntegration` object | no | GPU and host-library integration for this path. |
| `mpi` | `ContainerMpiSupport` object | no | How MPI works inside containers on this path. |
| `cpu_architectures` | array of IRI URN (`cpu-architecture`) | no | CPU architectures supported for container execution on this path. Unique. |
| `build_support` | IRI URN (`container-build`) | no | Where a user may build or convert an image using facility compute. |
| `build_docs_uri` | string (URI) | no | Human documentation for the build/convert workflow. |
| `image_scanning` | string enum: `required`, `optional`, `not-supported`, `unknown` | no | Facility image-scanning policy for this path. |
| `signature_verification` | string enum: `required`, `optional`, `not-supported`, `unknown` | no | Facility image-signature policy for this path. |
| `network_modes` | array of string enum: `host`, `none`, `isolated` | no | Non-empty unique set of supported container network modes. |
| `default_network_mode` | string enum: `host`, `none`, `isolated` | required when `network_modes` is present | One member of `network_modes`. |
| `max_image_bytes` | integer (> 0) | no | Maximum accepted source/compressed image size when the facility enforces one. |
| `notes` | string | no | Human-readable clarification. Not machine-interpreted. |

The `GpuIntegration` object contains:

| Attribute | Type | Required | Description |
|---|---|---|---|
| `programming_interfaces` | array of IRI URN (`gpu-programming-interface`) | no | GPU programming interfaces usable from within the container on this path. Unique. |
| `injection_mechanism` | IRI URN (`container-gpu-injection`) | no | How the adapter exposes GPU devices and host libraries in the container. |

`GpuIntegration` MUST NOT contain native runtime flags. Runtime identity is informational and MUST NOT be used to infer accepted formats, native execution format, acquisition behavior, registry policy, architecture, or execution policy; those are stated explicitly by the entry.

The `ContainerMpiSupport` object describes how an MPI application inside a container obtains a working MPI at run time. This is the sharpest difference between facilities and is not implied by `runtime`: the common DOE pattern is that the container carries an ABI-compatible MPICH and the facility supplies its optimized host MPI (HPE Cray MPICH, Aurora MPICH) at run time, either bind-mounted into the container (OLCF, ALCF) or swapped/injected over the container's MPICH by a runtime option (NERSC `podman-hpc --mpi`, Shifter `--module=mpich`). A container-native Open MPI built with PMIx is the portable but non-optimized alternative.

| Attribute | Type | Required | Description |
|---|---|---|---|
| `models` | array of IRI URN (`container-mpi-model`) | yes (≥ 1) | Supported MPI integration models: `bind`, `hybrid`, `container-native`, `none`. Unique. |
| `default_model` | IRI URN (`container-mpi-model`) | required when `models` has more than one entry and is not solely `none` | Model the facility recommends. Member of `models`. |
| `host_transfer` | IRI URN (`container-mpi-host-transfer`) | no | How the host MPI stack reaches the container for a non-native model: `bind-mount`, `library-injection`, `library-swap`, `launcher-only`, `none`. |
| `host_mpi` | string | no | Host MPI stack the container integrates with, e.g. `HPE Cray MPICH 8`. Informational. |
| `abi` | IRI URN (`container-mpi-abi`) | no | ABI family the in-container MPI must conform to for a non-native model: `mpich` or `open-mpi`. |
| `required_container_mpi` | string | no | In-container MPI the facility requires for ABI-compatible operation, e.g. `MPICH 3.4.2 or 3.4.3`. |
| `gpu_aware` | string enum: `supported`, `not-supported`, `unknown` | no | Whether GPU-aware (CUDA / ROCm / Level Zero) MPI is available from within the container. |
| `process_managers` | array of string enum: `pmi1`, `pmi2`, `pmix` | no | Process-manager interfaces the host launcher offers the container. Non-empty unique when present. |
| `activation` | IRI URN (`container-mpi-activation`) | no | How the user enables host-MPI integration: `automatic`, `flag`, `module`, `env`, `none`. |
| `mpi_docs_uri` | string (URI) | no | Human documentation for running MPI in containers on this path. |
| `notes` | string | no | Human clarification, e.g. exact bind paths, module names, environment variables. Not machine-interpreted. |

`ContainerMpiSupport` values are descriptive. This profile defines no MPI-setup operation and does not guarantee native MPI performance for any given image.

[RFC: Container Execution Capability Discovery for IRI Compute Systems](../../../../rfc/rfc-container-capability-discovery.md) is authoritative for the complete normative producer and consumer requirements, validation rules, security considerations, and conformance plan for this attribute.

## 5 Compute System JSON Schema

```yaml
components:
  schemas:

    IriUrn:
      type: string
      description: >
        A DOE-IRI Uniform Resource Name (URN) identifying a registered
        IRI resource type, attribute value, capability, or other
        controlled vocabulary value.
      pattern: '^urn:doe-iri:[A-Za-z0-9][A-Za-z0-9:._~-]*$'
      example: urn:doe-iri:compute:system-capability:batch-scheduling

    GpuIntegration:
      type: object
      additionalProperties: false
      description: >
        Adapter-managed GPU and host-library integration for a container
        execution path.
      properties:
        programming_interfaces:
          type: array
          uniqueItems: true
          description: >
            Registered urn:doe-iri:compute:gpu-programming-interface values
            usable from within the container on this path.
          items:
            $ref: '#/components/schemas/IriUrn'
        injection_mechanism:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Registered urn:doe-iri:compute:container-gpu-injection value.

    ContainerMpiSupport:
      type: object
      additionalProperties: false
      description: >
        How an MPI application inside a container obtains a working MPI at
        run time on this path. RFC: Container Execution Capability Discovery
        is authoritative for the normative rules.
      required:
        - models
      properties:
        models:
          type: array
          uniqueItems: true
          minItems: 1
          description: >
            Registered urn:doe-iri:compute:container-mpi-model values:
            bind, hybrid, container-native, none.
          items:
            $ref: '#/components/schemas/IriUrn'
        default_model:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Recommended model. Required when models has more than one entry
            and is not solely none. Member of models.
        host_transfer:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Registered urn:doe-iri:compute:container-mpi-host-transfer value:
            bind-mount, library-injection, library-swap, launcher-only, none.
        host_mpi:
          type: string
          description: Host MPI stack the container integrates with. Informational.
        abi:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Registered urn:doe-iri:compute:container-mpi-abi value the
            in-container MPI must conform to for a non-native model.
        required_container_mpi:
          type: string
          description: >
            In-container MPI the facility requires for ABI-compatible
            operation, e.g. "MPICH 3.4.2 or 3.4.3".
        gpu_aware:
          type: string
          enum: [supported, not-supported, unknown]
        process_managers:
          type: array
          uniqueItems: true
          minItems: 1
          items:
            type: string
            enum: [pmi1, pmi2, pmix]
        activation:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Registered urn:doe-iri:compute:container-mpi-activation value:
            automatic, flag, module, env, none.
        mpi_docs_uri:
          type: string
          format: uri
        notes:
          type: string

    ContainerRuntimeProfile:
      type: object
      additionalProperties: false
      description: >
        One facility container execution path for a compute system.
        RFC: Container Execution Capability Discovery is authoritative for
        the normative rules.
      required:
        - runtime
        - default
        - accepted_image_formats
        - registry_pull
      properties:
        runtime:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: Registered urn:doe-iri:compute:container-runtime value.
        runtime_version:
          type: string
          description: Deployed or default runtime version. Informational.
        default:
          type: boolean
          description: >
            Whether this is the default path among otherwise matching
            entries. Exactly one entry has default true when the array is
            non-empty.
        applies_to_queues:
          type: array
          uniqueItems: true
          minItems: 1
          description: >
            Exact resource-local queue names this entry applies to. Absent
            means all queues represented by the resource.
          items:
            type: string
            minLength: 1
        accepted_image_formats:
          type: array
          uniqueItems: true
          minItems: 1
          description: >
            Registered urn:doe-iri:compute:container-image-format values this
            path can consume.
          items:
            $ref: '#/components/schemas/IriUrn'
        native_execution_format:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Registered urn:doe-iri:compute:container-image-format or
            urn:doe-iri:compute:container-execution-format value actually
            executed. Differs from the accepted input when conversion occurs.
        registry_pull:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: >
            Registered urn:doe-iri:compute:container-acquisition value:
            direct, pre-stage-required, or not-supported.
        pull_actor:
          type: string
          enum: [user, facility, runtime]
          description: Which actor performs the pull and any conversion.
        registry_policy_mode:
          type: string
          enum: [any, allowlist, deny-all, unknown]
          description: >
            Outbound registry access state. Required when registry_pull is
            not not-supported.
        allowed_registries:
          type: array
          uniqueItems: true
          minItems: 1
          description: >
            Exact HTTPS origins, scheme and authority only. Present and
            non-empty only when registry_policy_mode is allowlist.
            Informational discovery aid, not an authorization statement.
          items:
            type: string
            format: uri
        private_registry_auth:
          type: array
          uniqueItems: true
          description: >
            Registered urn:doe-iri:compute:container-registry-auth methods
            available for private repositories. Names methods, not material.
          items:
            $ref: '#/components/schemas/IriUrn'
        auth_docs_uri:
          type: string
          format: uri
          description: >
            Human documentation for establishing private-registry access.
        rootless_required:
          type: boolean
        privileged_allowed:
          type: boolean
        uid_mode:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: Registered urn:doe-iri:compute:container-uid-mode value.
        gpu_integration:
          $ref: '#/components/schemas/GpuIntegration'
        mpi:
          $ref: '#/components/schemas/ContainerMpiSupport'
        cpu_architectures:
          type: array
          uniqueItems: true
          description: >
            Registered urn:doe-iri:compute:cpu-architecture values supported
            for container execution on this path.
          items:
            $ref: '#/components/schemas/IriUrn'
        build_support:
          allOf:
            - $ref: '#/components/schemas/IriUrn'
          description: Registered urn:doe-iri:compute:container-build value.
        build_docs_uri:
          type: string
          format: uri
        image_scanning:
          type: string
          enum: [required, optional, not-supported, unknown]
        signature_verification:
          type: string
          enum: [required, optional, not-supported, unknown]
        network_modes:
          type: array
          uniqueItems: true
          minItems: 1
          items:
            type: string
            enum: [host, none, isolated]
        default_network_mode:
          type: string
          enum: [host, none, isolated]
          description: >
            One member of network_modes. Required when network_modes is
            present.
        max_image_bytes:
          type: integer
          format: int64
          minimum: 1
        notes:
          type: string

    ComputeSystemAttributes:
      type: object
      description: >
        Attributes describing a compute system resource with resource type
        urn:doe-iri:resource:compute:system.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          description: >
            Version of the compute-system attribute contract.
          enum:
            - "1.0.0"
          example: "1.0.0"

        system_capabilities:
          type: array
          description: >
            Identifies capabilities exposed by the compute system.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'

        configured_node_count:
          type: integer
          format: int64
          minimum: 0
          description: Configured number of compute nodes represented by the system.

        configured_cpu_core_count:
          type: integer
          format: int64
          minimum: 0
          description: Configured aggregate CPU core count represented by the system.

        configured_gpu_count:
          type: integer
          format: int64
          minimum: 0
          description: Configured aggregate GPU device count represented by the system.

        configured_memory_gib:
          type: integer
          format: int64
          minimum: 0
          description: Configured aggregate memory represented by the system in GiB (2^30 bytes).

        vendor:
          type: string
          description: Identifies the compute system vendor when relevant.

        product:
          type: string
          description: Identifies the compute system product or platform when relevant.

        version:
          type: string
          description: Identifies the deployed platform or system version when relevant.

        container_runtimes:
          type: array
          description: >
            Container execution capability discovery. OPTIONAL. Absent means
            container capability is not published (unknown). MAY be empty,
            which states that containerized execution is unsupported. When
            non-empty, system_capabilities MUST include
            urn:doe-iri:compute:system-capability:container-execution and
            exactly one entry MUST have default true.
          items:
            $ref: '#/components/schemas/ContainerRuntimeProfile'
```

## 6 Example Compute System JSON Instances

### 6.1 Without Container Runtimes

```json
{
  "schema_version": "1.0.0",
  "system_capabilities": [
    "urn:doe-iri:compute:system-capability:batch-scheduling",
    "urn:doe-iri:compute:system-capability:container-execution",
    "urn:doe-iri:compute:system-capability:accelerator-support"
  ],
  "configured_node_count": 1024,
  "configured_cpu_core_count": 131072,
  "configured_gpu_count": 4096,
  "configured_memory_gib": 524288,
  "vendor": "Example Vendor",
  "product": "Example Compute Platform",
  "version": "1.0"
}
```

### 6.2 With Container Runtimes

```json
{
  "schema_version": "1.0.0",
  "system_capabilities": [
    "urn:doe-iri:compute:system-capability:batch-scheduling",
    "urn:doe-iri:compute:system-capability:container-execution",
    "urn:doe-iri:compute:system-capability:accelerator-support"
  ],
  "configured_node_count": 1024,
  "configured_cpu_core_count": 131072,
  "configured_gpu_count": 4096,
  "configured_memory_gib": 524288,
  "vendor": "Example Vendor",
  "product": "Example Compute Platform",
  "version": "1.0",
  "container_runtimes": [
    {
      "runtime": "urn:doe-iri:compute:container-runtime:apptainer",
      "runtime_version": "1.3.6",
      "default": true,
      "accepted_image_formats": [
        "urn:doe-iri:compute:container-image-format:oci-image",
        "urn:doe-iri:compute:container-image-format:docker-v2-image",
        "urn:doe-iri:compute:container-image-format:sif"
      ],
      "native_execution_format": "urn:doe-iri:compute:container-image-format:sif",
      "registry_pull": "urn:doe-iri:compute:container-acquisition:pre-stage-required",
      "pull_actor": "user",
      "registry_policy_mode": "any",
      "private_registry_auth": [
        "urn:doe-iri:compute:container-registry-auth:anonymous",
        "urn:doe-iri:compute:container-registry-auth:user-login"
      ],
      "rootless_required": true,
      "privileged_allowed": false,
      "uid_mode": "urn:doe-iri:compute:container-uid-mode:fakeroot",
      "gpu_integration": {
        "programming_interfaces": [
          "urn:doe-iri:compute:gpu-programming-interface:hip"
        ],
        "injection_mechanism": "urn:doe-iri:compute:container-gpu-injection:host-library-bind"
      },
      "mpi": {
        "models": [
          "urn:doe-iri:compute:container-mpi-model:hybrid",
          "urn:doe-iri:compute:container-mpi-model:bind",
          "urn:doe-iri:compute:container-mpi-model:container-native"
        ],
        "default_model": "urn:doe-iri:compute:container-mpi-model:hybrid",
        "host_transfer": "urn:doe-iri:compute:container-mpi-host-transfer:bind-mount",
        "host_mpi": "HPE Cray MPICH 8",
        "abi": "urn:doe-iri:compute:container-mpi-abi:mpich",
        "required_container_mpi": "MPICH 3.4.2 or 3.4.3, ABI-compatible with the cray-mpich-abi module",
        "gpu_aware": "supported",
        "process_managers": ["pmi2", "pmix"],
        "activation": "urn:doe-iri:compute:container-mpi-activation:module",
        "notes": "Load apptainer-enable-mpi and apptainer-enable-gpu at run time to bind the host Cray MPICH and ROCm libraries; do not load them before 'apptainer build'."
      },
      "cpu_architectures": [
        "urn:doe-iri:compute:cpu-architecture:x86-64"
      ],
      "build_support": "urn:doe-iri:compute:container-build:compute-node",
      "image_scanning": "not-supported",
      "signature_verification": "optional",
      "network_modes": ["host", "none"],
      "default_network_mode": "host",
      "notes": "Docker/OCI sources must be converted to SIF with 'apptainer pull' before job submission."
    }
  ]
}
```

A compute system that does not support containerized execution publishes `"container_runtimes": []` and omits `urn:doe-iri:compute:system-capability:container-execution` from `system_capabilities`.

## 7. Applicable Operation Affordances

This profile supplements the [common Resource profile](../../status/resource.md).
The registered relation definitions remain authoritative for operation
semantics, and the applicable deployed OpenAPI description remains
authoritative for the invocation contract.

A compute-system Resource MAY advertise the following compute operation
relations when each operation is applicable and visible:

- [`iri:submit-job`](../../../relations/submit-job.md),
  [`iri:update-job`](../../../relations/update-job.md),
  [`iri:get-job`](../../../relations/get-job.md),
  [`iri:query-jobs`](../../../relations/query-jobs.md), and
  [`iri:cancel-job`](../../../relations/cancel-job.md).

The filesystem operation family is conditionally applicable only when this
compute system is explicitly configured as a filesystem execution context and
the adapter establishes an unambiguous path namespace and operation context:

- metadata and security: [`iri:change-file-mode`](../../../relations/change-file-mode.md),
  [`iri:change-file-owner`](../../../relations/change-file-owner.md),
  [`iri:identify-file`](../../../relations/identify-file.md),
  [`iri:stat-file`](../../../relations/stat-file.md), and
  [`iri:checksum-file`](../../../relations/checksum-file.md);
- directory and read: [`iri:create-directory`](../../../relations/create-directory.md),
  [`iri:create-symlink`](../../../relations/create-symlink.md),
  [`iri:list-directory`](../../../relations/list-directory.md),
  [`iri:read-file-head`](../../../relations/read-file-head.md), and
  [`iri:read-file-tail`](../../../relations/read-file-tail.md);
- content transfer: [`iri:view-file`](../../../relations/view-file.md),
  [`iri:copy-path`](../../../relations/copy-path.md),
  [`iri:download-file`](../../../relations/download-file.md), and
  [`iri:upload-file`](../../../relations/upload-file.md); and
- mutation and archive: [`iri:remove-path`](../../../relations/remove-path.md),
  [`iri:compress-paths`](../../../relations/compress-paths.md),
  [`iri:extract-archive`](../../../relations/extract-archive.md), and
  [`iri:move-path`](../../../relations/move-path.md).

[`iri:resolve-storage-locations`](../../../relations/resolve-storage-locations.md)
MAY be advertised when storage-location resolution is supported for this
compute-system context. `iri:get-storage-access-endpoints` does not apply to a
compute-system Resource.

Compute-system classification, configured capacity, capabilities, and job
operations do not by themselves establish a filesystem execution context.
Operation eligibility also does not flow from this system to its compute
nodes.

When any applicable operation relation is advertised, the representation MUST
also advertise at least one applicable `service-desc` whose deployed OpenAPI
contains the matching canonical `x-iri-relation` binding. An operation link
targets an operation entry point and MUST NOT carry an IRI representation
`profile`. Clients MUST NOT infer an operation path from the Resource Type,
profile URI, Resource identifier, topology, or capability attributes.

A provider MAY omit an operation link because it is not configured,
applicable, or visible to the requester. Absence means only that the operation
is not advertised in the current representation. Presence grants no
permission and guarantees no successful invocation.

---

*DOE Integrated Research Infrastructure — URN Registry: Compute System*
