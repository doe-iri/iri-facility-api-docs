# IRI Object Storage Resource Definition Profile

**Profile URI:** `https://iri.science/profiles/resource-definition/storage/object`  
**Base Profile:** `https://iri.science/profiles/status/resource`  
**Resource Type:** `urn:doe-iri:resource:storage:object`  
**Status:** Draft  
**Version:** 1.0.0

## Profile Applicability

This profile applies when `resource_type` is
`urn:doe-iri:resource:storage:object` and MUST be used together with the
[IRI Status Resource Profile](../../status/resource.md). The authoritative
URN record is [Resource Type URNs](../../../urns/resource-types.md).

This document is for the `urn:doe-iri:resource:storage:object` resource type hierarchy.

## 1. Profile Context

The following retained context identifies the type to which this profile applies;
registration metadata and lifecycle are authoritative in the URN registry.

| Field             | Description |
| ----------------- | ----------- |
| URN               | `urn:doe-iri:resource:storage:object` |
| Short name        | Object Storage |
| Description       | This namespace collects object storage-related type definitions. |
| Parent URN        | `urn:doe-iri:resource:storage` |
| Status            | `provisional` |
| Introduced        | IRI v2.0 |
| Change controller | IRI technical subcommittee. |
| Reference         | Proposed type extensions for object storage resources. |
| Legacy value      | `storage` enumeration. |
| Examples          | `urn:doe-iri:resource:storage:object` |
| Notes             | These attributes are proposed for describing logical object storage resources provided by an IRI facility. |

## 2. Introduction

The purpose of this document is to define a common, implementation-independent representation of object storage resources within the DOE Integrated Research Infrastructure (IRI). An object storage resource is a logical storage resource that manages data as independently addressable objects, typically consisting of object data, associated metadata, and an object identifier or key.

Unlike filesystem storage, object storage does not inherently expose files and directories through a hierarchical filesystem namespace. Unlike block storage, it does not expose raw addressable blocks or volumes to consumers. Instead, consumers interact with object storage via an object storage API, typically through one or more service endpoints.

The IRI storage model intentionally separates the storage infrastructure from the logical object storage resource that consumers use. A `urn:doe-iri:resource:storage:system` resource represents the managed storage infrastructure, while a `urn:doe-iri:resource:storage:object` resource represents an independently consumable logical object-storage service or namespace provided by that infrastructure.

For example:

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        │ iri:provides-object
        ▼
Object Storage
urn:doe-iri:resource:storage:object
        │
        ├── object_apis
        ├── access_endpoints
        ├── object_technology
        ├── object_capabilities
        └── object_consistency
```

This separation allows a storage system to provide multiple logical object-storage resources without duplicating infrastructure-level characteristics. Each object resource can independently describe the API through which it is accessed, the endpoint or endpoints available to consumers, the implementation technology, supported capabilities, and other resource-specific characteristics.

Access endpoints are modeled as attributes of the object resource rather than as independent IRI resources. An endpoint describes where and through which API a consumer accesses the object resource, but normally does not require independent resource identity, lifecycle, or relationships.

If a future IRI use case requires an endpoint to have independently discoverable identity, relationships, or configuration, the endpoint MAY be promoted to a separately defined resource type in a future profile version.

This document defines configured characteristics of object storage resources. This version of the profile does not define current utilization, request rate, latency, health, available capacity, or service availability. If represented, the semantics and update behavior of those time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

## 3. Taxonomy

The taxonomy defined in this section identifies the DOE-IRI URN namespaces and controlled vocabulary values used by this Resource Definition Profile. It provides a machine-readable classification for the `urn:doe-iri:resource:storage:object` resource type and for object-storage attributes whose values require consistent semantics across IRI facilities.

The taxonomy distinguishes between the resource being described and the controlled characteristics used to describe that resource. The `urn:doe-iri:resource:storage:object` namespace identifies the resource type itself, while values beneath the `urn:doe-iri:storage` namespace identify standardized characteristics such as object-storage APIs, implementation technologies, consistency semantics, capabilities, storage tiers, and physical media.

The taxonomy is not intended to represent the relationship between an object storage resource and the storage system that provides it. That relationship is represented separately using the `iri:provides-object` IRI link relation.

Only attributes represented using controlled DOE-IRI URNs appear in the taxonomy. Scalar or structured attributes such as `access_endpoints` do not appear as taxonomy branches.

The following tree shows the resource type and controlled vocabulary namespaces defined by this profile.

```text
urn:doe-iri
│
├── resource
│   └── storage
│       └── object
│
└── storage
    │
    ├── object-api
    │   ├── s3
    │   └── swift
    │
    ├── object-technology
    │   ├── ceph-rgw
    │   ├── openstack-swift
    │   └── amazon-s3
    │
    ├── object-consistency
    │   ├── strong-read-after-write
    │   └── eventual
    │
    ├── object-capability
    │   ├── multipart-upload
    │   ├── versioning
    │   └── object-lock
    │
    ├── tier
    │   ├── home
    │   ├── project
    │   ├── scratch
    │   ├── campaign
    │   └── archive
    │
    └── media-type
        ├── magnetic-disk
        ├── solid-state
        ├── tape
        └── optical
```

## 4. Object Storage Attributes

This Resource Definition Profile defines the set of attributes that MAY be used to describe resources of type `urn:doe-iri:resource:storage:object`. These attributes provide a consistent, implementation-independent representation of logical object-storage characteristics while allowing facilities to expose only those characteristics that are known and relevant to IRI consumers.

The profile separates the identity of the object storage resource from the characteristics of the infrastructure that implements it. Controlled characteristics requiring consistent machine-readable semantics are represented using registered DOE-IRI URNs, while endpoint information is represented using structured JSON values.

Except for `schema_version`, attributes in this profile are optional. The absence of an optional attribute indicates that the information has not been provided and MUST NOT be interpreted as implying a particular value or capability. Clients SHOULD rely only on characteristics explicitly advertised by the resource.

The attributes defined by this profile describe configured characteristics of the object resource. The semantics of any time-varying values are governed by the applicable IRI API contract and Resource Definition Profile.

The following table defines version `1.0.0` of the object-storage attribute contract.

| Attribute             | Version | Type                 | Description                                                                                                                                   | Mandatory |
| --------------------- | ------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `schema_version`      | 1.0.0   | string               | Version of the profile definition (e.g. `"1.0.0"`).                                                                                           | yes       |
| `object_apis`         | 1.0.0   | Array IRI URN string | Identifies object-storage APIs through which the resource may be accessed.                                                                    | no        |
| `access_endpoints`    | 1.0.0   | Array ObjectEndpoint | Identifies service endpoints through which consumers may access the object resource.                                                          | no        |
| `object_technology`   | 1.0.0   | IRI URN string       | Identifies the technology, implementation, or platform providing the object storage resource.                                                 | no        |
| `object_consistency`  | 1.0.0   | IRI URN string       | Identifies the consistency model advertised by the object storage resource when it can be meaningfully represented by the defined vocabulary. | no        |
| `object_capabilities` | 1.0.0   | Array IRI URN string | Identifies capabilities exposed by the object storage resource.                                                                               | no        |
| `tier`                | 1.0.0   | IRI URN string       | Identifies the intended storage lifecycle or usage tier associated with the object resource.                                                  | no        |
| `media_types`         | 1.0.0   | Array IRI URN string | Identifies physical storage media known to back the object storage resource.                                                                  | no        |

### 4.1. Object Storage APIs

The `object_apis` attribute identifies the object-storage APIs or API families through which consumers may access a `urn:doe-iri:resource:storage:object` resource.

An object resource may expose more than one API. The `object_apis` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:object-api` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:object-api:s3`    | S3         | An object-storage API model in which objects are addressed by keys within buckets and manipulated using S3-compatible operations. | `provisional` |
| `urn:doe-iri:storage:object-api:swift` | Swift      | An object-storage API model in which objects are organized within containers and accessed using the OpenStack Swift API.          | `provisional` |

For example:

```json
{
  "object_apis": [
    "urn:doe-iri:storage:object-api:s3"
  ]
}
```

The API identifies the logical interface through which consumers interact with the object resource and is independent of the technology or product implementing that interface.

For example:

```text
Object Storage

object_technology = ceph-rgw

object_apis:
    s3
    swift
```

A single implementation may therefore expose multiple object-storage APIs.

Clients SHOULD NOT infer the object-storage API solely from `object_technology`. Facilities SHOULD explicitly advertise the APIs available to consumers.

API versions, extensions, authentication mechanisms, or provider-specific functionality SHOULD be represented independently if future interoperability requirements require them.

### 4.2. Object Storage Access Endpoints

The `access_endpoints` attribute identifies the service endpoints through which consumers may access a `urn:doe-iri:resource:storage:object` resource.

An object resource may expose multiple endpoints, including endpoints corresponding to different APIs or different access environments. The attribute is therefore represented as an array of structured endpoint descriptions.

Each endpoint contains:

| Property | Type           | Description                                                       | Mandatory |
| -------- | -------------- | ----------------------------------------------------------------- | --------- |
| `url`    | string URI     | Network location at which the object-storage API is exposed.      | yes       |
| `api`    | IRI URN string | Identifies the object-storage API available through the endpoint. | yes       |

For example:

```json
{
  "access_endpoints": [
    {
      "url": "https://objects.example.gov",
      "api": "urn:doe-iri:storage:object-api:s3"
    }
  ]
}
```

A resource exposing multiple APIs MAY advertise separate endpoints:

```json
{
  "access_endpoints": [
    {
      "url": "https://s3.example.gov",
      "api": "urn:doe-iri:storage:object-api:s3"
    },
    {
      "url": "https://swift.example.gov",
      "api": "urn:doe-iri:storage:object-api:swift"
    }
  ]
}
```

The endpoint identifies where requests are directed, while the `api` property identifies how consumers interact with that endpoint.

The presence of an endpoint does not imply that an unauthenticated consumer is authorized to access it. Authentication and authorization requirements are outside the scope of the endpoint description and SHOULD be represented through the applicable IRI security and access-control mechanisms.

Endpoint URLs SHOULD identify the service endpoint rather than an individual object URL.

Current endpoint availability is a time-varying observation and SHOULD NOT be inferred solely from the presence of an endpoint in this Resource Definition Profile.

### 4.3. Object Storage Technology

The `object_technology` attribute identifies the technology, implementation, or platform used to provide a `urn:doe-iri:resource:storage:object` resource.

The value of `object_technology` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:object-technology` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:object-technology:ceph-rgw`        | Ceph Object Gateway | An object-storage implementation provided by the Ceph Object Gateway (RGW), capable of exposing object data through supported object-storage APIs. | `provisional` |
| `urn:doe-iri:storage:object-technology:openstack-swift` | OpenStack Swift     | A distributed object-storage implementation provided by the OpenStack Swift platform.                                                              | `provisional` |
| `urn:doe-iri:storage:object-technology:amazon-s3`       | Amazon S3           | The Amazon S3 managed object-storage platform.                                                                                                     | `provisional` |

For example:

```json
{
  "object_technology":
    "urn:doe-iri:storage:object-technology:ceph-rgw"
}
```

The `object_technology` attribute identifies the implementation providing the logical object resource and is distinct from `storage_technology`, which identifies the technology implementing the underlying storage system.

It is also distinct from `object_apis`, which identify the interfaces exposed to consumers.

For example:

```text
Ceph Storage System
storage_technology = ceph
        │
        │ iri:provides-object
        ▼
Object Storage
object_technology = ceph-rgw

object_apis:
    s3
    swift
```

Clients SHOULD NOT infer APIs, capabilities, consistency semantics, storage media, or operational state solely from the value of `object_technology`.

### 4.4. Object Storage Consistency

The `object_consistency` attribute identifies the consistency semantics advertised by a `urn:doe-iri:resource:storage:object` resource when those semantics can be accurately represented using the defined DOE-IRI vocabulary.

The value of `object_consistency` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:object-consistency` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:object-consistency:strong-read-after-write` | Strong read-after-write | Successful writes are reflected by subsequent reads according to the consistency guarantees applicable to the object-storage resource.                                      | `provisional` |
| `urn:doe-iri:storage:object-consistency:eventual`                | Eventual consistency    | Updates may not be immediately visible to all subsequent operations, but replicas or service views are expected to converge over time in the absence of additional updates. | `provisional` |

For example:

```json
{
  "object_consistency":
    "urn:doe-iri:storage:object-consistency:strong-read-after-write"
}
```

Consistency semantics can vary by implementation, operation type, configuration, replication mode, or API behavior. The values defined by this profile intentionally represent broad consistency characteristics rather than a complete formal consistency model.

A facility SHOULD advertise `object_consistency` only when the selected value accurately characterizes the guarantees relevant to IRI consumers.

If the consistency behavior cannot be accurately represented using a single value, the attribute SHOULD be omitted rather than approximated.

Clients SHOULD NOT infer consistency semantics solely from the object-storage API or implementation technology.

### 4.5. Object Storage Capabilities

The `object_capabilities` attribute identifies capabilities exposed by a `urn:doe-iri:resource:storage:object` resource.

An object resource may expose multiple capabilities. The `object_capabilities` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:object-capability` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:object-capability:multipart-upload` | Multipart upload  | The object resource supports creation of an object by uploading its data as multiple independently transferred parts that are subsequently assembled into the completed object. | `provisional` |
| `urn:doe-iri:storage:object-capability:versioning`       | Object versioning | The object resource supports retaining and distinguishing multiple versions of an object associated with the same object key or identifier.                                     | `provisional` |
| `urn:doe-iri:storage:object-capability:object-lock`      | Object lock       | The object resource supports controls that prevent an object or object version from being modified or deleted for a defined period or under an applicable retention policy.     | `provisional` |

For example:

```json
{
  "object_capabilities": [
    "urn:doe-iri:storage:object-capability:multipart-upload",
    "urn:doe-iri:storage:object-capability:versioning",
    "urn:doe-iri:storage:object-capability:object-lock"
  ]
}
```

The `object_capabilities` attribute SHOULD describe capabilities actually exposed by the logical object resource.

Clients SHOULD NOT infer capabilities solely from the object technology or API. A technology may support a capability while that capability is disabled, restricted, or unavailable for a particular logical object resource.

Capabilities describe functionality and SHOULD NOT be interpreted as current operational condition.

The capability vocabulary is intended to be extensible. Additional capability URNs SHOULD be registered when they identify meaningful, implementation-independent functionality that an IRI consumer may need to discover or reason about.

### 4.6. Storage Tier

The `tier` attribute identifies the intended storage lifecycle, usage pattern, or purpose associated with a `urn:doe-iri:resource:storage:object` resource.

The value of `tier` MUST be a registered DOE-IRI URN from the `urn:doe-iri:storage:tier` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:tier:home`     | Home       | Persistent user-oriented storage intended for user-specific data and ongoing individual use.                                                                       | `provisional` |
| `urn:doe-iri:storage:tier:project`  | Project    | Shared persistent storage allocated to a project, collaboration, or team for ongoing project data and collaborative use.                                           | `provisional` |
| `urn:doe-iri:storage:tier:scratch`  | Scratch    | Temporary storage intended for active workloads, intermediate data, or transient working data and typically subject to limited retention.                          | `provisional` |
| `urn:doe-iri:storage:tier:campaign` | Campaign   | Intermediate-term storage intended to retain data associated with a scientific campaign, experiment, project, or allocation for the duration of that activity.     | `provisional` |
| `urn:doe-iri:storage:tier:archive`  | Archive    | Storage intended for durable, long-term retention of data that is accessed less frequently and is not expected to provide active-tier performance characteristics. | `provisional` |

For example:

```json
{
  "tier":
    "urn:doe-iri:storage:tier:project"
}
```

Storage tier describes the intended role or lifecycle of the object resource and is independent of the API, object technology, physical media, and consistency semantics.

For example:

```text
Object Storage

tier = archive

object_api = s3

media_types:
    magnetic-disk
    tape
```

A client SHOULD NOT infer performance, retention policy, durability, retrieval latency, or media type solely from the `tier` value.

### 4.7. Storage Media Types

The `media_types` attribute identifies physical storage media known to retain data associated with a `urn:doe-iri:resource:storage:object` resource.

An object resource may be backed by more than one type of physical storage media. The `media_types` attribute is therefore represented as an array of registered DOE-IRI URNs. Values are drawn from the `urn:doe-iri:storage:media-type` namespace.

| URN | Short name | Description | Status |
|---|---|---|---|
| `urn:doe-iri:storage:media-type:magnetic-disk` | Magnetic disk | Storage media that retains data magnetically on rotating disks, such as hard disk drives (HDDs).                                                   | `provisional` |
| `urn:doe-iri:storage:media-type:solid-state`   | Solid-state   | Nonvolatile electronic storage media with no moving mechanical components, such as flash-based solid-state drives (SSDs).                          | `provisional` |
| `urn:doe-iri:storage:media-type:tape`          | Tape          | Storage media that retains data magnetically on tape and is generally optimized for high-capacity, sequential access and long-term data retention. | `provisional` |
| `urn:doe-iri:storage:media-type:optical`       | Optical       | Storage media that retains data using optically readable media, such as CD, DVD, Blu-ray, or other optical storage technologies.                   | `provisional` |

For example:

```json
{
  "media_types": [
    "urn:doe-iri:storage:media-type:magnetic-disk",
    "urn:doe-iri:storage:media-type:tape"
  ]
}
```

The presence of multiple media types indicates that object data associated with the resource may be retained using more than one physical medium. It does not indicate how individual objects are distributed or moved between those media.

For example, a system may automatically move object data from disk to tape according to lifecycle or tiering policy. The `media_types` attribute communicates only that those physical media are associated with the object resource; it does not describe the placement policy.

Media types SHOULD be advertised at the object-resource level only when the backing media are known and meaningful to consumers. Where physical media information is available only for the underlying storage infrastructure, the information SHOULD instead be advertised on the corresponding storage-system resource.

Clients SHOULD NOT infer performance, latency, durability, accessibility, or storage tier solely from media type.

The attribute SHOULD be omitted when the underlying media cannot be meaningfully determined for the logical object resource or when the facility does not intend to expose that implementation detail.

## 5. Object Storage JSON Schema

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
      example: urn:doe-iri:storage:object-api:s3

    ObjectEndpoint:
      type: object
      description: >
        An access endpoint through which consumers may access an
        object storage resource.
      required:
        - url
        - api
      properties:

        url:
          type: string
          format: uri
          description: >
            Network service endpoint through which the object storage
            resource may be accessed.
          example: https://objects.example.gov

        api:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the object-storage API exposed by this endpoint.
          example: urn:doe-iri:storage:object-api:s3

    ObjectStorageAttributes:
      type: object
      description: >
        Attributes describing an object storage resource with resource type
        urn:doe-iri:resource:storage:object.
      required:
        - schema_version

      properties:

        schema_version:
          type: string
          description: >
            Version of the object-storage attribute contract.
          enum:
            - "1.0.0"
          example: "1.0.0"

        object_apis:
          type: array
          description: >
            Identifies object-storage APIs through which the resource
            may be accessed.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:object-api:s3

        access_endpoints:
          type: array
          description: >
            Identifies service endpoints through which consumers may
            access the object resource.
          items:
            $ref: '#/components/schemas/ObjectEndpoint'

        object_technology:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the technology, implementation, or platform
            providing the object storage resource.
          example: urn:doe-iri:storage:object-technology:ceph-rgw

        object_consistency:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the consistency model advertised by the
            object storage resource.
          example: urn:doe-iri:storage:object-consistency:strong-read-after-write

        object_capabilities:
          type: array
          description: >
            Identifies capabilities exposed by the object storage resource.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:object-capability:multipart-upload
            - urn:doe-iri:storage:object-capability:versioning

        tier:
          $ref: '#/components/schemas/IriUrn'
          description: >
            Identifies the intended storage lifecycle or usage tier
            associated with the object resource.
          example: urn:doe-iri:storage:tier:project

        media_types:
          type: array
          description: >
            Identifies physical storage media known to back the
            object storage resource.
          uniqueItems: true
          items:
            $ref: '#/components/schemas/IriUrn'
          example:
            - urn:doe-iri:storage:media-type:magnetic-disk
```

## 6. Example Object Storage JSON Instance

```json
{
  "schema_version": "1.0.0",
  "object_apis": [
    "urn:doe-iri:storage:object-api:s3"
  ],
  "access_endpoints": [
    {
      "url": "https://objects.example.gov",
      "api": "urn:doe-iri:storage:object-api:s3"
    }
  ],
  "object_technology": "urn:doe-iri:storage:object-technology:ceph-rgw",
  "object_consistency": "urn:doe-iri:storage:object-consistency:strong-read-after-write",
  "object_capabilities": [
    "urn:doe-iri:storage:object-capability:multipart-upload",
    "urn:doe-iri:storage:object-capability:versioning"
  ],
  "tier": "urn:doe-iri:storage:tier:project",
  "media_types": [
    "urn:doe-iri:storage:media-type:magnetic-disk"
  ]
}
```

The complete resource model associates the object resource with the storage system that provides it while keeping consumer access information within the object resource's profile:

```text
Storage System
urn:doe-iri:resource:storage:system
        │
        │ iri:provides-object
        ▼
Object Storage
urn:doe-iri:resource:storage:object

attributes:
    object_apis = [s3]
    access_endpoints:
        https://objects.example.gov
    object_technology = ceph-rgw
    object_consistency = strong-read-after-write
    object_capabilities:
        multipart-upload
        versioning
    tier = project
```

The endpoint identifies **where and how the logical object resource is accessed**. It does not represent a separate storage resource unless an IRI use case requires independent endpoint identity, configuration, relationships, or lifecycle.

---

*DOE Integrated Research Infrastructure — URN Registry: Object Storage*
