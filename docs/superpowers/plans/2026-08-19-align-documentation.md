Review and align the remaining DOE-IRI RFC, registry, profile, relation, and
OpenAPI documentation with the recently committed:

    rfc/rfc-type-specific-attributes.md

Repository:
    doe-iri/iri-facility-api-docs

Read the repository's local AGENTS.md instructions before making changes.

The newly committed rfc/rfc-type-specific-attributes.md is the architectural
baseline for this work.

IMPORTANT DESIGN CONSTRAINT

IRI v2 does NOT introduce or require separate Resource Definition and Resource
State API representations.

Resource Definition Profiles specialize the existing IRI v2 Resource
representation according to resource_type.

Do not introduce:
- a ResourceDefinition API object;
- a ResourceState API object;
- a Resource State endpoint;
- a requirement that dynamic values MUST be moved to separate state resources;
- a new HAL state relation solely to prepare for IRI v3.

IRI v3 may introduce a definition/state separation later, but that architecture
is explicitly outside the scope of this cleanup.

At the same time, preserve useful semantic distinctions such as:
- current_status vs Event history;
- configured topology vs current reachability;
- capability support vs current availability;
- a relationship existing vs the target currently being healthy;
- Task state and Job state.

The goal is to remove architectural prescriptions for separate state
representations, not to erase legitimate semantics concerning current
condition.

Do not commit or push unless explicitly requested.

===============================================================================
PHASE 1 — FIX CANONICAL PROFILE URI ERRORS
===============================================================================

Correct known stale or erroneous target representation profile URIs.

1. registry/relations/generated-by.md

The target is an Incident, but the document currently incorrectly identifies:

    https://iri.science/profiles/storage/mount

Replace the target representation profile with:

    https://iri.science/profiles/status/incident

Update every occurrence in that relation document.

2. registry/relations/has-mount.md

Replace:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/resource-definition/storage/mount

3. registry/relations/accesses-mount.md

Replace:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/resource-definition/storage/mount

4. registry/relations/attached-to.md

Replace:

    https://iri.science/profiles/compute/system

with:

    https://iri.science/profiles/resource-definition/compute/system

and:

    https://iri.science/profiles/compute/node

with:

    https://iri.science/profiles/resource-definition/compute/node

5. rfc/rfc-hal-links.md

Replace the obsolete mount profile:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/resource-definition/storage/mount

6. Search the complete current normative tree for additional old Resource
Definition profile identifiers.

At minimum search:

    grep -R "https://iri.science/profiles/storage/" \
        registry rfc specification-v2 README.md 2>/dev/null || true

    grep -R "https://iri.science/profiles/compute/system" \
        registry rfc specification-v2 README.md 2>/dev/null || true

    grep -R "https://iri.science/profiles/compute/node" \
        registry rfc specification-v2 README.md 2>/dev/null || true

    grep -R "https://iri.science/profiles/compute/cpu" \
        registry rfc specification-v2 README.md 2>/dev/null || true

    grep -R "https://iri.science/profiles/compute/gpu" \
        registry rfc specification-v2 README.md 2>/dev/null || true

Canonical Resource Definition profile identifiers are:

    https://iri.science/profiles/resource-definition/compute/system
    https://iri.science/profiles/resource-definition/compute/node
    https://iri.science/profiles/resource-definition/compute/cpu
    https://iri.science/profiles/resource-definition/compute/gpu

    https://iri.science/profiles/resource-definition/storage/system
    https://iri.science/profiles/resource-definition/storage/filesystem
    https://iri.science/profiles/resource-definition/storage/mount
    https://iri.science/profiles/resource-definition/storage/block
    https://iri.science/profiles/resource-definition/storage/object

    https://iri.science/profiles/resource-definition/service/dtn
    https://iri.science/profiles/resource-definition/service/inference

Do not change representation profiles such as:

    https://iri.science/profiles/status/resource
    https://iri.science/profiles/status/event
    https://iri.science/profiles/status/incident
    https://iri.science/profiles/facility
    https://iri.science/profiles/facility/site
    https://iri.science/profiles/account/...
    https://iri.science/profiles/compute/job
    https://iri.science/profiles/task

unless another verified inconsistency exists.

===============================================================================
PHASE 2 — ALIGN ALLOCATION UNIT URNS
===============================================================================

The governing URN RFC and current V2 OpenAPI use hierarchical allocation-unit
URNs:

    urn:doe-iri:allocation:compute:node-hours
    urn:doe-iri:allocation:storage:bytes
    urn:doe-iri:allocation:storage:inodes

Make these the canonical registered values.

Update:

    registry/urns/README.md

which currently contains the obsolete flat forms:

    urn:doe-iri:allocation:node-hours
    urn:doe-iri:allocation:bytes
    urn:doe-iri:allocation:inodes

to:

    urn:doe-iri:allocation:compute:node-hours
    urn:doe-iri:allocation:storage:bytes
    urn:doe-iri:allocation:storage:inodes

Search all current normative material for the obsolete forms:

    grep -R "urn:doe-iri:allocation:node-hours" \
        registry rfc specification-v2 README.md 2>/dev/null || true

    grep -R "urn:doe-iri:allocation:bytes" \
        registry rfc specification-v2 README.md 2>/dev/null || true

    grep -R "urn:doe-iri:allocation:inodes" \
        registry rfc specification-v2 README.md 2>/dev/null || true

Update current normative examples and documentation to the hierarchical forms.

Do not rewrite specification-v1 historical material.

===============================================================================
PHASE 3 — REMOVE THE UNREGISTERED scratch RESOURCE TYPE
===============================================================================

The current Resource Type Registry registers:

    urn:doe-iri:resource:storage:filesystem

but does NOT register:

    urn:doe-iri:resource:storage:filesystem:scratch

The current controlled attribute registry instead represents scratch semantics
using:

    tier = urn:doe-iri:storage:tier:scratch

Align current normative material to this model.

1. Update:

    registry/profiles/status/resource.md

Remove examples and normative guidance treating:

    urn:doe-iri:resource:storage:filesystem:scratch

as a registered Resource Type.

Where a scratch filesystem example is useful, use:

    resource_type =
      urn:doe-iri:resource:storage:filesystem

and:

    attributes.tier =
      urn:doe-iri:storage:tier:scratch

Do NOT create or register filesystem:scratch as part of this work.

2. Update:

    rfc/rfc-iri-urn-structure-and-registry.md

Remove filesystem:scratch as an example of a canonical registered Resource Type.

For hierarchy examples, use known registered values such as:

    urn:doe-iri:resource:storage
        ↓
    urn:doe-iri:resource:storage:filesystem

or another actually registered parent/child pair.

In Appendix A, replace/remove the filesystem:scratch Resource Type entry.

If a scratch example is desirable, show it as the controlled value:

    urn:doe-iri:storage:tier:scratch

rather than as a Resource Type.

3. Search:

    grep -R "resource:storage:filesystem:scratch" \
        registry rfc specification-v2 README.md 2>/dev/null || true

No current normative document should claim this is a registered shared
Resource Type when this phase is complete.

===============================================================================
PHASE 4 — ALIGN THE COMMON RESOURCE PROFILE WITH CURRENT OPENAPI AND THE NEW RFC
===============================================================================

Update:

    registry/profiles/status/resource.md

1. Structural Contract

The current V2 OpenAPI Resource schema includes optional/nullable:

    attributes

Add it to the structural-contract property table.

Use semantics equivalent to:

    | `attributes` | No | Optional type-specific metadata whose semantics
      are defined by the applicable Resource Definition Profile selected by
      `resource_type`. |

Document that OpenAPI remains authoritative for:
- optionality;
- nullability;
- object structure;
- additionalProperties behavior.

Do not incorrectly make attributes mandatory or non-null.

2. Resource Definition Profile semantics

Align the wording with:

    rfc/rfc-type-specific-attributes.md

The Resource Definition Profile:
- supplements the common Resource profile;
- is selected through the registry mapping associated with resource_type;
- defines type-specific attribute semantics, relationships, and operation
  affordances as applicable;
- does not replace the common Resource representation;
- does not define a separate IRI v2 Resource Definition API object.

Remove blanket wording that implies Resource Definition Profiles can contain
only "relatively stable" attributes if that wording conflicts with the new RFC.

A Resource Definition Profile may itself constrain the meaning of its own
attributes. Do not globally prohibit time-varying attributes merely because
IRI v3 may later separate definition and state.

3. Keep current_status

Do NOT remove or relocate current_status.

Keep the distinction:

    Resource.current_status
        current reported Resource status

    Event.status
        status associated with the historical Event at occurred_at

This distinction remains valid in IRI v2 and does not imply a separate
ResourceState representation.

===============================================================================
PHASE 5 — REMOVE IRI v2 PRESCRIPTIONS FOR A SEPARATE STATE REPRESENTATION
===============================================================================

Perform a focused semantic audit of:

    registry/README.md
    registry/profiles/resource-definition/**
    registry/relations/**
    rfc/rfc-hal-links.md

Search for phrases such as:

    resource state
    resource-state
    state representation
    state resource
    state object
    state mechanism
    state mechanisms
    dynamic state resource
    dynamic state resources
    represented separately
    MUST be represented separately
    SHOULD be represented separately
    separate state

Do NOT mechanically delete every occurrence.

Apply these rules:

A. KEEP useful negative relation semantics.

For example, preserve statements equivalent to:

    iri:has-mount does not prove that the mount is currently active,
    reachable, healthy, or usable.

    iri:attached-to does not prove that a block device is currently logged
    in, mapped, healthy, or accessible.

    iri:hosted-on does not prove that a service is currently reachable.

These describe the meaning of a relationship and are valuable.

B. REMOVE architectural prescriptions requiring a separate v2 state object.

For example, change:

    Current attachment state MUST be represented separately.

to something equivalent to:

    Current attachment condition is outside the semantics of this relation
    and, when represented, is governed by the applicable IRI API contract.

Change:

    Dynamic operational information ... SHOULD be represented through the
    corresponding resource-state mechanisms.

to wording equivalent to:

    The semantics of operational or time-varying values are governed by the
    applicable IRI API contract and Resource Definition Profile.

If a particular Resource Definition Profile intentionally excludes a specific
value, it MAY continue to say that value is outside that profile's scope.

It MUST NOT claim that IRI v2 therefore requires a separate Resource State
representation.

C. registry/README.md

The current README says dynamic health, capacity, utilization, availability,
transfer activity, and workload activity are "state, not Resource Definition
attributes."

Replace that blanket architecture rule with wording equivalent to:

    Resource Type URNs classify a Resource. Resource Definition Profiles define
    additional type-specific semantics selected by resource_type. A profile may
    define configuration, descriptive metadata, capabilities, quantitative
    values, or time-varying observations as appropriate to that Resource type.

    IRI v2 does not require a separate Resource Definition / Resource State
    representation model. A future separation is outside the scope of IRI v2.

Do not add detailed IRI v3 design to current v2 documentation.

D. rfc/rfc-hal-links.md

Remove language that assumes "dynamic state resources" are an established
IRI v2 architectural layer when no current registered relationship or API
contract establishes such a representation.

Examples:

- Abstract/scope should focus on:
    related resources,
    topology,
    operation entry points,
    navigable URI-property migration,
    service descriptions.

- Replace questions such as:
    "Which resource exposes current state or capacity information?"
  with wording that does not assume a distinct state resource.

- Do not invent a state relation.

===============================================================================
PHASE 6 — UPDATE rfc/rfc-hal-links.md FOR CURRENT V2
===============================================================================

In addition to Phase 5:

1. Remove the obsolete statement that current v2 ResourceType is still a
legacy enum requiring later OpenAPI migration.

Current V2 resource_type is already an extensible string carrying a DOE-IRI
Resource Type URN.

Use wording equivalent to:

    The examples use the current V2 Resource Type URN model. This RFC does not
    assign Resource Type URNs; the DOE-IRI URN Registry is authoritative for
    registered values.

2. Correct the mount profile URI to:

    https://iri.science/profiles/resource-definition/storage/mount

3. Replace wording such as:

    consult the registered profile for each iri:* relation

with:

    consult the registered relation definition for each iri:* relation

A link relation definition is not a representation profile.

4. Preserve the existing mapping:

    TaskSubmitResponse.task_uri -> monitor

This mapping is correct.

5. Preserve lowercase kebab-case requirements for iri:* relations.

===============================================================================
PHASE 7 — FIX TASK HYPERMEDIA SEMANTICS
===============================================================================

Update:

    registry/profiles/task.md

The current profile directly depicts:

    TaskSubmitResponse.task_uri
            ↓
    Task._links.self.href

Align it with the HAL RFC.

The semantic chain should be:

    asynchronous operation
            ↓
    TaskSubmitResponse
            │
            ├── task_id
            └── task_uri
                    │
                    ▼
            _links.monitor.href
                    │
                    ▼
              Task representation
                    │
                    ▼
              Task._links.self.href

Clarify:

- task_uri identifies the Task used to monitor the asynchronous operation.
- In a HAL-enabled TaskSubmitResponse, task_uri maps to the standard `monitor`
  relation.
- `monitor` describes WHY the response links to the Task.
- `self` identifies the Task's canonical representation once the Task itself
  is retrieved.
- monitor.href and Task._links.self.href may identify the same URI while having
  different relation semantics.
- Do not invent an iri:monitor or Task-specific replacement for the standard
  `monitor` relation.

Add a small HAL TaskSubmitResponse example if useful:

    {
      "task_id": "task-123",
      "task_uri": "https://api.example.org/api/v2/task/task-123",
      "_links": {
        "monitor": {
          "href": "https://api.example.org/api/v2/task/task-123",
          "type": "application/hal+json",
          "profile": "https://iri.science/profiles/task"
        }
      }
    }

Keep Task._links.self on the Task representation itself.

===============================================================================
PHASE 8 — NORMALIZE RESOURCE DEFINITION PROFILE TERMINOLOGY
===============================================================================

The moved Resource Definition Profile files still contain legacy terms such as:

    Attribute Profile
    Storage Attribute Profile
    Filesystem Attribute Profile
    corresponding attribute profile
    resource attribute profile

Align terminology with the newly committed RFC.

Search:

    grep -R -n -E \
      "Attribute Profile|attribute profile|attributes profile" \
      registry/profiles/resource-definition

Prefer:

    Resource Definition Profile

when referring to the complete semantic document.

When referring specifically to the table/schema of attributes within a Resource
Definition Profile, use wording such as:

    "Attributes"
    "Type-Specific Attributes"
    "Attribute Contract"

For example:

    ## 4. Storage Attribute Profile

could become:

    ## 4. Storage System Attributes

Do NOT mechanically change ordinary uses of the word "attribute".

Do not move the files.

Do not change their canonical profile URIs.

===============================================================================
PHASE 9 — NORMALIZE REMAINING CAMELCASE RELATION EXAMPLES
===============================================================================

Current normative registry/profile material should use registered lowercase
kebab-case CURIEs.

Search for likely old names, including:

    providesFilesystem
    providesBlock
    providesObject
    hasMount
    mountedOn
    attachedTo
    hasNode
    hasCpu
    hasGpu
    hostedOn
    accessesMount
    submitJob
    generatedBy
    hasCapability
    hasProject
    hasProjectAllocation

Use registered forms such as:

    iri:provides-filesystem
    iri:provides-block
    iri:provides-object
    iri:has-mount
    iri:mounted-on
    iri:attached-to
    iri:has-node
    iri:has-cpu
    iri:has-gpu
    iri:hosted-on
    iri:accesses-mount
    iri:submit-job
    iri:generated-by
    iri:has-capability
    iri:has-project
    iri:has-project-allocation

Apply this to current normative documents under:

    registry/
    rfc/

Do not rewrite historical planning/spec documents under docs/superpowers
unless needed to repair a live link.

Do not change OpenAPI operationId names simply because they are camelCase.

===============================================================================
PHASE 10 — UPDATE NAVIGATION AND RFC INDEX TEXT
===============================================================================

1. registry/relations/README.md

The current final link:

    [Back to the DOE-IRI Registry README](./README.md)

points back to registry/relations/README.md itself.

Change it to:

    [Back to the DOE-IRI Registry README](../README.md)

2. rfc/README.md

Update the description of:

    rfc-type-specific-attributes.md

The current README still describes the old "attribute profile" proposal and
claims the RFC defines necessary OpenAPI changes.

Update the title/summary to reflect the committed RFC:

    Type-Specific Attributes and Resource Definition Profiles for IRI Resource
    Objects

Summarize that it:

- defines semantic use of Resource.attributes;
- uses resource_type to select Resource Definition semantics;
- distinguishes Resource Type URNs from Resource Definition Profiles;
- relies on the current V2 OpenAPI structural contract;
- does not introduce separate Resource Definition/Resource State API objects.

===============================================================================
PHASE 11 — OPENAPI EXAMPLE CLEANUP
===============================================================================

Perform narrowly scoped OpenAPI consistency changes.

1. Resource.resource_type example

Inspect:

    specification-v2/openapi/production/_components.yaml
    specification-v2/openapi/all_spec_v2.yaml

Remove obsolete examples such as:

    urn:doe-iri:service:generic

Use a registered Resource Type such as:

    urn:doe-iri:resource:service

or:

    urn:doe-iri:resource:service:dtn

Prefer examples already registered in:

    registry/urns/resource-types.md

2. Attribute description terminology

For Resource.attributes, replace wording such as:

    resource_type URN selects its attribute profile

with:

    resource_type selects the applicable Resource Definition Profile

Keep the structural contract unchanged.

3. Generated OpenAPI consistency

If all_spec_v2.yaml is generated from production fragments, modify the
authoritative source and regenerate using the repository's existing generation
process rather than editing generated output independently.

===============================================================================
PHASE 12 — AUDIT GENERIC attributes PROPAGATION, BUT DO NOT MAKE A BROAD
           BREAKING CHANGE WITHOUT EVIDENCE
===============================================================================

The current V2 generated components show an `attributes` property on several
schemas other than Resource, with Resource-specific explanatory text.

Examples may include:

    Facility
    Site
    Event
    Incident
    Capability
    Project
    ProjectAllocation
    AllocationEntry
    Container
    ResourceSpec
    others

The newly committed RFC defines Resource.attributes; it does not define a
generic profile-selection mechanism for all API objects.

Determine why those other schemas contain `attributes`.

Possible causes include:
- deliberate base-model inheritance;
- code-generation inheritance;
- an earlier attempt to make attributes universal.

For each non-Resource schema that contains attributes:

1. identify the authoritative model/source that adds it;
2. determine whether another current RFC/profile defines its semantics;
3. report whether its presence appears intentional or inherited accidentally.

DO NOT remove attributes from multiple existing API schemas in this cleanup
unless the repository clearly establishes that they are generation artifacts
and removing them is intended.

Instead, report the findings separately at completion.

This avoids turning a documentation consistency cleanup into an unreviewed API
contract change.

===============================================================================
PHASE 13 — VALIDATION
===============================================================================

Run the repository's normal Markdown/link/OpenAPI validation commands if they
exist.

Also run:

    git diff --check
    git status --short
    git diff --stat
    git diff

Search for stale profile URIs:

    grep -R "https://iri.science/profiles/storage/" \
        registry rfc specification-v2 2>/dev/null || true

    grep -R -E \
      "https://iri.science/profiles/compute/(system|node|cpu|gpu)" \
      registry rfc specification-v2 2>/dev/null || true

Search for the unregistered scratch Resource Type:

    grep -R "urn:doe-iri:resource:storage:filesystem:scratch" \
        registry rfc specification-v2 2>/dev/null || true

Search for old allocation units:

    grep -R -E \
      "urn:doe-iri:allocation:(node-hours|bytes|inodes)" \
      registry rfc specification-v2 2>/dev/null || true

Search for old Resource Definition terminology:

    grep -R -n -E \
      "Attribute Profile|attribute profile|attributes profile" \
      registry/profiles/resource-definition \
      rfc/rfc-hal-links.md \
      registry/README.md 2>/dev/null || true

Search for v2 state-separation prescriptions:

    grep -R -n -E \
      "resource-state|Resource State|state representation|state resource|state object|state mechanism|state mechanisms|represented separately" \
      registry rfc 2>/dev/null || true

Review every match manually. Some uses such as Task state, Job state,
current_status, and historical Event status are legitimate and MUST remain.

Search for likely camelCase relation names:

    grep -R -n -E \
      "providesFilesystem|providesBlock|providesObject|hasMount|mountedOn|attachedTo|hasNode|hasCpu|hasGpu|hostedOn|accessesMount|submitJob|generatedBy|hasCapability|hasProjectAllocation|hasProject" \
      registry rfc 2>/dev/null || true

Again, do not change unrelated OpenAPI operationId or programming-language
symbols.

===============================================================================
PHASE 14 — FINAL CONSISTENCY REVIEW
===============================================================================

Before completion verify:

1. rfc/rfc-type-specific-attributes.md remains the new committed architectural
   baseline and has not been reverted to the old attribute-profile model.

2. No current RFC or registry document requires a separate Resource State
   representation in IRI v2.

3. Resource.current_status remains part of the current IRI v2 Resource model.

4. Resource Definition Profiles remain:

       https://iri.science/profiles/resource-definition/<domain>/<type>

5. Resource Type URNs remain separately registered under:

       registry/urns/resource-types.md

6. Controlled attribute URNs remain separately registered under:

       registry/urns/attributes.md

7. Link relation semantics remain separately registered under:

       registry/relations/

8. No unregistered filesystem:scratch Resource Type is presented as canonical.

9. Scratch filesystem semantics use the registered storage tier vocabulary when
   needed.

10. Allocation unit URNs agree across:
       rfc/rfc-iri-urn-structure-and-registry.md
       registry/urns/README.md
       specification-v2 OpenAPI

11. TaskSubmitResponse.task_uri maps to standard monitor in HAL.

12. Task._links.self remains the canonical identity of the Task representation.

13. Relation target profile URIs point to the correct current representation
    profiles.

14. Current normative iri:* names use lowercase kebab-case.

15. The relation-index Back link points to registry/README.md.

16. rfc/README.md describes the newly committed RFC accurately.

17. No broad non-Resource OpenAPI attributes removal was made without an
    explicit documented basis.

At completion provide:

- files changed;
- a concise description of each semantic correction;
- stale identifiers removed;
- state-separation language that was changed and why;
- OpenAPI changes made;
- results of the non-Resource attributes audit;
- validation commands and results;
- any remaining ambiguity requiring architectural review.

Do not commit or push unless explicitly instructed.

