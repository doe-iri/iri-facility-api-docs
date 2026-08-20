# IRI Block Storage Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/storage/block`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:storage:block`  
**Status:** Draft  
**Version:** 1.0.0

## Profile Applicability

This profile applies when `resource_type` is
`urn:doe-iri:resource:storage:block` and MUST be used together with the
[IRI Status Resource Profile](../../status/resource.md). The authoritative
URN record is [Resource Type URNs](../../../urns/resource-types.md).

This document is for the `urn:doe-iri:resource:storage:block` resource type hierarchy.

## 1. Profile Context

The following retained context identifies the type to which this profile applies;
registration metadata and lifecycle are authoritative in the URN registry.

| Field             | Description                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| URN               | `urn:doe-iri:resource:storage:block`                                                                      |
| Short name        | Block Storage                                                                                             |
| Description       | This namespace collects block storage-related type definitions.                                           |
| Parent URN        | `urn:doe-iri:resource:storage`                                                                            |
| Status            | `provisional`                                                                                             |
| Introduced        | IRI v2.0                                                                                                  |
| Change controller | IRI technical subcommittee.                                                                               |
| Reference         | Proposed type extensions for block storage resources.                                                     |
| Legacy value      | `storage` enumeration.                                                                                    |
| Examples          | `urn:doe-iri:resource:storage:block`                                                                      |
| Notes             | These attributes are proposed for describing logical block storage resources provided by an IRI facility. |

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of block storage resources within the DOE Integrated Research Infrastructure (IRI). A block storage resource represents a logical storage resource that presents data as addressable blocks or volumes that may be consumed directly by a host, operating system, database, filesystem, or other application.

Unlike a filesystem resource, block storage does not inherently define files, directories, or a hierarchical namespace. The consuming system determines how the exposed blocks are used. For example, a block resource may contain a filesystem, may be managed directly by a database or application, or may be incorporated into another logical storage layer.

The IRI storage model intentionally separates the infrastructure that provides storage from the logical block resources consumers use. A `urn:doe-iri:resource:storage:system` resource represents the managed storage infrastructure, while a `urn:doe-iri:resource:storage:block` resource represents an independently consumable logical block-storage volume.

For example:

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        │ iri:provides-block
        ▼
Block Storage
urn:doe-iri:resource:storage:block
        │
        │ iri:attached-to
        ▼
Compute System / Compute Node
```

This separation allows a storage system to provide multiple independently addressable block resources without duplicating infrastructure-level information. It also allows a block resource to be described independently of the system or systems to which it may be attached.

The block resource describes relatively stable characteristics of the logical storage volume, including its access scope, supported block protocols, attachment model, provisioning model, capabilities, configured capacity, intended storage tier, and known backing media.

Information specific to a particular consuming system, such as the device name under which the block resource appears—for example `/dev/nvme1n1`—is not an intrinsic characteristic of the block resource and SHOULD NOT be represented by this profile. Such information is specific to an attachment and MAY be represented through relationship metadata or a future block-attachment resource if independent attachment identity and configuration are required.

This version of the profile does not define whether a volume is currently attached or its current I/O throughput, latency, health, or utilization. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by this Resource Definition Profile. It provides a machine-readable classification for the `urn:doe-iri:resource:storage:block` resource type and for block-storage attributes whose values require consistent semantics across IRI facilities.

The taxonomy distinguishes between the resource being described and the controlled characteristics used to describe that resource. The `urn:doe-iri:resource:storage:block` namespace identifies the resource type itself, while values beneath the `urn:doe-iri:storage` namespace identify standardized characteristics such as access scope, access protocol, access mode, provisioning model, capabilities, storage tier, and physical media.

The taxonomy is not intended to represent relationships between the block resource and the storage system that provides it or the consuming system to which it is attached. Those relationships are represented separately using IRI link relations.

Only attributes represented using controlled DOE-IRI URNs appear in the taxonomy. Scalar attributes such as `capacity_gib` do not appear as taxonomy branches.

The following tree shows the resource type and controlled vocabulary namespaces defined by this profile.

```text
urn:doe-iri
│
├── resource
│   └── storage
│       └── block
│
└── storage
    │
    ├── block-scope
    │   ├── local
    │   └── network
    │
    ├── block-protocol
    │   ├── iscsi
    │   ├── fibre-channel
    │   └── nvme-o-f
    │
    ├── block-access-mode
    │   ├── exclusive
    │   └── shared
    │
    ├── block-provisioning
    │   ├── thin
    │   └── thick
    │
    ├── block-capability
    │   ├── snapshot
    │   ├── clone
    │   └── multipath
    │
    ├── tier
    │   ├── home
    │   ├── project
    │   ├── scratch
    │   ├── campaign
    │   └── archive
    │
    └── media-type
        ├── magnetic-disk
        ├── solid-state
        ├── tape
        └── optical
```

## 4. Block Storage Attributes

This Resource Definition Profile defines the set of attributes that MAY be used to describe resources of type `urn:doe-iri:resource:storage:block`. These attributes provide a consistent, implementation-independent representation of logical block storage characteristics while allowing facilities to expose only those characteristics known and relevant to IRI consumers.

The profile separates the identity of the block resource from both the characteristics of the infrastructure that implements it and the configuration of individual attachments to consuming systems. Controlled characteristics that require consistent machine-readable semantics are represented using registered DOE-IRI URNs.

Except for `schema_version`, attributes in this profile are optional. The absence of an optional attribute indicates that the information has not been provided and MUST NOT be interpreted as implying a particular value or capability. Clients SHOULD rely only on characteristics explicitly advertised by the resource.

The attributes defined by this profile describe configured characteristics of the block resource. The semantics of any time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

The following table defines version `1.0.0` of the block-storage attribute contract.

| Attribute            | Version | Type                 | Description                                                                                         | Mandatory |
| -------------------- | ------- | -------------------- | --------------------------------------------------------------------------------------------------- | --------- |
| `schema_version`     | 1.0.0   | string               | Version of the profile definition (e.g. `"1.0.0"`).                                                 | yes       |
| `block_scope`        | 1.0.0   | IRI URN string       | Identifies whether the block storage is locally available or accessed through a storage network.    | no        |
| `block_protocols`    | 1.0.0   | Array IRI URN string | Identifies block-storage protocols or protocol families through which the resource may be accessed. | no        |
| `block_access_mode`  | 1.0.0   | IRI URN string       | Identifies whether the block resource is intended for exclusive or shared attachment.               | no        |
| `block_provisioning` | 1.0.0   | IRI URN string       | Identifies the capacity-allocation model used to provision the block resource.                      | no        |
| `block_capabilities` | 1.0.0   | Array IRI URN string | Identifies capabilities exposed by the block storage resource.                                      | no        |
| `capacity_gib`       | 1.0.0   | integer              | Configured logical capacity of the block resource in GiB (2³⁰ bytes).                               | no        |
| `tier`               | 1.0.0   | IRI URN string       | Identifies the intended storage lifecycle or usage tier associated with the block resource.         | no        |
| `media_types`        | 1.0.0   | Array IRI URN string | Identifies physical storage media known to back the block resource.                                 | no        |

### 4.1. Block Storage Scope

The `block_scope` attribute describes the access scope of a `urn:doe-iri:resource:storage:block` resource. It distinguishes block storage local to a consuming system from block storage presented to consumers over a storage network.

The value of `block_scope` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:block-scope` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:block-scope:local`   | Local      | A block storage resource whose storage is directly attached to or locally available within a single host or system.                  | `provisional` |
| `urn:doe-iri:storage:block-scope:network` | Network    | A block storage resource presented to one or more consuming systems through a network-based block-storage service or storage fabric. | `provisional` |

For example:

```json
{
  "block_scope": "urn:doe-iri:storage:block-scope:network"
}
```

Block scope describes the general manner in which the storage resource is made available and SHOULD NOT be used to identify the specific protocol used for access. Network-scoped block storage may use iSCSI, Fibre Channel, NVMe over Fabrics, or another block-storage mechanism.

The applicable access mechanisms SHOULD be advertised independently using `block_protocols`.

### 4.2. Block Storage Protocols

The `block_protocols` attribute identifies the block-storage protocols or protocol families through which consumers may access a `urn:doe-iri:resource:storage:block` resource.

A block resource may support more than one access protocol. The `block_protocols` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:block-protocol` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:block-protocol:iscsi`         | iSCSI             | A block-storage protocol that transports SCSI commands over TCP/IP networks, allowing remote storage resources to be presented to consumers as block devices.                                    | `provisional` |
| `urn:doe-iri:storage:block-protocol:fibre-channel` | Fibre Channel     | A storage-network access mechanism that uses Fibre Channel fabrics, commonly carrying SCSI block-storage commands using Fibre Channel Protocol (FCP).                                            | `provisional` |
| `urn:doe-iri:storage:block-protocol:nvme-o-f`      | NVMe over Fabrics | A protocol family that extends NVMe block-storage command semantics across network fabrics, allowing remote NVMe storage to be accessed with semantics similar to locally attached NVMe devices. | `provisional` |

For example:

```json
{
  "block_protocols": [
    "urn:doe-iri:storage:block-protocol:nvme-o-f"
  ]
}
```

The protocol vocabulary identifies interoperable access mechanisms rather than specific products or storage-system implementations.

For example:

```text
Storage System
    storage_technology = vendor/platform implementation
            │
            │ iri:provides-block
            ▼
Block Resource
    block_protocols:
        nvme-o-f
```

Clients SHOULD NOT infer block protocols solely from the technology of the storage system that provides the block resource. Facilities SHOULD explicitly advertise the access mechanisms applicable to the logical block resource.

Protocol versions or transport-specific variants SHOULD be represented independently if a future interoperability requirement requires clients to distinguish them.

### 4.3. Block Access Mode

The `block_access_mode` attribute identifies the intended attachment model of a `urn:doe-iri:resource:storage:block` resource.

The value of `block_access_mode` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:block-access-mode` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:block-access-mode:exclusive` | Exclusive  | The block resource is intended to be actively attached to or accessed by a single consuming system at a time. | `provisional` |
| `urn:doe-iri:storage:block-access-mode:shared`    | Shared     | The block resource supports concurrent attachment or access by multiple consuming systems.                    | `provisional` |

For example:

```json
{
  "block_access_mode":
    "urn:doe-iri:storage:block-access-mode:exclusive"
}
```

A `shared` access mode indicates that the storage infrastructure permits the block resource to be exposed concurrently to multiple consumers. It does **not** imply that arbitrary concurrent writes from those consumers are safe.

Correct coordination of shared block access may require a clustered filesystem, distributed locking, application-level coordination, or other mechanisms outside the scope of this profile.

For example:

```text
Block Resource
    block_access_mode = shared
          │
          ├── iri:attached-to ──> Compute Node A
          └── iri:attached-to ──> Compute Node B
```

Clients SHOULD NOT interpret `block_access_mode` as an authorization policy or as an indication of the resource's current attachment state.

### 4.4. Block Provisioning

The `block_provisioning` attribute identifies how physical storage capacity is allocated to a logical block resource.

The value of `block_provisioning` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:block-provisioning` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:block-provisioning:thin`  | Thin provisioning  | A provisioning model in which the logical capacity presented to a block resource may exceed the physical storage initially allocated to it, with physical capacity allocated as data is written. | `provisional` |
| `urn:doe-iri:storage:block-provisioning:thick` | Thick provisioning | A provisioning model in which physical storage capacity corresponding to the requested logical capacity is allocated or reserved when the block resource is provisioned.                         | `provisional` |

For example:

```json
{
  "block_provisioning": "urn:doe-iri:storage:block-provisioning:thin"
}
```

The provisioning model describes how backing capacity is allocated and SHOULD NOT be interpreted as the current amount of physical storage consumed by the resource.

For example:

```text
capacity_gib
    Configured logical capacity

block_provisioning
    How backing capacity is allocated

current physical consumption
    Time-varying operational value
```

This version of the profile does not define current allocated capacity, consumed capacity, pool utilization, or remaining capacity. If represented, their semantics and update behavior are governed by the applicable IRI API contract and Resource Definition Profile.

### 4.5. Block Storage Capabilities

The `block_capabilities` attribute identifies capabilities exposed by a `urn:doe-iri:resource:storage:block` resource.

A block resource may provide multiple capabilities. The `block_capabilities` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:block-capability` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:block-capability:snapshot`  | Snapshot   | The block resource supports creation of point-in-time representations of its stored block data for recovery, rollback, cloning, or other data-management purposes.     | `provisional` |
| `urn:doe-iri:storage:block-capability:clone`     | Clone      | The block resource supports creation of a new independently addressable block resource based on the contents of an existing block resource or snapshot.                | `provisional` |
| `urn:doe-iri:storage:block-capability:multipath` | Multipath  | The block resource supports access through multiple I/O paths between consuming systems and the storage infrastructure for resiliency, failover, or load distribution. | `provisional` |

For example:

```json
{
  "block_capabilities": [
    "urn:doe-iri:storage:block-capability:snapshot",
    "urn:doe-iri:storage:block-capability:clone",
    "urn:doe-iri:storage:block-capability:multipath"
  ]
}
```

The `block_capabilities` attribute SHOULD describe capabilities actually exposed for the logical block resource. Clients SHOULD NOT infer capabilities solely from the storage technology or block protocol.

For example, a storage platform may support snapshots at the infrastructure level while snapshots are disabled or unavailable for a particular logical volume. In that case, the block resource SHOULD NOT advertise the snapshot capability.

Capabilities describe functionality and SHOULD NOT be interpreted as current operational condition. For example, support for multipath is a capability, while the number of currently healthy paths is a distinct time-varying observation.

The capability vocabulary is intended to be extensible. Additional capability URNs SHOULD be registered when they identify meaningful, implementation-independent functionality that IRI clients need to discover or reason about.

### 4.6. Block Storage Capacity

The `capacity_gib` attribute identifies the configured logical capacity represented by a `urn:doe-iri:resource:storage:block` resource.

Capacity is expressed in gibibytes (GiB), where one GiB is equal to 2³⁰ bytes.

For example:

```json
{
  "capacity_gib": 10240
}
```

In this example, the block resource exposes a configured logical capacity of 10,240 GiB.

The `capacity_gib` value represents the logical capacity presented by the block resource and does not necessarily represent the amount of physical storage currently allocated or consumed. This distinction is particularly important for thin-provisioned block resources.

For example:

```text
Block Resource

capacity_gib = 10240
    Logical capacity exposed to consumers

block_provisioning = thin
    Physical capacity allocated as needed

physical capacity currently consumed
    Time-varying operational value
```

If current consumption, remaining physical capacity, storage-pool utilization, or other changing capacity information is represented, its semantics and update behavior are governed by the applicable IRI API contract and Resource Definition Profile.

### 4.7. Storage Tier

The `tier` attribute identifies the intended storage lifecycle, usage pattern, or purpose associated with a `urn:doe-iri:resource:storage:block` resource.

The value of `tier` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:tier` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:tier:home`     | Home       | Persistent user-oriented storage intended for user-specific files or data.                                                                                         | `provisional` |
| `urn:doe-iri:storage:tier:project`  | Project    | Shared persistent storage allocated to a project, collaboration, or team for ongoing project data and use.                                                         | `provisional` |
| `urn:doe-iri:storage:tier:scratch`  | Scratch    | High-performance temporary storage intended for active workloads, intermediate data, or transient working data, typically subject to limited retention.            | `provisional` |
| `urn:doe-iri:storage:tier:campaign` | Campaign   | Intermediate-term storage intended to retain data associated with a scientific campaign, experiment, project, or allocation for the duration of that activity.     | `provisional` |
| `urn:doe-iri:storage:tier:archive`  | Archive    | Storage intended for durable, long-term retention of data that is accessed less frequently and is not expected to provide active-tier performance characteristics. | `provisional` |

For example:

```json
{
  "tier": "urn:doe-iri:storage:tier:project"
}
```

Storage tier describes the intended role or lifecycle of the block resource and is independent of the protocol, provisioning model, underlying media, or storage technology used to provide it.

A client SHOULD NOT infer performance, retention policy, durability, or media type solely from the `tier` value.

### 4.8. Storage Media Types

The `media_types` attribute identifies physical storage media known to retain data associated with a `urn:doe-iri:resource:storage:block` resource.

A block resource may be backed by more than one type of physical storage media. The `media_types` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:media-type` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:media-type:magnetic-disk` | Magnetic disk | Storage media that retains data magnetically on rotating disks, such as hard disk drives (HDDs).                                                   | `provisional` |
| `urn:doe-iri:storage:media-type:solid-state`   | Solid-state   | Nonvolatile electronic storage media with no moving mechanical components, such as flash-based solid-state drives (SSDs).                          | `provisional` |
| `urn:doe-iri:storage:media-type:tape`          | Tape          | Storage media that retains data magnetically on tape and is generally optimized for high-capacity, sequential access and long-term data retention. | `provisional` |
| `urn:doe-iri:storage:media-type:optical`       | Optical       | Storage media that retains data using optically readable media, such as CD, DVD, Blu-ray, or other optical storage technologies.                   | `provisional` |

For example:

```json
{
  "media_types": [
    "urn:doe-iri:storage:media-type:solid-state"
  ]
}
```

The presence of multiple values indicates that the logical block resource may be backed by multiple media types. It does not describe how data is distributed among those media or whether particular portions of the block address space reside on a particular medium.

Media types SHOULD be advertised at the block-resource level only when the backing media are known and meaningful to consumers. Where the physical media are known only for the underlying storage infrastructure, `media_types` SHOULD instead be advertised on the corresponding storage-system resource.

Clients SHOULD NOT infer performance, latency, durability, or storage tier solely from media type.

The attribute SHOULD be omitted when the underlying media cannot be meaningfully determined for the block resource or when the facility does not intend to expose that implementation detail.

## 5. Block Storage JSON Schema

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
      example: urn:doe-iri:storage:block-protocol:nvme-o-f

    BlockStorageAttributes:
      type: object
      description: >
        Attributes describing a block storage resource with resource type
        urn:doe-iri:resource:storage:block.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          description: >
            Version of the block-storage attribute contract.
          enum:
            - "1.0.0"
          example: "1.0.0"

        block_scope:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies whether the block resource is locally available
            or accessed through a storage network.
          example: urn:doe-iri:storage:block-scope:network

        block_protocols:
          type: array
          description: >
            Identifies block-storage protocols or protocol families
            through which the block resource may be accessed.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:block-protocol:nvme-o-f

        block_access_mode:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies whether the block resource is intended for
            exclusive or shared attachment.
          example: urn:doe-iri:storage:block-access-mode:exclusive

        block_provisioning:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the capacity-allocation model used to provision
            the block resource.
          example: urn:doe-iri:storage:block-provisioning:thin

        block_capabilities:
          type: array
          description: >
            Identifies capabilities exposed by the block storage resource.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:block-capability:snapshot
            - urn:doe-iri:storage:block-capability:clone
            - urn:doe-iri:storage:block-capability:multipath

        capacity_gib:
          type: integer
          format: int64
          minimum: 0
          description: >
            Configured logical capacity of the block resource,
            expressed in GiB (2^30 bytes).
          example: 10240

        tier:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the intended storage lifecycle or usage tier
            associated with the block resource.
          example: urn:doe-iri:storage:tier:project

        media_types:
          type: array
          description: >
            Identifies physical storage media known to back the
            block storage resource.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:media-type:solid-state
```

## 6. Example Block Storage JSON Instance

```json
{
  "schema_version": "1.0.0",
  "block_scope": "urn:doe-iri:storage:block-scope:network",
  "block_protocols": [
    "urn:doe-iri:storage:block-protocol:nvme-o-f"
  ],
  "block_access_mode": "urn:doe-iri:storage:block-access-mode:exclusive",
  "block_provisioning": "urn:doe-iri:storage:block-provisioning:thin",
  "block_capabilities": [
    "urn:doe-iri:storage:block-capability:snapshot",
    "urn:doe-iri:storage:block-capability:clone",
    "urn:doe-iri:storage:block-capability:multipath"
  ],
  "capacity_gib": 10240,
  "tier": "urn:doe-iri:storage:tier:project",
  "media_types": [
    "urn:doe-iri:storage:media-type:solid-state"
  ]
}
```

The complete resource model associates the block resource with the storage system that provides it and, where applicable, with consuming systems through IRI relationships:

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        │ iri:provides-block
        ▼
Block Storage
urn:doe-iri:resource:storage:block

attributes:
    block_scope = network
    block_protocols = [nvme-o-f]
    block_access_mode = exclusive
    block_provisioning = thin
    capacity_gib = 10240
        │
        │ iri:attached-to
        ▼
Compute System / Compute Node
```

The `iri:attached-to` relationship identifies the consuming resource. Attachment-specific details that can differ between consumers, such as local device paths or host-specific mappings, SHOULD NOT be represented as intrinsic attributes of the block resource.

---

*DOE Integrated Research Infrastructure — URN Registry: Block Storage*
