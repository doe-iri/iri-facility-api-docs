---
layout: default
title: Idempotency-Key and Job Retries
parent: IRI 2.0
nav_order: 6
permalink: /idempotency/
---

# Idempotency-Key and Job Retries

The Python reference implementation accepts an optional `Idempotency-Key`
request header for job submission and update. With a backing store configured,
it remembers a successful response and can return that response when a client
retries the same operation. This reduces the risk of submitting or updating a
job twice after a client timeout.

This page describes the [Python reference implementation at revision
`7867e74`](https://github.com/doe-iri/iri-facility-api-python/tree/7867e74b351458a4a5277225d708bb6770d37d89)
and the [demo adapter stores at revision
`e707cf4`](https://github.com/doe-iri/iri-facility-api-demo-adapter/tree/e707cf4aacdd25955f985f7d2c85d1eb9a5c8d23).
It is implementation guidance. The [checked-in IRI v2 compute
OpenAPI](https://github.com/doe-iri/iri-facility-api-docs/blob/main/specification-v2/openapi/production/compute.yaml)
does not declare this header. Confirm support and retention policy in the
facility's deployed API description and documentation before relying on it.
An advertised job operation alone does not establish idempotency support.

## Supported operations

| Python handler | HTTP operation in the current v2 contract | OpenAPI operation ID | Discovery relation |
|---|---|---|---|
| `submit_job` | `POST /api/v2/compute/job/{resource_id}` | `launchJob` | [`iri:submit-job`](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/relations/submit-job.md) |
| `update_job` | `PUT /api/v2/compute/job/{resource_id}/{job_id}` | `updateJob` | [`iri:update-job`](https://github.com/doe-iri/iri-facility-api-docs/blob/main/registry/relations/update-job.md) |

These paths identify the current contract mappings. Use the advertised
operation URL and the deployed OpenAPI method and request schema, as explained
in [Hypermedia and Discovery](hypermedia-and-discovery.md). Idempotency does
not change which callers, job states, or fields a facility allows for updates.

## Request and response behavior

For an authenticated, valid request whose resource lookup succeeds, the
reference implementation behaves as follows. The conflict and replay behavior
assumes a backing store implementing the reference store contract.

| Scenario | Result |
|---|---|
| Header omitted | Execute the adapter normally on every request; no `Idempotency-Key-Reply` header. |
| Non-empty header supplied, but no store configured | Return `501`; do not invoke the job submission or update handler. |
| Key not yet recorded | Acquire a lock and invoke the adapter. On success, store the Job response with status `200` and return `Idempotency-Key-Reply: miss`. |
| Completed key reused with a matching request body | Return the cached `200` response with `Idempotency-Key-Reply: hit`; do not invoke the job submission or update handler again. |
| Completed key reused with a different request body | Return `422`. |
| Key reused while its lock is still active | Return `409`. The demo stores do this even if the second request body differs. |
| Adapter raises an exception | Attempt to release the lock and propagate the error through the API's error handler; do not cache the error response. |

An empty raw header value also bypasses idempotency in this revision. Always
send a non-empty key when requesting retry protection.

The API returns errors as `application/problem+json`. Although the
[idempotency helper](https://github.com/doe-iri/iri-facility-api-python/blob/7867e74b351458a4a5277225d708bb6770d37d89/app/idempotency.py)
sets `Retry-After: 2` on its `409` exception, the installed
[HTTP error handler](https://github.com/doe-iri/iri-facility-api-python/blob/7867e74b351458a4a5277225d708bb6770d37d89/app/routers/error_handlers.py)
does not forward that header. Clients should handle `409` without a
`Retry-After` header in this revision.

A replay returns the original Job response snapshot. It does not refresh job
status. Use the advertised `iri:get-job` operation when you need current job
information. Authentication, request validation, and resource lookup still
occur before a cached response can be returned.

## Keys and request identity

Generate a fresh UUID for each logical submission or update, and preserve it
across retries of that operation. Send it as a quoted string, for example:

```http
Idempotency-Key: "8e03978e-40d5-43e8-bc93-6894a57f9324"
```

The current implementation uses the raw header value as the key. Quoted and
unquoted forms are different keys, so retain exactly the same header value on
every retry.

The cache key includes the authenticated user ID and the operation. For
updates it also includes the job ID. **It does not include the resource ID.**
Reusing a submission key on another resource can therefore replay the first
resource's response. Updates to identical job IDs on different resources can
also collide. Generate a new key for every distinct operation, including
operations on different resources, and keep the target URL and authenticated
user fixed across retries.

The body fingerprint is a SHA-256 hash of the parsed `JobSpec` model serialized
as JSON with sorted object keys. It compares parsed field values rather than
the original JSON bytes: whitespace and object-key order do not distinguish
requests. Other request headers are not part of this fingerprint. Preserve
the payload and request context when retrying.

## Retrying a job operation

1. Confirm that the deployment supports the header and establish its retention
   period. Generate a key before sending the first request.
2. If the request times out, retain the same operation URL, method, key, user,
   and payload when retrying within that period.
3. On `409`, wait before retrying the same request. Honor `Retry-After` when
   present; otherwise use bounded backoff. Avoid sending a continuous stream
   of concurrent retries.
4. On `422`, check whether the key was reused for a different request. A
   deliberate new operation needs a fresh key. Do not change the key merely
   to bypass a conflict when the original operation's outcome is uncertain.
5. On `501`, resolve the deployment's support or configuration before retrying
   with idempotency protection. Dropping the header executes the operation
   without this protection.
6. For other errors, follow the facility's recovery guidance. An error or
   expired cache entry does not establish that no scheduler action occurred.

### Submit example

Assume `SUBMIT_URL` contains the trusted operation URL advertised through
`iri:submit-job`, and `ACCESS_TOKEN` contains credentials for that facility.
The example assumes a deployment with idempotency enabled. Save this valid
`JobSpec` as `job-spec.json`:

```json
{
  "executable": "/bin/echo",
  "arguments": ["hello"]
}
```

Choose your own UUID for a new submission. For this illustrative request:

```bash
IDEMPOTENCY_KEY='"8e03978e-40d5-43e8-bc93-6894a57f9324"'
curl --include --request POST "$SUBMIT_URL" \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: $IDEMPOTENCY_KEY" \
  --data-binary @job-spec.json
```

Include any additional project or account context required by the facility.
If the request times out, repeat the same command with the same variables and
file. The first successful execution reports `miss`; a completed matching
retry reports `hit` and returns the original Job response.

### Update example

Assume `UPDATE_URL` contains the trusted, concrete operation URL for the
selected job, obtained from `iri:update-job`. Resolve a templated job ID
according to the advertised link and deployed contract when necessary.
For a facility that permits changing the job name in its current state,
save this `JobSpec` as `job-update.json`:

```json
{
  "name": "analysis-run"
}
```

Use a new key for this logical update:

```bash
IDEMPOTENCY_KEY='"5a9b8bf0-6754-4e10-bc0f-c9d1ab1d258b"'
curl --include --request PUT "$UPDATE_URL" \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --header 'Content-Type: application/json' \
  --header "Idempotency-Key: $IDEMPOTENCY_KEY" \
  --data-binary @job-update.json
```

Retry this update with its own unchanged key and payload. A later, intentional
update is a new operation and needs a new key.

## Facility configuration

The core Python library supplies the store interface and request handling,
but no backing store. Set `IRI_IDEMPOTENCY_STORE` to an importable class
implementing `IdempotencyStore`. An unset value disables idempotency.

The [demo adapter package](https://github.com/doe-iri/iri-facility-api-demo-adapter)
provides two reference stores. Install that package in the server environment
before selecting either class.

| Store | `IRI_IDEMPOTENCY_STORE` | Deployment use |
|---|---|---|
| In-memory | `demo_adapter.compute.idempotency.InMemoryIdempotencyStore` | Single-process development or demo. State is lost on restart and is not shared across workers or replicas. |
| Redis | `demo_adapter.compute.idempotency.RedisIdempotencyStore` | Shared state across workers or replicas using the same Redis service; also requires `REDIS_URL`. |

For a local Redis deployment, set these variables before starting the server:

```bash
export IRI_IDEMPOTENCY_STORE=demo_adapter.compute.idempotency.RedisIdempotencyStore
export REDIS_URL=redis://localhost:6379
export IDEMPOTENCY_TTL_SECONDS=86400
export LOCK_TTL_SECONDS=60
```

The localhost URL is illustrative; use the connection configuration appropriate
to your deployment. The reference stores use these defaults:

| Setting | Default | Meaning |
|---|---|---|
| `IRI_IDEMPOTENCY_STORE` | Unset | Store class; a non-empty key receives `501` when no store is configured. |
| `REDIS_URL` | Unset | Required connection URL when selecting the Redis store. |
| `IDEMPOTENCY_TTL_SECONDS` | `86400` | Retain a successful response for 24 hours after storing it. Cache hits do not renew the period. |
| `LOCK_TTL_SECONDS` | `60` | Expire an in-flight lock 60 seconds after acquisition. |

Publish the deployment's actual retention and recovery policy for clients.
Custom stores may have different configuration and retention behavior.

## Retention and failure limits

After a cached result expires or is lost, a retry is treated as a new request
and may call the adapter again. Set the lock duration to cover the expected
scheduler call duration: the reference stores do not renew an active lock.
If a scheduler call outlasts the lock, a retry can begin another execution
while the first is still running.

A scheduler can accept a submission before the API stores its response. A
process crash, adapter exception, or store failure in that interval can leave
the client uncertain while a job already exists. Releasing or expiring a lock
does not undo scheduler effects. Reconcile uncertain outcomes using the
facility's job-query and recovery procedures before initiating a new operation.

The header provides response replay while the relevant store state is retained.
It does not guarantee exactly-once execution across all failures.

## Relationship to the IETF draft

The [IETF Idempotency-Key draft,
revision 07](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-07)
is a work-in-progress reference, not an adopted IRI requirement. The Python
implementation follows the core pattern of response replay, `409` for an
outstanding request, and `422` for a completed key with a different payload.
There are differences to consider when assessing draft conformance:

- [Section 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-07#section-2.1)
  defines a Structured Fields string. This implementation neither parses that
  syntax nor validates UUIDs; it uses the raw header value. The examples above
  use the draft's quoted-string form.
- [Section 2.6](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-07#section-2.6)
  recommends replaying completed operation results, including errors. This
  implementation caches successful `200` responses and releases the lock on
  adapter exceptions instead of retaining an error response.

The `Idempotency-Key-Reply` response header is an implementation diagnostic;
the cited draft does not define it. Header absence is allowed here because
idempotency is optional; the draft's missing-key error guidance applies to
operations that require the header.

## Implementation references

- [Python compute handlers](https://github.com/doe-iri/iri-facility-api-python/blob/7867e74b351458a4a5277225d708bb6770d37d89/app/routers/compute/compute.py)
- [Python idempotency interface and helper](https://github.com/doe-iri/iri-facility-api-python/blob/7867e74b351458a4a5277225d708bb6770d37d89/app/idempotency.py)
- [Python HTTP error handling](https://github.com/doe-iri/iri-facility-api-python/blob/7867e74b351458a4a5277225d708bb6770d37d89/app/routers/error_handlers.py)
- [Demo adapter store implementations](https://github.com/doe-iri/iri-facility-api-demo-adapter/blob/e707cf4aacdd25955f985f7d2c85d1eb9a5c8d23/demo_adapter/compute/idempotency.py)
- [Demo adapter idempotency tests](https://github.com/doe-iri/iri-facility-api-demo-adapter/blob/e707cf4aacdd25955f985f7d2c85d1eb9a5c8d23/test/test_idempotency.py)
