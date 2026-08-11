# DOE IRI Registry

> Documentation for the identifiers, type-specific attribute profiles, and hypermedia relationships used by the Department of Energy Integrated Research Infrastructure (IRI) Facility API.

The DOE IRI Registry documents a three-layer specification model for the IRI Facility API. The model separates **resource type identifiers**, **type-specific attributes**, and **hypermedia relationships** so that each area can evolve without requiring every change to be reflected in the core OpenAPI schema.

At a high level, the model is:

**Type → Attributes → Relationships**

## Three-Layer Model

| Layer | Purpose |
|---|---|
| **1. URN Registry** | Identifies **what kind of resource** an API resource represents. |
| **2. Attribute Profiles** | Defines the **type-specific metadata** associated with that resource type. |
| **3. HAL `_links` Relations** | Describes **relationships between resource instances** and how clients navigate to related resources. |

The three layers are **independently extensible**:

- New type URNs can be introduced without requiring changes to the core OpenAPI schema.
- Attribute profiles can evolve through the registry as type-specific metadata changes.
- Link relations can be added or refined without adding relationship-specific properties to resource schemas.

The layers are related but serve different purposes. A resource's `resource_type` identifies its registered type and selects the applicable attribute profile, while registered HAL link relations describe how that resource is connected to other IRI resources.

## Registry Documents

The first three documents below correspond directly to the three-layer model. The fourth provides detailed documentation for the link relations defined in Layer 3.

| Section | File | Description |
|---|---|---|
| **1. URN Registry** | [01-urn-registry.md](01-urn-registry.md) | Defines the `doe-iri` Namespace ID, ABNF syntax, domain values, canonical URNs, hierarchical semantics, prefix-matching rules, registry model, and validation requirements. |
| **2. Attribute Profiles** | [02-attribute-profiles.md](02-attribute-profiles.md) | Defines profile selection through `resource_type`, the OpenAPI `ResourceAttributes` schema, profile definitions for each resource domain (storage, compute, network, service, compression), extension policies, and versioning rules. |
| **3. HAL `_links` Relations** | [03-hal-links.md](03-hal-links.md) | Defines the `HalLink` and `HalLinks` JSON schemas, CURIE conventions, registered and IRI-specific link relations, and schema-integration guidance. Link relations are grouped by state navigation, dynamic state, operations, and topology. |
| **4. Link Profile Documentation** | [04-link-profiles.md](04-link-profiles.md) | Provides per-relation documentation including source type, target type, cardinality, static/dynamic classification, profile URIs, example payloads, and authorization notes. |

## How to Use This Registry

Use the registry document that corresponds to the aspect of the resource model you are working with:

- **Defining or validating a resource type:** start with the [URN Registry](01-urn-registry.md).
- **Defining type-specific resource metadata:** use the [Attribute Profiles](02-attribute-profiles.md).
- **Representing relationships between resources:** use the [HAL `_links` Relations](03-hal-links.md).
- **Implementing or interpreting a specific IRI link relation:** consult the [Link Profile Documentation](04-link-profiles.md).

## Conceptual Example

The following example is illustrative only. It shows where each layer appears in an IRI resource representation without defining any new registry values.

```json
{
  "resource_type": "<registered IRI resource-type URN>",
  "attributes": {
    "<type-specific attribute>": "<value>"
  },
  "_links": {
    "<registered relation>": {
      "href": "<related-resource-URI>"
    }
  }
}
```

The mapping is:

```text
resource_type → Layer 1: resource classification
attributes    → Layer 2: type-specific metadata
_links        → Layer 3: resource relationships
```

## Related RFCs (Archived)

The original RFC documents synthesized by this registry are archived under [`docs/rfc-archive/`](../rfc-archive/).

| RFC | Source |
|---|---|
| A URN Namespace for the DoE IRI Project | [`rfc-iri-urn-structure-and-registry.md`](../rfc-archive/rfc-iri-urn-structure-and-registry.md) |
| Type-Specific Attributes for IRI Resource Objects | [`rfc-type-specific-attributes.md`](../rfc-archive/rfc-type-specific-attributes.md) |
| HAL `_links` Integration for IRI 2.0 | Pending publication |
| Facility Physical and Logical Topology API Using HAL Links | Pending publication |
| Separating ResourceDefinition from ResourceState | Pending publication |


---

*IRI specification — DOE Integrated Research Infrastructure*
