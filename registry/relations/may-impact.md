# IRI Link Relation: `may-impact`

**Relation URI:** `https://iri.science/rels/may-impact`<br>
**CURIE:** `iri:may-impact`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** Facility API `Incident` representation.<br>
**Target representation type:** DOE-IRI `Resource` representation identified by the source Incident's `resource_uris`.<br>
**Target resource type:** Any registered DOE-IRI resource type (`urn:doe-iri:resource:*`)

This document defines the `iri:may-impact` relationship used by Facility API Incident representations.

The canonical relation URI is `https://iri.science/rels/may-impact`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:may-impact`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:may-impact` |
| Relation URI | `https://iri.science/rels/may-impact` |
| Status | `provisional` |
| Semantic meaning | Identifies DOE-IRI Resources that may be affected by the source Incident. |
| Source representation type | Facility API `Incident` representation. |
| Target representation type | DOE-IRI `Resource` representation identified by the source Incident's `resource_uris`. |
| Cardinality | `0..*` targets from an Incident representation. |
| Target stability | Resource representation. Each target identifies a Resource in the Incident's assessed impact scope. |
| Authorization affects visibility | Yes. The relationship or individual Resource targets MAY be omitted when the requester is not authorized to discover them; absence does not generally prove that no targets exist. |
| Target classification | Resource |
| Relationship volatility | May change as Incident scope is assessed. |

## 2. Semantic Meaning

The `iri:may-impact` relationship identifies Resources that may be affected by an Incident. It provides HAL navigation to the DOE-IRI Resource representations named by the Incident's legacy `resource_uris` field.

The relationship expresses assessed or potential scope. It does not assert that every target is currently unavailable, impaired, or experiencing the same Event. `iri:impacts` is distinct because it identifies the one Resource to which a particular Event applies.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `Incident` representation and MUST target DOE-IRI `Resource` representations identified by that Incident's `resource_uris`.

The targets are Resources, not operation entry points or relationship resources.

## 4. Cardinality

An Incident MAY identify zero, one, or multiple potentially affected Resources:

```text
Incident  -- iri:may-impact -->  Resource
   1                0..*
```

The HAL relation uses an array when multiple targets are supplied. It does not impose an inverse-cardinality requirement.

## 5. Static and Dynamic Semantics

The target set may change as the Incident's scope is assessed, confirmed, or narrowed. It is not a substitute for current health, availability, capacity, or other operational state for a target Resource.

## 6. Authorization and Visibility

Authorization MAY affect Resource discoverability. A provider MAY expose an Incident while omitting individual `iri:may-impact` targets that the requester is not authorized to discover. The absence of visible targets does not generally prove that the Incident has no potential impacts.

## 7. Compatibility

This relation is additive. The required `resource_uris` array remains authoritative during migration.

1. Producers retain `resource_uris`.
2. Producers MAY add `_links["iri:may-impact"]` as an array of HAL links.
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
    "iri:may-impact": [
      { "href": "/api/v2/status/resources/pioneer" },
      { "href": "/api/v2/status/resources/pioneer-scratch" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: may-impact*
