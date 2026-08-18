# IRI Facility Profile

**Profile URI:** `https://iri.science/profiles/facility`<br>
**OpenAPI type:** `Facility`<br>
**Status:** Draft<br>
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Facility representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/facility
```

An IRI Facility represents the organizational entity that provides an IRI Facility API and coordinates one or more sites through which resources and services are exposed.

The Facility is the top-level organizational representation for a participating IRI provider. It identifies the facility itself and provides discovery of the sites associated with that facility.

A Facility is distinct from:

- a Site, which represents a physical, organizational, or logical location associated with the Facility;
- a Resource, which represents compute, storage, network, service, or other infrastructure;
- an Incident or Event, which represents dynamic operational state or activity.

The normative structural definition of a Facility representation is provided by the IRI Facility API OpenAPI specification. This profile supplements that schema with application-level semantics and interoperability requirements.

## 2. Profile Semantics

An IRI Facility representation describes the identity and organizational context of an IRI provider.

A Facility MAY contain one or more Sites.

Resources and services SHOULD be associated with Sites or other appropriate IRI resources rather than being modeled as intrinsic properties of the Facility.

The Facility representation SHOULD provide clients with sufficient hypermedia information to discover related Site representations without requiring the client to construct or infer API paths.

Clients MUST NOT assume that Facility identifiers, Site identifiers, or other identifiers encode URL structure.

## 3. Structural Contract

The structural definition of the Facility representation is defined by the IRI Facility API OpenAPI `Facility` schema.

The current Facility schema defines the following properties:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Facility. |
| `name` | No | Human-readable long name of the Facility. |
| `description` | No | Human-readable description of the Facility. |
| `last_modified` | Yes | Time at which the Facility representation was last modified. |
| `short_name` | No | Common or abbreviated name of the Facility. |
| `organization_name` | No | Name of the organization operating the Facility. |
| `support_uri` | No | URI of the Facility's support service or support portal. |
| `self_uri` | Yes | Canonical API URI of the Facility representation. |
| `site_uris` | Yes | URIs identifying Sites associated with the Facility. |

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- formats;
- structural validation;
- read-only properties.

This profile is authoritative for additional semantic and interoperability conventions associated with those properties and their corresponding hypermedia relationships.

## 4. Facility Identity

The `id` property identifies the Facility.

The identifier MUST be stable within the identifier scope established by the IRI Facility API.

Clients MUST treat `id` as an opaque identifier unless a separate specification explicitly defines internal semantics for the identifier.

Clients MUST NOT construct API URLs by combining the Facility identifier with assumed path templates.

For example, a client MUST NOT assume that a Facility having:

```json
{
  "id": "nersc"
}
```

can necessarily be retrieved by constructing:

```text
/api/v2/facility/nersc
```

The canonical API location of a representation MUST instead be determined from an advertised URI or hypermedia link.

## 5. Facility Naming

### 5.1 `name`

`name` provides the human-readable formal or descriptive name of the Facility.

Example:

```json
{
  "name": "National Energy Research Scientific Computing Center"
}
```

### 5.2 `short_name`

`short_name` provides the commonly used abbreviated name of the Facility.

Example:

```json
{
  "short_name": "NERSC"
}
```

Clients SHOULD use `short_name` for concise presentation when available and `name` when a full descriptive name is appropriate.

Neither property serves as the Facility's stable identifier.

## 6. Operating Organization

`organization_name` identifies the organization responsible for operating the Facility.

For example:

```json
{
  "organization_name": "Lawrence Berkeley National Laboratory"
}
```

The operating organization is descriptive information and MUST NOT be interpreted as the Facility's unique identity.

Multiple Facilities MAY be operated by the same organization.

## 7. Support Information

`support_uri` identifies a Facility-provided support resource.

For example:

```json
{
  "support_uri": "https://support.example.org/"
}
```

The support URI MAY identify a support portal, documentation system, ticketing interface, or other Facility-defined support entry point.

The presence of a support URI does not imply a particular support protocol or authentication mechanism.

Where IRI subsequently defines a registered hypermedia relation for Facility support, that relation SHOULD be preferred for hypermedia discovery while `support_uri` MAY be retained for compatibility with the OpenAPI data model.

## 8. Facility and Site Relationship

A Facility MAY be associated with one or more Site resources.

The current OpenAPI representation exposes these associations through:

```text
site_uris
```

Each URI identifies an IRI Site associated with the Facility.

A Site representation conforming to the IRI Facility Site Profile is identified by:

```text
https://iri.science/profiles/facility/site
```

The association between a Facility and a Site is a resource relationship and SHOULD be represented using hypermedia links when HAL-style representations are used.

Clients SHOULD NOT derive Site URLs from Facility or Site identifiers.

## 9. Hypermedia Representation

When represented using HAL, the Facility SHOULD advertise related resources through `_links`.

For example:

```json
{
  "id": "nersc",
  "name": "National Energy Research Scientific Computing Center",
  "short_name": "NERSC",
  "organization_name": "Lawrence Berkeley National Laboratory",
  "last_modified": "2026-08-17T12:00:00Z",

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/facility",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/facility"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "iri:site": [
      {
        "href": "https://api.example.org/api/v2/facility/sites/berkeley",
        "title": "Berkeley Site",
        "type": "application/hal+json",
        "profile": "https://iri.science/profiles/facility/site"
      },
      {
        "href": "https://api.example.org/api/v2/facility/sites/nersc",
        "title": "NERSC Site",
        "type": "application/hal+json",
        "profile": "https://iri.science/profiles/facility/site"
      }
    ]
  }
}
```

In this representation:

- `self` identifies the Facility representation itself;
- the `profile` on `self` identifies the Facility representation profile;
- `iri:site` identifies the relationship between the Facility and associated Site resources;
- each `href` identifies an actual Site resource;
- `type` identifies the expected media type of the target representation;
- `profile` identifies the semantic profile of the target Site representation.

The relation URI and representation profile URI serve different purposes and MUST NOT be treated as interchangeable identifiers.

## 10. Relationship URI

If `iri:site` is registered as the IRI relation identifying a Site associated with a Facility, the CURIE:

```text
iri:site
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
https://iri.science/rels/site
```

The canonical relation document defines the meaning of the Facility-to-Site relationship.

The Facility profile MUST NOT redefine the normative semantics of the `iri:site` relation.

## 11. Relationship to Existing URI Properties

The current IRI Facility OpenAPI schema defines:

```text
self_uri
site_uris
```

These properties expose resource URIs directly in the representation.

When the IRI HAL hypermedia model is used, the corresponding relationships SHOULD be represented through `_links`:

```text
self_uri
    ↓
_links.self

site_uris
    ↓
_links["iri:site"]
```

For example:

```json
{
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/facility"
    },
    "iri:site": [
      {
        "href": "https://api.example.org/api/v2/facility/sites/berkeley"
      },
      {
        "href": "https://api.example.org/api/v2/facility/sites/nersc"
      }
    ]
  }
}
```

The IRI specification SHOULD define whether the legacy URI properties remain present for backward compatibility or are superseded by the corresponding HAL links in a future API version.

Clients implementing the HAL representation SHOULD use the advertised `_links` rather than constructing URLs or depending upon URI-valued properties for navigation.

## 12. Media Type

This profile identifies the semantics of the Facility representation independently of a particular serialization.

When a Facility is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile through the `profile` parameter or a HAL Link Object where appropriate:

```text
https://iri.science/profiles/facility
```

The profile URI does not replace the media type.

The media type identifies how the representation is encoded; the profile identifies the additional IRI Facility semantics applied to that representation.

## 13. Static and Dynamic Semantics

A Facility representation primarily describes relatively stable organizational and discovery information.

The existence of a Facility or Site relationship MUST NOT be interpreted as evidence that:

- the Facility is currently fully operational;
- a Site is currently available;
- resources at the Site are currently available;
- a particular service is currently operational.

Dynamic operational information SHOULD be represented through the applicable IRI status resources, incidents, events, or other state representations.

## 14. Authorization and Visibility

Authorization MAY affect information exposed through a Facility representation.

A provider MAY omit Sites, links, support information, or other information when the requester is not authorized to discover that information.

The absence of a Site or other relationship from a Facility representation MUST NOT necessarily be interpreted as proof that the Site or relationship does not exist.

Clients SHOULD treat the representation as the set of Facility information visible to the authenticated requester.

## 15. Conformance

A representation conforms to the IRI Facility Profile when:

1. it conforms to the applicable IRI Facility API `Facility` schema;
2. its properties are interpreted according to the semantics defined by the IRI Facility API and this profile;
3. identifiers are treated as identifiers rather than URL templates;
4. related resources are discoverable through defined URIs or registered hypermedia relationships;
5. IRI-specific link relations use the canonical IRI relation namespace;
6. profile URIs identify representation semantics and are not used as substitutes for link-relation identifiers;
7. clients are not required to infer or construct related-resource URLs.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 16. Profile Identification

The canonical identifier for this profile is:

```text
https://iri.science/profiles/facility
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

## 17. Versioning

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes that materially alter the interpretation or processing semantics of the Facility representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Facility Profile*