# DRAFT: Job Model (v1.0)

## Overview
This is the interface for programatic job submission. Users must be able to submit a job to a facility resource batch scheulder, query the status of jobs via the identifiers returned, and delete jobs as needed.  Users must be able to submit jobs that run as an unprivliged user on the given resource.  The endpoints are per-resource.

## Attributes

### Job
A `Job` is defined with the following attributes:

| Attribute       | Type           | Description                                                                    | Required | Example |
|-----------------|----------------|--------------------------------------------------------------------------------|----------|---------|
| `id`            | string         | Unique identifier (UUID).                                                      | yes      | `003e33cd-fa5e-43f8-8670-e4681c41559a` |
| `self_uri`      | URI            | Canonical hyperlink to this Event.                                             | yes      | `https|//iri.example.com/api/v1/status/jobs/003e33cd-fa5e-43f8-8670-e4681c41559a` |
| `name`          | string         | Long name/title of the Job.                                                    | yes      | `TestJob` |
| `description`   | string         | Human-readable description of the Job.                                         | no       | `TestJob is NEW` |
|`native_id` | string | The native system identifier for the job assigned from the underlying `Resource`. | No | `12345.system.fqdn.org` |
| `last_modified` | date-time      | Timestamp (ISO 8601) when this Job was last modified.                          | yes      | `2025-05-24T17|04|30.000Z` |
| `status`        | JobStatus    | Status of the job at the time of query.                                        | yes      | `QUEUED` |

### JobStatus
A `JobStatus` is defined with the following attributes:

| Attribute   | Type       | Description                          | Required | Example                       |
|--------------|------------|--------------------------------------|----------|-------------------------------|
| `state`      | JobState     | Current state of the job. | Yes      | `ACTIVE`                     |
| `time`   | Timestamp  | The last time the status was updated. | Yes       | `2023-10-01T12|34|56Z`        |
| `message` | string | Information about state transition. | Yes | `QUEUED to ACTIVE` | 
| `exit_code` | integer | Exit code for job from underlying workload manager.  Null if job has not exited | No | `137` | 
| metadata      | string       | Reference to the associated Job.     | Yes      | `987e6543-e21b-45d3-b123-426614174999` |

### JobSpec
A `JobSpec` is defined with the following attributes:

| Attribute   | Type       | Description                          | Required | Example                       |
|--------------|------------|--------------------------------------|----------|-------------------------------|
| `executable` | string | Name of an executable to run | No | `/scratch/MyProject/job.bin`|
| `arguments` | string | Argument list to pass to the executable. argv[1] will be the first element of htis list. | No | `-o output.txt -ppn 4` |
| `directory` | string | Directory to run executable from as it's working directory. | No | `/scratch/MyProject/run123` |
| `name` | string | Name of job for workload manager defaults. | No | `MyJob` |
| `inherit_environment` |boolean | If set to true, job has aceess to variables in the job's default execution environment.  Otherwise the job starts with a clean environment with only explicitly set variables. | No | `false` |
| `environment` | string | Variable names to set in environment with values. Should be a JSON object providing the mapping | No | `{"FOO": "bar"}` | 
| `stdin_path` | string | Path to file which will be passed to the job's standard input. | No | `/scratch/project/input.txt`| 
| `stdout_path` | string | Path to file which to place job's standard output. | No | `/scratch/project/output.txt`| 
| `stderr_path` | string | Path to file which to place job's standard error. | No | `/scratch/project/error.txt`| 
| `pre_launch` | string | Path to script to run before job is launched.  Only run on the head/service node of the job. | No | `/home/user/prelaunch.sh` |
| `post_launch` | string | Path to script to run after job is completed.  Only run on the head/service node of the job. | No | `/home/user/postlaunch.sh` | 
| `resources` | ResourceSpec | The resource spec object for the requested job. | No | `{"node_count": 4}` |
| `attributes` | JobAttributes | The attributes for the requested job. | No | `{"duration": 1440}` |


### ResourceSpec
A `ResourceSpec` is defined with the following attributes:

| Attribute   | Type       | Description                          | Required | Example                       |
|--------------|------------|--------------------------------------|----------|-------------------------------|
| `node_count` | integer | Count of nodes to allocate to this job. | No |`256` |
| `process_count`| integer | Number of processes to start for the job. | No | `4`|
| `processes_per_node`| integer | Count of processes to run on each node. | No | `4` |
| `cpu_cores_per_process`| integer | Request this many CPU cores for each process instance. | No | `64` |
| `gpu_cores_per_process`| integer | Request this many GPU cores for each process instance. | No |`8` |
| `exclusive_node_use`| Exclusively allocate node to job.  Defaults to False. | boolean | No |`true` |
| `memory`| integer | Total amount of memory requested for the job, in bytes. | No |  `2147483648` |


### JobAttributes
`JobAttributes` are defined with the following attributes:

| Attribute   | Type       | Description                          | Required | Example                       |
|--------------|------------|--------------------------------------|----------|-------------------------------|
| `duration` | integer | Time in seconds requested for job.  Jobs that exceed this time will be killed by the workload manager. | Yes | `86400` |
| `queue_name` | string | Queue to submit job to if backend supports multiple queues. | No | `prod` | 
| `account` |  string | Account identifier to use for time used by job. | Yes | `IRIProject` |
| `custom_attributes` | string | Custom attributes for resource-specific resource specificaiton. String should be valid JSON.  | No | `{filesystems| "home,scratch"}` |
| `reservation_id` | string | Advance reservation id if an advance reservation is in use. | No | `R12345` | 

## ENUM JobState

```yaml
        StatusType:
          type: string
          description: The genericized status of a job.
          enum:
          - NEW
          - QUEUED
          - ACTIVE
          - COMPLETED
          - FAILED
          - CANCELED
        example: QUEUED
```

## API Endpoints
### POST `/compute/job/{resource_id}`

Submit a job to the resource specified by `reosource_id`. This endpoint shall 
accept the following json:

```json
{
  "executable": "string",
  "arguments": [],
  "directory": "string",
  "name": "string",
  "inherit_environment": true,
  "environment": {},
  "stdin_path": "string",
  "stdout_path": "string",
  "stderr_path": "string",
  "resources": {
    "node_count": 0,
    "process_count": 0,
    "processes_per_node": 0,
    "cpu_cores_per_process": 0,
    "gpu_cores_per_process": 0,
    "exclusive_node_use": true,
    "memory": 0
  },
  "attributes": {
    "duration": "PT10M",
    "queue_name": "string",
    "account": "string",
    "reservation_id": "string",
    "custom_attributes": {}
  },
  "pre_launch": "string",
  "post_launch": "string",
  "launcher": "string"
}
```
The following responses shall be returned:

**Successful Response**
- Code: 200
- Media type: applicaiton/json

```json
{
  "id": "string",
  "status": {
    "state": 0,
    "time": 0,
    "message": "string",
    "exit_code": 0,
    "meta_data": {
      "additionalProp1": {}
    }
  }
}
```
Where the id is the `job_id` for the submitted item that can be used for status
retrieval and management of the submitted job to resource with `resource_id`.

**Validation Error**
- Code: 422
- Media type: applicaiton/json
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### GET `/compute/status/{resource_id}/{job_id}`

Get the status of a job, given the `job_id` on a given resource with `resource_id`.

The following responses shall be returned:
**Successful Response**
- Code: 200
- Media type: applicaiton/json
```json
{
  "id": "string",
  "status": {
    "state": 0,
    "time": 0,
    "message": "string",
    "exit_code": 0,
    "meta_data": {
      "additionalProp1": {}
    }
  }
}
```
**Validation Rrror**
- Code: 422
- Media type: applicaiton/json
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## POST `/compute/status/{resource_id}`
Get multiple job statuses filtered by a `JobSpec` JSON object
An integer `offset` and integer `limit` for limiting the response length should be supported.

The interface shall take a JSON job object as a filter.  The following is an example:
```json
{
  "additionalProp1": {}
}
```

The following responses shall be returned:
**Succesful Response**
- Code: 200
- Media Type: applicaiton/json
```json
[
  {
    "id": "string",
    "status": {
      "state": 0,
      "time": 0,
      "message": "string",
      "exit_code": 0,
      "meta_data": {
        "additionalProp1": {}
      }
    }
  }
]
```
**Validation Error**
- Code: 422
- Media Type: applicaiton/json
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## DELETE `/compute/cancel/{resource_id}/{job_id}`

Cancel the job specified by `job_id` on the resource specified by `resource_id`.
This must invoke termination and cleanup operations on a job.  This should
return immediately, with status queries used to determine ultimate success and
disposition of the subject job.

The following responses shall be returned:

**Succesful Response**
- Code: 200

**Validation Error**
- Code: 422
- Media Type: applicaiton/json
```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
