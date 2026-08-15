# Link Profile: `iri:has-project-allocation`

This document defines the `iri:has-project-allocation` relationship used by Facility API UserAllocation representations.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-project-allocation` |
| Status | `provisional` |
| Semantic meaning | Identifies the ProjectAllocation of which the source UserAllocation is a part. |
| Source representation type | Facility API `UserAllocation` representation. |
| Target representation type | Facility API `ProjectAllocation` representation identified by the source UserAllocation's `project_allocation_uri`. |
| Cardinality | Exactly `1` target under the current required `project_allocation_uri` contract. |
| Target stability | API resource representation. The target identifies a stable accounting hierarchy association. |
| Authorization affects visibility | Yes. A provider MAY omit the relation when the target ProjectAllocation is not visible to the requester; absence does not generally prove that no ProjectAllocation association exists. |
| Target classification | API resource; not a DOE-IRI typed `Resource`, state object, operation entry point, or relationship resource. |
| Relationship volatility | Stable accounting hierarchy. Changes only when the represented UserAllocation is reassigned or replaced. |

## 2. Semantic Meaning

The `iri:has-project-allocation` relationship identifies the ProjectAllocation of which a UserAllocation is a part. It provides HAL navigation to the ProjectAllocation representation named by the UserAllocation's legacy `project_allocation_uri` field.

The relationship identifies accounting hierarchy. It does not assert a current allocation balance, current Project activity, current authorization, or whether the user can consume the allocation.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `UserAllocation` representation and MUST target the Facility API `ProjectAllocation` representation identified by that UserAllocation's required `project_allocation_uri`.

The target is an independently identifiable API resource, not a DOE-IRI typed Resource, state object, operation entry point, or relationship resource.

## 4. Cardinality

Each UserAllocation has exactly one semantic ProjectAllocation target:

```text
UserAllocation  -- iri:has-project-allocation -->  ProjectAllocation
      1                       1
```

The HAL relation uses a singular link object. During the additive transition, `_links` remains optional even though the semantic relationship is exact-one.

## 5. Static and Dynamic Semantics

The UserAllocation-to-ProjectAllocation association is a stable accounting relationship. It is not a live assertion about remaining allocation, user eligibility, authorization, Project state, or schedulability. Clients MUST use the relevant current representations and governing API contracts for those conditions.

## 6. Authorization and Visibility

Authorization MAY affect ProjectAllocation discoverability. A provider MAY omit `iri:has-project-allocation` when it cannot reveal the target. The absence of a visible relation does not generally prove that the UserAllocation has no ProjectAllocation target.

## 7. Compatibility

This relation is additive. The required `project_allocation_uri` field remains authoritative during migration.

1. Producers retain `project_allocation_uri`.
2. Producers MAY add a singular `_links["iri:has-project-allocation"]` HAL link object.
3. Whenever both forms are present, the link's `href` MUST equal `project_allocation_uri`.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to `project_allocation_uri`.

Removing or changing `project_allocation_uri` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "project_allocation_uri": "/api/v2/account/projects/climate-simulation/project_allocations/alloc-001",
  "_links": {
    "iri:has-project-allocation": {
      "href": "/api/v2/account/projects/climate-simulation/project_allocations/alloc-001"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: hasProjectAllocation*
