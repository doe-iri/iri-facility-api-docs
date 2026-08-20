# IRI Link Relation: `has-project`

**Relation URI:** `https://iri.science/rels/has-project`\
**CURIE:** `iri:has-project`\
**Status:** Provisional\
**Version:** 1.0.0<br>
**Source representation type:** Facility API `ProjectAllocation` representation.<br>
**Target representation type:** Facility API `Project` representation identified by the source ProjectAllocation's `project_uri`.

This document defines the `iri:has-project` relationship used by Facility API ProjectAllocation representations.

The canonical relation URI is `https://iri.science/rels/has-project`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:has-project`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-project` |
| Relation URI | `https://iri.science/rels/has-project` |
| Status | `provisional` |
| Semantic meaning | Identifies the Project to which the source ProjectAllocation belongs. |
| Source representation type | Facility API `ProjectAllocation` representation. |
| Target representation type | Facility API `Project` representation identified by the source ProjectAllocation's `project_uri`. |
| Cardinality | Exactly `1` target under the current required `project_uri` contract. |
| Target stability | API resource representation. The target identifies the Project in a stable accounting association. |
| Authorization affects visibility | Yes. A provider MAY omit the relation when the target Project is not visible to the requester; absence does not generally prove that no Project association exists. |
| Target classification | API resource; not a DOE-IRI typed `Resource`, operation entry point, or relationship resource. |
| Relationship volatility | Stable accounting association. Changes only when the represented allocation is reassigned or replaced. |

## 2. Semantic Meaning

The `iri:has-project` relationship identifies the Project to which a ProjectAllocation belongs. It provides HAL navigation to the Project representation named by the ProjectAllocation's legacy `project_uri` field.

The relationship identifies accounting hierarchy; it does not assert that the Project is currently active, that its allocation has remaining capacity, or that any user is authorized to consume the allocation.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `ProjectAllocation` representation and MUST target the Facility API `Project` representation identified by that allocation's required `project_uri`.

The target is an independently identifiable API resource, not a DOE-IRI typed Resource, operation entry point, or relationship resource.

## 4. Cardinality

Each ProjectAllocation has exactly one semantic Project target under the current required `project_uri` contract:

```text
ProjectAllocation  -- iri:has-project -->  Project
       1                    1
```

The HAL relation uses a singular link object. During the additive transition, `_links` remains optional even though the semantic relationship is exact-one.

## 5. Static and Dynamic Semantics

The ProjectAllocation-to-Project association is a stable accounting relationship. It is not a live assertion about allocation balances, Project activity, current user membership, authorization, or schedulability. Clients MUST use the relevant current representations and governing API contracts for those conditions.

## 6. Authorization and Visibility

Authorization MAY affect Project discoverability. A provider MAY omit `iri:has-project` when it cannot reveal the target Project. The absence of a visible relation does not generally prove that the ProjectAllocation has no Project target.

## 7. Compatibility

This relation is additive. The required `project_uri` field remains authoritative during migration.

1. Producers retain `project_uri`.
2. Producers MAY add a singular `_links["iri:has-project"]` HAL link object.
3. Whenever both forms are present, the link's `href` MUST equal `project_uri`.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to `project_uri`.

Removing or changing `project_uri` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "project_uri": "/api/v2/account/projects/climate-simulation",
  "_links": {
    "iri:has-project": {
      "href": "/api/v2/account/projects/climate-simulation"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: has-project*
