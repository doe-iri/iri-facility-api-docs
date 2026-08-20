Read AGENTS.md first.

Use the `_links` target-profile audit from the previous pass.

Modify ONLY current documentation/examples under:

    registry/

Do not modify:
    rfc/
    specification-v1/
    specification-v2/
    docs/superpowers/

Goal:
Every HAL Link Object example whose target is an IRI representation with a
known canonical profile should contain the correct `profile` member.

RULE

`profile` identifies the TARGET representation.

For example:

    "iri:has-mount": {
      "href":
        "https://api.example.org/api/v2/status/resources/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch filesystem",
      "type": "application/hal+json",
      "profile":
        "https://iri.science/profiles/resource-definition/storage/mount"
    }

===============================================================================
1. APPLY THE VERIFIED PROFILE MATRIX
===============================================================================

Use the verified relation definitions from:

    registry/relations/

Do not independently invent mappings.

For every applicable Link Object:

- preserve href;
- preserve title;
- preserve templated;
- preserve relation name;
- preserve existing semantics;
- add or correct only the `profile` value needed for the target;
- do not change cardinality.

When an IRI representation target uses HAL, retain or use:

    "type": "application/hal+json"

but do not perform a broad unrelated media-type cleanup.

===============================================================================
2. SELF LINKS
===============================================================================

For `_links.self`, use the profile of the represented object.

Examples:

registry/profiles/status/resource.md
    https://iri.science/profiles/status/resource

registry/profiles/status/event.md
    https://iri.science/profiles/status/event

registry/profiles/status/incident.md
    https://iri.science/profiles/status/incident

registry/profiles/facility.md
    https://iri.science/profiles/facility

registry/profiles/facility/site.md
    https://iri.science/profiles/facility/site

registry/profiles/task.md
    https://iri.science/profiles/task

registry/profiles/compute/job.md
    https://iri.science/profiles/compute/job

For a Resource Definition Profile example, use that specific profile for
`self`.

For example, in:

    registry/profiles/resource-definition/storage/filesystem.md

use:

    "profile":
      "https://iri.science/profiles/resource-definition/storage/filesystem"

for the example Resource's self link.

Do not replace a Resource Definition Profile self link with the generic
status/resource profile merely because the Resource also conforms to the base
profile.

===============================================================================
3. LINKS THAT MUST NOT RECEIVE A REPRESENTATION PROFILE
===============================================================================

Do NOT invent profile members on:

    curies
    service-desc
    help

unless `help` explicitly targets a defined IRI representation profile.

Do NOT add a representation profile to:

    iri:submit-job

because its target is an operation entry point, not a Job representation.

In particular, this is WRONG:

    "iri:submit-job": {
      "href": "...",
      "profile": "https://iri.science/profiles/compute/job"
    }

===============================================================================
4. POLYMORPHIC TARGETS
===============================================================================

For:

    iri:attached-to
    iri:hosted-on

inspect the actual target shown by each example.

If target is a Compute System:

    https://iri.science/profiles/resource-definition/compute/system

If target is a Compute Node:

    https://iri.science/profiles/resource-definition/compute/node

Do not choose one globally.

===============================================================================
5. GENERIC RESOURCE TARGETS
===============================================================================

For:

    iri:impacts
    iri:may-impact
    iri:has-resource

default to:

    https://iri.science/profiles/status/resource

because the registered relation target is a generic DOE-IRI Resource.

Use a more-specific Resource Definition Profile only when the example
unambiguously defines the target's specific Resource Type and doing so is
consistent with the surrounding documentation.

Do not infer a profile from a name such as "scratch", "gpu", or "storage".

===============================================================================
6. VALIDATION
===============================================================================

After edits:

    rg -n '"_links"|_links:' registry

    rg -n '"profile"\s*:' registry

    git diff --check
    git diff -- registry
    git status --short

Manually review every modified `_links` example.

Report:
- files changed;
- profile values added;
- incorrect profile values corrected;
- profile values deliberately omitted and why.

Do not commit or push.

