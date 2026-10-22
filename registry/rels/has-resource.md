# IRI Link Relation: `has-resource`

**Relation URI:** `https://iri.science/rels/has-resource`\
**CURIE:** `iri:has-resource`\
**Status:** Provisional\
**Version:** 1.0.0<br>
**Source representation type:** Facility API `Site` representation.<br>
**Target representation type:** DOE-IRI `Resource` representation identified by the source Site's `resource_uris`.<br>
**Target resource type:** Any registered DOE-IRI resource type (`urn:doe-iri:resource:*`)

This document defines the `iri:has-resource` relationship used by Facility API Site representations.

The canonical relation URI is `https://iri.science/rels/has-resource`. With
the canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:has-resource` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-resource` |
| Relation URI | `https://iri.science/rels/has-resource` |
| Status | `provisional` |
| Semantic meaning | Identifies DOE-IRI Resources hosted at the source Site. |
| Source representation type | Facility API `Site` representation. |
| Target representation type | DOE-IRI `Resource` representation identified by the source Site's `resource_uris`. |
| Cardinality | `0..*` targets from a Site representation. |
| Target stability | Resource representation. The target identifies a Resource associated with the Site's relatively stable topology. |
| Authorization affects visibility | Yes. The relationship or individual Resource targets MAY be omitted when the requester is not authorized to discover them; absence does not generally prove that no Resources exist. |
| Target classification | Resource |
| Relationship volatility | Relatively stable Site topology. Changes when represented Resource placement or Site association changes. |

## 2. Semantic Meaning

The `iri:has-resource` relationship identifies Resources hosted at a Site. It provides HAL navigation to the DOE-IRI Resource representations named by the Site's legacy `resource_uris` field.

The relationship describes Site topology or administrative association. It does not assert current Resource reachability, health, availability, workload activity, or operational placement beyond the represented Site association.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `Site` representation and MUST target DOE-IRI `Resource` representations identified by that Site's `resource_uris`.

The targets are Resources, not operation entry points or relationship resources.

## 4. Cardinality

A Site MAY identify zero, one, or multiple Resources:

```text
Site  -- iri:has-resource -->  Resource
 1              0..*
```

The HAL relation uses an array when multiple targets are supplied. It does not impose an inverse-cardinality requirement.

## 5. Static and Dynamic Semantics

`iri:has-resource` describes relatively stable Site topology. It SHOULD remain present across ordinary operational changes such as temporary Resource unavailability, maintenance, health changes, or workload activity.

## 6. Authorization and Visibility

Authorization MAY affect Resource discoverability. A provider MAY expose a Site while omitting individual `iri:has-resource` targets that the requester is not authorized to discover. The absence of visible targets does not generally prove that the Site has no associated Resources.

## 7. Compatibility

This relation is additive. The required `resource_uris` array remains authoritative during migration.

1. Producers retain `resource_uris`.
2. Producers MAY add `_links["iri:has-resource"]` as an array of HAL links.
3. Whenever both forms are present, the link array and `resource_uris` MUST identify the same targets, disregarding order.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to `resource_uris`.

Removing or changing `resource_uris` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "resource_uris": [
    "/api/v2/status/resources/pioneer",
    "/api/v2/status/resources/pioneer-scratch"
  ],
  "_links": {
    "iri:has-resource": [
      { "href": "/api/v2/status/resources/pioneer", "profile": "https://iri.science/profiles/status/resource" },
      { "href": "/api/v2/status/resources/pioneer-scratch", "profile": "https://iri.science/profiles/status/resource" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: has-resource*
