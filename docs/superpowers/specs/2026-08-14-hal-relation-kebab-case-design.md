# DOE-IRI HAL Relation Kebab-Case Migration Design

## 1. Purpose

DOE-IRI custom HAL link relation identifiers use the CURIE form
`iri:<relation-name>`. This change makes every registered multiword relation
name lowercase kebab-case while preserving its existing semantics.

This is an intentional pre-adoption lexical correction. It does not create new
relationships, change existing relationship meanings, or establish aliases for
the former camelCase spellings.

## 2. Authoritative Naming Rule

The governing naming rule will be added once to Section 4 of
`rfc/rfc-hal-links.md`, which defines authoritative relation sources and
conformance requirements:

> DOE-IRI custom link relation identifiers MUST use lowercase ASCII letters,
> digits, and hyphens. Multiword relation identifiers MUST separate words with
> a hyphen (`-`). DOE-IRI custom relation identifiers MUST NOT use camelCase,
> PascalCase, underscores, or whitespace.

The rule applies only to DOE-IRI custom `iri:*` relation identifiers. It does
not apply to JSON property names, DOE-IRI URNs, OpenAPI `operationId` values,
API paths, programming-language symbols, or standard registered Web Linking
relations.

The Link Profile Index records the assigned names and links to the profiles
that define their full semantics. The naming rule is not duplicated in the
index or individual profiles.

## 3. Registered Relation Mapping

The complete in-place conversion is:

| Former identifier | Canonical identifier |
|---|---|
| `iri:accessesMount` | `iri:accesses-mount` |
| `iri:attachedTo` | `iri:attached-to` |
| `iri:generatedBy` | `iri:generated-by` |
| `iri:hasCPU` | `iri:has-cpu` |
| `iri:hasCapability` | `iri:has-capability` |
| `iri:hasEvent` | `iri:has-event` |
| `iri:hasGPU` | `iri:has-gpu` |
| `iri:hasMount` | `iri:has-mount` |
| `iri:hasNode` | `iri:has-node` |
| `iri:hasProject` | `iri:has-project` |
| `iri:hasProjectAllocation` | `iri:has-project-allocation` |
| `iri:hasResource` | `iri:has-resource` |
| `iri:hasSite` | `iri:has-site` |
| `iri:hostedOn` | `iri:hosted-on` |
| `iri:locatedAt` | `iri:located-at` |
| `iri:mayImpact` | `iri:may-impact` |
| `iri:mountedOn` | `iri:mounted-on` |
| `iri:providesBlock` | `iri:provides-block` |
| `iri:providesFilesystem` | `iri:provides-filesystem` |
| `iri:providesObject` | `iri:provides-object` |
| `iri:submitJob` | `iri:submit-job` |

The registered single-word relation `iri:impacts` remains unchanged.

The nine conversions discovered beyond the request's minimum list are
`iri:accesses-mount`, `iri:attached-to`, `iri:has-cpu`, `iri:has-gpu`,
`iri:has-node`, `iri:hosted-on`, `iri:mounted-on`, `iri:provides-block`, and
`iri:provides-object`.

## 4. Scope

The migration updates every occurrence where a string denotes a DOE-IRI HAL
relation, including:

- the DOE-IRI Link Profile Index;
- all 22 individual link profiles;
- registry README navigation, type registries, taxonomy indexes, attribute
  profiles, diagrams, and the example HPC facility document;
- `rfc/rfc-hal-links.md` and `rfc/rfc-type-specific-attributes.md`;
- the v2 OpenAPI `Resource.site_uri` description in both the production
  component source and the consolidated v2 artifact;
- architectural context and active design/implementation-plan documents.

All existing individual profile filenames already use lowercase kebab-case,
including `link-profile-has-cpu.md` and `link-profile-has-gpu.md`. No file is
renamed, and relative profile paths remain stable.

The illustrative CURIE template remains unchanged. A relation local name such
as `has-mount` naturally expands to a lowercase kebab-case documentation path.

Literal rejected relation examples in design material will be rephrased so
they do not look like assigned camelCase CURIEs. Ignored execution reports
under `.superpowers/` remain historical runtime evidence and are not registry
or specification content.

## 5. Explicit Non-Goals

The migration does not change:

- `urn:doe-iri:*` values or legacy values such as `urn:iri:object:1234`;
- JSON properties such as `site_uri`, `self_uri`, `capability_uris`,
  `project_allocation_uri`, or `_links`;
- standard relations such as `self`, `help`, `monitor`, or `service-desc`;
- API paths, including `POST /api/v2/compute/job/{resource_id}`;
- OpenAPI operation identifiers, including `operationId: launchJob`;
- relationship semantics, direction, source or target type, cardinality,
  lifecycle, stability, target classification, authorization, or visibility;
- non-HAL camelCase labels in legacy conceptual or UML material;
- application-language symbols merely because their serialized relation value
  changes.

## 6. Compatibility

The correction replaces the registered spellings in place. The repository has
no alias, alternate-relation, or link-relation deprecation mechanism, and no
application or library implementation was found that serializes the current
names. Both spellings will therefore not be registered simultaneously.

Some provisional relation documentation is already committed on `main`.
`iri:located-at` is also mentioned in the production v2 OpenAPI description of
`Resource.site_uri`. External early adopters may need to update their emitted
or consumed relation keys. This risk is recorded in the final report, but it
does not justify inventing aliases that the registry cannot govern.

## 7. Dirty-Tree Preservation

The current working tree contains substantial approved but uncommitted HAL RFC
and profile work. The migration patches those live files in place. It must not
reset files from `HEAD`, discard untracked profiles, stage unrelated changes,
or overwrite concurrent user work.

The implementation uses only the exact mapping in Section 3. It must not apply
a general camelCase rewrite to unrelated text.

## 8. Validation

Completion requires all of the following:

1. Search explicitly for all 21 former registered identifiers and find no
   active repository occurrences.
2. Run the uppercase relation heuristic and inspect every match; active
   registry/specification content must contain no camelCase `iri:*` name.
3. Confirm the Link Profile Index still contains exactly 22 custom relations:
   21 lowercase kebab-case multiword names and `iri:impacts`.
4. Confirm every index link resolves and all 22 existing profile filenames
   remain present.
5. Parse all affected fenced JSON and YAML examples and
   `registry/examples/hpc-facility-resources.json`.
6. Verify `iri:located-at` targets still equal their corresponding `site_uri`
   values where both are present.
7. Confirm the production v2 component description and consolidated artifact
   agree.
8. Search the diff for unintended changes to URNs, JSON property names, API
   paths, `operationId` values, relation semantics, cardinalities, source or
   target types, lifecycle, authorization, and visibility.
9. Resolve affected relative Markdown links and run `git diff --check`.
10. Review `git status --short` and the complete diff to confirm the dirty-tree
    baseline was preserved.

## 9. Expected Result

Consumers see one canonical external spelling for each DOE-IRI custom HAL
relation. Every multiword local name is lowercase kebab-case, profile paths
remain stable, and all registry, RFC, OpenAPI-description, example, and design
surfaces agree without changing relationship behavior.
