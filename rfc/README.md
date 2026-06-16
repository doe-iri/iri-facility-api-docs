![Department of Energy - Office of Science](../images/doe-logo.jpg)

# DoE IRI Requests for Comments (RFC)

Welcome to the DoE Integrated Research Infrastructure (IRI) RFC repository. This space serves as the central hub for the proposal, discussion, and archival of technical specifications, architecture decisions, and registry standards governing the IRI ecosystem.

## Purpose

The primary objective of this repository is to provide a transparent, version-controlled process for evolving IRI technical standards. By documenting proposed specifications as Requests for Comments (RFCs), we aim to:

  - **Establish Stability:** Define extensible, long-term identifiers and data models that decouple infrastructure evolution from client-side implementation.
  - **Ensure Interoperability:** Create shared governance for IRI-type namespaces, service definitions, and registration policies.
  - **Foster Consensus: **Facilitate collaborative review of technical designs, ensuring broad applicability across Department of Energy facilities.

## Scope

This repository contains documents that define the shared language and interaction patterns for the IRI project, including but not limited to:

  - **URN Namespace Definitions:** Specifications for stable, hierarchical identifiers (e.g., urn:doe-iri:*).
  - **Registry Standards:** Guidelines for maintaining canonical sets of types, service endpoints, and allocation units.
  - **Architectural RFCs:** Proposals for API evolution, cross-facility interoperability, and security considerations.

## Contribution Process

This repository follows an open RFC process. Community members and facility representatives are encouraged to:

  1. **Review Existing RFCs: **Examine active documentation and registry entries to understand current standards.
  2. **Propose Changes:** Use the Issue tracker to initiate discussions on new requirements or refinements to existing specifications.
  3. **Draft Proposals:** Contribute new RFC documents via Pull Request, following the established templates and requirements language (RFC 2119/8174).

For more information on the broader DoE IRI project, official reference implementations, and toolkits, please visit the main GitHub organization page.

## Contents

1. **[IRI URN Structure and Registry](./rfc-iri-urn-structure-and-registry.md)**: 
This document outlines an extensible Uniform Resource Name (URN) structure for Department of Energy (DoE) Integrated Research Infrastructure (IRI) identifiers, designed to decouple data model stability from type taxonomy evolution. It provides guidelines for hierarchical identifier naming, registry management, and validation, facilitating interoperable resource and service typing without requiring frequent OpenAPI schema revisions.
