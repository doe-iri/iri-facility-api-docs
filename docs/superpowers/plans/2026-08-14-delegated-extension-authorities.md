# Delegated Extension Authorities Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile the governing facility-extension rules with the Root Registry by making explicit `:ext:<authority>:` delegation the sole canonical model.

**Architecture:** The RFC owns grammar, hierarchy exceptions, registration procedure, validation, and compatibility. The Root Registry separately records stable authority-code reservations and exact parent-scope delegations; local suffix values are governed by the delegated authority without central leaf registration.

**Tech Stack:** Markdown specifications and registries, ABNF-style grammar, shell-based structural and cross-document validation.

**Spec:** `docs/superpowers/specs/2026-08-14-delegated-extension-authorities-design.md`

## Global Constraints

- The only canonical extension form is `<parent-prefix>:ext:<authority>:<local-path>`.
- `ext` is a lowercase non-semantic delegation marker that appears exactly once; authority codes express governance, not classification.
- Parent scope and authority code are registered separately; one authority reservation grants no scope automatically.
- The existing five authority codes remain active reservations, but no active scope is inferred from an unresolved scope cell.
- Direct facility-code forms are removed from canonical examples; no aliases are created without deployment evidence.
- Shared-parent fallback stops immediately before `ext`; structural prefixes ending in `:ext` or `:ext:<authority>` are not semantic types.
- Syntax validity, scope authorization, and locally documented meaning are
  distinct validation levels; an assigned DOE-IRI extension satisfies all
  three.
- Preserve the current user-owned RFC history row and `compute` domain addition exactly while integrating the new RFC changes.
- Do not modify or stage the concurrent root README or link-profile-index changes.
- Do not commit: the working tree contains overlapping user-owned RFC edits that must remain user-owned.
- Use `registry_editor` for implementation, `registry_architect` for read-only semantic review, and `registry_maintainer` for deterministic validation.

---

### Task 1: Reconcile Extension Grammar, Governance, and Registry Records

**Files:**
- Modify: `rfc/rfc-iri-urn-structure-and-registry.md`
- Modify: `registry/urn-registry-root.md`
- Modify: `rfc/rfc-type-specific-attributes.md`
- Modify: `docs/ai-project-context.md`

**Interfaces:**
- Consumes: Approved delegated-extension design, registered shared semantic parents, and existing authority-code records.
- Produces: One canonical extension grammar, explicit authority/scope governance, deterministic fallback, and synchronized supporting guidance.

- [x] **Step 1: Run the failing structural contract checks**

Verify that the current documents still contain direct facility-code examples,
lack a normative extension production and fallback rule, and contain unresolved
scope cells. These failures establish that the approved contract is absent.

```bash
! rg -q '<facility-code>' rfc/rfc-iri-urn-structure-and-registry.md
rg -q 'EXTENSION-MARKER' rfc/rfc-iri-urn-structure-and-registry.md
! rg -q '\| [A-Z]{3} by delegation record \|' registry/urn-registry-root.md
```

Expected: all three desired-state checks fail before implementation.

- [x] **Step 2: Define the governing RFC model**

Update RFC terminology and grammar to define category-root URNs and the
canonical extension form. Reserve lowercase `ext`, require one lowercase
authority-code segment and a nonempty local path, and constrain insertion to
the namespace root or an exact registered canonical semantic parent.
Authority registration is evaluated during scope authorization. No separate
extension-point approval registry is created.

Add `storage` and the administrative `ext` branch to the domain/category
alignment without removing the current user-added `compute` entry.

- [x] **Step 3: Define hierarchy and fallback behavior**

State that `ext` and its authority are structural rather than semantic subtype
segments. Prefix fallback stops at the nearest recognized shared parent before
`ext`; root-scope extensions use opaque fallback. Forbid treating `:ext` and
`:ext:<authority>` prefixes as resource types or controlled values.

- [x] **Step 4: Replace Section 4 and update registry procedures**

Replace direct facility-code examples with the three approved `ext` examples.
Require authority-code reservation and exact scope delegation for scope
authorization, followed by local suffix assignment and documentation before a
producer claims an assigned DOE-IRI extension. Separate authority and scope
entry fields, state that local leaves do not require central registration, and
document promotion/deprecation behavior without defining string equivalence.

- [x] **Step 5: Define layered validation and compatibility**

Distinguish syntactic validity, scope authorization, and local definition.
Preserve unknown-extension fallback for general clients while allowing strict
contracts to reject unassigned values. State that proven direct-form deployments
require explicit deprecated mappings and must never be heuristically rewritten.

- [x] **Step 6: Reconcile the Root Registry**

Describe `ext` as an administrative delegation branch. Split Section 7 into an
authority-code table and a scope-delegation table. Keep all five authority codes
active and permanent, record that no scopes are currently assigned, remove all
unresolved cells, and list legal example shapes as specification-defined shapes
rather than active grants.

- [x] **Step 7: Align supporting guidance**

Update project context to record the adopted decision and remove its open
extension-placement question. Update facility-local attribute-profile guidance
in `rfc-type-specific-attributes.md` to require scope authorization, a local
definition supplied or linked by the profile, and shared-parent fallback.

- [x] **Step 8: Run focused contract checks**

```bash
! rg -q '<facility-code>' rfc/rfc-iri-urn-structure-and-registry.md
rg -q 'EXTENSION-MARKER|ExtensionURN|extension URN' rfc/rfc-iri-urn-structure-and-registry.md
! rg -q '\| [A-Z]{3} by delegation record \|' registry/urn-registry-root.md
rg -q 'No delegated scopes are currently assigned' registry/urn-registry-root.md
rg -q 'nearest recognized shared parent.*before `ext`' rfc/rfc-iri-urn-structure-and-registry.md
git diff --check -- rfc/rfc-iri-urn-structure-and-registry.md registry/urn-registry-root.md rfc/rfc-type-specific-attributes.md docs/ai-project-context.md
```

Expected: all checks succeed.

---

### Task 2: Deterministic Cross-Document Validation

**Files:**
- Validate: the four Task 1 semantic documents
- Preserve: `README.md` and `registry/link-profile-root.md`

**Interfaces:**
- Consumes: Task 1's governing rules, registry records, and supporting guidance.
- Produces: Evidence of grammar, terminology, lifecycle, scope, fallback, compatibility, links, and unrelated-change preservation.

- [x] **Step 1: Validate canonical and prohibited forms**

Confirm all canonical examples use `ext`, direct placeholder forms are absent,
and extension examples have one marker, a registered authority code, and a
nonempty suffix.

- [x] **Step 2: Validate governance separation**

Confirm the RFC and Root Registry distinguish authority reservations from exact
scope delegations; all five authority codes remain active; the scope table has
no active rows; and no language implies code reservation grants scope.

- [x] **Step 3: Validate hierarchy and validation semantics**

Confirm both documents agree on the non-semantic marker, pre-marker fallback,
root opaque handling, and the syntax/scope-authorization/local-definition
distinction.

- [x] **Step 4: Validate preservation and document hygiene**

Confirm the pre-existing RFC version-history and `compute` domain additions
remain present, the concurrent README/link-index changes are byte-preserved,
relative Markdown links resolve, and focused `git diff --check` passes.
