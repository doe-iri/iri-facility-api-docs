# Service Resource Types Design

## Status

Approved in-chat design for adding two refined DOE-IRI service resource types and their supporting registry documentation.

Date: 2026-08-13

## 1. Objective

Extend the DOE-IRI registry with these resource types:

```text
urn:doe-iri:resource:service:dtn
urn:doe-iri:resource:service:inference
```

The change will provide complete type registries, attribute profiles, controlled vocabularies, relationship profiles, examples, navigation, cross-domain references, and governing-specification alignment.

## 2. Governing Semantic Decisions

### 2.1. Namespace roles

The canonical resource-type hierarchy is:

```text
urn:doe-iri:resource:service
├── dtn
└── inference
```

The namespaces have distinct roles:

```text
urn:doe-iri:resource:service:*
    Service resource types.

urn:doe-iri:service:*
    Controlled vocabulary values describing service resources.
```

The governing URN specification currently contains draft mappings and examples that use `urn:doe-iri:service:*` as resource types. Those references will be reconciled with the active registry and this design:

- legacy `service` maps to `urn:doe-iri:resource:service`;
- legacy `website` maps to `urn:doe-iri:resource:website`;
- service-specific controlled values remain beneath `urn:doe-iri:service`;
- the draft `urn:doe-iri:service:dtn:globus` resource-type example is replaced by the controlled technology value `urn:doe-iri:service:dtn-technology:globus`.

No deprecated alias will be registered for the draft service-type forms because they are not entries in the active registry. If evidence of deployed producers using those forms emerges, compatibility registration and replacement semantics will require separate review.

### 2.2. Resource boundaries

A DTN service resource represents a consumable data-transfer service. It does not represent an individual host or compute node. A node hosting a DTN remains a `urn:doe-iri:resource:compute:node`, and a single DTN service may be hosted across multiple nodes or systems.

An inference service resource represents a consumable model-invocation service. It does not make individual model artifacts, model deployments, endpoint URLs, replicas, hosts, or accelerators independent IRI resources. Those concepts may become resource types later only when a use case requires independent identity, lifecycle, relationships, authorization, or state.

The two service types are siblings in the semantic classification hierarchy. Hosting, filesystem access, and other topology are represented with link relations rather than deeper resource-type nesting.

### 2.3. Definition and state

Relatively stable service configuration belongs in the resource attribute profiles. Operational information remains separate.

For inference services:

- `served_models` describes the configured or advertised model catalog in the resource definition;
- `active_models` identifies the subset currently loaded and available, in a companion operational-state schema.

The registry will document the companion state schema without changing the core Facility API OpenAPI in this change. Integration into the governing state representation is future specification work.

## 3. Lifecycle

The existing parent remains:

| URN | Status |
|---|---|
| `urn:doe-iri:resource:service` | `active` |

The following new entries will be `provisional`:

- both refined service resource types;
- all initial service controlled vocabulary values;
- `iri:hosted-on`;
- `iri:accesses-mount`.

The subtype metadata will identify `urn:doe-iri:resource:service` as the parent, IRI v2.0 as the introduction version, and legacy `service` as the broad legacy value. The legacy value does not distinguish the two refinements.

## 4. DTN Attribute Profile

The DTN profile applies to:

```text
urn:doe-iri:resource:service:dtn
```

Only `schema_version` is mandatory. Optional attributes are omitted when unknown rather than guessed.

| Attribute | Type | Meaning |
|---|---|---|
| `schema_version` | string | Profile version; initially `"1.0.0"`. |
| `dtn_technology` | DOE-IRI URN string | Technology or implementation providing the DTN service. |
| `technology_version` | string | Deployed technology version when useful and known. |
| `transfer_protocols` | array of DOE-IRI URN strings | Transfer protocols supported by the DTN service. |
| `transfer_endpoints` | array of `TransferEndpoint` objects | Configured endpoints through which transfers can be requested or performed. |

### 4.1. DTN technology vocabulary

Register:

```text
urn:doe-iri:service:dtn-technology:globus
urn:doe-iri:service:dtn-technology:xrootd
```

Globus and XRootD are technologies, not resource subtypes. The profile will distinguish technology from protocol and will not define a `urn:doe-iri:resource:service:dtn:globus` subtype.

### 4.2. Transfer protocol vocabulary

Register:

```text
urn:doe-iri:service:transfer-protocol:https
urn:doe-iri:service:transfer-protocol:gridftp
urn:doe-iri:service:transfer-protocol:xrootd
urn:doe-iri:service:transfer-protocol:sftp
```

XRootD may appear as both a technology and a protocol because those values answer different questions. A DTN may expose multiple protocols independently of its implementation technology.

### 4.3. Transfer endpoints

Each `TransferEndpoint` contains:

| Property | Required | Type | Meaning |
|---|---:|---|---|
| `url` | yes | URI string | Configured network endpoint. |
| `protocol` | yes | DOE-IRI URN string | Registered transfer protocol exposed at the endpoint. |
| `name` | no | string | Human-readable endpoint label. |

Endpoint presence is configuration, not a guarantee of current reachability, authorization, or availability.

### 4.4. DTN state exclusions

The definition profile will exclude current endpoint reachability, active transfers, queue depth, transfer rate, transient host placement, credential validity, health, and availability.

## 5. Inference Attribute and State Profiles

The inference attribute profile applies to:

```text
urn:doe-iri:resource:service:inference
```

Only `schema_version` is mandatory. Optional attributes are omitted when unknown rather than guessed.

| Attribute | Type | Meaning |
|---|---|---|
| `schema_version` | string | Profile version; initially `"1.0.0"`. |
| `inference_technology` | DOE-IRI URN string | Serving technology or implementation. |
| `technology_version` | string | Deployed technology version when useful and known. |
| `inference_apis` | array of DOE-IRI URN strings | Supported inference APIs. |
| `inference_endpoints` | array of `InferenceEndpoint` objects | Configured service endpoints. |
| `served_models` | array of `ServedModel` objects | Configured or advertised model catalog. |

### 5.1. Inference API vocabulary

Register:

```text
urn:doe-iri:service:inference-api:openai
urn:doe-iri:service:inference-api:kserve-v2
```

These identify API families, not the serving technology or current endpoint state.

### 5.2. Inference technology vocabulary

Register:

```text
urn:doe-iri:service:inference-technology:vllm
urn:doe-iri:service:inference-technology:hugging-face-tgi
urn:doe-iri:service:inference-technology:nvidia-triton
urn:doe-iri:service:inference-technology:kserve
```

Clients must not infer supported APIs, model availability, capacity, or operational state solely from the technology value.

### 5.3. Inference endpoints

Each `InferenceEndpoint` contains:

| Property | Required | Type | Meaning |
|---|---:|---|---|
| `url` | yes | URI string | Configured inference endpoint. |
| `api` | yes | DOE-IRI URN string | Registered inference API exposed at the endpoint. |
| `name` | no | string | Human-readable endpoint label. |

Endpoint presence does not guarantee reachability, authorization, or current service availability.

### 5.4. Served model catalog

Each `ServedModel` contains:

| Property | Required | Type | Meaning |
|---|---:|---|---|
| `id` | yes | string | Service-local stable identifier used by clients and state references. |
| `name` | yes | string | Human-readable model name. |
| `version` | no | string | Advertised model version. |
| `model_uri` | no | URI string | Persistent catalog, model-card, or descriptive model URI. |

`ServedModel.id` values must be unique within a service resource. This is a semantic constraint because the repository's OpenAPI-compatible schema dialect cannot express uniqueness by one property of array objects.

The catalog describes configured or advertised models. It does not assert that every catalog entry is currently loaded or ready.

### 5.5. Companion operational state

Define an `InferenceServiceState` schema alongside the inference profile:

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | string | State-profile version; initially `"1.0.0"`. |
| `active_models` | unique array of strings | IDs from `served_models` that are currently loaded and available for requests. |

`schema_version` is required. `active_models` may be omitted when the active set is not reported or is unknown. An explicitly empty array means that the service reports no active models. Each reported ID must correspond to a `served_models.id` in the associated resource definition.

The state schema will not include deployment replicas, GPU inventory or utilization, queue depth, rate limits, traffic, latency, token throughput, or service availability. Those may be defined through future operational-state work when concrete interoperability requirements exist.

## 6. Relationship Profiles

### 6.1. `iri:hosted-on`

| Field | Design |
|---|---|
| Source | `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference` |
| Target | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` |
| Cardinality | `0..*` targets from a service |
| Target classification | Resource |
| Stability | Relatively static hosting topology |
| Authorization affects visibility | Yes |

`iri:hosted-on` means that the target provides hosting infrastructure for the source service. It does not state that the target is currently healthy, serving requests, selected by a router, or running a particular live replica. Operational failover, scale-to-zero, and temporary placement changes do not by themselves alter the stable relationship.

A provider may expose system-level or node-level topology. Absence of a visible link is not proof that the service has no host.

### 6.2. `iri:accesses-mount`

| Field | Design |
|---|---|
| Source | `urn:doe-iri:resource:service:dtn` |
| Target | `urn:doe-iri:resource:storage:mount` |
| Cardinality | `0..*` targets from a DTN service |
| Target classification | Relationship resource |
| Stability | Relatively static configured access topology |
| Authorization affects visibility | Yes |

`iri:accesses-mount` means that a DTN service is configured to access a filesystem through the identified mount relationship resource for transfer operations. The mount is the correct target because it carries the exposure-specific path, protocol, access mode, and consuming-system relationship.

The link does not imply current mount availability, endpoint reachability, credential validity, unrestricted read or write authorization, or an active transfer. It remains stable through ordinary outages, maintenance, failover, and idle periods.

No inverse relation or direct DTN-to-filesystem relation will be registered initially. Co-location through `iri:hosted-on` and `iri:mounted-on` must not be treated as proof that a DTN can use a mount; `iri:accesses-mount` expresses the intentional configured access.

### 6.3. HAL examples

Each link profile will include singular and plural HAL representations as applicable. Domain examples will show:

```text
DTN Service
├── iri:hosted-on ──────> Compute System or Compute Node
└── iri:accesses-mount ─> Filesystem Mount
                              │
                              └── iri:mounted-on ─> Compute System
```

and:

```text
Inference Service
└── iri:hosted-on ─> Compute System or Compute Node
```

Authorization-filtered examples and prose will state that absence is not necessarily semantic absence.

## 7. Documentation Structure

Create:

```text
registry/urn-registry-type-service.md
registry/urn-registry-type-service-taxonomy.md
registry/urn-registry-attributes-service-dtn.md
registry/urn-registry-attributes-service-inference.md
registry/link-profile-hosted-on.md
registry/link-profile-accesses-mount.md
```

The inference attribute document will contain a clearly separate companion operational-state section and schema. No new registry-wide state-profile filename convention will be introduced by this change.

Update:

```text
registry/urn-registry-root.md
registry/README.md
registry/urn-registry-type-compute.md
registry/urn-registry-type-compute-taxonomy.md
registry/urn-registry-type-storage.md
registry/urn-registry-type-storage-taxonomy.md
rfc/rfc-iri-urn-structure-and-registry.md
rfc/rfc-type-specific-attributes.md
docs/ai-project-context.md
```

The compute documents will index `iri:hosted-on` as an incoming cross-domain relationship. The storage documents will index `iri:accesses-mount` as an incoming cross-domain relationship. Existing user-owned uncommitted edits in overlapping files must be preserved.

The root registry and registry README will delegate the service subtree to the new domain documents and add navigation to both attribute and relationship profiles.

## 8. Schema Conventions

Profiles will follow the established registry structure and OpenAPI-compatible schema style:

- `type: object` profiles;
- required `schema_version` with enum `"1.0.0"`;
- the established `IriUrn` reusable schema and DOE-IRI URN pattern;
- `uniqueItems: true` for URN arrays and `active_models`;
- URI formatting for endpoint URLs and `model_uri`;
- nonempty semantic identifiers and names where supported consistently by the repository's schema dialect;
- optional fields omitted rather than populated with guessed values.

Controlled fields will document the exact vocabulary family that applies. Examples and prose will not imply that arbitrary DOE-IRI URNs from unrelated families are valid merely because they satisfy the lexical URN pattern.

## 9. Examples

The documentation will include at least:

1. A Globus DTN using HTTPS and GridFTP, hosted on compute infrastructure and accessing multiple filesystem mounts.
2. An XRootD DTN exposing XRootD and HTTPS endpoints, demonstrating the distinction between XRootD technology and XRootD protocol.
3. A vLLM inference service exposing an OpenAI-compatible endpoint and a configured model catalog.
4. An `InferenceServiceState` instance listing the IDs of the currently active models.
5. HAL examples for both registered link relations.

Examples must use internally consistent resource types, controlled values, endpoint declarations, model IDs, and relationship targets.

## 10. Validation

Before completion:

1. Check all relative Markdown links in changed registry and RFC documents.
2. Search for stale uses of `urn:doe-iri:service:*` as resource types and reconcile all relevant occurrences.
3. Verify that resource-type trees and tables contain the same entries.
4. Verify that service attribute profiles and the consolidated service taxonomy contain the same controlled values.
5. Verify that service, compute, and storage relationship indexes agree with the two link profiles.
6. Validate schema fragments to the extent supported by repository tooling and inspect all examples for schema consistency.
7. Confirm that `served_models` and `active_models` remain in definition and state respectively.
8. Review the complete git diff and confirm that pre-existing user changes were neither reverted nor accidentally included in an implementation commit.

## 11. Non-Goals

This change will not:

- create product-specific DTN resource subtypes;
- make models, deployments, endpoints, replicas, or accelerators independent service resources;
- add direct DTN-to-filesystem or inverse mount relationships;
- extend `iri:mounted-on` to compute-node targets;
- define authentication-method, modality, deployment, rate-limit, or performance vocabularies;
- encode current service health, traffic, throughput, latency, queue depth, or utilization in stable attributes;
- integrate `InferenceServiceState` into the core Facility API OpenAPI;
- deprecate unregistered draft URN examples as if they were active registry assignments.

## 12. Architecture Review Note

Repository guidance calls for the `registry_architect` role for new resource types and vocabularies. That role could not launch because its configured model was unavailable for the active account. A read-only fallback architecture reviewer performed the required ontology and compatibility analysis, and the resulting decisions were reviewed and approved section by section in the main task.
