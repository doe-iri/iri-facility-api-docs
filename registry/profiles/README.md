# IRI Representation Profiles

This directory contains the semantic profiles used by the DOE Integrated Research
Infrastructure (IRI) Facility API.

Profiles define **semantic and interoperability conventions** for IRI
representations. They supplement the structural API contract defined by OpenAPI
and do not replace it.

The canonical profile namespace is:

```text
https://iri.science/profiles/...
```

Repository paths such as `registry/profiles/...` and GitHub URLs are documentation
locations, not profile identifiers.

## Profile Model

IRI uses two related kinds of profiles in this directory:

```text
Representation Profiles
    Define semantic conventions for independently meaningful API representations.

Resource Definition Profiles
    Define additional type-specific semantics for an IRI Resource selected by
    resource_type.
```

For an ordinary independently meaningful representation:

```text
OpenAPI schema
    ↓
Representation Profile
    ↓
semantic and interoperability conventions
```

For a typed IRI Resource:

```text
OpenAPI Resource schema
    ↓
https://iri.science/profiles/status/resource
    common Resource semantics
    ↓
resource_type
    ↓
registered Resource Type URN
    ↓
https://iri.science/profiles/resource-definition/<domain>/<type>
    additional type-specific semantics
```

A Resource Definition Profile supplements the common Resource profile; it does
not replace it and does not define a separate Resource Definition API object.

IRI v2 does not require separate Resource Definition and Resource State
representations, endpoints, or conformance models.

## Sources of Truth

Authority is resolved by concern.

| Concern | Authoritative source |
|---|---|
| JSON properties, types, required/nullable rules, formats, operation shapes, structural validation | IRI v2 OpenAPI |
| DOE-IRI URN syntax, hierarchy, delegation, registration rules, and conformance | Governing DOE-IRI URN specification |
| Assigned Resource Type URNs and controlled values | [`../urns/`](../urns/README.md) |
| Registered IRI link-relation names and complete relation semantics | [`../relations/`](../relations/README.md) |
| HAL wire conventions and URI-property migration | [`../../rfc/rfc-hal-links.md`](../../rfc/rfc-hal-links.md) |
| Common IRI Resource semantic conventions | [`status/resource.md`](status/resource.md) |
| Type-specific Resource semantics | [`resource-definition/`](resource-definition/) |
| Other representation semantics | The applicable profile in this directory |

A profile MUST NOT silently override the OpenAPI structural contract, URN
registry, or registered link-relation semantics.

## Current Profiles

### Facility

| Representation | Repository document | Canonical profile URI |
|---|---|---|
| Facility | [`facility.md`](facility.md) | `https://iri.science/profiles/facility` |
| Site | [`facility/site.md`](facility/site.md) | `https://iri.science/profiles/facility/site` |

### Status

| Representation | Repository document | Canonical profile URI |
|---|---|---|
| Resource | [`status/resource.md`](status/resource.md) | `https://iri.science/profiles/status/resource` |
| Event | [`status/event.md`](status/event.md) | `https://iri.science/profiles/status/event` |
| Incident | [`status/incident.md`](status/incident.md) | `https://iri.science/profiles/status/incident` |

### Account and Allocation

| Representation | Repository document | Canonical profile URI |
|---|---|---|
| Capability | [`account/capability.md`](account/capability.md) | `https://iri.science/profiles/account/capability` |
| Project | [`account/project.md`](account/project.md) | `https://iri.science/profiles/account/project` |
| Project Allocation | [`account/project-allocation.md`](account/project-allocation.md) | `https://iri.science/profiles/account/project-allocation` |
| User Allocation | [`account/user-allocation.md`](account/user-allocation.md) | `https://iri.science/profiles/account/user-allocation` |

### Compute and Task

| Representation | Repository document | Canonical profile URI |
|---|---|---|
| Job | [`compute/job.md`](compute/job.md) | `https://iri.science/profiles/compute/job` |
| Task | [`task.md`](task.md) | `https://iri.science/profiles/task` |

## Resource Definition Profiles

Resource Definition Profiles specialize the common IRI Resource representation
according to a registered `resource_type`.

The canonical URI form is:

```text
https://iri.science/profiles/resource-definition/<domain>/<type>
```

The authoritative mapping between Resource Type URNs and Resource Definition
Profiles is maintained in:

[`../urns/resource-types.md`](../urns/resource-types.md)

Clients MUST NOT assume that a profile URI can be derived mechanically from a
Resource Type URN.

### Compute Resource Definitions

| Resource Type | Repository document | Canonical profile URI |
|---|---|---|
| `urn:doe-iri:resource:compute:system` | [`resource-definition/compute/system.md`](resource-definition/compute/system.md) | `https://iri.science/profiles/resource-definition/compute/system` |
| `urn:doe-iri:resource:compute:node` | [`resource-definition/compute/node.md`](resource-definition/compute/node.md) | `https://iri.science/profiles/resource-definition/compute/node` |
| `urn:doe-iri:resource:compute:cpu` | [`resource-definition/compute/cpu.md`](resource-definition/compute/cpu.md) | `https://iri.science/profiles/resource-definition/compute/cpu` |
| `urn:doe-iri:resource:compute:gpu` | [`resource-definition/compute/gpu.md`](resource-definition/compute/gpu.md) | `https://iri.science/profiles/resource-definition/compute/gpu` |

### Storage Resource Definitions

| Resource Type | Repository document | Canonical profile URI |
|---|---|---|
| `urn:doe-iri:resource:storage:system` | [`resource-definition/storage/system.md`](resource-definition/storage/system.md) | `https://iri.science/profiles/resource-definition/storage/system` |
| `urn:doe-iri:resource:storage:filesystem` | [`resource-definition/storage/filesystem.md`](resource-definition/storage/filesystem.md) | `https://iri.science/profiles/resource-definition/storage/filesystem` |
| `urn:doe-iri:resource:storage:mount` | [`resource-definition/storage/mount.md`](resource-definition/storage/mount.md) | `https://iri.science/profiles/resource-definition/storage/mount` |
| `urn:doe-iri:resource:storage:block` | [`resource-definition/storage/block.md`](resource-definition/storage/block.md) | `https://iri.science/profiles/resource-definition/storage/block` |
| `urn:doe-iri:resource:storage:object` | [`resource-definition/storage/object.md`](resource-definition/storage/object.md) | `https://iri.science/profiles/resource-definition/storage/object` |

### Service Resource Definitions

| Resource Type | Repository document | Canonical profile URI |
|---|---|---|
| `urn:doe-iri:resource:service:dtn` | [`resource-definition/service/dtn.md`](resource-definition/service/dtn.md) | `https://iri.science/profiles/resource-definition/service/dtn` |
| `urn:doe-iri:resource:service:inference` | [`resource-definition/service/inference.md`](resource-definition/service/inference.md) | `https://iri.science/profiles/resource-definition/service/inference` |

## Identifier Roles

The following identifiers answer different questions and MUST NOT be used
interchangeably.

```text
Resource Type URN
    WHAT kind of Resource is this?

Representation Profile URI
    WHAT semantic representation contract applies?

Link Relation
    WHY is the target related or applicable?

Instance URI / href
    WHERE is the target representation or operation entry point?
```

For example:

```text
urn:doe-iri:resource:storage:mount
    Resource Type

https://iri.science/profiles/resource-definition/storage/mount
    Resource Definition Profile

iri:has-mount
    Link Relation

https://api.example.org/api/v2/status/resources/frontier-orion-scratch-mount
    Target instance URI
```

## HAL Link Target Profiles

In a HAL Link Object, `profile` identifies the semantic profile of the **link
target**.

The four parts of a typical IRI HAL link answer different questions:

```text
relation
    WHY is the target linked?

href
    WHERE is the target?

type
    HOW is the target represented?

profile
    WHAT semantic representation contract applies to the target?
```

Example:

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-orion-scratch-mount",
      "title": "Frontier mount of Orion scratch filesystem",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    }
  }
}
```

The `profile` value above describes the target mount representation. It does not
identify the `iri:has-mount` relation or the source representation.

When the target is an IRI representation with a known canonical profile,
documentation examples SHOULD include that target profile.

Important exceptions include:

- `curies`, which is HAL metadata;
- `service-desc`, whose target is normally a service description such as
  OpenAPI rather than an IRI representation;
- ordinary external `help` targets;
- operation-affordance targets such as `iri:submit-job`, whose target is an
  operation entry point rather than a Job representation.

For polymorphic relations such as `iri:attached-to` and `iri:hosted-on`, the
profile MUST be chosen from the actual target type shown by the example. The
registered relation definition is authoritative for target classification.

For `_links.self`, use the profile applicable to the represented object. In a
Resource Definition Profile example, use that representation's most-specific
Resource Definition Profile.

## What Belongs in a Profile

Representation profiles define semantic and interoperability conventions such
as:

- interpretation of OpenAPI properties;
- identity semantics;
- relationships and navigation;
- compatibility between legacy URI properties and HAL links;
- authorization-sensitive visibility;
- processing expectations;
- conformance requirements;
- profile identification and versioning.

Resource Definition Profiles may additionally define:

- type-specific attributes;
- controlled vocabularies used by those attributes;
- type-specific relationships;
- applicable operation affordances;
- interpretation and conformance requirements for the selected Resource Type.

Profiles SHOULD reference the authoritative URN and link-relation registries
instead of duplicating their registration authority.

## What Does Not Belong in a Profile

Profiles SHOULD NOT:

- redefine OpenAPI property types, requiredness, or nullability;
- independently define the DOE-IRI URN grammar;
- independently register Resource Type or controlled attribute URNs;
- invent `iri:*` link relations;
- redefine registered link-relation semantics;
- use GitHub or repository paths as canonical profile identifiers;
- invent lifecycle transition rules absent from a governing specification;
- infer API paths from identifiers;
- require a separate Resource Definition / Resource State model in IRI v2.

Not every OpenAPI schema requires a representation profile. Helper schemas,
request objects, enums, and nested value objects generally remain OpenAPI-only
unless they acquire independent semantic identity or interoperability
requirements.

## Adding or Updating a Profile

Before adding or modifying a profile:

1. Read the current IRI v2 OpenAPI schema.
2. Read the applicable URN registry entries.
3. Read the applicable link-relation definitions.
4. Read `rfc/rfc-hal-links.md` when hypermedia is involved.
5. Determine whether the representation warrants an independent profile or is
   better represented as part of another profile.
6. Use the canonical `https://iri.science/profiles/...` identifier.
7. Preserve the distinction between structure, semantics, registered
   identifiers, relations, and instance URIs.
8. Update this README when adding or removing a profile.

Resource Definition Profiles follow the repository guidance in `AGENTS.md` and
the type-specific attribute/profile model defined by:

[`../../rfc/rfc-type-specific-attributes.md`](../../rfc/rfc-type-specific-attributes.md)

## Related Registry Documentation

- [DOE-IRI Registry](../README.md)
- [DOE-IRI URN Registry](../urns/README.md)
- [Resource Type URNs](../urns/resource-types.md)
- [Controlled Attribute URNs](../urns/attributes.md)
- [IRI Link Relation Index](../relations/README.md)
- [HAL `_links` RFC](../../rfc/rfc-hal-links.md)
- [Type-Specific Attributes and Resource Definition Profiles RFC](../../rfc/rfc-type-specific-attributes.md)

---

*DOE Integrated Research Infrastructure — IRI Representation Profiles*
