# RFC: Generic Queue Attributes for IRI Resources

## Abstract
This document defines an extension to the Integrated Research Infrastructure (IRI) API for representing queue information as optional type-specific members within the `attributes` object of a `Resource`, rather than as a first-class `Resource` of its own. The extension is scheduler-agnostic and standardizes queue semantics that matter to users and tooling: what work can be submitted through a queue associated with a resource, what work can run from it, queue-specific constraints and limits, subject-scoped limits, queue operational state, and queue load represented as queued eligible work in node-hours.

Queues are optional. A resource MAY expose queue-related members within `attributes` when queue semantics are relevant to the service offered by that resource, and a resource MAY omit those members entirely when no queue applies.

The proposal is additive and is intended to remain compatible with existing IRI API resource representations. It aligns with the current IRI API `Resource` model and OpenAPI structure.

## Status of This Memo
- **Status:** Draft for review
- **Author:** Paul Rich and OpenAI ChatGPT-5
- **Version:** v0.3
- **Intended Status:** Informational RFC / API extension proposal
- **Review Status:** Frozen baseline

| Revision | Author | Date | Notes |
| :---- | :---- | :---- | :---- |
| 0.1 | Paul Rich, OpenAI ChatGPT-5 | Aug 14, 2026 | Initial draft introducing queue resources for the IRI API, including queue state, submission/run semantics, limits, load metrics, and scheduler mapping appendices. |
| 0.2 | Paul Rich, OpenAI ChatGPT-5 | Aug 24, 2026 | Revised draft changing queues from first-class resources to optional resource attributes usable on any resource type. |
| 0.3 | Paul Rich, OpenAI ChatGPT-5 | Sep 2, 2026 | Aligned queue attributes with Resource Definition Profiles and registry-governed URN candidates, clarified HAL coexistence, and expanded `route_targets` to identify target resource, queue, and optional priority. |

## 1. Introduction
The IRI API already models facility resources through a common `Resource` abstraction with typed endpoints and status exposure. In practice, many resources expose queue semantics that are not well captured today.

In this document, "Queue" refers to the general method and construct of queuing work for later admission, routing, dispatch, or execution. It does not refer exclusively to any specific workload-management, scheduling, or workload-distribution system's native object named "queue".

Queue semantics are key to facility policy implementation, routing user jobs to resources, enforcing site policies, QoS, and limits on jobs, and enabling efficient resource use in line with a given site's requirements and metrics.

For the purposes of this RFC, **job** refers to a submitted or managed unit of workload as represented by the implementation’s scheduler, resource manager, or equivalent execution-control system. **Work** refers to a normalized aggregate quantity of demand represented by one or more jobs, such as queued or running work expressed in `node_hours`. These terms are used here for interoperability and may not correspond exactly to the local terminology used by every site or workload-management system.

Users and automated clients often need answers to questions such as:

- Which resources expose queues that can accept work for submission?
- Which queue-bearing resources are accepting work but cannot currently dispatch jobs?
- What job-level constraints does a queue associated with a resource enforce, and for which subject classes?
- What limits apply to a user, group, project, account, or the queue as a whole?
- How heavily loaded is the queue right now?
- What, if any, QoS behavior is associated with a queue? This includes preemption and backfilling policies.

Representing queue information as structured resource attributes allows IRI clients to discover, filter, authorize, and present queue semantics using the same patterns already used for other type-specific resource metadata. This approach also reflects that a queue is not independent of a resource: a queue is always associated with some resource context, and some resources may have no queue at all.

### 1.1 Requirements Language
The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119  RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## 2. Scope

### 2.1 In Scope
This document defines:

1. scheduler-agnostic queue semantics for use as resource attributes,
2. normalized queue state and submission semantics,
3. normalized per-job constraints and aggregate subject limits,
4. queue load reporting based on queued eligible work in node-hours,
5. additive API and schema changes required to expose optional queue information on resources,
6. resource-discovery and representation patterns for resources that expose queue-related attributes.

### 2.2 Out of Scope
This document does not:

- Standardize scheduler policy settings for IRI-connected sites
- Require exact semantic parity across schedulers
- Redefine the IRI job submission API
- Prescribe a single scheduler-specific implementation strategy
- Require every resource to expose queue information
- Define an interface for modifying queues via IRI

## 3. Design Goals
This document aims to:

1. Represent queues as optional type-specific members within the `attributes` object of resources in the IRI API.
2. Remain scheduler-agnostic across scheduler and workload-manager implementations.
3. Allow queue information to be attached to any resource type when relevant, not only compute resources.
4. Distinguish submission eligibility, admission constraints, and run eligibility.
5. Expose common queue constraints and limits in a normalized, scheduler-agnostic form.
6. Express queue-scoped limits for subjects such as user, group, project, account, and overall/global usage.
7. Expose queue state using at least two dimensions: whether the queue is accepting new work and whether work can run from it.
8. Provide a queue load metric based on queued eligible work, expressed in `node_hours`.
9. Preserve room for site-specific, scheduler-specific, and resource-specific capability expression without forcing scheduler-native schema leakage into the core object.

## 4. Proposed Resource Model

### 4.1 Queue Information within `attributes`
This document defines queue information as optional type-specific metadata carried directly within the `attributes` object on an IRI `Resource`.

The semantic meaning of these queue-related members is selected by the exact `resource_type` of the enclosing `Resource`, consistent with the current IRI Resource Definition Profile model.

This RFC is intended to define a queue-related attribute contract for use by applicable Resource Definition Profiles, rather than a standalone schema detached from profile selection.

A resource SHOULD expose queue information when queue semantics are relevant to the service offered by that resource. A resource MAY omit those queue-related members entirely when no queue applies.

Queue information is not limited to compute resources. Any resource type MAY expose queue-related members in `attributes` when the resource has queue semantics that matter to users or automated clients.

When a queue spans or coordinates more than one underlying resource, an implementation MAY model that situation by exposing a higher-level resource representing the combined service context and carrying queue-related members in that resource's `attributes` object.

New queue-specific classifications introduced by this RFC SHOULD be represented as URNs carried in string-valued fields rather than as new OpenAPI enums.

### 4.2 Queue Attribute Shape
The following additive attribute set defines queue-specific metadata. It SHOULD be carried directly within `attributes` on any `Resource` for which queue information is applicable, consistent with the current IRI API `Resource.attributes` model.

This RFC defines queue-related attribute semantics, but it does not replace the common `Resource` schema or the general rules for `attributes`. The governing OpenAPI contract remains authoritative for the wire-level structure.

Illustrative shape:

```yaml
Resource:
  type: object
  properties:
    attributes:
      anyOf:
        - type: object
          additionalProperties: true
          properties:
            schema_version:
              type: string
            queue_name:
              type: string
            queue_class:
              type: string
            submission_mode:
              type: string
            accepting_submissions:
              type: boolean
            dispatching_enabled:
              type: boolean
            default_submission_target:
              type: boolean
            qos:
              type: string
            admission_constraints:
              $ref: '#/components/schemas/QueueAdmissionConstraints'
            effective_run_constraints:
              $ref: '#/components/schemas/QueueRunConstraints'
            execution_target_url:
              type: string
            subject_limits:
              type: array
              items:
                $ref: '#/components/schemas/QueueSubjectLimit'
            load:
              $ref: '#/components/schemas/QueueLoad'
            route_targets:
              type: array
              items:
                $ref: '#/components/schemas/QueueRouteTarget'
            raw_scheduler_attributes:
              type: object
              additionalProperties: true
        - type: 'null'
```

The queue-specific members defined by this RFC are:

```yaml
schema_version:
  type: string
  description: Version of the queue-specific attribute contract defined by the applicable Resource Definition Profile.
  example: 1.0.0

queue_name:
  type: string
  description: User-facing queue name used when selecting or referring to the queue within the resource context.

queue_class:
  type: string
  description: Queue-class URN identifying the normalized queue class.
  example: urn:doe-iri:queue-class:execution

submission_mode:
  type: string
  description: |
    Queue-submission-mode URN describing how work can enter the queue.
    `urn:doe-iri:queue-submission-mode:routed-only` means the queue can receive work only via another queue or scheduler path.
  example: urn:doe-iri:queue-submission-mode:direct

accepting_submissions:
  type: boolean
  description: Whether the queue is currently accepting new work through its allowed submission path.

dispatching_enabled:
  type: boolean
  description: Whether work is currently eligible to start running from this queue, subject to normal resource availability and policy.

default_submission_target:
  type: boolean
  description: Whether this queue is a default submission target for the site or scheduler context.

qos:
  type: string
  description: Queue-QoS URN identifying the expected quality-of-service behavior for jobs in the queue. If omitted, consumers SHOULD treat the queue as `urn:doe-iri:queue-qos:default`.
  example: urn:doe-iri:queue-qos:preemptable

admission_constraints:
  $ref: '#/components/schemas/QueueAdmissionConstraints'

effective_run_constraints:
  $ref: '#/components/schemas/QueueRunConstraints'

execution_target_url:
  type: string
  description: Resource URL identifying the execution target to which work from this queue may execute or otherwise be realized in the implementation's service model. This field is the normative execution-target field for this RFC. A future profile or registered link-relation mapping may add link-backed navigation without silently changing this field's semantics.

subject_limits:
  type: array
  items:
    $ref: '#/components/schemas/QueueSubjectLimit'

load:
  $ref: '#/components/schemas/QueueLoad'

route_targets:
  type: array
  items:
    $ref: '#/components/schemas/QueueRouteTarget'
  description: Ordered or prioritized routing targets when routing applies. Each target identifies both the target resource and the target queue identifier on that resource. If routing priority is meaningful for the implementation, the target entry should include `routing_priority`.

raw_scheduler_attributes:
  type: object
  additionalProperties: true
  description: Implementation-defined raw scheduler attributes, when exposed.
```

This RFC does not, by itself, make `attributes.schema_version` mandatory for every Resource with non-null `attributes`. However, when queue-specific data is present, producers SHOULD include `attributes.schema_version` to identify the version of the queue-specific attribute contract in use. A Resource Definition Profile that normatively incorporates this queue contract SHOULD declare `attributes.schema_version` mandatory whenever queue-specific data is present; producers conforming to such a profile MUST then provide it.

Queue-specific members defined by this RFC MUST NOT redefine or override common top-level Resource properties such as `id`, `last_modified`, `current_status`, `resource_type`, `self_uri`, `site_uri`, or `capability_uris`.

When no queue-specific data is being reported, a producer SHOULD omit those queue-related members. As with the underlying IRI API `Resource` schema, `attributes` itself MAY be absent or `null` when permitted by the governing OpenAPI contract.

### 4.3 Proposed New URNs
This section records URNs proposed by this RFC for queue representation. They are proposal candidates for DOE-IRI registry review, rather than an RFC-local vocabulary or already-authoritative registry entries.

The DOE-IRI URN registry is authoritative for category structure, canonical parentage, lifecycle status, and any approved canonical values. Accordingly, the URNs listed here are proposal candidates for registry review and are not authoritative unless and until they are registered through the current DOE-IRI governance process.

This RFC uses concrete candidate URN strings to make the queue attribute contract reviewable. Registry review determines the final canonical spellings, parent branches, and category placement.

#### 4.3.1 Queue Class URNs
The following are candidate URNs for normalized queue-class values, subject to DOE-IRI registry approval and final branch placement.

- `urn:doe-iri:queue-class:execution` — normalized execution queue class.
- `urn:doe-iri:queue-class:routing` — normalized routing queue class.
- `urn:doe-iri:queue-class:hybrid` — normalized queue class for queues that combine routing and execution behavior.

#### 4.3.2 Queue Submission Mode URNs
This RFC defines a baseline set of candidate well-known queue submission-mode URNs. Sites MAY use more specific descendant URNs where needed, consistent with broader IRI URN governance and cross-site registration practices.

- `urn:doe-iri:queue-submission-mode:direct` — end users can submit directly to the queue.
- `urn:doe-iri:queue-submission-mode:routed-only` — work can enter only through another queue or scheduler-controlled routing path.
- `urn:doe-iri:queue-submission-mode:none` — the queue is not a valid submission target.

#### 4.3.3 Queue Subject Type URNs
The following are candidate URNs for normalized subject-type values used in queue limits and constraints.

- `urn:doe-iri:queue-subject-type:user` — limit applies to a user identity.
- `urn:doe-iri:queue-subject-type:group` — limit applies to a group identity.
- `urn:doe-iri:queue-subject-type:project` — limit applies to a project identity.
- `urn:doe-iri:queue-subject-type:account` — limit applies to an account identity.
- `urn:doe-iri:queue-subject-type:overall` — limit applies queue-wide rather than to a named identity.

#### 4.3.4 Queue Subject Scope URNs
The following are candidate URNs for normalized subject-scope values used in queue limits.

- `urn:doe-iri:queue-subject-scope:generic` — limit applies generically to all subjects of a class.
- `urn:doe-iri:queue-subject-scope:named` — limit applies to a specific named subject.

#### 4.3.5 Queue Limit Kind URNs
The following are candidate URNs for normalized queue limit kinds.

- `urn:doe-iri:queue-limit-kind:max-queued-jobs` — hard or soft cap on queued job count.
- `urn:doe-iri:queue-limit-kind:max-running-jobs` — hard or soft cap on running job count.
- `urn:doe-iri:queue-limit-kind:max-queued-work` — cap on queued work in the declared unit.
- `urn:doe-iri:queue-limit-kind:max-running-work` — cap on running work in the declared unit.
- `urn:doe-iri:queue-limit-kind:soft-max-running-jobs` — scheduler-reported soft preference/cap for running job count.
- `urn:doe-iri:queue-limit-kind:soft-max-running-work` — scheduler-reported soft preference/cap for running work.

#### 4.3.6 Queue Applies-To URNs
The following are candidate URNs for normalized queue applicability values.

- `urn:doe-iri:queue-applies-to:queued` — rule applies to queued work only.
- `urn:doe-iri:queue-applies-to:running` — rule applies to running work only.
- `urn:doe-iri:queue-applies-to:queued-or-running` — rule applies across queued and running work.

#### 4.3.7 Queue Enforcement URNs
The following are candidate URNs for normalized queue enforcement values.

- `urn:doe-iri:queue-enforcement:hard` — limit is enforced as a hard boundary.
- `urn:doe-iri:queue-enforcement:soft` — limit is advisory, preferential, or soft-enforced.

#### 4.3.8 Queue QoS URNs
This RFC defines a baseline set of candidate well-known queue QoS URNs. These URNs describe normalized site-policy expectations associated with a queue, not scheduler-native configuration primitives. Sites MAY use more specific descendant URNs where needed, consistent with broader IRI URN governance and cross-site registration practices.

- `urn:doe-iri:queue-qos:default` — no special QoS behavior is expected.
- `urn:doe-iri:queue-qos:preemptable` — jobs in this queue may be preempted.
- `urn:doe-iri:queue-qos:demand` — jobs in this queue are associated with a site policy intended to minimize startup delay and that may allow them to preempt other jobs.
- `urn:doe-iri:queue-qos:backfill` — jobs in this queue are considered for backfilling and typically have lower relative priority under site policy than other jobs on the system.
- `urn:doe-iri:queue-qos:high-priority` — jobs in this queue are intended for high-priority execution.
- `urn:doe-iri:queue-qos:reservation` — jobs in this queue are associated with advance reservation behavior.

These URNs are carried in string-valued properties. This RFC does not require adding new OpenAPI enums for them.

## 5. Normative Semantics

### 5.1 Queue as Resource Attribute Data
A queue exposed by the IRI API SHALL be represented as queue-specific members carried within a `Resource` object's `attributes` field.

The exact semantics of those members SHALL be determined by the applicable Resource Definition Profile, if any, selected by the Resource's exact `resource_type`.

This RFC defines a queue-related attribute contract that applicable Resource Definition Profiles MAY incorporate. It does not create a separate standalone queue representation independent of the current `Resource` model.

A queue SHALL NOT be treated by this RFC as a first-class standalone `Resource` independent of some resource context.

A resource that exposes queue information SHOULD be stable enough to support bookmarking, inventory, and policy inspection over time.

### 5.2 Submission and Run Semantics
Queue state SHALL expose both of the following dimensions:

- `accepting_submissions`: whether new work can currently be accepted into the queue through the queue's valid submission path.
- `dispatching_enabled`: whether work can currently start running from the queue.

These dimensions are intentionally independent.

### 5.3 Submission Mode
`submission_mode` communicates how work can enter the queue. The field carries a queue-submission-mode URN.

In this RFC, the well-known baseline values are:

- `urn:doe-iri:queue-submission-mode:direct` — end users can submit directly.
- `urn:doe-iri:queue-submission-mode:routed-only` — work can enter only via another queue or scheduler-controlled routing path.
- `urn:doe-iri:queue-submission-mode:none` — the queue is not a valid submission target.

Sites MAY define more specific descendant URNs when needed. This RFC defines only a baseline set of well-known submission-mode URNs and does not require an explicit catch-all value.

### 5.4 Constraints, Limits, Execution Targets, and QoS
This document distinguishes:

- **admission constraints**: per-job properties that determine whether work can enter or be routed into the queue,
- **effective run constraints**: properties that affect whether work from that queue can run,
- **execution target**: the resource onto which work from the queue may execute or otherwise be realized,
- **subject limits**: aggregate caps on queued/running work by user/group/project/account/global scope,
- **QoS expectation**: the normalized expected quality-of-service behavior associated with the queue.

This separation is necessary because a queue can admit work under one path and dispatch it under another, and because schedulers expose both per-job admissibility rules and aggregate fairness/enforcement limits.

A resource that exposes queue information in `attributes` SHALL include `execution_target_url` as part of that same queue-bearing resource description. That field SHALL contain exactly one resource URL identifying the execution target to which work from the queue may be dispatched or otherwise realized.

If routing behavior is relevant to the queue-bearing resource description, `route_targets` MAY identify downstream queues used for routing. This RFC does not require `route_targets` for non-routing queues. Each route target SHALL identify the target resource URL and the target queue identifier. If the target queue is on a different resource from the queue-bearing resource or from `execution_target_url`, the target resource URL SHALL identify that other resource explicitly. When routing priority or preference is meaningful for the implementation, the route target SHOULD include `routing_priority`; lower numeric values indicate higher preference unless the applicable profile documents a different convention.

HAL `_links` are outside the queue attribute contract unless an applicable Resource Definition Profile or registered link-relation definition says otherwise. Implementations MAY additionally advertise registered links for related resources. When URI-valued queue navigation fields and advertised links are intended to describe the same relationship, they SHOULD remain semantically consistent and MUST NOT communicate conflicting targets or meanings. This RFC does not register queue-specific link relations; therefore, for v0.3, `execution_target_url` and `route_targets` remain the normative queue-navigation fields defined by this RFC.

If a queue exposes `qos`, the value SHALL be a queue-QoS URN. If `qos` is omitted, consumers SHOULD interpret the queue as having `urn:doe-iri:queue-qos:default`.

Every submitted job that uses queue semantics SHALL be associated with exactly one queue, either explicitly selected by the client or implicitly assigned by the implementation's default-queue policy.

## 6. Queue Constraints, Limits, Load, and Routing

### 6.1 Admission Constraints
Admission constraints capture normalized per-job bounds checked when a job is considered for entry into a queue.

```yaml
QueueAdmissionConstraints:
  type: array
  items:
    $ref: '#/components/schemas/QueueConstraint'
```

```yaml
QueueConstraint:
  type: object
  required:
    - constraint_id
    - units
    - applies_to
  properties:
    constraint_id:
      type: string
      description: Site-provided scheduler constraint identifier, such as walltime, node_count, process_count, or memory_bytes.
    minimum_value:
      type: number
      nullable: true
      description: Minimum permitted value for the constraint, when applicable.
    maximum_value:
      type: number
      nullable: true
      description: Maximum permitted value for the constraint, when applicable.
    units:
      type: string
      description: Units for the constraint value, such as seconds, nodes, processes, or bytes.
    applies_to:
      type: string
      description: Queue-subject-type URN identifying the subject class to which this constraint applies.
      example: urn:doe-iri:queue-subject-type:overall
```

Semantics:

- Each constraint entry identifies a queue admission constraint by `constraint_id`.
- `constraint_id` uses a site-provided scheduler value. This RFC does not require a globally standardized constraint identifier vocabulary.
- At least one of `minimum_value` or `maximum_value` SHALL be present in each constraint entry.
- Multiple constraint entries MAY use the same `constraint_id` when they apply to different classes or site-defined cases.
- `applies_to` identifies the subject class to which the constraint applies by queue-subject-type URN.
- Constraint precedence and conflict resolution are scheduler-specific and need not be represented by this interface.

### 6.2 Effective Run Constraints
Some queue characteristics affect execution rather than direct admission.

```yaml
QueueRunConstraints:
  type: object
  properties:
    run_windows:
      type: array
      items:
        $ref: '#/components/schemas/QueueRunWindow'
      description: Time windows during which jobs in the queue are permitted to run.
```

This RFC defines only a minimal normalized structure for effective run constraints; implementations MAY convey additional execution-related detail through documented profile semantics or `raw_scheduler_attributes`.

### 6.3 Subject Limits
Queue-scoped aggregate limits SHALL be represented in a scheduler-agnostic array of subject-specific rules.

```yaml
QueueSubjectLimit:
  type: object
  required:
    - subject_type
    - scope
    - limit_kind
  properties:
    subject_type:
      type: string
      description: Queue-subject-type URN identifying the class of subject to which the rule applies.
      example: urn:doe-iri:queue-subject-type:user

    subject_id:
      type: string
      nullable: true
      description: |
        Identifier of the subject when the limit applies to a named entity.
        Null when the rule applies generically to all subjects of that type or to `urn:doe-iri:queue-subject-type:overall`.

    scope:
      type: string
      description: Queue-subject-scope URN describing whether the rule is generic or named.
      example: urn:doe-iri:queue-subject-scope:generic

    limit_kind:
      type: string
      description: Queue-limit-kind URN describing the kind of limit.
      example: urn:doe-iri:queue-limit-kind:max-running-jobs

    value:
      type: number
      description: Numeric limit value.

    unit:
      type: string
      description: Unit string for the numeric limit value.
      example: node_hours

    applies_to:
      type: string
      description: Queue-applies-to URN describing whether the rule applies to queued, running, or combined work.
      example: urn:doe-iri:queue-applies-to:running

    enforcement:
      type: string
      description: Queue-enforcement URN describing whether the limit is hard or soft.
      example: urn:doe-iri:queue-enforcement:hard
```

Notes:

- `urn:doe-iri:queue-subject-type:project` covers sites that expose project semantics directly.
- `urn:doe-iri:queue-subject-type:account` covers systems where the scheduler-native concept is account rather than project. Sites MAY normalize an internal account concept to `urn:doe-iri:queue-subject-type:project` when that is the facility's user-facing model.
- `urn:doe-iri:queue-subject-type:overall` represents queue-wide/global limits not tied to a specific identity class.

### 6.4 Queue Load
Queue load is intended to provide a coarse indication of how much work is ahead of a newly submitted job.

Queue load SHALL be represented as a numerical value in `node_hours` of queued eligible work.

```yaml
QueueLoad:
  type: object
  properties:
    node_hours:
      type: number
      description: Total node-hours of queued eligible work included in queue load.
    measured_at:
      type: string
      format: date-time
```

Queue load SHOULD include only jobs that are queued and eligible to run.

Jobs in an ineligible-to-run state SHOULD NOT be included unless they are part of a dependency chain of jobs.

Running jobs SHALL NOT be included.

This metric is intended only as a coarse comparison signal for users and agents.

### 6.5 Route Targets
Route targets describe where work may be routed after entering a routing queue or a queue-bearing resource with routing behavior.

```yaml
QueueRouteTarget:
  type: object
  required:
    - target_resource_url
    - target_queue_identifier
  properties:
    target_resource_url:
      type: string
      description: Resource URL identifying the resource that contains, represents, or otherwise owns the downstream target queue.
    target_queue_identifier:
      type: string
      description: Queue identifier on the target resource. This may be the user-facing queue name, scheduler queue name, partition name, routing class, or another profile-defined queue identifier.
    routing_priority:
      type: integer
      nullable: true
      description: Optional implementation-reported routing priority or preference. Lower numeric values indicate higher preference unless the applicable profile documents a different convention.
    description:
      type: string
      nullable: true
      description: Optional human-readable description of the route target.
```

Each route target SHALL identify both the resource and the queue identifier to which work can be routed. Implementations MUST NOT require consumers to infer the target resource from the target queue identifier alone.

## 7. API Behavior

### 7.1 Additive Changes
This document is backward-compatible because it only:

- introduces new optional queue-specific fields under `attributes`,
- allows resources to expose queue information when applicable,
- relies on the existing IRI API `attributes` object-or-null wire contract.

Existing clients that ignore unknown `resource_type` values or unknown object properties remain functional.

### 7.2 Discovery
Clients that want queue awareness SHOULD:

- inspect queue-specific members within `attributes` on returned resources,
- prefer the normalized queue fields over parsing `raw_scheduler_attributes`,
- treat absent optional fields as unknown rather than false.

Sites MAY expose queue-bearing resources under existing resource endpoints and MAY add queue-aware filtering parameters where useful.

### 7.3 Queue Information Endpoints
Implementations SHOULD expose queue information through existing resource endpoints.

#### 7.3.1 Reuse Existing Resource Endpoints
A conforming implementation MAY expose queue-bearing resources through the existing resource endpoints, including:

- `GET /api/v2/status/resources`
- `GET /api/v2/status/resources/{resource_id}`
- resource-type-specific collection endpoints when applicable

When queue-bearing resources are exposed through these endpoints, clients inspect queue-specific members within `attributes` for queue metadata.

#### 7.3.2 Queue Information Query Parameters
If queue-bearing resources are exposed in shared collection endpoints, implementations MAY support additive query parameters such as:

- `queue_class=<queue-class-urn>`
- `accepting_submissions=true|false`
- `dispatching_enabled=true|false`
- `default_submission_target=true|false`
- `has_queue=true|false`

Implementations MAY also support filtering by site, capability, scheduler family, resource type, or queue name, provided those filters are documented clearly.

#### 7.3.3 Queue Discovery Requirements
If an implementation exposes queue information, it SHOULD provide at least one stable collection endpoint from which authorized clients can enumerate queue-bearing resources.

## 8. Producer Requirements
Producers exposing queue information:

1. SHALL represent queue information as queue-specific members within `attributes`.
2. SHALL interpret and document those members according to the applicable Resource Definition Profile for the Resource's `resource_type`.
3. SHALL expose `accepting_submissions` and `dispatching_enabled` independently.
4. SHALL represent queue limits using normalized admission constraints and subject-limit structures where the underlying scheduler data can be normalized faithfully.
5. SHOULD expose queue load as `node_hours` of eligible queued work.
6. MAY expose raw scheduler attributes for fidelity, provided doing so does not violate local security or disclosure policy.
7. SHOULD document implementation-specific mapping choices when the native scheduler model does not map cleanly to the normalized queue model.
8. SHALL expose `execution_target_url` with exactly one resource URL for each queue description.
9. MAY expose `route_targets` when routing behavior is part of the queue description and SHOULD omit it when no routing targets are relevant. Each route target SHALL identify the target resource and target queue identifier, and SHOULD include `routing_priority` when priority or preference is meaningful for the implementation.
10. SHOULD expose queue information through at least one stable collection endpoint.
11. MAY omit queue-specific members from `attributes` entirely for resources to which no queue applies.
12. SHOULD include `attributes.schema_version` when publishing queue-specific data under this queue attribute contract. A profile that normatively incorporates this queue contract SHOULD require it whenever queue-specific data is present; producers conforming to such a profile MUST then provide it.
13. MUST NOT use queue-specific members in `attributes` to override common top-level Resource properties.

## 9. Consumer Requirements
Consumers processing queue-bearing resources:

1. SHOULD treat queue information as additive and optional.
2. SHOULD interpret queue-specific members in the context of the applicable Resource Definition Profile for the exact `resource_type` when that profile is known.
3. MAY treat unfamiliar queue-specific members as opaque JSON data.
4. SHOULD prefer normalized queue fields over scheduler-native raw attributes.
5. SHOULD treat absent optional fields as unknown rather than false or zero.
6. MUST NOT infer direct-submission capability solely from queue health or visibility.
7. SHOULD be prepared for queue semantics to differ slightly across implementations, especially when normalized from different schedulers.
8. MUST NOT infer a complete queue attribute contract solely from hierarchical similarity between resource types.
9. SHOULD treat `execution_target_url` and `route_targets`, when present, as the authoritative queue-navigation fields defined by this RFC. If a later applicable profile or registered link-relation mapping defines stricter link-backed navigation, consumers SHOULD follow that profile or relation definition without inferring an implicit replacement from unrelated HAL links.

## 10. Backward Compatibility and Versioning
This extension is additive. Existing IRI API producers and consumers remain valid if they ignore unknown properties.

No existing resource schema is removed or semantically redefined by this document.

## 11. Security Considerations
Queue policy can reveal operational and organizational information. Implementations SHOULD consider the following:

1. **Per-principal visibility.** A site MAY suppress queues that the caller is not authorized to view or submit to.
2. **Subject-limit sensitivity.** Named limits for specific users, groups, projects, or accounts MAY expose internal policy and SHOULD be filtered according to authorization policy.
3. **Load sensitivity.** Queue load metrics can reveal usage intensity and campaign timing. Sites MAY coarsen or omit these values for unauthorized callers.
4. **Raw attribute leakage.** `raw_scheduler_attributes` SHOULD be filtered to avoid leaking scheduler internals, filesystem paths, hook names, or admin-only policy details.
5. **Consistency with submission authorization.** If a queue is visible but not usable by the caller, the implementation SHOULD avoid implying authorization merely because `accepting_submissions=true` at the resource level.

The RECOMMENDED practice is that implementations SHOULD expose both queue-global semantics and, when supported, caller-effective semantics. If both are exposed, they SHOULD be clearly distinguished in the schema or documentation.

## 12. References
- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels," RFC 2119, March 1997.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words," RFC 8174, May 2017.
- [RFC3986] Berners-Lee, T., Fielding, R., and L. Masinter, "Uniform Resource Identifier (URI): Generic Syntax," RFC 3986, January 2005.
- [RFC8141] Saint-Andre, P. and J. Klensin, "Uniform Resource Names (URNs)," RFC 8141, April 2017.
- [OPENAPI] OpenAPI Initiative, "OpenAPI Specification," current published version at https://spec.openapis.org/oas/latest.html.

## 13. Rationale

### 13.1 Why model queues as attributes on resources instead of as resources themselves?
Because queues are not independent of resource context. A queue is always associated with some resource or service context, and queue semantics may apply to more than just compute resources. Modeling queue information as optional type-specific members within `attributes` preserves that relationship while fitting the current Resource Definition Profile approach used by the IRI API.

### 13.2 Why separate `accepting_submissions` from `dispatching_enabled`?
Schedulers commonly distinguish these concepts. Clients need both signals.

### 13.3 Why include both `submission_mode` and `accepting_submissions`?
A queue can be healthy and accepting jobs through its valid path while still disallowing direct user submission. `submission_mode` answers how work can enter; `accepting_submissions` answers whether that path is open.

### 13.4 Why prefer node-hours over queued job count?
Job count alone poorly represents queue pressure. Ten short one-node jobs and ten week-long 512-node jobs are operationally very different. Node-hours provide a more useful coarse indicator of how much work is ahead in the queue.

## 14. Open Questions
1. Should IRI standardize separate fields for caller-effective submission eligibility, distinct from global queue state?
2. Should a future extension allow a single resource representation to expose multiple distinct queue descriptions when a site presents materially different queue paths within the same service context?
3. Is `node_hours` sufficient as the preferred metric, or should `core_hours` be elevated to equal standing for CPU-centric systems?

## Appendix A. OpenAPI Sketch (Informative)
The following minimal changes would be required in the OpenAPI model for profiles that choose to incorporate this RFC's queue-related attribute contract:

1. Define queue-specific members that may appear within `attributes` for applicable resources.
2. Add supporting schemas for queue-related arrays and objects such as `QueueAdmissionConstraints`, `QueueConstraint`, `QueueRunConstraints`, `QueueRunWindow`, `QueueSubjectLimit`, `QueueLoad`, and `QueueRouteTarget`.
3. Optionally document query/filter behavior for queue-bearing resources on existing resource endpoints.

As in the main body, this sketch is illustrative of one way to express the queue contract in OpenAPI. The governing OpenAPI specification and the applicable Resource Definition Profile remain authoritative for the wire-level structure and type-specific semantics.

Illustrative patch:

```yaml
Resource:
  properties:
    attributes:
      anyOf:
        - type: object
          additionalProperties: true
          description: Optional type-specific resource metadata.
          properties:
            schema_version:
              type: string
            queue_name:
              type: string
            queue_class:
              type: string
            submission_mode:
              type: string
            accepting_submissions:
              type: boolean
            dispatching_enabled:
              type: boolean
            default_submission_target:
              type: boolean
            qos:
              type: string
            admission_constraints:
              $ref: '#/components/schemas/QueueAdmissionConstraints'
            effective_run_constraints:
              $ref: '#/components/schemas/QueueRunConstraints'
            execution_target_url:
              type: string
            subject_limits:
              type: array
              items:
                $ref: '#/components/schemas/QueueSubjectLimit'
            load:
              $ref: '#/components/schemas/QueueLoad'
            route_targets:
              type: array
              items:
                $ref: '#/components/schemas/QueueRouteTarget'
            raw_scheduler_attributes:
              type: object
              additionalProperties: true
        - type: 'null'
```

When queue semantics are present, `attributes.schema_version` SHOULD identify the version of the queue-specific attribute contract in use. Profiles that normatively adopt this queue contract SHOULD require it whenever queue-specific data is present; producers conforming to such a profile MUST then provide it.

When queue semantics are present, `attributes.qos` MAY include a queue-QoS URN. If omitted, consumers SHOULD treat the queue as `urn:doe-iri:queue-qos:default`.

When queue semantics are present, `attributes.execution_target_url` SHALL identify exactly one resource URL.

HAL `_links` are outside the queue attribute contract unless an applicable profile or registered link-relation definition says otherwise. If an implementation also advertises queue-related navigation through HAL `_links`, any corresponding URI-valued queue navigation fields and advertised links SHOULD remain semantically consistent and MUST NOT communicate conflicting targets or meanings.

Queue-specific members defined by this RFC MUST NOT override common top-level `Resource` properties.

Illustrative queue-aware query parameters on existing endpoints:

```yaml
parameters:
  - in: query
    name: has_queue
    schema:
      type: boolean
  - in: query
    name: queue_class
    schema:
      type: string
      description: Queue-class URN.
      example: urn:doe-iri:queue-class:execution
  - in: query
    name: accepting_submissions
    schema:
      type: boolean
  - in: query
    name: dispatching_enabled
    schema:
      type: boolean
```

Suggested helper schemas:

```yaml
QueueRunWindow:
  type: object
  properties:
    type:
      type: string
      description: URN or implementation-defined string indicating the type of run window.
      example: reservation
    start:
      type: string
      format: date-time
      description: Inclusive ISO 8601 timestamp marking the start of the run window.
    end:
      type: string
      format: date-time
      description: Exclusive ISO 8601 timestamp marking the end of the run window.
    reservation_start:
      type: string
      format: date-time
      description: ISO 8601 timestamp marking the start of an associated reservation, when applicable.
    reservation_end:
      type: string
      format: date-time
      description: ISO 8601 timestamp marking the end of an associated reservation, when applicable.
    queue_active_time:
      type: string
      format: date-time
      description: ISO 8601 timestamp when the queue becomes active for the described window, when applicable.
    queue_disable_time:
      type: string
      format: date-time
      description: ISO 8601 timestamp when the queue becomes disabled for the described window, when applicable.

```

## Appendix B. Implementation Notes (Informative)

### B.1 Deriving Load in Node-Hours
Queue load SHOULD be computed as:

`sum(requested_node_count * requested_walltime_hours)` over queued jobs that are eligible to run

Queued jobs in an ineligible-to-run state SHOULD NOT be included unless they are part of a dependency chain of jobs.

Running jobs are not part of queue load and SHOULD NOT be included.

### B.2 Walltime and Run-Window Normalization
Implementations SHOULD normalize scheduler-native durations into integer seconds in the API representation, while optionally retaining the native form in `raw_scheduler_attributes`.

When queue runnability is constrained by advance reservations or other scheduled time windows, implementations SHOULD represent those windows using ISO 8601 timestamps in `effective_run_constraints.run_windows`.

Where available, implementations MAY distinguish reservation timing from queue activation timing by using `reservation_start` / `reservation_end` and `queue_active_time` / `queue_disable_time`.

### B.3 Queue Limits with Mixed Provenance
At some sites, effective queue behavior is determined by a combination of scheduler config, fairshare/QoS rules, and site policy overlays. Implementations MAY publish the effective, user-visible result even when it is assembled from multiple sources, provided the semantics remain truthful.

### B.4 Default Queues and Submission Guidance
If a site has a default queue or recommended submission path, `default_submission_target` SHOULD indicate that preference. This is especially useful when clients may omit an explicit queue selection and the implementation will then assign the default queue. It is also useful when execution queues use `urn:doe-iri:queue-submission-mode:routed-only` and the correct user action is to submit to an upstream routing queue instead.

## Appendix C. Scheduler Mapping Notes (Informative)
This appendix is informative and non-normative. It provides implementation-oriented mapping suggestions for common schedulers and should not be read as defining the core semantics of the queue attribute model.

### C.1 PBS Professional Mapping Notes
Possible PBS-oriented mappings include:

- `enabled` -> `accepting_submissions`
- `started` -> `dispatching_enabled`
- execution queue restricted to routed input -> `submission_mode = urn:doe-iri:queue-submission-mode:routed-only`
- execution queue -> `queue_class = urn:doe-iri:queue-class:execution`
- routing queue -> `queue_class = urn:doe-iri:queue-class:routing`
- `resources_min.walltime` / `resources_max.walltime` -> `admission_constraints` entry with `constraint_id=walltime`, units `seconds`, and the corresponding minimum/maximum value
- `resources_min.nodect` / `resources_max.nodect` -> `admission_constraints` entry with `constraint_id=node_count`, units `nodes`, and the corresponding minimum/maximum values
- queue job-count and resource limits -> `subject_limits`

A routed-only execution queue can still dispatch jobs while disallowing direct submission. Its admission constraints remain authoritative for work entering through a routing path.

Routing queues MAY be represented through queue-specific members within `attributes` on a resource that serves as the routing context. When exposed, downstream targets MAY be listed in `route_targets`, with each entry identifying the target resource, target queue identifier, and optional routing priority.

### C.2 SLURM Mapping Notes
Possible SLURM-oriented mappings include:

- partition -> queue information attached to a relevant resource
- partition availability -> `accepting_submissions`
- partition dispatchability -> `dispatching_enabled`
- partition used primarily for direct execution -> `queue_class = urn:doe-iri:queue-class:execution`
- `MaxTime` -> `admission_constraints` entry with `constraint_id=walltime`, units `seconds`, and a maximum value
- `MinNodes` / `MaxNodes` -> `admission_constraints` entries with `constraint_id=node_count`, units `nodes`, and the corresponding minimum/maximum values
- TRES limits or QoS/account limits -> `subject_limits` or implementation-defined extensions

In practice, SLURM partitions are often the closest native construct to the queue semantics described in this RFC.

A site MAY expose multiple logical queue descriptions for a single partition when submission and run policy differ materially by QoS, account, or other policy overlays, provided those descriptions remain attached to an appropriate resource context.

### C.3 Grounding Notes
The scheduler-oriented notes in this appendix are informed by PBS Professional documentation available in `resources/pbspro-pdfs/` and by the general SLURM partition/accounting model. They are illustrative guidance, not normative requirements.

## Appendix D. Example Payloads (Informative)
These examples retain the queue navigation fields defined by this RFC. Some examples also include ordinary Resource HAL links, such as `self` and `iri:located-at`, to illustrate coexistence with the HAL migration model. Those ordinary links are not part of the queue attribute contract. When a deployment also advertises queue-specific navigation through future registered HAL link relations, the URI-valued queue navigation fields and the advertised links should remain semantically consistent.


### D.1 Resource with a Generic Execution Queue
```json
{
  "id": "perlmutter-service",
  "name": "Perlmutter Service",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "supported_endpoints": ["compute"],
  "self_uri": "https://api.example.org/api/v2/status/resources/perlmutter-service",
  "site_uri": "https://api.example.org/api/v2/facility/sites/site-a",
  "capability_uris": [],
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/perlmutter-service"
    },
    "iri:located-at": {
      "href": "https://api.example.org/api/v2/facility/sites/site-a"
    }
  },
  "last_modified": "2026-08-12T18:00:00Z",
  "current_status": "up",
  "attributes": {
    "schema_version": "1.0.0",
    "queue_name": "general",
    "queue_class": "urn:doe-iri:queue-class:execution",
    "submission_mode": "urn:doe-iri:queue-submission-mode:direct",
    "accepting_submissions": true,
    "dispatching_enabled": true,
    "qos": "urn:doe-iri:queue-qos:default",
    "execution_target_url": "https://api.example.org/api/v2/status/resources/perlmutter-cpu",
    "admission_constraints": [
      {
        "constraint_id": "walltime",
        "minimum_value": 0,
        "maximum_value": 17940,
        "units": "seconds",
        "applies_to": "urn:doe-iri:queue-subject-type:overall"
      },
      {
        "constraint_id": "node_count",
        "minimum_value": 1,
        "maximum_value": 32,
        "units": "nodes",
        "applies_to": "urn:doe-iri:queue-subject-type:overall"
      }
    ],
    "subject_limits": [
      {
        "subject_type": "urn:doe-iri:queue-subject-type:overall",
        "subject_id": null,
        "scope": "urn:doe-iri:queue-subject-scope:generic",
        "limit_kind": "urn:doe-iri:queue-limit-kind:max-running-jobs",
        "value": 500,
        "unit": "jobs",
        "applies_to": "urn:doe-iri:queue-applies-to:running",
        "enforcement": "urn:doe-iri:queue-enforcement:hard"
      }
    ],
    "load": {
      "node_hours": 9142.5,
      "measured_at": "2026-08-12T18:00:00Z"
    }
  }
}
```

### D.2 Resource with a Routed-Only Execution Queue
```json
{
  "id": "perlmutter-large-service",
  "name": "Perlmutter Large Service",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "supported_endpoints": ["compute"],
  "self_uri": "https://api.example.org/api/v2/status/resources/perlmutter-large-service",
  "site_uri": "https://api.example.org/api/v2/facility/sites/site-a",
  "capability_uris": [],
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/perlmutter-large-service"
    },
    "iri:located-at": {
      "href": "https://api.example.org/api/v2/facility/sites/site-a"
    }
  },
  "last_modified": "2026-08-12T18:00:00Z",
  "current_status": "up",
  "attributes": {
    "schema_version": "1.0.0",
    "queue_name": "long",
    "queue_class": "urn:doe-iri:queue-class:execution",
    "submission_mode": "urn:doe-iri:queue-submission-mode:routed-only",
    "accepting_submissions": true,
    "dispatching_enabled": true,
    "qos": "urn:doe-iri:queue-qos:preemptable",
    "execution_target_url": "https://api.example.org/api/v2/status/resources/perlmutter-large",
    "admission_constraints": [
      {
        "constraint_id": "walltime",
        "minimum_value": 18000,
        "maximum_value": null,
        "units": "seconds",
        "applies_to": "urn:doe-iri:queue-subject-type:project"
      },
      {
        "constraint_id": "node_count",
        "minimum_value": 1,
        "maximum_value": 128,
        "units": "nodes",
        "applies_to": "urn:doe-iri:queue-subject-type:overall"
      }
    ],
    "effective_run_constraints": {},
    "load": {
      "node_hours": 18240,
      "measured_at": "2026-08-12T18:00:00Z"
    }
  }
}
```

### D.3 Resource with a Routing Queue
```json
{
  "id": "perlmutter-routing-service",
  "name": "Perlmutter Routing Service",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "supported_endpoints": ["compute"],
  "self_uri": "https://api.example.org/api/v2/status/resources/perlmutter-routing-service",
  "site_uri": "https://api.example.org/api/v2/facility/sites/site-a",
  "capability_uris": [],
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/perlmutter-routing-service"
    },
    "iri:located-at": {
      "href": "https://api.example.org/api/v2/facility/sites/site-a"
    }
  },
  "last_modified": "2026-08-12T18:00:00Z",
  "current_status": "up",
  "attributes": {
    "schema_version": "1.0.0",
    "queue_name": "route",
    "queue_class": "urn:doe-iri:queue-class:routing",
    "submission_mode": "urn:doe-iri:queue-submission-mode:direct",
    "accepting_submissions": true,
    "dispatching_enabled": false,
    "qos": "urn:doe-iri:queue-qos:backfill",
    "execution_target_url": "https://api.example.org/api/v2/status/resources/perlmutter-routing-aggregate",
    "route_targets": [
      {
        "target_resource_url": "https://api.example.org/api/v2/status/resources/perlmutter-short-service",
        "target_queue_identifier": "short",
        "routing_priority": 10,
        "description": "Preferred short-walltime execution queue"
      },
      {
        "target_resource_url": "https://api.example.org/api/v2/status/resources/perlmutter-long-service",
        "target_queue_identifier": "long",
        "routing_priority": 20,
        "description": "Fallback longer-walltime execution queue"
      }
    ],
    "admission_constraints": [],
    "effective_run_constraints": {},
    "load": {
      "node_hours": 210.5,
      "measured_at": "2026-08-12T18:00:00Z"
    }
  }
}
```
