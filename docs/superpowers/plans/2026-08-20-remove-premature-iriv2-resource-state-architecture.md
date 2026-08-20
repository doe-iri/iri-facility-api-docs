Read AGENTS.md and:

    rfc/rfc-type-specific-attributes.md

Perform ONLY an IRI v2 state-separation terminology cleanup within:

    registry/README.md
    registry/profiles/resource-definition/
    registry/relations/

Do NOT modify RFC files, OpenAPI, Task, Job, Event, or Incident profiles in
this pass.

ARCHITECTURAL RULE

IRI v2 does NOT require separate Resource Definition and Resource State API
representations.

A future definition/state decomposition is deferred and is not part of this
work.

Search for:

    resource-state
    Resource State
    state representation
    state resource
    state object
    state mechanism
    state mechanisms
    represented separately
    MUST be represented separately
    SHOULD be represented separately

Review matches manually.

KEEP useful negative semantics such as:

    This relation does not imply current health.
    This relation does not prove current availability.
    This relation does not mean the mount is currently usable.
    This capability does not guarantee current availability.

REMOVE or neutralize architecture statements such as:

    Current state MUST be represented separately.
    Dynamic values SHOULD be represented through resource-state mechanisms.

Use neutral wording such as:

    Current operational condition is outside the semantics of this relation
    and, when represented, is governed by the applicable IRI API contract.

or:

    The semantics of time-varying values are governed by the applicable IRI
    API contract and Resource Definition Profile.

registry/README.md specifically:

Replace the blanket statement that dynamic health, capacity, utilization,
availability, transfer activity, and workload activity are "state, not
Resource Definition attributes."

Use wording equivalent to:

    Resource Type URNs classify a Resource. Resource Definition Profiles define
    additional type-specific semantics selected by resource_type. A profile may
    define configuration, descriptive metadata, capabilities, quantitative
    values, or time-varying observations as appropriate to that Resource type.

    IRI v2 does not require a separate Resource Definition / Resource State
    representation model.

Do not describe future IRI v3 architecture in detail.

Validation:

    grep -R -n -E \
      "resource-state|Resource State|state representation|state resource|state object|state mechanism|state mechanisms|represented separately" \
      registry 2>/dev/null || true

Review any remaining matches and explain why they are valid.

Then run:

    git diff --check
    git diff
    git status --short

Do not commit or push.
