# DRAFT: Job Model (v1.0)

This is the interface for programatic job submission. Users must be able to submit a job to a facility resource batch scheulder, query the status of jobs via the identifiers returned, and delete jobs as needed.  Users must be able to submit jobs that run as an unprivliged user on the given resource.  The endpoints are per-resource.


## API Endpoints
POST `/compute/job/{resource_id}`

Submit a job to the resource specified by `reosource_id`. This endpoint shall 
accept the following json:

```{
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
On successful submission the following shall be returned.
```
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
retrieval and management of the submitted job.

GET `/compute/status/{resource_id}/{job_id}`

POST `/compute/status/{resource_id}`

DELETE `/compute/cancel/{resource_id}/{job_id}`