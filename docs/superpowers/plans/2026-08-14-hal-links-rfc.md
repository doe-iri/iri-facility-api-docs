# HAL Links RFC Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the broad HAL draft with a concise registry-consistent RFC and register the ten IRI link relations required by the approved URI-migration and `submitJob` design.

**Architecture:** The RFC defines HAL representation, migration, compatibility, agentic/RAG motivation, CURIE usage, and reusable OpenAPI 3.1 components. The Link Profile Index and ten dedicated profiles define the new `iri:*` semantics; existing registered profiles remain authoritative and production OpenAPI files remain unchanged.

**Tech Stack:** Markdown RFC and registry documents, OpenAPI 3.1 YAML examples, HAL JSON examples, shell/Ruby structural validation.

**Spec:** `docs/superpowers/specs/2026-08-14-hal-links-rfc-design.md`

## Global Constraints

- Do not introduce or retain `ResourceDefinition`, `ResourceState`, or a required definition/state split in `rfc/rfc-hal-links.md`.
- Treat the DOE-IRI URN Registry and Link Profile Index as authoritative.
- Use exact registered resource-type and controlled-value URNs.
- Register all ten new IRI relations as `provisional`.
- Use standard `self`, `help`, and `monitor` without adding them to the DOE-IRI link index.
- Keep the agentic/RAG rationale concise and independent of resource/state separation.
- Keep the CURIE example explicitly illustrative; do not establish a canonical DOE-IRI relation URI.
- Do not modify production OpenAPI v1 or v2 files.
- Do not modify URN registry files, project context, or unrelated link profiles.
- Use `apply_patch` for edits and preserve unrelated work.
- Do not stage or commit unless the user separately requests it.

---

### Task 1: Register Status and Facility URI-Migration Relations

**Files:**
- Create: `registry/link-profile-generated-by.md`
- Create: `registry/link-profile-has-event.md`
- Create: `registry/link-profile-impacts.md`
- Create: `registry/link-profile-may-impact.md`
- Create: `registry/link-profile-has-resource.md`
- Create: `registry/link-profile-has-site.md`
- Modify: `registry/link-profile-root.md`

**Interfaces:**
- Consumes: Current Event, Incident, Site, Facility, and Resource URI-property semantics from the OpenAPI and conceptual model.
- Produces: Registered `iri:generated-by`, `iri:has-event`, `iri:impacts`, `iri:may-impact`, `iri:has-resource`, and `iri:has-site` contracts for RFC examples and migration mappings.

- [x] **Step 1: Run the failing registration contract**

```bash
for rel in generated-by has-event impacts may-impact has-resource has-site; do
  test -f "registry/link-profile-${rel}.md"
done
```

Expected: nonzero because the six profiles do not yet exist.

- [x] **Step 2: Create the six profiles**

Each profile must follow the repository structure and include metadata,
semantics, source/target, cardinality, stability, authorization, compatibility,
and HAL representation. Use these exact contracts:

| Relation | Source | Target | Cardinality | Target class |
|---|---|---|---|---|
| `iri:generated-by` | `Event` | `Incident` | `0..1` | API resource |
| `iri:has-event` | `Incident` | `Event` | `0..*` | API resource |
| `iri:impacts` | `Event` | DOE-IRI `Resource` | Exactly `1` | Resource |
| `iri:may-impact` | `Incident` | DOE-IRI `Resource` | `0..*` | Resource |
| `iri:has-resource` | `Site` | DOE-IRI `Resource` | `0..*` | Resource |
| `iri:has-site` | `Facility` | `Site` | `0..*` | API resource |

All six have status `provisional`. Required legacy fields remain authoritative
during migration. Null `incident_uri` omits `iri:generated-by`; it never creates
a null `href`. Authorization-sensitive omissions do not generally prove that
the relationship is absent.

- [x] **Step 3: Add six index rows**

Add Core/Status/Facility rows to `registry/link-profile-root.md`. Each row must
link to the corresponding profile and copy its exact source, target,
cardinality, and concise semantic meaning.

- [x] **Step 4: Run the focused registration checks**

```bash
for rel in generated-by has-event impacts may-impact has-resource has-site; do
  test -f "registry/link-profile-${rel}.md"
done
rg -n 'iri:(generatedBy|hasEvent|impacts|mayImpact|hasResource|hasSite)' \
  registry/link-profile-root.md registry/link-profile-*.md
git diff --check -- registry/link-profile-root.md registry/link-profile-*.md
```

Expected: all six files exist, every relation is indexed, and the diff check
prints no errors.

---

### Task 2: Register Allocation and Job-Submission Relations

**Files:**
- Create: `registry/link-profile-has-project.md`
- Create: `registry/link-profile-has-capability.md`
- Create: `registry/link-profile-has-project-allocation.md`
- Create: `registry/link-profile-submit-job.md`
- Modify: `registry/link-profile-root.md`

**Interfaces:**
- Consumes: Current ProjectAllocation, UserAllocation, Capability, Resource, and compute-system contracts.
- Produces: Registered allocation navigation and one representative operation-affordance relation used by the RFC.

- [x] **Step 1: Run the failing registration contract**

```bash
for rel in has-project has-capability has-project-allocation submit-job; do
  test -f "registry/link-profile-${rel}.md"
done
```

Expected: nonzero because the four profiles do not yet exist.

- [x] **Step 2: Create the three allocation profiles**

Use these exact contracts and status `provisional`:

| Relation | Source | Target | Cardinality | Target class |
|---|---|---|---|---|
| `iri:has-project` | `ProjectAllocation` | `Project` | Exactly `1` | API resource |
| `iri:has-capability` | `Resource` or `ProjectAllocation` | `Capability` | Resource `0..*`; ProjectAllocation exactly `1` | API resource |
| `iri:has-project-allocation` | `UserAllocation` | `ProjectAllocation` | Exactly `1` | API resource |

Define one shared `iri:has-capability` meaning: the target Capability is
associated with the source. Resource usage means the Resource provides it;
ProjectAllocation usage means the allocation applies to it.

- [x] **Step 3: Create `iri:submit-job` profile**

The profile must define:

```text
Source: urn:doe-iri:resource:compute:system
Target: operation entry point
Current operation: POST /api/v2/compute/job/{resource_id}
OpenAPI operationId: launchJob
Cardinality: 0..1
Status: provisional
```

State that the relation advertises an applicable operation entry point but
does not specify the request contract, grant permission, prove capacity, or
guarantee schedulability. OpenAPI remains authoritative for method, `JobSpec`,
response, error, and security behavior.

- [x] **Step 4: Add four index rows**

Add Allocation and Compute rows to `registry/link-profile-root.md`, matching
each profile exactly.

- [x] **Step 5: Run the focused registration checks**

```bash
for rel in has-project has-capability has-project-allocation submit-job; do
  test -f "registry/link-profile-${rel}.md"
done
rg -n 'iri:(hasProject|hasCapability|hasProjectAllocation|submitJob)' \
  registry/link-profile-root.md registry/link-profile-*.md
rg -n 'POST /api/v2/compute/job/\{resource_id\}|operationId.*launchJob' \
  registry/link-profile-submit-job.md
git diff --check -- registry/link-profile-root.md registry/link-profile-*.md
```

Expected: all four files exist, relations are indexed, operation metadata is
present, and the diff check prints no errors.

---

### Task 3: Rewrite the HAL Links RFC

**Files:**
- Replace: `rfc/rfc-hal-links.md`

**Interfaces:**
- Consumes: The approved design, the complete Link Profile Index, ten new profiles, existing registered topology profiles, and current OpenAPI URI fields.
- Produces: A concise normative RFC describing HAL representation and additive URI migration without changing production schemas.

- [x] **Step 1: Run the failing RFC contract**

```bash
rg -n 'ResourceDefinition|ResourceState' rfc/rfc-hal-links.md
test "$(wc -l < rfc/rfc-hal-links.md)" -lt 600
```

Expected: the first command finds many stale references and the line-count
check fails against the current 1,379-line draft.

- [x] **Step 2: Replace the document with a focused structure**

Use these sections only:

1. Abstract and status.
2. Scope and semantic model.
3. Agentic and RAG motivation.
4. HAL `_links`, link objects, arrays, and CURIEs.
5. Authoritative relation sources.
6. Legacy URI-property mapping table.
7. Operation affordances with `iri:submit-job`.
8. OpenAPI 3.1 `HalLink`, `HalLinkValue`, and `HalLinks` schemas.
9. Compatibility and migration.
10. Producer, consumer, authorization, and security rules.
11. Three compact JSON examples.
12. References.

The resulting RFC must be under 600 lines and must contain no
`ResourceDefinition`, `ResourceState`, capacity-state, companion-separation,
generic relationship-resource, or broad operation-catalog material.

- [x] **Step 3: Add the complete URI mapping**

Document these mappings, including plural arrays where present:

| Existing source field | Relation |
|---|---|
| Any `self_uri` | `self` |
| `Resource.site_uri` | `iri:located-at` |
| `Facility.support_uri` | `help` |
| `Facility.site_uris` | `iri:has-site` |
| `Event.incident_uri` | `iri:generated-by` |
| `Incident.event_uris` | `iri:has-event` |
| `Event.resource_uri` | `iri:impacts` |
| `Incident.resource_uris` | `iri:may-impact` |
| `Site.resource_uris` | `iri:has-resource` |
| `ProjectAllocation.project_uri` | `iri:has-project` |
| `ProjectAllocation.capability_uri` | `iri:has-capability` |
| `Resource.capability_uris` | `iri:has-capability` |
| `UserAllocation.project_allocation_uri` | `iri:has-project-allocation` |
| `TaskSubmitResponse.task_uri` | `monitor` |

State that mapping depends on source semantics, not the property spelling.

- [x] **Step 4: Add concise agentic/RAG and CURIE text**

Explain that links avoid facility-specific URL guessing and can improve RAG
discovery, but current representations and OpenAPI govern invocation. Include
the non-normative template:

```json
{
  "name": "iri",
  "href": "https://example.org/iri/rels/{rel}",
  "templated": true
}
```

State that `example.org` must not be copied into deployments and that CURIE
expansion does not assign or redefine relations.

- [x] **Step 5: Add the OpenAPI 3.1 schema once**

Include exactly one definition each for `HalLink`, `HalLinkValue`, and
`HalLinks`, plus the `_links` property fragment. Use `uri-reference` for
`href`, require `href`, allow singular objects or arrays, and keep
`additionalProperties: true` on `HalLink`.

- [x] **Step 6: Add three compact JSON examples**

Use:

1. A `urn:doe-iri:resource:storage:system` Resource with `self`,
   `iri:located-at`, and `iri:provides-filesystem`.
2. Event/Incident migration with legacy URI fields and the corresponding new
   registered relations.
3. A `urn:doe-iri:resource:compute:system` Resource with `iri:submit-job`, plus
   a task response using `monitor`.

Use current `/api/v2/...` paths and no unregistered URNs or relations.

- [x] **Step 7: Run RFC structural and example checks**

```bash
! rg -n 'ResourceDefinition|ResourceState|ResourceCapacityState|companion separation' \
  rfc/rfc-hal-links.md
test "$(wc -l < rfc/rfc-hal-links.md)" -lt 600
rg -n 'agent|RAG|curies|https://example.org/iri/rels/\{rel\}' rfc/rfc-hal-links.md
rg -n 'self_uri|site_uri|incident_uri|event_uris|resource_uri|support_uri|project_uri|capability_uri|project_allocation_uri|task_uri' \
  rfc/rfc-hal-links.md
git diff --check -- rfc/rfc-hal-links.md
```

Expected: no forbidden architecture text, fewer than 600 lines, required
agentic/CURIE/migration content present, and no diff errors.

---

### Task 4: Cross-Document Review and Validation

**Files:**
- Validate: `rfc/rfc-hal-links.md`
- Validate: `registry/link-profile-root.md`
- Validate: the ten new `registry/link-profile-*.md` files
- Preserve: all `specification-v1/**` and `specification-v2/**` files

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: Evidence that RFC, registry, examples, and compatibility language agree.

- [x] **Step 1: Perform read-only semantic review**

Use `registry_architect` to verify exact relation meanings, directions,
cardinality, target classification, operation-affordance boundaries, CURIE
wording, compatibility, and registered URNs. Resolve findings through the
same `registry_editor` that owns the affected files.

- [x] **Step 2: Parse fenced JSON and YAML examples**

Extract every `json` and `yaml` fenced block from the RFC and ten profiles.
Parse JSON with Ruby `JSON.parse` and YAML with Ruby `YAML.safe_load`.
Expected: every complete example parses.

- [x] **Step 3: Validate index/profile equality**

Check that all ten relations occur exactly once in the Link Profile Index and
that index source, target, cardinality, lifecycle, and target classification
match their profile metadata.

- [x] **Step 4: Validate registry coverage and prohibited values**

Confirm every `iri:*` key in the RFC is indexed and every example resource
type is registered. Reject `urn:doe-iri:relationship:*`,
`resource:storage:filesystem:scratch`, and unregistered state/capacity/API
relations.

- [x] **Step 5: Validate compatibility and protected files**

Confirm scalar equality, array target-set equality, null omission, consumer
preference/fallback, and later-OpenAPI-removal language. Confirm no file under
`specification-v1/` or `specification-v2/` changed.

- [x] **Step 6: Validate links and final diff**

Resolve all relative Markdown links in affected documents and run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors and only the approved RFC, index, profiles,
design, and plan files are changed or untracked.
