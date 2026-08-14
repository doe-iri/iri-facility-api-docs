# DOE-IRI Link Profile Index

This page is the authoritative navigation index for every currently defined
DOE-IRI link profile. It groups the registered relationships by domain and
links to the profile that defines each relationship.

The linked profile remains authoritative for the relationship's full
stability semantics, authorization and visibility rules, target
classification, volatility, and HAL representation details. This index is
intended for navigation and summary only.

| Domain | Relationship | Semantic meaning | Source representation | Target representation | Cardinality | Link profile |
|---|---|---|---|---|---|---|
| Core | `iri:locatedAt` | Indicates the relatively stable physical and administrative Site associated with the source Resource. | Any DOE-IRI `Resource` representation. | Facility API `Site` representation identified by the source Resource's `site_uri`. | Exactly one semantic target under the current required, singular `site_uri` contract. | [`iri:locatedAt`](./link-profile-located-at.md) |
| Storage | `iri:providesFilesystem` | Indicates that a storage system provides the identified logical filesystem resource. | `urn:doe-iri:resource:storage:system` | `urn:doe-iri:resource:storage:filesystem` | `0..*` targets from a storage-system resource. | [`iri:providesFilesystem`](./link-profile-provides-filesystem.md) |
| Storage | `iri:providesBlock` | Indicates that a storage system provides the identified logical block-storage resource. | `urn:doe-iri:resource:storage:system` | `urn:doe-iri:resource:storage:block` | `0..*` targets from a storage-system resource. | [`iri:providesBlock`](./link-profile-provides-block.md) |
| Storage | `iri:providesObject` | Indicates that a storage system provides the identified logical object-storage resource. | `urn:doe-iri:resource:storage:system` | `urn:doe-iri:resource:storage:object` | `0..*` targets from a storage-system resource. | [`iri:providesObject`](./link-profile-provides-object.md) |
| Storage | `iri:hasMount` | Indicates that a filesystem is exposed through the identified mount relationship resource. | `urn:doe-iri:resource:storage:filesystem` | `urn:doe-iri:resource:storage:mount` | `0..*` targets from a filesystem resource. | [`iri:hasMount`](./link-profile-has-mount.md) |
| Storage | `iri:mountedOn` | Identifies the consuming compute system on which the filesystem represented by the mount resource is exposed. | `urn:doe-iri:resource:storage:mount` | `urn:doe-iri:resource:compute:system` | Exactly `1` target for a valid mount resource. | [`iri:mountedOn`](./link-profile-mounted-on.md) |
| Storage | `iri:attachedTo` | Indicates that a logical block-storage resource is configured to be presented or attached to the identified consuming compute resource. | `urn:doe-iri:resource:storage:block` | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` | `0..1` for an `exclusive` block resource; `0..*` for a `shared` block resource. | [`iri:attachedTo`](./link-profile-attached-to.md) |
| Compute | `iri:hasNode` | Indicates that the identified compute node participates in or is managed as part of the source compute system. | `urn:doe-iri:resource:compute:system` | `urn:doe-iri:resource:compute:node` | `0..*` targets from a compute-system resource. | [`iri:hasNode`](./link-profile-has-node.md) |
| Compute | `iri:hasCPU` | Indicates that the compute node contains, provides, or is associated with the identified CPU resource. | `urn:doe-iri:resource:compute:node` | `urn:doe-iri:resource:compute:cpu` | `0..*` targets from a compute-node resource. | [`iri:hasCPU`](./link-profile-has-cpu.md) |
| Compute | `iri:hasGPU` | Indicates that the compute node contains, provides, or is associated with the identified GPU resource. | `urn:doe-iri:resource:compute:node` | `urn:doe-iri:resource:compute:gpu` | `0..*` targets from a compute-node resource. | [`iri:hasGPU`](./link-profile-has-gpu.md) |
| Service | `iri:hostedOn` | Indicates that the identified compute system or compute node provides hosting infrastructure for the source service. | `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference` | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` | `0..*` targets from a service resource. | [`iri:hostedOn`](./link-profile-hosted-on.md) |
| Service | `iri:accessesMount` | Indicates that the source DTN service is configured to access a filesystem through the identified mount relationship resource for transfer operations. | `urn:doe-iri:resource:service:dtn` | `urn:doe-iri:resource:storage:mount` | `0..*` targets from a DTN service resource. | [`iri:accessesMount`](./link-profile-accesses-mount.md) |

[Back to the DOE-IRI Registry README](./README.md)

---

*DOE Integrated Research Infrastructure — Link Profile Index*
