# AGENTS.md

Do not spawn subagents or use collaboration tools.

Perform all work in the current agent/thread.

# DOE-IRI Registry Repository Instructions

This repository contains the DOE Integrated Research Infrastructure (IRI)
registry documentation for Resource Type URNs, controlled attribute URNs,
Resource Definition profiles, and hypermedia link-relation definitions used by
the IRI Facility API.

Before modifying registry documentation, read:

- `docs/ai-project-context.md` if present.
- `registry/urns/README.md`.
- The applicable Resource Type and controlled-attribute URN registries,
  Resource Definition profile, and link-relation definitions for the area being
  changed.

Treat repository contents as authoritative for current registered values.
Treat `docs/ai-project-context.md` as architectural and historical context.
If the repository and context document disagree, identify the inconsistency
before changing registry semantics.

### Source-of-Truth Precedence

Resolve authority by concern rather than by document age or location:

```text
Checked-out IRI v2 OpenAPI
    Structural API contract: properties, types, required/nullable rules, formats,
    operation shapes, and structural validation.

Governing DOE-IRI URN specification
    Namespace syntax, hierarchy matching, registration procedure, delegation,
    extension rules, and conformance.

registry/urns/README.md and registry/urns/*.md
    Assigned DOE-IRI URNs, controlled values, parentage, and lifecycle status.

registry/relations/README.md and registry/relations/<relation>.md
    Registered IRI link-relation names and complete relation semantics.

rfc/rfc-hal-links.md
    HAL wire conventions, legacy URI-property migration, and common hypermedia
    mappings.

registry/profiles/status/resource.md
    Common semantic and interoperability conventions for the current IRI v2
    Resource representation.

registry/profiles/resource-definition/<domain>/<type>.md
    Additional type-specific semantics selected by `resource_type`.

Other registry/profiles/** documents
    Semantic and interoperability conventions for their corresponding API
    representations.

docs/ai-project-context.md
    Architectural and historical context only.

docs/decisions/**
    Non-normative architectural decision records. They explain why accepted
    choices were made but never override OpenAPI, RFCs, URN registries,
    relation definitions, or representation profiles.
```

If sources that are authoritative for different concerns appear to conflict, do
not silently choose one. Identify whether the mismatch is structural, semantic,
registry-related, or stale documentation before changing normative content.

### Documentation Lifecycle

Keep normative rules in the source authoritative for that concern: OpenAPI for
structure; RFCs for governing protocol and namespace rules; URN registries for
assigned identifiers and lifecycle; relation definitions for `iri:*` semantics;
and representation and Resource Definition profiles for representation
semantics.

Use `docs/decisions/` only for durable architectural rationale that helps future
maintainers understand why an accepted choice was made. Decision records are
non-normative and MUST NOT become a second registry, schema, or conformance
source. A decision record never overrides OpenAPI, RFCs, registries, relation
definitions, or representation profiles.

Do not retain transient AI/Codex implementation plans, scratch analyses,
command transcripts, or completed migration checklists as durable repository
documentation. Git history is the implementation record.

If a decision record conflicts with a current authoritative source, the
authoritative source wins. Update, supersede, or mark the decision record
historical rather than changing normative semantics to match stale rationale.

## 1. Core Modeling Rules

### 1.1. Resource type URNs identify what a resource is

Resource types use:

```text
urn:doe-iri:resource:<domain>[:<refinement>...]
```

Examples:

```text
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:compute:node
```

The URN hierarchy is a **semantic classification hierarchy**, not a physical
containment hierarchy.

Do not encode topology by nesting resource types merely because one resource
physically contains another.

For example, keep:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu
```

rather than inventing:

```text
urn:doe-iri:resource:compute:system:node:cpu
```

### 1.2. Attributes describe type-specific characteristics

Type-specific attributes belong in the Resource Definition profile selected by
the resource's `resource_type` when those attributes are part of the applicable
IRI v2 Resource model.

Use controlled DOE-IRI URNs when interoperability benefits from a governed
vocabulary. Use ordinary JSON scalar types for values such as counts, capacity,
product names, versions, paths, and URLs unless a controlled vocabulary is
explicitly required.

### 1.3. Relationships describe topology and navigation

Relationships between independently identifiable resources belong in
registered IRI/HAL link relations, not duplicated as ordinary attributes.

Examples:

```text
iri:provides-filesystem
iri:has-mount
iri:mounted-on
iri:has-node
iri:has-gpu
```

When documenting a relationship, include:

- semantic meaning;
- source representation type;
- target representation type;
- cardinality;
- the expected stability of the relationship target, when relevant;
- whether authorization affects visibility;
- whether the target is an API representation, operation entry point, or
  relationship resource;
- example HAL representation.

### 1.4. IRI v2 Resource Modeling Scope

IRI v2 does not define or require separate Resource Definition and Resource
State representations, endpoints, or conformance models.

Resource Definition profiles under `registry/profiles/resource-definition/`
provide additional type-specific semantics for the current IRI v2 `Resource`
representation according to `resource_type`. The term **Resource Definition
Profile** does not imply a separate Resource Definition API representation in
IRI v2.

Do not introduce requirements for a future Resource Definition / Resource State
split unless explicitly working on IRI v3. Any such future separation is outside
the scope of these IRI v2 repository instructions.

## 2. Registry vs. Governing Specifications

```text
Specifications
    Define the rules.

Registries
    Record the values assigned under those rules.
```

Do not duplicate namespace grammar, ABNF, matching rules, extension rules,
registration procedure, or conformance language into registry pages when those
rules belong in the governing specification.

## 3. Namespace Conventions

The DOE-IRI namespace prefix is:

```text
urn:doe-iri:
```

Primary branches currently include:

```text
urn:doe-iri:resource
urn:doe-iri:storage
urn:doe-iri:compute
urn:doe-iri:allocation
urn:doe-iri:compression
urn:doe-iri:ext
```

Use the repository's exact namespace spelling and capitalization. Do not
invent new top-level namespaces or controlled values without explicitly
identifying them as proposals and explaining why they are needed.

## 4. Documentation Structure

```text
urns/README.md
    Root DOE-IRI namespace registry.

urns/resource-types.md
    Authoritative registry for Resource Type URNs.

urns/attributes.md
    Authoritative registry for controlled attribute URNs.

profiles/resource-definition/<domain>/<type>.md
    Resource Definition profile for a specific resource type.

relations/<relation>.md
    Semantic definition of an IRI link relation.
```

When adding a domain or subtype, update applicable navigation/index documents
and relative links.

## 5. Resource Definition Profile Format

Recommended structure:

1. `# IRI <Type> Resource Definition Profile`
2. Profile URI, Base Profile, Resource Type, status, and version.
3. Profile Applicability.
4. Introduction and conceptual model.
5. Type-specific attribute table.
6. Numbered sections for attributes and controlled URN families.
7. OpenAPI / JSON Schema.
8. Example JSON instance.
9. DOE-IRI footer.

Resource Definition profiles specialize the common
`https://iri.science/profiles/status/resource` representation according to
`resource_type`. They belong under
`registry/profiles/resource-definition/<domain>/<type>.md` and use canonical
URIs of the form
`https://iri.science/profiles/resource-definition/<domain>/<type>`.

They are semantic specializations of the current IRI v2 Resource representation;
they do not define a separate Resource Definition representation, endpoint, or
lifecycle. Do not use their directory name to infer a future IRI v3
architecture.

Resource Type registration belongs in `registry/urns/resource-types.md` and
controlled attribute registration belongs in `registry/urns/attributes.md`.
A Resource Definition profile MAY reference registered URNs but MUST NOT be
the authoritative registration record for them.

For controlled URN families:

- define semantic purpose;
- enumerate registered values;
- provide concise descriptions;
- distinguish related concepts;
- state singular vs multi-valued;
- state when omission is preferable to guessing.

## 6. OpenAPI / JSON Schema Conventions

Where profiles use a reusable DOE-IRI URN schema, reuse the repository's current
canonical schema or reference rather than creating a second independent URN
grammar in `AGENTS.md` or in each profile.

The governing DOE-IRI URN specification is authoritative for URN syntax. If an
inline JSON Schema fragment is required in a Resource Definition profile, copy
it from the current canonical schema source and keep it synchronized with the
governing specification.

General conventions:

- profile schemas use `type: object`;
- `schema_version` is normally required;
- `schema_version` currently uses `"1.0.0"` where applicable;
- URN arrays use `uniqueItems: true`;
- configured counts/capacities are non-negative;
- use `format: int64` when consistent with existing profiles;
- preserve compatibility with the repository's actual OpenAPI version.

## 7. Lifecycle Status

Registry lifecycle values include:

```text
active
provisional
deprecated
```

A deprecated entry should identify a replacement URN when one exists.
Do not silently change lifecycle status.

## 8. Storage Domain Rules

Current storage resource types:

```text
urn:doe-iri:resource:storage:system
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:storage:mount
urn:doe-iri:resource:storage:block
urn:doe-iri:resource:storage:object
```

Important rules:

- `storage:system` is managed infrastructure.
- `filesystem`, `block`, and `object` are logical storage resources.
- `mount` is an exposure/relationship resource.
- Archive is a tier/lifecycle concept, not a fundamental access model.
- Mount path belongs to the mount resource.
- Block device path is attachment-specific.
- Object endpoints are attributes/access descriptors unless independent
  endpoint identity, lifecycle, or relationships are required.

Storage relationships:

```text
iri:provides-filesystem
iri:provides-block
iri:provides-object
iri:has-mount
iri:mounted-on
iri:attached-to
```

## 9. Compute Domain Rules

Current compute resource types:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu
```

They remain siblings in the resource-type hierarchy. Physical containment is
represented with links.

Compute relationships:

```text
iri:has-node
iri:has-cpu
iri:has-gpu
```

Facilities are not required to expose every CPU/GPU individually if aggregate
information is sufficient.

## 10. Link Relation Definition Rules

A link-relation definition should distinguish:

- long-lived relationship semantics from condition-dependent behavior;
- API-representation targets from operation-entry-point targets;
- relationship resources from ordinary resources;
- authorization-filtered visibility from semantic absence.

If authorization may hide a target, document that absence of a visible link is
not necessarily proof that the relationship does not exist.

## 11. CBORG Model Profiles and Agent Routing

### 11.1. Runtime configuration boundary

This repository intentionally does **not** pin concrete model names, model
providers, credentials, or reasoning-effort settings in project-scoped
`.codex/config.toml` or in the named agent TOML files.

Keep these concerns separate:

- **User-level Codex configuration** (`~/.codex/config.toml`) selects the model
  provider, authentication mechanism, and normal/default model for the local
  Codex installation.
- **User-level Codex profile files** (`~/.codex/<profile-name>.config.toml`)
  provide optional runtime model/quality overrides selected by the user.
- **Repository configuration** (`.codex/config.toml`) defines project-specific
  Codex behavior such as multi-agent concurrency, but must not override the
  user's provider or authentication configuration.
- **Named agent files** (`.codex/agents/*.toml`) define role, instructions, and
  sandbox boundaries. They intentionally inherit the selected parent session's
  model and reasoning configuration.

When using the LBL CBORG service, configure CBORG only in the user-level Codex
configuration. The repository must never contain `CBORG_API_KEY`, other model
credentials, or a machine-specific CBORG endpoint override.

For the current LBL CBORG setup, the normal user-level default is expected to be
an alias such as:

```text
openai/gpt-5.6-sol-medium
```

CBORG/LiteLLM aliases may already encode reasoning policy. For example, the
current `openai/gpt-5.6-sol-medium` alias resolves to GPT-5.6 Sol with medium
reasoning. Do not add a second repository-level `model_reasoning_effort`
override for such aliases.

Useful user-level CBORG profile intent is:

```text
cborg-sol-medium     normal/default work
cborg-sol-xhigh      architecture, difficult debugging, broad semantic review
cborg-sol-max        exceptional quality-first work
cborg-terra-medium   faster/lower-cost routine work
```

Profile names are user-local configuration, not repository requirements. A
contributor using another approved model provider may use different profile
names or models while preserving the same agent roles and safety boundaries.

Current Codex profile files live beside `~/.codex/config.toml` as
`~/.codex/<profile-name>.config.toml` and are selected from the CLI with:

```text
codex --profile <profile-name>
```

For Codex 0.134.0 and later, do not use the legacy top-level
`profile = "..."` selector in `~/.codex/config.toml`. Put the normal/default
CBORG model directly in the base user configuration and use profile files only
as explicit CLI overlays. The base user configuration applies when no CLI
profile is selected.

### 11.2. Model inheritance policy

The selected parent Codex session is the **runtime quality knob** for this
repository.

The named agents intentionally omit both:

```text
model = ...
model_reasoning_effort = ...
```

The project `.codex/config.toml` should also omit:

```text
default_subagent_model = ...
default_subagent_reasoning_effort = ...
```

unless the project deliberately decides to stop inheriting the parent session's
model policy.

With those fields omitted, named agents inherit the parent session's model and
reasoning configuration unless the parent explicitly supplies a per-spawn
override. Therefore, starting Codex with a stronger or faster user-level profile
applies that runtime choice consistently to the main thread and to
`registry_architect`, `registry_editor`, and `registry_maintainer`.

Do not silently switch an agent to a different model, reasoning level, or model
provider merely because its task appears easier or harder. Preserve the user's
selected session policy. If the inherited model appears insufficient for a
high-impact semantic decision, identify that concern rather than guessing.

Do not treat model names mentioned in historical project notes as runtime
requirements.

### 11.3. Architecture and semantic design

Delegate to `registry_architect` when the task involves:

- new resource types;
- new URNs or controlled vocabularies;
- taxonomy design;
- resource type vs attribute vs relationship vs operation/representation decisions;
- relationship semantics/cardinality;
- compatibility/deprecation decisions;
- ontology review;
- broad registry consistency analysis.

`registry_architect` is read-only. It returns a semantic decision and
implementation plan.

### 11.4. Implementation of approved designs

Delegate to `registry_editor` after semantic decisions are made.

Examples:

- creating/updating a Resource Definition profile;
- adding an approved URN;
- updating taxonomy/index tables;
- updating schemas/examples;
- creating an approved link-relation definition;
- updating README/root/domain navigation;
- propagating approved terminology.

If `registry_editor` encounters a new semantic question, return it to the main
thread for `registry_architect` review.

### 11.5. Mechanical maintenance

Delegate to `registry_maintainer` for deterministic maintenance:

- broken Markdown links;
- stale filenames/references;
- formatting;
- duplicate detection;
- table/taxonomy synchronization;
- approved filename changes;
- navigation checks.

`registry_maintainer` must not make ontology or lifecycle decisions.

### 11.6. Preferred sequencing

For mixed architecture + edit work:

```text
Main thread
    │
    ├── registry_architect
    │       read-only semantic analysis
    │
    ├── main thread
    │       resolve/approve decisions
    │
    ├── registry_editor
    │       implement approved changes
    │
    └── registry_maintainer
            validate links/indexes/mechanical consistency
```

Avoid parallel write-heavy agents on overlapping files.

### 11.7. Fallback behavior

If a named custom agent cannot start because of client/account/configuration
limitations:

1. Do not bypass the semantic stage.
2. For `registry_architect`, perform the architecture review in the main thread
   without editing files, or use an available general read-only subagent if
   the runtime can enforce that boundary.
3. Record that a fallback was used only when it materially affects the review.
4. Continue to `registry_editor` only after the semantic decision is explicit.
5. Never silently substitute a write-capable agent for the read-only
   architecture stage.

The objective is to preserve the **role boundary**, not a particular model ID.

## 12. Editing Discipline

Before changes:

1. Inspect neighboring files.
2. Identify affected indexes, taxonomy pages, README links, and examples.
3. Preserve relative Markdown links.
4. Avoid duplicate controlled vocabularies.
5. Prefer shared vocabularies only when semantics are truly shared.
6. Do not infer equivalence merely from similar names.
7. Do not silently rename registered URNs.
8. Call out compatibility effects.

After changes:

1. Search for stale references.
2. Check Markdown relative links.
3. Check taxonomy trees vs tables.
4. Check Resource Definition profiles vs URN registry/index pages.
5. Check link-relation-definition source/target types vs domain diagrams.
6. Review the git diff.

## 13. Preferred Working Style

For broad registry changes:

- inspect related documents first;
- keep semantic decisions explicit;
- use `registry_architect` for design analysis;
- use `registry_editor` for approved implementation;
- use `registry_maintainer` for deterministic validation;
- identify unresolved design questions instead of guessing;
- summarize changed files and compatibility implications.

For a new concept, determine whether it belongs as:

```text
resource type
controlled attribute
ordinary scalar attribute
link relation
relationship resource
representation property
operation entry point
```

Choose based on semantics, not implementation convenience.

## 14. Delegated Extension Conventions

Facility- or project-controlled DOE-IRI values use an explicit
`:ext:<authority>:` segment beneath the exact registered shared parent. Use the
nearest accurate shared parent; the root form `urn:doe-iri:ext:...` requires a
root-scope delegation and is not the default placement for local values.

Keep these extension states distinct:

- a syntactically valid Extension URN only has the canonical extension shape;
- an authority-code reservation identifies the change controller but grants no
  namespace scope;
- scope authorization requires an active delegation for the exact parent and
  authority; and
- an assigned DOE-IRI extension also requires the authority to assign and
  document the nonempty local suffix.

An exact scope delegation covers the local suffix subtree beneath its assigned
prefix, not adjacent, ancestor, or sibling scopes. Proven legacy direct-form
identifiers require explicit compatibility or deprecation mappings; never
heuristically rewrite them into `ext` form.

## 15. Service Domain Conventions

Use `urn:doe-iri:resource:service:*` for service resource types and
`urn:doe-iri:service:*` for controlled service technologies, protocols, and
APIs. A controlled service value is not a `resource_type`, and a technology,
protocol, or API does not become a resource subtype merely because it describes
a service.

A DTN resource identifies a consumable data-transfer service, not its host. An
inference-service resource identifies a consumable model-invocation service,
not a model, deployment, endpoint, replica, host, or accelerator. Endpoint
descriptors remain attributes unless independent endpoint identity, lifecycle,
or relationships are required.

Keep implementation technology distinct from the protocols or APIs it exposes.
Advertise supported protocols and APIs explicitly; clients must not infer them
from a technology value, including when the same product name appears in both
vocabularies.

For inference services, `served_models` is the catalog of models configured to
be served. `active_models`, when present, identifies models currently active or
loaded, and its items reference `served_models.id`; catalog membership alone
does not mean a model is currently loaded or available.

`iri:hosted-on` links a DTN or inference service to its compute-system or
compute-node hosting infrastructure; it does not assert current routing, live
replica placement, health, or availability. `iri:accesses-mount` links a DTN to
the mount relationship resource through which filesystem access is configured;
co-location does not imply that access, and the link does not assert current
mount availability, authorization, credentials, or transfer activity.

## 16. HAL Link Conventions

Use standard Web Linking relations when their established semantics apply. For
DOE-IRI `iri:*` relations, `registry/relations/README.md` is the authoritative
name index and each linked definition is authoritative for the relation's
complete semantics. Link-relation identifiers are not DOE-IRI URNs.

DOE-IRI extension relation identifiers use lowercase ASCII letters, digits,
and hyphens, with hyphens between words. Examples include `iri:has-mount`,
`iri:mounted-on`, `iri:generated-by`, and `iri:provides-filesystem`. Do not use
camelCase forms such as `iri:hasMount`, `iri:mountedOn`, `iri:generatedBy`, or
`iri:providesFilesystem`, or use PascalCase, underscores, or whitespace. This
naming rule does not change JSON property names, URNs, OpenAPI `operationId`
values, API paths, or standard relations. Keep filenames, headings, metadata,
examples, diagrams, and footers aligned to the exact registered relation
spelling.

The canonical URI for an IRI link relation is
`https://iri.science/rels/{relation}`. For example, `iri:has-mount` expands to
`https://iri.science/rels/has-mount` when the `iri` CURIE uses that template.

A link-relation URI defines relationship semantics. An RFC 6906 representation
profile URI identifies additional semantic constraints on a representation.
For example, `https://iri.science/rels/has-mount` identifies the relation,
whereas
`https://iri.science/profiles/resource-definition/storage/mount` identifies the
target mount Resource Definition profile. These identifiers MUST NOT be conflated. Raw
GitHub and GitHub repository URLs MUST NOT be used as canonical IRI relation or
profile identifiers.

When moving a navigable URI property into `_links`, choose the relation from the
source representation's semantics rather than the property's spelling. Until a
separate schema revision removes the legacy property, preserve its required and
nullable contract. Canonical representation identity uses the standard `self`
relation; while `self_uri` is retained, it must equal `_links.self.href`.
Retained `site_uri` maps to `iri:located-at`, must equal that link's `href`, and
the link must not be independently hidden while `site_uri` exposes the Site.
`iri:located-at` identifies the Resource's Site, whereas `iri:hosted-on`
identifies compute infrastructure hosting a service. When plural URI properties
and plural link arrays coexist, they must identify the same target set,
regardless of order. A null or absent optional URI maps to an omitted relation,
never a null `href`.

An operation relation identifies that an operation applies and where its entry
point is located. It does not identify an API resource, define the HTTP method
or payload, grant authorization, or guarantee current availability; the
governing OpenAPI contract defines invocation semantics.

HAL CURIEs may abbreviate relation identifiers only. CURIE expansion does not
assign or redefine a relation. The canonical IRI template is
`https://iri.science/rels/{rel}`; deployments MUST NOT substitute an
illustrative `example.org` value as the canonical template.

### 16.1. HAL Example Target Profiles

In documentation examples, a HAL Link Object `profile` identifies the profile
of the link target, not the relation or source representation. When the target
is an IRI representation with a known canonical profile, examples SHOULD
include that target profile. For example:

```text
iri:has-mount
    -> https://iri.science/profiles/resource-definition/storage/mount

iri:located-at
    -> https://iri.science/profiles/facility/site

iri:has-capability
    -> https://iri.science/profiles/account/capability
```

For `_links.self`, use the profile applicable to the represented object. In a
Resource Definition Profile example, use that representation's most-specific
Resource Definition Profile.

Do not add an IRI representation profile merely because a link exists. In
particular, do not add one to `curies`, `service-desc`, ordinary external
`help` targets, or operation-affordance targets such as `iri:submit-job`.

For polymorphic relations such as `iri:attached-to` and `iri:hosted-on`, select
the profile from the actual target type shown in the example. The registered
relation definition is authoritative for target classification.

# IRI Representation Profile Generation

These instructions apply when creating or modifying IRI representation profile
documents under the canonical namespace:

```text
https://iri.science/profiles/...
```

Examples include:

```text
https://iri.science/profiles/facility
https://iri.science/profiles/facility/site

https://iri.science/profiles/status/resource
https://iri.science/profiles/status/event
https://iri.science/profiles/status/incident

https://iri.science/profiles/account/capability
https://iri.science/profiles/account/project
https://iri.science/profiles/account/project-allocation
https://iri.science/profiles/account/user-allocation

https://iri.science/profiles/compute/job

https://iri.science/profiles/task
```

Resource Definition profiles also use the `https://iri.science/profiles/...`
namespace, for example:

```text
https://iri.science/profiles/resource-definition/compute/system
https://iri.science/profiles/resource-definition/compute/node
https://iri.science/profiles/resource-definition/storage/filesystem
https://iri.science/profiles/resource-definition/service/dtn
```

The goal of an IRI representation profile is to define semantic and
interoperability conventions for an IRI representation without duplicating the
structural contract already defined by OpenAPI.

The 17-section generation rules in this part apply to profiles that correspond
to independently meaningful API representations. Resource Definition profiles
are type-specific specializations of the current IRI v2 Resource representation
and instead follow **Section 5. Resource Definition Profile Format** above. They
do not need to duplicate the 17-section representation-profile template.

---

## 1. Sources of Truth

Before generating or modifying a profile, inspect the current repository.

The primary structural source of truth is:

```text
specification-v2/openapi/all_spec_v2.yaml
```

When useful, inspect the split production OpenAPI files under:

```text
specification-v2/openapi/production/
```

including:

```text
_components.yaml
facility.yaml
status.yaml
account.yaml
compute.yaml
filesystem.yaml
task.yaml
```

Also inspect any applicable registry documents under:

```text
registry/
```

especially:

```text
urns/README.md
urns/resource-types.md
urns/attributes.md
profiles/resource-definition/<domain>/<type>.md
relations/<relation>.md
```

and the HAL specification:

```text
rfc/rfc-hal-links.md
```

Do not generate profile semantics from memory when the repository contains the
applicable schema or relation definition.

OpenAPI is authoritative for structural details.

Registered relation documents are authoritative for link-relation semantics.

IRI URN registry documents are authoritative for registered URN semantics.

A profile MUST NOT silently override any of these sources.

---

## 2. Structural vs Semantic Responsibilities

Every profile MUST preserve the following separation of responsibility:

```text
OpenAPI schema
  ├── property names
  ├── JSON types
  ├── required properties
  ├── nullable properties
  ├── formats
  ├── enums
  ├── defaults
  ├── structural validation
  └── read-only properties

IRI Representation Profile
  ├── semantics
  ├── interpretation
  ├── interoperability rules
  ├── identity conventions
  ├── processing conventions
  ├── hypermedia expectations
  ├── authorization/visibility semantics
  └── compatibility conventions
```

Do not duplicate OpenAPI validation rules unnecessarily.

Do not move structural requirements from OpenAPI into a profile unless needed
to explain their semantics.

Do not use the profile to alter the OpenAPI schema.

---

## 3. Required Structural Contract Section

Every representation profile MUST contain a section named:

```markdown
## 3. Structural Contract
```

Use wording equivalent to:

```markdown
## 3. Structural Contract

The structural definition of the <Representation> representation is defined by
the IRI <API> OpenAPI `<Schema>` schema.

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- nullable properties;
- formats;
- structural validation;
- read-only properties.

This profile is authoritative for additional semantic and interoperability
conventions associated with those properties and their corresponding
hypermedia relationships.
```

Adjust the authoritative list when the schema also contains important
structural concepts such as:

```text
enums
defaults
nested schema structure
```

Include a property table based on the CURRENT OpenAPI schema.

Example:

```markdown
| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the representation. |
| `last_modified` | Yes | Time at which the representation was last modified. |
| `self_uri` | Yes | Canonical API URI of the representation. |
```

Never derive this table from an older version of the API if V2 is available.

---

## 4. Standard Profile Structure

Representation profiles SHOULD use the following 17-section structure unless a
domain-specific reason requires a small variation.

```text
1. Purpose
2. Profile Semantics
3. Structural Contract
4. Identity
5. Domain-specific semantics
6. Domain-specific semantics
7. Domain-specific semantics
8. Relationships / domain model
9. Hypermedia Representation
10. Relationship URIs / Hypermedia Semantics
11. Relationship to Existing URI Properties
12. Media Type
13. Static and Dynamic Semantics
14. Authorization and Visibility
15. Conformance
16. Profile Identification
17. Versioning
```

Sections 5 through 8 SHOULD be adapted to the representation.

Examples:

```text
Resource:
  Resource Classification
  Current Status
  Site Association
  Capabilities

Event:
  Temporal Semantics
  Status Semantics
  Event-to-Resource Relationship
  Event-to-Incident Relationship

Incident:
  Incident Type
  Status and Resolution
  Temporal Semantics
  Incident Relationships

ProjectAllocation:
  Project Relationship
  Capability Relationship
  Allocation Entries
  Allocation Semantics

Job:
  Job Status
  Job State
  Job Status Details
  Job Specification

Task:
  Task Status
  Task Lifecycle
  Task Result
  Task Command
```

Keep the profile organization consistent across representations.

---

## 5. Profile Identity

Each profile MUST declare its canonical URI near the top.

Example:

```markdown
# IRI Compute Job Profile

**Profile URI:** `https://iri.science/profiles/compute/job`
**OpenAPI type:** `Job`
**Status:** Draft
**Version:** 1.0.0
```

The canonical profile URI is the semantic identifier.

Repository locations MUST NOT be used as profile identifiers.

Do not use identifiers such as:

```text
https://github.com/doe-iri/...
raw.githubusercontent.com/...
registry/profiles/foo.md
```

as substitutes for:

```text
https://iri.science/profiles/...
```

The canonical profile URI SHOULD remain stable across compatible revisions.

---

## 6. Profile vs Resource Type vs Link Relation

Always preserve the distinction between:

```text
Resource Type
Link Relation
Representation Profile
```

They answer different questions.

Example:

```text
urn:doe-iri:resource:compute:system
    ↓
WHAT kind of Resource is this?


https://iri.science/rels/submit-job
    ↓
WHY is the linked target related to the source?


https://iri.science/profiles/compute/job
    ↓
WHAT semantic representation contract applies?
```

Never use these identifiers interchangeably.

For example:

```json
{
  "_links": {
    "iri:has-capability": {
      "href": "...",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/account/capability"
    }
  }
}
```

means:

```text
iri:has-capability
    = relation

href
    = target instance

application/hal+json
    = representation encoding

https://iri.science/profiles/account/capability
    = target representation semantics
```

---

## 7. IRI Link Relation Naming

IRI extension relations MUST use the `iri:` CURIE namespace.

Relation identifiers MUST use lowercase kebab-case.

Correct:

```text
iri:has-capability
iri:has-project
iri:has-project-allocation
iri:located-at
iri:generated-by
iri:submit-job
```

Incorrect:

```text
iri:hasCapability
iri:hasProject
iri:generatedBy
iri:submitJob
```

The CURIE namespace is:

```json
{
  "name": "iri",
  "href": "https://iri.science/rels/{rel}",
  "templated": true
}
```

For example:

```text
iri:has-capability
```

expands to:

```text
https://iri.science/rels/has-capability
```

---

## 8. Never Invent Link Relations

Before using an `iri:*` relation in a profile, search the relation registry.

If a relation exists, use its registered semantics, source type, target type,
cardinality, authorization behavior, and stability rules.

If no relation exists, DO NOT invent one inside the representation profile.

Instead, explicitly document the hypermedia gap.

For example, if a Job representation has no registered link back to its compute
Resource, say:

```text
The current Job representation does not define a Resource URI relationship,
and no registered Job-to-Resource relation currently applies. This profile
therefore does not invent relations such as iri:executed-on or iri:runs-on.
```

A new relation MUST be registered separately before normative use.

Representation profiles MUST NOT become implicit link-relation registries.

---

## 9. Existing URI Properties and HAL Migration

Many existing IRI representations contain legacy URI-valued properties such as:

```text
self_uri
site_uri
resource_uri
resource_uris
event_uris
incident_uri
site_uris
capability_uri
capability_uris
project_uri
project_allocation_uri
task_uri
```

When a registered HAL mapping exists, document it explicitly.

Example:

```text
site_uri
    ↓
_links["iri:located-at"]
```

During the additive compatibility period, follow these rules:

1. Existing required URI properties remain present.
2. Producers MAY additionally emit the registered HAL relation.
3. When both forms are present, they MUST identify the same target.
4. Arrays MUST identify the same set of targets, disregarding order.
5. Consumers SHOULD prefer advertised HAL relationships.
6. Consumers MAY fall back to legacy URI properties.
7. Removing a legacy URI property requires a separate OpenAPI schema revision.

For optional nullable URI properties:

```text
null URI
    ↓
HAL relation omitted
```

Never emit:

```json
{
  "href": null
}
```

---

## 10. Representations Without `self_uri`

Some V2 schemas are independently retrievable but do not currently contain
`self_uri`.

Examples include:

```text
ProjectAllocation
UserAllocation
Job
Task
```

Do NOT invent a `self_uri` property in the profile.

A HAL-enabled representation with canonical identity MUST expose `_links.self`.
For example:

```json
{
  "_links": {
    "self": {
      "href": "...",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/..."
    }
  }
}
```

This allows canonical hypermedia identity without adding another transitional
URI property.

Do not infer the self URI from the representation identifier.

---

## 11. HAL Examples

Profiles SHOULD include a realistic HAL representation.

Use:

```text
application/hal+json
```

for HAL examples.

The `self` link SHOULD carry the representation profile:

```json
{
  "_links": {
    "self": {
      "href": "...",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/..."
    }
  }
}
```

When a link target is an IRI representation with a known canonical profile, HAL examples SHOULD include that target representation profile.

Example:

```json
{
  "iri:has-project": {
    "href": "...",
    "type": "application/hal+json",
    "profile": "https://iri.science/profiles/account/project"
  }
}
```

Do not attach arbitrary profiles to targets whose profile has not been defined.

HAL examples MUST preserve the current OpenAPI representation contract during
the additive migration period unless the profile explicitly documents a future
schema.

---

## 12. Resource Type Rules

For the intended IRI v2 Resource contract, `resource_type` is an extensible
string containing an IRI Resource Type URN.

Verify this against the checked-out V2 OpenAPI before changing generated or
normative schema content. If the checked-out OpenAPI still describes
`resource_type` as a closed enum, report the inconsistency rather than silently
overriding the structural source of truth.

Do NOT describe the intended registry-driven `resource_type` semantics as a
closed vocabulary in Resource Definition profile prose.

Example:

```json
{
  "resource_type": "urn:doe-iri:resource:compute:system"
}
```

The DOE-IRI Resource Type registry, not OpenAPI enum values, defines the
resource-type taxonomy.

A producer SHOULD emit the most specific registered Resource Type URN that
accurately describes the Resource.

A generic consumer MUST NOT reject a syntactically valid Resource Type URN
solely because its local code does not recognize the most-specific value.

Hierarchy-aware consumers SHOULD use nearest-recognized-parent fallback.

Hierarchy matching MUST operate on complete colon-delimited semantic segments.

Do NOT implement arbitrary string-prefix matching.

For delegated extension URNs, hierarchy fallback stops at the applicable shared
semantic parent before `ext`.

---

## 13. Operation Affordances

A link to an operation entry point is not the same as a link to another API
resource.

For example:

```text
iri:submit-job
```

targets a Resource-specific job-submission operation entry point.

It does NOT target a Job representation.

An operation-affordance relation identifies:

```text
WHAT operation is applicable
and
WHERE its entry point is
```

It does not define:

```text
HTTP method
request body
response body
authentication
authorization
error handling
scheduling policy
```

Those remain defined by OpenAPI.

Profiles SHOULD explain this distinction whenever operation affordances are
relevant.

A `service-desc` link MAY identify the applicable OpenAPI document.

Example:

```json
{
  "_links": {
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

---

## 14. Do Not Invent Lifecycle Rules

When a schema defines lifecycle/status enum values but does not define a
normative transition graph, the profile MUST NOT invent one.

Examples include:

```text
JobState
TaskStatus
Incident resolution/status behavior
```

A profile MAY show an illustrative/common transition diagram only when clearly
identified as non-normative.

Use wording such as:

```text
The OpenAPI schema defines the available states but does not define a complete
normative state-transition graph. This profile therefore does not impose
additional mandatory transitions.
```

Do not infer requirements such as:

```text
completed MUST have end != null
failed MUST follow active
canceled MUST follow active
```

unless the governing specification explicitly states them.

---

## 15. Historical vs Current State

Profiles MUST distinguish historical records from current-state
representations.

For example:

```text
Event.status
    = Resource status at Event.occurred_at

Resource.current_status
    = current reported Resource status
```

An Event MUST NOT be interpreted as current Resource state merely because its
status value is `up`, `down`, or `degraded`.

Similarly:

```text
Incident relationship to Resource
```

does not automatically establish current actual Resource state.

Use the specific semantics defined by the applicable relation.

---

## 16. Authorization and Visibility

Every profile SHOULD include an Authorization and Visibility section.

Do not assume that absence from a representation proves non-existence when
authorization can affect discoverability.

Appropriate wording includes:

```text
The absence of a visible relationship does not generally prove that no
underlying relationship exists when authorization or filtering may affect
visibility.
```

Likewise, visibility MUST NOT automatically be interpreted as:

```text
authorization
allocation grant
operation permission
current availability
schedulability
```

Keep discovery, authorization, allocation, and operational state distinct.

Be careful with required OpenAPI URI properties: authorization behavior MUST
remain compatible with the structural contract.

---

## 17. Allocation Profiles

For:

```text
Capability
ProjectAllocation
UserAllocation
```

keep these concepts separate:

```text
Capability
    = something that can be allocated

ProjectAllocation
    = allocation of a Capability to a Project

UserAllocation
    = allocation/accounting assignment for a user within a ProjectAllocation

AllocationEntry
    = allocation + usage + unit
```

Do not interpret positive remaining arithmetic allocation as proof of
schedulability or availability.

For example:

```text
allocation - usage > 0
```

does NOT prove:

```text
Resource available
Capability available
user authorized
allocation still valid
job schedulable
```

Do not assume that visible User Allocations sum exactly to the Project
Allocation unless another specification establishes that invariant.

---

## 18. User Identifiers

The V2 `UserAllocation` representation contains:

```text
user_id
```

but there is currently no independently addressable V2 `User` representation.

Do not invent a User relation solely because `user_id` exists.

Do not assume that `user_id` is:

```text
email
username
OIDC sub
URI
globally unique identity
```

unless an applicable identity specification defines it.

Treat it as an opaque user identifier within the applicable identity context.

---

## 19. Job Profile Rules

For `https://iri.science/profiles/compute/job`:

```text
Job
    = submitted computational work

JobSpec
    = requested execution specification

JobStatus
    = current execution state associated with the Job
```

Do not treat JobSpec as Job identity.

Do not create a Job-to-Resource link unless a relation has been registered.

The current compute Resource is identified through the governing operation
context.

`iri:submit-job` is:

```text
Compute Resource
    → job-submission operation entry point
```

not:

```text
Job → Resource
```

---

## 20. Task Profile Rules

For:

```text
https://iri.science/profiles/task
```

distinguish:

```text
Task
    = persistent asynchronous operation state

TaskSubmitResponse
    = transient response identifying the Task

TaskCommand
    = command metadata associated with the Task

Task.result
    = operation-specific result data
```

Use the standard `monitor` relation for navigation from an asynchronous
operation response to its Task representation:

```text
TaskSubmitResponse.task_uri
        ↓
_links.monitor.href
        ↓
Task representation
        ↓
Task._links.self.href
```

`monitor` and `self` have different relation semantics even when their `href`
values identify the same Task URI: `monitor` identifies where asynchronous work
is monitored, while `self` identifies the canonical Task representation.

Do not assume:

```text
DELETE /api/v2/task/{task_id}
```

means:

```text
cancel the underlying operation
```

merely because `TaskStatus` also contains `canceled`.

Deletion semantics and cancellation semantics MUST remain separate unless the
governing specification explicitly equates them.

---

## 21. Profiles Should Not Mirror Every OpenAPI Schema

Do not automatically create a profile for every schema in
`components/schemas`.

Profiles are primarily appropriate for independently meaningful
representations with one or more of the following:

```text
stable identity
independent retrieval
domain semantics beyond structure
lifecycle semantics
hypermedia relationships
authorization-sensitive visibility
interoperability requirements
```

Current examples suitable for profiles include:

```text
Facility
Site
Resource
Event
Incident
Capability
Project
ProjectAllocation
UserAllocation
Job
Task
```

Schemas that generally SHOULD remain OpenAPI-only include:

```text
AllocationEntry
JobSpec
JobStatus
JobAttributes
ResourceSpec
Container
VolumeMount
TaskCommand
TaskSubmitResponse
request-body schemas
enum schemas
simple helper/value schemas
```

Only create a profile for these if they later acquire independent semantic
identity or exchange requirements beyond their enclosing API operation.

---

## 22. Problem Details

Do not create an IRI representation profile merely for the RFC 9457 `Problem`
schema.

Problem Details already has standardized representation semantics.

If IRI-specific errors require stable semantic identifiers, create problem type
URIs instead, for example:

```text
https://iri.science/problems/resource-not-found
https://iri.science/problems/not-authorized
```

Problem Type URIs are not representation profile URIs.

---

## 23. Conformance Section

Every profile MUST include a concrete conformance section.

Use numbered requirements.

The conformance section SHOULD summarize the profile's important processing
requirements rather than merely repeating the OpenAPI schema.

Typical requirements include:

```text
- conform to the applicable OpenAPI schema;
- treat identifiers as opaque;
- do not construct URLs from identifiers;
- use registered relations;
- preserve legacy URI/HAL consistency;
- distinguish profiles from relation identifiers;
- do not invent lifecycle transitions;
- respect authorization-dependent visibility;
- do not infer operational availability from static relationships.
```

---

## 24. Profile Versioning

Profile versioning concerns the semantic profile document.

Changes to individual representation instances do not change the profile
version.

Adding new instances does not change the profile URI.

Adding compatible registered relation targets does not necessarily change the
profile URI.

For extensible registry-driven values, adding a new registry value does not
automatically require a new profile version.

For example, registering another:

```text
urn:doe-iri:resource:...
```

does not require a new:

```text
https://iri.science/profiles/status/resource
```

profile version merely because the taxonomy grew.

Material semantic changes require compatibility review.

---

## 25. Writing Style

Profile documents MUST use normative language consistently.

Use:

```text
MUST
MUST NOT
SHOULD
SHOULD NOT
MAY
```

only for normative requirements or strong interoperability recommendations.

A standalone profile that uses the uppercase BCP 14 keywords normatively SHOULD
include the standard RFC 2119 / RFC 8174 interpretation statement, unless that
interpretation is inherited unambiguously from a governing specification.

Use declarative prose for descriptive information.

Avoid unnecessary repetition between:

```text
Purpose
Profile Semantics
relationship sections
Conformance
```

The Purpose section should explain what the representation represents.

Profile Semantics should explain its conceptual role.

Domain sections should define specific semantics.

Conformance should summarize actionable requirements.

Do not repeat the same paragraph in multiple sections.

---

## 26. Generation Procedure

When asked to generate a new profile:

1. Identify the canonical profile URI and corresponding OpenAPI schema.
2. Read the CURRENT V2 schema.
3. Identify required, optional, nullable, read-only, enum, and nested properties.
4. Identify all URI-valued properties.
5. Search `rfc/rfc-hal-links.md` for existing mappings.
6. Search `registry/relations/README.md` and the applicable
   `registry/relations/<relation>.md` files for registered relations.
7. Search the URN registry when any property uses DOE-IRI URNs.
8. Determine whether the representation has an independently retrievable API
   endpoint.
9. Determine whether it has `self_uri`.
10. If independently retrievable but lacking `self_uri`, use `_links.self` in the
    HAL profile example without modifying the schema.
11. Identify which semantics are stable and which are dynamic.
12. Identify authorization-sensitive properties or relationships.
13. Do not invent unresolved lifecycle rules.
14. Do not invent unregistered link relations.
15. Generate the standard profile structure.
16. Include a realistic HAL example.
17. Include explicit compatibility mappings for existing URI properties.
18. Include a numbered Conformance section.
19. Verify every MUST/SHOULD statement is supported by:
    - OpenAPI,
    - a registered relation,
    - an applicable IRI specification, or
    - a clearly identified interoperability rule introduced by the profile.
20. Review the finished document for accidental conflict with OpenAPI.

---

## 27. Final Validation Checklist

Before considering a profile complete, verify all of the following:

- The canonical profile URI is correct.
- The OpenAPI schema name is correct.
- The property table matches current V2 OpenAPI.
- Required vs optional properties are correct.
- Nullable properties are correctly described.
- No obsolete V1 enum or property semantics were imported.
- No unregistered `iri:*` relation was invented.
- Registered relation cardinalities are preserved.
- Relation names use lowercase kebab-case.
- Legacy URI properties remain authoritative during additive HAL migration.
- HAL links and legacy URI properties agree when both are present.
- No `href: null` is emitted.
- `_links.self` is used appropriately.
- Resource Type values use DOE-IRI URNs where defined by V2.
- Profile URIs, Resource Type URNs, relation identifiers, and instance URIs are
  clearly distinguished.
- Lifecycle transitions are not invented.
- Historical and current state are distinguished.
- Authorization and visibility are addressed.
- Operation affordances do not replace OpenAPI.
- The profile does not unnecessarily duplicate OpenAPI.
- The Conformance section summarizes the important interoperability rules.
- Repository or GitHub URLs are not used as canonical profile identifiers.
