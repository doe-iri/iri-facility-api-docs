# Type Registry: `urn:doe-iri:resource:storage`

This document defines the `urn:doe-iri:resource:storage` resource type hierarchy and serves as the entry point for the DOE-IRI storage resource model.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field             | Description                                                                                                                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| URN               | `urn:doe-iri:resource:storage`                                                                                                                                                                     |
| Short name        | Storage                                                                                                                                                                                            |
| Description       | This namespace collects storage-related resource type definitions.                                                                                                                                 |
| Parent URN        | `urn:doe-iri:resource`                                                                                                                                                                             |
| Status            | `active`                                                                                                                                                                                           |
| Introduced        | IRI v2.0                                                                                                                                                                                           |
| Change controller | IRI technical subcommittee.                                                                                                                                                                        |
| Reference         | Proposed type extensions for storage resources.                                                                                                                                                    |
| Legacy value      | `storage` enumeration.                                                                                                                                                                             |
| Examples          | `urn:doe-iri:resource:storage:filesystem`                                                                                                                                                          |
| Notes             | This namespace defines the provisional child resource types used to refine the generic `storage` resource type. Type-specific characteristics are defined by the corresponding attribute profiles. |

## 2. Introduction

The purpose of the IRI storage model is to provide a consistent, implementation-independent way to describe storage infrastructure and the logical storage resources made available by an IRI facility.

This document defines the top-level storage resource taxonomy and the relationships between its primary resource types. Detailed characteristics and controlled vocabularies applicable to each resource type are defined by the corresponding attribute profiles referenced in Section 5. This document therefore serves as the entry point for the IRI storage model rather than defining all characteristics of each storage resource.

The storage model separates the infrastructure that **provides storage** from the logical storage resources that consumers **use** and from the mechanisms through which those resources are **exposed or connected** to consuming systems.

A primary goal of this separation is to avoid embedding storage topology, access configuration, implementation details, or usage semantics into a single generic storage resource. Independently meaningful components are represented as resources with their own identities and characteristics, while relationships between those resources are expressed explicitly using IRI link relations.

The storage model follows the broader IRI separation between resource identity, resource characteristics, resource relationships, and operational state:

```text
Resource Type
    "What kind of resource is this?"

Attributes
    "What relatively stable characteristics does this resource have?"

Relationships
    "How is this resource related to other resources?"

State
    "What is happening with this resource now?"
```

Resource type URNs identify what kind of resource is being described. Attribute profiles describe the characteristics of that resource. IRI link relations describe topology and relationships between independently identifiable resources. Dynamic information such as availability, utilization, health, or current performance is represented separately through the appropriate resource-state mechanisms.

### 2.1. Storage Resource Model

The storage model defines a **Storage System** as the managed infrastructure that provides one or more logical storage resources. Those logical resources may expose filesystem, block, or object storage semantics.

The general model is:

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        ├── iri:providesFilesystem ──> Filesystem
        │                               │
        │                               │ iri:hasMount
        │                               ▼
        │                             Mount
        │                               │
        │                               │ iri:mountedOn
        │                               ▼
        │                         Compute System
        │
        ├── iri:providesBlock ────────> Block Storage
        │
        └── iri:providesObject ───────> Object Storage
```

This model distinguishes the infrastructure providing storage from the logical storage interfaces presented to consumers.

A **Storage System** represents managed infrastructure that provides storage services. A storage system may provide one or more filesystem, block, or object-storage resources and may represent infrastructure based on technologies such as Lustre, IBM Storage Scale, Ceph, or another storage platform.

A **Filesystem** represents a logical file-oriented storage resource that organizes data as files and directories within a hierarchical namespace. Filesystems may define characteristics such as scope, architecture, capabilities, filesystem technology, supported protocols, storage tier, and backing media.

A **Mount** represents the exposure of a filesystem within the namespace of a particular consuming system. A mount may identify characteristics specific to that exposure, such as a mount path and access mode. A mount is not itself another type of storage medium; it represents how a filesystem is made accessible to another resource.

A **Block Storage** resource represents a logical storage resource that exposes addressable blocks or volumes. Block resources may be consumed by operating systems, filesystems, databases, or applications and may be presented to consuming systems using block-storage protocols or storage fabrics.

An **Object Storage** resource represents a logical storage resource that manages data as independently addressable objects with associated metadata. Object resources are typically accessed through object-storage APIs and service endpoints rather than through filesystem mounts.

### 2.2. Filesystem Example

Filesystem storage includes an additional resource abstraction because the same logical filesystem may be exposed differently on multiple consuming systems.

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        │ iri:providesFilesystem
        ▼
Filesystem
urn:doe-iri:resource:storage:filesystem
        │
        │ iri:hasMount
        ▼
Mount
urn:doe-iri:resource:storage:mount
        │
        │ iri:mountedOn
        ▼
Compute System
urn:doe-iri:resource:compute:system
```

This separation allows a single storage system to provide multiple filesystems, a filesystem to be exposed to multiple consuming systems, and each mount to describe system-specific access information without duplicating the filesystem definition itself.

For example, a facility may operate a single storage system that provides both Scratch and Home filesystems. The Scratch filesystem may appear as `/scratch` on one compute system and `/global/scratch` on another. In this model, the filesystem is defined once while separate mount resources describe each exposure.

### 2.3. Example Facility Topology

The following theoretical example illustrates how a facility named `NERSC` could expose logical filesystems from a storage system to a compute system named `Perlmutter`.

```text
NERSC Storage System
resource_type = urn:doe-iri:resource:storage:system

        │ iri:providesFilesystem
        │
        ├──────────────────────────────────────┐
        ▼                                      ▼

Scratch Filesystem                       Home Filesystem
resource_type =                          resource_type =
  urn:doe-iri:resource:storage:filesystem  urn:doe-iri:resource:storage:filesystem

tier =                                   tier =
  urn:doe-iri:storage:tier:scratch         urn:doe-iri:storage:tier:home

        │                                      │
        │ iri:hasMount                         │ iri:hasMount
        ▼                                      ▼

Perlmutter Scratch Mount                Perlmutter Home Mount
resource_type =                         resource_type =
  urn:doe-iri:resource:storage:mount      urn:doe-iri:resource:storage:mount

mount_path = /pscratch                  mount_path = /global/homes

        │                                      │
        └──────────── iri:mountedOn ────────────┘
                            │
                            ▼
                       Perlmutter
                       resource_type =
                         urn:doe-iri:resource:compute:system
```

The example illustrates an important property of the model: the filesystem resource describes the logical storage resource, while the mount resource describes how that filesystem is exposed to a particular consuming system.

## 3. Taxonomy

The following taxonomy defines the resource types registered beneath `urn:doe-iri:resource:storage`.

The hierarchy represents **resource type refinement only**. It does not represent physical containment, provisioning, attachment, mounting, or other topology relationships between storage resources. Those relationships are represented using IRI link relations.

```text
urn:doe-iri:resource:storage
│
├── system
│   └── "What infrastructure provides the storage?"
│
├── filesystem
│   └── "What logical filesystem can I use?"
│
├── mount
│   └── "Where and how is a filesystem exposed?"
│
├── block
│   └── "What logical block-storage resource can I use?"
│
└── object
    └── "What logical object-storage resource can I use?"
```

Although these resource types appear as siblings in the taxonomy, their operational and topology relationships are expressed separately. For example, a storage system may provide a filesystem, but `filesystem` is not a subtype of `system`; both are refinements of the generic storage resource type.

## 4. Storage Resource Types

The following URNs are registered as child resource types of `urn:doe-iri:resource:storage`. Each type refines the generic storage resource into a more specific resource abstraction and links to an attribute profile defining the characteristics applicable to that resource type.

| URN                                                                                          | Short name       | Description                                                                                                                                                         | Status        |
| -------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| [`urn:doe-iri:resource:storage:system`](./urn-registry-attributes-storage-system.md)         | Storage System   | A managed storage infrastructure system that provides one or more logical storage resources, such as filesystems, block volumes, or object-storage services.        | `provisional` |
| [`urn:doe-iri:resource:storage:filesystem`](./urn-registry-attributes-storage-filesystem.md) | Filesystem       | A logical storage resource that organizes data as files and directories within a hierarchical namespace and exposes filesystem-based access semantics.              | `provisional` |
| [`urn:doe-iri:resource:storage:mount`](./urn-registry-attributes-storage-mount.md)           | Filesystem Mount | A representation of a filesystem being exposed to a particular consuming system at a specific mount point or namespace location.                                    | `provisional` |
| [`urn:doe-iri:resource:storage:block`](./urn-registry-attributes-storage-block.md)           | Block Storage    | A logical storage resource that presents raw, addressable blocks or volumes to a host or system, typically for use by a filesystem, database, or other application. | `provisional` |
| [`urn:doe-iri:resource:storage:object`](./urn-registry-attributes-storage-object.md)         | Object Storage   | A logical storage resource that manages data as independently addressable objects with associated metadata, typically accessed through an object-storage API.       | `provisional` |

The linked attribute profiles define the resource-specific characteristics and controlled DOE-IRI vocabularies applicable to each type. Shared concepts, such as storage tier and physical media type, may be reused across multiple storage resource profiles where those concepts are meaningful at that resource's level of abstraction.

## 5. Storage Controlled Attribute Vocabulary

The storage attribute profiles define controlled DOE-IRI URN vocabularies for characteristics that require consistent, machine-readable semantics across IRI facilities. These URNs are used as attribute values when describing storage-system, filesystem, mount, block, and object-storage resources.

Controlled attribute URNs are distinct from the resource type URNs defined in Section 4. A resource type URN identifies **what kind of resource is being represented**, while a controlled attribute URN identifies a standardized **characteristic, capability, technology, protocol, classification, or other property of that resource**. For example:

```text
Resource type:
    urn:doe-iri:resource:storage:filesystem

Attribute:
    filesystem_technology

Controlled attribute value:
    urn:doe-iri:storage:filesystem-technology:lustre
```

Only attributes that require a registered controlled vocabulary are represented by URNs in this section. Attributes whose values are naturally represented using ordinary JSON types, such as `capacity_gib`, `vendor`, `product`, `version`, `mount_path`, or endpoint URLs, are defined by their applicable attribute profiles but are not part of the controlled attribute vocabulary.

Controlled vocabularies may be specific to a particular storage resource type or may be shared across multiple resource types. For example, filesystem technology and filesystem capabilities apply specifically to filesystem resources, while storage tier and media type may be applicable to multiple kinds of storage resources where those concepts are meaningful. The individual attribute profiles define the resource types to which each vocabulary applies and the semantics associated with each value.

The following table enumerates the controlled storage attribute URNs currently defined by the Storage System, Filesystem, Mount, Block Storage, and Object Storage attribute profiles. Each URN links to the attribute profile that defines its meaning and usage requirements. Unless otherwise indicated, the values are currently registered with `provisional` status.

| URN                                                              | Short name              | Description                                                                                                                                                                                                                         | Status        |
| ---------------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| [`urn:doe-iri:storage:system-technology:lustre`](./urn-registry-attributes-storage-system.md) | Lustre                  | A distributed storage and parallel filesystem technology commonly used to provide scalable, high-performance storage for HPC environments.                                                                                          | `provisional` |
| [`urn:doe-iri:storage:system-technology:spectrum-scale`](./urn-registry-attributes-storage-system.md) | IBM Storage Scale       | A clustered storage and filesystem technology, formerly known as IBM Spectrum Scale and GPFS, providing shared data access across multiple systems.                                                                                 | `provisional` |
| [`urn:doe-iri:storage:system-technology:ceph`](./urn-registry-attributes-storage-system.md) | Ceph                    | A distributed storage platform capable of providing object, block, and filesystem storage services from a common storage infrastructure.                                                                                            | `provisional` |
| [`urn:doe-iri:storage:system-technology:beegfs`](./urn-registry-attributes-storage-system.md) | BeeGFS                  | A distributed parallel storage and filesystem technology designed to provide scalable, high-performance shared storage across multiple storage servers and clients.                                                                 | `provisional` |
| [`urn:doe-iri:storage:system-architecture:distributed`](./urn-registry-attributes-storage-system.md) | Distributed             | A storage architecture in which data, metadata, or storage services are distributed across multiple systems or nodes that collectively provide the storage service.                                                                 | `provisional` |
| [`urn:doe-iri:storage:system-architecture:clustered`](./urn-registry-attributes-storage-system.md) | Clustered               | A storage architecture in which multiple systems or nodes operate together as a coordinated storage system, typically sharing responsibility for availability, consistency, service delivery, or resource management.               | `provisional` |
| [`urn:doe-iri:storage:system-capability:replication`](./urn-registry-attributes-storage-system.md) | Replication             | The storage system is capable of maintaining multiple copies of data across storage devices, nodes, or locations to support data durability, availability, or recovery.                                                             | `provisional` |
| [`urn:doe-iri:storage:system-capability:erasure-coding`](./urn-registry-attributes-storage-system.md) | Erasure coding          | The storage system is capable of protecting data by encoding it into multiple data and parity fragments distributed across storage devices or nodes, allowing data to be reconstructed following the loss of one or more fragments. | `provisional` |
| [`urn:doe-iri:storage:system-capability:encryption-at-rest`](./urn-registry-attributes-storage-system.md) | Encryption at rest      | The storage system is capable of encrypting stored data while it resides on persistent storage media.                                                                                                                               | `provisional` |
| [`urn:doe-iri:storage:system-capability:snapshot`](./urn-registry-attributes-storage-system.md) | Snapshot                | The storage system is capable of creating point-in-time representations of stored data that can be used for recovery, rollback, or data protection purposes.                                                                        | `provisional` |
| [`urn:doe-iri:storage:system-capability:data-tiering`](./urn-registry-attributes-storage-system.md) | Data tiering            | The storage system is capable of placing or moving data between different storage tiers or media classes based on policy, access patterns, lifecycle, or other criteria.                                                            | `provisional` |
| [`urn:doe-iri:storage:filesystem-scope:local`](./urn-registry-attributes-storage-filesystem.md) | Local                   | A filesystem whose storage is directly accessible to and primarily managed by a single host or operating-system instance.                                                                                                           | `provisional` |
| [`urn:doe-iri:storage:filesystem-scope:network`](./urn-registry-attributes-storage-filesystem.md) | Network                 | A filesystem made available to one or more clients over a network through a filesystem service or client/server filesystem interface.                                                                                               | `provisional` |
| [`urn:doe-iri:storage:filesystem-architecture:distributed`](./urn-registry-attributes-storage-filesystem.md) | Distributed             | A filesystem architecture in which data, metadata, or filesystem services are distributed across multiple systems while presenting a unified filesystem namespace to consumers.                                                     | `provisional` |
| [`urn:doe-iri:storage:filesystem-architecture:clustered`](./urn-registry-attributes-storage-filesystem.md) | Clustered               | A filesystem architecture in which multiple hosts or nodes coordinate access to shared filesystem resources using mechanisms for maintaining consistent filesystem state, metadata, locking, or cache coherence.                    | `provisional` |
| [`urn:doe-iri:storage:filesystem-capability:parallel-io`](./urn-registry-attributes-storage-filesystem.md) | Parallel I/O            | The filesystem supports concurrent I/O from multiple clients and can distribute I/O across multiple storage resources to provide scalable aggregate throughput.                                                                     | `provisional` |
| [`urn:doe-iri:storage:filesystem-capability:direct-io`](./urn-registry-attributes-storage-filesystem.md) | Direct I/O              | The filesystem supports I/O mechanisms that bypass or minimize use of the operating system page cache, allowing more direct transfer between application buffers and storage.                                                       | `provisional` |
| [`urn:doe-iri:storage:filesystem-capability:asynchronous-io`](./urn-registry-attributes-storage-filesystem.md) | Asynchronous I/O        | The filesystem supports submission of I/O operations without requiring the submitting execution context to block until each operation completes.                                                                                    | `provisional` |
| [`urn:doe-iri:storage:filesystem-capability:data-striping`](./urn-registry-attributes-storage-filesystem.md) | Data striping           | The filesystem supports distributing portions of a file across multiple storage devices or targets to enable concurrent access and increased aggregate throughput.                                                                  | `provisional` |
| [`urn:doe-iri:storage:filesystem-capability:shared-namespace`](./urn-registry-attributes-storage-filesystem.md) | Shared namespace        | The filesystem provides a common filesystem namespace accessible by multiple clients with a consistent file and directory hierarchy.                                                                                                | `provisional` |
| [`urn:doe-iri:storage:filesystem-technology:lustre`](./urn-registry-attributes-storage-filesystem.md) | Lustre                  | An open-source distributed parallel filesystem designed to provide scalable, high-performance shared storage, particularly for high-performance computing environments.                                                             | `provisional` |
| [`urn:doe-iri:storage:filesystem-technology:spectrum-scale`](./urn-registry-attributes-storage-filesystem.md) | IBM Storage Scale       | A clustered filesystem technology, formerly known as IBM Spectrum Scale and GPFS, supporting concurrent shared filesystem access across multiple systems.                                                                           | `provisional` |
| [`urn:doe-iri:storage:filesystem-technology:cephfs`](./urn-registry-attributes-storage-filesystem.md) | CephFS                  | A distributed POSIX-compatible filesystem built on the Ceph distributed storage platform and providing a shared hierarchical namespace.                                                                                             | `provisional` |
| [`urn:doe-iri:storage:filesystem-technology:beegfs`](./urn-registry-attributes-storage-filesystem.md) | BeeGFS                  | A distributed parallel filesystem designed to provide scalable, high-performance shared filesystem access across multiple clients and storage servers.                                                                              | `provisional` |
| [`urn:doe-iri:storage:filesystem-protocol:nfs`](./urn-registry-attributes-storage-filesystem.md) | NFS                     | The Network File System protocol family for providing remote filesystem access to files and directories over a network.                                                                                                             | `provisional` |
| [`urn:doe-iri:storage:filesystem-protocol:smb`](./urn-registry-attributes-storage-filesystem.md) | SMB                     | The Server Message Block protocol family for providing network-based file and directory sharing.                                                                                                                                    | `provisional` |
| [`urn:doe-iri:storage:filesystem-protocol:webdav`](./urn-registry-attributes-storage-filesystem.md) | WebDAV                  | An HTTP-based protocol extension that supports remote access and management of files and other resources.                                                                                                                           | `provisional` |
| [`urn:doe-iri:storage:mount-access-mode:read-only`](./urn-registry-attributes-storage-mount.md) | Read only               | The mount permits consumers to read filesystem content but does not permit modification of filesystem data through this mount.                                                                                                      | `provisional` |
| [`urn:doe-iri:storage:mount-access-mode:read-write`](./urn-registry-attributes-storage-mount.md) | Read/write              | The mount permits consumers to read and, subject to applicable authorization and filesystem permissions, modify filesystem content through this mount.                                                                              | `provisional` |
| [`urn:doe-iri:storage:block-scope:local`](./urn-registry-attributes-storage-block.md) | Local                   | A block storage resource whose storage is directly attached to or locally available within a single host or system.                                                                                                                 | `provisional` |
| [`urn:doe-iri:storage:block-scope:network`](./urn-registry-attributes-storage-block.md) | Network                 | A block storage resource presented to one or more consuming systems through a network-based block-storage service or storage fabric.                                                                                                | `provisional` |
| [`urn:doe-iri:storage:block-protocol:iscsi`](./urn-registry-attributes-storage-block.md) | iSCSI                   | A block-storage protocol that transports SCSI commands over TCP/IP networks, allowing remote storage resources to be presented to consumers as block devices.                                                                       | `provisional` |
| [`urn:doe-iri:storage:block-protocol:fibre-channel`](./urn-registry-attributes-storage-block.md) | Fibre Channel           | A storage-network access mechanism that uses Fibre Channel fabrics, commonly carrying SCSI block-storage commands using Fibre Channel Protocol (FCP).                                                                               | `provisional` |
| [`urn:doe-iri:storage:block-protocol:nvme-o-f`](./urn-registry-attributes-storage-block.md) | NVMe over Fabrics       | A protocol family that extends NVMe block-storage command semantics across network fabrics, allowing remote NVMe storage to be accessed with semantics similar to locally attached NVMe devices.                                    | `provisional` |
| [`urn:doe-iri:storage:block-access-mode:exclusive`](./urn-registry-attributes-storage-block.md) | Exclusive               | The block resource is intended to be actively attached to or accessed by a single consuming system at a time.                                                                                                                       | `provisional` |
| [`urn:doe-iri:storage:block-access-mode:shared`](./urn-registry-attributes-storage-block.md) | Shared                  | The block resource supports concurrent attachment or access by multiple consuming systems.                                                                                                                                          | `provisional` |
| [`urn:doe-iri:storage:block-provisioning:thin`](./urn-registry-attributes-storage-block.md) | Thin provisioning       | A provisioning model in which the logical capacity presented to a block resource may exceed the physical storage initially allocated to it, with physical capacity allocated as data is written.                                    | `provisional` |
| [`urn:doe-iri:storage:block-provisioning:thick`](./urn-registry-attributes-storage-block.md) | Thick provisioning      | A provisioning model in which physical storage capacity corresponding to the requested logical capacity is allocated or reserved when the block resource is provisioned.                                                            | `provisional` |
| [`urn:doe-iri:storage:block-capability:snapshot`](./urn-registry-attributes-storage-block.md) | Snapshot                | The block resource supports creation of point-in-time representations of its stored block data for recovery, rollback, cloning, or other data-management purposes.                                                                  | `provisional` |
| [`urn:doe-iri:storage:block-capability:clone`](./urn-registry-attributes-storage-block.md) | Clone                   | The block resource supports creation of a new independently addressable block resource based on the contents of an existing block resource or snapshot.                                                                             | `provisional` |
| [`urn:doe-iri:storage:block-capability:multipath`](./urn-registry-attributes-storage-block.md) | Multipath               | The block resource supports access through multiple I/O paths between consuming systems and the storage infrastructure for resiliency, failover, or load distribution.                                                              | `provisional` |
| [`urn:doe-iri:storage:object-api:s3`](./urn-registry-attributes-storage-object.md) | S3                      | An object-storage API model in which objects are addressed by keys within buckets and manipulated using S3-compatible operations.                                                                                                   | `provisional` |
| [`urn:doe-iri:storage:object-api:swift`](./urn-registry-attributes-storage-object.md) | Swift                   | An object-storage API model in which objects are organized within containers and accessed using the OpenStack Swift API.                                                                                                            | `provisional` |
| [`urn:doe-iri:storage:object-technology:ceph-rgw`](./urn-registry-attributes-storage-object.md) | Ceph Object Gateway     | An object-storage implementation provided by the Ceph Object Gateway (RGW), capable of exposing object data through supported object-storage APIs.                                                                                  | `provisional` |
| [`urn:doe-iri:storage:object-technology:openstack-swift`](./urn-registry-attributes-storage-object.md) | OpenStack Swift         | A distributed object-storage implementation provided by the OpenStack Swift platform.                                                                                                                                               | `provisional` |
| [`urn:doe-iri:storage:object-technology:amazon-s3`](./urn-registry-attributes-storage-object.md) | Amazon S3               | The Amazon S3 managed object-storage platform.                                                                                                                                                                                      | `provisional` |
| [`urn:doe-iri:storage:object-consistency:strong-read-after-write`](./urn-registry-attributes-storage-object.md) | Strong read-after-write | Successful writes are reflected by subsequent reads according to the consistency guarantees applicable to the object-storage resource.                                                                                              | `provisional` |
| [`urn:doe-iri:storage:object-consistency:eventual`](./urn-registry-attributes-storage-object.md) | Eventual consistency    | Updates may not be immediately visible to all subsequent operations, but replicas or service views are expected to converge over time in the absence of additional updates.                                                         | `provisional` |
| [`urn:doe-iri:storage:object-capability:multipart-upload`](./urn-registry-attributes-storage-object.md) | Multipart upload        | The object resource supports creation of an object by uploading its data as multiple independently transferred parts that are subsequently assembled into the completed object.                                                     | `provisional` |
| [`urn:doe-iri:storage:object-capability:versioning`](./urn-registry-attributes-storage-object.md) | Object versioning       | The object resource supports retaining and distinguishing multiple versions of an object associated with the same object key or identifier.                                                                                         | `provisional` |
| [`urn:doe-iri:storage:object-capability:object-lock`](./urn-registry-attributes-storage-object.md) | Object lock             | The object resource supports controls that prevent an object or object version from being modified or deleted for a defined period or under an applicable retention policy.                                                         | `provisional` |
| [`urn:doe-iri:storage:tier:home`](./urn-registry-attributes-storage-filesystem.md) | Home                    | Persistent user-oriented storage intended for files such as configuration data, source code, personal working data, and other user-specific content.                                                                                | `provisional` |
| [`urn:doe-iri:storage:tier:project`](./urn-registry-attributes-storage-filesystem.md) | Project                 | Shared persistent storage allocated to a project, collaboration, or team for ongoing project data and collaborative use.                                                                                                            | `provisional` |
| [`urn:doe-iri:storage:tier:scratch`](./urn-registry-attributes-storage-filesystem.md) | Scratch                 | High-performance temporary storage intended for active workloads, intermediate data, and transient working files, typically subject to limited retention or purge policies.                                                         | `provisional` |
| [`urn:doe-iri:storage:tier:campaign`](./urn-registry-attributes-storage-filesystem.md) | Campaign                | Intermediate-term storage intended to retain data associated with a scientific campaign, experiment, project, or allocation for the duration of that activity.                                                                      | `provisional` |
| [`urn:doe-iri:storage:tier:archive`](./urn-registry-attributes-storage-filesystem.md) | Archive                 | Storage intended for durable, long-term retention of data that is accessed less frequently and is not expected to provide active-tier performance characteristics.                                                                  | `provisional` |
| [`urn:doe-iri:storage:media-type:magnetic-disk`](./urn-registry-attributes-storage-system.md) | Magnetic disk           | Storage media that retains data magnetically on rotating disks, such as hard disk drives (HDDs).                                                                                                                                    | `provisional` |
| [`urn:doe-iri:storage:media-type:solid-state`](./urn-registry-attributes-storage-system.md) | Solid-state             | Nonvolatile electronic storage media with no moving mechanical components, such as flash-based solid-state drives (SSDs).                                                                                                           | `provisional` |
| [`urn:doe-iri:storage:media-type:tape`](./urn-registry-attributes-storage-system.md) | Tape                    | Storage media that retains data magnetically on tape and is generally optimized for high-capacity, sequential access and long-term data retention.                                                                                  | `provisional` |
| [`urn:doe-iri:storage:media-type:optical`](./urn-registry-attributes-storage-system.md) | Optical                 | Storage media that retains data using optically readable media, such as CD, DVD, Blu-ray, or other optical storage technologies.                                                                                                    | `provisional` |

## 6. Storage Resource Relationships

Relationships between storage resources, and incoming relationships from other resource domains, are represented using registered IRI link relations. These relationships describe topology and access without embedding one resource definition inside another.

| Relationship | Source | Target | Cardinality | Target Stability | Authorization Affects Visibility | Description |
|---|---|---|---|---|---|---|
| [`iri:providesFilesystem`](./link-profile-provides-filesystem.md) | Storage System | Filesystem | `0..*` | Static | Yes | Indicates that the storage system provides the identified logical filesystem resource. |
| [`iri:providesBlock`](./link-profile-provides-block.md) | Storage System | Block Storage | `0..*` | Static | Yes | Indicates that the storage system provides the identified logical block-storage resource. |
| [`iri:providesObject`](./link-profile-provides-object.md) | Storage System | Object Storage | `0..*` | Static | Yes | Indicates that the storage system provides the identified logical object-storage resource. |
| [`iri:hasMount`](./link-profile-has-mount.md) | Filesystem | Mount | `0..*` | Relatively static | Yes | Indicates that the filesystem is exposed through the identified mount resource. |
| [`iri:mountedOn`](./link-profile-mounted-on.md) | Mount | Compute System | `1` | Static | Yes | Indicates the consuming system on which the filesystem represented by the mount is exposed. |
| [`iri:attachedTo`](./link-profile-attached-to.md) | Block Storage | Compute System or Compute Node | `0..1` exclusive / `0..*` shared | Static target; dynamic state separate | Yes | Indicates that the block resource is attached or presented to the identified consuming resource. |
| [`iri:accessesMount`](./link-profile-accesses-mount.md) | DTN Service | Filesystem Mount | `0..*` targets from a DTN service | Relatively static configured access topology | Yes | Incoming cross-domain relationship indicating that the DTN service is configured to access the identified mount for transfer operations. |

Relationships describe independently identifiable resources and SHOULD NOT be duplicated as ordinary attributes when an IRI link relation is defined for the relationship.

Object-storage service endpoints are described by the Object Storage Attribute Profile and are not modeled as independent resources unless a future IRI use case requires endpoint-specific identity, relationships, lifecycle, or operational state.

---

*DOE Integrated Research Infrastructure — URN Registry: Storage*
