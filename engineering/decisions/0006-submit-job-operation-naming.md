# Decision 0006: Keep the job-submission relation and operation ID distinct

**Status:** Accepted

**Date:** 2026-09-10

**Scope:** IRI v2 compute job-submission relation and operation naming

> **Non-normative:** This record explains architectural rationale. The checked-out OpenAPI, HAL RFC, and link-relation registry remain authoritative by concern.

## Context

The registered operation-affordance relation is `iri:submit-job`, and the current `POST /api/v2/compute/job/{resource_id}` summary and semantics describe submitting a job. The checked-out IRI v2 OpenAPI contract identifies that operation as `launchJob`.

Although an OpenAPI `operationId` is not an HTTP method, path, or representation field, client and server generators commonly use it to create method names. The relation and operation identifier use different verbs, but they also serve different roles: the relation identifies why an operation target is linked, while the OpenAPI Operation Object defines how that operation is invoked.

## Decision

Retain `iri:submit-job` as the DOE-IRI link relation and `https://iri.science/rels/submit-job` as its canonical relation URI.

`launchJob` remains the authoritative current `operationId` in the OpenAPI specification.

These identifiers remain distinct. Neither is renamed or treated as an alias for the other.

## Rationale

`submit` is the established term in the relation registry, OpenAPI operation summary, API description, and job-processing domain. The registered relation is part of the representation vocabulary used for runtime discovery, whereas `launchJob` identifies the corresponding Operation Object in the current structural contract.

Clients resolve the canonical relation URI to the applicable deployed OpenAPI Operation Object and use that object's method, parameters, request body, responses, and security requirements. Identifier spelling does not need to match across those layers because the relation URI, rather than the `operationId`, is the semantic binding key.

## Consequences and tradeoffs

Generated clients and server stubs may expose a method named from `launchJob`, as defined by the applicable IRI v2 OpenAPI description. Implementations and documentation should use that description rather than deriving a method name from `iri:submit-job`.

Hypermedia clients must not infer the OpenAPI `operationId`, HTTP method, path template, or payload contract from the relation name. They should follow `service-desc`, locate the Operation Object bound to the canonical relation URI, and apply that OpenAPI contract.

Keeping the identifiers distinct avoids changing the registered relation vocabulary or the generated-code surface of the current OpenAPI contract. Historical verification results remain historical records and are not rewritten.

This decision does not authorize unrelated changes to job submission, routing, payloads, authentication, authorization, idempotency, or lifecycle behavior.

## Normative and current sources

- `specification-v2/openapi/production/compute.yaml`
- `specification-v2/openapi/all_spec_v2.yaml`
- `registry/relations/submit-job.md`
- `registry/relations/README.md`
- `rfc/rfc-hal-links.md`

## Historical notes

This decision preserves the existing `iri:submit-job` relation after considering whether its name should instead follow the current `launchJob` operation identifier. No prior decision record is superseded.
