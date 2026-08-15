# 1. Taxonomy

The following service taxonomy defines the resource types and controlled attribute vocabularies used to model service resources within an IRI facility.

```text
urn:doe-iri
│
├── resource
│   └── service
│       ├── dtn       - "What consumable data-transfer service can I use?"
│       └── inference - "What consumable model-invocation service can I use?"
│
└── service           - The service controlled attribute vocabulary
    │
    │   DTN SERVICE ATTRIBUTES
    │
    ├── dtn-technology
    │   ├── globus
    │   └── xrootd
    │
    ├── transfer-protocol
    │   ├── https
    │   ├── gridftp
    │   ├── xrootd
    │   └── sftp
    │
    │   INFERENCE SERVICE ATTRIBUTES
    │
    ├── inference-api
    │   ├── openai
    │   └── kserve-v2
    │
    └── inference-technology
        ├── vllm
        ├── hugging-face-tgi
        ├── nvidia-triton
        └── kserve
```

# 2. Service URN Definitions

| URN | Short name | Description | Status |
|---|---|---|---|
| [`urn:doe-iri:resource:service:dtn`](./urn-registry-attributes-service-dtn.md) | DTN Service | A consumable data-transfer service. It does not identify an individual host or compute node. | `provisional` |
| [`urn:doe-iri:resource:service:inference`](./urn-registry-attributes-service-inference.md) | Inference Service | A consumable model-invocation service. It does not identify a model, deployment, endpoint, replica, or accelerator. | `provisional` |
| [`urn:doe-iri:service:dtn-technology:globus`](./urn-registry-attributes-service-dtn.md) | Globus | A DTN service technology or implementation provided by Globus. | `provisional` |
| [`urn:doe-iri:service:dtn-technology:xrootd`](./urn-registry-attributes-service-dtn.md) | XRootD | A DTN service technology or implementation provided by XRootD. | `provisional` |
| [`urn:doe-iri:service:transfer-protocol:https`](./urn-registry-attributes-service-dtn.md) | HTTPS | The Hypertext Transfer Protocol Secure protocol family for transfer endpoints. | `provisional` |
| [`urn:doe-iri:service:transfer-protocol:gridftp`](./urn-registry-attributes-service-dtn.md) | GridFTP | The GridFTP protocol for high-performance, managed data transfer. | `provisional` |
| [`urn:doe-iri:service:transfer-protocol:xrootd`](./urn-registry-attributes-service-dtn.md) | XRootD | The XRootD protocol for high-performance data access and transfer. | `provisional` |
| [`urn:doe-iri:service:transfer-protocol:sftp`](./urn-registry-attributes-service-dtn.md) | SFTP | The SSH File Transfer Protocol. | `provisional` |
| [`urn:doe-iri:service:inference-api:openai`](./urn-registry-attributes-service-inference.md) | OpenAI-compatible API | An inference API family compatible with the OpenAI API. | `provisional` |
| [`urn:doe-iri:service:inference-api:kserve-v2`](./urn-registry-attributes-service-inference.md) | KServe V2 | The KServe V2 inference API family. | `provisional` |
| [`urn:doe-iri:service:inference-technology:vllm`](./urn-registry-attributes-service-inference.md) | vLLM | The vLLM inference serving technology. | `provisional` |
| [`urn:doe-iri:service:inference-technology:hugging-face-tgi`](./urn-registry-attributes-service-inference.md) | Hugging Face TGI | The Hugging Face Text Generation Inference serving technology. | `provisional` |
| [`urn:doe-iri:service:inference-technology:nvidia-triton`](./urn-registry-attributes-service-inference.md) | NVIDIA Triton | The NVIDIA Triton inference serving technology. | `provisional` |
| [`urn:doe-iri:service:inference-technology:kserve`](./urn-registry-attributes-service-inference.md) | KServe | The KServe inference serving technology. | `provisional` |

# 3. Service Resource Relationships

Registered IRI link relations describe service-domain topology, configured access, and applicable cross-model navigation without embedding host or storage identifiers in ordinary attributes. Their targets may be DOE-IRI Resource representations, relationship resources, or, for `iri:located-at`, the Facility API Site representation; the Site target is not a DOE-IRI typed Resource.

| Relationship | Status | Source | Target | Cardinality | Target classification | Target Stability | Authorization Affects Visibility | Description |
|---|---|---|---|---|---|---|---|---|
| [`iri:hosted-on`](./link-profile-hosted-on.md) | `provisional` | `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference` | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` | `0..*` targets from a service | Resource | Static resource representation. The target identifies hosting infrastructure independently of current routing, live replica placement, health, or availability. | Yes | The target provides hosting infrastructure for the source service. It does not state that the target is currently healthy, serving requests, selected by a router, or running a particular live replica. |
| [`iri:accesses-mount`](./link-profile-accesses-mount.md) | `provisional` | `urn:doe-iri:resource:service:dtn` | `urn:doe-iri:resource:storage:mount` | `0..*` targets from a DTN service | Relationship resource | Relatively static relationship resource. The target identifies configured filesystem access topology, not current mount availability, endpoint reachability, credential validity, unrestricted access, or transfer activity. | Yes | The DTN service is configured to access a filesystem through the identified mount relationship resource for transfer operations. It does not imply current mount availability, endpoint reachability, credential validity, unrestricted read or write authorization, or an active transfer. |
| [`iri:located-at`](./link-profile-located-at.md) | `provisional` | Any DOE-IRI `Resource` representation | Facility API Site representation | `1` semantic target | Site API representation | Independently identifiable, relatively stable Site representation | No; `site_uri` already discloses Site identity | The target is the relatively stable physical and administrative Site associated with the source Resource. |

Authorization MAY affect visibility of `iri:hosted-on` and `iri:accesses-mount`; the absence of either visible link is not proof that the relationship does not exist. `iri:located-at` MUST NOT be independently authorization-filtered while the required `site_uri` field is returned because that field already discloses Site identity.

---

*DOE Integrated Research Infrastructure — URN Registry: Service Taxonomy*
