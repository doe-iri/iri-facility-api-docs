# IRI Task Profile

**Profile URI:** `https://iri.science/profiles/task`  
**OpenAPI type:** `Task`  
**Status:** Draft  
**Version:** 1.0.0

## 1. Purpose

This document defines the semantic profile for an IRI Task representation.

The canonical identifier for this profile is:

```text
https://iri.science/profiles/task
```

An IRI Task represents the asynchronous execution state of an operation initiated through an IRI Facility API.

A Task provides a persistent representation through which a client can determine the progress and outcome of an asynchronous operation.

Tasks are particularly useful for operations that cannot reasonably complete within the lifetime of the initiating HTTP request.

A Task is distinct from:

- the operation that created the Task;
- the Resource against which the operation was performed;
- a Job, which represents submitted computational work;
- a Task Command, which records command information associated with the Task;
- a Task submission response, which identifies the Task created by an asynchronous operation.

The normative structural definition of a Task representation is provided by the IRI Facility API OpenAPI specification.

This profile supplements that schema with lifecycle semantics, result interpretation, command semantics, hypermedia conventions, authorization considerations, and interoperability requirements.

## 2. Profile Semantics

An IRI Task represents asynchronous processing associated with an IRI API operation.

Conceptually:

```text
IRI operation
     │
     │ initiates asynchronous work
     ▼
TaskSubmitResponse
     │
     │ task_uri
     ▼
    Task
     │
     ├── status
     ├── command
     └── result
```

A Task allows a client to separate:

```text
operation invocation
        ↓
request accepted

from

operation completion
        ↓
result available
```

The existence of a Task indicates that an identifiable asynchronous operation is represented.

It does not by itself establish:

- successful completion;
- authorization to repeat the operation;
- current Resource availability;
- continued validity of the original operation;
- that a result is currently available.

Clients SHOULD retrieve the Task representation to determine its current execution state.

## 3. Structural Contract

The structural definition of the Task representation is defined by the IRI Facility API OpenAPI `Task` schema.

The current Task schema defines:

| Property | Required | Semantic purpose |
|---|---:|---|
| `id` | Yes | Stable identifier for the Task. |
| `status` | No | Current execution state of the Task. |
| `result` | No | Result of Task execution when available. |
| `command` | No | Command information associated with the Task when available. |

The current `status` property defaults to:

```text
pending
```

when not otherwise supplied according to the governing OpenAPI contract.

The `result` property MAY be `null`.

The `command` property MAY be `null`.

The OpenAPI schema is authoritative for:

- property names;
- JSON data types;
- required properties;
- nullable properties;
- default values;
- Task Status values;
- Task Command structure;
- structural validation.

This profile is authoritative for additional semantic and interoperability conventions associated with the Task representation.

## 4. Task Identity

The `id` property identifies the Task instance.

For example:

```json
{
  "id": "task-123"
}
```

The Task identifier MUST be treated as opaque unless another IRI specification explicitly defines additional semantics for the identifier.

Clients MUST NOT assume that the Task identifier encodes:

- the operation type;
- the Resource against which the operation was performed;
- the user initiating the operation;
- the Facility;
- the Task creation time;
- an API path.

For example, a client discovering:

```json
{
  "id": "task-123"
}
```

MUST NOT independently construct:

```text
/api/v2/task/task-123
```

merely from the identifier.

The Task's canonical retrieval URI SHOULD be obtained from an advertised URI or hypermedia link.

## 5. Task Status

The `status` property represents the current execution state of the Task.

The current IRI Facility API defines the following Task Status values:

```text
pending
active
completed
failed
canceled
```

Conceptually:

```text
pending
   │
   ▼
 active
   │
   ├────────► completed
   │
   ├────────► failed
   │
   └────────► canceled
```

The diagram above illustrates a common interpretation only.

The current OpenAPI schema defines the available states but does not itself establish a complete normative state-transition graph.

Accordingly, implementations MUST NOT infer mandatory state transitions solely from the ordering or naming of the Task Status values.

### 5.1 `pending`

`pending` indicates that the Task has been created but execution has not yet been represented as active.

### 5.2 `active`

`active` indicates that execution of the Task is in progress.

### 5.3 `completed`

`completed` indicates that Task execution has completed successfully according to the Facility's Task-processing semantics.

A completed Task MAY contain a `result`.

### 5.4 `failed`

`failed` indicates that Task execution did not complete successfully.

A failed Task MAY contain result or diagnostic information when permitted by the governing API contract.

### 5.5 `canceled`

`canceled` indicates that Task processing has been canceled according to the Facility's Task-processing semantics.

Cancellation of a Task MUST NOT automatically be interpreted as proof that all effects of the underlying operation were rolled back.

The semantics of partially completed operations remain operation-specific.

## 6. Task Lifecycle

A Task is a dynamic representation.

Its `status` may change as asynchronous processing progresses.

For example:

```json
{
  "id": "task-123",
  "status": "pending"
}
```

may later become:

```json
{
  "id": "task-123",
  "status": "active"
}
```

and later:

```json
{
  "id": "task-123",
  "status": "completed"
}
```

Clients MUST NOT assume that a previously retrieved Task representation reflects current Task state.

Clients monitoring asynchronous work SHOULD retrieve the Task's advertised URI until the Task reaches an appropriate terminal state according to the governing API contract.

This profile does not define:

- polling frequency;
- Task retention duration;
- expiration semantics;
- retry policy;
- result retention duration.

Those concerns remain defined by the applicable Facility implementation or future IRI specifications.

## 7. Task Result

The `result` property contains the result of Task execution when available.

For example:

```json
{
  "id": "task-123",
  "status": "completed",
  "result": {
    "path": "/project/data/output.dat"
  }
}
```

The current Task schema permits arbitrary object content in `result`.

Therefore, the meaning and structure of `result` are operation-specific unless another IRI specification defines a portable result representation for that operation.

A generic client:

- MUST NOT assume particular members are present in `result`;
- SHOULD ignore unrecognized members;
- SHOULD use the governing operation contract to interpret known result data.

### 7.1 Result and Task Status

The presence of `result` MUST NOT independently determine the Task Status.

For example, a Task MAY contain diagnostic or partial information while:

```text
status = failed
```

Likewise:

```text
status = completed
```

does not require a non-null `result` unless the governing operation contract explicitly requires one.

Clients SHOULD interpret `status` and `result` together.

## 8. Task Command

The `command` property MAY contain a `TaskCommand` describing the command associated with the Task.

The current Task Command structure contains:

| Property | Required | Semantic purpose |
|---|---:|---|
| `router` | Yes | Identifies the command router or operation domain. |
| `command` | Yes | Identifies the command executed by the Task. |
| `args` | Yes | Command arguments associated with the Task. |

For example:

```json
{
  "command": {
    "router": "filesystem",
    "command": "chmod",
    "args": {
      "path": "/home/user/file",
      "mode": "755"
    }
  }
}
```

### 8.1 `router`

`router` identifies the operation domain or command router associated with the Task.

For example:

```text
filesystem
```

The current schema represents `router` as a string.

This profile does not define a controlled vocabulary for router values.

### 8.2 `command`

`command` identifies the command associated with the Task.

For example:

```text
chmod
```

The command value is descriptive of the represented Task operation.

It MUST NOT be interpreted as an HTTP method or API path.

### 8.3 `args`

`args` contains arguments associated with the command.

The schema permits arbitrary object content.

The meaning of individual arguments is therefore determined by the applicable operation contract.

## 9. Task Creation and Discovery

Tasks may be created as a consequence of invoking asynchronous IRI operations.

The current V2 API uses `TaskSubmitResponse` to return Task identity information from such operations.

The response contains:

```text
task_id
task_uri
```

Conceptually:

```text
asynchronous operation
        │
        ▼
TaskSubmitResponse
        │
        ├── task_id
        │
        └── task_uri
                 │
                 ▼
                Task
```

`task_id` identifies the Task.

`task_uri` identifies the URI through which the Task representation can be retrieved.

Clients SHOULD use `task_uri` rather than construct a Task URI from `task_id`.

For example, given:

```json
{
  "task_id": "task-123",
  "task_uri": "https://api.example.org/api/v2/task/task-123"
}
```

a client SHOULD follow:

```text
https://api.example.org/api/v2/task/task-123
```

rather than independently assuming the Facility's Task routing structure.

## 10. Hypermedia Representation

When represented using HAL, a Task SHOULD advertise its canonical representation through `_links.self`.

For example:

```json
{
  "id": "task-123",
  "status": "active",

  "command": {
    "router": "filesystem",
    "command": "chmod",
    "args": {
      "path": "/project/data/file.txt",
      "mode": "755"
    }
  },

  "result": null,

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/task/task-123",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/task"
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

- `self` identifies the Task representation;
- `profile` identifies the IRI Task semantic profile;
- `service-desc` identifies a machine-readable service description defining applicable Task operations.

The current IRI relation registry does not define a Task-specific relation required by this profile.

This profile therefore does not invent relations such as:

```text
iri:created-by
iri:operates-on
iri:result-of
iri:cancel-task
```

Such relations SHOULD be separately registered before normative use.

## 11. Relationship to Existing URI Properties

The current `Task` schema does not define:

```text
self_uri
```

or other URI-valued relationship properties.

Therefore there is no legacy Task URI property requiring migration to HAL.

However, the asynchronous Task submission response defines:

```text
task_uri
```

which identifies the Task representation produced by the asynchronous operation.

Conceptually:

```text
TaskSubmitResponse.task_uri
        │
        ▼
Task._links.self.href
```

When both forms are available for the same Task, they SHOULD identify the same Task representation.

A HAL-enabled Task producer SHOULD advertise `_links.self`.

This allows Task identity and navigation to be expressed directly in the Task representation without adding another transitional `self_uri` property.

## 12. Task Operations

The current V2 Task API supports operations including:

```text
GET /api/v2/task/{task_id}

GET /api/v2/task

DELETE /api/v2/task/{task_id}
```

The OpenAPI specification remains authoritative for:

- HTTP methods;
- paths;
- path parameters;
- response schemas;
- authentication;
- authorization;
- error handling.

A representation profile does not replace the OpenAPI operation contract.

### 12.1 Task Deletion

The presence of an HTTP `DELETE` operation does not, by itself, define an IRI hypermedia relation.

This profile therefore does not invent:

```text
iri:delete-task
```

or:

```text
iri:cancel-task
```

Furthermore, deletion and cancellation MUST NOT be assumed to have identical semantics.

The current Task model contains a `canceled` Task Status, while the Task API also exposes an HTTP DELETE operation.

Unless a governing API specification explicitly equates these concepts, clients MUST NOT assume:

```text
DELETE Task
```

means:

```text
cancel underlying operation
```

Deletion may instead concern the Task representation or implementation-specific Task processing.

The governing OpenAPI and Facility semantics remain authoritative.

## 13. Media Type

This profile identifies the semantics of the Task representation independently of a particular serialization.

When a Task is represented using HAL JSON, the representation SHOULD use:

```text
application/hal+json
```

and MAY identify this profile where appropriate:

```text
https://iri.science/profiles/task
```

These identifiers answer different questions:

```text
application/hal+json
    ↓
HOW the representation is encoded


https://iri.science/profiles/task
    ↓
WHAT semantic representation contract applies
```

They MUST NOT be treated as interchangeable.

## 14. Static and Dynamic Semantics

A Task combines stable identity with dynamic execution information.

Relatively stable information includes:

```text
id
command
```

Dynamic information includes:

```text
status
result
```

The `command` generally describes the operation associated with Task creation and SHOULD NOT change merely because execution status changes.

The `status` is inherently dynamic.

The `result` MAY appear or change as processing progresses according to the governing implementation.

The existence of a Task does not imply that the Resource associated with the originating operation remains:

- available;
- reachable;
- healthy;
- authorized for additional operations.

Task state and Resource state are distinct.

## 15. Authorization and Visibility

Task representations are authorization-sensitive.

A provider MAY restrict:

- whether a Task is visible;
- whether its command is visible;
- whether command arguments are visible;
- whether its result is visible;
- whether Task deletion is permitted;
- whether Task collections expose the Task.

Command arguments and results MAY contain sensitive operational or user information.

Implementations SHOULD apply authorization appropriate to that information.

Visibility of a Task MUST NOT itself be interpreted as authorization to:

- repeat the originating operation;
- delete the Task;
- cancel underlying work;
- access the Resource associated with the original operation.

The absence of a Task from a collection MUST NOT necessarily be interpreted as proof that the Task does not exist when authorization or retention policy may affect visibility.

## 16. Conformance

A representation conforms to the IRI Task Profile when:

1. it conforms to the applicable IRI Facility API `Task` schema;
2. its properties are interpreted according to the IRI Facility API and this profile;
3. `id` is treated as a Task identifier rather than a URL template;
4. `status` is interpreted using the Task Status values defined by the governing OpenAPI contract;
5. clients do not impose an undocumented Task Status transition graph;
6. `result` is treated as operation-specific unless another IRI specification defines its contents;
7. `command`, when present, conforms to the applicable `TaskCommand` structure;
8. `router` and `command` are not interpreted as API paths or HTTP methods;
9. Task discovery uses advertised Task URIs rather than URL construction where such URIs are available;
10. `_links.self`, when supplied, identifies the canonical retrievable Task representation;
11. profile URIs identify representation semantics and are not used as Task identifiers or link-relation identifiers;
12. no Task-specific `iri:*` relationships are inferred without registered relation definitions;
13. HTTP DELETE is not automatically equated with Task cancellation;
14. Task visibility is not interpreted as authorization to invoke related operations;
15. clients do not require operation-specific `result` or `args` members unless defined by the governing operation contract.

A conforming representation MAY contain additional properties and links where permitted by the applicable IRI API specification.

## 17. Profile Identification and Versioning

The canonical identifier for this profile is:

```text
https://iri.science/profiles/task
```

The profile URI is a stable semantic identifier.

Repository paths, GitHub URLs, OpenAPI document locations, Task identifiers, Task instance URLs, command names, and documentation-generation URLs MUST NOT be substituted for this canonical identifier.

The canonical URI SHOULD resolve to documentation describing this profile.

The profile version identifies the revision of this profile document.

Compatible editorial clarifications and backward-compatible semantic additions MAY retain the same profile URI.

Changes to individual:

- Tasks;
- Task Status values;
- Task commands;
- Task results;
- asynchronous operation types;
- registered Task-related link relations

do not themselves require a new Task profile URI unless they materially change the semantics of the common Task representation.

Changes that materially alter the interpretation or processing semantics of the Task representation SHOULD be evaluated for compatibility before incorporation into the existing profile.

The canonical profile URI SHOULD remain stable across compatible revisions.

---

*DOE Integrated Research Infrastructure — Task Profile*