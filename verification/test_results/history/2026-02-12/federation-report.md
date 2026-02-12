# API Endpoints Report

**Generated at:** 2026-02-12 22:52 UTC

**Sites tested:** 127.0.0.1_8000

**Official endpoints defined in spec:** 25


## Spec Compliance (OperationId and API available at site from official spec)

| operationId | 127.0.0.1_8000 |
|---|---|
| GET /api/v1/account | ![][badge-missing] |
| GET /api/v1/account/capabilities | ![][badge-pass] |
| GET /api/v1/account/capabilities/{capability_id} | ![][badge-pass] |
| GET /api/v1/account/project_allocations | ![][badge-missing] |
| GET /api/v1/account/project_allocations/{project_allocation_id} | ![][badge-missing] |
| GET /api/v1/account/projects | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id} | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id} | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id}/user_allocations | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id}/user_allocations/{user_allocation_id} | ![][badge-pass] |
| GET /api/v1/account/user_allocations | ![][badge-missing] |
| GET /api/v1/account/user_allocations/{user_allocation_id} | ![][badge-missing] |
| GET /api/v1/facility | ![][badge-pass] |
| GET /api/v1/facility/sites | ![][badge-pass] |
| GET /api/v1/facility/sites/{site_id} | ![][badge-pass] |
| GET /api/v1/status/events | ![][badge-missing] |
| GET /api/v1/status/events/{event_id} | ![][badge-missing] |
| GET /api/v1/status/events/{event_id}/incident | ![][badge-missing] |
| GET /api/v1/status/events/{event_id}/resource | ![][badge-missing] |
| GET /api/v1/status/incidents | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id} | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id}/resources | ![][badge-missing] |
| GET /api/v1/status/resources | ![][badge-pass] |
| GET /api/v1/status/resources/{resource_id} | ![][badge-pass] |

## Official Spec Schemathesis Test

| operationId | 127.0.0.1_8000 |
|---|---|
| GET /api/v1/account | ![][badge-pass] |
| GET /api/v1/account/capabilities | ![][badge-pass] |
| GET /api/v1/account/capabilities/{capability_id} | ![][badge-pass] |
| GET /api/v1/account/project_allocations | ![][badge-pass] |
| GET /api/v1/account/project_allocations/{project_allocation_id} | ![][badge-pass] |
| GET /api/v1/account/projects | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id} | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id} | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id}/user_allocations | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id}/user_allocations/{user_allocation_id} | ![][badge-pass] |
| GET /api/v1/account/user_allocations | ![][badge-pass] |
| GET /api/v1/account/user_allocations/{user_allocation_id} | ![][badge-pass] |
| GET /api/v1/facility | ![][badge-pass] |
| GET /api/v1/facility/sites | ![][badge-pass] |
| GET /api/v1/facility/sites/{site_id} | ![][badge-pass] |
| GET /api/v1/status/events | ![][badge-pass] |
| GET /api/v1/status/events/{event_id} | ![][badge-pass] |
| GET /api/v1/status/events/{event_id}/incident | ![][badge-pass] |
| GET /api/v1/status/events/{event_id}/resource | ![][badge-pass] |
| GET /api/v1/status/incidents | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id} | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id}/resources | ![][badge-pass] |
| GET /api/v1/status/resources | ![][badge-pass] |
| GET /api/v1/status/resources/{resource_id} | ![][badge-pass] |

## Local Site Schemathesis Test


**Total endpoints discovered across local schemas:** 42

| operationId | 127.0.0.1_8000 |
|---|---|
| DELETE /api/v1/compute/cancel/{resource_id}/{job_id} | ![][badge-pass] |
| DELETE /api/v1/filesystem/rm/{resource_id} | ![][badge-pass] |
| GET /api/v1/account/capabilities | ![][badge-pass] |
| GET /api/v1/account/capabilities/{capability_id} | ![][badge-pass] |
| GET /api/v1/account/projects | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id} | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id} | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id}/user_allocations | ![][badge-pass] |
| GET /api/v1/account/projects/{project_id}/project_allocations/{project_allocation_id}/user_allocations/{user_allocation_id} | ![][badge-pass] |
| GET /api/v1/compute/status/{resource_id}/{job_id} | ![][badge-pass] |
| GET /api/v1/facility | ![][badge-pass] |
| GET /api/v1/facility/sites | ![][badge-pass] |
| GET /api/v1/facility/sites/{site_id} | ![][badge-pass] |
| GET /api/v1/filesystem/checksum/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/download/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/file/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/head/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/ls/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/stat/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/tail/{resource_id} | ![][badge-pass] |
| GET /api/v1/filesystem/view/{resource_id} | ![][badge-pass] |
| GET /api/v1/status/incidents | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id} | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id}/events | ![][badge-pass] |
| GET /api/v1/status/incidents/{incident_id}/events/{event_id} | ![][badge-pass] |
| GET /api/v1/status/resources | ![][badge-pass] |
| GET /api/v1/status/resources/{resource_id} | ![][badge-pass] |
| GET /api/v1/task | ![][badge-pass] |
| GET /api/v1/task/{task_id} | ![][badge-pass] |
| POST /api/v1/compute/job/{resource_id} | ![][badge-pass] |
| POST /api/v1/compute/status/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/compress/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/cp/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/extract/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/mkdir/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/mv/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/symlink/{resource_id} | ![][badge-pass] |
| POST /api/v1/filesystem/upload/{resource_id} | ![][badge-pass] |
| PUT /api/v1/compute/job/{resource_id}/{job_id} | ![][badge-pass] |
| PUT /api/v1/filesystem/chmod/{resource_id} | ![][badge-pass] |
| PUT /api/v1/filesystem/chown/{resource_id} | ![][badge-pass] |

---

<!-- Badge references -->
[badge-pass]: https://img.shields.io/badge/PASS-brightgreen
[badge-fail]: https://img.shields.io/badge/FAIL-red
[badge-missing]: https://img.shields.io/badge/MISSING-red
[badge-extra]: https://img.shields.io/badge/EXTRA-orange