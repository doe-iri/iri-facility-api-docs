# RFC: Streaming Data Transport Reservations

## Abstract

Some facilities operate a high-rate streaming data-transport service: a hardware load balancer that receives UDP event streams from one or more senders and distributes them across a dynamic set of receivers. The ESnet/JLab FPGA Accelerated Transport (EJFAT) load balancer is the reference technology. Today users get access through a hand-distributed connection URI that carries a reservation-capable control-plane token, or through a prototype in the AmSC Transfer API. Neither ties a reservation to a project, enforces a quota, records usage, or presents a uniform interface across facilities.

This RFC defines how an IRI facility describes a streaming transport service as an IRI Resource, how it grants and accounts for streaming capacity through the existing IRI allocation model, and the facility API through which a user reserves a load balancer against a project allocation, obtains the connection details, manages the permitted senders, watches live status, and releases it.

It proposes one Resource Type, one controlled technology vocabulary, two allocation units (`instance-hours` and concurrent `instances`), one new IRI v2 API section (`/streaming`), and a small set of operation-affordance relations. It reuses the Project Allocation, Capability, and Allocation Entry representations unchanged.

## Status of This Memo

**Status:** Draft / Proposed

**Target:** IRI Facility API v2 (optional, conditional section), DOE-IRI URN Registry, Link Relation Registry

| Revision | Author | Date | Notes |
|---|---|---|---|
| 0.1 | Justas Balcas | Nov 12, 2026 | Initial draft. |

The Resource Type, technology value, allocation units, and operation relations in this document are recorded in the DOE-IRI registries in `provisional` status while this RFC is under review, together with the Resource Definition Profile; approval moves them to `active`. Paths, operation identifiers, and API property names remain proposals until the OpenAPI change in Section 15 lands. The registries remain the assignment authority.

This RFC depends on the Allocation Entry attributes (`period_start`, `period_end`, `renewal_interval`, `usage_as_of`, `usage_basis`) and the general interpretation rules for Allocation Entries proposed in the [Monetary and Inference-Token Allocation Units](./rfc-monetary-and-inference-allocation-units.md) RFC (Draft / Proposed). If that RFC is not approved, Section 6 of this RFC needs to define those attributes itself.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Terminology](#3-terminology)
4. [Model Overview](#4-model-overview)
5. [Resource Type and Definition Profile](#5-resource-type-and-definition-profile)
6. [Allocation Model](#6-allocation-model)
7. [Reservation API](#7-reservation-api)
8. [Credential Model](#8-credential-model)
9. [Operation Affordances](#9-operation-affordances)
10. [Conformance](#10-conformance)
11. [Migration and Backward Compatibility](#11-migration-and-backward-compatibility)
12. [Security and Privacy Considerations](#12-security-and-privacy-considerations)
13. [Alternatives Considered](#13-alternatives-considered)
14. [Open Questions](#14-open-questions)
15. [Required Specification and Registry Changes](#15-required-specification-and-registry-changes)
16. [References](#16-references)
- [Appendix A. Examples](#appendix-a-examples)
- [Appendix B. EJFAT Control-Plane Mapping (Informative)](#appendix-b-ejfat-control-plane-mapping-informative)

## 1. Introduction

A streaming transport service lets an instrument stream data at N x 100 Gbps to a pool of analysis receivers while the data is being produced, instead of writing files and transferring them afterwards. In EJFAT the service is co-designed hardware and software: an FPGA data plane that forwards and load-balances UDP packets, a control plane (`udplbd`) that manages reservations, sender allow-lists, receiver registration, and slot assignment, and a client library (E2SAR) that senders and receivers link against.

The scarce resource is the load balancer instance. One control plane manages a small, fixed number of instances (`udplbd` supports at most eight concurrently), and a reservation holds one instance exclusively from the moment it is reserved until it is freed or expires, whether or not data is flowing.

Current access paths have the following gaps:

- **Hand-distributed URIs.** An administrator gives the user an `ejfats://<token>@<host>:<port>/` URI whose token can reserve load balancers. Anyone holding it can reserve any number of instances for any duration, the reservation is not attributed to a project, and the facility has no usage record beyond control-plane logs.
- **Broker prototype.** The AmSC Transfer API prototype proxies reserve, get, and free calls to the control plane. Reservations are still not bound to a project, no quota is checked, no usage is recorded, and the capability is available only to users of that broker rather than to every user of the facility.
- **No uniform discovery or status.** A client cannot discover from the IRI API that a facility offers streaming transport, what its limits are, or what a project is entitled to, and cannot read live reservation status through an authenticated, project-scoped interface.

The load balancer is a facility resource, so the standard belongs in the facility API, where project membership, allocations, and accounting already live. Brokers such as AmSC then become clients of the facility API instead of holding control-plane credentials of their own.

## 2. Scope

In scope:

- a Resource Type and Resource Definition Profile for streaming transport services;
- the allocation units, Capability conventions, admission rules, and accounting rules for load balancer reservations;
- the reservation API: reserve, list, get, extend, update senders, read status, rotate the reservation credential, and release;
- the reservation credential handed to senders and receivers, and how it is scoped;
- operation-affordance relations for discovering these operations from a Resource.

Out of scope:

- the data plane, its packet formats, and the E2SAR library;
- receiver registration and receiver state reporting, which receivers perform directly against the technology's control plane using the reservation credential (Section 8);
- control-plane administration, FPGA configuration, and load balancer chaining;
- reservations scheduled to start in the future (advance reservations, Section 14);
- network path provisioning between senders, the load balancer, and receivers;
- pricing and rate cards, which follow the monetary allocation RFC when a facility charges in currency.

## 3. Terminology

- **Streaming transport service**: a consumable facility service that forwards and distributes high-rate datagram streams from senders to receivers. Represented as a Resource (Section 5).
- **Load balancer instance** (**instance**): one independently reservable unit of the service's data plane. In EJFAT, one FPGA load balancer ID.
- **Control plane**: the technology-specific service that manages instances, reservations, senders, and receivers. In EJFAT, `udplbd`.
- **Reservation**: the exclusive assignment of one instance to one project for a bounded interval. Reservations are API objects defined by this RFC; they are not IRI Resources.
- **Sender**: a host whose source address is permitted to send data and synchronization traffic into a reserved instance.
- **Receiver**: a process that registers with the control plane to receive part of a reservation's stream and reports its state.
- **Connection bundle**: the information senders and receivers need to use a reservation: data-plane and synchronization addresses and ports, control-plane endpoint, and the reservation credential.
- **Reservation credential**: a secret, scoped to one reservation, that senders and receivers present to the control plane.
- **Adapter**: the facility's implementation of this API. It holds the facility's control-plane service credential.
- **Allocation Entry**, **Project Allocation**, **User Allocation**, and **Capability** have the meanings given in the [account profiles](../registry/profiles/account/).

## 4. Model Overview

```text
 Resource (resource_type = urn:doe-iri:resource:service:streaming-transport)
   │  attributes: technology, limits, supported options
   │  capability_uris / iri:has-capability
   ▼
 Capability ("ejfat-lb")            units: instance-hours, instances
   ▲
   │ capability_uri
 ProjectAllocation (project P)      entries: instance-hours {allocation, usage}
   ▲                                         instances      {allocation, usage}
   │ project_allocation_uri  (charged to)
 Reservation ──────────────────────► control plane instance (lb id, fpga id)
   │  connection bundle (credential returned once)
   └─ status (receivers, senders, health)   ◄── receivers register directly
```

The Resource says what the facility offers. The Capability says what is allocatable and in which units. The Project Allocation says how much a project may consume and has consumed. A Reservation is one act of consumption, charged to exactly one Project Allocation. Receivers talk to the control plane directly; no data and no high-frequency receiver state passes through the IRI API.

## 5. Resource Type and Definition Profile

### 5.1. Resource Type

This RFC requests registration of:

| URN | Short name | Description | Parent | Status on registration |
|---|---|---|---|---|
| `urn:doe-iri:resource:service:streaming-transport` | Streaming Transport Service | Consumable service that forwards and load-balances high-rate datagram streams from senders to registered receivers, through reservable load balancer instances. | `urn:doe-iri:resource:service` | `provisional` |

The type classifies the consumable service, consistent with the existing DTN and inference service types. It does not identify an FPGA, a host, an instance, or a reservation. Relating the service to separately represented hardware would require extending the source types of `iri:hosted-on`; this RFC does not propose that.

### 5.2. Controlled Vocabulary

| URN | Short name | Description |
|---|---|---|
| `urn:doe-iri:service:streaming-technology` | Streaming technology | Namespace for streaming transport implementations. |
| `urn:doe-iri:service:streaming-technology:ejfat` | EJFAT | ESnet/JLab FPGA Accelerated Transport load balancer and its `udplbd` control plane. |

Clients MUST NOT infer limits, supported options, or the connection URI scheme solely from the technology value.

### 5.3. Profile Attributes

A Resource Definition Profile at `https://iri.science/profiles/resource-definition/service/streaming-transport` (proposed) defines the following `attributes`. Except for `schema_version`, all are optional, and absence means the value was not provided.

| Attribute | Type | Meaning |
|---|---|---|
| `schema_version` | string | Profile version, for example `"1.0.0"`. |
| `streaming_technology` | IRI URN | Technology providing the service, from `urn:doe-iri:service:streaming-technology`. |
| `technology_version` | string | Deployed control-plane version, when known. |
| `instance_count` | integer | Configured number of load balancer instances. Configured capacity, not current availability. |
| `data_plane_capacity_gbps` | number | Configured aggregate data-plane capacity. |
| `ip_families` | array of string | Supported values of the reservation `ip_family` property: `ipv4`, `ipv6`, `dual_stack`. |
| `slot_strategies` | array of string | Technology-defined receiver slot assignment strategies a reservation may request. For EJFAT: `dynamic`, `static`, `explicit`. |
| `max_reservation_duration` | string, ISO 8601 duration | Longest interval between reservation creation (or extension) and `until`. |
| `default_reservation_duration` | string, ISO 8601 duration | Duration applied when a reservation request omits `until`. |
| `max_senders_per_reservation` | integer | Maximum size of a reservation's sender allow-list. |
| `max_receivers_per_reservation` | integer | Maximum number of concurrently registered receivers per reservation. |

Live free-instance counts, active reservations, and control-plane health are time-varying and are not profile attributes. Control-plane health maps to the existing `Resource.current_status`.

## 6. Allocation Model

### 6.1. Allocation Units

This RFC requests two allocation-unit registrations. They are named for service instances in general rather than for EJFAT, because other reservable services (for example persistent service instances) have the same shape; the Capability determines what an instance is.

| URN | Short name | Description | Kind |
|---|---|---|---|
| `urn:doe-iri:allocation:service:instance-hours` | Instance-hours | Wall-clock hours during which one service instance is reserved for the project, regardless of use. | Cumulative |
| `urn:doe-iri:allocation:service:instances` | Concurrent instances | Number of service instances the project may hold at the same time. | Concurrent |

Interpretation:

1. **Instance-hours.** `allocation` is the number of instance-hours granted for the entry's accounting period. `usage` is the instance-hours charged so far in that period (Section 6.6). Values are decimal hours and MAY be fractional.
2. **Instances.** `allocation` is the maximum number of simultaneously active reservations charged to the Project Allocation. `usage` is the number currently active. This is a concurrent quantity in the same sense that `urn:doe-iri:allocation:storage:bytes` reports bytes currently held, not a cumulative count of reservations ever made. A producer SHOULD include `usage_as_of`.
3. `urn:doe-iri:allocation:service` is a grouping level and MUST NOT appear as a `unit`.
4. Both units are scoped by Capability. A consumer MUST NOT aggregate instance-hours across Capabilities, because an instance of one Capability is not equivalent to an instance of another.

### 6.2. Capability

A facility that offers streaming transport SHOULD expose one Capability per streaming transport Resource, listed in that Resource's `capability_uris`, whose `units` include `urn:doe-iri:allocation:service:instance-hours`. It MAY also include `urn:doe-iri:allocation:service:instances` and, when the facility charges in currency, `urn:doe-iri:allocation:currency:usd` as defined by the monetary allocation RFC.

The Capability MAY carry, in `Capability.attributes`:

| Attribute | Type | Meaning |
|---|---|---|
| `accounting_granularity` | string, ISO 8601 duration | Increment to which each reservation's charged duration is rounded up, for example `PT1M` or `PT1H`. Absent means the facility charges exact elapsed time. |

### 6.3. Quantities That Are Not Allocations

The following are limits or telemetry, not Allocation Entries, and MUST NOT be expressed as Allocation Entries:

- **Data rate.** Gbps is a rate, not a granted quantity. Per-reservation rate expectations, if a facility needs them, belong in the reservation request, and configured capacity in `data_plane_capacity_gbps`.
- **Per-reservation limits.** Maximum duration, senders, and receivers per reservation are service policy and belong in Resource attributes (Section 5.3).
- **Bytes or events streamed.** Counters reported through the control plane are partly self-reported by receivers and are not a reliable basis for enforcement. They appear in reservation status (Section 7.7). A future RFC MAY register a transferred-bytes unit if a facility meters the data plane itself.

### 6.4. Admission Control

On a reserve request for project P, Capability C, and requested end time `until`, the adapter determines the Project Allocation A of P for C (and, where the facility uses User Allocations for C, the caller's User Allocation U within A) and MUST reject the request unless all of the following hold:

1. The authenticated caller is authorized by the facility to consume allocations of P. Project selection comes from the request body (Section 7.2), never from a client-supplied header, and the adapter MUST verify membership itself.
2. A exists and is not expired.
3. If A (or U) has an `instances` entry: the number of active reservations charged to A (or U), plus one, does not exceed its `allocation`.
4. If A (or U) has an `instance-hours` entry: `usage + holds + requested <= allocation`, where `usage` is the charged amount in the current accounting period, `holds` is the sum over P's active reservations on C of the time remaining until each one's `until`, and `requested` is the duration from now to the requested `until`, rounded up to `accounting_granularity`.
5. `until` is in the future and within `max_reservation_duration` of now.
6. A load balancer instance is free.

A reservation therefore holds its full requested duration against the allocation while active, and the hold collapses to the actual charge when the reservation ends. A facility MAY cap `until` at the end of the current accounting period instead of rejecting a request that spans it, and MUST tell the client the effective `until` in the response.

The same checks, applied to the added duration only, govern extension (Section 7.1). Checks 3 and 4 are independent limits, consistent with the rule that each Allocation Entry is an independent limit.

### 6.5. Expiry

Every reservation MUST have a finite `until`. The adapter MUST NOT create a non-expiring control-plane reservation, even when the control plane supports one. The adapter MUST pass `until` to the control plane, where the technology supports it, so that the instance is released at `until` even if the adapter is unavailable.

### 6.6. Accounting and Reconciliation

1. A reservation's charge is `ceil((ended_at - created_at) / accounting_granularity) * accounting_granularity`, expressed in hours, where `ended_at` is the earliest of: release through this API, release or expiry observed at the control plane, and `until`.
2. The charge is added to the instance-hours `usage` of the Project Allocation it was charged to, and of the User Allocation when one applies. When a reservation spans accounting periods, each period is charged the time that falls within it.
3. Charges MUST NOT depend on data-plane counters or receiver-reported state.
4. The adapter SHOULD periodically reconcile its records with the control plane. A reservation that the control plane no longer holds MUST be closed with `ended_at` no later than the time the adapter observed its absence. A control-plane reservation with no adapter record is a facility operational issue; it MUST NOT be charged to a project without an attribution record.
5. If the reservation credential permits operations that change the reservation's end time at the control plane (Section 8), the adapter MUST detect the change during reconciliation and either restore the adapter's `until` or charge the actual interval.
6. A producer SHOULD set `usage_basis` to `estimated` while charges for active reservations are included and to `reconciled` once a period's reservations are all closed and reconciled.

## 7. Reservation API

### 7.1. Operations

The operations live in a new optional IRI v2 API section. `{resource_id}` identifies a streaming transport Resource and is bound to that Resource's adapter context. Clients SHOULD discover the entry points through the relations in Section 9 instead of constructing paths.

| Method and path | `operationId` | Purpose | Conformance |
|---|---|---|---|
| `POST /api/v2/streaming/{resource_id}/reservations` | `createStreamReservation` | Reserve an instance against a project allocation. Returns `201` with the Reservation, including the credential, and a `Location` header. | MUST |
| `GET /api/v2/streaming/{resource_id}/reservations` | `listStreamReservations` | List reservations visible to the caller. Filters: `project_id`, `state`, `modified_since`. | MUST |
| `GET /api/v2/streaming/{resource_id}/reservations/{reservation_id}` | `getStreamReservation` | Get one reservation. The credential is never included. | MUST |
| `PATCH /api/v2/streaming/{resource_id}/reservations/{reservation_id}` | `updateStreamReservation` | Extend `until` and/or replace `sender_addresses` (JSON Merge Patch). | SHOULD |
| `GET /api/v2/streaming/{resource_id}/reservations/{reservation_id}/status` | `getStreamReservationStatus` | Live status: senders, receivers, health. | MUST |
| `POST /api/v2/streaming/{resource_id}/reservations/{reservation_id}/credentials` | `rotateStreamReservationCredential` | Issue a new reservation credential and revoke the previous one. Returns the new connection bundle. | MAY |
| `DELETE /api/v2/streaming/{resource_id}/reservations/{reservation_id}` | `releaseStreamReservation` | Release the reservation. Idempotent; releasing an ended reservation returns `204`. | MUST |

Reservation and release complete synchronously. The control-plane calls involved take well under a second, so these operations do not use the IRI Task model.

### 7.2. Reserve Request

| Property | Type | Required | Meaning |
|---|---|---|---|
| `project_id` | string | Yes | Project to charge. The adapter verifies the caller's authorization for it (Section 6.4). |
| `capability_id` | string | No | Capability to charge. Required only when the Resource lists more than one Capability. |
| `name` | string | Yes | Human-readable label, 1 to 64 characters. Not unique. |
| `until` | string, RFC 3339 date-time | No | Requested end time. Default: now plus `default_reservation_duration`. |
| `sender_addresses` | array of string | No | Initial sender allow-list: IPv4 or IPv6 literals, no host names. |
| `ip_family` | string | No | `ipv4`, `ipv6`, or `dual_stack`; one of the Resource's `ip_families`. |
| `slot_strategy` | string | No | One of the Resource's `slot_strategies`. Default is technology-defined. |

The reserve operation SHOULD honour the `Idempotency-Key` request header with the same semantics as job submission, so that a client retrying after a timeout does not reserve, and get charged for, a second instance.

### 7.3. Reservation Representation

| Property | Type | Meaning |
|---|---|---|
| `id` | string | Opaque, stable reservation identifier. Not the control-plane identifier. |
| `name` | string | Label from the request. |
| `state` | string | `active`, `released`, `expired`, or `failed` (Section 7.5). |
| `resource_uri` | string URI | The streaming transport Resource. |
| `project_uri` | string URI | The Project charged. |
| `capability_uri` | string URI | The Capability charged. |
| `project_allocation_uri` | string URI | The Project Allocation charged. |
| `created_at` | string, date-time | Start of the charged interval. |
| `until` | string, date-time | Effective scheduled end. |
| `ended_at` | string, date-time or null | Actual end, or null while active. |
| `sender_addresses` | array of string | Effective sender allow-list as last observed at the control plane. |
| `ip_family` | string | Effective IP family. |
| `slot_strategy` | string | Effective strategy. |
| `charges` | array of `{unit, amount}` | Amount charged so far per allocation unit, for example instance-hours. |
| `connection` | ConnectionBundle | Section 7.4. |
| `attributes` | object | Technology-specific details, such as the EJFAT control-plane `lb_id` and `fpga_lb_id`, useful for correlating logs and metrics. |
| `self_uri` | string URI | Canonical URI of this reservation. |
| `_links` | HAL links | `self`, plus the relations in Section 9. |

Ended reservations SHOULD remain retrievable for at least the accounting period in which they ended, so that charges can be inspected.

### 7.4. Connection Bundle

| Property | Type | Meaning |
|---|---|---|
| `data_ipv4_address`, `data_ipv6_address` | string | Data-plane addresses senders send to. Present according to `ip_family`. |
| `data_min_port`, `data_max_port` | integer | Accepted destination UDP port range. |
| `sync_ipv4_address`, `sync_ipv6_address` | string | Synchronization addresses. |
| `sync_udp_port` | integer | Synchronization UDP port. |
| `control_plane_host`, `control_plane_port` | string, integer | Control-plane endpoint receivers register with. |
| `control_plane_tls` | boolean | Whether the control-plane endpoint requires TLS. |
| `token` | string, secret | Reservation credential (Section 8). Present only in the reserve and credential-rotation responses. |
| `token_expires_at` | string, date-time | When the credential stops working: no later than `until`. |
| `uri` | string, secret when it contains `token` | Technology connection URI. For EJFAT: `ejfat[s]://<token>@<host>:<port>/lb/<lb_id>?sync=...&data=...`, directly usable by E2SAR. Present with the token only in the reserve and rotation responses. |

`GET` and list responses MUST omit `token` and MUST NOT include a `uri` that embeds it. A client that loses the credential uses the rotation operation, or releases and reserves again.

### 7.5. Lifecycle

```text
   reserve ──► active ──► released   (DELETE, or freed at the control plane)
                 │
                 ├──────► expired    (until reached)
                 │
                 └──────► failed     (control plane lost the instance; charged to ended_at)
```

A reserve request that fails admission or control-plane allocation creates no reservation and incurs no charge. State transitions are monotonic: an ended reservation is never reactivated. Extending an expired reservation is an error; the client reserves again.

### 7.6. Errors

Errors use the IRI v2 error representation. Adapters MUST distinguish at least:

| Status | Condition |
|---|---|
| `400` | Malformed request, address literal invalid, unsupported `ip_family` or `slot_strategy`, `until` in the past or beyond `max_reservation_duration`, too many senders. |
| `403` | Caller not authorized for the project, or the project has no allocation for the Capability. |
| `404` | Reservation not found or not visible to the caller. Adapters MUST NOT reveal the existence of other projects' reservations. |
| `409` | Allocation limit reached: concurrent-instance limit, or insufficient instance-hours for the requested duration. The error identifies which limit. Also returned for extending or patching an ended reservation. |
| `503` | No free instance, or the control plane is unavailable. SHOULD include `Retry-After`. |

### 7.7. Status Representation

Status is time-varying and read on demand from the control plane; it is not cached in the Reservation representation.

| Property | Type | Meaning |
|---|---|---|
| `observed_at` | string, date-time | When the control plane produced this status. |
| `expires_at` | string, date-time | Control-plane expiry. Differs from the reservation's `until` only during reconciliation. |
| `sender_addresses` | array of string | Current allow-list at the control plane. |
| `receivers` | array of ReceiverStatus | Registered receivers. |
| `health_issues` | array of `{severity, type, message, detected_at}` | Reservation-level issues reported by the control plane. `severity` is `warning`, `error`, or `critical`. |
| `attributes` | object | Technology-specific status, such as the EJFAT current epoch and slot resolution. |

ReceiverStatus: `session_id`, `name`, `ip_address`, `udp_port`, `port_range`, `ready` (boolean), `fill_percent`, `control_signal`, `slots_assigned`, `last_updated`, `health_issues`, and a `counters` object (`events_received`, `events_reassembled`, `reassembly_errors`, `bytes_received`, `packets_received`). Counters are reported by the receivers themselves and are informational only (Section 6.3).

## 8. Credential Model

Two credentials exist, and they MUST be kept apart:

1. **Adapter credential.** The facility's control-plane service credential, able to reserve, extend, and free instances and to mint scoped credentials. It MUST be held only by the adapter and MUST NOT be returned to clients, forwarded to brokers, or derived from a caller's own token. The adapter MUST NOT accept a client-supplied control-plane URL.
2. **Reservation credential.** A credential the adapter mints per reservation and returns in the connection bundle. It MUST be scoped to that one reservation, MUST stop working no later than the reservation's end, and MUST be revoked when the reservation is released.

The reservation credential SHOULD carry the narrowest permission that lets receivers register, report state, and deregister, and lets senders add their own address to the allow-list when the client tooling requires it. It MUST NOT permit reserving other instances. It SHOULD NOT permit freeing, extending, or resetting the reservation; if the technology cannot separate those permissions, Section 6.6 items 4 and 5 make the out-of-band changes observable and correctly charged.

For EJFAT, the adapter mints a child token of the adapter credential, scoped to the reservation's load balancer, and SHOULD NOT hand out the instance token returned by the control plane's reserve call. Current client tooling releases reservations with that token, so it can at least free the reservation, and it may also be able to extend it. Which `udplbd` permission level is the narrowest one that covers E2SAR receivers and sender self-registration is an open question (Section 14).

Rotation issues a new reservation credential and revokes the previous one. Because control-plane revocation can cascade to credentials derived from the old one, rotation MAY disconnect registered receivers; the adapter SHOULD document whether it does.

## 9. Operation Affordances

Following the [operation affordances RFC](./rfc-resource-operation-affordances.md), this RFC proposes the following relations. Names are proposals subject to the relation registry's review.

| Relation | Source | Target operation |
|---|---|---|
| `iri:create-stream-reservation` | Resource with `resource_type` `urn:doe-iri:resource:service:streaming-transport` | `POST .../reservations` |
| `iri:query-stream-reservations` | Same | `GET .../reservations` |
| `iri:get-stream-reservation-status` | Reservation | `GET .../reservations/{reservation_id}/status` |
| `iri:rotate-stream-credential` | Reservation | `POST .../reservations/{reservation_id}/credentials` |

The relation definitions are registered as `provisional` in the [relation index](../registry/rels/README.md). Until the operations exist in the IRI v2 OpenAPI with matching `x-iri-relation` bindings, producers MUST NOT advertise them. Get, update, and release are the `GET`, `PATCH`, and `DELETE` methods on the Reservation's `self` link and need no relation. A Reservation representation also links to the Project Allocation it is charged to; whether that reuses an existing relation or needs a new one is decided in the relation registry change (Section 15).

Each relation is a configured affordance. Its presence grants no permission and does not assert that an instance is currently free.

## 10. Conformance

The streaming section is optional. A facility that does not operate a streaming transport service does not implement it. A facility that advertises `iri:create-stream-reservation` on any Resource:

- MUST implement the operations marked MUST in Section 7.1;
- MUST expose a Capability for the Resource with the instance-hours unit and MUST account for reservations as in Section 6.6;
- MUST apply admission control (Section 6.4) and finite expiry (Section 6.5);
- MUST follow the credential separation in Section 8;
- SHOULD implement `PATCH` and `Idempotency-Key`;
- MAY implement credential rotation.

## 11. Migration and Backward Compatibility

- **Existing IRI clients** are unaffected. The section, units, Resource Type, and relations are additive. Consumers that do not recognise the new units display them by URN, as the URN specification already requires.
- **Hand-distributed reservation-capable tokens.** A facility adopting this RFC SHOULD stop issuing them to users and SHOULD revoke existing ones after a published transition window, because any user-held credential that can reserve bypasses admission control and accounting.
- **Brokers.** A broker such as the AmSC Transfer API SHOULD call this API on behalf of the user and project, presenting a credential that the facility maps to that user, instead of calling the control plane. The broker then inherits project binding, quota, and accounting without implementing them.
- **IRI v1** is not extended.

## 12. Security and Privacy Considerations

- **Credential exposure.** The reservation credential and any `uri` embedding it are secrets. Adapters MUST NOT log them, MUST return them only in the reserve and rotation responses, and SHOULD serve those responses with `Cache-Control: no-store`.
- **Traffic redirection.** A receiver chooses the address it registers, and the load balancer then sends up to line rate to that address. A holder of a reservation credential could direct a high-rate stream at a third-party host. Facilities SHOULD restrict registrable receiver addresses to approved networks, by control-plane policy or network filtering, and SHOULD reject loopback, link-local, multicast, and unspecified addresses.
- **Sender allow-list.** Adapters MUST accept only IP literals and SHOULD reject the same special-purpose ranges. A facility MAY restrict senders to approved prefixes.
- **Project binding.** Project selection comes from the authenticated request body and is verified against facility membership. Client-supplied project headers MUST NOT select or override the charged project.
- **Control-plane exposure.** Control-plane reservation and administration endpoints SHOULD NOT be reachable with any user-held credential that can reserve. Unauthenticated control-plane metrics expose per-instance activity and SHOULD NOT be published outside the facility.
- **Visibility.** Reservation details, sender and receiver addresses, and status reveal network topology and project activity. They MUST be visible only to callers authorized for the reservation's project, and facility staff.
- **Denial of service.** Instances are few. Concurrent-instance allocations, `max_reservation_duration`, and finite expiry together bound how long one project can hold capacity. Facilities SHOULD rate-limit reserve requests per caller.
- **Data plane.** No data-plane traffic passes through the IRI API or adapter.

## 13. Alternatives Considered

| Alternative | Assessment |
|---|---|
| Keep the broker (AmSC) prototype as the standard | Limits a facility capability to one broker's users, and the broker cannot enforce facility allocations or produce facility accounting. Useful as a prototype and as a future client of this API. |
| Continue hand-distributed URIs | No authentication per user, no project attribution, no quota, no accounting, no uniform discovery. |
| Model streaming as a Job or Task | A Job is batch work; a reservation is a held capacity with its own lifecycle, credential, and live status. Reusing the Job model would overload its states and accounting. |
| Model each reservation as an IRI Resource | Resources describe what a facility offers and are relatively stable. Reservations are short-lived, per-project consumption records. Making them Resources would flood the Resource catalog. |
| EJFAT-specific units such as `urn:doe-iri:allocation:streaming:lb-hours` | Simpler to read, but persistent services and other reservable services have the same instance-hour shape. Capability scoping already says what an instance is. |
| Account by bytes streamed | Not what is scarce (instances are), not enforceable during a stream, and partly self-reported by receivers. |
| Account by reserved bandwidth (Gbps-hours) | Current EJFAT reservations do not reserve bandwidth; an instance is either held or not. Can be added if a technology supports rate reservations. |
| Return the control plane's own reservation token | Simplest, but in EJFAT that token can free and possibly extend the reservation, which lets users bypass admission and accounting. |
| Proxy receiver registration and state through the IRI API | Receivers report state many times per second; routing that through the facility API adds latency and load for no accounting benefit. |

## 14. Open Questions

1. **EJFAT permission mapping.** Which `udplbd` permission level and resource type (load balancer or reservation) is the narrowest that covers E2SAR receiver `Register`, `SendState`, and `Deregister`, and sender self-registration through `AddSenders`? Does that level also permit `ExtendReservation` or `FreeLoadBalancer`? To be confirmed with the `udplbd` maintainers.
2. **Receiver address restriction.** Does `udplbd` support an allow-list of registrable receiver prefixes, or must facilities rely on network filtering?
3. **Advance reservations.** Should a later version allow reserving an instance for a future window, for scheduled experiment runs? That needs a calendar and changes admission control.
4. **Rate reservations.** If a future technology reserves bandwidth per instance, should a rate parameter in the request feed admission control?
5. **Release timing evidence.** Can the control plane report the time it freed or expired an instance, so that reconciliation charges the exact end instead of the observation time?
6. **Charged-to relation.** Reuse an existing relation for Reservation to Project Allocation, or register a new one?

## 15. Required Specification and Registry Changes

Per repository practice, each item is a separate bounded change, in this order. This revision includes items 1 to 4.

1. **This RFC** under review; index entry in `rfc/README.md`.
2. **URN registry.** Register `urn:doe-iri:resource:service:streaming-transport` in [Resource Type URNs](../registry/urns/resource-types.md), `urn:doe-iri:service:streaming-technology:ejfat` in [Controlled Attribute URNs](../registry/urns/attributes.md), and `urn:doe-iri:allocation:service:instance-hours` and `urn:doe-iri:allocation:service:instances` in the [Allocation Unit Registry](../registry/urns/README.md#5-allocation-unit-registry), all `provisional`.
3. **Resource Definition Profile.** Add `registry/profiles/resource-definition/service/streaming-transport.md` with the attributes in Section 5.3 and its JSON Schema.
4. **Relation registry.** Register the relations in Section 9 as `provisional`, bound to planned operations, and decide the charged-to relation.
5. **OpenAPI.** Add the `streaming` section: the seven operations in Section 7.1 with `x-iri-relation` bindings, and the `StreamReservationRequest`, `StreamReservation`, `StreamReservationPatch`, `ConnectionBundle`, `StreamReservationStatus`, and `ReceiverStatus` schemas.
6. **Account profiles.** On approval of this RFC, reference Section 6 from the Capability and Project Allocation profiles, following the same approach as the monetary allocation RFC.
7. **Reference implementation.** `iri-facility-api-python`: streaming router, a `StreamingAdapter` interface, and the reservation and allocation-unit models. Demo adapter: an in-memory control plane with a fixed instance count, for conformance testing. ESnet adapter: `udplbd` REST client using a facility service token.

## 16. References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174): requirements language.
- [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339): date and time; [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html): durations.
- [RFC 7396](https://www.rfc-editor.org/rfc/rfc7396): JSON Merge Patch.
- [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md)
- [RFC: Type-Specific Attributes for IRI Resource Objects](./rfc-type-specific-attributes.md)
- [RFC: HAL `_links` for the IRI Facility API](./rfc-hal-links.md)
- [RFC: Migrating Resource.supported_endpoints to HAL Operation Affordances](./rfc-resource-operation-affordances.md)
- [RFC: Monetary and Inference-Token Allocation Units](./rfc-monetary-and-inference-allocation-units.md)
- [Service Resource Boundaries decision](../engineering/decisions/0001-service-resource-boundaries.md) (non-normative).
- [IRI Account Capability Profile](../registry/profiles/account/capability.md), [Project Allocation Profile](../registry/profiles/account/project-allocation.md), [User Allocation Profile](../registry/profiles/account/user-allocation.md)
- EJFAT control plane `udplbd2`: <https://github.com/esnet/udplbd2>
- E2SAR data-plane library: <https://github.com/JeffersonLab/E2SAR>

## Appendix A. Examples

These examples are illustrative. Identifiers, addresses, quantities, and tokens do not describe any deployed facility.

### A.1. Streaming Transport Resource

```json
{
  "id": "ejfat-lb",
  "name": "EJFAT Load Balancer",
  "resource_type": "urn:doe-iri:resource:service:streaming-transport",
  "group": "network",
  "current_status": "up",
  "last_modified": "2026-11-12T15:00:00Z",
  "self_uri": "https://api.example.org/api/v2/status/resources/ejfat-lb",
  "site_uri": "https://api.example.org/api/v2/facility/sites/site-1",
  "capability_uris": ["https://api.example.org/api/v2/account/capabilities/ejfat-lb"],
  "attributes": {
    "schema_version": "1.0.0",
    "streaming_technology": "urn:doe-iri:service:streaming-technology:ejfat",
    "instance_count": 8,
    "data_plane_capacity_gbps": 400,
    "ip_families": ["ipv4", "ipv6", "dual_stack"],
    "slot_strategies": ["dynamic", "static", "explicit"],
    "max_reservation_duration": "P7D",
    "default_reservation_duration": "PT2H",
    "max_senders_per_reservation": 64
  },
  "_links": {
    "self": {"href": "https://api.example.org/api/v2/status/resources/ejfat-lb"},
    "service-desc": {"href": "https://api.example.org/openapi.json", "type": "application/vnd.oai.openapi+json;version=3.1"},
    "iri:create-stream-reservation": {"href": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations"},
    "iri:query-stream-reservations": {"href": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations"}
  }
}
```

### A.2. Capability and Project Allocation

```json
{
  "id": "ejfat-lb",
  "name": "EJFAT load balancer instances",
  "units": [
    "urn:doe-iri:allocation:service:instance-hours",
    "urn:doe-iri:allocation:service:instances"
  ],
  "attributes": {"accounting_granularity": "PT1M"},
  "self_uri": "https://api.example.org/api/v2/account/capabilities/ejfat-lb"
}
```

```json
{
  "id": "alloc-ejfat-p1",
  "project_uri": "https://api.example.org/api/v2/account/projects/p1",
  "capability_uri": "https://api.example.org/api/v2/account/capabilities/ejfat-lb",
  "entries": [
    {
      "allocation": 500,
      "usage": 132.25,
      "unit": "urn:doe-iri:allocation:service:instance-hours",
      "attributes": {
        "period_start": "2026-10-01T00:00:00Z",
        "period_end": "2027-10-01T00:00:00Z",
        "usage_as_of": "2026-11-12T15:00:00Z",
        "usage_basis": "estimated"
      }
    },
    {
      "allocation": 2,
      "usage": 1,
      "unit": "urn:doe-iri:allocation:service:instances",
      "attributes": {"usage_as_of": "2026-11-12T15:00:00Z"}
    }
  ]
}
```

### A.3. Reserve

```http
POST /api/v2/streaming/ejfat-lb/reservations
Authorization: Bearer <user token>
Idempotency-Key: 4f1c2a9e-7d1b-4c51-9a0f-1b2c3d4e5f60
Content-Type: application/json

{
  "project_id": "p1",
  "name": "detector-run-42",
  "until": "2026-11-12T19:00:00Z",
  "sender_addresses": ["198.51.100.10", "2001:db8::10"],
  "ip_family": "dual_stack"
}
```

```http
HTTP/1.1 201 Created
Location: https://api.example.org/api/v2/streaming/ejfat-lb/reservations/r-7d2f
Cache-Control: no-store
Content-Type: application/json

{
  "id": "r-7d2f",
  "name": "detector-run-42",
  "state": "active",
  "resource_uri": "https://api.example.org/api/v2/status/resources/ejfat-lb",
  "project_uri": "https://api.example.org/api/v2/account/projects/p1",
  "capability_uri": "https://api.example.org/api/v2/account/capabilities/ejfat-lb",
  "project_allocation_uri": "https://api.example.org/api/v2/account/projects/p1/project_allocations/alloc-ejfat-p1",
  "created_at": "2026-11-12T15:00:00Z",
  "until": "2026-11-12T19:00:00Z",
  "ended_at": null,
  "sender_addresses": ["198.51.100.10", "2001:db8::10"],
  "ip_family": "dual_stack",
  "slot_strategy": "dynamic",
  "charges": [{"unit": "urn:doe-iri:allocation:service:instance-hours", "amount": 0}],
  "connection": {
    "data_ipv4_address": "192.0.2.20",
    "data_ipv6_address": "2001:db8::20",
    "data_min_port": 16384,
    "data_max_port": 32767,
    "sync_ipv4_address": "192.0.2.21",
    "sync_ipv6_address": "2001:db8::21",
    "sync_udp_port": 19523,
    "control_plane_host": "lb.example.org",
    "control_plane_port": 18008,
    "control_plane_tls": true,
    "token": "<reservation credential>",
    "token_expires_at": "2026-11-12T19:00:00Z",
    "uri": "ejfats://<reservation credential>@lb.example.org:18008/lb/17?sync=192.0.2.21:19523&sync=[2001:db8::21]:19523&data=192.0.2.20:16384-32767&data=[2001:db8::20]:16384-32767"
  },
  "attributes": {"lb_id": "17", "fpga_lb_id": 3},
  "self_uri": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations/r-7d2f",
  "_links": {
    "self": {"href": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations/r-7d2f"},
    "iri:get-stream-reservation-status": {"href": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations/r-7d2f/status"},
    "iri:rotate-stream-credential": {"href": "https://api.example.org/api/v2/streaming/ejfat-lb/reservations/r-7d2f/credentials"}
  }
}
```

### A.4. Extend and Release

```http
PATCH /api/v2/streaming/ejfat-lb/reservations/r-7d2f
Content-Type: application/merge-patch+json

{"until": "2026-11-12T21:00:00Z"}
```

Admission checks the added two hours. If the project lacks them, the response is `409` naming the instance-hours limit and the reservation keeps its previous `until`.

```http
DELETE /api/v2/streaming/ejfat-lb/reservations/r-7d2f

HTTP/1.1 204 No Content
```

Released at 17:31:20 with `accounting_granularity` `PT1M`, the reservation is charged 2.533333 instance-hours (152 minutes, rounded up from 2 h 31 min 20 s).

### A.5. Status

```json
{
  "observed_at": "2026-11-12T16:10:04Z",
  "expires_at": "2026-11-12T19:00:00Z",
  "sender_addresses": ["198.51.100.10", "2001:db8::10"],
  "receivers": [
    {
      "session_id": "41",
      "name": "rx-node-a",
      "ip_address": "203.0.113.5",
      "udp_port": 10000,
      "port_range": 4,
      "ready": true,
      "fill_percent": 0.12,
      "control_signal": 0.0,
      "slots_assigned": 256,
      "last_updated": "2026-11-12T16:10:03Z",
      "health_issues": [],
      "counters": {"events_received": 1204411, "events_reassembled": 1204398, "reassembly_errors": 13, "bytes_received": 98320441344, "packets_received": 11003221}
    }
  ],
  "health_issues": [],
  "attributes": {"current_epoch": 9182, "slot_resolution": 512}
}
```

## Appendix B. EJFAT Control-Plane Mapping (Informative)

How an adapter can implement this API against the `udplbd` REST interface (`/api/v1`). Route and field names are taken from the `udplbd2` source at the time of writing and may change.

| This API | `udplbd` call | Notes |
|---|---|---|
| Reserve | `POST /lb` (`name`, `until`, `sender_addresses`, `ip_family`, `strategy`), then `POST /tokens` | Adapter credential. The reply `token` is kept by the adapter; a scoped child token is minted for the connection bundle. |
| Get / list | Adapter records, refreshed with `GET /lb/{id}` | |
| Extend | `POST /lb/{id}/extend` (`until`) | After admission check. |
| Update senders | `POST /lb/{id}/senders` and `DELETE /lb/{id}/senders` (`sender_addresses`) | Adapter computes the difference from the requested set. |
| Status | `GET /lb/{id}/status` | Maps `workers[]` to `receivers[]`, `healthIssues`, `expiresAt`, `currentEpoch`, `slotResolution`. |
| Rotate credential | `POST /tokens`, then `DELETE /tokens/{old}` | |
| Release | `DELETE /tokens/{id}`, then `DELETE /lb/{id}` | |
| Reconciliation | `GET /overview` | Detects instances freed or extended out of band, and orphans. |
| Resource `current_status` | `GET /version`, control-plane reachability | `technology_version` from `GET /version`. |

Receivers continue to use E2SAR against the control plane directly (`Register`, `SendState`, `Deregister`) with the reservation credential from the connection bundle. `ResetLoadBalancer`, load balancer chaining, and timeseries endpoints are not exposed by this API.
