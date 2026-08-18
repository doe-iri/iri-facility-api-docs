# IRI Link Relation: `has-capability`

**Relation URI:** `https://iri.science/rels/has-capability`\
**CURIE:** `iri:has-capability`\
**Status:** Provisional\
**Version:** 1.0.0<br>
**Source representation type:** DOE-IRI `Resource` representation or Facility API `ProjectAllocation` representation.<br>
**Source resource type:** Any registered DOE-IRI resource type (`urn:doe-iri:resource:*`) when the source is a Resource; not applicable when the source is a ProjectAllocation.<br>
**Target representation type:** Facility API `Capability` representation identified by `capability_uris` on a Resource or `capability_uri` on a ProjectAllocation.

This document defines the `iri:has-capability` relationship used by Facility API Resource and ProjectAllocation representations.

The canonical relation URI is `https://iri.science/rels/has-capability`. With
the canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:has-capability` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-capability` |
| Relation URI | `https://iri.science/rels/has-capability` |
| Status | `provisional` |
| Semantic meaning | Identifies a Capability associated with the source. For a Resource, the Capability is provided by that Resource; for a ProjectAllocation, it is the Capability to which the allocation applies. |
| Source representation type | DOE-IRI `Resource` representation or Facility API `ProjectAllocation` representation. |
| Target representation type | Facility API `Capability` representation identified by `capability_uris` on a Resource or `capability_uri` on a ProjectAllocation. |
| Cardinality | Resource: `0..*` targets; ProjectAllocation: exactly `1` target under the current required `capability_uri` contract. |
| Target stability | API resource representation. The target identifies a capability in a relatively stable Resource association or stable allocation association. |
| Authorization affects visibility | Yes. The relationship or individual Capability targets MAY be omitted when the requester is not authorized to discover them; absence does not generally prove that no Capability association exists. |
| Target classification | API resource; not a DOE-IRI typed `Resource`, state object, operation entry point, or relationship resource. |
| Relationship volatility | Resource membership changes when configured capabilities change. ProjectAllocation membership is a stable accounting association that changes only when the represented allocation is reassigned or replaced. |

## 2. Semantic Meaning

The `iri:has-capability` relationship identifies a Capability associated with its source. The relation has one shared meaning, with source-specific interpretation:

- On a DOE-IRI `Resource`, the target Capability is provided by the Resource.
- On a Facility API `ProjectAllocation`, the target Capability is the Capability to which the allocation applies.

It does not assert current availability, allocation balance, enabled state, user permission, or schedulability of the Capability.

## 3. Source and Target Representation

The relationship MAY originate from either of the following source representations:

- A DOE-IRI `Resource` representation, targeting the Facility API `Capability` representations named by its `capability_uris` array.
- A Facility API `ProjectAllocation` representation, targeting the Facility API `Capability` representation named by its required `capability_uri`.

The targets are independently identifiable API resources, not DOE-IRI typed Resources, state objects, operation entry points, or relationship resources.

## 4. Cardinality

A Resource MAY identify zero, one, or multiple Capability targets:

```text
Resource  -- iri:has-capability -->  Capability
   1                 0..*
```

A ProjectAllocation has exactly one semantic Capability target under the current required `capability_uri` contract:

```text
ProjectAllocation  -- iri:has-capability -->  Capability
       1                      1
```

A Resource uses an array when multiple targets are supplied. A ProjectAllocation uses a singular link object. During the additive transition, `_links` remains optional even for the exact-one ProjectAllocation association.

## 5. Static and Dynamic Semantics

For a Resource, this relation describes relatively stable configured capability membership and SHOULD NOT change solely because a Capability is temporarily unavailable, exhausted, disabled for a requester, or otherwise affected by operational conditions.

For a ProjectAllocation, this relation identifies the Capability against which the allocation is recorded. It is not a live assertion of remaining allocation, current service availability, or whether the source is usable by a particular requester.

## 6. Authorization and Visibility

Authorization MAY affect Capability discoverability. A provider MAY omit individual `iri:has-capability` targets or the relation when it cannot reveal the target. The absence of visible targets does not generally prove that the source has no Capability associations.

## 7. Compatibility

This relation is additive. Existing URI fields remain authoritative during migration.

1. Resource producers retain `capability_uris` and MAY add `_links["iri:has-capability"]` as an array of HAL links.
2. ProjectAllocation producers retain `capability_uri` and MAY add `_links["iri:has-capability"]` as a singular HAL link object.
3. Whenever both forms are present, the Resource link array and `capability_uris` MUST identify the same targets, disregarding order; the ProjectAllocation link's `href` MUST equal `capability_uri`.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to the corresponding legacy URI field.

Removing or changing either URI field requires a subsequent OpenAPI change.

## 8. HAL Representation

Resource example:

```json
{
  "capability_uris": [
    "/api/v2/account/capabilities/cpu-node-hours",
    "/api/v2/account/capabilities/gpu-node-hours"
  ],
  "_links": {
    "iri:has-capability": [
      { "href": "/api/v2/account/capabilities/cpu-node-hours" },
      { "href": "/api/v2/account/capabilities/gpu-node-hours" }
    ]
  }
}
```

ProjectAllocation example:

```json
{
  "capability_uri": "/api/v2/account/capabilities/gpu-node-hours",
  "_links": {
    "iri:has-capability": {
      "href": "/api/v2/account/capabilities/gpu-node-hours"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: has-capability*
