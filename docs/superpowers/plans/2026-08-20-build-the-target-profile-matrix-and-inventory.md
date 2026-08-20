Read AGENTS.md first.

Repository:
    doe-iri/iri-facility-api-docs

This is an AUDIT ONLY pass. Do not modify files.

Goal:
Identify every current documentation example containing `_links` and determine
the correct HAL Link Object `profile` value for every link whose target is an
IRI representation with a known canonical profile.

SOURCE OF TRUTH

Use:

    registry/relations/README.md
    registry/relations/*.md
    registry/urns/resource-types.md
    registry/profiles/**
    rfc/rfc-hal-links.md

The `profile` member of a HAL Link Object identifies the semantic profile of
the TARGET representation.

It does NOT identify:
- the link relation;
- the source representation;
- the Resource Type URN;
- an operation contract.

Do not infer profile URIs from path names when the registry provides the
answer.

===============================================================================
1. EXPECTED TARGET PROFILE MATRIX
===============================================================================

Verify the following against the current registry before using it.

STANDARD RELATIONS

self
    Target:
        current representation
    Profile:
        profile of the current representation

    Examples:
        Facility
            https://iri.science/profiles/facility

        Site
            https://iri.science/profiles/facility/site

        Event
            https://iri.science/profiles/status/event

        Incident
            https://iri.science/profiles/status/incident

        generic Resource
            https://iri.science/profiles/status/resource

        compute-system Resource in its Resource Definition Profile example
            https://iri.science/profiles/resource-definition/compute/system

        storage-filesystem Resource in its Resource Definition Profile example
            https://iri.science/profiles/resource-definition/storage/filesystem

        Project
            https://iri.science/profiles/account/project

        Capability
            https://iri.science/profiles/account/capability

        ProjectAllocation
            https://iri.science/profiles/account/project-allocation

        UserAllocation
            https://iri.science/profiles/account/user-allocation

        Job
            https://iri.science/profiles/compute/job

        Task
            https://iri.science/profiles/task


monitor
    Target:
        Task representation

    Profile:
        https://iri.science/profiles/task


help
    Usually targets an external support/help resource rather than an IRI
    representation.

    Do NOT add `profile` unless the example explicitly targets an IRI
    representation with a defined profile.


service-desc
    Targets a machine-readable service description such as OpenAPI.

    Do NOT add an IRI representation `profile`.

    Preserve the appropriate `type`, for example:

        application/vnd.oai.openapi+json;version=3.1


curies
    HAL metadata.

    Do NOT add `profile`.


IRI RELATIONS

iri:located-at
    Target:
        Site
    Profile:
        https://iri.science/profiles/facility/site


iri:has-site
    Target:
        Site
    Profile:
        https://iri.science/profiles/facility/site


iri:generated-by
    Target:
        Incident
    Profile:
        https://iri.science/profiles/status/incident


iri:has-event
    Target:
        Event
    Profile:
        https://iri.science/profiles/status/event


iri:impacts
    Target:
        generic DOE-IRI Resource
    Profile:
        https://iri.science/profiles/status/resource


iri:may-impact
    Target:
        generic DOE-IRI Resource
    Profile:
        https://iri.science/profiles/status/resource


iri:has-resource
    Target:
        generic DOE-IRI Resource
    Profile:
        https://iri.science/profiles/status/resource


iri:has-capability
    Target:
        Capability
    Profile:
        https://iri.science/profiles/account/capability


iri:has-project
    Target:
        Project
    Profile:
        https://iri.science/profiles/account/project


iri:has-project-allocation
    Target:
        ProjectAllocation
    Profile:
        https://iri.science/profiles/account/project-allocation


iri:provides-filesystem
    Target:
        urn:doe-iri:resource:storage:filesystem

    Profile:
        https://iri.science/profiles/resource-definition/storage/filesystem


iri:provides-block
    Target:
        urn:doe-iri:resource:storage:block

    Profile:
        https://iri.science/profiles/resource-definition/storage/block


iri:provides-object
    Target:
        urn:doe-iri:resource:storage:object

    Profile:
        https://iri.science/profiles/resource-definition/storage/object


iri:has-mount
    Target:
        urn:doe-iri:resource:storage:mount

    Profile:
        https://iri.science/profiles/resource-definition/storage/mount


iri:accesses-mount
    Target:
        urn:doe-iri:resource:storage:mount

    Profile:
        https://iri.science/profiles/resource-definition/storage/mount


iri:mounted-on
    Target:
        urn:doe-iri:resource:compute:system

    Profile:
        https://iri.science/profiles/resource-definition/compute/system


iri:has-node
    Target:
        urn:doe-iri:resource:compute:node

    Profile:
        https://iri.science/profiles/resource-definition/compute/node


iri:has-cpu
    Target:
        urn:doe-iri:resource:compute:cpu

    Profile:
        https://iri.science/profiles/resource-definition/compute/cpu


iri:has-gpu
    Target:
        urn:doe-iri:resource:compute:gpu

    Profile:
        https://iri.science/profiles/resource-definition/compute/gpu


iri:attached-to
    Target may be:
        urn:doe-iri:resource:compute:system
    or:
        urn:doe-iri:resource:compute:node

    Profile MUST be selected from the actual target in the example:

        compute system:
          https://iri.science/profiles/resource-definition/compute/system

        compute node:
          https://iri.science/profiles/resource-definition/compute/node


iri:hosted-on
    Target may be:
        urn:doe-iri:resource:compute:system
    or:
        urn:doe-iri:resource:compute:node

    Profile MUST match the actual target shown in the example.


iri:submit-job
    Target:
        operation entry point

    This is NOT a representation profile target.

    Do NOT add:
        "profile": "https://iri.science/profiles/compute/job"

    The operation endpoint is not a Job representation.

    Preserve service-desc/OpenAPI discovery for operation semantics.


===============================================================================
2. IMPORTANT RESOURCE RULE
===============================================================================

For relations whose registered target is a generic DOE-IRI Resource, such as:

    iri:impacts
    iri:may-impact
    iri:has-resource

use:

    https://iri.science/profiles/status/resource

unless the example explicitly establishes a specific target Resource Type and
there is a clear reason to advertise the more-specific Resource Definition
Profile.

Do not guess a specific Resource Definition Profile solely from an href or
resource name.

For relations whose target Resource Type is fixed by the relation definition,
such as:

    iri:has-mount
    iri:has-node
    iri:has-cpu
    iri:has-gpu
    iri:provides-filesystem

use the corresponding canonical Resource Definition Profile.

===============================================================================
3. INVENTORY CURRENT EXAMPLES
===============================================================================

Search current normative/user-facing material:

    rg -n '"_links"|_links:' \
      registry \
      rfc \
      specification-v2 \
      README.md \
      docs \
      --glob '!docs/superpowers/**' \
      2>/dev/null || true

Also search:

    rg -n '"profile"\s*:' \
      registry \
      rfc \
      specification-v2 \
      README.md \
      docs \
      --glob '!docs/superpowers/**' \
      2>/dev/null || true

Do NOT modify:

    specification-v1/
    docs/superpowers/

unless a current document links directly to an obsolete example that must be
fixed.

For every `_links` example, record:

- file;
- relation;
- target;
- existing profile, if any;
- expected target profile;
- action:
    ADD
    CORRECT
    KEEP
    REMOVE
    NO PROFILE APPLICABLE

Pay particular attention to arrays: every Link Object in an array must be
evaluated independently.

===============================================================================
4. OUTPUT
===============================================================================

Report an inventory grouped by file.

Do not edit anything.

Identify any example where the correct target profile cannot be determined
without an architectural decision.

