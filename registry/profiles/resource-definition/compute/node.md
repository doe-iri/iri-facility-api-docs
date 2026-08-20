# IRI Compute Node Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/compute/node`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:compute:node`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Profile Applicability

This profile applies to an IRI Resource representation whose `resource_type` is
`urn:doe-iri:resource:compute:node`. It specializes the [IRI Status Resource
Profile](../../status/resource.md); a conforming representation MUST also
satisfy that base profile. The authoritative registration record for this
Resource Type URN is in [Resource Type URNs](../../../urns/resource-types.md).

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of compute nodes within the DOE Integrated Research Infrastructure (IRI). A compute node represents an individual computing host within a compute system and provides processing, memory, and other local resources used to execute workloads or support operation of the compute environment.

The compute model intentionally separates node identity from CPU and GPU resources. A node may expose relationships to one or more CPU or GPU resources without embedding those processor definitions directly into the node representation.

```text
Compute System
        │
        │ iri:has-node
        ▼
Compute Node
urn:doe-iri:resource:compute:node
        │
        ├── iri:has-cpu ──> CPU
        └── iri:has-gpu ──> GPU
```

The attributes in this profile describe configured characteristics of the node. This version of the profile does not define current load, free memory, allocation condition, health, or workload activity. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The following taxonomy identifies the controlled vocabulary values used by the Compute Node Attribute Profile.

```text
urn:doe-iri
│
├── resource
│   └── compute
│       └── node
│
└── compute
    └── node-role
        ├── compute
        ├── login
        └── service
```

## 4. Compute Node Attribute Profile

The Compute Node Attribute Profile defines attributes that MAY be used to describe resources of type `urn:doe-iri:resource:compute:node`.

Except for `schema_version`, attributes are optional. Configured counts and capacities describe the node definition rather than current available capacity.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition. | yes |
| `node_roles` | 1.0.0 | Array IRI URN string | Identifies one or more functional roles associated with the node. | no |
| `memory_gib` | 1.0.0 | integer | Configured system memory of the node in GiB (2³⁰ bytes). | no |
| `local_storage_gib` | 1.0.0 | integer | Configured directly attached or node-local storage capacity in GiB (2³⁰ bytes). | no |
| `cpu_socket_count` | 1.0.0 | integer | Configured number of CPU sockets or processor packages associated with the node. | no |
| `cpu_core_count` | 1.0.0 | integer | Configured aggregate CPU core count associated with the node. | no |
| `gpu_count` | 1.0.0 | integer | Configured number of GPU devices associated with the node. | no |
| `vendor` | 1.0.0 | string | Identifies the node vendor when relevant. | no |
| `product` | 1.0.0 | string | Identifies the node product or platform when relevant. | no |
| `model` | 1.0.0 | string | Identifies the node model when relevant. | no |

### 4.1 Compute Node Roles

The `node_roles` attribute identifies functional roles associated with a compute node. A node MAY advertise more than one role. Values are drawn from the `urn:doe-iri:compute:node-role` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:compute:node-role:compute` | Compute | The node is primarily intended to execute computational workloads. | `provisional` |
| `urn:doe-iri:compute:node-role:login` | Login | The node provides interactive access to a compute environment for tasks such as job preparation, submission, and management. | `provisional` |
| `urn:doe-iri:compute:node-role:service` | Service | The node primarily provides supporting services used by the compute environment. | `provisional` |

Example:

```json
{
  "node_roles": [
    "urn:doe-iri:compute:node-role:compute"
  ]
}
```

Node role describes intended function and SHOULD NOT be interpreted as current availability or authorization.

### 4.2 Configured Node Capacity

`memory_gib`, `local_storage_gib`, `cpu_socket_count`, `cpu_core_count`, and `gpu_count` describe configured node capacity.

For example:

```json
{
  "memory_gib": 512,
  "local_storage_gib": 2048,
  "cpu_socket_count": 2,
  "cpu_core_count": 128,
  "gpu_count": 4
}
```

These values SHOULD NOT be interpreted as current available memory, free local storage, idle CPU cores, or available GPUs. If such time-varying values are represented, their semantics and update behavior are governed by the applicable IRI API contract and Resource Definition Profile.

Where CPU and GPU resources are separately exposed through `iri:has-cpu` and `iri:has-gpu`, the aggregate counts MAY be derivable from those relationships. Facilities MAY still publish counts when detailed processor topology is not exposed.

### 4.3 Vendor, Product, and Model

The optional `vendor`, `product`, and `model` attributes provide descriptive implementation information for the node and are represented as strings.

## 5 Compute Node JSON Schema

```yaml
components:
  schemas:

    IriUrn:
      type: string
      pattern: '^urn:doe-iri:[A-Za-z0-9][A-Za-z0-9:._~-]*$'

    ComputeNodeAttributes:
      type: object
      description: >
        Attributes describing a compute node resource with resource type
        urn:doe-iri:resource:compute:node.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          enum:
            - "1.0.0"
          example: "1.0.0"

        node_roles:
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'

        memory_gib:
          type: integer
          format: int64
          minimum: 0

        local_storage_gib:
          type: integer
          format: int64
          minimum: 0

        cpu_socket_count:
          type: integer
          minimum: 0

        cpu_core_count:
          type: integer
          minimum: 0

        gpu_count:
          type: integer
          minimum: 0

        vendor:
          type: string

        product:
          type: string

        model:
          type: string
```

## 6 Example Compute Node JSON Instance

```json
{
  "schema_version": "1.0.0",
  "node_roles": [
    "urn:doe-iri:compute:node-role:compute"
  ],
  "memory_gib": 512,
  "local_storage_gib": 2048,
  "cpu_socket_count": 2,
  "cpu_core_count": 128,
  "gpu_count": 4,
  "vendor": "Example Vendor",
  "product": "Example Node Platform",
  "model": "X1000"
}
```

---

*DOE Integrated Research Infrastructure — URN Registry: Compute Node*
