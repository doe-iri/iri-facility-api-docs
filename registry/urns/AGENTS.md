# DOE-IRI URN Registry Instructions

These rules apply under `registry/urns/`.

## 1. Authority

The governing DOE-IRI URN specification is authoritative for:

- syntax and grammar;
- hierarchy matching;
- delegation and `ext` rules;
- registration procedure;
- conformance.

Files in this directory are authoritative for assigned DOE-IRI identifiers,
controlled values, parentage, lifecycle status, and current mappings.

Do not duplicate the complete namespace grammar or registration procedure here.

## 2. Resource Type URNs

Resource Type URNs identify WHAT kind of Resource is represented.

Use:

```text
urn:doe-iri:resource:<domain>[:<refinement>...]
```

Do not encode topology as Resource Type nesting.

When a canonical Resource Definition Profile exists, record the explicit
mapping in the Resource Type registry. Do not require clients to construct the
profile URI mechanically from the URN.

## 3. Controlled Attribute URNs

Controlled attribute URNs define governed values used by profile properties.

A profile property name is not itself a controlled-value URN.

Keep separate:

```text
property name
    e.g. storage_technology

controlled value
    e.g. urn:doe-iri:storage:system-technology:lustre
```

Register a controlled URN only when a governed vocabulary materially improves
interoperability.

Do not create URNs for ordinary numeric values, capacities, versions, paths,
free-form names, or URLs without a clear interoperability requirement.

## 4. Delegated Extensions

Use the canonical explicit delegation form defined by the governing URN
specification:

```text
<registered-parent>:ext:<authority>:<local-path>
```

Do not infer a delegation merely because an authority code is known.

Distinguish:

1. syntactic validity;
2. scope authorization;
3. locally defined assignment.

Do not centrally register every delegated local leaf when the governing
delegation model assigns that responsibility to the delegated authority.

## 5. Lifecycle and Replacements

Use current registry lifecycle values consistently.
Never repurpose an identifier.

If a value is deprecated, preserve exact identity and provide an explicit
replacement when one exists.

## 6. Task Boundaries

A URN task should normally concern one of:

- one Resource Type family;
- one controlled-value family;
- one lifecycle/deprecation decision;
- one delegated-authority scope issue.

Do not combine unrelated URN families into a single semantic task.

## 7. Validation

After a URN edit, validate only the directly coupled surfaces:

- registry table/tree/index consistency;
- exact parentage;
- lifecycle status;
- directly referenced Resource Definition Profile;
- directly affected RFC example if required by the task.

Do not rewrite profiles or RFCs merely because they mention the same domain
unless the approved change requires propagation.
