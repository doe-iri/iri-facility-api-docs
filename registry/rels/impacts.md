# IRI Link Relation: `impacts`

**Relation URI:** `https://iri.science/rels/impacts`<br>
**CURIE:** `iri:impacts`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** Facility API `Event` representation.<br>
**Target representation type:** DOE-IRI `Resource` representation identified by the source Event's `resource_uri`.<br>
**Target resource type:** Any registered DOE-IRI resource type (`urn:doe-iri:resource:*`)

This document defines the `iri:impacts` relationship used by Facility API Event representations.

The canonical relation URI is `https://iri.science/rels/impacts`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`, `iri:impacts`
expands to that URI. The relation URI identifies the link-relation semantics
and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:impacts` |
| Relation URI | `https://iri.science/rels/impacts` |
| Status | `provisional` |
| Semantic meaning | Identifies the DOE-IRI Resource to which the source Event applies. |
| Source representation type | Facility API `Event` representation. |
| Target representation type | DOE-IRI `Resource` representation identified by the source Event's `resource_uri`. |
| Cardinality | Exactly `1` target under the current required `resource_uri` contract. |
| Target stability | Resource representation. The association is stable for an immutable Event. |
| Authorization affects visibility | Yes. A provider MAY omit the relation when the target Resource is not visible to the requester; absence does not generally prove that no target exists. |
| Target classification | Resource |
| Relationship volatility | Stable for an immutable Event; it is not a live assertion about the Resource's current condition. |

## 2. Semantic Meaning

The `iri:impacts` relationship identifies the Resource to which an Event applies. It provides HAL navigation to the DOE-IRI Resource representation named by the Event's legacy `resource_uri` field.

This relation is source-specific: it means an Event applies to one Resource. It MUST NOT be substituted for `iri:may-impact`, which identifies Resources within an Incident's assessed impact scope.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `Event` representation and MUST target the DOE-IRI `Resource` representation identified by that Event's required `resource_uri`.

The target is a Resource, not an operation entry point or relationship resource.

## 4. Cardinality

Each Event has exactly one semantic Resource target under the current required `resource_uri` contract:

```text
Event  -- iri:impacts -->  Resource
  1             1
```

The HAL relation uses a singular link object. During the additive transition, `_links` remains optional even though the semantic relationship is exact-one.

## 5. Static and Dynamic Semantics

The Event-to-Resource association is stable for an immutable Event. It does not by itself state that the Resource is currently degraded, unavailable, or otherwise affected; clients must consult applicable current representations.

## 6. Authorization and Visibility

Authorization MAY affect Resource discoverability. A provider MAY omit `iri:impacts` when the target cannot be revealed. The absence of a visible relation does not generally prove that the Event has no Resource target.

## 7. Compatibility

This relation is additive. The required `resource_uri` field remains authoritative during migration.

1. Producers retain `resource_uri`.
2. Producers MAY add a singular `_links["iri:impacts"]` HAL link object.
3. Whenever both forms are present, the link's `href` MUST equal `resource_uri`.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to `resource_uri`.

Removing or changing `resource_uri` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "resource_uri": "/api/v2/status/resources/pioneer",
  "_links": {
    "iri:impacts": {
      "href": "/api/v2/status/resources/pioneer",
      "profile": "https://iri.science/profiles/status/resource"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: impacts*
