Justas Balcas:
### API name

Logical file name/directory normalization

### Summary

Anyone working across multiple HPC facilities faces inconsistent filesystem layouts at each HPC Facility. Home, scratch, and project directories may follow different naming conventions, mount points, quota policies, and performance characteristics. For example, a user's working directory might be located under /home/<user>, /users/<user>, /global/u/<user>, or /scratch/<project>/<user>. This requires everyone to maintain site-specific knowledge and scripts.
Need an API that answers this question: Given this user/project/allocation, and following intent, where should data be at this facility?


### Specification pull request

- [x] I confirm that a pull request with the detailed specification and proposal will be submitted as part of this process.

### Implementation commitment

- [x] I commit to providing a reference Python implementation and demo adapter expansion for the IRI API within a reasonable timeframe after the proposal is accepted.
- [ ] I am not able to provide a reference implementation at this time.

### Key capabilities, features, performance requirements, and interactions

API Example:
Examples of logical names: home, scratch, project, campaign, archive, shared, temporary

API Endpoints:
GET /storage/locations -> return a list of logical names (there is no requirement for all to be supported)
GET /storage/locations/{resource_id} - with possible parameters
  logicalpath - one of the logical names;
  project/allocation - path specific to project/allocation
  intent — optional (read/write, staging, long-term storage)


GET /storage/locations/RESID123?project=ABC123
{
  "logical_name": "scratch",
  "path": "/scratch/ABC123/jbalcas",
  "filesystem": "lustre-scratch",
  "performance_tier": "high",
  "quota_bytes": 5000000000000,
  "available_bytes": 4200000000000,
  "purge_policy_days": 30,
  "shared": false,
  "access": {
    "read": true,
    "write": true,
    "execute": true
  }
}


### Existing implementations

None

### Implementation level

Required for all facilities

### Why is this API needed?

user's working directory might be located under /home/<user>, /users/<user>, /global/u/<user>, or /scratch/<project>/<user>. This requires everyone to maintain site-specific knowledge and scripts.


### Alternatives considered, and why they were rejected

None

### Proposal authors / maintainers

@juztas 
------
@frobnitzem

Let's try answer the question: "If I want to upload my script, I need a way to know where to upload it, and where to access it from within a job."

- potentially multiple filesystems mounted to data transfer nodes (home, proj, scratch, etc.)
- same with xrootd: need to know where, with what permissions each filesystem is mounted
- compute: different set of filesystems accessible here (e.g. may not have write access to HOME within a job)

The proposal above is a reasonable short-term fix to support our current HPC systems.  I would add that we should see if we can merge the concept of "logical names" with "volumes", and then the API should answer the above question when posed as, "For a given resource, in a given state (in-job or out-of-job), what volumes mounts are made (volume / logical name):(mountpoint) and with what permissions?"

```
GET /storage/mounts/resource-id-123?project=ABC123
[ {
  # the basic mount info.
  "logical_name": "scratch", 
  "path": "/scratch/ABC123/jbalcas",
  "access": {
    "read": true,
    "write": true,
    "execute": true
  },
  "access-outside-of-job": {
    "read": true,
    "write": true,
    "execute": true
  },

  # extra info. FYI
  "filesystem": "lustre-scratch",
  "performance_tier": "high",
  "quota_bytes": 5000000000000,
  "available_bytes": 4200000000000,
  "purge_policy_days": 30,
  "shared": false,
  }
  ...
]
```

Ideally, we could run all user jobs in a container.  On HPC systems, this would actually help manage the many minor variations in system-level software (e.g. drivers, CUDA/ROCM versions, etc.) via the image name.

Then we can re-attach these volumes where we like as part of jobs:
```
[ {
  "logical_name": "scratch", 
  "path": "/scratch",
  "access": {
    "read": true,
    "write": falso,
    "execute": true
  }
} ]
```

However, we would still need an API like proposed here to know what set of volumes the system provides.
