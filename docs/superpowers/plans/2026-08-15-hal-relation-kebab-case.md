# DOE-IRI HAL Relation Kebab-Case Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace every registered multiword DOE-IRI custom HAL relation identifier with its lowercase kebab-case spelling across the registry, RFCs, OpenAPI descriptions, examples, and active supporting documentation.

**Architecture:** The Link Profile Index and individual profiles are migrated first as the authoritative registry layer. RFC, OpenAPI-description, example, context, and historical design consumers then adopt those exact names. A final cross-document validation proves lexical consistency without changing relation semantics or unrelated identifiers.

**Tech Stack:** Markdown, JSON, OpenAPI YAML, Ruby validation scripts, ripgrep, Git diff checks.

**Spec:** `docs/superpowers/specs/2026-08-14-hal-relation-kebab-case-design.md`

## Global Constraints

- Apply only the 21 exact relation conversions in the approved design; `iri:impacts` remains unchanged.
- DOE-IRI custom relation identifiers use lowercase ASCII letters, digits, and hyphens; multiword names use hyphens.
- Do not add aliases, deprecated duplicate relations, or simultaneous camelCase/kebab-case registrations.
- Do not change resource or controlled-value URNs, JSON property names, API paths, OpenAPI `operationId` values, standard Web Linking relations, or programming-language symbols merely because they are camelCase.
- Do not change relationship semantics, direction, source or target type, cardinality, lifecycle, stability, target classification, authorization, or visibility.
- Do not rename link-profile files; all existing profile filenames already conform.
- Preserve the current dirty working tree in place. Do not reset, restore from `HEAD`, stage, commit, or overwrite unrelated edits.
- The approved migration design and this plan may retain former identifiers only in explicit former-to-canonical migration tables.
- Ignore historical runtime reports beneath `.superpowers/`; do not edit another plan's SDD workspace.

---

### Task 1: Migrate the Authoritative Registry and Examples

**Files:**

- Modify: `registry/link-profile-root.md`
- Modify: all 22 existing `registry/link-profile-*.md` relation profiles
- Modify: `registry/README.md`
- Modify: `registry/examples/hpc-facility-resources.json`
- Modify: `registry/urn-registry-type-storage.md`
- Modify: `registry/urn-registry-type-storage-taxonomy.md`
- Modify: `registry/urn-registry-type-compute.md`
- Modify: `registry/urn-registry-type-compute-taxonomy.md`
- Modify: `registry/urn-registry-type-service.md`
- Modify: `registry/urn-registry-type-service-taxonomy.md`
- Modify: affected files matching `registry/urn-registry-attributes-*.md`

**Interfaces:**

- Consumes: The exact lexical mapping below and the existing registered relation semantics.
- Produces: One authoritative index containing 21 kebab-case multiword relations plus unchanged `iri:impacts`, with every linked profile and registry example using the same names.

- [x] **Step 1: Run the failing registry naming contract**

Run:

```bash
rg -n 'iri:[A-Za-z0-9_-]*[A-Z][A-Za-z0-9_-]*' registry
```

Expected: nonzero output containing the existing 21 camelCase registered relation names.

- [x] **Step 2: Apply the exact registry mapping**

Apply only these complete-string substitutions wherever they denote DOE-IRI custom relations in `registry/**`:

```text
iri:accessesMount        -> iri:accesses-mount
iri:attachedTo           -> iri:attached-to
iri:generatedBy          -> iri:generated-by
iri:hasCPU               -> iri:has-cpu
iri:hasCapability        -> iri:has-capability
iri:hasEvent             -> iri:has-event
iri:hasGPU               -> iri:has-gpu
iri:hasMount             -> iri:has-mount
iri:hasNode              -> iri:has-node
iri:hasProject           -> iri:has-project
iri:hasProjectAllocation -> iri:has-project-allocation
iri:hasResource          -> iri:has-resource
iri:hasSite              -> iri:has-site
iri:hostedOn             -> iri:hosted-on
iri:locatedAt            -> iri:located-at
iri:mayImpact            -> iri:may-impact
iri:mountedOn            -> iri:mounted-on
iri:providesBlock        -> iri:provides-block
iri:providesFilesystem   -> iri:provides-filesystem
iri:providesObject       -> iri:provides-object
iri:submitJob            -> iri:submit-job
```

Use an exact literal mapping, not a general camelCase transformation. Preserve all surrounding prose and formatting.

- [x] **Step 3: Verify registry structure and examples**

Run:

```bash
! rg -n 'iri:[A-Za-z0-9_-]*[A-Z][A-Za-z0-9_-]*' registry
jq empty registry/examples/hpc-facility-resources.json
git diff --check -- registry
```

Then verify programmatically that:

- the index has exactly 22 relation rows;
- every local name matches `^[a-z0-9]+(?:-[a-z0-9]+)*$`;
- `iri:impacts` appears exactly once;
- every index profile link resolves;
- every one of the 22 profile headings and metadata rows matches its index relation;
- each `_links["iri:located-at"].href` equals the representation's `site_uri` wherever both appear in the HPC example.

Expected: all checks pass with no registry camelCase relation identifiers.

---

### Task 2: Migrate RFC, OpenAPI, and Supporting Documentation Consumers

**Files:**

- Modify: `rfc/rfc-hal-links.md`
- Modify: `rfc/rfc-type-specific-attributes.md`
- Modify: `specification-v2/openapi/production/_components.yaml`
- Modify: `specification-v2/openapi/all_spec_v2.yaml`
- Modify: `docs/ai-project-context.md`
- Modify: `docs/superpowers/plans/2026-08-13-service-resource-types.md`
- Modify: `docs/superpowers/plans/2026-08-14-hal-links-rfc.md`
- Modify: `docs/superpowers/plans/2026-08-14-located-at-link.md`
- Modify: `docs/superpowers/specs/2026-08-13-service-resource-types-design.md`
- Modify: `docs/superpowers/specs/2026-08-14-hal-links-rfc-design.md`
- Modify: `docs/superpowers/specs/2026-08-14-located-at-link-design.md`
- Preserve: `docs/superpowers/specs/2026-08-14-hal-relation-kebab-case-design.md`
- Preserve: `docs/superpowers/plans/2026-08-15-hal-relation-kebab-case.md`

**Interfaces:**

- Consumes: The canonical names registered by Task 1.
- Produces: Governing naming rules and all active RFC/OpenAPI/design consumers aligned with the authoritative index.

- [x] **Step 1: Run the failing consumer naming contract**

Run:

```bash
rg -n 'iri:[A-Za-z0-9_-]*[A-Z][A-Za-z0-9_-]*' rfc specification-v2 docs
```

Expected: matches in active RFC, v2 OpenAPI description, context, and earlier design/plan documents, plus the intentional former-name migration tables.

- [x] **Step 2: Apply the exact consumer mapping**

Apply the same 21 complete-string substitutions from Task 1 to the Task 2 modify-list only. Do not rewrite the approved migration design or this plan, where former spellings are retained intentionally in migration tables.

In `docs/superpowers/specs/2026-08-14-hal-links-rfc-design.md`, rephrase the two rejected, unregistered camelCase CURIE-like examples as prose referring to generic compute-API and filesystem-API relations. Do not register either concept.

- [x] **Step 3: Add the single normative naming rule**

In Section 4, “Authoritative Relation Sources,” of `rfc/rfc-hal-links.md`, add:

```text
DOE-IRI custom link relation identifiers MUST use lowercase ASCII letters,
digits, and hyphens. Multiword relation identifiers MUST separate words with
a hyphen (`-`). DOE-IRI custom relation identifiers MUST NOT use camelCase,
PascalCase, underscores, or whitespace.
```

Immediately clarify that the rule does not apply to JSON property names, DOE-IRI URNs, OpenAPI `operationId` values, API paths, programming-language symbols, or standard registered Web Linking relations. Do not duplicate the rule in registry pages or individual profiles.

- [x] **Step 4: Validate RFC, OpenAPI, and consumer documents**

Run:

```bash
git diff --check -- rfc specification-v2 docs
```

Parse every complete JSON/YAML fence in the two RFCs and affected design/plan documents. Parse both v2 OpenAPI YAML files. Confirm the production component description and consolidated artifact both say `iri:located-at`, while `operationId: launchJob` and `/api/v2/compute/job/{resource_id}` remain unchanged.

Search the Task 2 modify-list for uppercase `iri:*` identifiers. Expected: none. The only active-tree matches may be the explicit former-name migration tables in the approved migration design and this implementation plan.

---

### Task 3: Integrated Semantic and Mechanical Validation

**Files:**

- Validate: all files modified by Tasks 1 and 2
- Preserve: every unrelated file and ignored SDD workspace

**Interfaces:**

- Consumes: The canonical registry from Task 1 and aligned consumers from Task 2.
- Produces: Evidence that the repository has one canonical spelling per relation and no semantic or unrelated-identifier drift.

- [x] **Step 1: Verify old-name containment**

Search explicitly for every former identifier from the approved mapping. Expected: occurrences only in the former-name columns of:

```text
docs/superpowers/specs/2026-08-14-hal-relation-kebab-case-design.md
docs/superpowers/plans/2026-08-15-hal-relation-kebab-case.md
```

Run the uppercase heuristic repository-wide, excluding `.git/` and ignored `.superpowers/` runtime reports, and inspect every match.

- [x] **Step 2: Validate the complete registered relation set**

Verify that `registry/link-profile-root.md` contains exactly these canonical relations and no others:

```text
iri:accesses-mount
iri:attached-to
iri:generated-by
iri:has-capability
iri:has-cpu
iri:has-event
iri:has-gpu
iri:has-mount
iri:has-node
iri:has-project
iri:has-project-allocation
iri:has-resource
iri:has-site
iri:hosted-on
iri:impacts
iri:located-at
iri:may-impact
iri:mounted-on
iri:provides-block
iri:provides-filesystem
iri:provides-object
iri:submit-job
```

Confirm every relation has one index row, one profile heading, and one profile metadata registration, and that all index links resolve.

- [x] **Step 3: Validate protected identifiers and semantics**

Inspect the complete diff and confirm there are no changes to:

- `urn:doe-iri:*` values;
- JSON property names;
- standard relations `self`, `help`, `monitor`, and `service-desc`;
- API paths or OpenAPI `operationId` values;
- relationship meaning, direction, source/target types, cardinality, lifecycle, stability, target classification, authorization, or visibility;
- profile filenames.

- [x] **Step 4: Run final parsers and repository checks**

Parse all affected fenced JSON/YAML blocks, the HPC JSON example, and both v2 OpenAPI YAML files. Resolve affected relative Markdown links. Run:

```bash
git diff --check
git status --short
```

Expected: no parser, link, or whitespace failures, and only the approved existing dirty-tree files plus this migration's design/plan and relation-name edits are visible.

---
