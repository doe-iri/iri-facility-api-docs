# IRI Link Relation: `generated-by`

**Relation URI:** `https://iri.science/rels/generated-by`<br>
**CURIE:** `iri:generated-by`<br>
**Status:** Provisional<br>
**Version:** 1.0.0<br>
**Source representation type:** Facility API `Event` representation.<br>
**Target representation type:** Facility API `Incident` representation identified by the source Event's `incident_uri`.
**Target representation profile:** `https://iri.science/profiles/status/incident`

This document defines the `iri:generated-by` relationship used by Facility API Event representations.

The canonical relation URI is `https://iri.science/rels/generated-by`. With
the canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:generated-by` expands to that URI. The relation URI identifies the
link-relation semantics and is distinct from any target representation profile.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:generated-by` |
| Relation URI | `https://iri.science/rels/generated-by` |
| Status | `provisional` |
| Semantic meaning | Identifies the Incident with which the source Event is associated. |
| Source representation type | Facility API `Event` representation. |
| Target representation type | Facility API `Incident` representation identified by the source Event's `incident_uri`. |
| Cardinality | `0..1` target from an Event representation. |
| Target stability | API resource representation. The association is stable once it is set for the Event. |
| Authorization affects visibility | Yes. A provider MAY omit the relation when the target Incident is not visible to the requester; its absence does not generally prove that no association exists. |
| Target classification | API resource; not a DOE-IRI typed `Resource`, operation entry point, or relationship resource. |
| Relationship volatility | Stable association once set. A null `incident_uri` represents no associated Incident. |

## 2. Semantic Meaning

The `iri:generated-by` relationship identifies the Incident associated with an Event. It provides HAL navigation to the Incident representation named by the Event's legacy `incident_uri` field.

The relationship does not assert that the Incident currently remains active or that it is the sole cause of an Event. Its target is the Incident API resource; any DOE-IRI Resource referenced by the Event is a separate `iri:impacts` target. This relation does not assert current Resource health, availability, or other operational state.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `Event` representation and, when present, MUST target the Facility API `Incident` representation identified by that Event's `incident_uri`.

The target is an independently identifiable API resource, not a DOE-IRI typed Resource, operation entry point, or relationship resource.

## 4. Cardinality

An Event has zero or one associated Incident:

```text
Event  -- iri:generated-by -->  Incident
  1              0..1
```

The HAL relation uses a singular link object when it is supplied. A null `incident_uri` omits `iri:generated-by`; it MUST NOT produce a link with `"href": null`.

## 5. Static and Dynamic Semantics

The Event-to-Incident association is stable once set. It is not a live assertion about Incident status, Resource health, availability, or impact scope.

## 6. Authorization and Visibility

Authorization MAY affect whether an associated Incident is discoverable. A provider MAY omit `iri:generated-by` when it cannot reveal the target. The absence of a visible relation does not generally prove that the Event has no associated Incident.

When a requester can observe a null `incident_uri`, that null is the authoritative legacy statement that the Event has no associated Incident.

## 7. Compatibility

This relation is additive. The required, nullable `incident_uri` field remains authoritative during migration.

1. Producers retain `incident_uri`.
2. Producers MAY add `_links["iri:generated-by"]` when `incident_uri` is non-null and the target is visible.
3. Whenever both forms are present, the link's `href` MUST equal `incident_uri`.
4. A null `incident_uri` maps to an omitted relation, never a null `href`.
5. Consumers SHOULD prefer the advertised relation and MAY fall back to `incident_uri`.

Removing or changing `incident_uri` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "incident_uri": "/api/v2/status/incidents/network-maintenance",
  "_links": {
    "iri:generated-by": {
      "href": "/api/v2/status/incidents/network-maintenance"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: generated-by*
