# RFC: Facility-Scoped URN Instance Identifiers

## Abstract

This RFC proposes a common identifier scheme for IRI API objects:

```text
urn:doe-iri:id:<authority>:<kind>:<local-id>
```

The `authority` identifies the facility responsible for issuing the identifier,
`kind` identifies a broad API object family, and `local-id` is a permanent key
assigned by that authority. Facilities can issue identifiers independently
within their delegated namespaces. UUIDs remain usable as local keys but are
not required.

Instance identity is distinct from Resource Type URNs, representation profiles,
and the HTTP URLs used to retrieve representations. The proposal defines
issuance, persistence, comparison, and migration rules without introducing a
new representation, endpoint, link relation, or resolution service.

## Status of This Memo

**Status:** Draft / Proposed

**Target:** Explicit adoption in a future IRI API contract revision

**Revision:** 0.2

**Date:** 2026-09-27

This draft was reviewed against repository commit
[`76a4a0c89924`](https://github.com/doe-iri/iri-facility-api-docs/commit/76a4a0c89924).
The `id` branch, object-kind tokens, and instance-issuance delegations below
are proposals, not current registry assignments. Facility-specific examples
are illustrative and do not assert deployed identifiers or authorized scopes.
This draft changes neither the governing URN specification nor the OpenAPI
contract or registry assignments.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in this document are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they
appear in all capitals. These requirements describe the proposed adopted
contract; they do not impose new requirements on current IRI v2 deployments.

## 1. Motivation and Current Contract

A bare UUID can provide globally unique identity, but does not identify its
issuing facility. A facility-scoped URN adds a governed issuance namespace and
allows durable local keys without requiring globally coordinated object
registration. It does not make UUID collision avoidance obsolete, and it does
not itself provide discovery, resolution, or proof of origin.

The checked-out [IRI v2 schemas](../specification-v2/openapi/production/_components.yaml)
already declare object `id` properties as strings rather than `format: uuid`.
For `Facility`, `Site`, `Resource`, `Capability`, `Incident`, and `Event`, the
descriptions explicitly allow a UUID or URN. Other models also use string IDs,
including illustrative values such as `job-12345` and `proj-abc123`.
Thus this proposal standardizes instance naming and migrates deployed UUID or
other local identifiers; it does not remove an existing schema-wide UUID rule.

The [governing DOE-IRI URN specification](rfc-iri-urn-structure-and-registry.md)
currently defines types, controlled values, and delegated semantic extensions.
Its grammar does not include `id`. The
[URN registry](../registry/urns/README.md) reserves authority codes including
`nersc`, `alcf`, and `olcf`, but those reservations grant no instance-issuance
rights. Section 8 identifies the coordinated changes required for adoption.

## 2. Proposed Hierarchy

```text
urn:doe-iri
├── resource:...                  Resource Type URNs (existing)
├── compute:...                   Controlled compute values (existing)
├── storage:...                   Controlled storage values (existing)
├── ...                          Other existing registry branches
└── id                           Instance identifier branch (proposed)
    ├── nersc                    Illustrative issuing authority
    │   ├── facility:<local-id>
    │   ├── site:<local-id>
    │   ├── resource:<local-id>
    │   ├── job:<local-id>
    │   └── ...                  Other object kinds from Section 3
    ├── alcf
    │   └── resource:<local-id>
    └── olcf
        └── resource:<local-id>
```

| Segment | Meaning | Proposed example |
| --- | --- | --- |
| `urn:doe-iri` | Shared DOE-IRI URN namespace | `urn:doe-iri` |
| `id` | Administrative branch for instance identity | `id` |
| `authority` | Permanently reserved issuing-facility code | `nersc` |
| `kind` | Stable API object family | `resource` |
| `local-id` | Opaque key unique within that authority and kind | `r-001` |

For example:

```text
urn:doe-iri:id:nersc:facility:facility-001
urn:doe-iri:id:nersc:site:site-001
urn:doe-iri:id:nersc:resource:r-001
urn:doe-iri:id:alcf:resource:r-001
urn:doe-iri:id:olcf:job:j-84027
```

The two `resource:r-001` values identify different objects because their
authorities differ. The authority denotes the original issuance namespace,
not necessarily current ownership, physical location, or API hosting.

This hierarchy expresses allocation of names, not physical containment or
subtype inheritance. Prefixes such as `urn:doe-iri:id:nersc` are administrative
prefixes, not object IDs. The Facility representation has its own full
`facility:<local-id>` identifier. Its mutable display name or `short_name`
MUST NOT determine namespace identity.

## 3. Object Kinds and Scope

The following proposed tokens map to existing API model families. They do not
create new Resource Types or representations.

| Proposed kind | Existing model |
| --- | --- |
| `facility` | `Facility` |
| `site` | `Site` |
| `resource` | `Resource` |
| `capability` | `Capability` |
| `incident` | `Incident` |
| `event` | `Event` |
| `project` | `Project` |
| `project-allocation` | `ProjectAllocation` |
| `user-allocation` | `UserAllocation` |
| `job` | `Job` |
| `task` | `Task` |

Adoption applies to these models' `id` properties and fields explicitly
defined as references to those IDs. It MUST preserve existing requiredness,
nullability, and cardinality except where a separately reviewed structural
change is approved. It is not a blanket conversion of every property whose
name ends in `_id`.

Native scheduler identifiers, authentication subjects, usernames, protocol
identifiers, endpoint-local IDs, and local keys inside `attributes` are outside
this proposal. In particular, backend-specific scheduler IDs in
`JobStatus.meta_data` remain distinct from `Job.id`; there is no standardized
`Job.scheduler_id` field. The current contract has user references but no
`User` representation, so `Project.user_ids` and `UserAllocation.user_id` are
also outside this proposal. Any ambiguous existing reference must have its
target and identifier role resolved in the adoption change before its
representation is changed.

All compute, storage, network, and service Resource instances use kind
`resource`; `resource_type` continues to carry classification. A change in
classification MUST NOT change the instance identifier. Kind tokens are
permanent once assigned and do not track schema renames or API versions.
Future kinds require governed registration, not arbitrary facility additions.

## 4. Syntax and Equality

The proposed syntax uses the ABNF conventions of
[RFC 5234](https://www.rfc-editor.org/rfc/rfc5234):

```abnf
INSTANCE-URN = "urn:doe-iri:" %x69.64 ":" AUTHORITY ":" KIND ":" LOCAL-ID
AUTHORITY    = LOWER-ALNUM *(LOWER-ALNUM / "-")
KIND         = LOWER-ALNUM *(LOWER-ALNUM / "-")
LOCAL-ID     = LOWER-ALNUM *(LOWER-ALNUM / "-" / "." / "_" / "~")
LOWER-ALNUM  = %x61-7A / DIGIT
DIGIT        = %x30-39
```

The quoted scheme and namespace identifier are case-insensitive under ABNF;
`%x69.64` denotes the exact lowercase `id` marker. Producers MUST emit the
entire identifier in the canonical lowercase form. Only reserved authority
codes and registered object-kind tokens are assignable; `ext` is not an
assignable authority or kind in this branch.

The local key is one nonempty ASCII segment. Colons, slashes, whitespace,
percent escapes, query/resolution components, and fragments are not permitted
in an instance `id`. Additional site, system, API-version, or resource-type
segments MUST NOT be inserted into the hierarchy. A facility MAY encode an
internal issuer discriminator in its opaque local key, but clients MUST NOT
interpret its punctuation or substrings as a portable structure.

For accepted instance IDs, equality follows the assigned-name rules in
[RFC 8141, Section 3](https://www.rfc-editor.org/rfc/rfc8141#section-3): normalize
the scheme and NID to lowercase, then compare the complete strings. No other
case folding or suffix transformation is defined. Two canonical IDs are equal
only when their complete strings are equal. General URN components excluded
by this field's grammar are invalid field values, not additional identities.

Consumers MUST NOT use type-style prefix fallback to establish identity, drop
the authority, or compare only local keys. A legacy UUID and a URN containing
that UUID are different identifiers; any association is an explicit migration
mapping, not URN equivalence.

## 5. Issuance and Persistence

1. **Central governance:** IRI reserves permanent authority codes and records
   explicit instance-issuance delegations for `urn:doe-iri:id:<authority>:`.
   Reuse the existing authority-code reservation identity where appropriate,
   with a separate issuance record identifying the responsible facility,
   change controller, scope, status, and reference. An extension reservation
   or `ext` scope does not grant this right. Authority codes MUST NOT be reused
   for another organization; organizational succession requires a recorded
   continuity decision.
2. **Local issuance:** An authorized facility assigns local keys without
   registering individual objects centrally. It MUST maintain uniqueness for
   each `(authority, kind, local-id)` across all of its issuing systems and
   over time. Multiple schedulers, services, and API deployments sharing a
   facility code therefore require coordinated allocation or a collision-safe
   key strategy.
3. **Permanent identity:** An assigned ID MUST remain stable through renaming,
   reclassification, site relocation, API relocation, and ordinary updates
   to the same object. Deleted IDs MUST NOT be reassigned. A replacement
   object receives a new ID even if it inherits the old object's name or URL.
   Namespace retirement stops new issuance but does not invalidate old IDs.
4. **Native key reuse:** A raw scheduler job number is insufficient when it can
   repeat across schedulers or after counter reset. Facilities MUST distinguish
   such occurrences, for example with a persisted random key or an issuer and
   issuance-epoch discriminator encoded in the opaque local key. The binding
   MUST survive restarts and restoration of the service's state.
5. **Transfer and replication:** A mirror representing the same object preserves
   its ID. Administrative transfer preserves the original issuance namespace;
   current location and ownership are represented separately. Facilities MUST
   document stewardship continuity if the original issuer retires. A copy
   with an independent lifecycle receives a new ID.

An existing UUID can be retained as the local key:

```text
Existing id: 550e8400-e29b-41d4-a716-446655440000
Proposed id: urn:doe-iri:id:nersc:resource:550e8400-e29b-41d4-a716-446655440000
```

This is a low-disruption allocation strategy, not a mandate to retain UUID
generation. A mnemonic key can also be used if it is permanently reserved:
changing a display name never changes the key. Keys SHOULD avoid personal or
sensitive information because identifiers can appear in logs and shared data.

## 6. Identity, Classification, and Retrieval

### 6.1. Full Identifier Binding

An adopting API MUST preserve the binding between an object's `id` and an
operation parameter that identifies that object. For example, in
`GET /api/v2/status/resources/{resource_id}`, the logical value of
`resource_id` is the complete `Resource.id`, including the entire URN. A
client MUST NOT extract only `local-id` for substitution, and a server MUST
NOT discard the authority or kind when determining identity. An internal
database may use a local key after validating the complete identifier and its
scope; that implementation choice does not change the API parameter value.

The current [Resource retrieval operation](../specification-v2/openapi/production/status.yaml)
already declares `resource_id` as a required string path parameter. A URN can
be carried in that parameter without changing the path template. This rule
also applies to other parameters defined as instance-ID references. Operations
requiring both Resource and Job identifiers retain both parameters and their
existing context and authorization checks.

For example:

```text
Resource.id: urn:doe-iri:id:nersc:resource:r-001
resource_id: urn:doe-iri:id:nersc:resource:r-001

GET /api/v2/status/resources/urn%3Adoe-iri%3Aid%3Anersc%3Aresource%3Ar-001
```

### 6.2. Path Serialization

The percent escapes above are HTTP path serialization, not part of the
identifier stored in `Resource.id`. After transport decoding, the server's
parameter value is `urn:doe-iri:id:nersc:resource:r-001`.

[OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html#parameter-object)
defaults path parameters to `simple` style, corresponding to
[RFC 6570 simple expansion](https://www.rfc-editor.org/rfc/rfc6570#section-3.2.2).
Clients MUST serialize the full ID as one parameter value under the operation's
serialization rules. Simple expansion percent-encodes the colons as `%3A`.
Pass the unencoded ID to an SDK that performs this serialization; pre-encoding
it would risk producing `%253A` through double encoding. Servers MUST accept
the serialized form and recover the ID through a single transport-decoding
step across the request pipeline. Application code MUST NOT decode an already
decoded framework parameter again.

Literal colons are also legal within this HTTP path segment under
[RFC 3986, Section 3.3](https://www.rfc-editor.org/rfc/rfc3986#section-3.3), so
the following is syntactically a valid HTTP request target:

```text
/api/v2/status/resources/urn:doe-iri:id:nersc:resource:r-001
```

An implementation MAY additionally accept this literal-colon spelling, but
clients use the operation's specified serialization. The enclosing URL remains
an HTTP URL; the embedded `urn:` text is path data, not a second URL scheme.
The proposed ID grammar excludes `/`, `?`, and `#`, so IDs do not introduce
additional path segments, queries, or fragments.

Deployments must verify their SDKs, proxies, routers, and application lookup
logic together. Any implementation-specific UUID route converter or UUID-only
validator needs updating even though the current OpenAPI parameter is a
string. This RFC does not assert that every existing deployment already
accepts URNs.

### 6.3. Representation and Navigable Links

This illustrative Resource uses existing fields and a proposed instance ID:

```json
{
  "id": "urn:doe-iri:id:nersc:resource:r-001",
  "name": "Example compute system",
  "last_modified": "2026-09-26T12:00:00Z",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "self_uri": "https://api.example.org/api/v2/status/resources/urn%3Adoe-iri%3Aid%3Anersc%3Aresource%3Ar-001",
  "site_uri": "https://api.example.org/api/v2/facility/sites/urn%3Adoe-iri%3Aid%3Anersc%3Asite%3Asite-001",
  "capability_uris": [],
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/urn%3Adoe-iri%3Aid%3Anersc%3Aresource%3Ar-001"
    }
  }
}
```

The `id` identifies the object; `resource_type` classifies it; `self_uri` and
`_links.self.href` locate its representation. Clients can follow an advertised
URL directly or invoke an OpenAPI operation by substituting the complete ID
into its defined template. They MUST NOT derive the API host or path template
by interpreting authority, kind, or local-key segments. In particular, a
facility code is not a hostname and an object-kind token is not an API path.
The [HAL RFC](rfc-hal-links.md) continues to govern link conventions and
legacy URI-property coexistence.

An instance URN MUST NOT replace a complete navigable HTTP `href`, `self_uri`,
`site_uri`, or other retrieval/operation URI merely because it is a URI.
Embedding an encoded URN as a parameter in an HTTP URL preserves that
distinction. No global URN resolution service or automatic mapping from an
arbitrary URN to an API base URL is defined.

## 7. Compatibility and Migration

Introducing a new naming convention is structurally possible with the current
string schemas, but replacing an existing `id` changes client-visible
identity. Clients may use IDs as database keys, cache keys, bookmarks, foreign
keys, or workflow references. Requiring this grammar also narrows the accepted
strings. Adoption MUST therefore publish an explicit compatibility and
versioning plan; it MUST NOT be presented as a transparent UUID-format fix.

The recommended rollout is:

1. **Approve the namespace:** Revise the governing namespace rules and register
   the branch, kinds, and facility issuance scopes. Until then, examples in
   this document do not authorize production issuance.
2. **Prepare clients and mappings:** Remove undocumented UUID assumptions from
   clients and storage. Inventory identity references and allocate one stable
   URN per existing object. Persist mappings scoped by issuing facility,
   object kind, and any legacy deployment namespace needed to disambiguate
   previously local IDs. Do not infer cross-facility identity from matching
   UUID suffixes.
3. **Introduce an explicit adoption contract:** Publish the affected field and
   parameter schemas, examples, and deployment OpenAPI description. For an
   existing service, use a new API major version unless an approved negotiated
   representation contract provides equivalent isolation for legacy clients.
   Each contract returns one consistent canonical `id` for an object. Keep
   legacy representations stable during their supported compatibility period.
4. **Preserve reference continuity:** Update identity-valued references and
   ID-bound path parameters together with canonical IDs. The adopting contract
   MUST accept the full URN wherever the corresponding object ID is expected;
   accepting only its local suffix is insufficient. Preserve existing retrieval
   URLs as documented compatibility aliases where practical. Any supported
   legacy-ID lookup aliases MUST use the persisted mapping and be documented
   per operation; aliases do not change the canonical full-ID binding. Historical
   records can retain their original IDs with a durable mapping to the same
   object. No new alias property, relation, or lookup endpoint is defined here.
5. **Retire compatibility deliberately:** Publish support dates and verify
   dependent clients before retiring legacy responses or lookup aliases.
   Preserve issuance records and historical mappings so old identifiers
   cannot be assigned to different objects.

Newly created objects do not need a bare UUID alias unless a supported legacy
contract requires one. The adoption work should verify full-ID path substitution
and percent-encoding round trips through the deployment's request pipeline,
cross-facility local-key collisions, recycled scheduler IDs, ID/URI reference
distinctions, historical mappings, and legacy-client behavior. A request using
another authority's URN with the same local key MUST NOT accidentally resolve
to a local object by suffix alone.

## 8. Required Specification and Registry Changes

Adoption requires coordinated, separately reviewable changes:

- **Governing URN specification:** Add a distinct instance-URN production and
  administrative `id` branch. Scope semantic hierarchy and prefix matching to
  type/value URNs. Revise the blanket `ext`-only delegation wording to recognize
  governed instance issuance while retaining `ext` for semantic extensions.
  Explicitly define that instance prefixes are not semantic extension parents.
- **URN registry:** Record the new branch, permanent kind tokens, and explicit
  authority issuance delegations. The registry remains the assignment
  authority; individual instance IDs remain under facility management.
- **OpenAPI and reference implementations:** Adopt the ID contract for the
  selected models and identity references, including request parameters and
  stored relationships. Audit native and local ID roles individually. Preserve
  navigable URL contracts and existing v2 representation distinctions.
- **Profiles and documentation:** Update examples and identifier guidance after
  adoption, without changing Resource Type URNs or profile identities.

The repository's governing URN RFC treats formal IANA namespace registration
as future work. This proposal does not assert that `doe-iri` has an IANA
registration and does not create one; that remains a separate governance task.

## 9. Alternatives and Decisions for Review

| Alternative | Assessment |
| --- | --- |
| Bare UUID | Retains existing identity, but supplies no explicit issuing-facility namespace. |
| `urn:uuid:<uuid>` | Provides a URN form, but does not add facility-specific issuance scope. |
| `urn:doe-iri:facility:<authority>:<kind>:<local-id>` | Viable if adopted explicitly, but `id` names the branch's purpose more directly and avoids confusing a namespace prefix with a Facility instance. |
| `urn:doe-iri:resource:<type>:<authority>:<local-id>` | Mixes instance identity with the existing type taxonomy and makes classification changes affect identity. |
| `urn:doe-iri:ext:<authority>:id:<kind>:<local-id>` | Would still need explicit scope authorization and new instance semantics; makes a shared API identity convention appear to be a facility-specific semantic extension. |

The recommended decision is the `id:<authority>:<kind>:<local-id>` hierarchy
with a flat opaque local key. Review should confirm the adoption version,
initial model coverage, participating authority delegations, and duration of
legacy compatibility. A portable resolution service or independently
delegated sub-issuer segment would require a separate proposal supported by
concrete use cases.

## 10. Security Considerations

An authority segment is a name, not proof that the named facility issued the
object. Implementations MUST authenticate the source and authorize access
independently of the URN. They MUST NOT infer access rights from a facility
prefix or use that prefix alone to choose a trusted network endpoint.

Identifiers are untrusted strings at API boundaries. Validate syntax, use
parameterized storage lookups, and enforce object-level authorization for both
canonical IDs and legacy aliases. Predictable keys are permitted, so secrecy
of an identifier cannot be an access-control mechanism. Facility prefixes can
disclose affiliation; local keys should not expose usernames or other personal
information.

## 11. References

The following standards and IRI source materials informed this proposal.
Repository sources were reviewed at the baseline commit identified in
**Status of This Memo**.

### 11.1. External Standards

- [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119).
  Defines the requirement keywords used in this RFC.
- [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174).
  Clarifies when those requirement keywords have their defined meanings.
- [RFC 8141: Uniform Resource Names (URNs)](https://www.rfc-editor.org/rfc/rfc8141).
  Defines URN syntax, persistent naming, and assigned-name equivalence,
  particularly Section 3.
- [RFC 3986: Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986).
  Defines URI components, percent encoding, and path-segment syntax,
  particularly Sections 2.1, 2.4, and 3.3.
- [RFC 5234: Augmented BNF for Syntax Specifications: ABNF](https://www.rfc-editor.org/rfc/rfc5234).
  Defines the notation used for the proposed identifier grammar.
- [RFC 6570: URI Template](https://www.rfc-editor.org/rfc/rfc6570).
  Defines template expansion and percent encoding, particularly simple string
  expansion in Section 3.2.2.
- [OpenAPI Specification, Version 3.1.0](https://spec.openapis.org/oas/v3.1.0.html).
  Defines path parameters and their serialization, particularly the Parameter
  Object and its default `simple` path style.

### 11.2. IRI Specifications, Registries, and API Sources

- [A URN Namespace for the DoE IRI Project](rfc-iri-urn-structure-and-registry.md).
  Governs existing DOE-IRI namespace syntax, hierarchy, matching, extension
  delegation, and registration; provides the baseline for the changes
  proposed here.
- [DOE-IRI URN Registry](../registry/urns/README.md).
  Records existing namespace branches, authority-code reservations, and
  scope delegations.
- [Resource Type URNs](../registry/urns/resource-types.md).
  Supplies the registered resource classifications kept distinct from
  instance identity, including the compute-system type used in the example.
- [HAL Links for the IRI Facility API](rfc-hal-links.md).
  Defines navigable link conventions and coexistence with legacy URI-valued
  properties.
- [IRI v2 OpenAPI component schemas](../specification-v2/openapi/production/_components.yaml).
  Supplies the current object models, identifier fields, reference fields,
  and structural constraints reviewed for migration.
- IRI v2 OpenAPI operation definitions:
  [Facility](../specification-v2/openapi/production/facility.yaml),
  [Status](../specification-v2/openapi/production/status.yaml),
  [Account](../specification-v2/openapi/production/account.yaml),
  [Compute](../specification-v2/openapi/production/compute.yaml),
  [Task](../specification-v2/openapi/production/task.yaml),
  [Storage](../specification-v2/openapi/production/storage.yaml), and
  [Filesystem](../specification-v2/openapi/production/filesystem.yaml).
  Supply the existing path and query parameter contracts, including Resource
  retrieval and operations requiring both Resource and Job identifiers.
- [Facility representation profile](../registry/profiles/facility.md).
  Distinguishes stable Facility identity from display names and short names.
- [Job representation profile](../registry/profiles/compute/job.md).
  Describes Job identity, backend-specific scheduler metadata, and
  Resource-scoped operation context.
- [Task representation profile](../registry/profiles/task.md).
  Describes Task identity and the existing opaque-identifier contract.
- [Inference Service Resource Definition Profile](../registry/profiles/resource-definition/service/inference.md).
  Defines service-local model identifiers, illustrating local keys excluded
  from this instance-ID migration.
