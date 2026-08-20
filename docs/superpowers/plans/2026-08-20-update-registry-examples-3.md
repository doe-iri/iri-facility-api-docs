Read AGENTS.md first.

Modify ONLY:

    rfc/

Do not modify registry or OpenAPI files in this pass.

Goal:
Normalize the `profile` member of every HAL `_links` example so it identifies
the target representation's canonical profile.

Use:

    registry/relations/README.md
    registry/relations/*.md
    registry/profiles/**
    registry/urns/resource-types.md

as authoritative sources.

Apply the same rules used for the registry pass.

Key examples:

iri:has-mount
    profile:
      https://iri.science/profiles/resource-definition/storage/mount

iri:located-at
    profile:
      https://iri.science/profiles/facility/site

iri:generated-by
    profile:
      https://iri.science/profiles/status/incident

iri:has-event
    profile:
      https://iri.science/profiles/status/event

iri:impacts
iri:may-impact
iri:has-resource
    generic target profile:
      https://iri.science/profiles/status/resource

iri:has-capability
    profile:
      https://iri.science/profiles/account/capability

iri:has-project
    profile:
      https://iri.science/profiles/account/project

iri:has-project-allocation
    profile:
      https://iri.science/profiles/account/project-allocation

iri:provides-filesystem
    profile:
      https://iri.science/profiles/resource-definition/storage/filesystem

iri:provides-block
    profile:
      https://iri.science/profiles/resource-definition/storage/block

iri:provides-object
    profile:
      https://iri.science/profiles/resource-definition/storage/object

iri:has-node
    profile:
      https://iri.science/profiles/resource-definition/compute/node

iri:has-cpu
    profile:
      https://iri.science/profiles/resource-definition/compute/cpu

iri:has-gpu
    profile:
      https://iri.science/profiles/resource-definition/compute/gpu

iri:mounted-on
    profile:
      https://iri.science/profiles/resource-definition/compute/system

iri:accesses-mount
    profile:
      https://iri.science/profiles/resource-definition/storage/mount

monitor
    profile:
      https://iri.science/profiles/task

Do not add profile to:
    service-desc
    curies
    iri:submit-job

For attached-to and hosted-on, inspect whether each example targets a system
or node and choose the correct profile accordingly.

For self, use the profile of the current represented object.

Validation:

    rg -n '"_links"|_links:' rfc
    rg -n '"profile"\s*:' rfc

    git diff --check
    git diff -- rfc

Report all changes.

Do not commit or push.

