# Decision 0004: Use lowercase kebab-case for DOE-IRI custom link relations

**Status:** Accepted  
**Date:** 2026-08-14  
**Scope:** DOE-IRI custom HAL relation identifiers

> **Non-normative:** This record explains the naming rationale. `rfc/rfc-hal-links.md` and `registry/relations/` define the current registered names and conformance requirements.

## Context

Early relation names used inconsistent camelCase forms such as `iri:hasMount` and `iri:generatedBy`. The repository needed one predictable lexical convention before wider adoption.

The convention had to apply only to DOE-IRI custom relation local names without changing JSON property names, DOE-IRI URNs, OpenAPI `operationId` values, API paths, programming-language symbols, or standard Web Linking relations.

## Decision

DOE-IRI custom `iri:*` relation local names use lowercase ASCII letters, digits, and hyphens. Multiword local names use kebab-case.

Examples:

```text
iri:has-mount
iri:generated-by
iri:has-project-allocation
iri:provides-filesystem
iri:submit-job
```

Do not register camelCase aliases solely for the former pre-adoption spellings. Compatibility or deprecation aliases require an explicit governance mechanism and demonstrated need.

The naming rule does not alter relation meaning, direction, cardinality, source/target types, lifecycle, visibility, or authorization semantics.

## Rationale

Lowercase kebab-case provides a uniform URI/CURIE-friendly external spelling and avoids special treatment for acronym capitalization such as CPU and GPU.

Keeping this rule scoped to link relations avoids unnecessary lexical churn in unrelated API and data-model identifiers.

## Consequences and tradeoffs

Early adopters of pre-correction relation spellings may need to update emitted or consumed relation keys. The registry presents one canonical name for each relation rather than two competing spellings.

Future relation names should be reviewed for semantics first; the naming convention does not justify creating a new relation when an existing standard or registered relation already fits.

## Normative and current sources

- `rfc/rfc-hal-links.md`
- `registry/relations/README.md`
- `registry/relations/*.md`

## Historical notes

This record distills the rationale from an earlier relation-naming design note retained in Git history. The exhaustive former-name migration table is intentionally left to Git history because current registered names are authoritative.
