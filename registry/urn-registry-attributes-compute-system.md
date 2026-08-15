# Attribute Profile: `urn:doe-iri:resource:compute:system`

This document is for the `urn:doe-iri:resource:compute:system` resource type hierarchy.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:compute:system` |
| Short name | Compute System |
| Description | This namespace collects compute-system-related type definitions. |
| Parent URN | `urn:doe-iri:resource:compute` |
| Status | `provisional` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | Proposed type extensions for compute-system resources. |
| Legacy value | `compute` enumeration. |
| Examples | `urn:doe-iri:resource:compute:system` |
| Notes | These attributes are proposed for describing managed compute-system resources exposed by an IRI facility. |

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

The attributes in this profile describe relatively stable characteristics of the compute system. Dynamic operational information, such as current utilization, available nodes, queue depth, free memory, job activity, health, or service availability, is outside the scope of this profile and SHOULD be represented through the appropriate resource-state mechanisms.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by the Compute System Attribute Profile.

Only attributes represented using controlled DOE-IRI URNs appear in the taxonomy. Quantitative or descriptive attributes such as configured resource counts, memory capacity, vendor, product, and version are defined by the profile but are not represented as taxonomy branches.

```text
urn:doe-iri
│
├── resource
│   └── compute
│       └── system
│
└── compute
    └── system-capability
        ├── batch-scheduling
        ├── interactive-access
        ├── container-execution
        └── accelerator-support
```

## 4. Compute System Attribute Profile

The Compute System Attribute Profile defines the set of attributes that MAY be used to describe resources of type `urn:doe-iri:resource:compute:system`.

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

These values represent configured capacity and MUST NOT be interpreted as currently idle, allocatable, or available capacity. Dynamic values such as available nodes, free memory, or idle GPUs SHOULD be represented through the applicable state resource.

Where a facility exposes detailed node, CPU, or GPU resources, configured aggregate counts MAY be derivable from those resources. Facilities MAY still advertise aggregate values when doing so is useful for discovery or when lower-level topology is not exposed.

### 4.3 Vendor, Product, and Version

The optional `vendor`, `product`, and `version` attributes provide descriptive implementation information about the compute system.

These values are represented as strings rather than controlled DOE-IRI URNs unless a future interoperability requirement demonstrates a need for a controlled vendor or product vocabulary.

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
            Version of the compute system attribute profile definition.
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
```

## 6 Example Compute System JSON Instance

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

---

*DOE Integrated Research Infrastructure — URN Registry: Compute System*
