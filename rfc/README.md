![Department of Energy - Office of Science](../images/doe-logo.jpg)

# DoE IRI Requests for Comments (RFC)

Welcome to the DoE Integrated Research Infrastructure (IRI) RFC repository. This space serves as the central hub for the proposal, discussion, and archival of technical specifications, architecture decisions, and registry standards governing the IRI ecosystem.

## Purpose

The primary objective of this repository is to provide a transparent, version-controlled process for evolving IRI technical standards. By documenting proposed specifications as Requests for Comments (RFCs), we aim to:

  - **Establish Stability:** Define extensible, long-term identifiers and data models that decouple infrastructure evolution from client-side implementation.
  - **Ensure Interoperability:** Create shared governance for IRI-type namespaces, service definitions, and registration policies.
  - **Foster Consensus:** Facilitate collaborative review of technical designs, ensuring broad applicability across Department of Energy facilities.

## Scope

This repository contains documents that define the shared language and interaction patterns for the IRI project, including but not limited to:

  - **URN Namespace Definitions:** Specifications for stable, hierarchical identifiers (e.g., urn:doe-iri:*).
  - **Registry Standards:** Guidelines for maintaining canonical sets of types, service endpoints, and allocation units.
  - **Architectural RFCs:** Proposals for API evolution, cross-facility interoperability, and security considerations.

## Contribution Process

This repository follows an open RFC process. Community members and facility representatives are encouraged to:

  1. **Review Existing RFCs:** Examine active documentation and registry entries to understand current standards.
  2. **Propose Changes:** Use the Issue tracker to initiate discussions on new requirements or refinements to existing specifications.
  3. **Draft Proposals:** Contribute new RFC documents via Pull Request, following the established templates and requirements language (RFC 2119/8174).

For more information on the broader DoE IRI project, official reference implementations, and toolkits, please visit the main GitHub organization page.

## Status

| Title | Status | Date |
| --- | --- | --- |
| IRI URN Structure and Registry | Approved | June 15, 2026 |
| Type-Specific Attributes for IRI Resource Objects | Approved | August 7, 2026 |
| HAL \_links for the IRI Facility API | Approved | August 14, 2026 |
| Container Execution Capability Discovery for IRI Compute Systems | Draft / Proposed | August 14, 2026 |
| Normalized Queueing Policy Discovery for IRI Resources | Draft / Proposed | September 4, 2026 |
| Migrating Resource.supported_endpoints to HAL Operation Affordances | Draft / Proposed | September 9, 2026 |

## Contents

1. **[IRI URN Structure and Registry](./rfc-iri-urn-structure-and-registry.md)**: 

	This document outlines an extensible Uniform Resource Name (URN) structure for Department of Energy (DoE) Integrated Research Infrastructure (IRI) identifiers, designed to decouple data model stability from evolving type taxonomies. It provides guidelines for hierarchical identifier naming, registry management, and validation, facilitating interoperable resource and service typing without requiring frequent OpenAPI schema revisions.

2. **[Type-Specific Attributes for IRI Resource Objects](./rfc-type-specific-attributes.md)**:

	This document defines the semantics of `Resource.attributes` and how `resource_type` selects the applicable Resource Definition semantics. Resource Type URNs and Resource Definition Profile URIs are distinct identifiers. The current IRI v2 OpenAPI schema remains authoritative for the structural contract, including the optionality, nullability, JSON structure, and additional-properties behavior of `attributes`. The RFC specializes the existing IRI v2 `Resource` representation and does not introduce separate Resource Definition or Resource State API objects.

3. **[HAL `_links` for the IRI Facility API](./rfc-hal-links.md)**:

	This document defines an additive HAL `_links` convention for IRI v2 resource-oriented JSON representations. It makes related resources, topology relationships, operation entry points, and machine-readable service descriptions explicit and navigable; defines migration of existing navigable URI-valued properties to standard or registered DOE-IRI link relations; and advertises an initial job-submission affordance. OpenAPI remains authoritative for operation invocation, and the RFC does not change the production OpenAPI schemas.

4. **[Container Execution Capability Discovery for IRI Compute Systems](./rfc-container-capability-discovery.md)**:

	This document defines a read-only, structured capability-discovery contract for containerized workloads on IRI compute systems. It adds an optional `container_runtimes` attribute to the in-progress Compute System Resource Definition Profile describing accepted runtimes and image formats, direct registry pull versus required pre-staging, registry policy and private-registry authentication model, execution identity and privilege policy, GPU integration, build availability, and CPU architecture. It reuses the type-specific `attributes` mechanism, the DOE-IRI URN registry, and HAL `_links`; it defines no new endpoint and no change to the `Container` job schema. A normalized image acquisition and reuse contract is deferred to a companion RFC.

5. **[Normalized Queueing Policy Discovery for IRI Resources](./rfc-normalized-queue-atttributes.md):**

    This document defines supplemental attributes for Resources that let a site describe what kind of queuing behavior exists for that resource and what the site policies are around it.

6. **[Migrating `Resource.supported_endpoints` to HAL Operation Affordances](./rfc-resource-operation-affordances.md)**:

	This document proposes replacing the broad `compute` and `filesystem` categories in `Resource.supported_endpoints` with Resource-specific HAL links to operation entry points. It maps all 25 Resource-scoped compute, filesystem, and storage operations in the reviewed IRI v2 OpenAPI contract to existing or proposed DOE-IRI link relations; defines applicability, authorization visibility, URI-template, and invocation rules; and describes a phased add, deprecate, and retire migration. OpenAPI remains authoritative for operation methods and payloads, and the RFC does not itself register the proposed relations or change the production schema.
