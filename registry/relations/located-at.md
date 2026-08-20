# IRI Link Relation: `located-at`

**Relation URI:** `https://iri.science/rels/located-at`<br>
**CURIE:** `iri:located-at`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** Any DOE-IRI `Resource` representation.<br>
**Source resource type:** Any registered DOE-IRI resource type (`urn:doe-iri:resource:*`)<br>
**Target representation type:** Facility API `Site` representation identified by the source Resource's `site_uri`.

This document defines the `iri:located-at` relationship used by DOE-IRI Resource representations.

The canonical relation URI is `https://iri.science/rels/located-at`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:located-at`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:located-at` |
| Relation URI | `https://iri.science/rels/located-at` |
| Status | `provisional` |
| Semantic meaning | Indicates the relatively stable physical and administrative Site associated with the source Resource. |
| Source representation type | Any DOE-IRI `Resource` representation. |
| Target representation type | Facility API `Site` representation identified by the source Resource's `site_uri`. |
| Cardinality | Exactly one semantic target under the current required, singular `site_uri` contract. |
| Target stability | Independently identifiable, relatively stable Site representation. |
| Authorization affects visibility | No. Site identity is already disclosed by required `site_uri`; an implementation MUST NOT independently authorization-filter this link while returning that field. |
| Target classification | Site API representation; not a DOE-IRI typed `Resource`, operation entry point, or relationship resource. |
| Relationship volatility | Relatively static site placement or administrative association. It changes only when the represented Resource is reassigned or relocated to another represented Site. |

## 2. Semantic Meaning

The `iri:located-at` relationship identifies the relatively stable physical and administrative Site associated with a Resource. It provides HAL navigation to the Site representation identified by the Resource's `site_uri` field.  In the future, the Resource's `site_uri` field will be deprecated.

The relationship MUST NOT be interpreted as asserting current process placement, compute hosting, endpoint reachability, health, availability, ownership, or live routing.

`iri:located-at` is distinct from `iri:hosted-on`. `iri:hosted-on` is limited to DTN or inference services and identifies compute systems or nodes that provide hosting infrastructure. `iri:located-at` applies to any DOE-IRI Resource and identifies its associated Site.

## 3. Source and Target Representation

The relationship MAY originate from any DOE-IRI `Resource` representation and MUST target the Facility API `Site` representation identified by that Resource's `site_uri`.

The target is a Site API representation, not a DOE-IRI typed Resource, operation entry point, or relationship resource.

## 4. Cardinality

Each Resource has exactly one semantic Site target under the current required, singular `site_uri` contract:

```text
Resource  -- iri:located-at -->  Site
   1                1
```

The HAL relation uses a singular link object. It does not define an inverse Site-to-Resource relationship.

## 5. Static and Dynamic Semantics

`iri:located-at` describes relatively static site placement or administrative association. The relationship SHOULD remain present across ordinary operational changes, including process placement changes, compute-host changes, endpoint reachability changes, health changes, availability changes, and live-routing changes.

Ordinary operational changes do not alter this relation. The relationship changes only when the represented Resource is reassigned or relocated to another represented Site.

## 6. Authorization and Visibility

The Site identity is already disclosed by the required `site_uri` field. An implementation MUST NOT independently authorization-filter `iri:located-at` while returning `site_uri`.

## 7. Compatibility

This relation is additive. `site_uri` remains required and authoritative under the current Facility API schema.

During the compatibility period:

1. Producers retain `site_uri`.
2. Producers MAY add a singular `_links["iri:located-at"]` HAL link object.
3. Whenever the link is present, its `href` MUST exactly equal `site_uri`.
4. New registry examples include the link.

Deprecating or removing `site_uri` requires a separate approved schema revision.

## 8. HAL Representation

```json
{
  "site_uri": "https://api.example.gov/api/v2/facility/sites/example-site",
  "_links": {
    "iri:located-at": {
      "href": "https://api.example.gov/api/v2/facility/sites/example-site"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: located-at*
