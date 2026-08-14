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
| Notes | This entry represents the root DOE-IRI URN namespace rather than an independently assignable resource or attribute value. Except for administrative delegation segments, the hierarchy beneath the namespace expresses registered semantic classification. Physical topology, runtime relationships, and operational state are represented separately by the applicable IRI resource and link models. |

> **Note:** The governing namespace specification is authoritative for the exact lexical form of the namespace root and subordinate URNs. This registry uses `urn:doe-iri:` as the namespace prefix for assigned values.

## 2. DOE-IRI Namespace Taxonomy

The following taxonomy shows the currently registered top-level registry branches beneath the DOE-IRI namespace.

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
    └── administrative extension authorities and scope delegations
```

Except for the administrative `ext` category and Extension URN marker/authority segments, the DOE-IRI URN hierarchy is a **semantic registration hierarchy**. Semantic placement identifies the category and refinement of a registered value; it does not imply physical containment, ownership, deployment topology, or runtime relationships between resources.

For example:

```text
urn:doe-iri:resource:compute:node
```

identifies a compute-node resource type, but does not imply that the node is physically contained by another resource because of the URN structure itself. Relationships between independently represented resources are expressed using registered IRI link relations.

## 3. Registry Categories

The first segment following `urn:doe-iri:` identifies the top-level registry category. Each category except administrative `ext` defines a separate semantic subtree within the DOE-IRI namespace.

| URN | Short name | Purpose | Status |
|---|---|---|---|
| `urn:doe-iri:resource` | Resource Types | Namespace for registered types of physical, logical, or virtual infrastructure resources. | `active` |
| [`urn:doe-iri:storage`](urn-registry-type-storage.md) | Storage Vocabulary | Namespace for the controlled attribute vocabulary used to describe storage resources. | `provisional` |
| [`urn:doe-iri:compute`](urn-registry-type-compute.md) | Compute Vocabulary | Namespace for the controlled attribute vocabulary used to describe compute resources. | `provisional` |
| [`urn:doe-iri:service`](urn-registry-type-service.md) | Service Vocabulary | Namespace for the controlled attribute vocabulary used to describe service resources. | `provisional` |
| `urn:doe-iri:allocation` | Allocation Units | Namespace for units used to express resource quantities in facility allocations. | `active` |
| `urn:doe-iri:compression` | Compression Types | Namespace for identifiers representing compression algorithms used by IRI APIs. | `active` |
| `urn:doe-iri:ext` | Extension Administration | Administrative branch for delegated facility- or project-specific extensions; it is not a semantic controlled vocabulary. | `active` |

These categories are separate DOE-IRI registry branches. Except for the administrative `ext` branch, they are controlled semantic vocabularies. Detailed registries MAY be maintained in separate documents when a category contains a substantial number of registered values.

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

## 7. Delegated Extension Administration

The `ext` category is an administrative delegation branch, not a semantic resource-type or controlled-value vocabulary. The governing specification defines the canonical extension grammar, validation layers, placement rules, and registration policy. This registry factually records authority-code reservations separately from exact scope delegations.

### 7.1. Authority-Code Reservations

All five authority-code reservations recorded below are active and permanent. A reservation alone does not constitute an active scope delegation; the governing specification defines the assignment and reassignment policy.

| Authority code | Organization | Change controller | Status | Reference |
|---|---|---|---|---|
| `esnet` | Energy Sciences Network | Energy Sciences Network | `active` | Root Registry authority-code reservation |
| `nersc` | National Energy Research Scientific Computing Center | National Energy Research Scientific Computing Center | `active` | Root Registry authority-code reservation |
| `alcf` | Argonne Leadership Computing Facility | Argonne Leadership Computing Facility | `active` | Root Registry authority-code reservation |
| `olcf` | Oak Ridge Leadership Computing Facility | Oak Ridge Leadership Computing Facility | `active` | Root Registry authority-code reservation |
| `slac` | SLAC National Accelerator Laboratory | SLAC National Accelerator Laboratory | `active` | Root Registry authority-code reservation |

### 7.2. Scope Delegations

No delegated scopes are currently assigned. An authority-code reservation does not imply a scope delegation. Scope records use the authority code, exact registered parent, assigned prefix, permitted semantic scope, lifecycle status, and reference fields shown below.

| Authority code | Exact registered parent | Assigned prefix | Permitted semantic scope | Status | Reference |
|---|---|---|---|---|---|
| None | None | None | No delegated scopes are currently assigned. | Not applicable | Not applicable |

The following legal shapes are syntactic Extension URNs defined by the governing specification. They are not scope authorizations, local definitions, or assigned DOE-IRI extensions:

```text
urn:doe-iri:ext:<authority>:<local-path>
urn:doe-iri:resource:ext:<authority>:<local-path>
urn:doe-iri:resource:compute:ext:<authority>:<local-path>
```

The registry is the factual record of active scope delegations; the governing specification defines their effect. The legal shapes above do not authorize a scope or adjacent namespace.

---

*DOE Integrated Research Infrastructure — URN Registry*
