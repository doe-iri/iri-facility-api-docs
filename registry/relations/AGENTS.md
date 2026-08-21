# IRI Link Relation Registry Instructions

These rules apply under `registry/relations/`.

## 1. Relation Identity

IRI custom HAL relations use lowercase kebab-case CURIEs:

```text
iri:has-mount
iri:generated-by
iri:submit-job
```

Canonical relation URIs use:

```text
https://iri.science/rels/<relation-name>
```

Do not use camelCase, PascalCase, underscores, or whitespace in custom
multiword relation identifiers.

Standard Web Linking relations such as `self`, `help`, `monitor`, and
`service-desc` are not registered as `iri:*` relations.

## 2. Relation Semantics

Each relation definition should identify:

- relation URI and CURIE;
- status/version;
- semantic meaning;
- source representation type;
- target representation type;
- source/target Resource Type where applicable;
- cardinality;
- target classification;
- target stability/relationship volatility when relevant;
- authorization/visibility behavior;
- omission semantics;
- HAL example.

Do not conflate target health or current availability with relationship
existence.

Useful negative semantics should remain explicit, for example:

```text
The relation does not prove the target is currently healthy, reachable, or
available.
```

Do not require a separate Resource State representation in IRI v2.

## 3. Target Classification

Distinguish:

```text
IRI/API representation target
operation entry point
relationship Resource
external documentation/service description
```

The target classification determines whether an IRI representation `profile`
belongs on a HAL Link Object.

## 4. HAL Link Profiles

`profile` describes the link target representation, never the relation itself.

For fixed-type targets, use the canonical target profile.

Examples:

```text
iri:has-mount
    → https://iri.science/profiles/resource-definition/storage/mount

iri:located-at
    → https://iri.science/profiles/facility/site

iri:generated-by
    → https://iri.science/profiles/status/incident

iri:has-capability
    → https://iri.science/profiles/account/capability
```

For generic DOE-IRI Resource targets, use the generic Resource profile unless
the example explicitly establishes a more-specific target type and the
relation/profile rules support advertising it.

For polymorphic targets such as `iri:hosted-on` or `iri:attached-to`, determine
the profile from the actual target in each example.

Do not add an IRI representation profile to an operation relation such as
`iri:submit-job`.

## 5. URI-Property Compatibility

When a registered relation is the additive HAL migration of an existing URI
property:

- retain the URI property according to current OpenAPI;
- when both forms appear, targets must agree;
- nullable/absent URI values map to omitted links, never `"href": null`;
- authorization filtering must not create contradictions between retained URI
  fields and HAL links.

The HAL RFC is authoritative for the general migration rules.

## 6. Task Boundaries

A normal relation task should address:

- one relation; or
- one tightly coupled relation family.

Do not mix relation registration with unrelated URN taxonomy or OpenAPI
redesign in one implementation task.

If a new relation changes architecture, use `registry_architect` first.

## 7. Validation

For changed relations:

- verify relation index entry;
- verify source/target classification;
- verify cardinality;
- verify target `profile` examples;
- verify lowercase kebab-case;
- parse changed JSON examples;
- run targeted searches for old spellings;
- run `git diff --check`.
