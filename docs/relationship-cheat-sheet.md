---
layout: default
title: Relationship Cheat Sheet
parent: IRI 2.0
nav_order: 7
permalink: /relationship-cheat-sheet/
---

# Relationship Cheat Sheet

This page summarizes all **47 registered IRI relations** and the standard links
used by IRI v2. Each relation name links to its authoritative definition. This
is an explanatory reference; the definitions, profiles, and checked-out OpenAPI
remain authoritative. Proposed changes are not included.

## Reading the tables

- **Direction:** source → target. Cardinality counts targets **per source**;
  it does not impose an inverse cardinality unless the definition says so.
- **Cardinality:** `1` means exactly one; `0..1` means optional, at most one;
  `0..*` means zero or more.
- **Type shorthand:** `compute:node`, `service:dtn`, and similar names expand
  under `urn:doe-iri:resource:`. They identify Resource Types. Names such as
  `Event`, `Site`, and `Job` identify API representations, not Resource Type URNs.
- **Any Resource:** any conforming IRI `Resource` representation, including a
  service Resource. This does not mean any API representation.
- **Visibility:** the tables describe semantic cardinality. Authorization can
  hide links or targets where the definition permits it. Required URI fields
  and retained HAL links must remain consistent; omission does not generally
  prove that a relationship or capability does not exist.
- **Configuration:** topology links describe configured relationships. They do
  not establish current health, availability, caller permission, or successful
  future access. Ordinary outages do not by themselves remove configured
  relationships.
- **Wire form:** HAL requires `href`; never emit `"href": null`. Use singular
  link objects for singular relations and arrays for plural relations, following
  the definition's examples and [HAL links RFC][hal-rfc]. A link's `profile`
  describes its target representation, not its relation.

## Core, facility, status, and allocation relations — 10

| Relation | Allowed source | Required target | Cardinality | Description and key restrictions |
|---|---|---|---|---|
| [iri:located-at][located-at] | Any Resource | `Site` | `1` | Physical/administrative site from required `site_uri`. Do not independently hide the link while returning that field. It does not identify live process placement or hosting. |
| [iri:has-site][has-site] | `Facility` | `Site` | `0..*` | Associated sites from `site_uris`. |
| [iri:has-resource][has-resource] | `Site` | Any Resource | `0..*` | Resources hosted at the site, from `resource_uris`. |
| [iri:generated-by][generated-by] | `Event` | `Incident` | `0..1` | Incident associated with the event. Required-but-nullable `incident_uri`: null means omit the link. |
| [iri:has-event][has-event] | `Incident` | `Event` | `0..*` | Events recorded as part of the incident, from `event_uris`. Does not require an inverse relationship on every event. |
| [iri:impacts][impacts] | `Event` | Any Resource | `1` | Resource to which the event applies, from required `resource_uri`. Distinct from an incident's possible impact scope. |
| [iri:may-impact][may-impact] | `Incident` | Any Resource | `0..*` | Resources within the incident's assessed possible impact scope, from `resource_uris`. |
| [iri:has-project][has-project] | `ProjectAllocation` | `Project` | `1` | Project to which the allocation belongs, from required `project_uri`. |
| [iri:has-capability][has-capability] | Any Resource; `ProjectAllocation` | `Capability` | Resource: `0..*`; ProjectAllocation: `1` | A Resource provides the Capability (`capability_uris`); a ProjectAllocation applies to it (required `capability_uri`). |
| [iri:has-project-allocation][has-project-allocation] | `UserAllocation` | `ProjectAllocation` | `1` | Parent project allocation, from required `project_allocation_uri`. |

Where both legacy URI properties and HAL links are returned, their targets
must agree. A nullable or absent URI maps to an omitted link. These mappings
are additive; HAL links do not remove the current URI-property requirements.

## Storage topology relations — 8

| Relation | Allowed source Resource Type | Required target Resource Type | Cardinality | Description and key restrictions |
|---|---|---|---|---|
| [iri:provides-filesystem][provides-filesystem] | `storage:system` | `storage:filesystem` | `0..*` | Storage infrastructure provides a logical filesystem. This is provider topology, not mount or health information. |
| [iri:provides-block][provides-block] | `storage:system` | `storage:block` | `0..*` | Storage infrastructure provides logical block storage. Current attachment is not implied. |
| [iri:provides-object][provides-object] | `storage:system` | `storage:object` | `0..*` | Storage infrastructure provides a logical object resource. The target is not an object API endpoint. |
| [iri:has-mount][has-mount] | `storage:filesystem` | `storage:mount` | `0..*` | Filesystem exposure through a mount relationship Resource. A mount should normally describe one filesystem-to-consuming-system exposure and be referenced by one filesystem. |
| [iri:mounted-on][mounted-on] | `storage:mount` | `compute:system` | `1` | Consuming system whose namespace contains the filesystem exposure. One mount describes one exposure on one system; use separate mounts for different systems. Nodes and services are not allowed targets. |
| [iri:accesses-mount][accesses-mount] | Any Resource representing an actual configured filesystem consumer | Exactly `storage:mount` | `0..*` | Consumer is configured to access a filesystem through this exposure. Includes compute, systems, nodes, generic services, DTNs, inference services, and other conforming types with that role; type validity alone is insufficient. |
| [iri:accessed-by][accessed-by] | Exactly `storage:mount` | Any Resource representing an actual configured filesystem consumer | `0..*` | Inverse of `iri:accesses-mount`: identifies consumers of this exposure. Target `profile` describes the actual consumer, using the common Resource profile unless an applicable specialized profile is established. |
| [iri:attached-to][attached-to] | `storage:block` | `compute:system` or `compute:node` | Exclusive: `0..1`; shared: `0..*` | Configured block presentation/attachment. Cardinality depends on `urn:doe-iri:storage:block-access-mode:exclusive` or `:shared`. Shared mode does not establish safe arbitrary concurrent writes. |

Mounts are relationship Resources carrying exposure-specific information such
as `mount_path`, access mode, and protocol. A mount path belongs to the
declared consuming system's namespace. If its required consuming-system target
cannot be disclosed, the definition recommends hiding the mount itself rather
than presenting misleading, incomplete topology.

The mount-access pair describes the same configured association in opposite
directions. Each direction is independently optional; neither reciprocal
advertisement nor exhaustive lists are required. Visible links describing the
same configuration must agree. Authorization may hide consumers or mounts,
and omission is not a negative access assertion. Resource Types, hosting,
containment, and `iri:mounted-on` alone do not establish access. Access links do
not relocate `mount_path` into a consumer's node, service, or container
namespace, change the exactly-one `iri:mounted-on` target, or confer operation
eligibility.

## Compute topology relations — 3

| Relation | Allowed source Resource Type | Required target Resource Type | Cardinality | Description and key restrictions |
|---|---|---|---|---|
| [iri:has-node][has-node] | `compute:system` | `compute:node` | `0..*` | Node participates in, or is managed as part of, the system. Does not assert availability for workload execution or require one parent system per node. |
| [iri:has-cpu][has-cpu] | `compute:node` | `compute:cpu` | `0..*` | Node contains, provides, or is associated with a CPU Resource. Hidden or omitted targets do not establish that the node has no CPUs. |
| [iri:has-gpu][has-gpu] | `compute:node` | `compute:gpu` | `0..*` | Node contains, provides, or is associated with a GPU Resource. Omission alone does not establish zero accelerators. |

## Service hosting relation — 1

| Relation | Allowed source Resource Type | Required target Resource Type | Cardinality | Description and key restrictions |
|---|---|---|---|---|
| [iri:hosted-on][hosted-on] | `service:dtn` or `service:inference` | `compute:system` or `compute:node` | `0..*` | Hosting infrastructure for the service. Does not identify current routing, live replica placement, or a target currently serving requests. |

DTN technology, transfer protocols, and service endpoint attributes do not by
themselves advertise operations, establish configured mount access, or grant
caller authorization. Mount access is described by the pair in the storage
topology table above.

## Rules shared by all 25 operation relations

An operation relation targets an **operation entry point**, not the Resource,
Job, Task, file, location, or endpoint description returned by the operation.
Its `0..1` cardinality counts advertised entry points, not result objects.

- The adapter must implement the operation in the source's explicit context.
  Bind `resource_id` to that context. Topology and Resource Type hierarchy alone
  do not establish operation applicability.
- Eligibility is based on the exact types listed for each operation family;
  it is not automatically inherited by CPU, GPU, or other descendants.
- Follow the advertised `href`. Obtain methods, inputs, responses, errors, and
  security from the applicable deployed OpenAPI description. Do not construct
  URLs or infer HTTP methods from relation names.
- An advertised operation relation requires at least one applicable
  `service-desc` whose deployed OpenAPI has the matching canonical
  `x-iri-relation` binding. Do not add an IRI representation `profile` to the
  operation link or use HAL metadata to invent its method or request schema.
- Presence grants no permission and guarantees no successful invocation.
  Omission means not advertised in this representation, not universally
  unsupported. Do not automatically forward credentials to an unrelated origin
  named by a discovered link or descriptor.
- When `supported_endpoints` is present on a Resource, compute-operation links
  require `"compute"` and filesystem-operation links require `"filesystem"` in
  that array. Neither category implies any particular operation. The two
  storage-discovery relations have no such category requirement. This rule does
  not apply to Job representations.

See the [operation-affordance RFC][operation-rfc] for the common binding rules.

## Compute operation relations — 5

All five targets below are operation entry points. Each has cardinality `0..1`
per eligible source. Generic `compute`, nodes, CPUs, and GPUs are not eligible.

| Relation | Allowed source | Cardinality | Description and additional restrictions |
|---|---|---|---|
| [iri:submit-job][submit-job] | `compute:system` | `0..1` | Submit a job in the system's adapter context. `resource_id` is bound; advertise a concrete link. |
| [iri:query-jobs][query-jobs] | `compute:system` | `0..1` | Query job statuses in that system context. Concrete link; query criteria remain in the OpenAPI-defined request. |
| [iri:get-job][get-job] | `compute:system` or `Job` | `0..1` | Retrieve a selected job and its current status. Apply the selected-job binding rules below. |
| [iri:update-job][update-job] | `compute:system` or `Job` | `0..1` | Update a selected job. On a Job, the link may be withdrawn when the update is not applicable to its lifecycle state. |
| [iri:cancel-job][cancel-job] | `compute:system` or `Job` | `0..1` | Cancel a selected job. On a Job, the link may be withdrawn when cancellation is not applicable to its lifecycle state. |

**Selected-job binding:** for `get-job`, `update-job`, and `cancel-job`, a
compute-system source binds `resource_id` and may leave only `job_id` as a URI
template variable, with `templated: true`. A Job source binds **both** identifiers
and must advertise a concrete URI. A client cannot infer the compute-system
context from `job_id`, and expanding a template grants no permission over an
arbitrary job. A Job's `get-job` link may cease to be advertised when its
operation context is no longer retained or visibility changes.

## Filesystem operation relations — 18

**Allowed source types for every row:** exactly `compute`, `compute:system`,
`compute:node`, `storage`, `storage:filesystem`, `storage:mount`, or `service:dtn`.
`storage:system`, `storage:block`, `storage:object`, other services, CPUs, and
GPUs are not eligible.

**Required context for every row:** the adapter must establish the source's
filesystem namespace and one unambiguous execution/access context. Generic
compute/storage semantics must be known; a mount requires its own mount-specific
context; a DTN must itself be the adapter context. Neither mounts nor DTNs
inherit operations from related Resources. If one source cannot identify an
unambiguous context, expose separate Resources and registered topology links;
do not silently select a host or add an undocumented context selector.

**Target and invocation for every row:** an asynchronous operation entry point.
The current mappings use `POST` and return `TaskSubmitResponse`; monitor the
Task for the outcome. They do not synchronously return the requested content,
metadata, or proof of completion. Bind `resource_id` and advertise a concrete
link, except for the permitted upload query template below.

| Relation | Cardinality | Description and additional restrictions |
|---|---|---|
| [iri:change-file-mode][change-file-mode] | `0..1` | Request a file permission-mode change. |
| [iri:change-file-owner][change-file-owner] | `0..1` | Request a file ownership change. |
| [iri:identify-file][identify-file] | `0..1` | Identify the type of a file or directory. |
| [iri:stat-file][stat-file] | `0..1` | Request file metadata. |
| [iri:checksum-file][checksum-file] | `0..1` | Request a file checksum. |
| [iri:create-directory][create-directory] | `0..1` | Create a directory. |
| [iri:create-symlink][create-symlink] | `0..1` | Create a symbolic link. |
| [iri:list-directory][list-directory] | `0..1` | List directory entries. |
| [iri:read-file-head][read-file-head] | `0..1` | Read the beginning of a file. |
| [iri:read-file-tail][read-file-tail] | `0..1` | Read the end of a file. |
| [iri:view-file][view-file] | `0..1` | Request file content asynchronously. Not a direct-content link or a `GET` file operation. |
| [iri:copy-path][copy-path] | `0..1` | Copy a file or directory path. |
| [iri:download-file][download-file] | `0..1` | Request asynchronous download work. Do not treat the link as a direct download, binary stream, redirect, or inferred `GET`. |
| [iri:upload-file][upload-file] | `0..1` | Submit a multipart file upload. Required query parameter `path` may be bound or exposed as `{?path}` with `templated: true`; no other variable may remain unresolved. Preserve binding and encoding during expansion. |
| [iri:remove-path][remove-path] | `0..1` | Request destructive removal. Requires an explicit invocation under caller policy; discovery or traversal must not execute it. |
| [iri:compress-paths][compress-paths] | `0..1` | Compress paths into an archive. |
| [iri:extract-archive][extract-archive] | `0..1` | Extract an archive. |
| [iri:move-path][move-path] | `0..1` | Move or rename a path. |

## Storage discovery operation relations — 2

Both targets are discovery operation entry points. Both current mappings use
`GET`; bind `resource_id` to the source's adapter context and advertise a
concrete link. Optional query filters are supplied according to OpenAPI.
Discovery results do not establish configured topology, authorization to use a
location or endpoint, health, or successful future access.

| Relation | Allowed source Resource Types | Cardinality | Description and additional restrictions |
|---|---|---|---|
| [iri:resolve-storage-locations][resolve-storage-locations] | Exactly `compute`, `compute:system`, `compute:node`, `storage`, `storage:system`, `storage:filesystem`, `storage:mount`, `storage:block`, `storage:object`, or `service:dtn` | `0..1` | Resolve user-context `StorageInstance` entries. Optional filters: `logicalpath`, `project`, `allocation`, `intent`. The adapter must support the particular source and its response semantics; see the context conditions below. |
| [iri:get-storage-access-endpoints][get-storage-access-endpoints] | Exactly `storage`, `storage:system`, `storage:filesystem`, `storage:block`, or `storage:object` | `0..1` | Retrieve `AccessEndpoint` descriptions. Optional filters: `protocol`, `endpoint_id`. Requires implemented discovery; generic storage semantics must be known and filesystem identifiers/path context explicitly supported. Mounts, compute Resources, and services are not eligible. Does not execute a transfer or protocol request. |

**Location-resolution context conditions:** generic `compute`/`storage` require
known, unambiguous adapter semantics; a compute system requires implementation
in that configured system context; a node requires explicit node configuration;
a filesystem requires accepted identifiers and a defined path/resolution
context; a mount requires explicit mount-specific support; a DTN must itself
be the adapter context. Storage systems, block storage, and object storage
require the existing `StorageInstance` response semantics to apply to them.
Classification, hosting, and mount-access links alone do not establish
eligibility. Ambiguous contexts require separate Resources rather than an
implicit host choice or undocumented selector.

The number of returned locations or endpoint descriptions is independent of
the discovery link's `0..1` cardinality. Returned `AccessEndpoint.capabilities`
describe supported operations; they do not grant permission or advertise
protocol-invocation links.

## Standard links and HAL CURIE declarations

These standard relations do not use the `iri:` prefix. Their IRI mappings and
requirements are defined by the [HAL links RFC][hal-rfc].

| Link | Source/context | Target | Cardinality or presence rule | Description and restrictions |
|---|---|---|---|---|
| `self` | Representation with canonical identity | Its canonical representation URI | `1` | Required on HAL representations with canonical identity; agrees with `self_uri` when retained. A transient `TaskSubmitResponse` has no such requirement. |
| `help` | `Facility` mapping | Help/support portal | `0..1` | Maps optional, nullable `support_uri`; omit when absent/null. |
| `monitor` | `TaskSubmitResponse` mapping | `Task` | `1` | Maps required `task_uri` to the Task used to monitor the asynchronous result. |
| `service-desc` | Applicable representation/context | Machine-readable deployed service description, usually OpenAPI | At least `1` when an operation relation is advertised; otherwise recommended by the HAL RFC, with no fixed maximum specified | Must describe the applicable deployment. The canonical IRI OpenAPI is appropriate only if it accurately describes that deployment. Grants no authorization. |

`curies` is a HAL declaration array, not a separately registered IRI domain
relation. It is optional; when the `iri:` abbreviation is used, declare its
mapping with `name: iri`, `href: https://iri.science/rels/{rel}`, and
`templated: true`. Canonical IRI relation URIs use
`https://iri.science/rels/<relation-name>`. Neither Resource Type URNs nor target
profile URIs replace these relation identifiers.

## Authoritative references

- [Complete IRI Link Relation Index][relation-index]
- [HAL links RFC][hal-rfc]
- [Resource operation-affordance RFC][operation-rfc]
- [IRI v2 OpenAPI][openapi]
- [Resource Type URN Registry][resource-types]
- [Hypermedia and Discovery](hypermedia-and-discovery.md)

[relation-index]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/README.md
[hal-rfc]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-hal-links.md
[operation-rfc]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/rfc/rfc-resource-operation-affordances.md
[openapi]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/all_spec_v2.yaml
[resource-types]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/urns/resource-types.md
[located-at]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/located-at.md
[has-site]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-site.md
[has-resource]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-resource.md
[generated-by]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/generated-by.md
[has-event]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-event.md
[impacts]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/impacts.md
[may-impact]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/may-impact.md
[has-project]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-project.md
[has-capability]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-capability.md
[has-project-allocation]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-project-allocation.md
[provides-filesystem]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/provides-filesystem.md
[provides-block]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/provides-block.md
[provides-object]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/provides-object.md
[has-mount]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-mount.md
[mounted-on]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/mounted-on.md
[attached-to]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/attached-to.md
[has-node]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-node.md
[has-cpu]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-cpu.md
[has-gpu]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/has-gpu.md
[hosted-on]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/hosted-on.md
[accesses-mount]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/accesses-mount.md
[accessed-by]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/accessed-by.md
[submit-job]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/submit-job.md
[query-jobs]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/query-jobs.md
[get-job]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/get-job.md
[update-job]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/update-job.md
[cancel-job]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/cancel-job.md
[change-file-mode]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/change-file-mode.md
[change-file-owner]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/change-file-owner.md
[identify-file]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/identify-file.md
[stat-file]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/stat-file.md
[checksum-file]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/checksum-file.md
[create-directory]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/create-directory.md
[create-symlink]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/create-symlink.md
[list-directory]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/list-directory.md
[read-file-head]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/read-file-head.md
[read-file-tail]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/read-file-tail.md
[view-file]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/view-file.md
[copy-path]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/copy-path.md
[download-file]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/download-file.md
[upload-file]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/upload-file.md
[remove-path]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/remove-path.md
[compress-paths]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/compress-paths.md
[extract-archive]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/extract-archive.md
[move-path]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/move-path.md
[resolve-storage-locations]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/resolve-storage-locations.md
[get-storage-access-endpoints]: https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/rels/get-storage-access-endpoints.md
