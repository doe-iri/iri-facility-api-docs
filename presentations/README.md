# Presentations

This directory contains presentations about the DOE Integrated Research
Infrastructure (IRI), its interfaces, and the evolution of the Facility API.
The presentations are informational snapshots from the dates shown; the
current OpenAPI specification, RFCs, registries, and profiles remain the
authoritative sources for the API and its semantics.

## Presentation Index

- [SC24 BoF: IRI Interfaces - November, 2024](<SC24_BoF_IRI_Interfaces.pdf>): Introduces the
  IRI vision and Interfaces Charter through the question of what new interfaces
  HPC facilities should expose for cross-facility workflows. It discusses
  API-based alternatives to traditional shell access and examples including the
  NERSC Superfacility API, Globus Flows, and FirecREST.

- [IRI API Deployment Models - February 6, 2025](<2025.02.06 - IRI API deployment models.pdf>):
  Compares deployment approaches for Facility API servers, centralized
  discovery, and function execution across multiple facilities. It also covers
  IRI-token authentication and facility-level policy enforcement.

- [SC25 BoF: IRI Interfaces at Work - November, 2025](<SC25_BoF_IRI_interfaces.pdf>): Reviews
  prototypes, implementation progress, and community feedback from the IRI
  Interfaces Technical Subcommittee. Topics include facility and status APIs,
  authenticated job and file operations, and FirecREST v2 for HPC and AI
  workflows.

- [Genesis of IRI - April 25, 2026](<2026.04.25 - Genesis-IRI.pdf>): Provides
  an introduction to IRI and its goal of creating unified interfaces across DOE
  ASCR facilities. It summarizes the development process, IRI v1 facility
  resources, job submission and filesystem operations, and the roadmap toward
  v2.

- [IRI v2.0 Proposed Changes - July 30, 2026](<2026.07.30 - IRI v2.0 Proposed Changes.pdf>):
  Records a proposal-stage discussion of changes to the IRI data model,
  including URN-based object types, type-specific attributes, HAL `_links`, and
  concepts derived from the American Science Cloud Resource Card. Some ideas in
  this presentation predate the current v2 architecture and should be read as
  historical proposals.

- [IRI Resource Architecture Overview - August 21, 2026](<2026.08.21 - iri-resource-architecture-overview.pdf>):
  Explains the self-describing IRI Resource model used to make facility
  capabilities discoverable to people, software clients, and agents. It covers
  `resource_type` URNs, profile-governed `attributes`, HAL `_links` and relation
  definitions, and OpenAPI operation contracts.

- [IRI Resource Operation Affordances - September 17, 2026](<2026.09.17 - IRI Resource Operation Affordances.pdf>):
  Proposes how IRI v2 Resource representations can advertise operation-specific
  applicability and invocation locations through HAL links while keeping the
  deployed OpenAPI document authoritative for methods, schemas, security, and
  responses. It also describes `x-iri-relation` bindings, caller-specific link
  visibility and omission semantics, client resolution behavior, and an
  additive migration from `supported_endpoints`.
