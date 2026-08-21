# IRI RFC Instructions

These rules apply under `rfc/`.

## 1. RFC Role

RFCs define governing semantic or protocol rules. They should not duplicate
registry tables merely to become a second assignment authority.

Use the correct source for each concern:

- OpenAPI for structural API contract;
- governing URN RFC for namespace/registration rules;
- URN registry for assigned identifiers;
- relation registry for assigned `iri:*` relation names and semantics;
- representation profiles for representation-specific semantics.

## 2. Normative Language

Use BCP 14 keywords only for genuinely normative requirements.

A standalone RFC using uppercase normative keywords SHOULD include the standard
RFC 2119/RFC 8174 interpretation statement unless inherited unambiguously.

Avoid converting descriptive rationale into unnecessary MUST/SHOULD language.

## 3. Registry References

Use current canonical identifiers and link to the authoritative registry rather
than copying large registries into the RFC.

If an informational appendix lists current registrations, label it
informational and state that the registry remains authoritative.

Do not invent a Resource Type, controlled URN, relation, or profile solely for
an RFC example.

## 4. IRI v2 Resource Scope

IRI v2 uses the existing `Resource` representation.

Resource Definition Profiles specialize it according to `resource_type`.

Do not introduce a required separate Resource Definition / Resource State
architecture in v2.

Preserve current status/history semantics where they are part of the existing
API.

## 5. HAL RFC Rules

For HAL material:

- relations answer WHY;
- `href` answers WHERE;
- `type` answers HOW represented;
- `profile` answers WHAT target semantic contract applies.

The relation registry is authoritative for `iri:*` relation semantics.

`service-desc` targets a service description such as OpenAPI and should not be
given an unrelated IRI representation profile.

Operation-affordance relations such as `iri:submit-job` target operation entry
points; do not use a Job representation profile on the operation link.

`TaskSubmitResponse.task_uri` maps to standard `monitor`; the retrieved Task
representation exposes `self`.

## 6. Examples

Examples should be compact and registry-consistent.

Validate:

- JSON/YAML syntax;
- Resource Type URNs;
- controlled values;
- relation names;
- target profile URIs;
- legacy URI ↔ HAL target equality when both appear.

Do not expand a small RFC edit into a full registry migration unless required
by the approved task.

## 7. Decision Records

`docs/decisions/` may explain why an RFC choice was made but is non-normative.

If a decision record conflicts with the current RFC, update or supersede the
decision record; do not weaken RFC authority by treating the decision record as
an equal source.
