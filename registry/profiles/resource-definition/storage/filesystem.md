# IRI Filesystem Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/storage/filesystem`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:storage:filesystem`  
**Status:** Draft  
**Version:** 1.0.0

## Profile Applicability

This profile applies when `resource_type` is
`urn:doe-iri:resource:storage:filesystem` and MUST be used together with the
[IRI Status Resource Profile](../../status/resource.md). The authoritative
URN record is [Resource Type URNs](../../../urns/resource-types.md).

This document is for the `urn:doe-iri:resource:storage:filesystem` resource type hierarchy.

## 1. Profile Context

The following retained context identifies the type to which this profile applies;
registration metadata and lifecycle are authoritative in the URN registry.

| Field             | Description                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| URN               | `urn:doe-iri:resource:storage:filesystem`                                                              |
| Short name        | Filesystem                                                                                             |
| Description       | This namespace collects filesystem-related type definitions.                                           |
| Parent URN        | `urn:doe-iri:resource:storage`                                                                         |
| Status            | `provisional`                                                                                          |
| Introduced        | IRI v2.0                                                                                               |
| Change controller | IRI technical subcommittee.                                                                            |
| Reference         | Proposed type extensions for filesystem storage resources.                                             |
| Legacy value      | `storage` enumeration.                                                                                 |
| Examples          | `urn:doe-iri:resource:storage:filesystem`                                                              |
| Notes             | These attributes are proposed for describing logical filesystem resources provided by an IRI facility. |

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of filesystem resources within the DOE Integrated Research Infrastructure (IRI). A filesystem resource represents a logical storage resource that organizes data as files and directories within a hierarchical namespace and exposes filesystem-based access semantics to users, applications, workflows, or compute systems.

The IRI storage model intentionally separates the storage infrastructure from the logical filesystem that consumers use. A `urn:doe-iri:resource:storage:system` resource describes the managed storage infrastructure, while a `urn:doe-iri:resource:storage:filesystem` resource describes a logical filesystem provided by that infrastructure. This separation allows infrastructure-level and filesystem-level characteristics to be represented independently.

For example:

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

A storage system may provide multiple filesystem resources, and a filesystem may be exposed to multiple consuming systems through separate mount resources. This allows a filesystem to be defined once while preserving system-specific information, such as mount paths and access configuration, independently.

This document defines attributes applicable specifically to filesystem resources. These attributes describe relatively stable characteristics such as filesystem scope, architecture, capabilities, implementation technology, supported access protocols, storage tier, and underlying media.

Infrastructure-level characteristics are defined by the Storage System Resource Definition Profile. Information describing how a filesystem is exposed to a particular consuming system is represented by mount resources and corresponding IRI link relations.

This version of the profile does not define current utilization, available capacity, health, performance, or service availability. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by this Resource Definition Profile. It provides a machine-readable classification for the `urn:doe-iri:resource:storage:filesystem` resource type and for filesystem attributes whose values require consistent semantics across IRI facilities.

The taxonomy distinguishes between the resource being described and the controlled characteristics used to describe that resource. The `urn:doe-iri:resource:storage:filesystem` namespace identifies the resource type itself, while values beneath the `urn:doe-iri:storage` namespace identify standardized filesystem characteristics such as scope, architecture, capabilities, implementation technology, access protocols, storage tier, and media type.

The taxonomy is not intended to represent infrastructure topology or containment relationships. Relationships between a filesystem and the storage system that provides it, or between a filesystem and the systems on which it is mounted, are represented separately using IRI link relations.

Only attributes represented by controlled DOE-IRI URNs appear in the taxonomy. Other descriptive or quantitative attributes, if added to future versions of this profile, do not require taxonomy branches unless their values are represented by controlled DOE-IRI vocabularies.

The following tree shows the resource type and controlled vocabulary namespaces defined by this profile.

```text
urn:doe-iri
│
├── resource
│   └── storage
│       └── filesystem
│
└── storage
    │
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

## 4. Filesystem Attributes

This Resource Definition Profile defines the set of attributes that MAY be used to describe resources of type `urn:doe-iri:resource:storage:filesystem`. These attributes provide a consistent, implementation-independent representation of filesystem characteristics while allowing facilities to expose only the characteristics known and relevant to IRI consumers.

The profile separates the identity of the filesystem resource from the characteristics of its implementation and use. Controlled characteristics that require consistent machine-readable semantics are represented using registered DOE-IRI URNs.

Except for `schema_version`, attributes in this profile are optional. The absence of an optional attribute indicates that the information has not been provided and MUST NOT be interpreted as implying a particular value or capability. Clients SHOULD rely only on attributes explicitly advertised by the resource.

The attributes defined by this profile describe configured characteristics of the filesystem. The semantics of any time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

The following table defines version `1.0.0` of the filesystem attribute contract.

| Attribute                 | Version | Type                 | Description                                                                                    | Mandatory |
| ------------------------- | ------- | -------------------- | ---------------------------------------------------------------------------------------------- | --------- |
| `schema_version`          | 1.0.0   | string               | Version of the profile definition (e.g. `"1.0.0"`).                                            | yes       |
| `filesystem_scope`        | 1.0.0   | IRI URN string       | Describes whether the filesystem is local to a consuming system or accessed through a network. | no        |
| `filesystem_architecture` | 1.0.0   | Array IRI URN string | Describes the architectural characteristics of the filesystem.                                 | no        |
| `filesystem_capabilities` | 1.0.0   | Array IRI URN string | Identifies filesystem capabilities exposed by the resource.                                    | no        |
| `filesystem_technology`   | 1.0.0   | IRI URN string       | Identifies the technology or implementation used to provide the filesystem.                    | no        |
| `filesystem_protocols`    | 1.0.0   | Array IRI URN string | Identifies network filesystem protocols through which the filesystem may be accessed.          | no        |
| `tier`                    | 1.0.0   | IRI URN string       | Identifies the intended storage lifecycle or usage tier of the filesystem.                     | no        |
| `media_types`             | 1.0.0   | Array IRI URN string | Identifies the physical storage media known to back the filesystem resource.                   | no        |

### 4.1. Filesystem Scope

The `filesystem_scope` attribute describes the access scope of a `urn:doe-iri:resource:storage:filesystem` resource. It distinguishes filesystems that are primarily local to a single host or operating system instance from those made available to clients over a network.

The value of `filesystem_scope` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:filesystem-scope` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:filesystem-scope:local`   | Local      | A filesystem whose storage is directly accessible to and primarily managed by a single host or operating-system instance.             | `provisional` |
| `urn:doe-iri:storage:filesystem-scope:network` | Network    | A filesystem made available to one or more clients over a network through a filesystem service or client/server filesystem interface. | `provisional` |

For example:

```json
{
  "filesystem_scope": "urn:doe-iri:storage:filesystem-scope:network"
}
```

Filesystem scope describes how broadly the filesystem is exposed and SHOULD NOT be used to represent architectural characteristics such as whether a filesystem is distributed or clustered. Those characteristics are represented using the `filesystem_architecture` attribute.

A network-scoped filesystem also does not imply a particular access protocol. The protocols exposed by the filesystem SHOULD be advertised independently using `filesystem_protocols`.

### 4.2. Filesystem Architecture

The `filesystem_architecture` attribute describes the architectural characteristics of a `urn:doe-iri:resource:storage:filesystem` resource. It identifies how filesystem data, metadata, namespace, and filesystem services are organized across the infrastructure that implements the filesystem.

A filesystem may exhibit more than one architectural characteristic. The `filesystem_architecture` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:filesystem-architecture` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:filesystem-architecture:distributed` | Distributed | A filesystem architecture in which data, metadata, or filesystem services are distributed across multiple systems while presenting a unified filesystem namespace to consumers.                                  | `provisional` |
| `urn:doe-iri:storage:filesystem-architecture:clustered`   | Clustered   | A filesystem architecture in which multiple hosts or nodes coordinate access to shared filesystem resources using mechanisms for maintaining consistent filesystem state, metadata, locking, or cache coherence. | `provisional` |

Architecture values are not necessarily mutually exclusive. A filesystem MAY therefore advertise both `distributed` and `clustered` where both architectural characteristics apply.

Example:

```json
{
  "filesystem_architecture": [
    "urn:doe-iri:storage:filesystem-architecture:distributed",
    "urn:doe-iri:storage:filesystem-architecture:clustered"
  ]
}
```

The `filesystem_architecture` attribute describes the filesystem architecture and SHOULD NOT be interpreted as describing the architecture of the storage system that provides it. Storage-system architecture is represented separately using the Storage System Resource Definition Profile.

Clients SHOULD NOT infer filesystem capabilities, protocols, performance, availability, or storage technology solely from architecture values.

### 4.3. Filesystem Capabilities

The `filesystem_capabilities` attribute identifies capabilities exposed by a `urn:doe-iri:resource:storage:filesystem` resource.

A filesystem may provide multiple capabilities. The `filesystem_capabilities` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:filesystem-capability` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:filesystem-capability:parallel-io`      | Parallel I/O     | The filesystem supports concurrent I/O from multiple clients and can distribute I/O across multiple storage resources to provide scalable aggregate throughput.               | `provisional` |
| `urn:doe-iri:storage:filesystem-capability:direct-io`        | Direct I/O       | The filesystem supports I/O mechanisms that bypass or minimize use of the operating system page cache, allowing more direct transfer between application buffers and storage. | `provisional` |
| `urn:doe-iri:storage:filesystem-capability:asynchronous-io`  | Asynchronous I/O | The filesystem supports submission of I/O operations without requiring the submitting execution context to block until each operation completes.                              | `provisional` |
| `urn:doe-iri:storage:filesystem-capability:data-striping`    | Data striping    | The filesystem supports distributing portions of a file across multiple storage devices or targets to enable concurrent access and increased aggregate throughput.            | `provisional` |
| `urn:doe-iri:storage:filesystem-capability:shared-namespace` | Shared namespace | The filesystem provides a common filesystem namespace accessible by multiple clients with a consistent file and directory hierarchy.                                          | `provisional` |

For example:

```json
{
  "filesystem_capabilities": [
    "urn:doe-iri:storage:filesystem-capability:parallel-io",
    "urn:doe-iri:storage:filesystem-capability:data-striping",
    "urn:doe-iri:storage:filesystem-capability:shared-namespace"
  ]
}
```

The `filesystem_capabilities` attribute SHOULD describe capabilities actually exposed by the filesystem resource. Clients SHOULD NOT infer capabilities solely from `filesystem_technology`, because deployment configuration may affect which capabilities are available.

Capabilities SHOULD describe functionality and SHOULD NOT be interpreted as current operational condition. For example, support for parallel I/O is a capability, while current I/O throughput is a distinct time-varying observation.

The capability vocabulary is intended to be extensible. Additional capability URNs SHOULD be registered when they identify implementation-independent functionality that an IRI client may need to discover or reason about.

### 4.4. Filesystem Technology

The `filesystem_technology` attribute identifies the filesystem technology or implementation used to provide a `urn:doe-iri:resource:storage:filesystem` resource.

The value of `filesystem_technology` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:filesystem-technology` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:filesystem-technology:lustre`         | Lustre            | An open-source distributed parallel filesystem designed to provide scalable, high-performance shared storage, particularly for high-performance computing environments. | `provisional` |
| `urn:doe-iri:storage:filesystem-technology:spectrum-scale` | IBM Storage Scale | A clustered filesystem technology, formerly known as IBM Spectrum Scale and GPFS, supporting concurrent shared filesystem access across multiple systems.               | `provisional` |
| `urn:doe-iri:storage:filesystem-technology:cephfs`         | CephFS            | A distributed POSIX-compatible filesystem built on the Ceph distributed storage platform and providing a shared hierarchical namespace.                                 | `provisional` |
| `urn:doe-iri:storage:filesystem-technology:beegfs`         | BeeGFS            | A distributed parallel filesystem designed to provide scalable, high-performance shared filesystem access across multiple clients and storage servers.                  | `provisional` |

For example:

```json
{
  "filesystem_technology":
    "urn:doe-iri:storage:filesystem-technology:lustre"
}
```

The `filesystem_technology` attribute identifies the implementation of the logical filesystem and is distinct from `storage_technology`, which identifies the technology that implements the storage system providing the filesystem.

For example:

```text
Ceph Storage System
storage_technology = ceph
        │
        │ iri:provides-filesystem
        ▼
CephFS Filesystem
filesystem_technology = cephfs
```

Similarly, filesystem technology SHOULD NOT be used to identify the protocol through which clients access the filesystem. Access protocols are represented using `filesystem_protocols`.

Clients SHOULD NOT infer capabilities, protocols, media types, performance, or operational state solely from the filesystem technology value.

### 4.5. Filesystem Protocols

The `filesystem_protocols` attribute identifies network filesystem protocols or protocol families through which clients may access files and directories exposed by a `urn:doe-iri:resource:storage:filesystem` resource.

A filesystem may be accessible through more than one protocol. The `filesystem_protocols` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:filesystem-protocol` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:filesystem-protocol:nfs`    | NFS        | The Network File System protocol family for providing remote filesystem access to files and directories over a network. | `provisional` |
| `urn:doe-iri:storage:filesystem-protocol:smb`    | SMB        | The Server Message Block protocol family for providing network-based file and directory sharing.                        | `provisional` |
| `urn:doe-iri:storage:filesystem-protocol:webdav` | WebDAV     | An HTTP-based protocol extension that supports remote access and management of files and other resources.               | `provisional` |

For example:

```json
{
  "filesystem_protocols": [
    "urn:doe-iri:storage:filesystem-protocol:nfs"
  ]
}
```

Protocol URNs identify protocol families and SHOULD NOT encode protocol versions unless version-specific discovery becomes necessary to satisfy an IRI interoperability requirement.

For example, NFSv3 and NFSv4 are represented by the common `nfs` protocol-family URN. If protocol-version information is required in a future profile version, it SHOULD be represented independently rather than by creating separate filesystem protocol identities without a demonstrated interoperability need.

Filesystem protocols are distinct from filesystem technologies. For example, a filesystem implemented using Lustre technology may also be exposed through an NFS gateway. In such a deployment, the filesystem technology and access protocol describe separate characteristics and SHOULD be advertised independently.

### 4.6. Storage Tier

The `tier` attribute identifies the intended storage lifecycle, usage pattern, or purpose associated with a `urn:doe-iri:resource:storage:filesystem` resource.

The value of `tier` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:tier` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:tier:home`     | Home       | Persistent user-oriented storage intended for files such as configuration data, source code, personal working data, and other user-specific content.                        | `provisional` |
| `urn:doe-iri:storage:tier:project`  | Project    | Shared persistent storage allocated to a project, collaboration, or team for ongoing project data and collaborative use.                                                    | `provisional` |
| `urn:doe-iri:storage:tier:scratch`  | Scratch    | High-performance temporary storage intended for active workloads, intermediate data, and transient working files, typically subject to limited retention or purge policies. | `provisional` |
| `urn:doe-iri:storage:tier:campaign` | Campaign   | Intermediate-term storage intended to retain data associated with a scientific campaign, experiment, project, or allocation for the duration of that activity.              | `provisional` |
| `urn:doe-iri:storage:tier:archive`  | Archive    | Storage intended for durable, long-term retention of data that is accessed less frequently and is not expected to provide active-tier performance characteristics.          | `provisional` |

For example:

```json
{
  "tier": "urn:doe-iri:storage:tier:scratch"
}
```

Storage tier describes the intended role or lifecycle of the filesystem and is independent of the technology used to implement it or the physical media on which its data resides.

For example:

```text
Filesystem
    tier = scratch

    filesystem_technology = lustre

    media_types:
        solid-state
        magnetic-disk
```

A client SHOULD NOT infer filesystem performance, retention policy, purge interval, durability, or media type solely from the `tier` value. Facilities SHOULD advertise such characteristics independently when they are defined by the applicable IRI API contract and Resource Definition Profile.

### 4.7. Storage Media Types

The `media_types` attribute identifies physical storage media known to retain data associated with a `urn:doe-iri:resource:storage:filesystem` resource.

A filesystem may be backed by more than one type of physical storage media. The `media_types` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:media-type` namespace.

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
    "urn:doe-iri:storage:media-type:solid-state",
    "urn:doe-iri:storage:media-type:magnetic-disk"
  ]
}
```

The presence of multiple values indicates that the filesystem is backed by or may store data on multiple media types. It does not indicate how data is distributed among those media types.

Media types SHOULD be advertised at the filesystem level only when the backing media are known and meaningful to consumers. Where media information is known only for the underlying storage infrastructure, it SHOULD instead be advertised on the corresponding `urn:doe-iri:resource:storage:system` resource.

Clients SHOULD NOT infer performance, latency, durability, persistence, or storage tier solely from media type.

The attribute SHOULD be omitted when the underlying media cannot be meaningfully determined for the filesystem or when the facility does not intend to expose that implementation detail.

## 5. Filesystem JSON Schema

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
      example: urn:doe-iri:storage:filesystem-technology:lustre

    FilesystemAttributes:
      type: object
      description: >
        Attributes describing a filesystem resource with resource type
        urn:doe-iri:resource:storage:filesystem.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          description: >
            Version of the filesystem attribute contract.
          enum:
            - "1.0.0"
          example: "1.0.0"

        filesystem_scope:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Describes whether the filesystem is local to a consuming
            system or accessed through a network.
          example: urn:doe-iri:storage:filesystem-scope:network

        filesystem_architecture:
          type: array
          description: >
            Describes the architectural characteristics of the filesystem.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:filesystem-architecture:distributed
            - urn:doe-iri:storage:filesystem-architecture:clustered

        filesystem_capabilities:
          type: array
          description: >
            Identifies capabilities exposed by the filesystem.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:filesystem-capability:parallel-io
            - urn:doe-iri:storage:filesystem-capability:data-striping
            - urn:doe-iri:storage:filesystem-capability:shared-namespace

        filesystem_technology:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the technology or implementation used to provide
            the filesystem.
          example: urn:doe-iri:storage:filesystem-technology:lustre

        filesystem_protocols:
          type: array
          description: >
            Identifies network filesystem protocols through which
            the filesystem may be accessed.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:filesystem-protocol:nfs

        tier:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the intended storage lifecycle or usage tier
            associated with the filesystem.
          example: urn:doe-iri:storage:tier:scratch

        media_types:
          type: array
          description: >
            Identifies physical storage media known to back the
            filesystem resource.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:media-type:solid-state
            - urn:doe-iri:storage:media-type:magnetic-disk
```

## 6. Example Filesystem JSON Instance

```json
{
  "schema_version": "1.0.0",
  "filesystem_scope": "urn:doe-iri:storage:filesystem-scope:network",
  "filesystem_architecture": [
    "urn:doe-iri:storage:filesystem-architecture:distributed",
    "urn:doe-iri:storage:filesystem-architecture:clustered"
  ],
  "filesystem_capabilities": [
    "urn:doe-iri:storage:filesystem-capability:parallel-io",
    "urn:doe-iri:storage:filesystem-capability:direct-io",
    "urn:doe-iri:storage:filesystem-capability:asynchronous-io",
    "urn:doe-iri:storage:filesystem-capability:data-striping",
    "urn:doe-iri:storage:filesystem-capability:shared-namespace"
  ],
  "filesystem_technology": "urn:doe-iri:storage:filesystem-technology:lustre",
  "filesystem_protocols": [
    "urn:doe-iri:storage:filesystem-protocol:nfs"
  ],
  "tier": "urn:doe-iri:storage:tier:scratch",
  "media_types": [
    "urn:doe-iri:storage:media-type:solid-state",
    "urn:doe-iri:storage:media-type:magnetic-disk"
  ]
}
```

---

*DOE Integrated Research Infrastructure — URN Registry: Filesystem*
