# DOE-IRI URN Root Registry

This document is the **registry of assigned DOE-IRI URN values**. The governing namespace specification is defined in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md).

The governing DOE-IRI URN specification defines the namespace syntax, matching and equivalence rules, registration process, extension rules, and conformance requirements. This registry records the values assigned under that specification, their semantic placement within the DOE-IRI hierarchy, and their current lifecycle status.

This document defines the root of the DOE-IRI registry and delegates detailed subtrees to their corresponding registry documents where appropriate.

## 1. Registry Entry Metadata

The root DOE-IRI namespace is registered as follows:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:` |
| Short name | DOE-IRI Namespace |
| Description | Root namespace for Uniform Resource Names defined and managed by the DOE Integrated Research Infrastructure (IRI) project. Registered resource types, controlled vocabulary values, allocation units, algorithm identifiers, extension authorities, and other DOE-IRI semantic identifiers are assigned beneath this namespace. |
| Parent URN | None. This is the root of the DOE-IRI registered semantic hierarchy. |
| Status | `active` |
| Introduced | IRI v2.0 |
| Deprecated | Not applicable |
| Replacement URN | Not applicable |
| Change controller | IRI technical subcommittee. |
| Reference | [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md) |
| Legacy value | None |
| Examples | `urn:doe-iri:resource:storage:filesystem`, `urn:doe-iri:resource:compute:system`, `urn:doe-iri:storage:tier:scratch` |
| Notes | This entry represents the root DOE-IRI URN namespace rather than an independently assignable resource or attribute value. The hierarchy beneath the namespace expresses registered semantic classification. Physical topology, runtime relationships, and operational state are represented separately by the applicable IRI resource and link models. |

> **Note:** The governing namespace specification is authoritative for the exact lexical form of the namespace root and subordinate URNs. This registry uses `urn:doe-iri:` as the namespace prefix for assigned values.

## 2. DOE-IRI Namespace Taxonomy

The following taxonomy shows the currently registered top-level semantic branches beneath the DOE-IRI namespace.

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
│   │   ├── dtn
│   │   └── inference
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
    └── delegated extension authorities
```

The DOE-IRI URN hierarchy is a **semantic registration hierarchy**. Hierarchical placement identifies the category and refinement of a registered value; it does not imply physical containment, ownership, deployment topology, or runtime relationships between resources.

For example:

```text
urn:doe-iri:resource:compute:node
```

identifies a compute-node resource type, but does not imply that the node is physically contained by another resource because of the URN structure itself. Relationships between independently represented resources are expressed using registered IRI link relations.

## 3. Registry Categories

The first segment following `urn:doe-iri:` identifies the top-level registry category. Each category defines a separate semantic subtree within the DOE-IRI namespace.

| URN | Short name | Purpose | Status |
|---|---|---|---|
| `urn:doe-iri:resource` | Resource Types | Namespace for registered types of physical, logical, or virtual infrastructure resources. | `active` |
| [`urn:doe-iri:storage`](urn-registry-type-storage.md) | Storage Vocabulary | Namespace for the controlled attribute vocabulary used to describe storage resources. | `provisional` |
| [`urn:doe-iri:compute`](urn-registry-type-compute.md) | Compute Vocabulary | Namespace for the controlled attribute vocabulary used to describe compute resources. | `provisional` |
| [`urn:doe-iri:service`](urn-registry-type-service.md) | Service Vocabulary | Namespace for the controlled attribute vocabulary used to describe service resources. | `provisional` |
| `urn:doe-iri:allocation` | Allocation Units | Namespace for units used to express resource quantities in facility allocations. | `active` |
| `urn:doe-iri:compression` | Compression Types | Namespace for identifiers representing compression algorithms used by IRI APIs. | `active` |
| `urn:doe-iri:ext` | Extension Authorities | Namespace reserved for delegated facility- or project-specific extensions. | `active` |

These categories are separate controlled vocabularies within the DOE-IRI URN namespace. Detailed registries MAY be maintained in separate documents when a category contains a substantial number of registered values.

## 4. Resource Type Registry

The following base URNs are defined to be compatible with the resource types in IRI version 1.0 and serve as root URNs for resource-type refinement.

| URN | Short name | Description | Legacy value | Status |
|---|---|---|---|---|
| [`urn:doe-iri:resource:compute`](urn-registry-type-compute.md) | Compute | Generic compute resource. | `compute` | `active` |
| [`urn:doe-iri:resource:storage`](urn-registry-type-storage.md) | Storage | Generic storage resource. | `storage` | `active` |
| `urn:doe-iri:resource:network` | Network | Generic network resource. | `network` | `active` |
| `urn:doe-iri:resource:system` | System | Generic system resource type. | `system` | `active` |
| `urn:doe-iri:resource:website` | Website | Generic website resource type. | `website` | `active` |
| [`urn:doe-iri:resource:service`](urn-registry-type-service.md) | Service | Generic service resource type. Detailed service resource types and controlled vocabulary values are delegated to the Service Type Registry. | `service` | `active` |
| `urn:doe-iri:resource:unknown` | Unknown | Fallback resource type used when the resource's more specific type is not known or cannot be represented by a registered resource-type URN. | `unknown` | `active` |

`urn:doe-iri:resource:unknown` SHOULD NOT be used when a more specific registered resource type is known.

Resource-type URNs classify resources. They do not encode containment or topology. A resource's relationship to other resources is represented separately using IRI link relations.

Detailed resource-type and controlled-vocabulary values beneath `urn:doe-iri:resource:service` and `urn:doe-iri:service` are maintained in the [Service Type Registry](urn-registry-type-service.md) and its [Service Taxonomy and URN Index](urn-registry-type-service-taxonomy.md).

## 5. Allocation Unit Registry

These URNs identify units used to express resource quantities in allocation objects.

| URN | Short name | Description | Legacy value | Status |
|---|---|---|---|---|
| `urn:doe-iri:allocation:node-hours` | Node-hours | Compute allocation measured in node-hours. | `node-hours` | `active` |
| `urn:doe-iri:allocation:bytes` | Bytes | Storage allocation measured in bytes. | `bytes` | `active` |
| `urn:doe-iri:allocation:inodes` | Inodes | Storage allocation measured in filesystem inodes. | `inodes` | `active` |

## 6. Compression Type Registry

These URNs identify compression algorithms used by IRI APIs.

| URN | Short name | Description | Legacy value | Status |
|---|---|---|---|---|
| `urn:doe-iri:compression:none` | None | No compression. | `none` | `active` |
| `urn:doe-iri:compression:bzip2` | bzip2 | bzip2 compression. | `bzip2` | `active` |
| `urn:doe-iri:compression:gzip` | gzip | gzip compression. | `gzip` | `active` |
| `urn:doe-iri:compression:xz` | xz | xz compression. | `xz` | `active` |

## 7. Delegated Extension Authorities

The DOE-IRI namespace specification may permit delegated extension subtrees for facility- or project-specific values.

The registry reserves the `ext` segment for this purpose. An extension authority MUST be registered before values beneath its delegated subtree are treated as assigned DOE-IRI values.

The governing specification defines where an `ext` segment may appear and the rules governing values beneath a delegated authority. This registry records the authorities that have been assigned.

### 7.1. Registered Extension Authorities

| Authority | Organization | Assigned prefix | Scope | Status |
|---|---|---|---|---|
| `esnet` | Energy Sciences Network | `urn:doe-iri:ext:esnet:` | TBD by delegation record | `active` |
| `nersc` | National Energy Research Scientific Computing Center | `urn:doe-iri:ext:nersc:` | TBD by delegation record | `active` |
| `alcf` | Argonne Leadership Computing Facility | `urn:doe-iri:ext:alcf:` | TBD by delegation record | `active` |
| `olcf` | Oak Ridge Leadership Computing Facility | `urn:doe-iri:ext:olcf:` | TBD by delegation record | `active` |
| `slac` | SLAC National Accelerator Laboratory | `urn:doe-iri:ext:slac:` | TBD by delegation record | `active` |

Example shapes defined by the governing specification include:

```text
urn:doe-iri:ext:<authority>:<type>
urn:doe-iri:resource:ext:<authority>:<type>
urn:doe-iri:resource:compute:ext:<authority>:<type>
```

The registry, rather than string uniqueness alone, is authoritative for determining which extension authorities have been delegated.

A delegated authority controls only the subtree explicitly assigned to it. The authority MUST NOT assume control of adjacent DOE-IRI namespaces or other extension points unless those scopes are separately delegated by the governing registry process.

---

*DOE Integrated Research Infrastructure — URN Registry*
