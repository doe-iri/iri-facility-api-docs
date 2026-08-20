Read AGENTS.md first.

Perform ONLY DOE-IRI URN consistency corrections described below.

Do not modify HAL relation semantics, Task behavior, state-model wording, or
unrelated OpenAPI schemas.

PART A — Allocation unit URNs

The canonical allocation units are:

    urn:doe-iri:allocation:compute:node-hours
    urn:doe-iri:allocation:storage:bytes
    urn:doe-iri:allocation:storage:inodes

These agree with:
- rfc/rfc-iri-urn-structure-and-registry.md
- current IRI v2 OpenAPI

Update registry/urns/README.md, which currently contains obsolete flat forms:

    urn:doe-iri:allocation:node-hours
    urn:doe-iri:allocation:bytes
    urn:doe-iri:allocation:inodes

Search current normative content for those obsolete forms and update them.

Do not modify specification-v1 historical material.

PART B — Scratch filesystem classification

Do NOT register:

    urn:doe-iri:resource:storage:filesystem:scratch

The current model represents a scratch filesystem using:

    resource_type =
      urn:doe-iri:resource:storage:filesystem

and:

    attributes.tier =
      urn:doe-iri:storage:tier:scratch

Update:

    registry/profiles/status/resource.md

Remove examples and normative guidance treating filesystem:scratch as a
registered Resource Type.

Update:

    rfc/rfc-iri-urn-structure-and-registry.md

Remove filesystem:scratch from canonical Resource Type examples and registry
entries.

Where a hierarchy example is needed, use an actually registered pair such as:

    urn:doe-iri:resource:storage
        ↓
    urn:doe-iri:resource:storage:filesystem

Search:

    grep -R "urn:doe-iri:resource:storage:filesystem:scratch" \
      registry rfc specification-v2 2>/dev/null || true

    grep -R -E \
      "urn:doe-iri:allocation:(node-hours|bytes|inodes)" \
      registry rfc specification-v2 2>/dev/null || true

Validation:

    git diff --check
    git diff
    git status --short

Report exactly what changed.

Do not commit or push.
