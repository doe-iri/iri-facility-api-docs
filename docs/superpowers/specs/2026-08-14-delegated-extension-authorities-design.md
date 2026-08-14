# Delegated Extension Authorities Design

## Status

Approved in-chat design for reconciling facility-local DOE-IRI extensions with
the root registry's delegated-authority model.

Date: 2026-08-14

## 1. Objective

Make the explicit `ext` marker the sole canonical mechanism for facility- or
project-controlled DOE-IRI extensions, while preserving shared-parent fallback
and preventing delegated names from colliding with future shared semantic
children.

## 2. Canonical Form

The canonical conceptual form is:

```text
<parent-prefix>:ext:<authority>:<local-path>
```

Examples:

```text
urn:doe-iri:ext:nersc:pdu:breaker
urn:doe-iri:resource:ext:nersc:scanner
urn:doe-iri:resource:compute:ext:nersc:fpga
```

`parent-prefix` is either the DOE-IRI namespace root or an exact registered
canonical semantic DOE-IRI URN. Every such semantic URN is structurally
eligible as an extension parent; the registry does not maintain a separate
extension-point approval layer.

The following syntactic rules apply:

- `ext` is the exact lowercase reserved delegation marker.
- `ext` appears exactly once in an extension URN and cannot be used as an
  ordinary local segment.
- `authority` is a lowercase authority-code segment. Registration is checked
  separately when determining scope authorization.
- `local-path` contains one or more nonempty local segments.
- The delegated authority controls the suffix beneath one explicitly assigned
  prefix and must preserve or refine the meaning of the shared parent.
- Root placement is permitted only through an explicit root-scope delegation
  and should be used only when no accurate shared semantic parent exists.

The governing RFC defines the grammar and validation rules. The registry
records authority-code reservations and exact scope delegations. A scope
delegation, rather than a separate extension-point record, determines whether
an authority may assign values beneath a particular parent.

## 3. Semantic Hierarchy and Fallback

Ordinary segments before `ext` form the shared semantic hierarchy. `ext` is a
non-semantic delegation switch, and the authority code identifies governance
rather than resource classification.

For example, an unfamiliar value beneath:

```text
urn:doe-iri:resource:compute:ext:nersc:fpga
```

falls back to:

```text
urn:doe-iri:resource:compute
```

Prefixes ending in `:ext` or `:ext:<authority>` are structural namespace
nodes, not semantic resource types. Locally defined suffix hierarchy has
meaning under the authority's documentation.

A root-scope extension has no domain-specific shared parent and therefore
supports only opaque handling when the local meaning is unknown.

## 4. Authority and Scope Governance

The registry separates two records.

### 4.1. Authority-code reservation

An authority-code record identifies:

- authority code;
- organization;
- change controller;
- lifecycle status;
- reference.

Authority codes are never reassigned, including after deprecation.

### 4.2. Scope delegation

A scope record identifies:

- authority code;
- exact registered parent;
- assigned prefix;
- permitted semantic scope;
- lifecycle status;
- reference.

One authority-code reservation does not grant every possible insertion point.
For example, these are separate scopes:

```text
urn:doe-iri:resource:ext:nersc:
urn:doe-iri:resource:compute:ext:nersc:
```

One active scope grants the full nonempty local suffix subtree beneath that
prefix. It grants no adjacent parent scope.

The existing `esnet`, `nersc`, `alcf`, `olcf`, and `slac` records remain active
authority-code reservations. No active scope delegation is inferred from an
unresolved scope cell. Scope records are added only through an explicit
governance decision.

## 5. Syntax, Authorization, Assignment, and Validation

Validation distinguishes:

1. **Syntactic validity** — an **Extension URN** follows the DOE-IRI grammar and
   canonical explicit `ext` form. This term alone does not imply registration,
   delegation, or local documentation.
2. **Scope authorization** — a **scope-authorized Extension URN** uses a
   reserved authority code with an active delegation for the exact parent and
   authority pair.
3. **Local definition** — a **locally defined Extension URN** is
   scope-authorized and has a suffix assigned and documented by the delegated
   authority.

An **assigned DOE-IRI extension** satisfies all three layers. Individual local
leaves do not require central registration; the delegated authority assigns and
documents them beneath its active prefix.

A structurally valid value with an unknown authority or undelegated parent is
unassigned and noncanonical. General clients should not reject it solely for
being unfamiliar; they use shared-parent fallback or opaque handling. An API
contract requiring assigned DOE-IRI values may reject it. Producers must not
claim an undelegated prefix as an assigned DOE-IRI extension.

The RFC must also align its base grammar with registered category-root URNs and
the current top-level registry branches, including `storage` and the
administrative `ext` branch.

## 6. Compatibility

Direct facility-code forms are not a second canonical syntax:

```text
urn:doe-iri:<facility-code>:...
urn:doe-iri:resource:<facility-code>:...
urn:doe-iri:resource:compute:<facility-code>:...
```

Repository search found no concrete deployed value in those forms, so this
change replaces the placeholder RFC examples without registering aliases.

If external deployment evidence is found later, only proven legacy prefixes or
exact values may be registered as deprecated. Each record keeps exact-string
identity and names an explicit `ext` replacement; clients must not heuristically
rewrite segments that happen to match an authority code.

Promotion of a local value to shared status creates a new shared URN and may
deprecate the old extension with replacement guidance. The old identifier is
never repurposed.

## 7. Documentation Scope

This change updates:

- the governing URN RFC's terminology, grammar, hierarchy, extension,
  registration, validation, compatibility, and example sections;
- the Root Registry's `ext` taxonomy and authority/scope records;
- the project context's extension-authority decision;
- facility-local profile guidance in the type-specific-attributes RFC.

It does not assign any facility a scope, create a second canonical extension
syntax, change unrelated service namespace edits, or alter the generic OpenAPI
URN pattern.
