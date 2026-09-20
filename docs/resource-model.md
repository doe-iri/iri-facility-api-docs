---
layout: default
title: IRI Resource Model
parent: IRI Architecture
nav_order: 1
permalink: /resource-model/
---

# IRI Resource Model

This page explains how the major IRI 2.0 representation concepts fit together: `Resource`, `resource_type`, Resource Definition Profiles, `attributes`, registered URNs, `_links`, relation definitions, target profiles, and OpenAPI.

> **Documentation status**
>
> This page is explanatory. Normative requirements are defined by the versioned specifications, registry entries, profiles, link relation definitions, RFCs, and OpenAPI documents in the `doe-iri/iri-facility-api-docs` repository.

## Overview

An IRI Resource representation combines:

- a **common structural representation**,
- a **semantic classification** using `resource_type`,
- optional **type-specific attributes**,
- **registered relationships and navigation links**, and
- optionally a **machine-readable service description**.

These concerns are intentionally separated so that clients can interpret resources consistently without requiring facility-specific URL construction or out-of-band conventions.

## Resource model diagram

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              IRI Resource                                   │
│                                                                              │
│  Common representation defined by specification / OpenAPI                    │
│                                                                              │
│  {                                                                           │
│    "resource_id": "...",                                                     │
│    "resource_type": "urn:doe-iri:resource:...",                              │
│    "attributes": { ... },                                                    │
│    "_links": { ... }                                                         │
│  }                                                                           │
└───────────────┬──────────────────────────────┬───────────────────────────────┘
                │                              │
                │                              │
                ▼                              ▼
      ┌──────────────────────┐      ┌──────────────────────┐
      │    resource_type     │      │        _links        │
      │  registered URN      │      │   relation-bearing   │
      └──────────┬───────────┘      │   navigation object   │
                 │                  └──────────┬───────────┘
                 │                             │
                 ▼                             ▼
   ┌─────────────────────────────┐   ┌─────────────────────────────┐
   │ Resource Type URN Registry  │   │ Link Relation Registry      │
   │ e.g. compute/system         │   │ e.g. iri:has-mount          │
   └──────────┬──────────────────┘   └──────────┬──────────────────┘
              │                                 │
              │ selects                         │ defines meaning of
              ▼                                 ▼
   ┌─────────────────────────────┐   ┌─────────────────────────────┐
   │ Resource Definition Profile │   │  Link target metadata       │
   │ type-specific semantics     │   │  href / type / profile      │
   └──────────┬──────────────────┘   └──────────┬──────────────────┘
              │                                 │
              │ governs meaning of              │ profile may identify
              ▼                                 ▼
   ┌─────────────────────────────┐   ┌─────────────────────────────┐
   │         attributes          │   │       Target Profile        │
   │ type-specific fields        │   │ representation semantics    │
   │ and controlled values       │   └─────────────────────────────┘
   └──────────┬──────────────────┘
              │
              │ may use
              ▼
   ┌─────────────────────────────┐
   │  Registered URNs            │
   │  controlled attribute       │
   │  values / identifiers       │
   └─────────────────────────────┘


                      Structural contract across the representation
                                      is defined by
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │           OpenAPI           │
                               │ + JSON Schema contract      │
                               └─────────────────────────────┘
```

## The core relationship

At a high level, the model works like this:

```text
Resource
  ├── structure comes from specification / OpenAPI
  ├── resource_type classifies what the resource is
  ├── resource_type selects the applicable Resource Definition Profile
  ├── attributes carry type-specific data under that semantic model
  ├── attributes may use registered URNs as controlled values
  └── _links advertise related resources, topology, state, and operations
          ├── relation name semantics come from the Link Relation Registry
          └── target profile may describe the linked representation semantics
```

## Component by component

### 1. Resource

A **Resource** is the IRI representation being exchanged.

It is the object a client receives and interprets. It carries both common structural elements and type-specific meaning.

Conceptually:

```json
{
  "resource_id": "frontier",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "attributes": {
    "...": "..."
  },
  "_links": {
    "...": {}
  }
}
```

The Resource itself is not defined solely by one registry file. Its full structure is governed by the specification and OpenAPI contract.

---

### 2. `resource_type`

`resource_type` answers:

> **What kind of resource is this?**

It is a **registered Resource Type URN**, such as:

```text
urn:doe-iri:resource:compute:system
```

This identifier classifies the resource semantically.

`resource_type` does **not** itself provide the full detailed semantics of every type-specific field. Instead, it points the client toward the appropriate Resource Definition semantics.

---

### 3. Resource Type URN registry

The **Resource Type URN registry** is the authoritative source of registered resource classifications.

It answers:

> **Is this a known IRI resource kind?**

Examples include classifications for compute, storage, network, and related infrastructure concepts.

This layer gives the ecosystem a shared vocabulary for identifying what a Resource represents.

---

### 4. Resource Definition Profile

The **Resource Definition Profile** answers:

> **What additional semantics apply to Resources of this type?**

The Resource Definition Profile is distinct from the Resource Type URN.

For example:

```text
resource_type:
urn:doe-iri:resource:compute:system
```

may correspond to a profile URI pattern such as:

```text
https://iri.science/profiles/resource-definition/compute/system
```

The profile defines how to interpret type-specific semantics for that resource type.

---

### 5. `attributes`

`attributes` answers:

> **What type-specific descriptive or operational data does this resource carry?**

The structure of `attributes` is governed at two levels:

1. the overall structural contract from the specification / OpenAPI, and
2. the type-specific semantics selected by the Resource Definition Profile.

So `attributes` are not interpreted in isolation. Their meaning depends on the resource type and profile context.

Conceptually:

```text
resource_type
      │
      ▼
Resource Definition Profile
      │
      ▼
meaning of attributes
```

---

### 6. Registered URNs used in `attributes`

Some attribute values are controlled identifiers rather than arbitrary local strings.

These **registered URNs** answer:

> **Which standardized controlled value is being used here?**

Examples may include controlled values for storage technology, media types, architectures, capabilities, or other registered semantics.

So the relationship is:

```text
attributes
   └── may contain registered controlled URNs
```

This gives type-specific fields portable, shared meanings across facilities.

---

### 7. `_links`

`_links` answers:

> **What related resources, state, operations, or service descriptions are available from here?**

`_links` provides the navigational and relationship layer of the representation.

Conceptually:

```json
{
  "_links": {
    "self": {
      "href": "https://facility.example/api/v2/status/resources/frontier"
    },
    "iri:has-mount": {
      "href": "https://facility.example/api/v2/status/resources/frontier-orion-scratch-mount",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    },
    "service-desc": {
      "href": "https://facility.example/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

The important idea is that `_links` advertises targets explicitly so clients do not have to construct URLs by guesswork.

---

### 8. Link relation definitions

Each link relation answers:

> **Why is this target linked from the current representation?**

For example:

```text
iri:has-mount
```

does not merely label a URL. It identifies the **semantic relationship** between the current Resource and the target.

The authoritative meaning of that relation belongs in the **Link Relation Registry**.

Relationship summary:

```text
_links
   └── relation names
           └── semantics defined by Link Relation Registry
```

---

### 9. Target profiles

A link target may include a `profile` value.

That answers:

> **What representation semantics apply to the target representation?**

This is different from the relation definition.

- The **relation** explains the semantic role of the link.
- The **target profile** explains how to interpret the linked representation.

Conceptually:

```text
Current Resource
    │
    ├── relation name: why linked?
    │
    └── target profile: how to interpret target representation?
```

Example:

```json
{
  "iri:has-mount": {
    "href": "https://facility.example/api/v2/status/resources/frontier-orion-scratch-mount",
    "profile": "https://iri.science/profiles/resource-definition/storage/mount"
  }
}
```

---

### 10. OpenAPI

OpenAPI answers:

> **What is the machine-readable structural contract of the API and its representations?**

OpenAPI governs the API surface and representation structure, including schema-level constraints.

It does **not** replace the registry or profile model.

OpenAPI and the registry solve different problems:

| Concern | Primary source |
|---|---|
| API path and schema structure | OpenAPI |
| Resource classification | Resource Type URNs |
| Type-specific semantics | Resource Definition Profiles |
| Controlled identifiers | Registered URNs |
| Link semantics | Link Relation Registry |
| Target representation semantics | Target profiles |

The combined model is what makes IRI both machine-validated and semantically interoperable.

## End-to-end interpretation flow

A generic client can interpret a Resource using this sequence:

```text
1. Receive Resource
2. Validate structure against OpenAPI / schema
3. Read resource_type
4. Resolve or recognize the registered Resource Type
5. Apply the selected Resource Definition Profile
6. Interpret attributes using that profile
7. Interpret any registered URNs used in attributes
8. Inspect _links
9. Interpret each relation using the Link Relation Registry
10. Follow target href when needed
11. Apply target profile semantics if provided
12. Retrieve the applicable deployed service-desc when a machine-readable contract is needed
```

## Worked conceptual example

```json
{
  "resource_id": "orion",
  "resource_type": "urn:doe-iri:resource:storage:filesystem",
  "attributes": {
    "storage_technology": "urn:doe-iri:attribute:storage-technology:lustre",
    "media_types": [
      "urn:doe-iri:attribute:media-type:nvme"
    ]
  },
  "_links": {
    "self": {
      "href": "https://facility.example/api/v2/status/resources/orion"
    },
    "iri:has-mount": {
      "href": "https://facility.example/api/v2/status/resources/frontier-orion-scratch-mount",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    },
    "service-desc": {
      "href": "https://facility.example/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

Interpretation:

1. The object is structurally an IRI Resource.
2. `resource_type` says it is a storage filesystem resource.
3. The corresponding Resource Definition Profile provides the type-specific semantics.
4. `attributes.storage_technology` and `attributes.media_types` use registered controlled URNs.
5. `_links["iri:has-mount"]` expresses a registered relationship to a mount representation.
6. The target `profile` tells the client how to interpret that mount representation.
7. `service-desc` advertises the applicable deployed OpenAPI service description.

## Common mistakes to avoid

### Mistake 1: Treating `resource_type` as if it were the full semantic definition

`resource_type` classifies the resource, but the detailed type semantics come from the corresponding Resource Definition Profile.

---

### Mistake 2: Treating a link relation as a target profile

A relation tells the client **why** the link exists. A profile tells the client **how to interpret** the linked representation.

---

### Mistake 3: Treating OpenAPI as the only semantic authority

OpenAPI defines structure. The registry and profiles define important shared semantics beyond structural schema validation.

---

### Mistake 4: Using local string conventions where a registered URN should be used

When a controlled semantic identifier exists, use the registered URN rather than inventing a facility-local value.

---

### Mistake 5: Making clients infer paths

Clients should prefer `_links` and advertised service descriptions rather than guessing facility-specific URLs.

## Summary

The IRI Resource model intentionally separates structure, type classification, type-specific semantics, controlled identifiers, and hypermedia semantics:

```text
OpenAPI
  └── defines structural API contract

Resource
  ├── resource_type
  │     └── selects Resource Definition semantics
  ├── attributes
  │     └── may use registered URNs
  └── _links
        ├── relation names defined by Link Relation Registry
        └── targets may carry profiles describing target semantics
```

That separation is what allows IRI to support heterogeneous facilities while preserving a shared, portable client model.

## Related pages

- [Core Concepts](core-concepts.md)
- [IRI Architecture](architecture.md)
- [IRI 2.0](iri-2.0.md)
- [Hypermedia and Discovery](hypermedia-and-discovery.md)
- [IRI Registry](registry.md)
- [Implementation Guide](implementation-guide.md)
