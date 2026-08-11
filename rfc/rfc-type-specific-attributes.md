# **RFC: Type-Specific Attributes for IRI Resource Objects**

## **Abstract**

This document defines an optional `attributes` property for the IRI Facility API `Resource` object, that could also be extended to other objects with a URN type attribute.

The `attributes` property provides a structured extension point for metadata that is specific to the resource type identified by `resource_type`. It allows facilities to describe resource-specific properties without continually expanding the common `Resource` schema.

This RFC adopts the IRI Type URN model for selecting the semantic interpretation and validation profile of `attributes`. A resource whose `resource_type` is `urn:doe-iri:resource:storage:system`, for example, may expose filesystem type and capacity information through a storage-system attribute profile.

This document defines the core extension mechanism, profile-selection rules, OpenAPI changes, compatibility expectations, an example storage-system profile, and implementation guidance.

## **Status of This Memo**

This document is a proposed IRI Facility API extension and is intended for adoption within the DOE IRI specification version 2.0 and reference implementations.

| Revision | Author | Date | Notes |
| :---- | :---- | :---- | :---- |
| 0.1 | ChatGPT | Jun 24, 2026 | Initial version from John’s dank prompt. |
| 0.2 | John MacAuley | Jun 24, 2026 | Revised based on initial thoughts. |
| 0.3 | John MacAuley | Jul 22, 2026 | Final revisions before subcommittee discussions. |
| 1.0 | John MacAuley | Aug 7, 2026 | Comments addressed.  Issuing version 1.0 for publication. |

## 

## 

## **1\. Introduction**

The IRI Facility API `Resource` object describes a facility resource through common properties such as `id`, `name`, `description`, `current_status`, `resource_type`, and `capability_uris`.

Facilities also need to describe information that is meaningful only for certain classes of resources. Examples include:

* filesystem capacity and storage technology;  
* compute-node architecture, accelerator inventory, and queue associations;  
* network bandwidth, interface type, and routing domain;  
* data-transfer protocol support and endpoint characteristics;  
* service implementation details and operational capabilities.

Adding every such property to the common `Resource` schema would create a broad, unstable, and difficult-to-implement model. Conversely, placing arbitrary fields directly on a `Resource` object makes those fields difficult to discover, validate, document, and process consistently.

This RFC defines `attributes` as the designated extension point for type-specific resource metadata.

## **1.1. Requirements Language**

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## **2\. Scope**

This RFC:

1. Adds an OPTIONAL `attributes` property to the `Resource` schema.  
2. Defines the `resource_type` property as the selector for a resource attribute profile.  
3. Defines rules for canonical and facility-local attribute profiles.  
4. Defines an example attribute profile for a fictitious storage-system resource.  
5. Applies to all API responses that use the `Resource` schema.

This RFC does not:

1. Define every possible resource-type attribute profile.  
2. Add generic query filtering for arbitrary attribute values.  
3. Add write operations for resource attributes.  
4. Define authorization policy based on attributes.  
5. Require clients to dereference or dynamically fetch schemas at runtime.

## **3\. Design Goals**

The design has the following goals:

1. Preserve a small and stable common `Resource` schema.  
2. Permit facilities to publish useful type-specific metadata.  
3. Make attribute meaning discoverable from `resource_type`.  
4. Allow shared attribute profiles to be standardized incrementally.  
5. Allow facility-local extensions without changing the core OpenAPI document.  
6. Permit clients to ignore unfamiliar attributes safely.  
7. Avoid collisions between common resource fields and type-specific metadata.  
8. Maintain compatibility with clients that do not use type-specific attributes.

## **4\. Proposed Resource Model**

### **4.1. The `attributes` Property**

A `Resource` MAY include an `attributes` property.

`attributes` MUST be a JSON object when present. It MUST NOT be `null`.

The property is OPTIONAL. A producer SHOULD omit `attributes` when it has no attributes to report rather than emitting an empty object.

The semantic meaning, allowed property names, value types, required fields, and validation rules for `attributes` are determined by the resource's `resource_type` value.

Example:

```json
{
  "id": "orion",
  "name": "Orion",
  "description": "Lustre HPE ClusterStor system",
  "last_modified": "2026-06-24T12:00:00Z",
  "current_status": "up",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "self_uri": "https://api.example.org/api/v2/status/resources/orion",
  "site_uri": "https://api.example.org/api/v2/sites/example-site",
  "capability_uris": [],
  "attributes": {
    "schema_version": "1.0.0",
    "storage_type": "urn:doe-iri:storage:filesystem",
    "filesystem_technology": "lustre",
    "vendor": "HPE",
    "product": "ClusterStor"
  }
}
```

### **4.2. Core-Field Precedence**

The following fields remain common, normative properties of a `Resource` object:

* `id`  
* `name`  
* `description`  
* `last_modified`  
* `group`  
* `current_status`  
* `resource_type`  
* `supported_endpoints`  
* `self_uri`  
* `site_uri`  
* `capability_uris`

An `attributes` object MUST NOT redefine or override any common `Resource` property.

If a profile defines an attribute that appears to overlap semantically with a common property, the common property is authoritative. Profiles SHOULD avoid such duplication.

For example, `attributes.current_status` MUST NOT be used because `current_status` is already a top-level property.

### **4.3. Attribute Value Types**

The core `attributes` schema permits valid JSON values, including objects, arrays, strings, booleans, numbers, and `null` values where permitted by the applicable profile.

Profiles SHOULD use explicit units in property names or companion fields. For example:

* `total_bytes`  
* `available_bytes`  
* `bandwidth_bps`  
* `node_count`  
* `gpu_count`

## **5\. Resource Type URN Prerequisite**

### **5.1. Resource Type as Profile Selector**

A resource attribute profile is selected by the full `resource_type` IRI Type URN.

For example:

```
urn:doe-iri:resource:storage:system
```

selects the storage-system resource attribute profile.

The profile-selection key is the complete URN. A client MAY use URN parent relationships for generic display or fallback behavior, but MUST NOT infer a complete validation schema solely from parent-prefix matching.

A child profile that inherits from a parent profile MUST declare that inheritance explicitly in its profile schema or documentation.

### **5.2. Valid Domains**

For a `Resource` object, the `resource_type` value MUST be an IRI Type URN when type-specific attributes are present.

Examples:

```
urn:doe-iri:resource:compute
urn:doe-iri:resource:storage:system
urn:doe-iri:resource:network
urn:doe-iri:service:website
urn:doe-iri:service:dtn:globus
```

## **6\. Attribute Profiles**

### **6.1. Profile Definition**

An attribute profile defines the valid structure and semantics of `attributes` for one specific `resource_type` URN.

Each profile SHOULD define:

| Field | Description |
| ----- | ----- |
| Resource type URN | Exact URN governed by the profile. |
| Profile version | Version of the profile definition. |
| Description | Human-readable statement of the profile's scope. |
| JSON Schema | Machine-readable schema for attributes. |
| Required properties | Properties required when the profile is used. |
| Units | Units and encoding rules for numeric quantities. |
| Extension policy | Whether and how additional facility-local properties are permitted. |
| Status | Active, deprecated, or superseded. |
| Examples | Representative API payloads. |

### **6.2. Profile Publication**

Canonical profiles SHOULD be published in the DOE-IRI URN Registry or an associated IRI specification repository.

A facility MAY publish a facility-local profile for a valid facility-local IRI Type URN.

A facility-local profile SHOULD:

1. Use the nearest accurate shared parent type.  
2. Be documented in a facility-controlled location.  
3. Identify its facility or project namespace where appropriate.  
4. Be proposed for shared registration when it becomes useful across multiple facilities.

Clients MUST NOT be required to retrieve a profile dynamically in order to process a `Resource` response. A client that does not recognize a profile MUST preserve or ignore the attributes according to its local behavior and MUST NOT reject the entire resource solely because the profile is unfamiliar.

#### **6.2.1. URN Collision and Resolution**

In the event that a client encounters a URN that it cannot resolve or validate:

1. **Unknown-Type Handling:** Clients MUST implement an "unknown-type-handler" pattern, treating unrecognized URNs as opaque objects. Consumers SHOULD NOT fail or reject the Resource object solely due to an unknown `resource_type` or invalid schema.

2. **Resolution Conflicts:** If a client encounters a URN that resolves to conflicting definitions (e.g., a facility-local URN that mimics a canonical URN), the client SHOULD prioritize the registry-published canonical definition if available.

3. **Validation Fallback:** Where canonical validation is unavailable, clients SHOULD implement a "best-effort" validation mode that enforces basic JSON structural requirements (e.g., checking for valid JSON types) rather than full schema validation.

### **6.3. Extension Policy**

The core `attributes` object permits additional properties.

A canonical profile SHOULD define the behavior of additional properties explicitly. Facilities introducing nonstandard fields SHOULD prefer one of these approaches:

1. Define a facility-local descendant `resource_type` URN and publish a corresponding profile.  
2. Use a documented, facility-qualified extension property name.  
3. Propose the property for inclusion in the shared canonical profile when cross-facility use emerges.

New type-specific metadata SHOULD be added beneath `attributes`, not as new arbitrary top-level `Resource` properties.

## **7\. Example Storage-System Attribute Profile**

This RFC defines an example profile for a ResourceType identified by URN:

```
urn:doe-iri:resource:storage:system
```

This profile describes a storage system or filesystem service represented as a `Resource`.

### **7.1. Profile Properties**

| Property | Type | Required | Description |
| ----- | ----- | ----- | ----- |
| `schema_version` | string | Yes | The version of the profile definition. |
| `storage_type` | IRI Type URN string | Yes | The storage abstraction provided by the resource. |
| `filesystem_technology` | string | Yes | The specific technology used by the filesystem (e.g., lustre, gpfs, nfs). |
| `vendor` | string | No | The manufacturer or vendor of the storage hardware. |
| `product` | string | No | The product name or model of the storage system. |

### **7.2. Semantic Rules**

For the storage-system profile:

1. `schema_version` MUST be provided as a string property representing the version of the profile definition.  
2. `storage_type` MUST identify the storage abstraction using an IRI Type URN.  
3. `filesystem_technology` MUST be provided as a string.  
4. `vendor` and `product` are optional string properties.  
5. The producer MUST update last\_modified when a material change to the attributes occurs.

Examples of valid `storage_type` values include:

```
urn:doe-iri:storage:filesystem
urn:doe-iri:storage:object
urn:doe-iri:storage:block
urn:doe-iri:storage:tape
```

### **7.3. Storage-System Profile Schema**

```
StorageSystemAttributes:
  type: object
  additionalProperties: true
  required:
    - schema_version
    - storage_type
    - filesystem_technology
  properties:
    schema_version:
      type: string
      example: "1.0.0"
      description: The version of the profile definition.

    storage_type:
      type: string
      format: uri
      pattern: '^urn:doe-iri:storage:.+$'
      description: IRI Type URN identifying the storage abstraction.
      example: urn:doe-iri:storage:filesystem

    filesystem_technology:
      type: string
      description: The specific technology used by the filesystem.
      example: lustre

    vendor:
      type: string
      description: The manufacturer or vendor of the storage hardware.
      example: HPE

    product:
      type: string
      description: The product name or model of the storage system.
      example: ClusterStor
```

## **8\. OpenAPI Changes**

### **8.1. New `ResourceAttributes` Schema**

The following schema MUST be added under `components.schemas`.

```
ResourceAttributes:
  type: object
  additionalProperties: true
  description: >
    Optional resource-type-specific metadata. The meaning, permitted
    property names, value types, and validation rules are defined by the
    attribute profile selected by the Resource.resource_type IRI Type URN.
```

### **8.2. Update to `Resource`**

The following property MUST be added to the `Resource` schema.

```
attributes:
  $ref: '#/components/schemas/ResourceAttributes'
```

`attributes` MUST NOT be added to the `required` list.

### **8.3. Illustrative `Resource` Fragment**

```
Resource:
  type: object
  additionalProperties: true
  required:
    - id
    - last_modified
    - resource_type
    - self_uri
    - site_uri
    - capability_uris
  properties:
    id:
      type: string

    resource_type:
      $ref: '#/components/schemas/ResourceType'

    attributes:
      $ref: '#/components/schemas/ResourceAttributes'
```

## **9\. API Behavior**

### **9.1. Applicable Endpoints**

No new endpoint is required.

The `attributes` property appears automatically wherever the API returns a `Resource` object, including:

```
GET /api/v2/status/resources
GET /api/v2/status/resources/{resource_id}
```

### **9.2. Filtering**

This RFC does not define filtering on arbitrary attribute values.

The existing `resource_type` filter SHOULD accept canonical URN.

```
?resource_type=urn:doe-iri:resource:storage
```

A future RFC MAY define profile-aware attribute filtering after common query semantics, authorization behavior, indexing requirements, and performance expectations are established.

### **9.3. Modification Semantics**

When an attribute value changes materially, the producer MUST update the resource's `last_modified` value.

An implementation MAY apply local policy to determine whether routine telemetry changes are material. That policy SHOULD be documented for values such as free capacity, bandwidth utilization, or transient operational statistics.

## **10\. Producer Requirements**

A producer that supports this RFC:

1. MAY omit `attributes` for any resource.  
2. MUST emit `attributes` as a JSON object when present.  
3. MUST use a valid IRI Type URN in `resource_type` when `attributes` is present.  
4. MUST ensure that attributes conform to the applicable profile.  
5. MUST NOT place credentials, access tokens, secrets, private keys, or other sensitive authentication material in attributes.  
6. MUST NOT use attributes to override common `Resource` fields.  
7. SHOULD publish profile documentation for facility-local resource types.  
8. SHOULD use canonical profiles and URNs where available.  
9. SHOULD omit empty `attributes` objects.  
10. MUST update `last_modified` when a material attribute change occurs.

## **11\. Consumer Requirements**

A consumer that supports this RFC:

1. MUST tolerate the absence of `attributes`.  
2. MUST treat an unfamiliar attribute profile as non-fatal.  
3. MUST NOT reject a resource solely because it contains unfamiliar attribute names.  
4. SHOULD use the full `resource_type` URN to select a known profile.  
5. MAY use a recognized parent URN for generic display or classification.  
6. MUST NOT rely on attributes alone for authorization, policy enforcement, or access control.  
7. SHOULD ignore attributes that are not relevant to the consumer's purpose.

## **12\. Backward Compatibility and Versioning**

### **12.1. API Compatibility**

Adding an optional `attributes` property is additive for clients that correctly tolerate unknown response properties.

The current `Resource` schema already permits additional properties. This RFC standardizes `attributes` as the designated and documented location for type-specific resource metadata.

### **12.2. Profile Evolution**

Adding OPTIONAL fields to a profile is backward compatible.

Removing a field, changing a field's meaning, changing units, or narrowing a field's accepted value range is not backward compatible. Such a change MUST use one of the following approaches:

1. A new profile version with explicit compatibility documentation.  
2. A new descendant resource-type URN.  
3. A new major API version.

### **12.3. Profile Versioning**

All attribute profiles MUST include a mandatory `schema_version` field (e.g., `schema_version`: `"1.2.0"`) as a string property within their metadata definition. This allows clients to programmatically distinguish between variations of a schema without inferring the structure from the context, and ensures that facilities can evolve their schemas while maintaining backward compatibility. 

The `schema_version` property is scoped to the specific attributes profile selected by the `resource_type`. It is not a global property of the Resource object, nor is it a global property of the attributes container. Consumers MUST validate the `schema_version` only in the context of the schema associated with the resource's `resource_type`.

## **13\. Security Considerations**

Attributes are descriptive metadata. They are not authorization artifacts, proof of entitlement, or trusted policy assertions.

Implementations MUST treat attribute values as data, not executable instructions.

Implementations SHALL NOT deserialize attribute values to define or instantiate an arbitrary class (e.g. unpickle).

Implementations SHOULD:

1. Validate data received from external systems before publishing it.  
2. Apply size, nesting-depth, and serialization limits appropriate to their environment.  
3. Avoid exposing internal hostnames, topology details, identifiers, or operational data where disclosure would create risk.  
4. Avoid automatic schema retrieval or execution based solely on a received URN.  
5. Ensure that displayed attribute values are safely escaped in user interfaces.  
6. Ensure that attributes do not expose credentials, tokens, secrets, or protected personal information.

## **14\. IANA Considerations**

This document requires no IANA action.

## **15\. References**

* RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*.  
* RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.  
* RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format*.  
* RFC 8141, *Uniform Resource Names (URNs)*.  
* OpenAPI Specification 3.1.0.  
* IRI RFC, *A URN Namespace for the DoE IRI Project*.  
* IRI Facility API OpenAPI Specification, version 2.0.0.

## **Appendix A. Complete Storage-System Example**

```json
{
  "id": "orion",
  "name": "Orion",
  "description": "Lustre HPE ClusterStor system",
  "last_modified": "2026-06-24T12:00:00Z",
  "current_status": "up",
  "resource_type": "urn:doe-iri:resource:storage:system",
  "self_uri": "https://api.example.org/api/v2/status/resources/orion",
  "site_uri": "https://api.example.org/api/v2/sites/example-site",
  "capability_uris": [],
  "attributes": {
    "schema_version": "1.0.0",
    "storage_type": "urn:doe-iri:storage:filesystem",
    "filesystem_technology": "lustre",
    "vendor": "HPE",
    "product": "ClusterStor"
  }
}
```

