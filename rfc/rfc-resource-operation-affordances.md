# RFC: Migrating Resource.supported_endpoints to HAL Operation Affordances

## Abstract

This RFC proposes replacing broad Resource endpoint categories with discoverable, Resource-specific HAL operation affordances. It maps the resource-scoped compute, filesystem, and storage operations in IRI 2.0 OpenAPI to existing or proposed DOE-IRI link relations, defines applicability and visibility rules, and specifies a staged migration from `Resource.supported_endpoints`.

## Status of This Memo

**Status:** Draft for discussion  
**Target:** IRI 2.0 additive adoption; field removal in a subsequently approved contract revision  
**Revision:** 0.1  
**Date:** 2026-09-09

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

The baseline is repository commit [`f030f46a82fb`](https://github.com/doe-iri/iri-facility-api-docs/commit/f030f46a82fb883df0fb59bf6f88e1b0cecf4364). OpenAPI defines existing operation contracts [1]; the relation registry defines existing relations [2]. Except for the already provisional `iri:submit-job`, all operation relations proposed below are **registration requests**, not existing assignments. This document changes no repository registry or production schema by itself.

## 1. Problem and Scope

The current optional `Resource.supported_endpoints` property contains `Endpoint` values `compute` and `filesystem`. It identifies broad router categories, but provides neither an invocation URI nor operation-level support information [1]. A `compute` value alone cannot distinguish job submission, status queries, updates, and cancellation.

This RFC proposes explicit links to applicable operations, using the HAL model already defined for IRI [3]. It covers all 25 Resource-scoped operations in the compute, filesystem, and storage sections of the reviewed OpenAPI: 5 compute + 18 filesystem + 2 storage. The proposal retains the current HTTP methods, inputs, and responses.

The following remain separate:

- Account `Capability`, `capability_uris`, and `iri:has-capability` describe the allocation model.
- Resource Type URNs classify Resources; Resource Definition Profiles govern type-specific semantics and `attributes`.
- Attributes such as `system_capabilities` and `filesystem_capabilities` describe Resource characteristics, not operational URLs.
- Deployment-level API conformance is a separate concern; this migration does not introduce a conformance declaration.

No generic `iri:compute` or `iri:filesystem` relation is required. No separate Resource Definition or Resource State object is introduced.

## 2. Common Relation Contract

For every proposed registration in §3:

| Registration field | Proposed rule |
| --- | --- |
| Canonical relation URI | `https://iri.science/rels/` followed by the exact proposed relation name. These URIs become authoritative only through registration. |
| Requested lifecycle status | Provisional; version 1.0.0 upon registration. |
| Source | An existing Resource representation satisfying §4; selected Job relations additionally permit Job representations as specified below. |
| Target | The Resource-scoped operation entry point, or an explicitly advertised URI template for it. |
| Cardinality | Zero or one link object per relation in each source representation. |
| Applicability | The adapter implements the mapped operation for the identified Resource and its operation context. |
| Stability | Configured applicability; changes with configuration or visibility, not solely with load, capacity, queue state, or health. |
| Visibility | Authorization MAY suppress a link. Presence grants no permission; absence means “not advertised in this representation,” not “unsupported everywhere.” |
| Invocation | The applicable deployed OpenAPI governs method, parameters, body, responses, errors, and security. |
| Registry ownership | Registration must identify an approved change controller and link the governing OpenAPI and relevant profiles. |

An adopting producer SHOULD advertise each applicable operation visible to the requester and MUST NOT advertise an operation its adapter does not implement for that context. It MUST NOT synthesize all operation links merely because a category appears in `supported_endpoints`.

The producer MUST bind `resource_id` to the represented Resource's adapter context. Clients MUST follow the advertised target rather than construct paths from IDs, types, or relation names. If an operation belongs to another Resource, the producer must expose the appropriate Resource relationship rather than label the operation as belonging to the source.

HAL does not encode an HTTP method or request schema. This RFC adds no nonstandard `method` or `operationId` member to HAL links. Producers SHOULD advertise `service-desc` for the deployed operation contract. Link `type` is a response representation hint, not a request Content-Type. Producers MUST NOT place a Job profile on `iri:submit-job` or another mutation-operation link.

## 3. Operation Registration Proposals

The tables bind proposed semantic names to the reviewed OpenAPI. They are not URL-construction instructions or a second assignment registry. Upon adoption, individual definitions under `registry/relations/` and the Link Relation Index become authoritative.

### 3.1 Compute

| Relation | Meaning | Method and current path | OpenAPI operationId |
| --- | --- | --- | --- |
| `iri:submit-job` | Submit a job | `POST /api/v2/compute/job/{resource_id}` | `launchJob` |
| `iri:update-job` | Update a selected job | `PUT /api/v2/compute/job/{resource_id}/{job_id}` | `updateJob` |
| `iri:get-job` | Retrieve a selected job and its status | `GET /api/v2/compute/status/{resource_id}/{job_id}` | `getJob` |
| `iri:query-jobs` | Query job statuses | `POST /api/v2/compute/status/{resource_id}` | `getJobs` |
| `iri:cancel-job` | Cancel a selected job | `DELETE /api/v2/compute/cancel/{resource_id}/{job_id}` | `cancelJob` |

`iri:submit-job` retains its existing definition and compute-system-only source scope [2]. The four other rows are new registrations. `query-jobs` intentionally reflects `POST getJobs`, not an invented GET collection operation.

On a compute-system Resource, the producer binds `resource_id`. For `get-job`, `update-job`, and `cancel-job`, it MAY leave only `job_id` as an advertised URI-template variable and MUST set `templated: true`. Expansion identifies a selected job in that Resource context; it grants no permission to act on arbitrary job IDs.

The new `get-job`, `update-job`, and `cancel-job` registrations also permit a Job source with both IDs already bound by the producer. A Job's canonical retrieval URI remains `self`; a `get-job` link is optional there. The producer must retain the operation context because clients cannot infer a Resource identifier from a Job identifier. Job updates remain limited to attributes supported by the facility's contract [1, 5].

### 3.2 Filesystem

| Relation | Meaning | Method and current path | OpenAPI operationId |
| --- | --- | --- | --- |
| `iri:change-file-mode` | Change file permission mode | `POST /api/v2/filesystem/chmod/{resource_id}` | `chmod` |
| `iri:change-file-owner` | Change file ownership | `POST /api/v2/filesystem/chown/{resource_id}` | `chown` |
| `iri:identify-file` | Identify file or directory type | `POST /api/v2/filesystem/file/{resource_id}` | `file` |
| `iri:stat-file` | Retrieve file metadata | `POST /api/v2/filesystem/stat/{resource_id}` | `stat` |
| `iri:create-directory` | Create a directory | `POST /api/v2/filesystem/mkdir/{resource_id}` | `mkdir` |
| `iri:create-symlink` | Create a symbolic link | `POST /api/v2/filesystem/symlink/{resource_id}` | `symlink` |
| `iri:list-directory` | List directory contents | `POST /api/v2/filesystem/ls/{resource_id}` | `ls` |
| `iri:read-file-head` | Read the beginning of files | `POST /api/v2/filesystem/head/{resource_id}` | `head` |
| `iri:view-file` | View file content | `POST /api/v2/filesystem/view/{resource_id}` | `view` |
| `iri:read-file-tail` | Read the end of a file | `POST /api/v2/filesystem/tail/{resource_id}` | `tail` |
| `iri:checksum-file` | Compute the file checksum | `POST /api/v2/filesystem/checksum/{resource_id}` | `checksum` |
| `iri:remove-path` | Remove a file or directory | `POST /api/v2/filesystem/rm/{resource_id}` | `rm` |
| `iri:compress-paths` | Compress files or directories | `POST /api/v2/filesystem/compress/{resource_id}` | `compress` |
| `iri:extract-archive` | Extract an archive | `POST /api/v2/filesystem/extract/{resource_id}` | `extract` |
| `iri:move-path` | Move a file or directory | `POST /api/v2/filesystem/mv/{resource_id}` | `mv` |
| `iri:copy-path` | Copy a file or directory | `POST /api/v2/filesystem/cp/{resource_id}` | `cp` |
| `iri:download-file` | Request a file download | `POST /api/v2/filesystem/download/{resource_id}` | `download` |
| `iri:upload-file` | Upload a file | `POST /api/v2/filesystem/upload/{resource_id}` | `upload` |

Each relation applies within an explicitly configured filesystem operation context (§4). File paths, ownership values, modes, and other inputs remain in their existing OpenAPI-defined request locations.

All 18 operations return `TaskSubmitResponse` in the reviewed contract, including inspection and download operations [1]. The response's existing `task_uri` maps to standard `monitor`; the retrieved Task exposes `self` [3, 5]. This RFC does not turn inspection operations into GET requests or make `download-file` a direct binary-download link.

`upload-file` requires the existing multipart body and the required query parameter `path`. A producer MAY advertise `.../upload/<bound-resource>{?path}` with `templated: true`; clients MUST supply `path` and the multipart body according to OpenAPI. Other file operands remain request-body data. Size limits and operation-specific result interpretation remain governed by the existing contract.

### 3.3 Storage Discovery

| Relation | Meaning | Method and current path | OpenAPI operationId |
| --- | --- | --- | --- |
| `iri:resolve-storage-locations` | Resolve storage locations in this Resource context | `GET /api/v2/storage/locations/{resource_id}` | `getStorageLocations` |
| `iri:get-storage-access-endpoints` | Retrieve access descriptions for this storage Resource | `GET /api/v2/storage/access-endpoints/{resource_id}` | `getStorageAccessEndpoints` |

These extend discovery beyond the two legacy endpoint categories; they do not add `storage` to the current `Endpoint` enumeration.

`resolve-storage-locations` identifies user-context resolution of `StorageInstance` entries, including optional project/allocation and intent filters. It is not a replacement for configured topology links such as `iri:has-mount`.

`get-storage-access-endpoints` identifies retrieval of `AccessEndpoint` descriptions for a storage Resource. It does not execute a Globus transfer, S3 operation, or XRootD request, nor guarantee every advertised protocol operation succeeds. Existing `AccessEndpoint.capabilities` retains its meaning; this migration concerns only `Resource.supported_endpoints` [1].

## 4. Applicability to Registered Resource Types

OpenAPI uses `resource_id` parameters but does not define an exhaustive Resource-Type-to-operation matrix. The mapping below is a **proposed semantic policy**, not a claim that every facility or every Resource of these types implements the operations. Type classification alone MUST NOT imply operation support.

All shortened type names below have prefix `urn:doe-iri:resource:`; they are assigned types in the reviewed registry [4].

| Resource types | Proposed eligible operations and conditions |
| --- | --- |
| `compute:system` | Compute relations; filesystem relations when the system is a configured filesystem execution context; storage-location resolution when supported for that context. |
| `compute:node` | Filesystem operations and storage-location resolution only if explicitly configured for that node. No automatic compute-job relations; a node is not the source permitted by existing `submit-job`. |
| `storage:filesystem` | Filesystem operations, location resolution, and access-endpoint discovery when the adapter accepts that filesystem ID and defines its path context. |
| `storage:mount` | Filesystem operations and location resolution only if the adapter supports that mount ID and its mount-specific context. A mount does not inherit operations from its filesystem or consuming system. |
| `storage:system`, `storage:block`, `storage:object` | Storage access-endpoint discovery where implemented; location resolution only where its existing response semantics apply. No file-operation inference from storage classification. |
| `service:dtn` | Filesystem operations and location resolution only if the DTN itself is the explicit adapter context. Existing hosting and mount-access links do not imply these operations. No generic transfer-execution relation is defined by this OpenAPI mapping. |
| Generic `compute`, `storage` | Conditional filesystem/location operations as above when actual adapter semantics are known; access-endpoint discovery for generic storage. Generic compute does not satisfy the existing compute-system-only `submit-job` source rule. |
| `compute:cpu`, `compute:gpu` | No operation family assigned by this RFC; hardware classification does not imply a scheduler or filesystem context. |
| `service`, `service:inference`, `network`, `system`, `website`, `unknown` | No operation family assigned by this RFC. The reviewed API does not supply corresponding type-specific execution contracts sufficient for new mappings. |

For filesystem operations, an adapter MUST establish the path namespace and execution/access context for the source Resource. A filesystem mounted on several systems does not imply one interchangeable execution context. If a single source cannot identify one unambiguous context, expose separate Resources using the existing model and link through registered topology relations; do not silently choose a host or add an undocumented context selector.

A legacy generic compute Resource supporting job submission requires either accurate reclassification as a registered compute system or an explicitly reviewed relation-scope extension before full migration. Do not silently broaden `iri:submit-job`, change Resource types, or discard legacy functionality.

## 5. Examples

These are partial Resource representations illustrating the proposed extension, not complete OpenAPI instances. The new relations require registration before normative use.

### 5.1 Compute Resource during coexistence

```json
{
  "id": "system-a",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "supported_endpoints": ["compute"],
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/system-a"
    },
    "curies": [
      {"name": "iri", "href": "https://iri.science/rels/{rel}", "templated": true}
    ],
    "iri:submit-job": {
      "href": "https://api.example.org/api/v2/compute/job/system-a"
    },
    "iri:query-jobs": {
      "href": "https://api.example.org/api/v2/compute/status/system-a"
    },
    "iri:cancel-job": {
      "href": "https://api.example.org/api/v2/compute/cancel/system-a/{job_id}",
      "templated": true
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

### 5.2 Filesystem Resource after field retirement

```json
{
  "id": "scratch",
  "resource_type": "urn:doe-iri:resource:storage:filesystem",
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/scratch"
    },
    "curies": [
      {"name": "iri", "href": "https://iri.science/rels/{rel}", "templated": true}
    ],
    "iri:list-directory": {
      "href": "https://api.example.org/api/v2/filesystem/ls/scratch"
    },
    "iri:upload-file": {
      "href": "https://api.example.org/api/v2/filesystem/upload/scratch{?path}",
      "templated": true
    },
    "iri:get-storage-access-endpoints": {
      "href": "https://api.example.org/api/v2/storage/access-endpoints/scratch"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

URI templates follow RFC 6570 [6]. Runtime template expansion and OpenAPI parameter serialization must preserve the advertised binding and encoding.

## 6. Migration and Compatibility

### Phase 1 — Register and add

Approve the relation definitions and update the affected profiles, Link Relation Index, and HAL RFC. Add the reusable HAL schema to OpenAPI through its normal revision process. Adopting implementations publish applicable links alongside the existing field.

`supported_endpoints` remains optional with its current category semantics. Do not change it into a list of relation names, URLs, or operations.

Where the field is supplied, advertised compute and filesystem operations MUST be consistent with their legacy category. The reverse does not hold: a category may remain when some or all operation links are hidden or not yet implemented in discovery. Storage-discovery links have no legacy category mapping. This is semantic consistency, not the URI-equality rule for `self_uri` and other URI-valued properties.

### Phase 2 — Deprecate and migrate clients

Mark `supported_endpoints` deprecated in an approved OpenAPI revision. Clients prefer a recognized advertised relation and its deployed operation contract. Legacy fallback MAY use an existing documented integration when no suitable link is advertised; clients MUST NOT turn a category label into a guessed URL or probe mutations to discover support.

Missing `_links` may indicate an older producer. Missing individual relations, or a Resource with only `self` and `service-desc`, does not prove lack of implementation support. This proposal intentionally replaces navigation information; it does not preserve an authorization-independent negative support assertion.

Internal adapter routing MAY retain endpoint categories independently of the public field. Existing `getComputeResources` and `getFilesystemResources` discovery operations remain unchanged.

### Phase 3 — Retire the field

Remove the field from the public contract only in a separately approved compatibility revision after implementations and clients have migrated. Its current optionality does not justify silently withdrawing it from clients that use it.

The retirement gate requires coverage for every legacy Resource operation, explicit resolution of generic-type and context ambiguities, and documented handling of callers needing broad support declarations. Such callers may need a separately specified conformance mechanism; this RFC does not invent one.

## 7. Authorization, Availability, and Safety

Operation links describe configured, discoverable affordances. They do not grant an allocation or permission, guarantee capacity, or promise successful execution. Producers enforce authorization at invocation regardless of link visibility.

Links MAY be filtered by authorization and, on Job representations, operation applicability. Temporary outages alone SHOULD NOT remove configured Resource operation links. Clients consult current representations and handle ordinary HTTP failures.

Caller-specific representations require appropriate cache controls. Links MUST NOT contain credentials or secrets. A client must not automatically forward credentials to an unrelated origin merely because a link or service description names it. Destructive actions such as removal, overwrite, cancellation, and ownership changes remain explicit invocations governed by the caller's policy.

## 8. Validation and Adoption Work

Before adoption:

1. Register the 24 new relations and retain the existing provisional `submit-job` definition.
2. Validate all 25 method/path/operationId mappings against the adopted OpenAPI version.
3. Verify source-type and context rules, singular cardinality, concrete Resource binding, and advertised template variables.
4. Test both visible and authorization-suppressed links without treating omission as unsupported behavior.
5. Verify multipart upload, POST job queries, Task monitoring, and legacy-field coexistence.
6. Update the affected Resource Definition Profiles, Job profile, HAL RFC, and OpenAPI in coordinated review.

This RFC does not register operations absent from the reviewed contract, such as object CRUD, block provisioning, inference invocation, or general transfer submission. Account/facility/status navigation and Task lifecycle management are outside this field migration. Standard `monitor` and Task `self` remain the completion-discovery mechanism; Task deletion is not redefined as cancellation.

## References

Repository links are pinned to the reviewed commit.

1. [IRI 2.0 OpenAPI](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/specification-v2/openapi/all_spec_v2.yaml), particularly `Resource`, `Endpoint`, `AccessEndpoint`, compute, filesystem, storage, and Task operations.
2. [Link Relation Index](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/registry/relations/README.md) and [submit-job](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/registry/relations/submit-job.md).
3. [HAL links RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/rfc/rfc-hal-links.md).
4. [Resource Type Registry](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/registry/urns/resource-types.md), [Representation Profiles](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/registry/profiles/README.md), and [Type-Specific Attributes RFC](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/rfc/rfc-type-specific-attributes.md).
5. [Job Profile](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/registry/profiles/compute/job.md) and [Task Profile](https://github.com/doe-iri/iri-facility-api-docs/blob/f030f46a82fb883df0fb59bf6f88e1b0cecf4364/registry/profiles/task.md).
6. [RFC 6570: URI Template](https://www.rfc-editor.org/rfc/rfc6570.html).
7. [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html).

