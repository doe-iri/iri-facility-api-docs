# Link Profile: `iri:has-event`

This document defines the `iri:has-event` relationship used by Facility API Incident representations.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:has-event` |
| Status | `provisional` |
| Semantic meaning | Identifies Events recorded as part of the source Incident. |
| Source representation type | Facility API `Incident` representation. |
| Target representation type | Facility API `Event` representation identified by the source Incident's `event_uris`. |
| Cardinality | `0..*` targets from an Incident representation. |
| Target stability | API resource representation. Each target identifies a recorded Event. |
| Authorization affects visibility | Yes. The relationship or individual Event targets MAY be omitted when the requester is not authorized to discover them; absence does not generally prove that no Events exist. |
| Target classification | API resource; not a DOE-IRI typed `Resource`, state object, operation entry point, or relationship resource. |
| Relationship volatility | Membership may grow as Events are recorded for the Incident. |

## 2. Semantic Meaning

The `iri:has-event` relationship identifies Events recorded as part of an Incident. It provides navigation to the Event representations named by the Incident's legacy `event_uris` field.

The relationship does not establish a required inverse for every Event, and it does not itself determine an Incident's current status, resolution, or impact scope.

## 3. Source and Target Representation

The relationship MAY originate only from a Facility API `Incident` representation and MUST target Facility API `Event` representations identified by that Incident's `event_uris`.

The targets are independently identifiable API resources, not DOE-IRI typed Resources, state objects, operation entry points, or relationship resources.

## 4. Cardinality

An Incident MAY identify zero, one, or multiple recorded Events:

```text
Incident  -- iri:has-event -->  Event
   1               0..*
```

The HAL relation uses an array when multiple Event targets are supplied. It does not impose an inverse-cardinality requirement.

## 5. Static and Dynamic Semantics

The membership can grow as Events are recorded. Existing Event identity is not a live status assertion, and clients MUST use the target Event and Incident representations for their current properties.

## 6. Authorization and Visibility

Authorization MAY affect Event discoverability. A provider MAY expose an Incident while omitting individual `iri:has-event` targets that the requester is not authorized to discover. The absence of visible targets does not generally prove that the Incident has no Events.

## 7. Compatibility

This relation is additive. The required `event_uris` array remains authoritative during migration.

1. Producers retain `event_uris`.
2. Producers MAY add `_links["iri:has-event"]` as an array of HAL links.
3. Whenever both forms are present, the link array and `event_uris` MUST identify the same targets, disregarding order.
4. Consumers SHOULD prefer the advertised relation and MAY fall back to `event_uris`.

Removing or changing `event_uris` requires a subsequent OpenAPI change.

## 8. HAL Representation

```json
{
  "event_uris": [
    "/api/v2/status/events/network-maintenance-start",
    "/api/v2/status/events/network-maintenance-complete"
  ],
  "_links": {
    "iri:has-event": [
      { "href": "/api/v2/status/events/network-maintenance-start" },
      { "href": "/api/v2/status/events/network-maintenance-complete" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: hasEvent*
