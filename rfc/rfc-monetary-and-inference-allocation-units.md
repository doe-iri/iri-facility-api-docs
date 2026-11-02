# RFC: Monetary and Inference-Token Allocation Units

## Abstract

An IRI Allocation Entry states a granted quantity (`allocation`) and a consumed quantity (`usage`) in a registered allocation unit (`unit`). The only registered units today are node-hours, bytes, and inodes. Facilities that run IRI resources on commercial cloud infrastructure account for and limit consumption in currency, and facilities that operate inference services account for consumption in model tokens. Neither can be expressed with the current registry.

This RFC requests two allocation-unit registrations, `urn:doe-iri:allocation:currency:usd` and `urn:doe-iri:allocation:inference:tokens`, and defines how producers and consumers interpret them. It also defines a small set of optional, unit-independent Allocation Entry attributes that describe the accounting period, renewal, data freshness, and reconciliation state of an entry, and a Capability attribute that scopes token allocations to specific served models.

This RFC does not change the IRI v2 OpenAPI structural contract. `AllocationEntry.unit` already accepts any URN in the `allocation` category, and `AllocationEntry.attributes` and `Capability.attributes` already exist as optional objects. It does not change the governing URN grammar, because the `allocation` category is already defined.

## Status of This Memo

**Status:** Draft / Proposed

**Target:** IRI Facility API v2 account contract and DOE-IRI URN Registry

| Revision | Author | Date | Notes |
|---|---|---|---|
| 0.1 | Justas Balcas | Oct 13, 2026 | Initial draft. |

The two allocation units in Section 4 are recorded in the DOE-IRI URN Registry in `provisional` status while this RFC is under review. Approval of this RFC moves them to `active`; the registry remains the assignment authority.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Terminology](#3-terminology)
4. [Allocation Unit Registrations](#4-allocation-unit-registrations)
5. [Interpretation Rules](#5-interpretation-rules)
6. [Allocation Entry Attributes](#6-allocation-entry-attributes)
7. [Capability Scoping for Token Allocations](#7-capability-scoping-for-token-allocations)
8. [OpenAPI and Reference Implementation](#8-openapi-and-reference-implementation)
9. [Backward Compatibility](#9-backward-compatibility)
10. [Security and Privacy Considerations](#10-security-and-privacy-considerations)
11. [Alternatives Considered](#11-alternatives-considered)
12. [Future Work](#12-future-work)
13. [Required Specification and Registry Changes](#13-required-specification-and-registry-changes)
14. [References](#14-references)
- [Appendix A. Examples](#appendix-a-examples)

## 1. Introduction

The IRI account API represents allocations as Project Allocations and User Allocations, each carrying an `entries` array. Each Allocation Entry has the structure:

| Property | Required | Meaning |
|---|---:|---|
| `allocation` | Yes | Total quantity granted, as a JSON number. |
| `usage` | Yes | Quantity consumed, as a JSON number. |
| `unit` | Yes | DOE-IRI allocation-unit URN in which `allocation` and `usage` are expressed. |
| `attributes` | No | Optional object for additional entry metadata. Its contents are defined by this RFC (Section 6). |

A Capability advertises the units in which its allocations may be expressed through `units`.

The registered units cover batch compute (`urn:doe-iri:allocation:compute:node-hours`) and storage (`urn:doe-iri:allocation:storage:bytes`, `urn:doe-iri:allocation:storage:inodes`). Two classes of IRI resource do not fit them:

- **Cloud-hosted resources.** A facility that runs compute, storage, or services on a commercial cloud pays for instance time, volumes, load balancers, and network egress at different rates. Node-hours are neither the unit the facility pays in nor the unit it limits, and storage or network charges have no node-hour equivalent. These facilities grant and track allocations in currency.
- **Inference services.** A facility that operates a model-invocation service (`urn:doe-iri:resource:service:inference`) meters consumption in tokens processed. When the service fronts commercial models, the facility often also limits spend in currency.

Without shared units, each facility invents its own unit URNs or reports these allocations outside the IRI API, and portals, resource brokers, and agents cannot display or reason about them consistently.

## 2. Scope

In scope:

- registration of a United States dollar allocation unit and an inference-token allocation unit;
- interpretation rules for those units, and rules for entries that share an `entries` array;
- common optional attributes on `AllocationEntry.attributes`, applicable to every allocation unit;
- an optional Capability attribute that scopes token allocations to served models.

Out of scope:

- prices, rate cards, and conversion between units;
- rate limits such as tokens per minute, requests per minute, or concurrent requests (Section 5.5);
- invoicing, payment, chargeback, and enforcement mechanisms;
- separate input-token and output-token units (Section 12);
- currencies other than USD, which follow the normal registration procedure (Section 4.1);
- IRI v1, whose `AllocationUnit` enumeration is closed (Section 9).

## 3. Terminology

- **Allocation Entry**, **Project Allocation**, **User Allocation**, and **Capability** have the meanings given in the [Project Allocation](../registry/profiles/account/project-allocation.md), [User Allocation](../registry/profiles/account/user-allocation.md), and [Capability](../registry/profiles/account/capability.md) profiles.
- **Monetary unit** means an allocation unit beneath `urn:doe-iri:allocation:currency`.
- **Token unit** means `urn:doe-iri:allocation:inference:tokens`.
- **Accounting period** means the time interval to which an entry's `allocation` and `usage` apply.
- **Input tokens** and **output tokens** mean the tokens an inference service counts for the content supplied to a model and the content the model generates, respectively.

## 4. Allocation Unit Registrations

This RFC requests the following registrations in the `allocation` category of the [DOE-IRI URN Registry](../registry/urns/README.md#5-allocation-unit-registry). Neither has a legacy IRI v1 value.

| URN | Short name | Description |
|---|---|---|
| `urn:doe-iri:allocation:currency:usd` | US dollars | Monetary allocation measured in United States dollars. |
| `urn:doe-iri:allocation:inference:tokens` | Inference tokens | Inference allocation measured in model tokens processed by an inference service, counted as input tokens plus output tokens. |

### 4.1. Naming

The existing units place the measured resource domain in the segment after `allocation` (`compute`, `storage`) and the measure in the leaf. The token unit follows that pattern with the `inference` domain.

Money is not tied to one resource domain: the same currency allocation can fund compute, storage, egress, or inference. The monetary unit therefore uses `currency` as its domain segment and the currency as its leaf. The leaf of a monetary unit is the lowercase form of the [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) alphabetic currency code. This RFC requests only `usd`. Other currencies are registered individually under the normal procedure in the governing URN specification when a facility needs one.

`urn:doe-iri:allocation:currency` and `urn:doe-iri:allocation:inference` are grouping levels, not units. A producer MUST NOT use either one as an Allocation Entry `unit` or in `Capability.units`.

### 4.2. Credits and Facility-Local Units

A monetary unit identifies an amount of real currency. A producer MUST NOT use a monetary unit for virtual credits, service units, charge-factor-weighted hours, or other platform-defined quantities that are not amounts of that currency, even when those quantities are pegged to it. Such units need their own registration, or an Extension URN beneath `urn:doe-iri:allocation` under the delegated-extension rules of the [governing URN specification](./rfc-iri-urn-structure-and-registry.md#4-delegated-extensions).

## 5. Interpretation Rules

### 5.1. Rules for All Allocation Units

These rules apply to every Allocation Entry, including entries in the existing units.

1. **Independent limits.** Each Allocation Entry states an independent limit. When an `entries` array contains more than one entry, the facility MAY refuse further consumption when any one entry is exhausted. This matches existing practice for storage allocations that carry both a bytes entry and an inodes entry.
2. **No derived entries.** A producer MUST NOT publish an Allocation Entry whose values are only a conversion of another entry in the same array, such as the dollar equivalent of a node-hours entry, unless the facility also accounts for and limits that unit independently. A consumer cannot otherwise distinguish a derived figure from an enforced limit.
3. **Repeated units.** An `entries` array MAY contain more than one entry with the same `unit` only when those entries apply to different accounting periods (for example, a monthly limit and a lifetime limit). Each such entry MUST carry the period attributes of Section 6 that distinguish it.
4. **Overrun.** `usage` MAY exceed `allocation`, because of accounting delay or because facility policy permits overrun. A consumer MUST NOT assume that `usage` is less than or equal to `allocation`.
5. **Per-entry arithmetic.** A consumer MAY compute `allocation - usage` within one entry. The caution in the Project Allocation profile still applies: a positive remainder is not proof that the allocation can be consumed now.

### 5.2. Monetary Units

1. `allocation` and `usage` are expressed in the major unit of the currency (dollars for `usd`, not cents), and MAY be fractional.
2. A producer SHOULD round monetary values to no more than six fractional digits. Usage meters commonly record charges smaller than one cent.
3. A consumer MUST NOT compare monetary values for exact equality, and SHOULD use decimal rather than binary floating-point arithmetic when aggregating or displaying them.
4. `usage` is the amount the facility has charged against the allocation under its own pricing, which may be list price, negotiated rates, or an internal rate card. It is not necessarily the amount on any invoice the facility receives from a provider.
5. A consumer MAY aggregate monetary values that share the same `unit`. A consumer MUST NOT aggregate monetary values across different monetary units.

### 5.3. Token Unit

1. A token is the unit in which an inference service counts model input and output, as determined by the serving model's tokenizer and reported by the service.
2. For each accounted request, `urn:doe-iri:allocation:inference:tokens` counts input tokens plus output tokens. For an OpenAI-compatible API (`urn:doe-iri:service:inference-api:openai`) this corresponds to the `total_tokens` value in the response's usage report.
3. Input tokens served from a prompt cache are counted as input tokens. Output tokens include tokens the service reports as generated but does not return to the client, such as reasoning tokens.
4. Operations that produce no generated output, such as embedding requests, count input tokens only.
5. Accounting for failed, rejected, or cancelled requests is facility policy. A facility SHOULD document it.
6. Token counts depend on the tokenizer, so the same text yields different counts on different models. A consumer MUST NOT compare or aggregate token quantities from entries that belong to different Capabilities. Section 7 defines how a Capability identifies the models its token allocations cover.

### 5.4. Entries Combining Monetary and Token Units

A Capability MAY list both a monetary unit and the token unit in `units`, and an allocation for it MAY carry an entry in each. Under Section 5.1, the two entries are independent limits: for example, a project may hold a token allocation for a self-hosted model and, separately, a spending limit that also covers it. Neither entry is a conversion of the other.

### 5.5. Rate Limits Are Not Allocations

Throughput controls such as tokens per minute, requests per minute, or concurrent request limits govern how fast an allocation may be consumed, not how much is granted. They MUST NOT be expressed as Allocation Entries.

## 6. Allocation Entry Attributes

This section defines the contents of the existing optional `AllocationEntry.attributes` object. The attributes apply to every allocation unit, not only the units registered by this RFC.

| Attribute | Type | Meaning |
|---|---|---|
| `period_start` | string, RFC 3339 date-time | Start of the accounting period to which `allocation` and `usage` apply. |
| `period_end` | string, RFC 3339 date-time | End of that accounting period (exclusive). |
| `renewal_interval` | string, ISO 8601 duration | When present, the allocation renews at this interval and `usage` restarts from zero at each renewal. `period_start` and `period_end`, if present, then describe the current interval. |
| `usage_as_of` | string, RFC 3339 date-time | Time at which `usage` was last computed from the facility's accounting data. |
| `usage_basis` | string: `estimated` or `reconciled` | `estimated` means `usage` is provisional and may be revised. `reconciled` means `usage` has been reconciled with the facility's authoritative accounting record. |

Rules:

1. Every attribute is OPTIONAL. Absence means the information was not provided. It does not imply an unbounded period, a non-renewing allocation, real-time usage, or reconciled usage.
2. When both are present, `period_end` MUST be later than `period_start`.
3. `renewal_interval` MUST be a positive ISO 8601 duration, such as `P1D`, `P30D`, `P1M`, or `P1Y`.
4. `usage_basis` values other than `estimated` and `reconciled` are not defined by this RFC. A consumer that encounters another value MUST treat it as unknown.
5. A consumer SHOULD ignore attribute names it does not recognize, consistent with the [Type-Specific Attributes RFC](./rfc-type-specific-attributes.md#54-unknown-resource-types). A producer MUST NOT give the names defined above any other meaning.
6. When `attributes` would be empty, the producer SHOULD omit it.

Monetary usage is commonly computed from delayed or estimated cost data. A producer that reports a monetary unit SHOULD include `usage_as_of` and `usage_basis`.

## 7. Capability Scoping for Token Allocations

An inference service is represented as a Resource of type `urn:doe-iri:resource:service:inference` and catalogs its models in the `served_models` attribute defined by the [Inference Service profile](../registry/profiles/resource-definition/service/inference.md). The Resource advertises the Capabilities it provides through `capability_uris` and, when HAL is used, the [`iri:has-capability`](../registry/relations/has-capability.md) relation.

A Capability whose `units` include the token unit SHOULD cover a single model, or a set of models that the facility accounts for interchangeably. Such a Capability SHOULD identify those models in `Capability.attributes`:

| Attribute | Type | Meaning |
|---|---|---|
| `served_model_ids` | array of string | `ServedModel.id` values, from Resources that provide this Capability, whose invocations are accounted against allocations for this Capability. |

Rules:

1. Each value in `served_model_ids` MUST equal the `id` of a `served_models` item on at least one Resource whose `capability_uris` include this Capability.
2. Values MUST be unique within the array.
3. Absence of `served_model_ids` means the facility has not identified the covered models. It does not mean the Capability covers every model the service serves.
4. `served_model_ids` describes accounting scope only. It does not assert that a model is currently loaded, reachable, or authorized for a particular caller.

## 8. OpenAPI and Reference Implementation

No structural change to the IRI v2 OpenAPI contract is required:

- `AllocationEntry.unit` and the items of `Capability.units` are strings constrained to the `allocation` category pattern, which both new URNs satisfy;
- `allocation` and `usage` are JSON numbers;
- `AllocationEntry.attributes` and `Capability.attributes` are optional objects that permit additional properties.

The OpenAPI `examples` for allocation-unit schemas SHOULD include the new units. The reference implementation ([iri-facility-api-python](https://github.com/doe-iri/iri-facility-api-python)) adds `usd` and `tokens` members to its `AllocationUnit` catalog. Its validation is unchanged because it already accepts any well-formed allocation-category URN.

## 9. Backward Compatibility

- **IRI v2 consumers.** The [governing URN specification](./rfc-iri-urn-structure-and-registry.md#281-opaque-handling) already requires consumers not to reject a syntactically valid URN solely because it is unfamiliar. A consumer that handles only the three existing units SHOULD display an unfamiliar unit by its URN and SHOULD NOT perform arithmetic across entries.
- **Attributes.** The attributes in Sections 6 and 7 are additive and optional. Existing producers conform without change.
- **IRI v1.** The v1 `AllocationUnit` schema is a closed enumeration (`node_hours`, `bytes`, `inodes`). A v1 deployment MUST NOT emit the units registered by this RFC.

## 10. Security and Privacy Considerations

- Monetary allocations and usage can reveal negotiated pricing, project spending, and activity levels, and token usage can reveal how intensively a project uses specific models. A producer SHOULD apply visibility rules to these entries that are at least as strict as for other usage data. Under the existing profiles a producer MAY omit entries the caller is not authorized to see.
- An Allocation Entry reports accounting state. It is not an enforcement point and MUST NOT be treated as authorization to consume. A third party such as a broker or portal that makes admission decisions from reported usage MUST account for staleness, using `usage_as_of` when present.
- Allocation-unit URNs are semantic labels. The security considerations of the [governing URN specification](./rfc-iri-urn-structure-and-registry.md#7-security-considerations) apply.

## 11. Alternatives Considered

| Alternative | Assessment |
|---|---|
| `urn:doe-iri:allocation:cloud:usd` | Ties money to cloud hosting, but inference, network egress, and on-premises chargeback are also priced in currency. |
| `urn:doe-iri:allocation:cost:usd` | "Cost" suggests what the facility pays its providers. The entry states what the project is granted and charged, which may differ (Section 5.2). `currency` names the measure. |
| Separate `currency` property on `AllocationEntry` | Requires an OpenAPI structural change and duplicates information the unit URN already carries. |
| Minor currency units (cents) as integers | Does not avoid fractional values, because meters record sub-cent charges, and differs from how other units are expressed. |
| Separate input-token and output-token units now | Prices often differ between input and output, but no current IRI implementation limits them separately. Deferred to Section 12. |
| One token unit per model, such as `urn:doe-iri:allocation:inference:tokens:<model>` | Would place deployment-specific model names in the shared registry. Capability scoping (Section 7) achieves the same result without registry changes. |

## 12. Future Work

- Refinements `urn:doe-iri:allocation:inference:tokens:input` and `urn:doe-iri:allocation:inference:tokens:output`, as semantic children of the token unit, with explicit rules for arrays that contain both the parent and its children so that consumers do not double-count.
- Additional currencies as facilities require them.
- A shared unit for platform credits that are not currency (Section 4.2).

## 13. Required Specification and Registry Changes

- **URN Registry.** Add both units to the [Allocation Unit Registry](../registry/urns/README.md#5-allocation-unit-registry) in `provisional` status; change them to `active` on approval of this RFC. This revision includes that registry change.
- **Governing URN specification.** No change. Its Section 3.2 lists the initial canonical set; the registry is authoritative for later assignments.
- **Account profiles.** On approval, the Project Allocation and User Allocation profiles reference Sections 5 and 6, and the Capability profile references Section 7. Their examples currently use the legacy value `node_hours`; they SHOULD be updated to canonical URNs at the same time.
- **OpenAPI.** Regenerate from the reference implementation so that unit examples include the new URNs. No structural change.

## 14. References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174): requirements language.
- [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339): date and time on the Internet.
- [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html): durations.
- [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html): currency codes.
- [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md)
- [RFC: Type-Specific Attributes for IRI Resource Objects](./rfc-type-specific-attributes.md)
- [RFC: HAL `_links` for the IRI Facility API](./rfc-hal-links.md)
- [DOE-IRI URN Registry](../registry/urns/README.md)
- [IRI Account Project Allocation Profile](../registry/profiles/account/project-allocation.md)
- [IRI Account User Allocation Profile](../registry/profiles/account/user-allocation.md)
- [IRI Account Capability Profile](../registry/profiles/account/capability.md)
- [IRI Inference Service Resource Definition Profile](../registry/profiles/resource-definition/service/inference.md)

## Appendix A. Examples

These examples are illustrative. Identifiers, hosts, prices, and quantities do not describe any deployed facility.

### A.1. Cloud Compute Allocation in US Dollars

A project holds a rolling 30-day spending limit for a cloud-hosted compute Capability. Usage is estimated from cost data computed at 17:00 UTC.

```json
{
  "id": "alloc-cloud-001",
  "entries": [
    {
      "allocation": 1000.0,
      "usage": 396.55,
      "unit": "urn:doe-iri:allocation:currency:usd",
      "attributes": {
        "period_start": "2026-10-01T00:00:00Z",
        "period_end": "2026-10-31T00:00:00Z",
        "renewal_interval": "P30D",
        "usage_as_of": "2026-10-13T17:00:00Z",
        "usage_basis": "estimated"
      }
    }
  ],
  "project_uri": "https://api.example.org/api/v2/account/projects/climate-simulation",
  "capability_uri": "https://api.example.org/api/v2/account/capabilities/cloud-compute"
}
```

### A.2. Inference Service and Token-Scoped Capability

An inference service serves one model and provides a Capability whose allocations are accounted in tokens and in dollars. Only the properties relevant to this RFC are shown.

Resource (abridged):

```json
{
  "id": "inference-service-01",
  "name": "Example Inference Service",
  "resource_type": "urn:doe-iri:resource:service:inference",
  "capability_uris": [
    "https://api.example.org/api/v2/account/capabilities/llama-70b-inference"
  ],
  "attributes": {
    "schema_version": "1.0.0",
    "inference_technology": "urn:doe-iri:service:inference-technology:vllm",
    "inference_apis": [
      "urn:doe-iri:service:inference-api:openai"
    ],
    "served_models": [
      {
        "id": "llama-3.1-70b-instruct",
        "name": "Llama 3.1 70B Instruct",
        "version": "3.1"
      }
    ]
  }
}
```

Capability:

```json
{
  "id": "llama-70b-inference",
  "name": "Llama 3.1 70B inference",
  "self_uri": "https://api.example.org/api/v2/account/capabilities/llama-70b-inference",
  "units": [
    "urn:doe-iri:allocation:inference:tokens",
    "urn:doe-iri:allocation:currency:usd"
  ],
  "attributes": {
    "served_model_ids": [
      "llama-3.1-70b-instruct"
    ]
  }
}
```

### A.3. Project Allocation with Token and Dollar Entries

The project may process up to 50 million tokens during the quarter and may spend up to 250 dollars per month on the same Capability. The two entries are independent limits (Section 5.4); the facility may refuse requests when either is exhausted.

```json
{
  "id": "alloc-inference-001",
  "entries": [
    {
      "allocation": 50000000,
      "usage": 12873311,
      "unit": "urn:doe-iri:allocation:inference:tokens",
      "attributes": {
        "period_start": "2026-10-01T00:00:00Z",
        "period_end": "2027-01-01T00:00:00Z",
        "usage_as_of": "2026-10-13T17:40:00Z",
        "usage_basis": "reconciled"
      }
    },
    {
      "allocation": 250.0,
      "usage": 81.204513,
      "unit": "urn:doe-iri:allocation:currency:usd",
      "attributes": {
        "renewal_interval": "P1M",
        "period_start": "2026-10-01T00:00:00Z",
        "period_end": "2026-11-01T00:00:00Z",
        "usage_as_of": "2026-10-13T17:40:00Z",
        "usage_basis": "estimated"
      }
    }
  ],
  "project_uri": "https://api.example.org/api/v2/account/projects/climate-simulation",
  "capability_uri": "https://api.example.org/api/v2/account/capabilities/llama-70b-inference"
}
```
