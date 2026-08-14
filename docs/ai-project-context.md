# DOE-IRI Registry AI Project Context

This document captures the architectural decisions, vocabulary choices, documentation conventions, and open design considerations developed during the DOE Integrated Research Infrastructure (IRI) registry work.

It is intended to give Codex or another repository-aware AI enough context to continue work consistently without relying on the original ChatGPT conversation.

The repository itself remains authoritative for the current files and registered values. If this context document conflicts with the repository, identify the discrepancy before modifying registry semantics.

---

# 1. Project Purpose

The project is defining a DOE-IRI registry for the IRI Facility API.

The registry provides stable semantic identifiers and profiles for:

1. resource types;
2. type-specific attributes;
3. controlled attribute vocabularies;
4. hypermedia relationships between resource representations.

The goal is to allow IRI facilities to describe heterogeneous scientific infrastructure in a consistent, implementation-independent manner without requiring every type or vocabulary change to modify the core OpenAPI resource schema.

The model is summarized as:

```text
Resource Type  →  Attributes  →  Relationships
```

Operational state is modeled separately.

---

# 2. Fundamental Architecture

## 2.1. Four conceptual concerns

The model distinguishes four concerns:

```text
Resource Type
    What kind of resource is this?

Attributes
    What relatively stable characteristics does this resource have?

Relationships
    How is this resource related to other resources?

State
    What is happening with this resource now?
```

The first three form the registry-driven resource-definition model. State is deliberately separate.

## 2.2. Resource definitions vs. resource state

The resource definition contains identity, classification, relatively stable characteristics, and relatively stable topology.

Typical resource-definition information:

- resource type;
- technology;
- architecture;
- capabilities;
- configured/logical capacity;
- vendor/product/version;
- mount path;
- supported protocols/APIs;
- topology relationships.

Typical dynamic state:

- current availability;
- current health;
- free/used capacity;
- utilization;
- throughput;
- latency;
- current mount status;
- current block attachment status;
- current workload/scheduler activity.

A topology link should not disappear merely because the target is temporarily unhealthy or unavailable.

---

# 3. URN Modeling Principles

## 3.1. DOE-IRI namespace

The namespace prefix used by the registry is:

```text
urn:doe-iri:
```

The root registry currently recognizes primary registry branches including:

```text
urn:doe-iri:resource
urn:doe-iri:storage
urn:doe-iri:compute
urn:doe-iri:service
urn:doe-iri:allocation
urn:doe-iri:compression
urn:doe-iri:ext
```

## 3.2. Semantic hierarchy, not physical topology

A major design principle for semantic URN segments is:

> The URN hierarchy is a semantic registration/classification hierarchy, not a physical containment hierarchy.

The administrative `ext` category, Extension URN marker, and authority code are explicit exceptions: they express delegated governance rather than semantic classification.

For example:

```text
urn:doe-iri:resource:compute
├── system
├── node
├── cpu
└── gpu
```

All four are type refinements of `compute`.

Do not use:

```text
compute
└── system
    └── node
        ├── cpu
        └── gpu
```

to represent physical containment.

Containment/topology is represented through links such as:

```text
iri:hasNode
iri:hasCPU
iri:hasGPU
```

The same principle applies to storage.

## 3.3. Resource type vs. controlled attribute URNs

Resource types use:

```text
urn:doe-iri:resource:...
```

Controlled attribute vocabularies use domain-specific branches such as:

```text
urn:doe-iri:storage:...
urn:doe-iri:compute:...
```

Example:

```text
resource_type:
    urn:doe-iri:resource:storage:filesystem

attribute:
    tier

controlled value:
    urn:doe-iri:storage:tier:scratch
```

Another example:

```text
resource_type:
    urn:doe-iri:resource:compute:cpu

attribute:
    cpu_architecture

controlled value:
    urn:doe-iri:compute:cpu-architecture:x86-64
```

A controlled attribute URN describes a standardized characteristic. It does not identify the resource itself.

---

# 4. Registry vs. Governing RFC

The registry is not the governing RFC.

The intended separation is:

```text
Specifications
    Define the rules.

Registries
    Record the values assigned under those rules.
```

The governing DOE-IRI URN specification is responsible for topics such as:

- namespace syntax;
- ABNF;
- matching/equivalence;
- registration procedures;
- extension rules;
- conformance requirements.

Registry documents record:

- assigned URNs;
- semantic descriptions;
- parentage in the semantic hierarchy;
- lifecycle status;
- references;
- legacy values;
- profile links;
- delegated extension authority-code reservations and exact scope delegations.

The root registry should therefore not duplicate normative grammar and registration-process text from the RFC.

---

# 5. Repository Documentation Model

The documentation was restructured from a small number of monolithic documents into a navigable registry hierarchy.

Preferred naming:

```text
urn-registry-root.md
    Root DOE-IRI namespace registry.

urn-registry-type-<domain>.md
    Domain resource-type registry and conceptual model.

urn-registry-type-<domain>-taxonomy.md
    Consolidated taxonomy, controlled URN index, and relationship index.

urn-registry-attributes-<domain>-<type>.md
    Attribute profile for a specific resource type.

link-profile-<relation>.md
    Semantic definition of an IRI link relation.
```

Current examples include:

```text
urn-registry-type-storage.md
urn-registry-type-storage-taxonomy.md

urn-registry-type-compute.md
urn-registry-type-compute-taxonomy.md

urn-registry-attributes-storage-filesystem.md
urn-registry-attributes-compute-node.md

link-profile-has-mount.md
link-profile-has-node.md
```

The repository README should function primarily as a navigation map rather than restating every registry value.

---

# 6. Root Registry

The root registry is the entry point for the DOE-IRI namespace.

Its purpose is to:

- register the root namespace;
- show the top-level registry taxonomy, distinguishing semantic categories from
  the administrative `ext` branch;
- register top-level categories;
- list base resource-type URNs;
- list allocation-unit URNs;
- list compression identifiers;
- record extension authority-code reservations and exact scope delegations;
- delegate detailed subtrees to domain registry documents.

The root registry taxonomy currently follows the conceptual shape:

```text
urn:doe-iri
│
├── resource
│   ├── compute
│   ├── storage
│   ├── network
│   ├── system
│   ├── website
│   ├── service
│   └── unknown
│
├── storage
│   └── controlled storage attribute vocabulary
│
├── compute
│   └── controlled compute attribute vocabulary
│
├── service
│   └── controlled service attribute vocabulary
│
├── allocation
│   └── allocation-unit vocabulary
│
├── compression
│   └── compression-type vocabulary
│
└── ext
    └── administrative authority-code reservations and scope delegations
```

Base resource types currently discussed:

```text
urn:doe-iri:resource:compute
urn:doe-iri:resource:storage
urn:doe-iri:resource:network
urn:doe-iri:resource:system
urn:doe-iri:resource:website
urn:doe-iri:resource:service
urn:doe-iri:resource:unknown
```

`resource:unknown` is intended as a fallback type and should not be used when a more specific registered resource type is known.

---

# 7. Registry Entry Metadata

Registry pages use metadata fields such as:

| Field | Purpose |
|---|---|
| URN | Registered DOE-IRI identifier |
| Short name | Human-readable label |
| Description | Semantic meaning |
| Parent URN | Parent in the registered semantic hierarchy |
| Status | `active`, `provisional`, or `deprecated` |
| Introduced | Registry version or introduction date |
| Deprecated | Deprecation version/date if applicable |
| Replacement URN | Preferred replacement if deprecated |
| Change controller | Responsible organization/process |
| Reference | Governing specification, decision, issue, or record |
| Legacy value | Prior enum or controlled-vocabulary value |
| Examples | Representative usage |
| Notes | Additional implementation/migration guidance |

---

# 8. Storage Resource Model

## 8.1. Storage resource types

The current storage resource taxonomy is:

```text
urn:doe-iri:resource:storage
├── system
├── filesystem
├── mount
├── block
└── object
```

Meaning:

### Storage System

```text
urn:doe-iri:resource:storage:system
```

Represents managed storage infrastructure that provides one or more logical storage resources.

It is not necessarily a single physical device.

### Filesystem

```text
urn:doe-iri:resource:storage:filesystem
```

Represents a logical file-oriented storage resource that organizes data as files/directories in a hierarchical namespace.

### Mount

```text
urn:doe-iri:resource:storage:mount
```

Represents a filesystem being exposed to a particular consuming system at a particular namespace location.

Mount is modeled as a resource because it can have independent:

- path;
- access mode;
- protocol;
- mount options;
- consuming-system relationship;
- state.

### Block

```text
urn:doe-iri:resource:storage:block
```

Represents a logical storage resource exposing addressable blocks/volumes.

### Object

```text
urn:doe-iri:resource:storage:object
```

Represents a logical object-storage resource managing independently addressable objects and metadata, normally accessed through an API.

## 8.2. Archive decision

Archive is **not** a fundamental access model.

It is modeled as a storage tier/lifecycle classification:

```text
urn:doe-iri:storage:tier:archive
```

The fundamental logical access models remain:

```text
filesystem
block
object
```

---

# 9. Storage Topology

The primary filesystem model is:

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

General provider topology:

```text
Storage System
        │
        ├── iri:providesFilesystem ──> Filesystem
        ├── iri:providesBlock ───────> Block Storage
        └── iri:providesObject ──────> Object Storage
```

Key reasoning:

- one storage system may provide multiple logical resources;
- a filesystem may be mounted on multiple systems;
- each mount can have a different path/configuration;
- the filesystem itself should not duplicate per-system mount information.

Example:

```text
Scratch Filesystem
    mounted as /pscratch on one system
    mounted as /global/scratch on another
```

These should be separate mount resources referencing the same filesystem.

---

# 10. Storage Relationships

Current storage link relations:

```text
iri:providesFilesystem
iri:providesBlock
iri:providesObject
iri:hasMount
iri:mountedOn
iri:attachedTo
```

## 10.1. iri:providesFilesystem

Source:

```text
urn:doe-iri:resource:storage:system
```

Target:

```text
urn:doe-iri:resource:storage:filesystem
```

Cardinality:

```text
0..*
```

Target classification:

```text
Resource
```

Semantics: relatively stable provider topology.

Authorization may affect visibility.

The relationship does not imply current filesystem health or availability.

## 10.2. iri:providesBlock

Source:

```text
urn:doe-iri:resource:storage:system
```

Target:

```text
urn:doe-iri:resource:storage:block
```

Cardinality:

```text
0..*
```

Target classification:

```text
Resource
```

Current attachment is not implied.

## 10.3. iri:providesObject

Source:

```text
urn:doe-iri:resource:storage:system
```

Target:

```text
urn:doe-iri:resource:storage:object
```

Cardinality:

```text
0..*
```

Target classification:

```text
Resource
```

Object API endpoints are not the target of this relationship.

## 10.4. iri:hasMount

Source:

```text
urn:doe-iri:resource:storage:filesystem
```

Target:

```text
urn:doe-iri:resource:storage:mount
```

Cardinality:

```text
0..*
```

Target classification:

```text
Relationship resource
```

A mount represents exposure/configuration, not current mounted/unmounted state.

## 10.5. iri:mountedOn

Source:

```text
urn:doe-iri:resource:storage:mount
```

Target:

```text
urn:doe-iri:resource:compute:system
```

Cardinality:

```text
1
```

Target classification:

```text
Resource
```

The relationship identifies the consuming system to which the mount applies.

Current mount state remains separate.

## 10.6. iri:attachedTo

Source:

```text
urn:doe-iri:resource:storage:block
```

Target:

```text
urn:doe-iri:resource:compute:system
```

or:

```text
urn:doe-iri:resource:compute:node
```

Cardinality depends on block access mode:

```text
exclusive -> 0..1
shared    -> 0..*
```

Target classification:

```text
Resource
```

This relation represents configured/presented topology rather than live attached/detached state.

Attachment-specific device paths and current path health do not belong intrinsically to the block resource.

If future use cases require attachment-specific identity/configuration/state, consider a dedicated block-attachment relationship resource.

---

# 11. Storage Controlled Vocabulary

The storage controlled vocabulary is under:

```text
urn:doe-iri:storage:...
```

## 11.1. Storage system technology

```text
urn:doe-iri:storage:system-technology:lustre
urn:doe-iri:storage:system-technology:spectrum-scale
urn:doe-iri:storage:system-technology:ceph
urn:doe-iri:storage:system-technology:beegfs
```

Important distinction:

```text
system-technology:ceph
```

describes the storage-system technology, while:

```text
filesystem-technology:cephfs
```

describes a filesystem technology implemented on Ceph.

## 11.2. Storage system architecture

```text
urn:doe-iri:storage:system-architecture:distributed
urn:doe-iri:storage:system-architecture:clustered
```

Architecture may be multi-valued; a system can reasonably be both distributed and clustered.

## 11.3. Storage system capabilities

```text
urn:doe-iri:storage:system-capability:replication
urn:doe-iri:storage:system-capability:erasure-coding
urn:doe-iri:storage:system-capability:encryption-at-rest
urn:doe-iri:storage:system-capability:snapshot
urn:doe-iri:storage:system-capability:data-tiering
```

A system capability does not imply that every logical child resource exposes that capability.

## 11.4. Filesystem scope

```text
urn:doe-iri:storage:filesystem-scope:local
urn:doe-iri:storage:filesystem-scope:network
```

Scope answers local vs. network accessibility.

Do not place distributed/clustered here.

## 11.5. Filesystem architecture

```text
urn:doe-iri:storage:filesystem-architecture:distributed
urn:doe-iri:storage:filesystem-architecture:clustered
```

Multi-valued when appropriate.

## 11.6. Filesystem capabilities

```text
urn:doe-iri:storage:filesystem-capability:parallel-io
urn:doe-iri:storage:filesystem-capability:direct-io
urn:doe-iri:storage:filesystem-capability:asynchronous-io
urn:doe-iri:storage:filesystem-capability:data-striping
urn:doe-iri:storage:filesystem-capability:shared-namespace
```

Advertise actual deployed capability; do not infer solely from filesystem technology.

## 11.7. Filesystem technology

```text
urn:doe-iri:storage:filesystem-technology:lustre
urn:doe-iri:storage:filesystem-technology:spectrum-scale
urn:doe-iri:storage:filesystem-technology:cephfs
urn:doe-iri:storage:filesystem-technology:beegfs
```

NFS is not a filesystem technology in this model; it is a protocol.

## 11.8. Filesystem protocol

```text
urn:doe-iri:storage:filesystem-protocol:nfs
urn:doe-iri:storage:filesystem-protocol:smb
urn:doe-iri:storage:filesystem-protocol:webdav
```

NFS is treated as a protocol family.

Do not advertise NFS on a Lustre filesystem unless that deployment actually exposes an NFS gateway/interface.

## 11.9. Mount access mode

```text
urn:doe-iri:storage:mount-access-mode:read-only
urn:doe-iri:storage:mount-access-mode:read-write
```

Access mode describes mount configuration, not per-user authorization.

## 11.10. Block scope

```text
urn:doe-iri:storage:block-scope:local
urn:doe-iri:storage:block-scope:network
```

## 11.11. Block protocol

```text
urn:doe-iri:storage:block-protocol:iscsi
urn:doe-iri:storage:block-protocol:fibre-channel
urn:doe-iri:storage:block-protocol:nvme-o-f
```

Open precision question:

- `fibre-channel` is currently used.
- A stricter model might eventually prefer `fcp` if the registry wants to distinguish the Fibre Channel fabric from the block protocol carried over it.

Do not rename without an explicit decision because it is a compatibility-visible URN.

## 11.12. Block access mode

```text
urn:doe-iri:storage:block-access-mode:exclusive
urn:doe-iri:storage:block-access-mode:shared
```

Shared means multiple concurrent attachments are supported; it does not imply arbitrary concurrent writes are safe.

## 11.13. Block provisioning

```text
urn:doe-iri:storage:block-provisioning:thin
urn:doe-iri:storage:block-provisioning:thick
```

## 11.14. Block capabilities

```text
urn:doe-iri:storage:block-capability:snapshot
urn:doe-iri:storage:block-capability:clone
urn:doe-iri:storage:block-capability:multipath
```

## 11.15. Object API

```text
urn:doe-iri:storage:object-api:s3
urn:doe-iri:storage:object-api:swift
```

The model intentionally calls these APIs rather than transport protocols.

## 11.16. Object technology

```text
urn:doe-iri:storage:object-technology:ceph-rgw
urn:doe-iri:storage:object-technology:openstack-swift
urn:doe-iri:storage:object-technology:amazon-s3
```

Open ontology question:

- `amazon-s3` is a managed service/product rather than an implementation technology in exactly the same sense as Ceph RGW or OpenStack Swift.
- Revisit only if there is a concrete need to normalize this vocabulary.

## 11.17. Object consistency

```text
urn:doe-iri:storage:object-consistency:strong-read-after-write
urn:doe-iri:storage:object-consistency:eventual
```

Consistency can vary by operation/configuration/provider.

If a single scalar value cannot accurately characterize the object resource, the profile should allow omission rather than forcing an inaccurate value.

## 11.18. Object capabilities

```text
urn:doe-iri:storage:object-capability:multipart-upload
urn:doe-iri:storage:object-capability:versioning
urn:doe-iri:storage:object-capability:object-lock
```

## 11.19. Storage tier

Shared storage-tier vocabulary:

```text
urn:doe-iri:storage:tier:home
urn:doe-iri:storage:tier:project
urn:doe-iri:storage:tier:scratch
urn:doe-iri:storage:tier:campaign
urn:doe-iri:storage:tier:archive
```

Intended meanings:

### Home

Persistent user-specific storage for configuration, source, and personal working data.

### Project

Shared persistent storage allocated to a project, collaboration, or team.

### Scratch

High-performance temporary storage for active workloads/intermediate data, typically subject to retention/purge rules.

### Campaign

Intermediate-term storage for a bounded scientific campaign, experiment, project, or allocation.

### Archive

Durable long-term, relatively infrequent-access retention.

Campaign and project semantics are not assumed to be universally standardized outside this registry; the profile definitions should be explicit.

## 11.20. Media type

Shared media vocabulary:

```text
urn:doe-iri:storage:media-type:magnetic-disk
urn:doe-iri:storage:media-type:solid-state
urn:doe-iri:storage:media-type:tape
urn:doe-iri:storage:media-type:optical
```

Media type describes fundamental physical storage medium.

Do not use these as media types:

```text
NVMe
SATA
SAS
iSCSI
```

Those are interface/protocol/transport concepts, not physical media types.

---

# 12. Storage Profile Attribute Decisions

## 12.1. Storage System profile

Current core attributes include:

```text
schema_version
storage_technology
storage_architecture
storage_capabilities
media_types
capacity_gib
vendor
product
version
```

`schema_version` is required.

`storage_architecture`, `storage_capabilities`, and `media_types` may be arrays.

`capacity_gib` is configured/usable capacity, not current free/used capacity.

## 12.2. Filesystem profile

Current core attributes include:

```text
schema_version
filesystem_scope
filesystem_architecture
filesystem_capabilities
filesystem_technology
filesystem_protocols
tier
media_types
```

No filesystem capacity field was included in the initial profile draft.

## 12.3. Mount profile

Current core attributes include:

```text
schema_version
mount_path
access_mode
filesystem_protocol
mount_options
```

`mount_path` is required.

`filesystem_protocol` is singular for a particular mount/exposure even though a filesystem may support multiple protocols.

`mount_options` are currently opaque strings.

Mounted/unmounted status belongs in state.

## 12.4. Block profile

Current core attributes include:

```text
schema_version
block_scope
block_protocols
block_access_mode
block_provisioning
block_capabilities
capacity_gib
tier
media_types
```

`capacity_gib` is logical configured capacity.

Current physical allocation/consumption belongs in state.

Device path is attachment-specific, not intrinsic to the block resource.

## 12.5. Object profile

Current core attributes include:

```text
schema_version
object_apis
access_endpoints
object_technology
object_consistency
object_capabilities
tier
media_types
```

`access_endpoints` is an array of endpoint descriptors, conceptually:

```json
{
  "url": "https://example.invalid",
  "api": "urn:doe-iri:storage:object-api:s3"
}
```

Endpoints are modeled as attributes/access descriptors by default.

Create a separate endpoint resource only if endpoint-specific identity, lifecycle, relationships, or state becomes necessary.

---

# 13. Capacity Decision

The project intentionally moved away from a numeric `capacity_bytes` field as the default representation because extremely large byte counts can exceed the exact integer range of common IEEE-754 JavaScript numbers.

Current preference:

```text
capacity_gib
```

where GiB means:

```text
2^30 bytes
```

Benefits:

- fewer digits;
- still deterministic and machine-readable;
- adequate precision for infrastructure capacity reporting.

If exact bytes are ever required, a string representation may be considered rather than an unsafe JSON numeric value.

Dynamic free/used capacity remains state.

---

# 14. Compute Resource Model

## 14.1. Compute resource types

Current compute taxonomy:

```text
urn:doe-iri:resource:compute
├── system
├── node
├── cpu
└── gpu
```

### Compute System

```text
urn:doe-iri:resource:compute:system
```

Managed computing environment composed of one or more compute nodes and supporting infrastructure, presented as a cohesive computational resource.

### Compute Node

```text
urn:doe-iri:resource:compute:node
```

Individual computing host providing processing, memory, and local resources.

### CPU

```text
urn:doe-iri:resource:compute:cpu
```

General-purpose processor resource associated with a compute node.

### GPU

```text
urn:doe-iri:resource:compute:gpu
```

Highly parallel/accelerated processor resource associated with a compute node.

Facilities do not have to expose every CPU or GPU as an individually addressable resource if aggregate representation is sufficient.

---

# 15. Compute Topology and Relationships

General topology:

```text
Compute System
urn:doe-iri:resource:compute:system
        │
        │ iri:hasNode
        ▼
Compute Node
urn:doe-iri:resource:compute:node
        │
        ├── iri:hasCPU ──> CPU
        │                  urn:doe-iri:resource:compute:cpu
        │
        └── iri:hasGPU ──> GPU
                           urn:doe-iri:resource:compute:gpu
```

Current compute relationships:

```text
iri:hasNode
iri:hasCPU
iri:hasGPU
```

These describe relatively stable topology.

They are not availability indicators.

Current node/CPU/GPU utilization, health, allocation, or idle/busy state belongs in operational state.

---

# 16. Compute Controlled Vocabulary

The current compute taxonomy/index generated during the project includes:

## 16.1. Compute system capability

```text
urn:doe-iri:compute:system-capability:batch-scheduling
urn:doe-iri:compute:system-capability:interactive-access
urn:doe-iri:compute:system-capability:container-execution
urn:doe-iri:compute:system-capability:accelerator-support
```

## 16.2. Node role

```text
urn:doe-iri:compute:node-role:compute
urn:doe-iri:compute:node-role:login
urn:doe-iri:compute:node-role:service
```

## 16.3. CPU architecture

```text
urn:doe-iri:compute:cpu-architecture:x86-64
urn:doe-iri:compute:cpu-architecture:arm64
urn:doe-iri:compute:cpu-architecture:ppc64le
urn:doe-iri:compute:cpu-architecture:riscv64
```

## 16.4. GPU programming interface

```text
urn:doe-iri:compute:gpu-programming-interface:cuda
urn:doe-iri:compute:gpu-programming-interface:hip
urn:doe-iri:compute:gpu-programming-interface:opencl
urn:doe-iri:compute:gpu-programming-interface:sycl
```

The decision was to keep vendor-specific GPU architecture/model information as ordinary strings initially while using controlled URNs for portable programming interfaces.

Before extending these vocabularies, inspect the current repository versions of the compute profiles because those drafts may have evolved.

---

# 17. Link Profile Documentation Standard

Each link profile should include a metadata section with at least:

| Field | Meaning |
|---|---|
| Relationship | Registered relation name |
| Semantic meaning | Exact relationship semantics |
| Source representation type | Allowed source resource type |
| Target representation type | Allowed target type |
| Cardinality | Number of targets |
| Target stability | Static/relatively static/dynamic |
| Authorization affects visibility | Whether links may be filtered |
| Target classification | Resource, state object, operation entry point, relationship resource |
| Relationship volatility | What causes link membership to change |

Then include sections covering:

1. semantic meaning;
2. source and target representation;
3. cardinality;
4. static vs. dynamic semantics;
5. authorization and visibility;
6. HAL representation example.

Authorization guidance developed during this work:

- a provider may omit targets the requester is not allowed to discover;
- absence of a visible target is not necessarily proof that no such relationship exists;
- authorization filtering must not change the meaning of links that remain visible.

---

# 18. HAL Relationship Philosophy

Links are used to avoid embedding topology-specific identifiers inside attributes.

Example:

Bad conceptual pattern:

```json
{
  "filesystem": {
    "mounted_on_system_id": "perlmutter"
  }
}
```

Preferred conceptual pattern:

```json
{
  "_links": {
    "iri:mountedOn": {
      "href": ".../perlmutter"
    }
  }
}
```

The relation name carries the semantics. The target remains an independently represented resource.

---

# 19. README Strategy

The README was redesigned to be a **map of the registry**, not the registry itself.

Preferred README sections:

1. What Is the DOE-IRI Registry?
2. Resource Model.
3. Registry Structure.
4. Root Registry.
5. Resource Type Registries.
   - Storage.
   - Compute.
   - future domains.
6. Controlled Attribute Vocabularies.
7. Link Profiles.
8. How the Documents Relate.
9. Where Do I Start?
10. Registry Conventions.
11. Governing Specifications.

The README should help developers answer:

- where do I find a type?
- which profile applies?
- where are controlled values defined?
- where is a relation defined?
- where do I add a new URN?
- which document is normative?

Avoid turning README into another duplicated registry table.

---

# 20. Domain Registry Page Strategy

A domain type registry such as:

```text
urn-registry-type-storage.md
urn-registry-type-compute.md
```

should serve as the conceptual entry point for that domain.

Typical sections:

1. Registry Metadata.
2. Introduction.
3. Domain conceptual model.
4. Example topology.
5. Taxonomy.
6. Resource Types.
7. Controlled Attribute Vocabulary introduction/index.
8. Resource Relationships.

The page should explain the model and link to refinement pages rather than duplicating all profile detail.

A separate `*-taxonomy.md` file can provide a compact consolidated index of:

- resource type taxonomy;
- all controlled URNs;
- relationship links.

---

# 21. Controlled Attribute Vocabulary Section Strategy

A domain's controlled vocabulary section should explain:

- controlled URNs are attribute values, not additional resource types;
- ordinary scalar attributes do not need URNs;
- vocabularies can be type-specific or shared;
- each value links to the attribute profile that defines it.

Example explanatory pattern:

```text
Resource type:
    urn:doe-iri:resource:storage:filesystem

Attribute:
    filesystem_technology

Controlled attribute value:
    urn:doe-iri:storage:filesystem-technology:lustre
```

Controlled vocabularies should be omitted when a scalar/string is more appropriate.

---

# 22. OpenAPI / JSON Schema Style

The storage profiles established a reusable `IriUrn` schema:

```yaml
IriUrn:
  type: string
  description: >
    A DOE-IRI Uniform Resource Name (URN) identifying a registered
    IRI resource type, attribute value, capability, or other
    controlled vocabulary value.
  pattern: '^urn:doe-iri:[A-Za-z0-9][A-Za-z0-9:._~-]*$'
```

General conventions:

- profile schemas are objects;
- `schema_version` is normally required;
- `schema_version` currently uses `1.0.0`;
- controlled-URN arrays use `uniqueItems: true`;
- capacities/counts are non-negative;
- `int64` is used where consistent with the existing schema;
- examples should use full URNs, not shorthand strings.

Check the repository's actual OpenAPI version before relying on OpenAPI-version-specific `$ref` behavior.

---

# 23. Extension Authorities

The project has adopted the explicit `ext` marker as the sole canonical mechanism for facility- or project-controlled DOE-IRI extensions. The root registry reserves `ext` as an administrative delegation branch, not a semantic controlled vocabulary.

Authorities discussed include:

```text
esnet
nersc
alcf
olcf
slac
```

The governing model defines the following legal extension shapes:

```text
urn:doe-iri:ext:<authority>:<local-path>
urn:doe-iri:resource:ext:<authority>:<local-path>
urn:doe-iri:resource:compute:ext:<authority>:<local-path>
```

Important principle:

> An authority-code reservation and an active exact scope delegation, not string uniqueness alone, determine whether an Extension URN is scope-authorized.

`urn:doe-iri:ext` is the valid administrative category-root exception. In Extension URNs, `ext` and its authority code are structural rather than semantic subtype segments. Shared-parent fallback stops at the nearest recognized shared parent before `ext`; a root-scope extension uses opaque fallback when its local meaning is unknown. Prefixes ending in `:ext` or `:ext:<authority>` are not resource types or controlled values.

The registry records authority-code reservations separately from scope delegations. Every exact registered canonical semantic DOE-IRI URN is structurally eligible as an extension parent; there is no separate extension-point approval registry. An authority controls only the full nonempty suffix subtree explicitly delegated to it; a reservation grants no insertion point, and no active scope is inferred from it. Local leaves beneath an active scope do not require central registration. Promotion creates a new shared URN and may deprecate the former extension with explicit replacement guidance; identifiers are never repurposed.

An **Extension URN** is syntax-only: it matches the explicit `ext` form but does not imply registration, scope, or documentation. A **scope-authorized Extension URN** has a reserved authority and active exact parent/authority scope. A **locally defined Extension URN** is scope-authorized and has an authority-assigned, documented suffix. An **assigned DOE-IRI extension** satisfies all three layers.

Validation is layered: syntactic validity, scope authorization, and local definition. General clients retain unknown-extension fallback, while strict contracts may reject scope-unauthorized or scope-authorized-but-undocumented values when assigned DOE-IRI extensions are required. Proven deployed legacy direct-form identifiers require explicit deprecated mappings and MUST NOT be heuristically rewritten.

---

# 24. Important Semantic Distinctions

Preserve these distinctions.

## 24.1. Technology vs. protocol

Example:

```text
filesystem technology:
    Lustre
    CephFS

filesystem protocol:
    NFS
    SMB
    WebDAV
```

Do not place NFS under filesystem technology.

## 24.2. System technology vs. logical-resource technology

Example:

```text
storage system:
    urn:doe-iri:storage:system-technology:ceph

filesystem:
    urn:doe-iri:storage:filesystem-technology:cephfs
```

A Ceph system may provide CephFS, RBD, and RGW logical resources.

## 24.3. Scope vs. architecture

Example:

```text
filesystem scope:
    local
    network

filesystem architecture:
    distributed
    clustered
```

Do not mix these axes.

## 24.4. Capability vs. dynamic state

A capability states that the resource can support something.

It does not state that the capability is currently active, healthy, or available.

## 24.5. Mount resource vs. filesystem resource

The filesystem describes the logical filesystem.

The mount describes one exposure of that filesystem to one consuming system.

## 24.6. Block resource vs. attachment

The block resource describes the logical volume.

Host-specific attachment details may require relationship-specific data or a future attachment resource.

## 24.7. Object resource vs. endpoint

The object resource describes the logical object-storage service/resource.

Endpoint URLs are currently access descriptors unless there is a need for independent endpoint identity/state.

---

# 25. Compatibility Principles

When changing the registry:

- do not rename an assigned URN casually;
- do not move a controlled value between namespaces without migration planning;
- preserve legacy mappings where relevant;
- use lifecycle status to manage deprecation;
- identify replacement URNs;
- avoid semantic reuse of an existing URN for a different meaning.

Taxonomy trees, definition tables, attribute profiles, and examples should stay synchronized.

---

# 26. Known/Open Questions

The following items were identified as areas that may merit future refinement but are **not** settled changes.

## 26.1. Fibre Channel naming

Current block protocol value:

```text
urn:doe-iri:storage:block-protocol:fibre-channel
```

Possible future precision improvement:

```text
...:fcp
```

because Fibre Channel is a fabric/transport and FCP is the SCSI mapping used for block storage.

Do not change without explicit approval.

## 26.2. Amazon S3 as object technology

Current value:

```text
urn:doe-iri:storage:object-technology:amazon-s3
```

This is arguably a service/product rather than an implementation technology in the same category as Ceph RGW and OpenStack Swift.

Revisit only if the ontology needs stronger separation between implementation technology and managed service/product.

## 26.3. Object consistency scalar

A single `object_consistency` value may be too coarse because consistency can vary by operation or provider behavior.

Current guidance: omit if one scalar cannot accurately characterize the resource.

## 26.4. Native Lustre mount protocol

The mount profile reuses the filesystem-protocol vocabulary currently containing NFS, SMB, and WebDAV.

Native Lustre client access may not map to those values.

The current design allows the protocol to be omitted when no registered value applies.

A future native-Lustre access-mechanism vocabulary may be warranted if interoperability use cases require it.

## 26.5. CPU/GPU resource granularity

CPU and GPU are modeled as resource types, but facilities are not required to expose each device individually.

A future profile may need clearer guidance for:

- aggregate processor descriptions;
- individual sockets/devices;
- accelerator partitions/slices;
- virtualized accelerator resources.

---

# 27. Recommended Workflow for Future Domain Work

When adding a new domain such as network or another future domain:

1. Define the parent resource type:
   ```text
   urn:doe-iri:resource:<domain>
   ```
2. Decide the minimal meaningful subtype taxonomy.
3. Ensure subtype hierarchy reflects classification, not physical topology.
4. Identify type-specific attributes.
5. Separate controlled vocabularies from ordinary scalar attributes.
6. Define topology using link relations.
7. Identify any relationship resources.
8. Keep current operational state separate.
9. Create:
   - domain type registry;
   - taxonomy/index;
   - subtype attribute profiles;
   - link profiles.
10. Update:
   - root registry;
   - README;
   - cross-domain relationship references.

---

# 28. Quality Checklist

Before finalizing a registry change, verify:

## URNs

- Does every URN have one clear semantic meaning?
- Is the parent namespace correct?
- Is it classification rather than topology?
- Is a new URN actually necessary?
- Is an existing controlled vocabulary reusable?

## Attributes

- Is the attribute relatively stable?
- Should it be a scalar, array, URN, object, or link instead?
- Is the vocabulary orthogonal to other vocabularies?
- Are optional values omitted rather than guessed?

## Relationships

- Are source and target types explicit?
- Is cardinality correct?
- Is the target a resource/state/operation/relationship resource?
- Is relationship membership stable or dynamic?
- Can authorization hide targets?
- Does the link accidentally encode transient state?

## State

- Has dynamic utilization/health/availability been kept out of definition?
- Are configured totals distinguished from current free/used quantities?

## Documentation

- Do taxonomy and tables agree?
- Do examples use full registered URNs?
- Are all relative links valid?
- Are README and root registry indexes updated?
- Are new values marked `provisional` unless approved otherwise?
- Are compatibility implications documented?

---

# 29. Service Resource Model

## 29.1. Namespace separation

The Service domain uses two distinct DOE-IRI branches:

```text
urn:doe-iri:resource:service:...
    Resource classification: what kind of service resource is represented.

urn:doe-iri:service:...
    Controlled attribute vocabulary: standardized characteristics of a
    service resource.
```

Do not use a controlled service value as `Resource.resource_type`, and do not
move a technology, protocol, or API value into the resource branch. For
example:

```text
resource type:
    urn:doe-iri:resource:service:dtn

attribute:
    dtn_technology

controlled value:
    urn:doe-iri:service:dtn-technology:globus
```

## 29.2. Service resource types

The current Service resource taxonomy is:

```text
urn:doe-iri:resource:service
├── dtn
└── inference
```

The parent `urn:doe-iri:resource:service` remains the active generic
consumable service resource type. Its two current refinements are provisional:

```text
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

A DTN service is a consumable data-transfer service, not an individual host or
compute node. An inference service is a consumable model-invocation service,
not a model, deployment, endpoint, replica, host, or accelerator.

Endpoints remain attributes of their service resource unless a future use case
requires endpoint-specific identity, lifecycle, relationships, or state.
Physical hosting and configured storage access are represented by links, not
by deeper resource-type nesting.

## 29.3. Service controlled vocabulary

The controlled Service vocabulary is registered under:

```text
urn:doe-iri:service:...
```

### DTN technology

```text
urn:doe-iri:service:dtn-technology:globus
urn:doe-iri:service:dtn-technology:xrootd
```

These values identify the technology or implementation providing a DTN
service. They do not identify resource subtypes, and they do not imply support
for a particular transfer protocol.

### Transfer protocol

```text
urn:doe-iri:service:transfer-protocol:https
urn:doe-iri:service:transfer-protocol:gridftp
urn:doe-iri:service:transfer-protocol:xrootd
urn:doe-iri:service:transfer-protocol:sftp
```

Transfer protocols are multi-valued service characteristics. XRootD appears in
both the technology and protocol families because those values answer different
questions: one identifies an implementation and the other identifies a
transfer interface.

### Inference API

```text
urn:doe-iri:service:inference-api:openai
urn:doe-iri:service:inference-api:kserve-v2
```

An inference API identifies an invocation interface exposed to consumers. It
is distinct from the technology implementing the service.

### Inference technology

```text
urn:doe-iri:service:inference-technology:vllm
urn:doe-iri:service:inference-technology:hugging-face-tgi
urn:doe-iri:service:inference-technology:nvidia-triton
urn:doe-iri:service:inference-technology:kserve
```

These values identify inference serving technologies, not resource subtypes.
Clients must not infer APIs, endpoint reachability, authorization, capacity,
or served-model activity solely from the technology value.

All current controlled Service values are provisional. Preserve their exact
spelling and lifecycle status unless an explicit registry decision changes
them.

## 29.4. Service definition and state

The DTN service definition may contain:

```text
schema_version
dtn_technology
technology_version
transfer_protocols
transfer_endpoints
```

Configured endpoint URLs and their registered protocols are definition
information. Current endpoint reachability, health, availability, active
transfers, queues, throughput, credentials, and authorization outcomes are
operational state or belong to the applicable security and transfer-state
mechanisms.

The inference service definition may contain:

```text
schema_version
inference_technology
technology_version
inference_apis
inference_endpoints
served_models
```

`served_models` is a stable catalog of models configured to be served. Each
entry has a service-local `id` and `name`, with optional `version` and
`model_uri`. Catalog membership does not claim that the model is currently
loaded or able to serve a request.

Current model activity belongs in the separate companion operational-state
contract:

```text
active_models
```

Each `active_models` item references a `served_models.id` from the corresponding
definition instance. Omission means current activity is unknown or unreported;
an empty array means the service reports no active models. Current endpoint
reachability, health, availability, request rate, queue depth, active replicas,
model loading, and model activity also remain state.

## 29.5. Service relationships

The Service model registers two link relations:

Both currently registered Service link relations, `iri:hostedOn` and
`iri:accessesMount`, have lifecycle status `provisional`.

```text
DTN Service or Inference Service
        │
        └── iri:hostedOn ──────> Compute System or Compute Node

DTN Service
        │
        └── iri:accessesMount ─> Filesystem Mount
```

### iri:hostedOn

Source:

```text
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

Target:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
```

Cardinality:

```text
0..*
```

Target classification:

```text
Resource
```

`iri:hostedOn` describes relatively static hosting topology. It does not state
current routing, live replica placement, health, availability, or that the
target is currently serving requests.

### iri:accessesMount

Source:

```text
urn:doe-iri:resource:service:dtn
```

Target:

```text
urn:doe-iri:resource:storage:mount
```

Cardinality:

```text
0..*
```

Target classification:

```text
Relationship resource
```

`iri:accessesMount` means the DTN service is configured to access a filesystem
through the identified mount relationship resource for transfer operations.
The mount is the target instead of the filesystem because it identifies the
particular exposure and can carry the path, access mode, protocol, mount
options, and consuming-system relationship.

Do not infer DTN access by combining `iri:hostedOn` with a mount's
`iri:mountedOn` link. Co-location on the same compute infrastructure does not
prove that the service can access that mount. The explicit `iri:accessesMount`
link is required to represent configured access.

The link does not imply current mount availability, endpoint reachability,
credential validity, unrestricted authorization, or active transfer activity.
Both Service relationships may be hidden by authorization; absence of a
visible link is not proof that the relationship does not exist.

---

# 30. Short Architectural Summary

If only one section of this document is read, use this:

```text
1. URNs classify.
2. Attributes characterize.
3. HAL links relate.
4. State changes over time.
5. URN hierarchy is semantic, not physical.
6. Registry records assignments; RFCs define rules.
7. Keep resource types, controlled vocabularies, relationships, and state orthogonal.
8. Prefer explicit reusable semantics over deep composite subtype names.
9. Do not invent values when omission is more accurate.
10. Keep all taxonomy, profile, link, README, and root-registry documentation synchronized.
```

---

# 31. `iri:locatedAt` Resource-to-Site Relation (2026-08-14)

`iri:locatedAt` is a provisional, singular HAL relation from any DOE-IRI
Resource representation to its relatively stable Facility API Site
representation. It identifies physical and administrative site association;
it does not assert current process placement, compute hosting, endpoint
reachability, health, availability, ownership, or live routing.

The existing required `site_uri` remains authoritative during the additive
compatibility period. A producer MAY expose a singular `iri:locatedAt` link;
when present, its `href` MUST exactly equal `site_uri`. The Site identity is
already disclosed by `site_uri`, so the relation MUST NOT be independently
authorization-filtered while that field is returned. Removing or deprecating
`site_uri` requires a separate approved schema revision.

`iri:locatedAt` is distinct from `iri:hostedOn`: `locatedAt` applies to any
Resource and identifies its Site, while `hostedOn` applies only to DTN or
inference services and identifies compute hosting infrastructure.
