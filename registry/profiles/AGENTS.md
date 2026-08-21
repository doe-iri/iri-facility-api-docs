# IRI Representation Profile Instructions

These rules apply under `registry/profiles/`.

Read `registry/profiles/README.md` when present for the current profile index
and canonical profile URI mappings.

## 1. Profile Classes

Two profile classes are used here:

```text
Representation Profile
    Semantic/interoperability conventions for an independently meaningful
    API representation.

Resource Definition Profile
    Additional type-specific semantics for the existing IRI v2 Resource
    representation selected by resource_type.
```

A Resource Definition Profile does not define a separate Resource Definition
API object, endpoint, or lifecycle in IRI v2.

## 2. Resource Definition Profile Format

Resource Definition Profiles live under:

```text
resource-definition/<domain>/<type>.md
```

and use canonical URIs:

```text
https://iri.science/profiles/resource-definition/<domain>/<type>
```

Recommended content:

1. title;
2. Profile URI, Base Profile, Resource Type, status, version;
3. applicability;
4. conceptual model;
5. type-specific attributes;
6. controlled-value semantics where applicable;
7. OpenAPI/JSON Schema fragment when useful;
8. example Resource representation;
9. applicable links/operations;
10. conformance notes.

Resource Type registration remains authoritative in
`registry/urns/resource-types.md`. Controlled values remain authoritative in
`registry/urns/attributes.md`.

## 3. OpenAPI Boundary

OpenAPI is authoritative for:

- property existence;
- types;
- required/optional rules;
- nullability;
- formats;
- structural validation;
- operation shapes.

Profiles interpret those structures semantically. Do not silently narrow or
contradict the checked-out OpenAPI contract.

When profiles use reusable DOE-IRI URN schemas, reuse the repository's canonical
schema/reference instead of creating an independent URN grammar.

## 4. HAL Target Profile Rule

In a HAL Link Object, `profile` describes the TARGET representation.

Use the four-layer distinction:

```text
relation
    WHY is the target linked?

href
    WHERE is the target?

type
    HOW is the target represented?

profile
    WHAT semantic representation contract applies to the target?
```

Example:

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/example-mount",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    }
  }
}
```

The relation definition is authoritative for target classification.

When the target is an IRI representation with a known canonical profile,
examples SHOULD include that target profile.

Do not add an IRI representation profile to:

- `curies`;
- `service-desc`;
- ordinary external `help` targets;
- operation entry points such as `iri:submit-job`.

For polymorphic relations such as `iri:attached-to` and `iri:hosted-on`, choose
the profile from the actual target type in the example.

For `_links.self`, use the profile applicable to the represented object. In a
Resource Definition Profile example, use that Resource Definition Profile.

## 5. Attributes

Use ordinary JSON names for profile properties.
Controlled DOE-IRI URNs are values when the applicable vocabulary requires
them.

`schema_version` is normally required for Resource Definition attribute
contracts where that convention is already established.

URN arrays should use `uniqueItems: true` when duplicates have no semantic
meaning.

Prefer omission of unknown optional values over guessed values.

A profile may define configuration, capabilities, descriptive metadata,
quantitative values, or time-varying observations when appropriate. Do not
apply a blanket "stable only" rule solely to anticipate a future IRI v3 state
model.

Do not duplicate or override common top-level Resource properties such as
`current_status`.

## 6. Relations and Operation Affordances

Profiles may state which registered relations are applicable to the
representation, but the relation definition under `registry/relations/` owns
the relation semantics.

Profiles may advertise operation-affordance relations. OpenAPI remains
authoritative for HTTP method, request/response schema, parameters, security,
and errors.

Do not infer operation paths from Resource Type or profile identifiers.

## 7. Profile Task Size

A normal profile implementation task should modify:

- one profile; or
- one tightly coupled family of profiles, normally no more than about six
  files.

If a profile edit requires new URNs or relations, stop and route those as
separate semantic decisions before implementing the profile change.

## 8. Validation

For changed profiles:

- parse changed fenced JSON/YAML examples where practical;
- verify all `iri:*` relations are registered;
- verify controlled URNs used normatively are registered;
- verify profile URIs are canonical;
- verify HAL link `profile` values describe targets;
- run `git diff --check`.

Avoid repository-wide validation unless the change is a profile-wide migration.
