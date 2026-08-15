# Attribute Profile: `urn:doe-iri:resource:service:inference`

This document defines attributes for the `urn:doe-iri:resource:service:inference` resource type.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:service:inference` |
| Short name | Inference Service |
| Description | A consumable model-invocation service. It does not identify a model, deployment, endpoint, replica, host, or accelerator. |
| Parent URN | `urn:doe-iri:resource:service` |
| Status | `provisional` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | [Service Resource Types Design](../docs/superpowers/specs/2026-08-13-service-resource-types-design.md). |
| Legacy value | `service` enumeration. The broad legacy value does not distinguish this refinement. |
| Examples | `urn:doe-iri:resource:service:inference` |
| Notes | This profile defines relatively stable characteristics of a consumable inference service. |

## 2. Introduction

An inference service is a consumable service through which a facility makes model-invocation operations available. It is distinct from the compute systems or compute nodes that host it; hosting topology is represented separately using `iri:hosted-on`.

This profile records relatively stable service definition. Models, deployments, endpoints, replicas, hosts, and accelerators are not independent resource types in this profile. Endpoint URLs and served-model catalog entries are attributes of the inference service because they normally do not require independent IRI identity, lifecycle, relationships, or state.

The profile distinguishes inference APIs from inference technologies. An API identifies an invocation interface exposed to consumers; a technology identifies the implementation providing the service. A technology can expose one or more APIs, and an API can be exposed by more than one technology.

Except for `schema_version`, attributes in this profile are optional. Omit an optional attribute when it is unknown or not relevant instead of guessing a technology, version, API, endpoint, or model. The absence of an optional attribute means that the information has not been provided; it does not imply a particular value, capability, or lack of support.

## 3. Taxonomy

The taxonomy distinguishes the inference service resource type from controlled values used to describe it. Only attributes represented by controlled DOE-IRI URNs appear in the controlled-vocabulary portion of the tree.

```text
urn:doe-iri
│
├── resource
│   └── service
│       └── inference
│
└── service
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

The complete service resource and controlled-vocabulary index is maintained in the [Service Taxonomy and URN Index](urn-registry-type-service-taxonomy.md).

## 4. Inference Service Attribute Profile

The Inference Service Attribute Profile defines the attributes that MAY describe a resource of type `urn:doe-iri:resource:service:inference`.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition (e.g. `"1.0.0"`). | yes |
| `inference_technology` | 1.0.0 | IRI URN string | Identifies the technology or implementation providing the inference service. | no |
| `technology_version` | 1.0.0 | string | Identifies the deployed technology version when useful and known. | no |
| `inference_apis` | 1.0.0 | Array IRI URN string | Identifies inference API families the service advertises to consumers. | no |
| `inference_endpoints` | 1.0.0 | Array InferenceEndpoint | Identifies configured endpoints through which consumers can invoke the service. | no |
| `served_models` | 1.0.0 | Array ServedModel | Catalogs models configured to be served by the service. | no |

### 4.1. Inference APIs

The `inference_apis` attribute identifies inference API families that the inference service advertises to consumers. It is an array because a service may expose more than one API. Each value MUST be a registered DOE-IRI URN from the `urn:doe-iri:service:inference-api` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:service:inference-api:openai` | OpenAI-compatible API | An inference API family compatible with the OpenAI API. | `provisional` |
| `urn:doe-iri:service:inference-api:kserve-v2` | KServe V2 | The KServe V2 inference API family. | `provisional` |

The API identifies the interface through which consumers invoke models and is distinct from the technology that implements the service. Facilities MUST explicitly advertise inference APIs; clients MUST NOT infer APIs or endpoint availability solely from `inference_technology`.

### 4.2. Inference Technology

The `inference_technology` attribute identifies the technology or implementation providing the inference service. Its value MUST be a registered DOE-IRI URN from the `urn:doe-iri:service:inference-technology` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:service:inference-technology:vllm` | vLLM | The vLLM inference serving technology. | `provisional` |
| `urn:doe-iri:service:inference-technology:hugging-face-tgi` | Hugging Face TGI | The Hugging Face Text Generation Inference serving technology. | `provisional` |
| `urn:doe-iri:service:inference-technology:nvidia-triton` | NVIDIA Triton | The NVIDIA Triton inference serving technology. | `provisional` |
| `urn:doe-iri:service:inference-technology:kserve` | KServe | The KServe inference serving technology. | `provisional` |

These values identify technologies, not resource subtypes. Clients MUST NOT infer available APIs, endpoint reachability, authorization, capacity, served-model activity, or other operational availability solely from `inference_technology`.

### 4.3. Inference Endpoints

The `inference_endpoints` attribute identifies configured network endpoints through which consumers can invoke the service. A service may expose multiple endpoints, including endpoints for different API families.

Each `InferenceEndpoint` contains:

| Property | Type | Description | Mandatory |
|---|---|---|---|
| `url` | string URI | Configured network endpoint for inference requests. | yes |
| `api` | IRI URN string | Registered inference API family exposed by the endpoint. | yes |
| `name` | string | Human-readable endpoint label. | no |

The `api` value MUST come from the `urn:doe-iri:service:inference-api:*` family. An endpoint is configured access information, not a claim that it is currently reachable, available to a particular consumer, or authorized for a particular request.

### 4.4. Served Models

The `served_models` attribute catalogs models configured to be served by the inference service. Each `ServedModel` has a stable, service-local `id` and a human-readable `name`; `version` and `model_uri` are optional descriptive values.

Each `ServedModel.id` MUST be unique within a `served_models` array. The companion state contract's `active_models` field contains IDs of served models that are currently loaded and available for requests. Model activity is operational state, so a model appearing in `served_models` is not by itself a claim that it is currently loaded or able to serve requests.

### 4.5. State Exclusions

This profile excludes current endpoint reachability, health, availability, request rate, queue depth, active replicas, model loading, and current model activity from the stable resource definition. Those dynamic operational facts SHOULD be represented through applicable resource-state mechanisms.

## 5. Inference Service JSON Schema

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

    InferenceEndpoint:
      type: object
      required:
        - url
        - api
      properties:
        url:
          type: string
          format: uri
        api:
          $ref: '#/components/schemas/IriUrn'
        name:
          type: string

    ServedModel:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
        name:
          type: string
        version:
          type: string
        model_uri:
          type: string
          format: uri

    InferenceServiceAttributes:
      type: object
      description: >
        Attributes describing an inference service resource with resource type
        urn:doe-iri:resource:service:inference.
      required:
        - schema_version
      properties:
        schema_version:
          type: string
          enum:
            - "1.0.0"
        inference_technology:
          $ref: '#/components/schemas/IriUrn'
        technology_version:
          type: string
        inference_apis:
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
        inference_endpoints:
          type: array
          items:
            $ref: '#/components/schemas/InferenceEndpoint'
        served_models:
          type: array
          items:
            $ref: '#/components/schemas/ServedModel'
```

## 6. Companion Inference Service Operational-State Schema

`InferenceServiceState` is a companion operational-state contract, separate from `InferenceServiceAttributes` and this stable resource definition. It is not an integration statement for the core Facility API OpenAPI.

| Field | Type | Description | Mandatory |
|---|---|---|---|
| `schema_version` | string | Version of the state-profile definition (e.g. `"1.0.0"`). | yes |
| `active_models` | Unique array of strings | IDs of served models that are currently loaded and available for requests. Omission means current model activity is unknown or unreported; an empty array means the service reports no active models. | no |

```yaml
InferenceServiceState:
  type: object
  required:
    - schema_version
  properties:
    schema_version:
      type: string
      enum:
        - "1.0.0"
    active_models:
      type: array
      description: >
        IDs of served models that are currently loaded and available for
        requests. Omission means current model activity is unknown or
        unreported; an empty array means the service reports no active models.
      uniqueItems: true
      items:
        type: string
```

The `active_models` field contains IDs of served models that are currently loaded and available for requests. Each item references a `served_models.id` from the corresponding definition instance. Omission of `active_models` means that current model activity is unknown or unreported. An empty `active_models` array means the service reports no active models.

## 7. Example Inference Service Definition and State JSON Instances

The following vLLM inference service advertises an OpenAI-compatible endpoint and catalogs two models. This definition instance describes configured service characteristics, not current model activity.

```json
{
  "schema_version": "1.0.0",
  "inference_technology": "urn:doe-iri:service:inference-technology:vllm",
  "technology_version": "0.6.3",
  "inference_apis": [
    "urn:doe-iri:service:inference-api:openai"
  ],
  "inference_endpoints": [
    {
      "url": "https://inference.example.gov/v1",
      "api": "urn:doe-iri:service:inference-api:openai",
      "name": "OpenAI-compatible inference endpoint"
    }
  ],
  "served_models": [
    {
      "id": "llama-3.1-8b-instruct",
      "name": "Llama 3.1 8B Instruct",
      "version": "3.1",
      "model_uri": "https://models.example.gov/llama-3.1-8b-instruct"
    },
    {
      "id": "mistral-7b-instruct-v0.3",
      "name": "Mistral 7B Instruct v0.3",
      "version": "0.3",
      "model_uri": "https://models.example.gov/mistral-7b-instruct-v0.3"
    }
  ]
}
```

The following separate operational-state instance reports one currently active model. Its ID exactly matches a `served_models.id` in the definition instance above.

```json
{
  "schema_version": "1.0.0",
  "active_models": [
    "llama-3.1-8b-instruct"
  ]
}
```

---

*DOE Integrated Research Infrastructure — URN Registry: Inference Service*
