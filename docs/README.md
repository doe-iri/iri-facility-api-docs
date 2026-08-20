# IRI Documentation Guide

This directory contains non-normative architectural context and decision rationale for the DOE Integrated Research Infrastructure (IRI) Facility API documentation repository.

## Source-of-truth model

Current normative and structural authority remains outside this directory and is resolved by concern:

| Concern | Authoritative source |
|---|---|
| API structure, properties, required/nullable rules, formats, and operation shapes | `specification-v2/openapi/` |
| DOE-IRI URN syntax, hierarchy, delegation, registration procedure, and conformance | Governing URN RFCs under `rfc/` |
| Assigned Resource Type and controlled-value URNs | `registry/urns/` |
| Registered `iri:*` relation names and complete relation semantics | `registry/relations/` |
| HAL wire conventions and URI-property migration | `rfc/rfc-hal-links.md` |
| Common Resource semantics | `registry/profiles/status/resource.md` |
| Type-specific Resource semantics selected by `resource_type` | `registry/profiles/resource-definition/` |
| Other representation-specific semantics | Other documents under `registry/profiles/` |

Documents under `docs/` do not override those sources.

## Directory structure

```text
docs/
├── README.md
├── ai-project-context.md
└── decisions/
    ├── README.md
    ├── _template.md
    ├── 0001-service-resource-boundaries.md
    ├── 0002-delegated-extension-governance.md
    ├── 0003-hal-hypermedia-model.md
    ├── 0004-link-relation-naming.md
    └── 0005-location-vs-hosting.md
```

### `ai-project-context.md`

Broad architectural and historical context. It may explain project evolution, but it is not a normative source.

### `decisions/`

Curated records of accepted architectural decisions and the rationale behind them. A decision record explains **why** the repository adopted a model; the current RFC, registry, relation, profile, or OpenAPI source defines **what is currently required**.

If a decision record conflicts with a current authoritative source, the authoritative source wins and the decision record should be updated, superseded, or marked historical.

## What does not belong here

Do not retain transient AI/Codex execution plans, one-time migration instructions, scratch analyses, command transcripts, or generated implementation checklists as durable repository documentation after the work is complete.

Git history provides the implementation record. Durable rationale should be distilled into a decision record only when it remains useful to future maintainers.
