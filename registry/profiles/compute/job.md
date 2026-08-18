# IRI Compute Job Profile

**Profile URI:** `https://iri.science/profiles/compute/job`  
**OpenAPI type:** `Job`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Compute Job representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/compute/job
```

An IRI Job represents a compute job submitted to a compute Resource through the IRI Compute API.

A Job provides identity and execution-state information for submitted work and MAY include the Job Specification associated with that work.

A Job is distinct from:

- a compute Resource, which represents the compute system on which jobs may be submitted;
- a Job Specification, which describes the requested execution;
- a Job Status, which describes the execution state associated with the Job;
- a Task, which represents asynchronous IRI API operation processing outside the compute-job model;
- an operation entry point, such as the endpoint advertised through `iri:submit-job`.

The normative structural definition of a Job representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with application-level semantics, identity rules, lifecycle interpretation, hypermedia conventions, and interoperability requirements.

## 2. Profile Semantics

An IRI Job represents a submitted unit of computational work.

A Job is created or identified within the context of a compute Resource.

Conceptually:

```text
Compute Resource
      │
      │ iri:submit-job
      ▼
Job-submission operation
      │
      │ returns
      ▼
     Job
```

A Job MAY contain:

- its unique job identifier;
- its current Job Status;
- the Job Specification associated with the job.

A Job representation MUST NOT be interpreted as describing the compute Resource itself.

Likewise, the existence of a Job does not establish:

- that the job is currently executing;
- that the compute Resource is currently available;
- that additional jobs may be submitted;
- that the requester remains authorized to modify the job;
- that the job's requested resources remain available.

Those conditions require the applicable current Job, Resource, authorization, scheduler, and API information.

## 3. Structural Contract

The structural definition of the Job representation is defined by the IRI Facility API OpenAPI `Job` schema.

The current Job schema defines:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Identifier of the Job. |
| `status` | No | Current Job Status when supplied. |
| `job_spec` | No | Job Specification associated with the Job when supplied. |

The `status` property MAY be `null`.

The `job_spec` property MAY be `null`.

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- nullable properties;
- nested Job Status structure;
- nested Job Specification structure;
- structural validation;
- enumerated Job State values.

This profile is authoritative for additional semantic and interoperability conventions associated with the Job representation.

## 4. Job Identity

The `id` property identifies the Job.

For example:

```json
{
  "id": "job-12345"
}
```

The Job identifier MUST be treated as opaque unless another IRI specification explicitly defines additional semantics for the identifier.

Clients MUST NOT assume that the Job identifier encodes:

- the compute Resource;
- the scheduler;
- the submitting user;
- the Project;
- the queue;
- an API path;
- a globally unique identifier.

For example, a client discovering:

```json
{
  "id": "job-12345"
}
```

MUST NOT independently construct:

```text
/api/v2/compute/status/perlmutter/job-12345
```

or:

```text
/api/v2/compute/job/perlmutter/job-12345
```

unless those URLs are supplied by the governing API contract or advertised through hypermedia.

The Job identifier identifies **which Job** is represented.

It does not identify **where the Job representation is located**.

## 5. Job Status

The `status` property contains a `JobStatus` representation when current Job Status information is included.

For example:

```json
{
  "status": {
    "state": "queued",
    "time": 1787072400,
    "message": "Job is waiting in queue"
  }
}
```

The current Job Status structure contains:

| Property | Required | Semantic purpose |
|---|---:|---|
| `state` | Yes | Current execution state represented by the Job Status. |
| `time` | No | Timestamp associated with the status, represented as seconds since the epoch. |
| `message` | No | Human-readable status information. |
| `exit_code` | No | Process exit code when available. |
| `meta_data` | No | Backend-specific metadata associated with the Job Status. |

The `status` property itself MAY be absent or `null` in a Job representation.

The absence of Job Status information MUST NOT be interpreted as establishing a particular Job State.

## 6. Job State

The current IRI Compute API defines the following Job State values:

```text
new
queued
held
active
completed
failed
canceled
```

A Job Status containing:

```json
{
  "state": "active"
}
```

indicates that the current Job Status reports the Job in the `active` state.

The Job State describes execution lifecycle state.

It MUST NOT be interpreted as:

- Resource health;
- Resource availability;
- allocation state;
- Project state;
- authorization state.

### 6.1 State Transitions

The current Job schema defines the set of Job State values but does not define a complete normative Job State transition graph.

Accordingly, this profile does not impose additional mandatory transitions between:

```text
new
queued
held
active
completed
failed
canceled
```

Implementations MUST NOT infer mandatory transition rules solely from the ordering of these values in the schema.

A future IRI specification MAY define additional Job lifecycle invariants or transition semantics.

## 7. Job Status Details

### 7.1 `time`

The `time` property identifies the timestamp associated with the Job Status when supplied.

The current OpenAPI representation expresses this value as seconds since the epoch.

For example:

```json
{
  "time": 1787072400
}
```

The timestamp applies to the represented Job Status.

It MUST NOT automatically be interpreted as:

- Job submission time;
- Job start time;
- Job completion time;
- Job creation time.

unless the governing API contract or backend semantics explicitly establish that meaning.

### 7.2 `message`

`message` provides human-readable information associated with the Job Status.

For example:

```json
{
  "message": "Job is waiting in queue"
}
```

Clients MAY display this value to users.

Clients MUST NOT depend on the free-form `message` string for portable machine processing when an applicable structured property exists.

### 7.3 `exit_code`

`exit_code` contains the process exit code when one is available.

For example:

```json
{
  "state": "completed",
  "exit_code": 0
}
```

The presence or interpretation of an exit code remains subject to the governing compute implementation and Job Status contract.

Clients MUST NOT assume that an absent `exit_code` indicates successful or unsuccessful execution.

### 7.4 `meta_data`

`meta_data` contains backend-specific Job Status information.

For example:

```json
{
  "meta_data": {
    "scheduler_id": "1234567"
  }
}
```

The contents of `meta_data` are backend-specific unless separately standardized.

Portable clients MUST NOT require particular `meta_data` members unless another IRI specification defines those members.

Clients SHOULD ignore unrecognized metadata fields.

## 8. Job Specification

The `job_spec` property MAY contain the Job Specification associated with the Job.

Conceptually:

```text
Job
 │
 ├── id
 ├── status
 └── job_spec
        │
        ├── executable
        ├── container
        ├── arguments
        ├── directory
        ├── name
        ├── environment
        ├── resources
        ├── attributes
        ├── launcher
        └── other execution parameters
```

The current V2 Job Specification includes execution-related concepts such as:

```text
executable
container
arguments
directory
name
inherit_environment
environment
stdin_path
stdout_path
stderr_path
resources
attributes
pre_launch
post_launch
launcher
```

The OpenAPI `JobSpec` schema is authoritative for the structure and validation of those properties.

### 8.1 Job Specification as Request and Representation Data

Job submission uses `JobSpec` as its request representation.

A returned Job MAY include that Job Specification through:

```text
job_spec
```

The two uses have related but distinct contexts:

```text
JobSpec submitted to operation
       ↓
desired execution specification


Job.job_spec
       ↓
specification represented as associated with the Job
```

Clients MUST NOT assume that `job_spec` is present in every returned Job.

The current status-retrieval operation allows Job Specification inclusion to be controlled separately.

### 8.2 Job Specification Is Not a Job

A Job Specification describes requested execution.

A Job represents submitted work.

For example:

```json
{
  "executable": "/usr/bin/python",
  "arguments": [
    "simulation.py"
  ]
}
```

is not, by itself, a Job identity.

A Job exists when the Facility's compute service assigns a Job identity according to the governing API contract.

## 9. Compute Resource Context

A Job executes within the context of a compute Resource.

The current V2 Compute API identifies the compute Resource through the `resource_id` path parameter used by Job operations.

For example:

```text
POST /api/v2/compute/job/{resource_id}

PUT /api/v2/compute/job/{resource_id}/{job_id}

GET /api/v2/compute/status/{resource_id}/{job_id}
```

However, the current `Job` representation does not contain:

```text
resource_uri
```

or another URI-valued Resource relationship.

Therefore, this profile does not invent a Job-to-Resource relation.

In particular, this profile does not normatively define unregistered relations such as:

```text
iri:executed-on
iri:runs-on
iri:submitted-to
```

A future IRI relation MAY define an explicit Job-to-compute-Resource relationship.

Until such a relation is registered, clients MUST NOT derive a Resource URI from the Job identifier.

The governing OpenAPI operation context remains authoritative for identifying the compute Resource used by the operation.

## 10. Job Submission

Job submission is an operation performed against an applicable compute Resource.

The registered operation-affordance relation is:

```text
iri:submit-job
```

with canonical relation URI:

```text
https://iri.science/rels/submit-job
```

The source of `iri:submit-job` is a compute-system Resource having:

```text
resource_type =
urn:doe-iri:resource:compute:system
```

Conceptually:

```text
Compute-system Resource
          │
          │ iri:submit-job
          ▼
Job-submission operation entry point
          │
          │ POST JobSpec
          ▼
         Job
```

The `iri:submit-job` target is the **operation entry point**, not a Job representation.

The relation identifies where an applicable submission operation is located.

It does not itself specify:

- the HTTP method;
- request structure;
- response structure;
- authentication;
- authorization;
- allocation requirements;
- queue policy;
- schedulability.

Those invocation semantics are defined by the governing OpenAPI contract.

## 11. Hypermedia Representation

When represented using HAL, an independently retrievable Job SHOULD advertise its canonical representation through `_links.self`.

For example:

```json
{
  "id": "job-12345",

  "status": {
    "state": "active",
    "time": 1787072400,
    "message": "Job is running"
  },

  "job_spec": {
    "executable": "/usr/bin/python",
    "arguments": [
      "simulation.py"
    ],
    "name": "climate-simulation"
  },

  "_links": {
    "self": {
      "href":
        "https://api.example.org/api/v2/compute/status/perlmutter/job-12345",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/compute/job"
    },

    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],

    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

In this representation:

- `self` identifies the Job representation;
- `profile` identifies the IRI Compute Job semantic profile;
- `service-desc` identifies a machine-readable service description governing applicable compute operations.

The example `self` URI reflects the current V2 retrieval operation.

Clients MUST use the advertised link rather than reconstructing it from `id` or other Job properties.

## 12. Relationship to Existing URI Properties

The current V2 `Job` schema does not define:

```text
self_uri
resource_uri
```

or other URI-valued relationship properties.

Therefore, unlike several Facility, Status, and Account representations, there is no legacy URI property requiring HAL compatibility mapping.

A HAL-enabled producer SHOULD advertise:

```text
_links.self
```

when the Job is independently retrievable.

This allows canonical Job navigation to be introduced without adding another transitional `*_uri` property solely for hypermedia migration.

The current Job schema also lacks an explicit compute-Resource URI.

This profile therefore does not define a compatibility mapping for a Job-to-Resource relationship.

## 13. Job Operations

The V2 Compute API supports operations associated with Jobs, including:

```text
submit Job
update Job
retrieve Job status
```

The current API uses `JobSpec` for submission and update and returns a `Job` representation.

The existence of an operation in OpenAPI does not automatically define an IRI link relation for that operation.

Job-specific operation relations SHOULD be registered before being emitted as normative `iri:*` links.

For example, this profile intentionally does **not** invent:

```text
iri:update-job
iri:cancel-job
iri:get-job-status
```

unless and until those relations are defined by the IRI relation registry.

Until explicit Job operation affordances are registered, clients SHOULD use the governing OpenAPI service description to discover and invoke Job operations.

## 14. Static and Dynamic Semantics

A Job combines relatively stable identity with dynamic execution state.

Relatively stable information includes:

```text
id
```

The following information is dynamic:

```text
status
```

The associated `job_spec` is generally derived from the Job's execution specification but MAY be affected by supported Job update operations.

Clients MUST NOT assume that a previously retrieved Job Status remains current.

For example:

```json
{
  "status": {
    "state": "queued"
  }
}
```

may later become:

```json
{
  "status": {
    "state": "active"
  }
}
```

or another state permitted by the governing Job implementation.

A Job representation SHOULD therefore be treated as a representation of Job information at retrieval time rather than an immutable execution-state record.

Historical execution information, where supported, remains governed by the applicable compute API operation.

## 15. Authorization and Visibility

Job representations and Job operations are authorization-sensitive.

A provider MAY restrict:

- whether a Job is visible;
- whether Job Status is visible;
- whether the Job Specification is visible;
- whether backend metadata is visible;
- whether update operations are permitted;
- whether other Job operations are permitted.

Visibility of a Job MUST NOT itself be interpreted as authorization to modify, cancel, or otherwise operate on the Job.

Likewise, visibility of:

```text
iri:submit-job
```

on a compute Resource does not itself grant permission to submit a Job.

Authorization remains governed by the applicable API security and Facility policy.

Clients SHOULD treat a returned Job representation as the information visible within the current authenticated requester context.

## 16. Conformance

A representation conforms to the IRI Compute Job Profile when:

1. it conforms to the applicable IRI Facility API `Job` schema;
2. its properties are interpreted according to the IRI Compute API and this profile;
3. `id` is treated as a Job identifier rather than a URL template;
4. `status`, when present, conforms to the applicable `JobStatus` schema;
5. `state` is interpreted using the Job State values defined by the governing OpenAPI contract;
6. clients do not impose an undocumented Job State transition graph;
7. `job_spec`, when present, conforms to the applicable `JobSpec` schema;
8. Job Specification semantics are distinguished from Job identity;
9. the compute Resource context is not inferred from the Job identifier;
10. no Job-to-Resource relation is invented without an applicable registered IRI relation;
11. `iri:submit-job` is interpreted as a Resource-to-operation-entry-point relationship, not as a Job relationship;
12. an advertised `_links.self` identifies the canonical retrievable Job representation;
13. profile URIs identify representation semantics and are not used as Job identifiers or link-relation identifiers;
14. clients do not infer or construct Job URLs when an advertised link or governing API contract supplies the applicable target;
15. Job visibility is not interpreted as authorization to perform Job operations.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 17. Profile Identification and Versioning

The canonical identifier for this profile is:

```text
https://iri.science/profiles/compute/job
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, Job identifiers, compute Resource Type URNs, Job instance URLs, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes to individual:

- Jobs;
- Job Status values;
- Job Specifications;
- compute Resources;
- scheduler identifiers;
- registered Job operation relationships

do not themselves require a new Job profile URI unless they materially change the semantics of the common Job representation.

Changes that materially alter the interpretation or processing semantics of the Job representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Compute Job Profile*