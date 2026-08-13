# Attribute Profile: `urn:doe-iri:resource:storage:mount`

This document is for the `urn:doe-iri:resource:storage:mount` resource type hierarchy.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN               | `urn:doe-iri:resource:storage:mount`                                                                                 |
| Short name        | Filesystem Mount                                                                                                     |
| Description       | This namespace collects filesystem mount-related type definitions.                                                   |
| Parent URN        | `urn:doe-iri:resource:storage`                                                                                       |
| Status            | `provisional`                                                                                                        |
| Introduced        | IRI v2.0                                                                                                             |
| Change controller | IRI technical subcommittee.                                                                                          |
| Reference         | Proposed type extensions for filesystem mount resources.                                                             |
| Legacy value      | None.                                                                                                                |
| Examples          | `urn:doe-iri:resource:storage:mount`                                                                                 |
| Notes             | These attributes are proposed for describing how a filesystem is exposed within the namespace of a consuming system. |

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of filesystem mounts within the DOE Integrated Research Infrastructure (IRI). A mount resource represents the exposure of a filesystem to a particular consuming system at a specific location within that system's filesystem namespace.

The IRI storage model intentionally separates the logical filesystem from the way that filesystem is exposed to a consuming system. A `urn:doe-iri:resource:storage:filesystem` resource describes the logical filesystem itself, while a `urn:doe-iri:resource:storage:mount` resource describes a particular presentation of that filesystem to a compute system or other consuming resource.

For example:

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

This separation allows a filesystem to be defined once while being exposed differently on multiple consuming systems. For example, the same filesystem might appear as `/scratch` on one compute system and `/global/scratch` on another:

```text
Scratch Filesystem
        │
        ├── hasMount ──> Mount A
        │                 mount_path = /scratch
        │                     │
        │                     └── mountedOn ──> Compute System A
        │
        └── hasMount ──> Mount B
                          mount_path = /global/scratch
                              │
                              └── mountedOn ──> Compute System B
```

The filesystem resource remains responsible for describing characteristics of the logical storage resource, such as filesystem technology, architecture, capabilities, protocols, tier, and media types. The mount resource contains only characteristics that are specific to a particular exposure of that filesystem to a consuming system.

The identities of the filesystem and consuming system are represented using IRI resource relationships rather than duplicated as mount attributes. The filesystem relates to the mount using `iri:hasMount`, and the mount relates to the consuming system using `iri:mountedOn`.

This document defines relatively stable mount configuration characteristics, such as the namespace location, access mode, access protocol, and optional implementation-specific mount options. Dynamic operational information, such as whether the filesystem is currently mounted, accessible, degraded, or unavailable, is outside the scope of this profile and SHOULD be represented through the appropriate resource-state mechanisms.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by the Filesystem Mount Attribute Profile. It provides a machine-readable classification for the `urn:doe-iri:resource:storage:mount` resource type and for mount attributes whose values require consistent semantics across IRI facilities.

The taxonomy distinguishes between the mount resource itself and the controlled characteristics used to describe that resource. The `urn:doe-iri:resource:storage:mount` namespace identifies the resource type, while values beneath the `urn:doe-iri:storage` namespace identify standardized mount characteristics.

The mount profile also reuses the `urn:doe-iri:storage:filesystem-protocol` vocabulary defined by the Filesystem Attribute Profile. Reusing this vocabulary ensures that a protocol has the same semantic meaning whether it is advertised as a protocol supported by a filesystem or as the protocol used by a particular mount.

The taxonomy does not represent the filesystem being mounted or the consuming system on which it is mounted. Those relationships are expressed separately using `iri:hasMount` and `iri:mountedOn`.

Only attributes represented using controlled DOE-IRI URNs appear in the taxonomy. Scalar attributes such as `mount_path` and implementation-specific `mount_options` do not appear as taxonomy branches.

The following tree shows the resource type and controlled vocabulary namespaces used by this profile.

```text
urn:doe-iri
│
├── resource
│   └── storage
│       └── mount
│
└── storage
    │
    ├── mount-access-mode
    │   ├── read-only
    │   └── read-write
    │
    └── filesystem-protocol
        ├── nfs
        ├── smb
        └── webdav
```

## 4. Filesystem Mount Attribute Profile

The Filesystem Mount Attribute Profile defines the set of attributes that MAY be used to describe resources of type `urn:doe-iri:resource:storage:mount`. These attributes provide a consistent representation of how a filesystem is exposed within the namespace of a particular consuming system.

The profile deliberately avoids duplicating characteristics that belong to the filesystem itself or to the consuming system. Information such as filesystem technology, filesystem tier, storage media, or compute-system identity SHOULD be obtained from the related resources.

The `schema_version` and `mount_path` attributes are mandatory. A mount resource represents a filesystem's presentation at a namespace location; therefore, the location represented by `mount_path` is considered an essential characteristic of the resource.

The remaining attributes are optional. The absence of an optional attribute indicates that the information has not been provided and MUST NOT be interpreted as implying a particular value or behavior.

The attributes defined by this profile describe relatively stable mount configuration. Dynamic information associated with a mount SHOULD be represented through the corresponding resource-state mechanisms.

The following table defines the attributes included in version `1.0.0` of the Filesystem Mount Attribute Profile.

| URN | Short name | Description | Status |
|---|---|---|---|
| `schema_version`      | 1.0.0   | string         | Version of the profile definition (e.g. `"1.0.0"`).                                              | yes       |
| `mount_path`          | 1.0.0   | string         | Namespace location at which the filesystem is exposed on the consuming system.                   | yes       |
| `access_mode`         | 1.0.0   | IRI URN string | Identifies whether the mount permits read-only or read-write access.                             | no        |
| `filesystem_protocol` | 1.0.0   | IRI URN string | Identifies the filesystem protocol used by this mount when applicable.                           | no        |
| `mount_options`       | 1.0.0   | Array string   | Identifies implementation-specific client or operating-system options associated with the mount. | no        |

### 4.1. Mount Path

The `mount_path` attribute identifies the location within the consuming system's filesystem namespace at which the filesystem is exposed.

The value is represented as a string because namespace syntax is determined by the consuming system and operating environment rather than by the DOE-IRI model.

For example:

```json
{
  "mount_path": "/global/scratch"
}
```

A POSIX-based compute environment might expose a filesystem using paths such as:

```text
/scratch
/home
/project
/global/cfs
```

Other operating environments MAY use different namespace conventions. Clients therefore SHOULD treat the value as an opaque namespace location unless they understand the conventions of the consuming system.

The `mount_path` identifies the location at which the filesystem is visible on the system referenced by `iri:mountedOn`. It does not identify the filesystem itself and SHOULD NOT be interpreted independently of the mount's resource relationships.

For example:

```text
Filesystem
    │
    │ iri:hasMount
    ▼
Mount
    mount_path = /scratch
        │
        │ iri:mountedOn
        ▼
Compute System
```

Because the same filesystem may have different mount paths on different systems, `mount_path` belongs to the mount resource rather than the filesystem resource.

### 4.2. Mount Access Mode

The `access_mode` attribute describes the level of data access provided through a particular mount.

The value of `access_mode` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:mount-access-mode` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:mount-access-mode:read-only`  | Read only  | The mount permits consumers to read filesystem content but does not permit modification of filesystem data through this mount.                         | `provisional` |
| `urn:doe-iri:storage:mount-access-mode:read-write` | Read/write | The mount permits consumers to read and, subject to applicable authorization and filesystem permissions, modify filesystem content through this mount. | `provisional` |

For example:

```json
{
  "access_mode": "urn:doe-iri:storage:mount-access-mode:read-write"
}
```

The `access_mode` attribute describes the mount's access semantics and does not represent user-specific authorization. A `read-write` mount indicates that the mount itself permits write operations; it does not imply that every user or workload accessing the mount is authorized to modify every file.

Similarly, `read-only` describes the mount configuration rather than the underlying filesystem. The same filesystem MAY be mounted read-write on one system and read-only on another:

```text
Filesystem
    │
    ├── Mount A
    │     access_mode = read-write
    │         │
    │         └── mountedOn ──> Compute System A
    │
    └── Mount B
          access_mode = read-only
              │
              └── mountedOn ──> Analysis System
```

Clients SHOULD NOT infer filesystem-level write capabilities or authorization policy solely from the `access_mode` value.

### 4.3. Filesystem Protocol

The `filesystem_protocol` attribute identifies the network filesystem protocol or protocol family used by a particular mount when applicable.

The value of `filesystem_protocol` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:filesystem-protocol` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:filesystem-protocol:nfs`    | NFS        | The Network File System protocol family for providing remote filesystem access to files and directories over a network. | `provisional` |
| `urn:doe-iri:storage:filesystem-protocol:smb`    | SMB        | The Server Message Block protocol family for providing network-based file and directory sharing.                        | `provisional` |
| `urn:doe-iri:storage:filesystem-protocol:webdav` | WebDAV     | An HTTP-based protocol extension that supports remote access and management of files and other resources.               | `provisional` |

For example:

```json
{
  "filesystem_protocol": "urn:doe-iri:storage:filesystem-protocol:nfs"
}
```

The Filesystem Attribute Profile may advertise multiple protocols that can be used to access a logical filesystem:

```text
Filesystem
    filesystem_protocols:
        nfs
        smb
```

A particular mount, however, represents one specific exposure of that filesystem and therefore uses the singular `filesystem_protocol` attribute:

```text
Filesystem
    filesystem_protocols:
        nfs
        smb
            │
            ├── Mount A
            │     filesystem_protocol = nfs
            │
            └── Mount B
                  filesystem_protocol = smb
```

The mount-level protocol SHOULD identify the protocol actually used for that mount and SHOULD NOT be inferred solely from the set of protocols supported by the filesystem.

The `filesystem_protocol` attribute MAY be omitted when a separately registered network filesystem protocol is not applicable or when the protocol is unknown. For example, a filesystem accessed through a technology-specific native client may not require a value from the currently defined filesystem-protocol vocabulary.

Protocol URNs identify protocol families rather than protocol versions. Version-specific characteristics SHOULD be represented independently if a future interoperability requirement requires them.

### 4.4. Mount Options

The `mount_options` attribute identifies implementation-specific client, filesystem, or operating-system options associated with the mount.

The attribute is represented as an array of strings because mount-option syntax and semantics are generally defined by the filesystem technology, client implementation, protocol, or consuming operating system rather than by DOE-IRI.

For example:

```json
{
  "mount_options": [
    "hard",
    "noatime"
  ]
}
```

Values in `mount_options` SHOULD be treated as opaque strings unless the client understands the applicable filesystem technology, protocol, and operating environment.

The `mount_options` attribute is intended to expose useful implementation-specific configuration without requiring DOE-IRI to standardize every technology-specific mount option.

Semantically important characteristics for which DOE-IRI defines a controlled vocabulary SHOULD NOT be encoded only as implementation-specific mount options. For example, read-only versus read-write access is represented using the standardized `access_mode` attribute rather than requiring clients to interpret values such as `ro` or `rw` from `mount_options`.

For example:

```json
{
  "access_mode": "urn:doe-iri:storage:mount-access-mode:read-only",

  "mount_options": [
    "hard",
    "noatime"
  ]
}
```

Facilities SHOULD omit `mount_options` when the underlying options are unknown, are not meaningful to IRI consumers, or would expose unnecessary implementation detail.

## 5. Mount JSON Schema

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
      example: urn:doe-iri:storage:mount-access-mode:read-write

    MountAttributes:
      type: object
      description: >
        Attributes describing a filesystem mount resource with resource type
        urn:doe-iri:resource:storage:mount.
      required:
        - schema_version
        - mount_path

      properties:

        schema_version:
          type: string
          description: >
            Version of the filesystem mount attribute profile definition.
          enum:
            - "1.0.0"
          example: "1.0.0"

        mount_path:
          type: string
          minLength: 1
          description: >
            Namespace location at which the filesystem is exposed
            on the consuming system.
          example: /global/scratch

        access_mode:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies whether the mount permits read-only or
            read-write access.
          example: urn:doe-iri:storage:mount-access-mode:read-write

        filesystem_protocol:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the filesystem protocol used by this mount
            when applicable.
          example: urn:doe-iri:storage:filesystem-protocol:nfs

        mount_options:
          type: array
          description: >
            Implementation-specific client or operating-system mount
            options associated with the mount.
          uniqueItems: true
          items:
            type: string
          example:
            - hard
            - noatime
```

## 6. Example Mount JSON Instance

```json
{
  "schema_version": "1.0.0",
  "mount_path": "/global/scratch",
  "access_mode": "urn:doe-iri:storage:mount-access-mode:read-write",
  "filesystem_protocol": "urn:doe-iri:storage:filesystem-protocol:nfs",
  "mount_options": [
    "hard",
    "noatime"
  ]
}
```

The complete resource model associates this attribute profile with the filesystem and consuming system through IRI relationships:

```text
Filesystem
urn:doe-iri:resource:storage:filesystem
        │
        │ iri:hasMount
        ▼
Mount
urn:doe-iri:resource:storage:mount

attributes:
    mount_path = /global/scratch
    access_mode = read-write
    filesystem_protocol = nfs
        │
        │ iri:mountedOn
        ▼
Compute System
urn:doe-iri:resource:compute:system
```

---

*DOE Integrated Research Infrastructure — URN Registry: Filesystem Mount*
