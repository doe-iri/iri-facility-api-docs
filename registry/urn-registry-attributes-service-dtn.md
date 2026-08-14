# Attribute Profile: `urn:doe-iri:resource:service:dtn`

This document defines attributes for the `urn:doe-iri:resource:service:dtn` resource type.

## 1. Registry Metadata

As described in [A URN Namespace for the DoE IRI Project](../rfc/rfc-iri-urn-structure-and-registry.md), the following metadata is recorded:

| Field | Description |
|---|---|
| URN | `urn:doe-iri:resource:service:dtn` |
| Short name | DTN Service |
| Description | A consumable data-transfer service. It does not identify an individual host or compute node. |
| Parent URN | `urn:doe-iri:resource:service` |
| Status | `provisional` |
| Introduced | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference | [Service Resource Types Design](../docs/superpowers/specs/2026-08-13-service-resource-types-design.md). |
| Legacy value | `service` enumeration. The broad legacy value does not distinguish this refinement. |
| Examples | `urn:doe-iri:resource:service:dtn` |
| Notes | This profile defines relatively stable characteristics of a consumable DTN service. |

## 2. Introduction

A DTN service is a consumable service through which a facility makes data-transfer operations available. It is distinct from the compute system or compute node that hosts it; hosting topology is represented separately using `iri:hostedOn`. A DTN service may also be configured to access filesystem mounts for transfer operations through `iri:accessesMount`.

This profile records relatively stable service configuration. Endpoint URLs are attributes of the DTN service rather than independent IRI resources because they normally do not require independent identity, lifecycle, relationships, or state. If a future use case requires those properties, an endpoint may be defined as a separate resource type in a future profile version.

The profile distinguishes a DTN technology or implementation from the transfer protocols it supports. A technology identifies the software or service implementation providing the DTN; a protocol identifies an interface through which transfers can be requested or performed. A DTN may advertise multiple transfer protocols regardless of its technology.

Except for `schema_version`, attributes in this profile are optional. Omit an optional attribute when it is unknown or not relevant instead of guessing a technology, version, protocol, or endpoint. The absence of an optional attribute means that the information has not been provided; it does not imply a particular value, capability, or lack of support.

## 3. Taxonomy

The taxonomy distinguishes the DTN service resource type from controlled values used to describe it. Only attributes represented by controlled DOE-IRI URNs appear in the controlled-vocabulary portion of the tree.

```text
urn:doe-iri
│
├── resource
│   └── service
│       └── dtn
│
└── service
    ├── dtn-technology
    │   ├── globus
    │   └── xrootd
    │
    └── transfer-protocol
        ├── https
        ├── gridftp
        ├── xrootd
        └── sftp
```

The complete service resource and controlled-vocabulary index is maintained in the [Service Taxonomy and URN Index](urn-registry-type-service-taxonomy.md).

## 4. DTN Service Attribute Profile

The DTN Service Attribute Profile defines the attributes that MAY describe a resource of type `urn:doe-iri:resource:service:dtn`.

| Attribute | Version | Type | Description | Mandatory |
|---|---|---|---|---|
| `schema_version` | 1.0.0 | string | Version of the profile definition (e.g. `"1.0.0"`). | yes |
| `dtn_technology` | 1.0.0 | IRI URN string | Identifies the technology or implementation providing the DTN service. | no |
| `technology_version` | 1.0.0 | string | Identifies the deployed technology version when useful and known. | no |
| `transfer_protocols` | 1.0.0 | Array IRI URN string | Identifies transfer protocols supported by the DTN service. | no |
| `transfer_endpoints` | 1.0.0 | Array TransferEndpoint | Identifies configured endpoints through which transfers can be requested or performed. | no |

### 4.1. DTN Technology

The `dtn_technology` attribute identifies the technology or implementation providing the DTN service. Its value MUST be a registered DOE-IRI URN from the `urn:doe-iri:service:dtn-technology` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:service:dtn-technology:globus` | Globus | A DTN service technology or implementation provided by Globus. | `provisional` |
| `urn:doe-iri:service:dtn-technology:xrootd` | XRootD | A DTN service technology or implementation provided by XRootD. | `provisional` |

Globus and XRootD in this vocabulary identify technologies, not resource subtypes. Clients MUST NOT infer supported transfer protocols, endpoint reachability, authorization, capacity, or operational state solely from `dtn_technology`.

### 4.2. Transfer Protocols

The `transfer_protocols` attribute identifies transfer protocols supported by the DTN service. It is an array because a DTN may support more than one protocol. Each value MUST be a registered DOE-IRI URN from the `urn:doe-iri:service:transfer-protocol` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:service:transfer-protocol:https` | HTTPS | The Hypertext Transfer Protocol Secure protocol family for transfer endpoints. | `provisional` |
| `urn:doe-iri:service:transfer-protocol:gridftp` | GridFTP | The GridFTP protocol for high-performance, managed data transfer. | `provisional` |
| `urn:doe-iri:service:transfer-protocol:xrootd` | XRootD | The XRootD protocol for high-performance data access and transfer. | `provisional` |
| `urn:doe-iri:service:transfer-protocol:sftp` | SFTP | The SSH File Transfer Protocol. | `provisional` |

The XRootD technology value and the XRootD protocol value answer different questions: the former identifies an implementation, while the latter identifies a transfer interface. A DTN may advertise several protocols regardless of its implementation technology. Facilities SHOULD explicitly advertise supported protocols rather than require clients to infer them from `dtn_technology`.

### 4.3. Transfer Endpoints

The `transfer_endpoints` attribute identifies configured network endpoints through which transfers can be requested or performed. A DTN may expose multiple endpoints, including endpoints for different protocols.

Each `TransferEndpoint` contains:

| Property | Type | Description | Mandatory |
|---|---|---|---|
| `url` | string URI | Configured network endpoint. | yes |
| `protocol` | IRI URN string | Registered transfer protocol exposed by the endpoint. | yes |
| `name` | string | Human-readable endpoint label. | no |

The `protocol` value MUST come from `urn:doe-iri:service:transfer-protocol:*`. An endpoint is configured access information, not a claim that it is currently reachable, available to a particular consumer, or authorized for a particular transfer.

### 4.4. State Exclusions

This profile excludes endpoint health, current endpoint reachability, active transfers, queues, throughput, credentials, and current availability from the stable resource definition. Those dynamic operational facts SHOULD be represented through the applicable resource-state, transfer-state, and security or access-control mechanisms.

## 5. DTN Service JSON Schema

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
      example: urn:doe-iri:service:dtn-technology:globus

    TransferEndpoint:
      type: object
      required:
        - url
        - protocol
      properties:

        url:
          type: string
          format: uri
          description: Configured network endpoint for transfer operations.

        protocol:
          $ref: '#/components/schemas/IriUrn'
          description: Registered transfer protocol exposed by this endpoint.

        name:
          type: string
          description: Human-readable endpoint label.

    DtnServiceAttributes:
      type: object
      description: >
        Attributes describing a DTN service resource with resource type
        urn:doe-iri:resource:service:dtn.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          description: Version of the DTN service attribute profile definition.
          enum:
            - "1.0.0"
          example: "1.0.0"

        dtn_technology:
          $ref: '#/components/schemas/IriUrn'
          description: Identifies the technology or implementation providing the DTN service.
          example: urn:doe-iri:service:dtn-technology:globus

        technology_version:
          type: string
          description: Identifies the deployed technology version when useful and known.

        transfer_protocols:
          type: array
          description: Identifies transfer protocols supported by the DTN service.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:service:transfer-protocol:https
            - urn:doe-iri:service:transfer-protocol:gridftp

        transfer_endpoints:
          type: array
          description: >
            Identifies configured endpoints through which transfers can be
            requested or performed.
          items:
            $ref: '#/components/schemas/TransferEndpoint'
```

## 6. Example DTN Service JSON Instances

The following Globus DTN service advertises HTTPS and GridFTP transfer protocols and provides one configured endpoint for each protocol.

```json
{
  "schema_version": "1.0.0",
  "dtn_technology": "urn:doe-iri:service:dtn-technology:globus",
  "technology_version": "5.4",
  "transfer_protocols": [
    "urn:doe-iri:service:transfer-protocol:https",
    "urn:doe-iri:service:transfer-protocol:gridftp"
  ],
  "transfer_endpoints": [
    {
      "url": "https://globus.example.gov",
      "protocol": "urn:doe-iri:service:transfer-protocol:https",
      "name": "Globus HTTPS endpoint"
    },
    {
      "url": "gsiftp://globus.example.gov",
      "protocol": "urn:doe-iri:service:transfer-protocol:gridftp",
      "name": "Globus GridFTP endpoint"
    }
  ]
}
```

The following illustrative complete resource representation applies the
`DtnServiceAttributes` profile inside `attributes` and adds HAL relationships
for its hosting infrastructure and configured mount access. It is a
resource-level example, not an instance of `DtnServiceAttributes` alone.

```json
{
  "id": "globus-dtn",
  "name": "Globus DTN Service",
  "description": "Facility data-transfer service with HTTPS and GridFTP access",
  "last_modified": "2026-08-13T12:00:00Z",
  "resource_type": "urn:doe-iri:resource:service:dtn",
  "self_uri": "https://api.example.gov/api/v2/status/resources/globus-dtn",
  "site_uri": "https://api.example.gov/api/v2/sites/example-site",
  "capability_uris": [],
  "attributes": {
    "schema_version": "1.0.0",
    "dtn_technology": "urn:doe-iri:service:dtn-technology:globus",
    "technology_version": "5.4",
    "transfer_protocols": [
      "urn:doe-iri:service:transfer-protocol:https",
      "urn:doe-iri:service:transfer-protocol:gridftp"
    ],
    "transfer_endpoints": [
      {
        "url": "https://globus.example.gov",
        "protocol": "urn:doe-iri:service:transfer-protocol:https",
        "name": "Globus HTTPS endpoint"
      },
      {
        "url": "gsiftp://globus.example.gov",
        "protocol": "urn:doe-iri:service:transfer-protocol:gridftp",
        "name": "Globus GridFTP endpoint"
      }
    ]
  },
  "_links": {
    "iri:locatedAt": {
      "href": "https://api.example.gov/api/v2/sites/example-site"
    },
    "iri:hostedOn": {
      "href": "/api/v2/status/resources/perlmutter"
    },
    "iri:accessesMount": [
      {
        "href": "/api/v2/status/resources/perlmutter-scratch-mount"
      },
      {
        "href": "/api/v2/status/resources/analysis-home-mount"
      }
    ]
  }
}
```

The following XRootD DTN service uses the XRootD technology and exposes XRootD and HTTPS endpoints.

```json
{
  "schema_version": "1.0.0",
  "dtn_technology": "urn:doe-iri:service:dtn-technology:xrootd",
  "technology_version": "5.7",
  "transfer_protocols": [
    "urn:doe-iri:service:transfer-protocol:xrootd",
    "urn:doe-iri:service:transfer-protocol:https"
  ],
  "transfer_endpoints": [
    {
      "url": "root://xrootd.example.gov",
      "protocol": "urn:doe-iri:service:transfer-protocol:xrootd",
      "name": "XRootD endpoint"
    },
    {
      "url": "https://xrootd.example.gov",
      "protocol": "urn:doe-iri:service:transfer-protocol:https",
      "name": "XRootD HTTPS endpoint"
    }
  ]
}
```

The examples describe configured service definition, not operational state. Endpoint health, active transfers, queues, throughput, credentials, and current availability remain outside this profile.

---

*DOE Integrated Research Infrastructure — URN Registry: DTN Service*
