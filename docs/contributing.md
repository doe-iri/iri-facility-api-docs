---
layout: default
title: Contributing
parent: IRI Registry
nav_order: 2
permalink: /contributing/
---

# Contributing

Normative IRI Facility API documentation is maintained in the main [`iri-facility-api-docs`](https://github.com/doe-iri/iri-facility-api-docs) repository.

Use the repository's version-controlled workflow for specification, registry, and RFC changes.

## Choose the right contribution path

| Change | Preferred location |
|---|---|
| Fix documentation-site explanation or onboarding material | `docs/` in the main repository |
| Fix specification wording | Main repository pull request |
| Change OpenAPI structure | Main repository pull request |
| Add or modify a registered URN | Registry pull request; RFC when architectural |
| Add or modify a Resource Definition Profile | Registry pull request; RFC when architectural |
| Add or modify an IRI link relation | Registry/RFC process |
| Propose a new interaction pattern | Issue followed by RFC |
| Report implementation interoperability problem | GitHub issue |

## Before proposing a new identifier

Check whether the desired semantic already exists in:

- [Resource Type URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md)
- [Controlled Attribute URNs](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/attributes.md)
- [Resource Definition Profiles](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/profiles/resource-definition)
- [Link Relation Registry](https://github.com/doe-iri/iri-facility-api-docs/tree/main/registry/relations)

Avoid creating two identifiers for the same semantic concept.

## RFC workflow

For architecture-level changes, see [RFC Process](rfc-process.md) and the authoritative [RFC README](https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/README.md).

## Pull-request review

A normative pull request should make it clear:

- what problem is being solved,
- which specification or registry area changes,
- whether the change is backward compatible,
- whether OpenAPI must change,
- whether examples or verification assets must change, and
- whether an RFC governs the change.

## Documentation-site edits

Content under `docs/` should:

- explain rather than redefine normative requirements,
- link directly to authoritative repository content,
- identify illustrative examples as non-normative,
- avoid copying large normative sections that can become stale, and
- be updated when the underlying specification changes materially.

## Source-of-truth rule

If a documentation page disagrees with a versioned specification, OpenAPI document, registry entry, or governing RFC, fix the documentation page. Do not use explanatory text to override the authoritative source.
