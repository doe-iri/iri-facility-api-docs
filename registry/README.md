# DOE IRI Registry

The DOE IRI Registry records semantic identifiers and representation conventions
used by the IRI Facility API. It keeps resource classification, relatively
stable resource definition, relationships, and operational state distinct.

```text
Resource Type  →  Resource Definition  →  Relationships
                         │
                         └── operational state is separate
```

## Registry structure

```text
registry/
├── profiles/
│   ├── status/resource.md
│   └── resource-definition/<domain>/<type>.md
├── urns/
│   ├── README.md
│   ├── resource-types.md
│   └── attributes.md
└── relations/
```

| Location | Authority |
|---|---|
| [profiles/status/resource.md](profiles/status/resource.md) | Common semantics for every IRI Resource representation. |
| [profiles/resource-definition/](profiles/resource-definition/) | Type-specific Resource Definition semantics selected by `resource_type`. |
| [urns/resource-types.md](urns/resource-types.md) | Assigned Resource Type URNs. |
| [urns/attributes.md](urns/attributes.md) | Assigned controlled attribute URNs. |
| [relations/](relations/README.md) | Registered relation names and their complete semantics. |

A Resource Type URN is not a profile URI. A Resource Definition profile is
selected by the Resource's `resource_type`, and supplements rather than
replaces the [IRI Status Resource Profile](profiles/status/resource.md). For
example, a Resource whose type is
`urn:doe-iri:resource:compute:system` conforms both to the common Resource
profile and to
`https://iri.science/profiles/resource-definition/compute/system`.

URN registry documents record assigned identifiers. Resource Definition
profiles define type-specific representation semantics, including stable
attributes and applicable relationships. The governing specifications define
URN syntax and registration rules; they are not duplicated here.

## Resource model

Resource Type URNs classify a resource. Type-specific attributes describe
relatively stable characteristics. Registered HAL link relations express
topology and navigation. Dynamic facts such as current health, capacity,
utilization, availability, transfer activity, and workload activity are state,
not Resource Definition attributes.

The Resource Type hierarchy is semantic, not a containment tree. For example,
compute systems, nodes, CPUs, and GPUs are sibling resource types; their
topology uses `iri:has-node`, `iri:has-cpu`, and `iri:has-gpu`.

## Start here

| I want to… | Start here |
|---|---|
| Understand the DOE-IRI namespace | [URN Registry](urns/README.md) |
| Find a Resource Type | [Resource Type URNs](urns/resource-types.md) |
| Find a controlled attribute value | [Controlled Attribute URNs](urns/attributes.md) |
| Describe a typed Resource | Its linked Resource Definition profile |
| Understand a relationship | [Link Relation Index](relations/README.md) |
| Understand the common Resource representation | [IRI Status Resource Profile](profiles/status/resource.md) |

*IRI specification — DOE Integrated Research Infrastructure*
