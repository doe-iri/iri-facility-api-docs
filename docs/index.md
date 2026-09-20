---
layout: default
title: Home
nav_order: 1
permalink: /
---

![Department of Energy - Office of Science](assets/images/doe-logo.jpg)

# DOE Integrated Research Infrastructure<br>Facility API Documentation

The U.S. Department of Energy (DOE) Integrated Research Infrastructure (IRI) is an effort to enable researchers and scientific workflows to use resources and services across DOE facilities through interoperable interfaces.

This documentation site is the **human-oriented guide** to the IRI Facility API. It explains the architecture, core concepts, discovery model, registry, and implementation approach, and then links to the authoritative specifications and registry content maintained in the [`iri-facility-api-docs`](https://github.com/doe-iri/iri-facility-api-docs) repository.

> **Documentation status**
>
> This site provides explanatory and implementation guidance. Normative IRI requirements are defined by the versioned specifications, RFCs, registries, profiles, and OpenAPI documents in the main documentation repository.

## Start here

| If you are... | Start with... |
|---|---|
| New to IRI Facility APIs | [IRI Architecture](architecture.md) |
| Interested in IRI v2 architecture changes | [Making IRI Facility Capabilities Discoverable](resource-architecture-overview.md)
| Implementing an IRI API at a facility | [Implementation Guide](implementation-guide.md) |
| Building an IRI client | [Getting Started](getting-started.md) |
| Building an orchestrator, MCP server, or AI agent | [Hypermedia and Discovery](hypermedia-and-discovery.md) |
| Looking for the current v2 API definition | [IRI 2.0](iri-2.0.md) |
| Looking for an IRI URN, profile, or relationship | [IRI Registry](registry.md) |
| Proposing a design or registry change | [RFC Process](rfc-process.md) |
| Looking for representative resource flows | [Examples](examples.md) |

## Documentation model

The documentation is organized into four complementary layers:

```text
Documentation site
 │
 │  How does IRI work?
 │  How should I implement or use it?
 │
 ├───────────────┬────────────────┬────────────────┐
 ▼               ▼                ▼                ▼
Specification   Registry          RFCs          OpenAPI
Normative       Identifiers,      Design         Machine-
API behavior    profiles, and     proposals      readable
                relations                        contract
```

The documentation site should explain concepts and workflows. It should **not** duplicate normative definitions from the repository.

## IRI Facility API model

At a high level, IRI clients discover facility resources and then follow advertised relationships and operation entry points instead of depending on facility-specific URL construction.

```text
                 ┌────────────────────────┐
                 │       IRI Client       │
                 │ Workflow / AI / MCP    │
                 └────────────┬───────────┘
                              │
                       Discover / Navigate
                              │
                 ┌────────────▼───────────┐
                 │   IRI Facility APIs    │
                 ├────────────────────────┤
                 │ Resource descriptions  │
                 │ Dynamic state          │
                 │ Relationships          │
                 │ Operation entry points │
                 └────────────┬───────────┘
                              │
                ┌─────────────┼──────────────┐
                │             │              │
                ▼             ▼              ▼
          Specifications   Registry         RFCs
```

See [Hypermedia and Discovery](hypermedia-and-discovery.md) for the detailed model.

## Authoritative documentation

### Specifications

- [IRI Specification 2.0](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2) — current v2 development line; currently marked **Draft** in the repository.
- [IRI Specification 1.0](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v1) — v1 documentation and design material.

### IRI Registry

- [Registry overview](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/README.md)
- [URN Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/urns)
- [Resource Definition Profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles)
- [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations)

### Requests for Comments

- [IRI RFC index](https://github.com/doe-iri/iri-facility-api-docs/tree/main/rfc)

### OpenAPI

- [IRI v2 OpenAPI sources](https://github.com/doe-iri/iri-facility-api-docs/tree/main/specification-v2/openapi)
- **Authoritative repository source:** [`specification-v2/openapi/all_spec_v2.yaml`](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/all_spec_v2.yaml)
- **Intended canonical publication URI:** `https://iri.science/api/v2/openapi.json`

Facility deployments normally publish their own OpenAPI descriptions and expose
those deployed contracts through `service-desc`. The canonical publication URI
defines the IRI v2 contract; it is not automatically a facility deployment's
service description.

## Key principles

The Facility API documentation is easier to understand when viewed through a few recurring design principles:

1. **Portable clients** — clients should not require facility-specific URL construction rules.
2. **Typed resources** — resource representations identify their semantic type using registered IRI identifiers.
3. **Registered semantics** — shared resource types, controlled values, profiles, and link relations are governed through the IRI Registry.
4. **Discoverable relationships and operations** — representations may advertise related resources and operation entry points using typed links.
5. **Machine-readable contracts** — OpenAPI defines the structural API contract while profiles and registry entries define additional semantics.
6. **Version-controlled governance** — normative changes are reviewed in the main Git repository through issues, RFCs, and pull requests.

## Where to go next

A first-time reader should continue with [IRI Architecture](architecture.md), followed by [Core Concepts](core-concepts.md) and [Hypermedia and Discovery](hypermedia-and-discovery.md).
