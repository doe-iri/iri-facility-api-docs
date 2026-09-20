---
layout: default
title: RFC Process
parent: IRI Registry
nav_order: 1
permalink: /rfc-process/
---

# RFC Process

IRI Requests for Comments provide a version-controlled mechanism for proposing, discussing, and documenting changes to shared IRI technical standards.

The authoritative RFC index is maintained in [`rfc/`](https://github.com/doe-iri/iri-facility-api-docs/tree/main/rfc).

## Purpose

The repository describes the RFC process as a mechanism for:

- establishing stable, extensible technical standards,
- promoting cross-facility interoperability, and
- building consensus through collaborative review.

## When an RFC is appropriate

Use an RFC when a change affects shared architecture or semantics, for example:

- a new cross-facility interaction pattern,
- a new identifier or registry governance rule,
- a change in how resources are modeled,
- a new class of link relation semantics,
- a significant compatibility or versioning decision, or
- a design change that affects multiple implementations.

A small correction to an already-defined registry entry or documentation typo may only require a pull request.

## Current RFC material

The repository currently tracks the following RFCs. The status shown in each
RFC and in the authoritative RFC index controls if either differs from this
summary.

| RFC | Current status |
|---|---|
| [IRI URN Structure and Registry](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-iri-urn-structure-and-registry.md) | Approved |
| [Type-Specific Attributes and Resource Definition Profiles](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-type-specific-attributes.md) | Approved |
| [HAL `_links` for the IRI Facility API](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-hal-links.md) | Approved |
| [Container Execution Capability Discovery](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-container-capability-discovery.md) | Approved |
| [Normalized Queueing Policy Discovery](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-normalized-queue-atttributes.md) | Draft / Proposed |
| [Resource Operation Affordances](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md) | Approved for IRI v2 Phase 1 |
| [IRI API Root Discovery and Implementation Conformance](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-iri-capability-discovery.md) | Draft / Proposed |

Approval of Resource Operation Affordances covers only the additive Phase 1
mapping. Deprecating or removing `Resource.supported_endpoints` requires a
separately approved revision. Queue discovery and API-root conformance remain
proposals and must not be treated as adopted contracts.

Always consult the [RFC index](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/README.md) for the current set.

## Suggested contribution flow

```text
Requirement / problem
        │
        ▼
GitHub issue / discussion
        │
        ▼
RFC draft
        │
        ▼
Review and revision
        │
        ▼
Consensus / disposition
        │
        ├──► specification change
        ├──► registry change
        └──► implementation guidance
```

## Normative language

The repository's RFC guidance calls for the established RFC 2119 / RFC 8174 requirements-language conventions when drafting normative requirements.

When using terms such as `MUST`, `SHOULD`, and `MAY`, use them deliberately and consistently with the governing RFC conventions.

## Documentation-site relationship

The documentation site is not the RFC review surface.

Once a concept is sufficiently established, the site can explain it in approachable language and link back to the governing RFC, specification, or registry entry.

That preserves a clean separation:

```text
RFC / specification / registry
          │
          │ authoritative
          ▼
  Documentation site
    explanatory
```
