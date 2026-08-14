# Type Registry: `urn:doe-iri:resource:service`

This document defines the `urn:doe-iri:resource:service` resource type hierarchy and serves as the entry point for the DOE-IRI service resource model.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:service` |
| Short name | Service |
| Description | This namespace collects service-related resource type definitions. |
| Parent URN | `urn:doe-iri:resource` |
| Status | `active` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | [Service Resource Types Design](../docs/superpowers/specs/2026-08-13-service-resource-types-design.md). |
| Legacy value | `service` enumeration. |
| Examples | `urn:doe-iri:resource:service:dtn` |
| Notes | This namespace defines the provisional child resource types used to refine the generic consumable `service` resource type. Type-specific characteristics are defined by the corresponding attribute profiles. |

## 2. Introduction

The IRI service model provides a consistent, implementation-independent way to describe consumable services made available by an IRI facility.

This document defines the top-level service resource taxonomy and the relationships between service resources and independently identifiable infrastructure resources. Detailed characteristics and controlled vocabularies applicable to each service type are defined by the corresponding attribute profiles referenced in Section 4. This document therefore serves as the entry point for the IRI service model rather than defining all characteristics of each service type.

The active parent `urn:doe-iri:resource:service` represents a generic consumable service resource. A data-transfer node (DTN) service represents a consumable data-transfer service, not its host node. An inference service represents a consumable model-invocation service, not a model, deployment, endpoint, replica, or accelerator.

The service model follows the broader IRI separation between resource identity, resource characteristics, resource relationships, and operational state:

```text
Resource Type
    "What kind of service resource is this?"

Attributes
    "What relatively stable characteristics does this service have?"

Relationships
    "How is this service related to other independently identifiable resources?"

State
    "What is happening with this service now?"
```

Resource type URNs identify what kind of resource is being described. Attribute profiles describe relatively stable characteristics of that resource. IRI link relations describe topology and relationships between independently identifiable resources. Endpoints are attributes of the applicable service resource, not independent resource types. Dynamic information such as current endpoint reachability, health, availability, active transfers, model loading, or workload activity is represented separately through the appropriate resource-state mechanisms.

### 2.1. Service Resource Model

The service model defines two provisional service resource types:

- A **DTN Service** is a consumable service for data-transfer operations. It may be hosted across one or more compute systems or nodes, and it may be configured to access one or more filesystem mount relationship resources for transfer operations.
- An **Inference Service** is a consumable service for model invocation. It may be hosted across one or more compute systems or nodes. Model artifacts, deployments, endpoint URLs, replicas, hosts, and accelerators remain attributes or related resources as applicable; they are not independent service resource types in this registry.

The general model is:

```text
DTN Service
urn:doe-iri:resource:service:dtn
        │
        ├── iri:hostedOn ──────> Compute System or Compute Node
        │
        └── iri:accessesMount ─> Filesystem Mount
                                      │
                                      └── iri:mountedOn ─> Compute System

Inference Service
urn:doe-iri:resource:service:inference
        │
        └── iri:hostedOn ──────> Compute System or Compute Node
```

Physical topology is expressed by these link relations, not by deeper resource-type nesting. A service may be hosted across multiple nodes or systems, and co-location does not by itself prove a DTN can access a mount.

## 3. Taxonomy

The following taxonomy defines the resource types registered beneath `urn:doe-iri:resource:service`.

The hierarchy represents **resource type refinement only**. It does not represent host placement, service deployment topology, endpoint identity, model deployment, or accelerator association. Those concerns are represented by attributes, IRI link relations, or operational state as applicable.

```text
urn:doe-iri:resource:service
│
├── dtn
│   └── "What consumable data-transfer service can I use?"
│
└── inference
    └── "What consumable model-invocation service can I use?"
```

Although these service types appear as siblings in the taxonomy, hosting and configured storage access are expressed separately through IRI link relations.

## 4. Service Resource Types

The following URNs are registered as child resource types of `urn:doe-iri:resource:service`. Each type refines the generic service resource into a more specific resource abstraction and links to an attribute profile defining the characteristics applicable to that resource type.

| URN | Short name | Description | Status |
|---|---|---|---|
| [`urn:doe-iri:resource:service:dtn`](./urn-registry-attributes-service-dtn.md) | DTN Service | A consumable data-transfer service. It does not identify an individual host or compute node. | `provisional` |
| [`urn:doe-iri:resource:service:inference`](./urn-registry-attributes-service-inference.md) | Inference Service | A consumable model-invocation service. It does not identify a model, deployment, endpoint, replica, or accelerator. | `provisional` |

The linked attribute profiles define resource-specific characteristics and controlled DOE-IRI vocabularies applicable to each service resource type.

## 5. Service Controlled Attribute Vocabulary

The service attribute profiles define controlled DOE-IRI URN vocabularies for characteristics that require consistent, machine-readable semantics across IRI facilities. These URNs are used as attribute values when describing service resources.

Controlled attribute URNs are distinct from the resource type URNs defined in Section 4. A resource type URN identifies **what kind of service resource is being represented**, while a controlled attribute URN identifies a standardized **technology, protocol, or API characteristic of that resource**. Endpoint URLs, technology versions, and model names use the corresponding JSON scalar or object fields rather than additional resource-type URNs.

| Controlled family | URN | Short name | Description | Status |
|---|---|---|---|---|
| `urn:doe-iri:service:dtn-technology` | [`urn:doe-iri:service:dtn-technology:globus`](./urn-registry-attributes-service-dtn.md) | Globus | A DTN service technology or implementation provided by Globus. | `provisional` |
| `urn:doe-iri:service:dtn-technology` | [`urn:doe-iri:service:dtn-technology:xrootd`](./urn-registry-attributes-service-dtn.md) | XRootD | A DTN service technology or implementation provided by XRootD. | `provisional` |
| `urn:doe-iri:service:transfer-protocol` | [`urn:doe-iri:service:transfer-protocol:https`](./urn-registry-attributes-service-dtn.md) | HTTPS | The Hypertext Transfer Protocol Secure protocol family for transfer endpoints. | `provisional` |
| `urn:doe-iri:service:transfer-protocol` | [`urn:doe-iri:service:transfer-protocol:gridftp`](./urn-registry-attributes-service-dtn.md) | GridFTP | The GridFTP protocol for high-performance, managed data transfer. | `provisional` |
| `urn:doe-iri:service:transfer-protocol` | [`urn:doe-iri:service:transfer-protocol:xrootd`](./urn-registry-attributes-service-dtn.md) | XRootD | The XRootD protocol for high-performance data access and transfer. | `provisional` |
| `urn:doe-iri:service:transfer-protocol` | [`urn:doe-iri:service:transfer-protocol:sftp`](./urn-registry-attributes-service-dtn.md) | SFTP | The SSH File Transfer Protocol. | `provisional` |
| `urn:doe-iri:service:inference-api` | [`urn:doe-iri:service:inference-api:openai`](./urn-registry-attributes-service-inference.md) | OpenAI-compatible API | An inference API family compatible with the OpenAI API. | `provisional` |
| `urn:doe-iri:service:inference-api` | [`urn:doe-iri:service:inference-api:kserve-v2`](./urn-registry-attributes-service-inference.md) | KServe V2 | The KServe V2 inference API family. | `provisional` |
| `urn:doe-iri:service:inference-technology` | [`urn:doe-iri:service:inference-technology:vllm`](./urn-registry-attributes-service-inference.md) | vLLM | The vLLM inference serving technology. | `provisional` |
| `urn:doe-iri:service:inference-technology` | [`urn:doe-iri:service:inference-technology:hugging-face-tgi`](./urn-registry-attributes-service-inference.md) | Hugging Face TGI | The Hugging Face Text Generation Inference serving technology. | `provisional` |
| `urn:doe-iri:service:inference-technology` | [`urn:doe-iri:service:inference-technology:nvidia-triton`](./urn-registry-attributes-service-inference.md) | NVIDIA Triton | The NVIDIA Triton inference serving technology. | `provisional` |
| `urn:doe-iri:service:inference-technology` | [`urn:doe-iri:service:inference-technology:kserve`](./urn-registry-attributes-service-inference.md) | KServe | The KServe inference serving technology. | `provisional` |

The complete index of registered service controlled values is maintained in the [Service Taxonomy and URN Index](./urn-registry-type-service-taxonomy.md).

## 6. Service Resource Relationships

Relationships between service resources and infrastructure resources are represented using registered IRI link relations. These relationships describe relatively stable topology and configured access without embedding host or storage identifiers in ordinary attributes.

| Relationship | Status | Source | Target | Cardinality | Target Stability | Authorization Affects Visibility | Description |
|---|---|---|---|---|---|---|---|
| [`iri:hostedOn`](./link-profile-hosted-on.md) | `provisional` | DTN Service or Inference Service | Compute System or Compute Node | `0..*` targets from a service | Static resource representation. The target identifies hosting infrastructure independently of current routing, live replica placement, health, or availability. | Yes | Indicates that the target provides hosting infrastructure for the source service. |
| [`iri:accessesMount`](./link-profile-accesses-mount.md) | `provisional` | DTN Service | Filesystem Mount | `0..*` targets from a DTN service | Relatively static relationship resource. The target identifies configured filesystem access topology, not current mount availability, endpoint reachability, credential validity, unrestricted access, or transfer activity. | Yes | Indicates that the DTN service is configured to access a filesystem through the identified mount relationship resource for transfer operations. |
| [`iri:locatedAt`](./link-profile-located-at.md) | `provisional` | Any DOE-IRI Resource | Facility API Site representation | `1` semantic target | Independently identifiable, relatively stable Site representation | No; `site_uri` already discloses Site identity | Indicates the relatively stable physical and administrative Site associated with the source Resource. |

`iri:hostedOn` does not state that a target is currently healthy, serving requests, selected by a router, or running a particular live replica. `iri:accessesMount` does not imply current mount availability, endpoint reachability, credential validity, unrestricted authorization, or an active transfer. Operational state is separate from these relatively stable relationships.

Authorization MAY affect relationship visibility. The absence of a visible link is not proof that the relationship does not exist.

---

*DOE Integrated Research Infrastructure — URN Registry: Service*
