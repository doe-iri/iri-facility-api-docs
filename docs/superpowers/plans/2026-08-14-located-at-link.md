# `iri:located-at` Link Relationship Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Register `iri:located-at` and add it consistently to DOE-IRI registry indexes, the common Resource contract, and complete Resource examples.

**Architecture:** Add one generic provisional Resource-to-Site HAL link-relation definition. Preserve required `site_uri` as the compatibility field, require equality whenever the new singular link is present, and index the relation across the Storage, Compute, and Service domains without changing domain-specific topology semantics.

**Tech Stack:** Markdown registry documents, OpenAPI-compatible YAML, JSON/HAL examples, and shell-based consistency checks.

**Spec:** `docs/superpowers/specs/2026-08-14-located-at-link-design.md`

## Global Constraints

- Register the exact relation name `iri:located-at` with lifecycle `provisional`.
- Source is any DOE-IRI `Resource`; target is the associated Facility API `Site` representation.
- The current semantic cardinality is exactly one because `site_uri` is required and singular.
- Retain `site_uri`; whenever `_links["iri:located-at"]` is present, its `href` MUST exactly equal `site_uri`.
- The target is a Site API representation, not a DOE-IRI typed `Resource`, state object, operation entry point, or relationship resource.
- Keep `iri:located-at` distinct from service-to-compute `iri:hosted-on`.
- Do not add an inverse relation, deprecate `site_uri`, change the Site schema, or invent authorization-filtered absence that contradicts visible `site_uri`.
- Preserve unrelated user changes and follow the repository's existing link-relation-definition and index formats.
- Use `registry_editor` for implementation and `registry_maintainer` for deterministic validation.

---

### Task 1: Register the Relation and Update Resource Examples

**Files:**
- Create: `registry/relations/located-at.md`
- Modify: `registry/README.md`
- Modify: `registry/urn-registry-type-storage.md`
- Modify: `registry/urn-registry-type-storage-taxonomy.md`
- Modify: `registry/urn-registry-type-compute.md`
- Modify: `registry/urn-registry-type-compute-taxonomy.md`
- Modify: `registry/urn-registry-type-service.md`
- Modify: `registry/urn-registry-type-service-taxonomy.md`
- Modify: `specification-v2/openapi/production/_components.yaml`
- Modify: `specification-v2/openapi/all_spec_v2.yaml`
- Modify: `rfc/rfc-type-specific-attributes.md`
- Modify: `registry/urn-registry-attributes-service-dtn.md`
- Modify: `registry/examples/hpc-facility-resources.json`
- Modify: `docs/ai-project-context.md`

**Interfaces:**
- Consumes: Required and singular `Resource.site_uri`, Site `self_uri`, and the approved design specification.
- Produces: A discoverable link-relation definition and examples whose `iri:located-at.href` values equal their enclosing Resource's `site_uri`.

- [ ] **Step 1: Run the failing contract checks**

```bash
test -e registry/relations/located-at.md
jq -e 'all(.[]; ._links["iri:located-at"].href == .site_uri)' registry/examples/hpc-facility-resources.json
```

Expected: both checks fail because the profile and links do not yet exist.

- [ ] **Step 2: Create the complete link-relation definition**

Follow the established link-relation metadata format and include the exact
source, target, cardinality, stability, authorization, classification,
compatibility, non-implication, and singular HAL example decisions from the
design specification.

- [ ] **Step 3: Add the relation to registry navigation and domain indexes**

Add a generic/core relationship entry to `registry/README.md`, plus compatible
rows in the Storage, Compute, and Service registry and taxonomy relationship
tables. Link every row to `relations/located-at.md` and preserve each table's
existing column format.

- [ ] **Step 4: Document the additive common-Resource contract**

Update the `site_uri` descriptions in both OpenAPI artifacts and the common
Resource discussion in `rfc/rfc-type-specific-attributes.md`. State that
`site_uri` remains required and authoritative and that a present
`iri:located-at` href must equal it. Do not make `_links` required in the current
OpenAPI schema.

- [ ] **Step 5: Update complete Resource examples**

Add singular `iri:located-at` link objects to all eight objects in
`registry/examples/hpc-facility-resources.json`, the complete DTN Resource
example, and both complete Resource examples in the type-specific-attributes
RFC. Preserve existing links and ensure every added href exactly equals the
same object's `site_uri`.

- [ ] **Step 6: Record the architectural decision**

Append a concise dated section to `docs/ai-project-context.md` capturing the
relation semantics, compatibility rule, and distinction from `iri:hosted-on`.

- [ ] **Step 7: Run focused verification**

```bash
test -e registry/relations/located-at.md
jq -e 'length == 8 and all(.[]; ._links["iri:located-at"].href == .site_uri)' registry/examples/hpc-facility-resources.json
cmp <(sed -n '998,1076p' specification-v2/openapi/production/_components.yaml) <(sed -n '998,1076p' specification-v2/openapi/all_spec_v2.yaml)
git diff --check
```

Expected: all commands succeed.

---

### Task 2: Deterministic Registry Validation

**Files:**
- Validate: all files changed by Task 1

**Interfaces:**
- Consumes: Registered relation, indexes, common contract wording, and examples from Task 1.
- Produces: Evidence that links, indexes, JSON, YAML, and compatibility invariants are mechanically consistent.

- [ ] **Step 1: Validate JSON and YAML syntax**

Parse the HPC JSON document and both OpenAPI YAML documents with available
repository-compatible parsers.

- [ ] **Step 2: Validate relation invariants**

Confirm all eight HPC resources have singular `iri:located-at` objects whose
only required member is `href`, and that every href equals `site_uri`. Confirm
the complete RFC and DTN examples make the same equality claim.

- [ ] **Step 3: Validate registry synchronization**

Confirm the new profile is linked from the central README and all six domain
registry/taxonomy documents, with consistent lifecycle, source, target,
cardinality, target classification, target stability, and authorization
semantics.

- [ ] **Step 4: Check relative Markdown links and diff hygiene**

Resolve every relative Markdown link in changed registry documents, run
`git diff --check`, and review the complete diff for unrelated changes.
