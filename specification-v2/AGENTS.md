# IRI v2 OpenAPI Instructions

These rules apply under `specification-v2/`.

## 1. Structural Authority

The checked-out IRI v2 OpenAPI is authoritative for:

- JSON properties;
- schemas/types;
- requiredness and nullability;
- formats;
- operation paths and methods;
- request/response shapes;
- structural validation.

Registry and profile prose must not silently override this structure.

## 2. Semantic References

Where OpenAPI descriptions refer to DOE-IRI semantics:

- use Resource Type URNs registered in `registry/urns/resource-types.md`;
- use controlled URNs registered in `registry/urns/attributes.md`;
- use relation names from `registry/relations/`;
- use canonical profile terminology from `registry/profiles/`.

Descriptions may reference semantics but should not duplicate complete registry
definitions.

## 3. Resource Type and Attributes

For the intended v2 Resource model:

- `resource_type` carries an extensible DOE-IRI Resource Type URN;
- `attributes`, when present according to the current schema, carries
  type-specific data interpreted by the applicable Resource Definition Profile.

If the checked-out OpenAPI contradicts this intended semantic model, report the
inconsistency rather than silently changing structural contract from a profile
or registry task.

## 4. HAL Additive Migration

Do not remove retained URI-valued properties as part of documentation-only HAL
work unless an approved OpenAPI revision explicitly changes the contract.

When examples show both legacy URI fields and HAL links, their targets must
agree.

Do not introduce `href: null`.

## 5. Generated Artifacts

Before editing consolidated/generated OpenAPI files, determine the authoritative
source and repository generation workflow.

Prefer:

```text
edit authoritative source
    ↓
run existing generation process
    ↓
validate generated artifact
```

Do not hand-maintain divergent generated copies.

## 6. Scope Discipline

OpenAPI work should be isolated from unrelated semantic registry cleanup.

A documentation consistency task may update descriptions/examples without
changing the API contract.

Do not remove generic properties from multiple schemas based only on suspicion
that they were generated accidentally. Audit first and require an explicit
contract decision for broad removals.

## 7. Validation

For bounded OpenAPI changes:

- parse YAML/JSON;
- run repository generation/validation commands when applicable;
- compare source and generated artifact if both exist;
- run `git diff --check`;
- inspect only directly affected schemas/operations.

Use full-spec validation when a structural or generated-artifact change
requires it.
