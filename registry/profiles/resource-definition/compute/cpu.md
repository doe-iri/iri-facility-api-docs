# IRI CPU Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/compute/cpu`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:compute:cpu`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Profile Applicability

This profile applies to an IRI Resource representation whose `resource_type` is
`urn:doe-iri:resource:compute:cpu`. It specializes the [IRI Status Resource
Profile](../../status/resource.md); a conforming representation MUST also
satisfy that base profile. The authoritative registration record for this
Resource Type URN is in [Resource Type URNs](../../../urns/resource-types.md).

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of CPU resources within the DOE Integrated Research Infrastructure (IRI).

A CPU resource represents a central processing unit or processor package associated with a compute node and used for general-purpose instruction execution. The profile describes processor characteristics that are relatively stable for the lifetime of the resource.

```text
Compute Node
urn:doe-iri:resource:compute:node
        │
        │ iri:has-cpu
        ▼
CPU
urn:doe-iri:resource:compute:cpu
```

This version of the profile does not define current utilization, active frequency, temperature, power consumption, health, workload assignment, or availability. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The taxonomy defined in this section identifies the controlled CPU architecture vocabulary used by this profile.

```text
urn:doe-iri
│
├── resource
│   └── compute
│       └── cpu
│
└── compute
    └── cpu-architecture
        ├── x86-64
        ├── arm64
        ├── ppc64le
        └── riscv64
```

## 4. CPU Attribute Profile

The CPU Attribute Profile defines attributes that MAY be used to describe resources of type `urn:doe-iri:resource:compute:cpu`.

Except for `schema_version`, attributes are optional.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition. | yes |
| `cpu_architecture` | 1.0.0 | IRI URN string | Identifies the processor instruction-set architecture family. | no |
| `core_count` | 1.0.0 | integer | Number of physical processor cores represented by the CPU resource. | no |
| `thread_count` | 1.0.0 | integer | Number of hardware execution threads represented by the CPU resource. | no |
| `base_clock_mhz` | 1.0.0 | integer | Nominal or base processor clock frequency in MHz when meaningful for the processor. | no |
| `max_clock_mhz` | 1.0.0 | integer | Maximum advertised processor clock frequency in MHz when meaningful for the processor. | no |
| `vendor` | 1.0.0 | string | Identifies the CPU vendor when relevant. | no |
| `model` | 1.0.0 | string | Identifies the CPU model or processor designation when relevant. | no |

### 4.1 CPU Architecture

The `cpu_architecture` attribute identifies the processor instruction-set architecture family represented by the CPU resource. The value MUST be a registered DOE-IRI URN from the `urn:doe-iri:compute:cpu-architecture` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:compute:cpu-architecture:x86-64` | x86-64 | A 64-bit processor architecture compatible with the x86-64 instruction-set architecture. | `provisional` |
| `urn:doe-iri:compute:cpu-architecture:arm64` | Arm64 | A 64-bit processor architecture compatible with the AArch64 execution state of the Arm architecture. | `provisional` |
| `urn:doe-iri:compute:cpu-architecture:ppc64le` | ppc64le | A 64-bit little-endian Power Architecture processor environment. | `provisional` |
| `urn:doe-iri:compute:cpu-architecture:riscv64` | RISC-V 64 | A 64-bit processor architecture based on the RISC-V instruction-set architecture. | `provisional` |

Example:

```json
{
  "cpu_architecture": "urn:doe-iri:compute:cpu-architecture:x86-64"
}
```

Architecture identifies the broad execution architecture and SHOULD NOT be used as a substitute for vendor, model, supported instruction extensions, or software environment information.

### 4.2 CPU Core and Thread Counts

The `core_count` attribute identifies the number of physical processor cores represented by the CPU resource. The `thread_count` attribute identifies the number of hardware execution threads exposed by those cores.

For example:

```json
{
  "core_count": 64,
  "thread_count": 128
}
```

These values describe configured processor topology and SHOULD NOT be interpreted as the number of cores or threads currently available to a user or workload.

### 4.3 CPU Clock Frequency

`base_clock_mhz` and `max_clock_mhz` describe advertised processor frequency characteristics when those concepts are meaningful for the CPU architecture and implementation.

They do not represent current operating frequency. If current frequency is exposed, its semantics and update behavior are governed by the applicable IRI API contract and Resource Definition Profile.

### 4.4 Vendor and Model

The optional `vendor` and `model` attributes provide descriptive implementation information and are represented as strings.

## 5 CPU JSON Schema

```yaml
components:
  schemas:

    IriUrn:
      type: string
      pattern: '^urn:doe-iri:[A-Za-z0-9][A-Za-z0-9:._~-]*$'

    CpuAttributes:
      type: object
      description: >
        Attributes describing a CPU resource with resource type
        urn:doe-iri:resource:compute:cpu.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          enum:
            - "1.0.0"
          example: "1.0.0"

        cpu_architecture:
          $ref: '#/components/schemas/IriUrn'

        core_count:
          type: integer
          minimum: 0

        thread_count:
          type: integer
          minimum: 0

        base_clock_mhz:
          type: integer
          minimum: 0

        max_clock_mhz:
          type: integer
          minimum: 0

        vendor:
          type: string

        model:
          type: string
```

## 6 Example CPU JSON Instance

```json
{
  "schema_version": "1.0.0",
  "cpu_architecture": "urn:doe-iri:compute:cpu-architecture:x86-64",
  "core_count": 64,
  "thread_count": 128,
  "base_clock_mhz": 2000,
  "max_clock_mhz": 3500,
  "vendor": "Example CPU Vendor",
  "model": "Example Processor"
}
```

---

*DOE Integrated Research Infrastructure — URN Registry: CPU*
