# Decision 0006: Align the job-submission operation ID with submit terminology

**Status:** Accepted

**Date:** 2026-09-10

**Scope:** IRI v2 compute job-submission operation naming

> **Non-normative:** This record explains architectural rationale. The checked-out OpenAPI, HAL RFC, and link-relation registry remain authoritative until the planned contract change is approved and implemented.

## Context

The registered operation-affordance relation is `iri:submit-job`, and the current `POST /api/v2/compute/job/{resource_id}` summary and semantics describe submitting a job. The checked-out IRI v2 OpenAPI contract identifies that operation as `launchJob`.

Although an OpenAPI `operationId` is not an HTTP method, path, or representation field, client and server generators commonly use it to create method names. Retaining different verbs for the relation and operation identifier creates avoidable terminology drift, while renaming the relation would change a registered hypermedia identifier exposed in representations.

## Decision

Retain `iri:submit-job` as the DOE-IRI link relation and `https://iri.science/rels/submit-job` as its canonical relation URI.

In a separately approved IRI v2 OpenAPI contract revision, rename the `operationId` for `POST /api/v2/compute/job/{resource_id}` from `launchJob` to `submitJob`.

The migration changes only the OpenAPI operation identifier. It does not change the HTTP method or path, `JobSpec` request, `Job` response, errors, security requirements, job-submission semantics, or link-relation identity.

Until that OpenAPI revision is adopted, `launchJob` remains the authoritative current `operationId`, and documentation describing the current contract should continue to report it accurately.

## Rationale

`submit` is the established term in the relation registry, OpenAPI operation summary, API description, and job-processing domain. Aligning the OpenAPI identifier with that terminology makes mappings between hypermedia discovery, generated client methods, documentation, and implementation code easier to understand.

Changing the OpenAPI metadata is preferable to changing the registered relation because the relation is part of the representation vocabulary used for runtime discovery. The relation and the `operationId` still serve different roles: the relation explains why an operation target is linked, while OpenAPI defines how that operation is invoked.

## Consequences and tradeoffs

The eventual OpenAPI revision may be source-incompatible for generated clients and server stubs that expose a method named from `launchJob`. The contract release must therefore document the rename and coordinate regeneration or compatibility handling for affected SDKs, implementations, tests, and examples.

OpenAPI permits only one `operationId` for an operation, so the contract cannot expose `launchJob` and `submitJob` as simultaneous aliases on the same operation. Deployed descriptions and older contract versions may continue to report `launchJob`; clients must use the applicable deployed or versioned OpenAPI description rather than assuming the new identifier is already present.

Implementation should update the authoritative OpenAPI source and regenerate consolidated artifacts through the repository workflow. Historical verification results remain historical records and are not rewritten.

This decision does not authorize unrelated changes to job submission, routing, payloads, authentication, authorization, idempotency, or lifecycle behavior.

## Normative and current sources

- `specification-v2/openapi/production/compute.yaml`
- `specification-v2/openapi/all_spec_v2.yaml`
- `registry/relations/submit-job.md`
- `registry/relations/README.md`
- `rfc/rfc-hal-links.md`

## Historical notes

This decision preserves the existing `iri:submit-job` relation after considering whether its name should instead follow the current `launchJob` operation identifier. No prior decision record is superseded.
