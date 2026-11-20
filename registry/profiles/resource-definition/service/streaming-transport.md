# IRI Streaming Transport Service Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/service/streaming-transport`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:service:streaming-transport`  
**Status:** Draft  
**Version:** 1.0.0

## Profile Applicability

This profile applies when `resource_type` is `urn:doe-iri:resource:service:streaming-transport`. It specializes the [IRI Status Resource Profile](../../status/resource.md), which a conforming representation MUST also satisfy. The authoritative URN record is [Resource Type URNs](../../../urns/resource-types.md).

This document defines attributes for the `urn:doe-iri:resource:service:streaming-transport` resource type. Reservations, allocation units, admission, accounting, and the reservation API are defined by [RFC: Streaming Data Transport Reservations](../../../../rfc/rfc-streaming-data-transport.md).

## 1. Profile Context

The following retained context identifies the profile's Resource Type; its registration is authoritative in the URN registry.

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:service:streaming-transport` |
| Short name | Streaming Transport Service |
| Description | A consumable service that forwards and load-balances high-rate datagram streams from senders to registered receivers through reservable load balancer instances. It does not identify an FPGA, host, load balancer instance, or reservation. |
| Parent URN | `urn:doe-iri:resource:service` |
| Status | `provisional` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | [RFC: Streaming Data Transport Reservations](../../../../rfc/rfc-streaming-data-transport.md); [Service Resource Types Design](../../../../engineering/decisions/0001-service-resource-boundaries.md). |
| Legacy value | `service` enumeration. The broad legacy value does not distinguish this refinement. |
| Examples | `urn:doe-iri:resource:service:streaming-transport` |
| Notes | This profile defines relatively stable characteristics and policy limits of a streaming transport service. |

## 2. Introduction

A streaming transport service lets senders stream data at high rate to a dynamic pool of receivers while the data is being produced. The facility exposes it as a set of load balancer instances that projects reserve, one instance per reservation, for a bounded interval. The ESnet/JLab FPGA Accelerated Transport (EJFAT) load balancer is the reference technology.

The service is distinct from the hardware that implements it. Relating the service to separately represented hardware would require extending the source types of `iri:hosted-on`, which this profile version does not do. Load balancer instances and reservations are not IRI Resources: instances are counted by `instance_count`, and reservations are API objects defined by the RFC.

Except for `schema_version`, attributes in this profile are optional. Omit an optional attribute when it is unknown or not relevant instead of guessing. The absence of an optional attribute means that the information has not been provided; it does not imply a particular value, capability, or lack of a limit.

## 3. Taxonomy

The taxonomy distinguishes the streaming transport service resource type from controlled values used to describe it. Only attributes represented by controlled DOE-IRI URNs appear in the controlled-vocabulary portion of the tree.

```text
urn:doe-iri
│
├── resource
│   └── service
│       └── streaming-transport
│
└── service
    └── streaming-technology
        └── ejfat
```

The complete controlled-vocabulary index is maintained in [Controlled Attribute URNs](../../../urns/attributes.md).

## 4. Streaming Transport Service Attributes

This Resource Definition Profile defines the attributes that MAY describe a resource of type `urn:doe-iri:resource:service:streaming-transport`.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition (e.g. `"1.0.0"`). | yes |
| `streaming_technology` | 1.0.0 | IRI URN string | Identifies the technology providing the streaming transport service. | no |
| `technology_version` | 1.0.0 | string | Identifies the deployed control-plane version when useful and known. | no |
| `instance_count` | 1.0.0 | integer | Configured number of load balancer instances. | no |
| `data_plane_capacity_gbps` | 1.0.0 | number | Configured aggregate data-plane capacity in gigabits per second. | no |
| `ip_families` | 1.0.0 | Array string | Reservation IP families the service supports: `ipv4`, `ipv6`, `dual_stack`. | no |
| `slot_strategies` | 1.0.0 | Array string | Technology-defined receiver slot assignment strategies a reservation may request. | no |
| `max_reservation_duration` | 1.0.0 | string, ISO 8601 duration | Longest interval between reservation creation or extension and the reservation's end. | no |
| `default_reservation_duration` | 1.0.0 | string, ISO 8601 duration | Duration applied when a reservation request does not give an end time. | no |
| `max_senders_per_reservation` | 1.0.0 | integer | Maximum size of a reservation's sender allow-list. | no |
| `max_receivers_per_reservation` | 1.0.0 | integer | Maximum number of concurrently registered receivers per reservation. | no |

### 4.1. Streaming Technology

The `streaming_technology` attribute identifies the technology providing the service. Its value MUST be a registered DOE-IRI URN from the `urn:doe-iri:service:streaming-technology` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:service:streaming-technology:ejfat` | EJFAT | The ESnet/JLab FPGA Accelerated Transport load balancer and its `udplbd` control plane. | `provisional` |

The value identifies a technology, not a resource subtype. Clients MUST NOT infer limits, supported options, the connection URI scheme, or operational availability solely from `streaming_technology`.

### 4.2. Capacity and Options

`instance_count` and `data_plane_capacity_gbps` are configured capacity. They are not claims about how many instances are currently free or how much bandwidth a reservation will receive.

`ip_families` values are fixed by this profile. Values MUST be unique within the array.

`slot_strategies` values are defined by the technology, because receiver slot assignment is technology-specific. For EJFAT the values are `dynamic`, `static`, and `explicit`, as defined by the `udplbd` control plane. Values MUST be unique within the array. A client MUST NOT assume a strategy is supported unless it is listed.

### 4.3. Reservation Limits

`max_reservation_duration`, `default_reservation_duration`, `max_senders_per_reservation`, and `max_receivers_per_reservation` are service policy that applies to every reservation. Per-project limits are allocations, expressed on the Project Allocation for the service's Capability, and are not profile attributes. When both durations are present, `default_reservation_duration` MUST NOT exceed `max_reservation_duration`.

### 4.4. Time-Varying and Security Information

This version of the profile does not define free instance counts, active reservations, current throughput, or control-plane health. Control-plane health maps to the existing `Resource.current_status`. Credentials, connection details, and reservation status are returned by the reservation API and MUST NOT appear in Resource attributes.

## 5. Streaming Transport Service JSON Schema

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

    StreamingTransportServiceAttributes:
      type: object
      description: >
        Attributes describing a streaming transport service resource with
        resource type urn:doe-iri:resource:service:streaming-transport.
      required:
        - schema_version
      properties:
        schema_version:
          type: string
          enum:
            - "1.0.0"
        streaming_technology:
          $ref: '#/components/schemas/IriUrn'
        technology_version:
          type: string
        instance_count:
          type: integer
          minimum: 1
        data_plane_capacity_gbps:
          type: number
          exclusiveMinimum: 0
        ip_families:
          type: array
          uniqueItems: true
          items:
            type: string
            enum:
              - ipv4
              - ipv6
              - dual_stack
        slot_strategies:
          type: array
          uniqueItems: true
          items:
            type: string
        max_reservation_duration:
          type: string
          format: duration
        default_reservation_duration:
          type: string
          format: duration
        max_senders_per_reservation:
          type: integer
          minimum: 1
        max_receivers_per_reservation:
          type: integer
          minimum: 1
```

## 6. Example Streaming Transport Service Attributes

The following EJFAT service has eight load balancer instances. This definition instance describes configured characteristics and policy, not current instance availability.

```json
{
  "schema_version": "1.0.0",
  "streaming_technology": "urn:doe-iri:service:streaming-technology:ejfat",
  "instance_count": 8,
  "data_plane_capacity_gbps": 400,
  "ip_families": ["ipv4", "ipv6", "dual_stack"],
  "slot_strategies": ["dynamic", "static", "explicit"],
  "max_reservation_duration": "P7D",
  "default_reservation_duration": "PT2H",
  "max_senders_per_reservation": 64
}
```

## 7. Applicable Links and Operations

A streaming transport Resource advertises its Capability through `capability_uris` and, when HAL is used, `iri:has-capability`. When the facility implements the reservation API, the Resource MAY advertise `iri:create-stream-reservation` and `iri:query-stream-reservations`, which are registered in the [relation index](../../../rels/README.md). They bind to operations that are not yet in the IRI v2 OpenAPI, and producers MUST NOT advertise them until the deployed OpenAPI carries the binding. Their presence grants no permission and does not assert that an instance is currently free.

---

*DOE Integrated Research Infrastructure — URN Registry: Streaming Transport Service*
