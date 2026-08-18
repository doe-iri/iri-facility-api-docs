# IRI Facility Site Profile

**Profile URI:** `https://iri.science/profiles/facility/site`<br>
**OpenAPI type:** `Site`<br>
**Status:** Draft<br>
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Facility Site representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/facility/site
```

An IRI Site represents a physical site that hosts IRI resources and is associated with an IRI Facility.

A Site provides physical, geographic, and organizational context for resources exposed through the IRI Facility API.

A Site is distinct from:

* a Facility, which represents the organizational entity providing the IRI Facility API;
* a Resource, which represents compute, storage, network, service, or other infrastructure associated with a Site;
* an Incident or Event, which represents dynamic operational state or activity.

The normative structural definition of a Site representation is provided by the IRI Facility API OpenAPI specification. This profile supplements that schema with application-level semantics and interoperability requirements.

## 2. Profile Semantics

An IRI Site representation describes a relatively stable physical and administrative location associated with an IRI Facility.

A Site MAY host zero or more IRI Resources.

Resources hosted at a Site SHOULD be represented as independent IRI Resource representations and related to the Site through defined IRI link relations rather than being embedded as intrinsic Site attributes.

The Site representation SHOULD provide clients with sufficient hypermedia information to discover Resources associated with the Site without requiring the client to construct or infer API paths.

Clients MUST NOT assume that Site identifiers, Resource identifiers, or other identifiers encode URL structure.

## 3. Structural Contract

The structural definition of the Site representation is defined by the IRI Facility API OpenAPI `Site` schema.

The current Site schema defines the following properties:

| Property                 | Required | Semantic purpose                                                                                                        |
| ------------------------ | -------: | ----------------------------------------------------------------------------------------------------------------------- |
| `id`                     |      Yes | Stable identifier for the Site.                                                                                         |
| `name`                   |       No | Human-readable long name of the Site.                                                                                   |
| `description`            |       No | Human-readable description of the Site.                                                                                 |
| `last_modified`          |      Yes | Time at which the Site representation was last modified.                                                                |
| `short_name`             |       No | Common or abbreviated name of the Site.                                                                                 |
| `operating_organization` |      Yes | Organization responsible for operating the Site. The property is required by the current schema but MAY contain `null`. |
| `country_name`           |       No | Country in which the Site is located.                                                                                   |
| `locality_name`          |       No | City or locality in which the Site is located.                                                                          |
| `state_or_province_name` |       No | State, province, or comparable administrative subdivision in which the Site is located.                                 |
| `street_address`         |       No | Street address associated with the Site.                                                                                |
| `unlocode`               |       No | United Nations Code for Trade and Transport Locations associated with the Site.                                         |
| `altitude`               |       No | Altitude associated with the Site location.                                                                             |
| `latitude`               |       No | Geographic latitude of the Site.                                                                                        |
| `longitude`              |       No | Geographic longitude of the Site.                                                                                       |
| `self_uri`               |      Yes | Canonical API URI of the Site representation.                                                                           |
| `resource_uris`          |      Yes | URIs identifying Resources hosted at the Site.                                                                          |

The OpenAPI schema is authoritative for:

* property names;
* JSON data types;
* required properties;
* nullable properties;
* formats;
* structural validation;
* read-only properties.

This profile is authoritative for additional semantic and interoperability conventions associated with those properties and their corresponding hypermedia relationships.

## 4. Site Identity

The `id` property identifies the Site.

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless a separate IRI specification explicitly defines internal semantics for that identifier.

Clients MUST NOT construct API URLs by combining the Site identifier with assumed path templates.

For example, a client MUST NOT assume that a Site having:

```json
{
  "id": "nersc"
}
```

can necessarily be retrieved by constructing:

```text
/api/v2/facility/sites/nersc
```

The canonical API location of a Site representation MUST instead be determined from an advertised URI or hypermedia link.

## 5. Site Naming

### 5.1 `name`

`name` provides the human-readable formal or descriptive name of the Site.

Example:

```json
{
  "name": "NERSC Berkeley Site"
}
```

### 5.2 `short_name`

`short_name` provides the commonly used abbreviated name of the Site.

Example:

```json
{
  "short_name": "NERSC"
}
```

Clients SHOULD use `short_name` for concise presentation when available and `name` when a full descriptive name is appropriate.

Neither property serves as the Site's stable identifier.

## 6. Operating Organization

`operating_organization` identifies the organization responsible for operating the Site.

For example:

```json
{
  "operating_organization": "Lawrence Berkeley National Laboratory"
}
```

The operating organization is descriptive organizational information and MUST NOT be interpreted as the Site's unique identity.

Multiple Sites MAY be operated by the same organization.

The current OpenAPI schema requires the `operating_organization` property to be present but permits its value to be `null`.

## 7. Geographic Location

The Site representation MAY provide geographic information using:

```text
country_name
locality_name
state_or_province_name
street_address
unlocode
altitude
latitude
longitude
```

These properties describe the physical location associated with the Site.

### 7.1 Administrative Location

The following properties provide human-readable geographic information:

* `country_name`
* `locality_name`
* `state_or_province_name`
* `street_address`

For example:

```json
{
  "country_name": "United States",
  "locality_name": "Berkeley",
  "state_or_province_name": "California",
  "street_address": "1 Cyclotron Rd"
}
```

These properties are descriptive and MUST NOT be used as stable Site identifiers.

### 7.2 UN/LOCODE

`unlocode` MAY provide the United Nations Code for Trade and Transport Locations associated with the Site.

For example:

```json
{
  "unlocode": "USOAK"
}
```

The presence of a UN/LOCODE provides standardized geographic context but does not replace the IRI Site identifier.

### 7.3 Geographic Coordinates

`latitude`, `longitude`, and `altitude` MAY provide geographic coordinates for the Site.

For example:

```json
{
  "latitude": 37.8762,
  "longitude": -122.2506,
  "altitude": 52.0
}
```

Coordinates describe the represented Site location and MUST NOT be interpreted as the Site's stable identity.

A Site MAY omit coordinates when precise geographic location is unavailable, inappropriate, or not intended for disclosure.

## 8. Site and Resource Relationship

A Site MAY host zero or more IRI Resources.

The current OpenAPI representation exposes these associations through:

```text
resource_uris
```

Each URI identifies an IRI Resource hosted at the Site.

The registered IRI link relation for navigating from a Site to its hosted Resources is:

```text
iri:has-resource
```

Its canonical relation URI is:

```text
https://iri.science/rels/has-resource
```

The relationship describes relatively stable Site topology or administrative association.

It MUST NOT be interpreted as asserting that a Resource is currently:

* reachable;
* healthy;
* available;
* processing workloads;
* operationally ready.

Those properties belong to the appropriate dynamic status representations.

## 9. Hypermedia Representation

When represented using HAL, the Site SHOULD advertise related Resources through `_links`.

For example:

```json
{
  "id": "nersc",
  "name": "NERSC Berkeley Site",
  "short_name": "NERSC",
  "operating_organization": "Lawrence Berkeley National Laboratory",
  "country_name": "United States",
  "locality_name": "Berkeley",
  "state_or_province_name": "California",
  "last_modified": "2026-08-17T12:00:00Z",

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/facility/sites/nersc",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/facility/site"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:has-resource": [
      {
        "href": "https://api.example.org/api/v2/status/resources/perlmutter",
        "title": "Perlmutter Compute System",
        "type": "application/hal+json"
      },
      {
        "href": "https://api.example.org/api/v2/status/resources/perlmutter-scratch",
        "title": "Perlmutter Scratch Filesystem",
        "type": "application/hal+json"
      }
    ]
  }
}
```

In this representation:

* `self` identifies the Site representation itself;
* the `profile` on `self` identifies the IRI Facility Site representation profile;
* `iri:has-resource` identifies the relationship between the Site and Resources hosted at the Site;
* each `href` identifies an actual Resource representation;
* `type` identifies the expected media type of the target representation.

A Resource link MAY additionally include a `profile` when a registered IRI representation profile exists for the target Resource type.

The relation URI and representation profile URI serve different purposes and MUST NOT be treated as interchangeable identifiers.

## 10. Relationship URI

The CURIE:

```text
iri:has-resource
```

expands through:

```json
{
  "name": "iri",
  "href": "https://iri.science/rels/{rel}",
  "templated": true
}
```

to:

```text
https://iri.science/rels/has-resource
```

The canonical relation document defines the normative meaning of the Site-to-Resource relationship.

The Site profile MUST NOT redefine the normative semantics of the `iri:has-resource` relation.

The inverse Resource-to-Site relationship is represented by:

```text
iri:located-at
```

with canonical relation URI:

```text
https://iri.science/rels/located-at
```

Under the current IRI Facility API model, a Resource has exactly one semantic Site target through its required `site_uri` property.

The inverse relationships describe the same Site association from opposite directions but retain independently defined link-relation semantics.

## 11. Relationship to Existing URI Properties

The current IRI Facility API OpenAPI schema defines:

```text
self_uri
resource_uris
```

These properties expose resource URIs directly in the representation.

When the IRI HAL hypermedia model is used, the corresponding relationships SHOULD be represented through `_links`:

```text
self_uri
    ↓
_links.self

resource_uris
    ↓
_links["iri:has-resource"]
```

For example:

```json
{
  "self_uri": "https://api.example.org/api/v2/facility/sites/nersc",

  "resource_uris": [
    "https://api.example.org/api/v2/status/resources/perlmutter",
    "https://api.example.org/api/v2/status/resources/perlmutter-scratch"
  ],

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/facility/sites/nersc"
    },

    "iri:has-resource": [
      {
        "href": "https://api.example.org/api/v2/status/resources/perlmutter"
      },
      {
        "href": "https://api.example.org/api/v2/status/resources/perlmutter-scratch"
      }
    ]
  }
}
```

During the compatibility period:

1. Producers retain the required `resource_uris` property.
2. Producers MAY additionally expose `_links["iri:has-resource"]`.
3. Whenever both forms are present, `resource_uris` and `_links["iri:has-resource"]` MUST identify the same targets, disregarding order.
4. Consumers SHOULD prefer the advertised hypermedia relation and MAY fall back to `resource_uris`.
5. Removing or changing the required `resource_uris` property requires a separate OpenAPI schema revision.

Likewise, `self_uri` remains authoritative under the current OpenAPI contract until changed by an approved schema revision.

Clients implementing the HAL representation SHOULD use advertised `_links` for navigation rather than constructing URLs from identifiers.

## 12. Media Type

This profile identifies the semantics of the Site representation independently of a particular serialization.

When a Site is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/facility/site
```

The profile URI does not replace the media type.

The media type identifies how the representation is encoded; the profile identifies the additional IRI Site semantics applied to that representation.

## 13. Static and Dynamic Semantics

A Site representation primarily describes relatively stable physical, organizational, geographic, and topology information.

The existence of a Site or Site-to-Resource relationship MUST NOT be interpreted as evidence that:

* the Site is currently operational;
* a Resource hosted at the Site is currently available;
* a Resource is healthy;
* a service is reachable;
* a compute system is accepting work;
* a filesystem is currently mounted or accessible.

Dynamic operational information SHOULD be represented through applicable IRI status resources, incidents, events, or other state representations.

Ordinary operational changes SHOULD NOT require changes to the Site-to-Resource relationship unless the represented Site association itself changes.

## 14. Authorization and Visibility

Authorization MAY affect information exposed through a Site representation.

A provider MAY omit Resources, relationships, geographic details, or other information when the requester is not authorized to discover that information, subject to requirements imposed by the applicable OpenAPI schema.

The absence of a Resource or relationship from a Site representation MUST NOT necessarily be interpreted as proof that the Resource or relationship does not exist.

Where `resource_uris` and `_links["iri:has-resource"]` are both returned, they MUST remain consistent with each other.

Clients SHOULD treat the representation as the set of Site information visible to the authenticated requester.

## 15. Conformance

A representation conforms to the IRI Facility Site Profile when:

1. it conforms to the applicable IRI Facility API `Site` schema;
2. its properties are interpreted according to the semantics defined by the IRI Facility API and this profile;
3. Site identifiers are treated as identifiers rather than URL templates;
4. related Resources are discoverable through defined URIs or registered hypermedia relationships;
5. IRI-specific link relations use the canonical IRI relation namespace;
6. profile URIs identify representation semantics and are not used as substitutes for link-relation identifiers;
7. `iri:has-resource` is used for Site-to-Resource hypermedia relationships;
8. when both `resource_uris` and `_links["iri:has-resource"]` are present, they identify the same targets;
9. clients are not required to infer or construct related-resource URLs.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/facility/site
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes that materially alter the interpretation or processing semantics of the Site representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Facility Site Profile*
