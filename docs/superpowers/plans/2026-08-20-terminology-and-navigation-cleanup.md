Read AGENTS.md first.

Perform ONLY terminology, relation-name, and navigation cleanup under:

    registry/
    rfc/README.md

Do not change OpenAPI or substantive relation semantics.

1. Resource Definition terminology

Within:

    registry/profiles/resource-definition/

replace legacy document-level terminology such as:

    Attribute Profile
    Storage Attribute Profile
    Filesystem Attribute Profile

with:

    Resource Definition Profile

or, for a section that specifically defines attributes:

    Storage System Attributes
    Filesystem Attributes
    Type-Specific Attributes
    Attribute Contract

Do not mechanically replace ordinary uses of the word "attribute".

2. Relation names

Search current normative registry material for old camelCase forms:

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

Replace relation references with registered CURIEs such as:

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

Do NOT change:
- OpenAPI operationId values;
- programming-language symbols;
- historical docs under docs/superpowers.

3. Fix registry/relations/README.md

Change:

    [Back to the DOE-IRI Registry README](./README.md)

to:

    [Back to the DOE-IRI Registry README](../README.md)

4. Update rfc/README.md

Update the entry for:

    rfc-type-specific-attributes.md

to the current title:

    Type-Specific Attributes and Resource Definition Profiles for IRI Resource
    Objects

Describe the new RFC accurately:
- Resource.attributes semantics;
- resource_type selects Resource Definition semantics;
- Resource Type URNs and Resource Definition Profile URIs are distinct;
- current V2 OpenAPI supplies the structural contract;
- no separate Resource Definition/Resource State API objects are introduced.

Validation:

    grep -R -n -E \
      "providesFilesystem|providesBlock|providesObject|hasMount|mountedOn|attachedTo|hasNode|hasCpu|hasGpu|hostedOn|accessesMount|submitJob|generatedBy|hasCapability|hasProjectAllocation|hasProject" \
      registry rfc 2>/dev/null || true

    git diff --check
    git diff

Do not commit or push.

