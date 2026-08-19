Refactor the DOE-IRI registry documentation to separate Resource Definition
profiles from the existing Status Resource profile and from the DOE-IRI URN
registry.

Repository:
doe-iri/iri-facility-api-docs

Read AGENTS.md before making changes.

IMPORTANT:
- Do not change the OpenAPI schemas as part of this work.
- Do not change the canonical profile URI of:
    https://iri.science/profiles/status/resource
- Do not move:
    registry/profiles/status/resource.md
- Preserve existing normative semantics unless a change is required solely to
  separate Resource Definition semantics from URN registration.
- Use git mv when a source document is substantially becoming a destination
  document so Git history is preserved.
- Do not invent new Resource Types, controlled vocabulary values, HAL relations,
  attributes, or lifecycle semantics.
- Search the entire repository for old paths and update references after the
  reorganization.

===============================================================================
1. TARGET ARCHITECTURE
===============================================================================

Restructure the relevant registry content toward:

```
registry/
│
├── profiles/
│   ├── status/
│   │   ├── resource.md
│   │   ├── event.md
│   │   └── incident.md
│   │
│   └── resource-definition/
│       ├── compute/
│       │   ├── system.md
│       │   ├── node.md
│       │   ├── cpu.md
│       │   └── gpu.md
│       │
│       ├── storage/
│       │   ├── system.md
│       │   ├── filesystem.md
│       │   ├── mount.md
│       │   ├── block.md
│       │   └── object.md
│       │
│       └── service/
│           ├── dtn.md
│           └── inference.md
│
├── urns/
│   ├── README.md
│   ├── resource-types.md
│   └── attributes.md
│
├── relations/
│   └── ...
│
└── README.md
```

Do not move or restructure registry/relations as part of this work.

Do not move account, job, task, facility, event, or incident representation
profiles except for updating links that point to relocated documents.

===============================================================================
2. RESOURCE DEFINITION PROFILE MODEL
===============================================================================

The documents under:

    registry/profiles/resource-definition/

are specializations of the generic IRI Resource representation.

The base profile remains:

    https://iri.science/profiles/status/resource

A Resource Definition profile is selected by the Resource's resource_type.

For example:

    resource_type = urn:doe-iri:resource:compute:system

means that the Resource:

1. conforms to the common Resource representation/profile defined by:

       https://iri.science/profiles/status/resource

2. and additionally conforms to the Resource Definition profile:

       https://iri.science/profiles/resource-definition/compute/system

The hierarchy is conceptual:

    OpenAPI Resource schema
            ↓
    IRI Status Resource Profile
    https://iri.science/profiles/status/resource
            ↓
    resource_type selects a specialization
            ↓
    IRI Resource Definition Profile
    https://iri.science/profiles/resource-definition/<domain>/<type>

Do NOT redefine the common Resource properties in every Resource Definition
profile.

The common Resource representation remains defined by the OpenAPI Resource
schema and registry/profiles/status/resource.md.

Resource Definition profiles define only semantics that apply because of the
specific resource_type, including as applicable:

- type-specific attributes;
- controlled vocabulary usage;
- relatively stable characteristics;
- type-specific relationships;
- type-specific operation affordances;
- interpretation rules;
- type-specific conformance requirements.

Dynamic operational state does NOT belong in Resource Definition profiles.

Examples of information that should NOT be treated as Resource Definition
attributes include:

- current utilization;
- current availability;
- free memory;
- queue depth;
- current health;
- current capacity remaining;
- current workload activity.

===============================================================================
3. MOVE/CONVERT THE EXISTING ATTRIBUTE PROFILE DOCUMENTS
===============================================================================

Create the target directories:

    mkdir -p registry/profiles/resource-definition/compute
    mkdir -p registry/profiles/resource-definition/storage
    mkdir -p registry/profiles/resource-definition/service
    mkdir -p registry/urns

Move the existing type-specific attribute documents with git mv:

COMPUTE

    git mv \
      registry/urn-registry-attributes-compute-system.md \
      registry/profiles/resource-definition/compute/system.md

    git mv \
      registry/urn-registry-attributes-compute-node.md \
      registry/profiles/resource-definition/compute/node.md

    git mv \
      registry/urn-registry-attributes-compute-cpu.md \
      registry/profiles/resource-definition/compute/cpu.md

    git mv \
      registry/urn-registry-attributes-compute-gpu.md \
      registry/profiles/resource-definition/compute/gpu.md

STORAGE

    git mv \
      registry/urn-registry-attributes-storage-system.md \
      registry/profiles/resource-definition/storage/system.md

    git mv \
      registry/urn-registry-attributes-storage-filesystem.md \
      registry/profiles/resource-definition/storage/filesystem.md

    git mv \
      registry/urn-registry-attributes-storage-mount.md \
      registry/profiles/resource-definition/storage/mount.md

    git mv \
      registry/urn-registry-attributes-storage-block.md \
      registry/profiles/resource-definition/storage/block.md

    git mv \
      registry/urn-registry-attributes-storage-object.md \
      registry/profiles/resource-definition/storage/object.md

SERVICE

    git mv \
      registry/urn-registry-attributes-service-dtn.md \
      registry/profiles/resource-definition/service/dtn.md

    git mv \
      registry/urn-registry-attributes-service-inference.md \
      registry/profiles/resource-definition/service/inference.md

===============================================================================
4. CONVERT THE MOVED DOCUMENTS INTO RESOURCE DEFINITION PROFILES
===============================================================================

Update each moved file so that it is explicitly a Resource Definition profile,
not a URN registry document.

For example, change the compute-system document header to approximately:

    # IRI Compute System Resource Definition Profile

    **Profile URI:** `https://iri.science/profiles/resource-definition/compute/system`
    **Base Profile:** `https://iri.science/profiles/status/resource`
    **Resource Type:** `urn:doe-iri:resource:compute:system`
    **Status:** Draft
    **Version:** 1.0.0

Add an applicability section near the beginning with semantics equivalent to:

    ## Profile Applicability

    This profile applies to an IRI Resource representation whose
    `resource_type` is:

    `urn:doe-iri:resource:compute:system`

    This profile specializes the IRI Status Resource Profile:

    `https://iri.science/profiles/status/resource`

    A representation conforming to this profile MUST also satisfy the
    requirements of the base IRI Status Resource Profile.

Use the equivalent canonical values for every moved document.

Expected mapping:

```
Compute System
    Profile:
      https://iri.science/profiles/resource-definition/compute/system
    Resource Type:
      urn:doe-iri:resource:compute:system

Compute Node
    Profile:
      https://iri.science/profiles/resource-definition/compute/node
    Resource Type:
      urn:doe-iri:resource:compute:node

CPU
    Profile:
      https://iri.science/profiles/resource-definition/compute/cpu
    Resource Type:
      urn:doe-iri:resource:compute:cpu

GPU
    Profile:
      https://iri.science/profiles/resource-definition/compute/gpu
    Resource Type:
      urn:doe-iri:resource:compute:gpu

Storage System
    Profile:
      https://iri.science/profiles/resource-definition/storage/system
    Resource Type:
      urn:doe-iri:resource:storage:system

Filesystem
    Profile:
      https://iri.science/profiles/resource-definition/storage/filesystem
    Resource Type:
      urn:doe-iri:resource:storage:filesystem

Filesystem Mount
    Profile:
      https://iri.science/profiles/resource-definition/storage/mount
    Resource Type:
      urn:doe-iri:resource:storage:mount

Block Storage
    Profile:
      https://iri.science/profiles/resource-definition/storage/block
    Resource Type:
      urn:doe-iri:resource:storage:block

Object Storage
    Profile:
      https://iri.science/profiles/resource-definition/storage/object
    Resource Type:
      urn:doe-iri:resource:storage:object

DTN Service
    Profile:
      https://iri.science/profiles/resource-definition/service/dtn
    Resource Type:
      urn:doe-iri:resource:service:dtn

Inference Service
    Profile:
      https://iri.science/profiles/resource-definition/service/inference
    Resource Type:
      urn:doe-iri:resource:service:inference
```

Retain the existing useful content from these files, including:

- attribute definitions;
- JSON Schema fragments;
- examples;
- controlled-vocabulary references;
- distinctions between configured/static information and dynamic state;
- applicable relationship descriptions.

However, remove or relocate sections whose only purpose is to REGISTER a URN.
Registration belongs under registry/urns/.

A Resource Definition profile MAY reference registered URNs, but MUST NOT be
the authoritative registry entry for those URNs.

===============================================================================
5. CREATE registry/urns/README.md
===============================================================================

Use the current:

    registry/urn-registry-root.md

as the starting source for:

    registry/urns/README.md

Use git mv if practical:

    git mv registry/urn-registry-root.md registry/urns/README.md

Refactor it into the entry point for the DOE-IRI URN Registry.

It should:

- identify `urn:doe-iri:` as the namespace root;
- explain that the governing RFC defines syntax, matching, registration,
  delegation, and extension rules;
- explain that this directory records assigned identifiers;
- show the top-level URN branches;
- link to:
    - resource-types.md
    - attributes.md
- retain registry information that does not belong in either of those two files,
  including the existing allocation-unit, compression, and extension-
  administration material unless there is already another canonical registry
  location for it.

Update relative links to the governing RFC because the file is now one
directory deeper.

For example, a former reference such as:

    ../rfc/rfc-iri-urn-structure-and-registry.md

will likely need to become:

    ../../rfc/rfc-iri-urn-structure-and-registry.md

Verify every relative path rather than applying blind string substitution.

===============================================================================
6. CREATE registry/urns/resource-types.md
===============================================================================

Create:

    registry/urns/resource-types.md

This document becomes the authoritative registry/index of assigned:

    urn:doe-iri:resource:*

Resource Type URNs.

Consolidate the Resource Type registration material currently distributed
across:

    registry/urn-registry-root.md
    registry/urn-registry-type-compute.md
    registry/urn-registry-type-compute-taxonomy.md
    registry/urn-registry-type-storage.md
    registry/urn-registry-type-storage-taxonomy.md
    registry/urn-registry-type-service.md
    registry/urn-registry-type-service-taxonomy.md

Do not copy large amounts of Resource Definition prose into this registry.

The purpose of resource-types.md is to answer:

    What Resource Type URNs are registered?
    What do they identify?
    What is their parent?
    What is their lifecycle status?
    Where is their Resource Definition profile?

Include at minimum:

- canonical URN;
- short name;
- semantic definition;
- parent Resource Type URN where applicable;
- lifecycle/status;
- legacy mapping where applicable;
- link to the applicable Resource Definition profile where one exists.

For refined types, link to the new profile files.

Example conceptual row:

    urn:doe-iri:resource:compute:system
        Short name: Compute System
        Parent: urn:doe-iri:resource:compute
        Status: provisional
        Definition profile:
          ../profiles/resource-definition/compute/system.md

The generic parent types:

    urn:doe-iri:resource:compute
    urn:doe-iri:resource:storage
    urn:doe-iri:resource:service

remain registered Resource Type URNs.

Do NOT create a Resource Definition profile for those generic parent types as
part of this change unless there is existing type-specific representation
content that cannot be represented cleanly in the Resource Type registry or
the child profiles.

The current broad domain-model prose from the old type documents should be
handled carefully:

- Keep actual URN classification/registration semantics in resource-types.md.
- Move type-specific Resource representation semantics to the appropriate
  child Resource Definition profiles.
- Do not duplicate relation definitions; link to registry/relations instead.
- Do not duplicate controlled attribute registries; link to attributes.md.

===============================================================================
7. CREATE registry/urns/attributes.md
===============================================================================

Create:

    registry/urns/attributes.md

This document becomes the authoritative consolidated registry/index for
controlled DOE-IRI attribute URNs used by Resource Definition profiles.

Consolidate controlled attribute URN registrations currently distributed
across:

    registry/urn-registry-type-compute.md
    registry/urn-registry-type-compute-taxonomy.md
    registry/urn-registry-attributes-compute-*.md

    registry/urn-registry-type-storage.md
    registry/urn-registry-type-storage-taxonomy.md
    registry/urn-registry-attributes-storage-*.md

    registry/urn-registry-type-service.md
    registry/urn-registry-type-service-taxonomy.md
    registry/urn-registry-attributes-service-*.md

This file should answer:

    What controlled attribute URNs are registered?
    What attribute/vocabulary do they belong to?
    What do they mean?
    What is their lifecycle status?
    Which Resource Definition profile uses them?

Organize the file by semantic domain, for example:

    Compute
      system-capability
      node-role
      cpu-architecture
      gpu-programming-interface

    Storage
      ...

    Service
      ...

Do NOT move ordinary JSON property definitions such as:

    configured_node_count
    configured_memory_gib
    vendor
    product
    version

into attributes.md merely because they are attributes.

Only the controlled DOE-IRI URNs and their registry metadata belong in the URN
attribute registry.

The JSON attribute property definitions remain in the appropriate Resource
Definition profile.

===============================================================================
8. REMOVE THE OLD MIXED-PURPOSE REGISTRY DOCUMENTS
===============================================================================

After all content has been accounted for and references have been updated,
remove the obsolete old domain/type/taxonomy files:

    registry/urn-registry-type-compute.md
    registry/urn-registry-type-compute-taxonomy.md

    registry/urn-registry-type-storage.md
    registry/urn-registry-type-storage-taxonomy.md

    registry/urn-registry-type-service.md
    registry/urn-registry-type-service-taxonomy.md

Do not delete them until you have verified that their normative/registry
content exists in the new locations.

The old urn-registry-attributes-* files should already have been moved with
git mv and transformed into Resource Definition profiles.

At the end there should be no remaining authoritative files matching:

    registry/urn-registry-type-*.md
    registry/urn-registry-attributes-*.md

unless you identify a file that does not fit the new model. If so, stop and
report it rather than deleting content.

===============================================================================
9. UPDATE registry/profiles/status/resource.md
===============================================================================

DO NOT MOVE:

    registry/profiles/status/resource.md

DO NOT change its canonical URI:

    https://iri.science/profiles/status/resource

Make only the changes necessary to explain the new Resource Definition profile
layer and update references.

In the section covering resource_type/type-specific attributes, explain
semantics equivalent to:

    The common Resource profile defines semantics applicable to all IRI Resource
    representations.

    More-specific Resource Definition profiles MAY apply according to the
    registered `resource_type`.

    For example:

      resource_type =
        urn:doe-iri:resource:compute:system

    identifies the applicable Resource Definition profile:

      https://iri.science/profiles/resource-definition/compute/system

A generic client MUST still be able to process the common Resource
representation without understanding the more-specific Resource Definition
profile.

Do not move current status/event/incident semantics into
resource-definition/.

The purpose of this restructuring is specifically to prepare for future
separation of Resource Definition and Resource State.

===============================================================================
10. UPDATE registry/README.md
===============================================================================

Rewrite the registry structure/navigation section to reflect the new model.

The high-level conceptual model should distinguish:

    Representation Profiles
    Resource Definition Profiles
    URN Registries
    Link Relation Definitions

Use wording equivalent to:

    profiles/status/resource.md
        Common Resource representation semantics

    profiles/resource-definition/<domain>/<type>.md
        Type-specific Resource Definition semantics selected by resource_type

    urns/resource-types.md
        Registration of Resource Type URNs

    urns/attributes.md
        Registration of controlled attribute URNs

    relations/
        Registration and complete semantics of link relations

Make clear that:

- a Resource Type URN is not a profile URI;
- a Resource Definition profile is selected based on resource_type;
- the Resource Definition profile does not replace the base Resource profile;
- URN registry documents register identifiers;
- Resource Definition profiles define representation semantics for Resources
  of a particular type.

===============================================================================
11. UPDATE AGENTS.md
===============================================================================

Update AGENTS.md so Codex uses the new structure.

Remove references to:

    registry/urn-registry-type-*.md
    registry/urn-registry-attributes-*.md

Replace them with the appropriate current sources:

    registry/urns/README.md
    registry/urns/resource-types.md
    registry/urns/attributes.md
    registry/profiles/resource-definition/

Add or update a rule equivalent to:

    Resource Definition profiles specialize the common
    `https://iri.science/profiles/status/resource` representation according to
    `resource_type`.

    Resource Definition profiles belong under:

      registry/profiles/resource-definition/<domain>/<type>.md

    Their canonical profile URI is:

      https://iri.science/profiles/resource-definition/<domain>/<type>

    DOE-IRI Resource Type URN registration belongs in:

      registry/urns/resource-types.md

    Controlled attribute URN registration belongs in:

      registry/urns/attributes.md

    A Resource Definition profile MAY reference registered URNs but MUST NOT
    become the authoritative registration record for those URNs.

Preserve the existing source-of-truth rules:

- OpenAPI controls JSON structure.
- URN specifications control namespace rules.
- registry/urns/* controls assigned URNs.
- registry/relations/* controls relation semantics.
- representation/resource-definition profiles control representation-specific
  semantic conventions.

===============================================================================
12. UPDATE ALL LINKS AND REFERENCES
===============================================================================

Search the entire repository for all references to:

    urn-registry-root.md
    urn-registry-type-
    urn-registry-attributes-

Also search for references to the old profile terminology:

    "Attribute Profile"
    "Resource attribute profile"
    "Type Registry"

Update links and terminology where the referenced document now represents a
Resource Definition profile or URN registry.

Do not blindly rewrite historical design documents under docs/superpowers/
unless necessary to keep their links functional.

Historical prose describing what existed at the time MAY remain historical,
but links should point to the current document when that does not distort the
historical meaning.

Verify relative links in:

- registry/README.md
- registry/profiles/**
- registry/relations/**
- rfc/**
- specification documentation
- AGENTS.md
- docs/** where appropriate

===============================================================================
13. RESOURCE DEFINITION PROFILE TERMINOLOGY
===============================================================================

For the moved type-specific documents, prefer:

    "Resource Definition Profile"

rather than:

    "Attribute Profile"

when referring to the complete document.

The attributes inside the Resource Definition profile remain "attributes".

For example:

    # IRI Compute System Resource Definition Profile

not:

    # Attribute Profile: urn:doe-iri:resource:compute:system

The Resource Type URN remains:

    urn:doe-iri:resource:compute:system

The profile identifier is separately:

    https://iri.science/profiles/resource-definition/compute/system

Do not conflate these identifiers.

===============================================================================
14. VALIDATION
===============================================================================

Before finishing, run checks equivalent to:

    git status --short

    find registry -maxdepth 5 -type f | sort

    grep -R "urn-registry-type-" -n \
      --exclude-dir=.git .

    grep -R "urn-registry-attributes-" -n \
      --exclude-dir=.git .

    grep -R "urn-registry-root.md" -n \
      --exclude-dir=.git .

    grep -R "profiles/resource-definition" -n \
      registry AGENTS.md rfc docs specification-v2 2>/dev/null || true

If the repository has an existing Markdown/link validation command, run it.

Also inspect:

    git diff --check
    git diff --stat
    git diff

Verify specifically that:

1. registry/profiles/status/resource.md remains in place.
2. Its canonical URI is still:
       https://iri.science/profiles/status/resource
3. Every refined Resource Definition file is under:
       registry/profiles/resource-definition/
4. Every Resource Definition profile has:
       - Profile URI
       - Base Profile
       - Resource Type
       - Status
       - Version
5. Resource Type URNs are registered in:
       registry/urns/resource-types.md
6. Controlled attribute URNs are registered in:
       registry/urns/attributes.md
7. No Resource Definition profile is treated as the authoritative URN
   registration source.
8. No controlled URN was accidentally dropped during consolidation.
9. No registered Resource Type was accidentally dropped.
10. Existing registered HAL relation names or semantics were not changed.
11. No dynamic operational-state attribute was moved into a Resource Definition
    profile as a static definition.
12. No old authoritative urn-registry-type-* or
    urn-registry-attributes-* files remain after migration.

At completion, provide:

- a concise summary of the new structure;
- the exact old → new file mapping;
- a list of deleted/consolidated files;
- any content that could not be cleanly classified;
- validation commands run and their results.

Do not commit or push the changes unless explicitly requested.
