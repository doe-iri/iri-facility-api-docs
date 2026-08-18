# IRI Link Relation: `has-site`

**Relation URI:** `https://iri.science/rels/has-site`<br>
**CURIE:** `iri:has-site`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** Facility API `Facility` representation.<br>
**Target representation type:** Facility API `Site` representation.
**Target representation profile:** `https://iri.science/profiles/facility/site`

This document defines the `iri:has-site` relationship used by Facility API Facility representations.

The canonical relation URI is `https://iri.science/rels/has-site`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:has-site`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-site` |
| Relation URI | `https://iri.science/rels/has-site` |
| Status | `provisional` |
| Semantic meaning | Identifies Sites associated with the source Facility. |
| Source representation type | Facility API `Facility` representation. |
| Target representation type | Facility API `Site` representation identified by the source Facility's `site_uris`. |
| Cardinality | `0..*` targets from a Facility representation. |
| Target stability | API resource representation. The target identifies a Site in the Facility's relatively stable topology or administrative association. |
| Authorization affects visibility | Yes. The relationship or individual Site targets MAY be omitted when the requester is not authorized to discover them; absence does not generally prove that no Sites exist. |
| Target classification | API resource; not a DOE-IRI typed `Resource`, state object, operation entry point, or relationship resource. |
| Relationship volatility | Relatively stable Facility topology or administrative association. Changes when the associated Site set changes. |

## 2. Semantic Meaning

The `iri:has-site` relationship identifies Sites associated with a Facility. It provides HAL navigation to the Site representations named by the Facility's legacy `site_uris` field.

The relationship does not assert current service availability, operational status, ownership transfer, or that all Resources at a Site are visible to the requester.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `Facility` representation and MUST target Facility API `Site` representations identified by that Facility's `site_uris`.

The targets are independently identifiable API resources, not DOE-IRI typed Resources, state objects, operation entry points, or relationship resources.

## 4. Cardinality

A Facility MAY identify zero, one, or multiple Sites:

```text
Facility  -- iri:has-site -->  Site
    1              0..*
```

The HAL relation uses an array when multiple targets are supplied. It does not impose an inverse-cardinality requirement.

## 5. Static and Dynamic Semantics

`iri:has-site` describes a relatively stable Facility-to-Site association. It SHOULD remain present across ordinary operational changes such as maintenance, temporary Site unavailability, or Resource health changes.

## 6. Authorization and Visibility

Authorization MAY affect Site discoverability. A provider MAY expose a Facility while omitting individual `iri:has-site` targets that the requester is not authorized to discover. The absence of visible targets does not generally prove that the Facility has no associated Sites.

## 7. Compatibility

This relation is additive. The required `site_uris` array remains authoritative during migration.

1. Producers retain `site_uris`.
2. Producers MAY add `_links["iri:has-site"]` as an array of HAL links.
3. Whenever both forms are present, the link array and `site_uris` MUST identify the same targets, disregarding order.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to `site_uris`.

Removing or changing `site_uris` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "site_uris": [
    "/api/v2/facility/sites/pioneer",
    "/api/v2/facility/sites/analysis"
  ],
  "_links": {
    "iri:has-site": [
      { "href": "/api/v2/facility/sites/pioneer" },
      { "href": "/api/v2/facility/sites/analysis" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: has-site*
