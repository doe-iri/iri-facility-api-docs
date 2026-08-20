# IRI GPU Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/compute/gpu`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:compute:gpu`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Profile Applicability

This profile applies to an IRI Resource representation whose `resource_type` is
`urn:doe-iri:resource:compute:gpu`. It specializes the [IRI Status Resource
Profile](../../status/resource.md); a conforming representation MUST also
satisfy that base profile. The authoritative registration record for this
Resource Type URN is in [Resource Type URNs](../../../urns/resource-types.md).

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of GPU resources within the DOE Integrated Research Infrastructure (IRI).

A GPU resource represents a graphics processing unit or similar highly parallel accelerator associated with a compute node and used to accelerate computational workloads.

```text
Compute Node
urn:doe-iri:resource:compute:node
        │
        │ iri:has-gpu
        ▼
GPU
urn:doe-iri:resource:compute:gpu
```

This profile describes relatively stable device characteristics, including memory capacity, vendor-defined architecture information, and programming interfaces made available by the facility software environment.

This version of the profile does not define current utilization, allocated memory, temperature, power consumption, health, workload assignment, or availability. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The taxonomy defined in this section identifies the controlled GPU programming-interface vocabulary used by this profile.

```text
urn:doe-iri
│
├── resource
│   └── compute
│       └── gpu
│
└── compute
    └── gpu-programming-interface
        ├── cuda
        ├── hip
        ├── opencl
        └── sycl
```

## 4. GPU Attribute Profile

The GPU Attribute Profile defines attributes that MAY be used to describe resources of type `urn:doe-iri:resource:compute:gpu`.

Except for `schema_version`, attributes are optional.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition. | yes |
| `programming_interfaces` | 1.0.0 | Array IRI URN string | Identifies programming interfaces through which the GPU may be used in the facility environment. | no |
| `memory_gib` | 1.0.0 | integer | Configured device memory in GiB (2³⁰ bytes). | no |
| `vendor` | 1.0.0 | string | Identifies the GPU vendor when relevant. | no |
| `model` | 1.0.0 | string | Identifies the GPU model when relevant. | no |
| `architecture` | 1.0.0 | string | Identifies the vendor-defined GPU architecture or generation when relevant. | no |

### 4.1 GPU Programming Interfaces

The `programming_interfaces` attribute identifies programming interfaces through which the GPU may be used within the facility environment. A GPU may advertise more than one interface, so the attribute is represented as an array of registered DOE-IRI URNs from the `urn:doe-iri:compute:gpu-programming-interface` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:compute:gpu-programming-interface:cuda` | CUDA | The GPU is usable through a CUDA programming environment when supported by the facility software stack. | `provisional` |
| `urn:doe-iri:compute:gpu-programming-interface:hip` | HIP | The GPU is usable through a HIP programming environment when supported by the facility software stack. | `provisional` |
| `urn:doe-iri:compute:gpu-programming-interface:opencl` | OpenCL | The GPU is usable through an OpenCL programming environment when supported by the facility software stack. | `provisional` |
| `urn:doe-iri:compute:gpu-programming-interface:sycl` | SYCL | The GPU is usable through a SYCL programming environment when supported by the facility software stack. | `provisional` |

Example:

```json
{
  "programming_interfaces": [
    "urn:doe-iri:compute:gpu-programming-interface:cuda"
  ]
}
```

The programming-interface vocabulary describes usable interfaces in the facility environment rather than intrinsic hardware identity alone. A facility SHOULD advertise only interfaces that are actually supported for the resource through its deployed software and driver stack.

Current software-module availability, version, or user authorization SHOULD NOT be inferred solely from the presence of a programming-interface value.

### 4.2 GPU Memory

The `memory_gib` attribute identifies configured device memory associated with the GPU resource.

For example:

```json
{
  "memory_gib": 80
}
```

The value represents configured device memory and SHOULD NOT be interpreted as currently free or allocatable memory. If current memory usage is represented, its semantics and update behavior are governed by the applicable IRI API contract and Resource Definition Profile.

### 4.3 Vendor, Model, and Architecture

The optional `vendor`, `model`, and `architecture` attributes provide descriptive implementation information.

`architecture` is represented as a string because GPU architecture and generation naming are vendor-defined and evolve rapidly. A controlled DOE-IRI vocabulary SHOULD be introduced only if cross-facility interoperability requirements demonstrate that standardized architecture identifiers are necessary.

## 5 GPU JSON Schema

```yaml
components:
  schemas:

    IriUrn:
      type: string
      pattern: '^urn:doe-iri:[A-Za-z0-9][A-Za-z0-9:._~-]*$'

    GpuAttributes:
      type: object
      description: >
        Attributes describing a GPU resource with resource type
        urn:doe-iri:resource:compute:gpu.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          enum:
            - "1.0.0"
          example: "1.0.0"

        programming_interfaces:
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'

        memory_gib:
          type: integer
          format: int64
          minimum: 0

        vendor:
          type: string

        model:
          type: string

        architecture:
          type: string
```

## 6 Example GPU JSON Instance

```json
{
  "schema_version": "1.0.0",
  "programming_interfaces": [
    "urn:doe-iri:compute:gpu-programming-interface:cuda"
  ],
  "memory_gib": 80,
  "vendor": "Example GPU Vendor",
  "model": "Example Accelerator",
  "architecture": "Example Architecture"
}
```

---

*DOE Integrated Research Infrastructure — URN Registry: GPU*
