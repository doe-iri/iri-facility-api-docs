---
layout: default
title: Examples
parent: IRI 2.0
nav_order: 5
permalink: /examples/
---

# Examples

These examples illustrate how the IRI concepts fit together. They are not normative schemas.

For exact fields, required properties, relation semantics, and allowed identifiers, consult the applicable specification, OpenAPI contract, and registry.

## Example 1: Discovering a related mount

```json
{
  "resource_id": "frontier",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "_links": {
    "self": {
      "href": "https://facility.example/api/v2/status/resources/frontier"
    },
    "iri:has-mount": {
      "href": "https://facility.example/api/v2/status/resources/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch storage",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    }
  }
}
```

Traversal:

```text
compute resource
      │
      │ iri:has-mount
      ▼
mount relationship resource
```

The client follows the advertised `href`; it does not construct the mount URL from the compute resource ID.

## Example 2: Discovering the API description

```json
{
  "_links": {
    "service-desc": {
      "href": "https://facility.example/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

A client that needs the machine-readable API contract can retrieve the advertised service description.

## Example 3: Resource classification and profile interpretation

```text
resource_type
   │
   └── urn:doe-iri:resource:compute:system
                     │
                     ▼
          Resource Definition semantics
```

The Resource Type URN and Resource Definition Profile are separate identifiers with separate purposes.

See [IRI Registry](registry.md).

## Example 4: Portable client behavior

Avoid client logic like:

```python
job_url = facility_base + "/api/v2/compute/jobs/" + resource_id
```

The problem is not the programming language; the problem is assuming a routing convention that is not part of the discovered representation.

Prefer the conceptual flow:

```python
resource = get_resource(resource_uri)
operation = find_registered_relation(resource, desired_relation)
target_uri = operation["href"]
```

The exact relation names and operation semantics must come from the governing IRI specification and registry.

## Example 5: Cross-facility traversal

```text
Facility A representation
        │
        │ registered relation
        ▼
advertised target
        │
        ▼
Facility or service endpoint
        │
        ├── target representation
        └── service-desc ──► OpenAPI
```

Because the URI is advertised, the target does not need to share the same hostname or path layout as the source representation.

## Authoritative references

- [IRI v2 OpenAPI](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi)
- [IRI Registry](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/README.md)
- [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations)
- [IRI RFCs](https://github.com/doe-iri/iri-facility-api-docs/tree/main/rfc)
