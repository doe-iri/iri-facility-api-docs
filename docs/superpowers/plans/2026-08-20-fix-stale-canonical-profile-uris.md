Read AGENTS.md first.

Perform ONLY a canonical profile-URI cleanup. Do not make unrelated semantic,
OpenAPI, URN, state-model, or terminology changes.

Repository:
doe-iri/iri-facility-api-docs

1. Fix registry/relations/generated-by.md

The source is Event and the target is Incident.

Replace the incorrect target profile:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/status/incident

Update every occurrence in that file.

2. Fix registry/relations/has-mount.md

Replace:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/resource-definition/storage/mount

3. Fix registry/relations/accesses-mount.md

Replace:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/resource-definition/storage/mount

4. Fix registry/relations/attached-to.md

Replace:

    https://iri.science/profiles/compute/system

with:

    https://iri.science/profiles/resource-definition/compute/system

Replace:

    https://iri.science/profiles/compute/node

with:

    https://iri.science/profiles/resource-definition/compute/node

5. Fix rfc/rfc-hal-links.md

Replace:

    https://iri.science/profiles/storage/mount

with:

    https://iri.science/profiles/resource-definition/storage/mount

6. Search current normative material for any remaining obsolete forms:

    grep -R "https://iri.science/profiles/storage/" \
      registry rfc specification-v2 2>/dev/null || true

    grep -R -E \
      "https://iri.science/profiles/compute/(system|node|cpu|gpu)" \
      registry rfc specification-v2 2>/dev/null || true

Only correct verified Resource Definition profile references.

Validation:

    git diff --check
    git diff
    git status --short

Report:
- files changed;
- old → new identifiers;
- any questionable matches not changed.

Do not commit or push.

