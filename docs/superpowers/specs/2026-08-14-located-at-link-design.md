# `iri:located-at` Link Relationship Design

## Status

Approved in-chat design for replacing the navigation role of `Resource.site_uri`
with a registered HAL link relation while preserving the existing field during
an additive compatibility period.

Date: 2026-08-14

## 1. Objective

Register and document this provisional link relation:

```text
iri:located-at
```

The relation allows any DOE-IRI `Resource` representation to navigate to the
`Site` representation identified by its existing `site_uri` field.

## 2. Semantic Contract

| Property | Decision |
|---|---|
| Relation | `iri:located-at` |
| Lifecycle | `provisional` |
| Source | Any DOE-IRI `Resource` representation |
| Target | The associated Facility API `Site` representation |
| Cardinality | Exactly one semantic target under the current Resource schema |
| Target classification | Site API representation; not a DOE-IRI typed `Resource`, state object, operation entry point, or relationship resource |
| Target stability | Independently identifiable, relatively stable Site representation |
| Relationship volatility | Relatively static site placement or administrative association |
| Authorization | Site identity is already disclosed by required `site_uri`; implementations must not independently authorization-filter the link while returning that field |

The relationship identifies the relatively stable physical and administrative
Site associated with a Resource. It does not assert current process placement,
compute hosting, endpoint reachability, health, availability, ownership, or
live routing.

`iri:located-at` is distinct from `iri:hosted-on`. The latter is limited to DTN
or inference services and identifies compute systems or nodes that provide
hosting infrastructure.

## 3. Compatibility Contract

This is an additive change. The required `site_uri` field remains authoritative
under the current Facility API schema.

During the compatibility period:

1. Producers retain `site_uri`.
2. Producers may add a singular `_links["iri:located-at"]` HAL link object.
3. Whenever the link is present, its `href` must exactly equal `site_uri`.
4. New registry examples include the link.
5. Deprecating or removing `site_uri` requires a separate approved schema
   revision.

The link target remains present across ordinary operational changes. It changes
only when the represented Resource is reassigned or relocated to another
represented Site.

## 4. HAL Example

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

The relation uses a singular HAL link object because the current `site_uri`
contract is required and singular.

## 5. Scope

This change includes the link profile, registry navigation and relationship
indexes, common Resource documentation, and complete Resource examples. It does
not add an inverse Site-to-Resource link relation, deprecate `site_uri`, alter
the Site schema, or change the meaning of `iri:hosted-on`.
