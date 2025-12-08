/**
 * This is the UML description for the IRI Allocation Model version 1 circa 2025.
 */
@startuml

skinparam class {
    BackgroundColor D0E2F2
    ArrowColor Black
    BorderColor Black
}

class Capability {
    Defines an aspect of a resource that can have
    an allocation. For example, Perlmutter nodes
    with GPUs. For some resources at a facility,
    this will be 1 to 1 with the resource. It is
    a way to subdivide a resource into allocatable
    sub-resources further.  The word "capability"
    is also known to users as something they need
    for a job to run. (eg. gpu)
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String</b>
  + description <b>: String</b>
  + last_modified <b>: DateTime</b>
  + units <b>: AllocationUnit[]</b>
}

Capability --> "      1" Capability : self_uri (self)

enum AllocationUnit {
  The allocation type will have an associated unit
  based on technology.  For example, compute is
  allocated based on node hours.
---
  node_hours,
  bytes,
  inodes
}

class AllocationEntry {
  Defines an allocation.
---
  + allocation <b>: Float</b>
  + usage <b>: Float</b>
  + unit <b>: AllocationUnit</b>
}

Capability ..> "0..n  " AllocationUnit : units
AllocationEntry ..> "1   " AllocationUnit : unit

class UserAllocation {
  Defines a user's allocation in a project.
  This allocation is a piece of the project's 
  allocation.
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String [0..1]</b>
  + description <b>: String [0..1]</b>
  + last_modified <b>: DateTime</b>
  + user_id <b>: String</b>
  + entries <b>: AllocationEntry[]</b>
  + project_allocation_uri <b>: Uri</b>
}

UserAllocation --> "      1" UserAllocation : self_uri (self)
UserAllocation *-- "0..n   " AllocationEntry : "  entries"

class Project {
  A project and its list of users at a facility.
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String</b>
  + description <b>: String</b>
  + last_modified <b>: DateTime</b>
  + user_ids <b>: String[]</b>
}

Project --> "      1" Project : self_uri (self)

class ProjectAllocation {
  Defines a project's allocation for a capability 
  (aka. repository).  This allocation is a piece of 
  the total allocation for the capability (eg. 5% 
  of the total node hours of Perlmutter GPU nodes).
  A project would at least have a one storage and job 
  repository at an HPC facility, maybe more than 1 of 
  each.
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String [0..1]</b>
  + description <b>: String [0..1]</b>
  + last_modified <b>: DateTime</b>
  + entries <b>: AllocationEntry[]</b>
  + project_uri <b>: Uri</b>
  + capability_uri <b>: Uri</b>
  + user_allocation_uris <b>: Uri[]</b>
}

ProjectAllocation --> "      1" ProjectAllocation : self_uri (self)
ProjectAllocation *-- "0..n   " AllocationEntry : "  entries"
ProjectAllocation --> "1   " Project : project_uri (hasProject)
ProjectAllocation --> "      0..n" UserAllocation : user_allocation_uris (hasUserAllocation)
ProjectAllocation --> "0..n   " Capability : capability_uri (hasCapability)
UserAllocation --> "1   " ProjectAllocation : project_allocation_uri (hasProjectAllocation)

@enduml
