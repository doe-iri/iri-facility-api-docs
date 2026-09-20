---
layout: default
title: Getting Started
nav_order: 2
permalink: /getting-started/
---

# Getting Started

This page provides entry points for the most common IRI Facility API audiences.

> Normative requirements are defined in the [iri-facility-api-docs](https://github.com/doe-iri/iri-facility-api-docs) repository. This site explains how the pieces fit together.

## Before you begin

Become familiar with three concepts:

1. An IRI **Resource** represents a facility resource that can be described and discovered.
2. `resource_type` identifies what kind of resource is being represented.
3. Typed links can advertise relationships, related state, and operation entry points.

Read [Core Concepts](core-concepts.md) for the terminology and [Hypermedia and Discovery](hypermedia-and-discovery.md) for the traversal model.

## I am implementing IRI at a facility

Recommended path:

1. Review [IRI Architecture](architecture.md).
2. Review the [IRI 2.0 specification](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2).
3. Review the [v2 OpenAPI definition](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi).
4. Identify the IRI Resource Types your facility will expose using the [Resource Type registry](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md).
5. Review applicable [Resource Definition Profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles/resource-definition).
6. Review the [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations).
7. Implement and validate the API using the guidance in [Implementation Guide](implementation-guide.md).

A facility implementation should use the registered semantics rather than creating local meanings for shared IRI identifiers.

## I am building an IRI client

A client should be designed around representations and advertised links rather than hard-coded facility URL layouts.

Recommended path:

1. Retrieve a known or discovered IRI resource representation.
2. Inspect `resource_type`.
3. Interpret the common resource representation.
4. Apply the Resource Definition Profile associated with that type when needed.
5. Inspect `_links` for available relationships and operation entry points.
6. Follow the advertised URI rather than constructing a URI from assumed path templates.
7. Use an advertised service description, when provided, to obtain the applicable machine-readable API contract.

See [Hypermedia and Discovery](hypermedia-and-discovery.md).

## I am building a workflow orchestrator, MCP server, or AI agent

Treat IRI representations as the authoritative source of navigational information available at runtime.

The preferred pattern is:

```text
Discover resource
      │
      ▼
Inspect representation
      │
      ├── resource_type ──► semantic interpretation
      │
      └── _links ─────────► available traversal / operations
                                │
                                ▼
                         follow advertised URI
```

An agent should not guess a path such as `/jobs/{resource_id}` simply because another facility uses that structure. If the operation is discoverable through a registered relation, use the advertised target.

## I am reviewing or proposing specification changes

Start with the [RFC Process](rfc-process.md).

Use the repository's issue and pull-request workflow for normative changes. This site should document adopted concepts but should not become a second standards-development channel.

## Suggested reading order

1. [IRI Architecture](architecture.md)
2. [Core Concepts](core-concepts.md)
3. [IRI 2.0](iri-2.0.md)
4. [Hypermedia and Discovery](hypermedia-and-discovery.md)
5. [IRI Registry](registry.md)
6. [Implementation Guide](implementation-guide.md)
7. [Examples](examples.md)
