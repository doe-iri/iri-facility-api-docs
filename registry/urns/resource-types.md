# DOE-IRI Resource Type URNs

This is the authoritative registry and index of assigned
`urn:doe-iri:resource:*` values. The governing [DOE-IRI URN
specification](../../rfc/rfc-iri-urn-structure-and-registry.md) defines
namespace rules; Resource Definition profiles define the type-specific
semantics of a Resource representation.

| URN | Short name | Semantic definition | Parent | Status | Legacy mapping | Definition profile |
|---|---|---|---|---|---|---|
| `urn:doe-iri:resource:compute` | Compute | Generic compute resource. | `urn:doe-iri:resource` | `active` | `compute` | — |
| `urn:doe-iri:resource:compute:system` | Compute System | Managed computing environment composed of compute nodes and supporting infrastructure. | `urn:doe-iri:resource:compute` | `provisional` | `compute` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `urn:doe-iri:resource:compute:node` | Compute Node | Individual computing host that provides processing, memory, and local resources. | `urn:doe-iri:resource:compute` | `provisional` | `compute` | [Compute Node](../profiles/resource-definition/compute/node.md) |
| `urn:doe-iri:resource:compute:cpu` | CPU | Central processor or processor package associated with a compute node. | `urn:doe-iri:resource:compute` | `provisional` | `compute` | [CPU](../profiles/resource-definition/compute/cpu.md) |
| `urn:doe-iri:resource:compute:gpu` | GPU | Highly parallel accelerator associated with a compute node. | `urn:doe-iri:resource:compute` | `provisional` | `compute` | [GPU](../profiles/resource-definition/compute/gpu.md) |
| `urn:doe-iri:resource:storage` | Storage | Generic storage resource. | `urn:doe-iri:resource` | `active` | `storage` | — |
| `urn:doe-iri:resource:storage:system` | Storage System | Managed storage infrastructure that provides logical storage resources. | `urn:doe-iri:resource:storage` | `provisional` | `storage` | [Storage System](../profiles/resource-definition/storage/system.md) |
| `urn:doe-iri:resource:storage:filesystem` | Filesystem | Logical storage resource with files, directories, and filesystem access semantics. | `urn:doe-iri:resource:storage` | `provisional` | `storage` | [Filesystem](../profiles/resource-definition/storage/filesystem.md) |
| `urn:doe-iri:resource:storage:mount` | Filesystem Mount | Exposure of a filesystem to a consuming system at a particular mount location. | `urn:doe-iri:resource:storage` | `provisional` | — | [Filesystem Mount](../profiles/resource-definition/storage/mount.md) |
| `urn:doe-iri:resource:storage:block` | Block Storage | Logical storage resource that presents addressable blocks or volumes. | `urn:doe-iri:resource:storage` | `provisional` | `storage` | [Block Storage](../profiles/resource-definition/storage/block.md) |
| `urn:doe-iri:resource:storage:object` | Object Storage | Logical storage resource that manages independently addressable objects. | `urn:doe-iri:resource:storage` | `provisional` | `storage` | [Object Storage](../profiles/resource-definition/storage/object.md) |
| `urn:doe-iri:resource:service` | Service | Generic service resource. | `urn:doe-iri:resource` | `active` | `service` | — |
| `urn:doe-iri:resource:service:dtn` | DTN Service | Consumable data-transfer service, distinct from its host. | `urn:doe-iri:resource:service` | `provisional` | `service` | [DTN Service](../profiles/resource-definition/service/dtn.md) |
| `urn:doe-iri:resource:service:inference` | Inference Service | Consumable model-invocation service, distinct from its deployment and host. | `urn:doe-iri:resource:service` | `provisional` | `service` | [Inference Service](../profiles/resource-definition/service/inference.md) |
| `urn:doe-iri:resource:network` | Network | Generic network resource. | `urn:doe-iri:resource` | `active` | `network` | — |
| `urn:doe-iri:resource:system` | System | Generic system resource. | `urn:doe-iri:resource` | `active` | `system` | — |
| `urn:doe-iri:resource:website` | Website | Generic website resource. | `urn:doe-iri:resource` | `active` | `website` | — |
| `urn:doe-iri:resource:unknown` | Unknown | Fallback type when a more-specific registered Resource Type is unavailable. | `urn:doe-iri:resource` | `active` | `unknown` | — |

Resource Type URNs classify resources; they do not encode containment or
topology. Registered link relations in [the relation index](../relations/README.md)
define relationships between independently identified resources.

*DOE Integrated Research Infrastructure — URN Registry*
