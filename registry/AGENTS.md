# DOE-IRI Registry Instructions

These rules apply to work under `registry/` and supplement the repository-root
instructions.

## 1. Registry Role

The registry records assigned identifiers and semantic contracts. It does not
replace the governing specifications.

```text
Specifications
    Define rules.

Registries
    Record values assigned under those rules.

Profiles
    Define representation semantics.

Relations
    Define why targets are related or applicable.
```

## 2. Core Resource Modeling

### Resource types

Resource types use:

```text
urn:doe-iri:resource:<domain>[:<refinement>...]
```

The hierarchy is semantic classification, not physical containment.
Do not encode topology by nesting Resource Types merely because one Resource
contains another.

### Attributes

Type-specific attributes belong in the Resource Definition Profile selected by
`resource_type` when those attributes are part of the applicable IRI v2
Resource model.

Use controlled DOE-IRI URNs when interoperability benefits from a governed
vocabulary. Use normal JSON scalar types for counts, capacities, names,
versions, paths, and URLs unless a controlled vocabulary is required.

### Relationships

Relationships between independently identifiable targets belong in registered
IRI/HAL link relations rather than duplicated ordinary attributes.

For any relation, distinguish:

- source representation;
- target representation;
- cardinality;
- target classification;
- relation meaning;
- expected stability/volatility when relevant;
- authorization-sensitive visibility;
- semantic absence versus filtered absence.

## 3. Lifecycle

Registry lifecycle values include:

```text
active
provisional
deprecated
```

Do not silently alter lifecycle status. Deprecated entries should name a
replacement when one exists.

## 4. Cross-Registry Consistency

When a change affects one registry surface, inspect only the directly coupled
surfaces needed to maintain consistency:

```text
Resource Type registration
    ↔ Resource Definition Profile mapping

controlled attribute value
    ↔ profile property using that vocabulary

link relation
    ↔ source/target profiles that advertise it

profile URI
    ↔ HAL examples that target that representation
```

Do not turn a local fix into a full-repository audit unless requested.

## 5. Current Domain Boundaries

### Storage

Current storage Resource Types include:

```text
urn:doe-iri:resource:storage:system
urn:doe-iri:resource:storage:filesystem
urn:doe-iri:resource:storage:mount
urn:doe-iri:resource:storage:block
urn:doe-iri:resource:storage:object
```

Important modeling rules:

- `storage:system` is managed storage infrastructure.
- filesystem, block, and object are logical storage Resources.
- mount is an independently represented exposure/relationship Resource.
- archive is a tier/lifecycle concept, not a fundamental access model.
- mount path belongs to the mount Resource.
- block device path is attachment-specific.
- object endpoints remain attributes/access descriptors unless independent
  identity, lifecycle, or relationships justify a Resource.

### Compute

Current compute Resource Types include:

```text
urn:doe-iri:resource:compute:system
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu
```

Physical containment is represented with links such as:

```text
iri:has-node
iri:has-cpu
iri:has-gpu
```

Facilities are not required to expose every CPU/GPU independently when
aggregate information is sufficient.

### Services

Service Resources describe consumable services independently of hosting
infrastructure.

Hosting topology uses registered relations such as `iri:hosted-on`; configured
mount access uses `iri:accesses-mount`.

Endpoint descriptors normally remain attributes unless independent identity,
lifecycle, or relationships justify separate Resources.

## 6. Validation

For a bounded registry edit, prefer:

```text
git diff --check
targeted Markdown-link checks
targeted searches for the identifiers changed
JSON/YAML parsing of examples that changed
```

Use broad registry scans only for registry-wide migrations.
