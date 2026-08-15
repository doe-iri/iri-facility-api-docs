# Attribute Profile: `urn:doe-iri:resource:storage:system`

This document is for the `urn:doe-iri:resource:storage:system` resource type hierarchy.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:storage:system` |
| Short name | Storage System |
| Description | This namespace collects all storage system-related type definitions. |
| Parent URN | `urn:doe-iri:resource:storage` |
| Status | `provisional` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | Proposed type extensions for storage system resources. |
| Legacy value | `storage` enumeration. |
| Examples | `urn:doe-iri:resource:storage:system`  |
| Notes | These attributes are proposed as examples for the refined `urn:doe-iri:resource:storage:system` resource. |

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of storage systems within the DOE Integrated Research Infrastructure (IRI). A storage system is the managed infrastructure that provides one or more logical storage resources, such as file systems, block storage, or object storage. The storage-system resource provides a common point for describing infrastructure-level characteristics such as storage technology, architecture, capabilities, physical media, and configured capacity.

The storage model intentionally separates the storage infrastructure from the logical storage resources consumers use. A `urn:doe-iri:resource:storage:system` resource therefore describes the underlying storage infrastructure, while filesystem, block, and object resources describe the logical storage interfaces made available by that infrastructure. Relationships between these resources are expressed through IRI link relations rather than by embedding the logical resources within the storage-system definition.

For example, a storage system may provide one or more filesystem resources, each of which may in turn be exposed to compute systems through mount resources:

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        │ iri:provides-filesystem
        ▼
Filesystem
urn:doe-iri:resource:storage:filesystem
        │
        │ iri:has-mount
        ▼
Mount
urn:doe-iri:resource:storage:mount
        │
        │ iri:mounted-on
        ▼
Compute System
urn:doe-iri:resource:compute:system
```

This separation allows the same storage infrastructure to provide multiple logical storage resources without duplicating infrastructure-level information and allows those logical resources to be independently described, discovered, and related to consuming systems.

This document defines the attributes applicable specifically to the storage-system resource. These attributes describe relatively stable characteristics of the storage infrastructure. Characteristics specific to filesystem, block, or object resources are defined by their respective attribute profiles. Dynamic operational information, such as current utilization, available capacity, health, or service availability, is outside the scope of this profile and is represented through the appropriate resource-state mechanisms.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by the Storage System Attribute Profile. It provides a machine-readable classification for the `urn:doe-iri:resource:storage:system` resource type and for those storage-system attributes whose values require consistent semantics across IRI facilities.

The taxonomy distinguishes between the resource being described and the controlled characteristics used to describe that resource. The `urn:doe-iri:resource:storage:system` namespace identifies the resource type itself, while values beneath the `urn:doe-iri:storage` namespace identify standardized attribute values such as storage technology, architecture, capabilities, and physical media.

The taxonomy is not intended to represent the physical topology or containment relationships of a storage system. Relationships between a storage system and the logical resources it provides—such as filesystems, block storage, or object storage—are represented separately using IRI link relations. Similarly, relationships between those logical storage resources and consuming compute systems are outside the scope of this taxonomy.

Only attributes represented by controlled DOE-IRI URNs appear in the taxonomy. Scalar or descriptive attributes such as `capacity_gib`, `vendor`, `product`, and `version` are defined by the attribute profile but are not represented as branches of the URN taxonomy.

The following tree shows the resource type and controlled vocabulary namespaces defined by this profile.

```
urn:doe-iri
│
├── resource
│   └── storage
│       └── system
│
└── storage
    │
    ├── system-technology
    │   ├── lustre
    │   ├── spectrum-scale
    │   ├── ceph
    │   └── beegfs
    │
    ├── system-architecture
    │   ├── distributed
    │   └── clustered
    │
    ├── system-capability
    │   ├── replication
    │   ├── erasure-coding
    │   ├── encryption-at-rest
    │   ├── snapshot
    │   └── data-tiering
    │
    └── media-type
        ├── magnetic-disk
        ├── solid-state
        ├── tape
        └── optical
```
## 4. Storage Attribute Profile

The Storage Attribute Profile defines the set of attributes that MAY be used to describe resources of type urn:doe-iri:resource:storage:system. These attributes provide a consistent, implementation-independent representation of a storage system's characteristics while allowing facilities to expose only those characteristics known and relevant to IRI consumers.

The profile separates the identity of the storage resource from the characteristics of the infrastructure that implements it. Controlled characteristics that require consistent machine-readable semantics, such as storage technology, architecture, capabilities, and media types, are represented using registered DOE-IRI URNs. Other descriptive or quantitative characteristics, such as capacity, vendor, product, and software version, are represented using their corresponding JSON scalar types.

Except for schema_version, attributes in this profile are optional. The absence of an optional attribute indicates that the information has not been provided and MUST NOT be interpreted as implying a particular value or capability. Clients SHOULD rely only on attributes explicitly advertised by the resource.

The attributes defined by this profile describe relatively stable characteristics of the storage system. Dynamic operational information, such as current utilization, available capacity, health, performance, or service availability, is outside the scope of this attribute profile and SHOULD be represented through the corresponding resource state mechanisms.

The following table defines the attributes included in version 1.0.0 of the Storage System Attribute Profile.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version `      | 1.0.0 | string | Version of the profile definition (e.g. "1.0.0"). | yes |
| `storage_technology`   | 1.0.0 | IRI URN string | Identifies the storage platform or implementation. | no |
| `storage_architecture` | 1.0.0 | Array IRI URN string | Describes the architectural characteristics of the storage system. A storage system may advertise multiple architecture values. | no |
| `storage_capabilities` | 1.0.0 | Array IRI URN string | Identifies capabilities provided by the storage infrastructure | no |
| `media_types`          | 1.0.0 | Array IRI URN string | Media type identifies the physical storage medium used to retain data for a storage system resource. | no |
| `capacity_gib`         | 1.0.0 | integer | Configured or usable capacity represented by the system in GiB (2³⁰ bytes) | no |
| `vendor`               | 1.0.0 | string | Identifies the vendor when relevant. | no |
| `product`              | 1.0.0 | string | Identifies the product/platform when relevant. | no |
| `version`              | 1.0.0 | string | Identifies the deployed software/platform version. | no |

### 4.1. Storage System Technology

The `storage_technology` attribute identifies the storage platform or implementation used to provide a `urn:doe-iri:resource:storage:system` resource. It describes the underlying storage-system technology independently of the logical filesystem, block, or object resources that the system may provide.

The value of `storage_technology` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:system-technology` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:system-technology:lustre` | Lustre | A distributed storage and parallel filesystem technology commonly used to provide scalable, high-performance storage for HPC environments. | `provisional` |
| `urn:doe-iri:storage:system-technology:spectrum-scale` | IBM Storage Scale | A clustered storage and filesystem technology, formerly known as IBM Spectrum Scale and GPFS, providing shared data access across multiple systems. | `provisional` |
| `urn:doe-iri:storage:system-technology:ceph` | Ceph | A distributed storage platform capable of providing object, block, and filesystem storage services from a common storage infrastructure. | `provisional` |
| `urn:doe-iri:storage:system-technology:beegfs` | BeeGFS  | A distributed parallel storage and filesystem technology designed to provide scalable, high-performance shared storage across multiple storage servers and clients. | `provisional` |

The `storage_technology` attribute identifies the technology implementing the storage infrastructure and SHOULD NOT be used to identify the logical storage interface exposed to consumers. Logical resources provided by the system are modeled independently using their corresponding resource types and type-specific attributes.

For example, a Ceph storage system may provide multiple logical storage resource types:

```text
Ceph Storage System
storage_technology = urn:doe-iri:storage:system-technology:ceph
    |
    ├── providesFilesystem ──> CephFS Filesystem
    │                          filesystem_technology = cephfs
    │
    ├── providesBlock ────────> RBD Block Storage
    │
    └── providesObject ───────> Ceph Object Gateway
```

Similarly, a Lustre storage system may provide one or more logical filesystems:

```text
Lustre Storage System
storage_technology = urn:doe-iri:storage:system-technology:lustre
    |
    ├── providesFilesystem ──> Scratch Filesystem
    └── providesFilesystem ──> Project Filesystem
```

The storage-system technology is also distinct from vendor and product information. For example:

```json
{
  "storage_technology": "urn:doe-iri:storage:system-technology:lustre",
  "vendor": "DDN",
  "product": "EXAScaler"
}
```

In this example, `lustre` identifies the storage technology, while `vendor` and `product` identify the particular commercial implementation or platform.

Clients SHOULD NOT infer the capabilities, protocols, media types, or logical resources provided by a storage system solely from its `storage_technology` value. Those characteristics SHOULD be advertised explicitly using the appropriate attributes and resource relationships.

### 4.2. Storage System Architecture

The `storage_architecture` attribute describes the architectural characteristics of a `urn:doe-iri:resource:storage:system` resource. It identifies how the storage infrastructure is organized and coordinated at the system level, independently of the logical filesystem, block, or object resources that the system may provide.

A storage system may exhibit more than one architectural characteristic. The `storage_architecture` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:system-architecture` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:system-architecture:distributed` | Distributed | A storage architecture in which data, metadata, or storage services are distributed across multiple systems or nodes that collectively provide the storage service.                                                   | `provisional` |
| `urn:doe-iri:storage:system-architecture:clustered`   | Clustered   | A storage architecture in which multiple systems or nodes operate together as a coordinated storage system, typically sharing responsibility for availability, consistency, service delivery, or resource management. | `provisional` |

Architecture values are not necessarily mutually exclusive. For example, a storage system may be both distributed and clustered if storage responsibilities are distributed across multiple nodes that also operate as a coordinated cluster.

Example:

```json
{
  "storage_architecture": [
    "urn:doe-iri:storage:system-architecture:distributed",
    "urn:doe-iri:storage:system-architecture:clustered"
  ]
}
```

The `storage_architecture` attribute describes the architecture of the **storage system as a whole** and SHOULD NOT be used to describe the architecture of an individual logical filesystem. Filesystem-specific architectural characteristics are represented separately using the `filesystem_architecture` attribute.

For example:

```text
Storage System
    storage_architecture:
        distributed
        clustered
            │
            │ providesFilesystem
            ▼
Filesystem
    filesystem_architecture:
        distributed
```

Although the same architectural term may apply at both levels, the values describe different resources. A distributed storage system means the underlying storage infrastructure is distributed across multiple systems or nodes, whereas a distributed filesystem means the filesystem's data, metadata, or filesystem services are distributed across multiple systems.

Clients SHOULD NOT infer storage capabilities, availability characteristics, performance, or logical storage resources solely from a `storage_architecture` value. Those characteristics SHOULD be advertised explicitly through their corresponding attributes, state resources, or IRI resource relationships.

### 4.3. Storage System Capabilities

The `storage_capabilities` attribute identifies capabilities provided by a `urn:doe-iri:resource:storage:system` resource. These capabilities describe functions supported by the storage infrastructure as a whole and are independent of the particular filesystem, block, or object resources that the system may provide.

A storage system may support multiple capabilities. The `storage_capabilities` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:system-capability` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:system-capability:replication`        | Replication        | The storage system is capable of maintaining multiple copies of data across storage devices, nodes, or locations to support data durability, availability, or recovery.                                                             | `provisional` |
| `urn:doe-iri:storage:system-capability:erasure-coding`     | Erasure coding     | The storage system is capable of protecting data by encoding it into multiple data and parity fragments distributed across storage devices or nodes, allowing data to be reconstructed following the loss of one or more fragments. | `provisional` |
| `urn:doe-iri:storage:system-capability:encryption-at-rest` | Encryption at rest | The storage system is capable of encrypting stored data while it resides on persistent storage media.                                                                                                                               | `provisional` |
| `urn:doe-iri:storage:system-capability:snapshot`           | Snapshot           | The storage system is capable of creating point-in-time representations of stored data that can be used for recovery, rollback, or data protection purposes.                                                                        | `provisional` |
| `urn:doe-iri:storage:system-capability:data-tiering`       | Data tiering       | The storage system is capable of placing or moving data between different storage tiers or media classes based on policy, access patterns, lifecycle, or other criteria.                                                            | `provisional` |

For example:

```json
{
  "storage_capabilities": [
    "urn:doe-iri:storage:system-capability:replication",
    "urn:doe-iri:storage:system-capability:encryption-at-rest",
    "urn:doe-iri:storage:system-capability:snapshot"
  ]
}
```

An advertised capability on the storage system indicates that the underlying infrastructure supports it. It does **not** necessarily indicate that every logical storage resource provided by the system exposes or enables that capability.

For example:

```text
Storage System
    storage_capabilities:
        replication
        snapshot
        encryption-at-rest
            │
            ├── providesFilesystem ──> Scratch Filesystem
            ├── providesFilesystem ──> Home Filesystem
            └── providesBlock ───────> Project Volume
```

The fact that the storage system supports snapshots does not imply that snapshots are available to consumers of every filesystem or block resource. When a capability is meaningful at the logical-resource level, it SHOULD also be advertised using the capability attribute defined for that resource type.

This distinction allows the model to express both infrastructure-level and resource-level capability:

```text
Storage System capability
    "What can the underlying storage infrastructure provide?"

Filesystem capability
    "What capabilities are exposed by this filesystem?"

Block capability
    "What capabilities are exposed by this block resource?"

Object capability
    "What capabilities are exposed by this object resource?"
```

The `storage_capabilities` attribute SHOULD describe relatively stable capabilities of the storage infrastructure and SHOULD NOT be used to represent current operational condition or availability. For example, support for replication is a capability of the resource, while whether replication is currently healthy or degraded is operational state and SHOULD be represented by the corresponding state resource.

Capabilities also SHOULD NOT be inferred solely from the value of `storage_technology`. Although a particular technology may commonly support specific features, a facility SHOULD explicitly advertise only capabilities that are supported and applicable to the deployed storage system.

The capability vocabulary is intended to be extensible. Additional capability URNs SHOULD be registered when a capability represents a meaningful, implementation-independent characteristic that an IRI client may need to discover or reason about.

### 4.4. Storage Media Types

The `media_types` attribute identifies the physical storage media used to retain data within a `urn:doe-iri:resource:storage:system` resource. It describes the underlying media used by the storage infrastructure, independent of the storage technology, architecture, logical storage resource type, or intended storage tier.

A storage system may use more than one type of physical media. The `media_types` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:media-type` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:media-type:magnetic-disk` | Magnetic disk | Storage media that retains data magnetically on rotating disks, such as hard disk drives (HDDs). | `provisional` |
| `urn:doe-iri:storage:media-type:solid-state`   | Solid-state   | Nonvolatile electronic storage media with no moving mechanical components, such as flash-based solid-state drives (SSDs). | `provisional` |
| `urn:doe-iri:storage:media-type:tape`          | Tape          | Storage media that retains data magnetically on tape and is generally optimized for high-capacity, sequential access and long-term data retention. | `provisional` |
| `urn:doe-iri:storage:media-type:optical`       | Optical       | Storage media that retains data using optically readable media, such as CD, DVD, Blu-ray, or other optical storage technologies. | `provisional` |

For example, a storage system containing both solid-state and magnetic-disk storage may advertise:

```json
{
  "media_types": [
    "urn:doe-iri:storage:media-type:solid-state",
    "urn:doe-iri:storage:media-type:magnetic-disk"
  ]
}
```

The `media_types` attribute describes the physical media available within or backing the storage system. The presence of multiple values does not indicate how data is distributed between those media types or which logical storage resources use a particular medium.

For example:

```text
Storage System
    media_types:
        solid-state
        magnetic-disk
        tape
            │
            ├── providesFilesystem ──> Scratch Filesystem
            ├── providesFilesystem ──> Project Filesystem
            └── providesFilesystem ──> Archive Filesystem
```

In this example, the storage-system definition indicates that all three media types are present somewhere within the infrastructure. It does not imply that every filesystem uses all three media types.

Where the backing media of a particular logical storage resource is known and is meaningful to IRI consumers, the `media_types` attribute MAY also be associated with that logical storage resource. This allows a facility to provide more specific information when appropriate:

```text
Storage System
    media_types:
        solid-state
        magnetic-disk

        ├── Scratch Filesystem
        │       media_types:
        │           solid-state
        │
        └── Project Filesystem
                media_types:
                    magnetic-disk
```

A client SHOULD NOT infer a resource's performance, latency, durability, persistence, or storage tier solely from its media type. These are independent characteristics. For example, `solid-state` identifies the physical storage medium; it does not inherently indicate that the storage resource is a scratch tier or has a particular performance level.

The media-type vocabulary is intended to describe the fundamental physical medium rather than its interface, protocol, implementation technology, or intended use.

The attribute SHOULD be omitted when the underlying storage media are unknown, cannot be meaningfully determined at the resource's level of abstraction, or would expose implementation details that the facility does not intend to publish. Clients SHOULD NOT assume a particular media type when `media_types` is absent.

## 5. Storage-System JSON Schema

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
      example: urn:doe-iri:storage:system-technology:lustre

    StorageSystemAttributes:
      type: object
      description: >
        Attributes describing a storage system resource with resource type
        urn:doe-iri:resource:storage:system.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          description: >
            Version of the storage system attribute profile definition.
          enum:
            - "1.0.0"
          example: "1.0.0"

        storage_technology:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the storage platform or implementation.
          example: urn:doe-iri:storage:system-technology:lustre

		storage_architecture:
		  type: array
		  description: >
		    Describes the architectural characteristics of the storage system.
		    A storage system may advertise more than one architecture value.
		  uniqueItems: true
		  items:
		    $ref: '#/components/schemas/IriUrn'
		  example:
		    - urn:doe-iri:storage:system-architecture:distributed
		    - urn:doe-iri:storage:system-architecture:clustered

        storage_capabilities:
          type: array
          description: >
            Identifies capabilities provided by the storage infrastructure.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:system-capability:replication
            - urn:doe-iri:storage:system-capability:encryption-at-rest

        media_types:
          type: array
          description: >
            Identifies the physical storage media used to retain data
            for the storage system resource.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:media-type:solid-state
            - urn:doe-iri:storage:media-type:magnetic-disk

        capacity_gib:
          type: integer
          format: int64
          minimum: 0
          description: >
            Configured or usable storage capacity represented by the
            system, expressed in GiB (2^30 bytes).
          example: 10485760

        vendor:
          type: string
          description: >
            Identifies the storage system vendor when relevant.
          example: DDN

        product:
          type: string
          description: >
            Identifies the storage product or platform when relevant.
          example: EXAScaler

        version:
          type: string
          description: >
            Identifies the deployed software or platform version.
          example: "6.0"
```

## 6. Example Storage-System JSON Instance

```json
{
  "schema_version": "1.0.0",
  "storage_technology": "urn:doe-iri:storage:system-technology:lustre",
  "storage_architecture": [
    "urn:doe-iri:storage:system-architecture:distributed",
    "urn:doe-iri:storage:system-architecture:clustered"
  ],
  "storage_capabilities": [
    "urn:doe-iri:storage:system-capability:replication",
    "urn:doe-iri:storage:system-capability:encryption-at-rest"
  ],
  "media_types": [
    "urn:doe-iri:storage:media-type:solid-state",
    "urn:doe-iri:storage:media-type:magnetic-disk"
  ],
  "capacity_gib": 10485760,
  "vendor": "DDN",
  "product": "EXAScaler",
  "version": "6.0"
}
```
---

*DOE Integrated Research Infrastructure — URN Registry: Storage System*
