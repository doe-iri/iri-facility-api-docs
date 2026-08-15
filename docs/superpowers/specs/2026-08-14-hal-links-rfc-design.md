# HAL Links RFC Simplification Design

## Status

Approved design for simplifying `rfc/rfc-hal-links.md` and registering the
link relations needed to migrate existing URI-valued OpenAPI properties into
HAL `_links`.

Date: 2026-08-14

## 1. Objective

Replace the current broad HAL draft with a concise RFC about one concern:
representing navigable relationships and one representative operation
affordance in HAL `_links` on existing IRI API representations.

The RFC must not introduce, name, or depend on a `ResourceDefinition` /
`ResourceState` split. The current OpenAPI `Resource` representation remains
unchanged by this work.

## 2. Semantic Boundary

The revised RFC uses this model:

```text
resource_type identifies what a Resource is.
ordinary properties describe the representation.
_links identifies related representations and applicable operation entry points.
OpenAPI defines how an operation is invoked.
```

The DOE-IRI URN Registry is authoritative for resource-type and
controlled-value URNs. The DOE-IRI Link Profile Index and its linked profiles
are authoritative for `iri:*` relation names and semantics. Link relations are
not DOE-IRI URNs, and the RFC must not create a second relation registry.

## 3. Scope

In scope:

- the HAL `_links` representation;
- migration of existing URI-valued OpenAPI properties into link relations;
- standard versus DOE-IRI relation selection;
- the reusable OpenAPI 3.1 HAL schema components;
- singular and plural link cardinality;
- one representative operation relation, `iri:submit-job`;
- concise compatibility, authorization, consumer, and producer rules;
- compact, registry-consistent JSON examples;
- a short agentic and RAG justification;
- an illustrative HAL CURIE example.

Out of scope:

- changing the production OpenAPI v1 or v2 schemas;
- separating resource definition from operational state;
- state, capacity, health, or metrics models;
- a generic relationship-resource framework;
- a complete operation or topology ontology;
- job lifecycle relations other than the `submitJob` illustration;
- filesystem operation relations;
- assigning a canonical DOE-IRI CURIE expansion URI.

## 4. Agentic and RAG Rationale

The RFC retains one concise justification. HAL links let clients and agents
traverse advertised relationships and operation entry points without guessing
facility-specific paths. RAG systems may index relation names and linked
resource context to improve discovery, but an agent must consult the current
representation and governing OpenAPI contract before invoking an operation.
Indexed links are not proof of current authorization, availability,
applicability, or permission.

The RFC must not connect this rationale to a resource-definition/resource-state
architecture.

## 5. Standard Relations

Use standard Web Linking relations where their established semantics fit:

| Existing property | Relation | Rule |
|---|---|---|
| Any `self_uri` | `self` | Identifies the canonical URI of the current representation. |
| `Facility.support_uri` | `help` | Identifies the facility help or support portal. |
| `TaskSubmitResponse.task_uri` | `monitor` | Identifies the Task resource used to monitor asynchronous progress or result. |

`self` is required only for a HAL representation with its own canonical
identity. A transient `TaskSubmitResponse` does not require `self`; it uses
`monitor` for the resulting Task.

These standard relations are not added to the DOE-IRI Link Profile Index as
IRI-specific relations.

## 6. DOE-IRI URI-Migration Relations

Register the following relations with lifecycle status `provisional`:

| Relation | Source | Target | Semantic cardinality | Target classification | Stability / volatility |
|---|---|---|---|---|---|
| `iri:generated-by` | `Event` | `Incident` | `0..1` | API resource | Stable association once set. |
| `iri:has-event` | `Incident` | `Event` | `0..*` | API resource | Membership may grow as events are recorded. |
| `iri:impacts` | `Event` | DOE-IRI `Resource` | Exactly `1` under the current `resource_uri` contract | Resource | Stable for an immutable Event. |
| `iri:may-impact` | `Incident` | DOE-IRI `Resource` | `0..*` | Resource | May change as incident scope is assessed. |
| `iri:has-resource` | `Site` | DOE-IRI `Resource` | `0..*` | Resource | Relatively stable site topology. |
| `iri:has-site` | `Facility` | `Site` | `0..*` | API resource | Relatively stable facility topology. |
| `iri:has-project` | `ProjectAllocation` | `Project` | Exactly `1` under the current `project_uri` contract | API resource | Stable accounting association. |
| `iri:has-capability` | `Resource` or `ProjectAllocation` | `Capability` | Resource: `0..*`; ProjectAllocation: exactly `1` | API resource | Relatively stable association. |
| `iri:has-project-allocation` | `UserAllocation` | `ProjectAllocation` | Exactly `1` | API resource | Stable accounting hierarchy. |

The relation profiles must include exact source and target representations,
cardinality, target classification, static/dynamic behavior, authorization and
visibility rules, omission semantics, and a HAL example.

### 6.1. Source-sensitive mappings

URI property names are not sufficient to determine relation meaning:

```text
Event.resource_uri       -> iri:impacts
Incident.resource_uris   -> iri:may-impact
Site.resource_uris       -> iri:has-resource
```

A required but nullable `Event.incident_uri` maps to `iri:generated-by` with
`0..1` cardinality. A null URI produces no relation; HAL never contains
`"href": null`.

`iri:has-capability` has one general meaning: it identifies a Capability
associated with the source. On a Resource, the Capability is provided by that
Resource. On a ProjectAllocation, it is the Capability to which the allocation
applies.

## 7. Existing Registered Relations in Examples

The RFC examples must use the existing profiles without changing their
semantics. Suitable examples include:

- `iri:located-at`;
- `iri:provides-filesystem`;
- `iri:has-mount`;
- `iri:mounted-on`;
- `iri:has-node`;
- `iri:has-cpu`;
- `iri:has-gpu`;
- `iri:hosted-on`;
- `iri:accesses-mount`.

Examples must use exact registered resource types. In particular, scratch is a
storage-tier controlled value, not a filesystem resource subtype.

## 8. Operation Affordance

Register `iri:submit-job` with lifecycle status `provisional`:

| Field | Definition |
|---|---|
| Source | `urn:doe-iri:resource:compute:system` |
| Target | Resource-specific job-submission operation entry point |
| Current OpenAPI operation | `POST /api/v2/compute/job/{resource_id}`, `operationId: launchJob` |
| Cardinality | `0..1` |
| Target classification | Operation entry point |
| Target stability | Applicable configured affordance, not a live capacity assertion |
| Authorization | Visibility may be filtered |

The link identifies where job submission is defined for the source compute
system. It does not itself specify the HTTP method or request body, grant
permission, guarantee schedulability, or replace the OpenAPI `JobSpec`,
response, error, and security contracts.

Other compute lifecycle operations and all filesystem operation relations are
deferred. The RFC must not invent generic compute-API or filesystem-API
relations.

## 9. HAL CURIEs

The RFC retains the HAL CURIE concept. It uses this explicitly illustrative,
non-normative example:

```json
"curies": [
  {
    "name": "iri",
    "href": "https://example.org/iri/rels/{rel}",
    "templated": true
  }
]
```

The RFC must state that the `example.org` URI must not be copied into an
implementation. A deployed CURIE template must be stable and expand to
documentation for the corresponding registered relation. CURIE expansion does
not assign or redefine a relation; the DOE-IRI Link Profile Index remains
authoritative. This work does not establish a canonical DOE-IRI expansion URI.

## 10. OpenAPI 3.1 Schema

The RFC includes one reusable schema definition:

```yaml
HalLink:
  type: object
  required:
    - href
  properties:
    href:
      type: string
      format: uri-reference
    templated:
      type: boolean
      default: false
    type:
      type: string
    deprecation:
      type: string
      format: uri
    name:
      type: string
    profile:
      type: string
      format: uri
    title:
      type: string
    hreflang:
      type: string
  additionalProperties: true

HalLinkValue:
  oneOf:
    - $ref: '#/components/schemas/HalLink'
    - type: array
      items:
        $ref: '#/components/schemas/HalLink'

HalLinks:
  type: object
  additionalProperties:
    $ref: '#/components/schemas/HalLinkValue'
```

An existing representation adopts the components with:

```yaml
_links:
  $ref: '#/components/schemas/HalLinks'
  readOnly: true
```

The generic schema allows a singular link or an array. Each relation profile
remains authoritative for semantic cardinality. The schema permits `curies` as
an array of `HalLink` objects.

## 11. Compatibility

This work documents an additive migration and does not modify current OpenAPI
conformance:

1. Existing URI properties remain authoritative with their current
   required/nullability rules until a later OpenAPI revision.
2. Producers may add the corresponding HAL relation during the transition.
3. When both forms are present, their targets must agree.
4. A scalar URI equals the migrated link's `href`.
5. A URI array and link array identify the same targets, disregarding order.
6. A null or absent optional URI maps to an omitted relation, never a null
   `href`.
7. Consumers should prefer `_links` and may fall back to legacy URI fields.
8. Removing URI properties requires a subsequent OpenAPI change.
9. The existing `site_uri` / `iri:located-at` compatibility contract remains
   unchanged.

For exact-one relations backed by currently required fields, exact-one is the
semantic cardinality after the relation is supplied or becomes the replacement
contract. `_links` itself remains optional during the additive transition.

## 12. Examples

Keep examples compact:

1. A storage-system Resource using exact registered URNs, `self`,
   `iri:located-at`, and `iri:provides-filesystem`.
2. An Event or Incident showing legacy URI properties alongside equivalent
   registered links.
3. A compute-system Resource showing `iri:submit-job`, followed by a
   `TaskSubmitResponse` using `monitor`.

Examples must not use unregistered state, capacity, operation, inverse,
relationship, or resource-type values.

## 13. Files

Modify:

- `rfc/rfc-hal-links.md`
- `registry/link-profile-root.md`

Create:

- `registry/link-profile-generated-by.md`
- `registry/link-profile-has-event.md`
- `registry/link-profile-impacts.md`
- `registry/link-profile-may-impact.md`
- `registry/link-profile-has-resource.md`
- `registry/link-profile-has-site.md`
- `registry/link-profile-has-project.md`
- `registry/link-profile-has-capability.md`
- `registry/link-profile-has-project-allocation.md`
- `registry/link-profile-submit-job.md`

Do not modify production OpenAPI files, URN registry files,
`docs/ai-project-context.md`, or unrelated link profiles.

## 14. Validation

Validation must confirm:

- no `ResourceDefinition`, `ResourceState`, or companion separation-RFC text
  remains in `rfc/rfc-hal-links.md`;
- all `iri:*` relations used by the RFC are present in the authoritative link
  index;
- all resource-type and controlled-value URNs used by examples are registered;
- JSON and YAML examples parse;
- the ten new profiles and index agree on lifecycle, source, target,
  cardinality, and target classification;
- legacy scalar/array mappings match the RFC table;
- the CURIE URI is clearly illustrative and non-normative;
- no production OpenAPI file changes;
- all relative Markdown links resolve;
- `git diff --check` passes.
