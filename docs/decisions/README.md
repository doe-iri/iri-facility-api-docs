# IRI Architectural Decision Records

This directory records durable rationale for accepted IRI architectural decisions.

> **Non-normative:** Decision records explain why a choice was made. They do not assign URNs, register link relations, define OpenAPI structure, or override RFCs, registries, relation definitions, or representation profiles.

## When to create a decision record

Create a decision record when a choice is likely to be revisited or misunderstood and the rationale is not appropriate to repeat in normative documents. Typical examples include:

- deciding whether a concept is a Resource, attribute, relationship resource, or operation entry point;
- choosing a namespace or delegation strategy;
- selecting a hypermedia approach;
- choosing a naming convention with compatibility consequences;
- distinguishing two similar relationships whose semantics are intentionally different.

Do not create a decision record merely to preserve an implementation plan.

## File naming

Use stable, sequential names:

```text
NNNN-short-decision-title.md
```

Do not encode tool names or workflow names in filenames.

## Status values

Use one of:

- `Proposed` — under architectural review.
- `Accepted` — current rationale for an adopted decision.
- `Superseded` — replaced by another decision record; identify the replacement.
- `Rejected` — considered but not adopted.

A status in this directory is descriptive only. Normative lifecycle status for URNs and relations remains in the corresponding registry.

## Recommended structure

Each record should contain:

1. Title and metadata.
2. Non-normative authority notice.
3. Context.
4. Decision.
5. Rationale.
6. Consequences and tradeoffs.
7. Normative/current sources.
8. Historical source or supersession information when useful.

Avoid reproducing large registry tables, schemas, or conformance text. Link to the authoritative current source instead.

## Updating decision records

When current architecture changes:

- update a record when the rationale is still the same but references have moved;
- supersede it when the decision itself changes materially;
- do not silently edit history to make a rejected or replaced decision appear to have always been current.

Completed execution plans should not be moved into this directory.
