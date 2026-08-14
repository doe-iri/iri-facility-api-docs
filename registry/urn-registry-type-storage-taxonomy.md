# 1. Taxonomy

The following storage taxonomy defines the resource types used to model storage within an IRI facility.

```
urn:doe-iri
│
├── resource
│   └── storage
│       ├── system     - "What infrastructure provides the storage?"
│       ├── filesystem - "What logical filesystem can I use?"
│       ├── mount      - "Where/how is a filesystem exposed on a consuming system?"
│       ├── block      - "What logical block storage resource can I use?"
│       └── object     - "What logical object storage resource can I use?"
│
└── storage            - The storage controlled attribute vocabulary
    │
    │   SYSTEM ATTRIBUTES
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
    |   FILESYSTEM ATTRIBUTES
    |
    ├── filesystem-scope
    │   ├── local
    │   └── network
    │
    ├── filesystem-architecture
    │   ├── distributed
    │   └── clustered
    │
    ├── filesystem-capability
    │   ├── parallel-io
    │   ├── direct-io
    │   ├── asynchronous-io
    │   ├── data-striping
    │   └── shared-namespace
    │
    ├── filesystem-technology
    │   ├── lustre
    │   ├── spectrum-scale
    │   ├── cephfs
    │   └── beegfs
    │
    ├── filesystem-protocol
    │   ├── nfs
    │   ├── smb
    │   └── webdav
    │
    |   MOUNT ATTRIBUTES
    |
    ├── mount-access-mode
    │   ├── read-only
    │   └── read-write
    │
    ├── NOTE: Mount resources reuse the filesystem-protocol vocabulary above.
    |
    |   BLOCK STORAGE ATTRIBUTES
    |
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
    │   OBJECT STORAGE ATTRIBUTES
    |
    ├── object-api
    │   ├── s3
    │   └── swift
    │
    ├── object-technology
    │   ├── ceph-rgw
    │   ├── openstack-swift
    │   └── amazon-s3
    │
    ├── object-consistency
    │   ├── strong-read-after-write
    │   └── eventual
    │
    ├── object-capability
    │   ├── multipart-upload
    │   ├── versioning
    │   └── object-lock
    │
    │   COMMON STORAGE ATTRIBUTES
    |
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

# 2. Storage URN Definitions
| URN                                                              | Short name              | Description                                                                                                                                                                                                                         | Status        |
| ---------------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| [`urn:doe-iri:resource:storage:system`](./urn-registry-attributes-storage-system.md) | Storage System          | This namespace collects all storage system-related type definitions.                                                                                                                                                                | `provisional` |
| [`urn:doe-iri:resource:storage:filesystem`](./urn-registry-attributes-storage-filesystem.md) | Filesystem              | This namespace collects filesystem-related type definitions.                                                                                                                                                                        | `provisional` |
| [`urn:doe-iri:resource:storage:mount`](./urn-registry-attributes-storage-mount.md) | Filesystem Mount        | This namespace collects filesystem mount-related type definitions.                                                                                                                                                                  | `provisional` |
| [`urn:doe-iri:resource:storage:block`](./urn-registry-attributes-storage-block.md) | Block Storage           | This namespace collects block storage-related type definitions.                                                                                                                                                                     | `provisional` |
| [`urn:doe-iri:resource:storage:object`](./urn-registry-attributes-storage-object.md) | Object Storage          | This namespace collects object storage-related type definitions.                                                                                                                                                                    | `provisional` |
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

# 3. Storage Resource Relationships

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
