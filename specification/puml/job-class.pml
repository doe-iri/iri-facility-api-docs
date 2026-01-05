/**
 * This is the UML description for the IRI Job class version 1 circa 2025.
 */
@startuml

skinparam class {
    BackgroundColor D0E2F2
    ArrowColor Black
    BorderColor Black
}

class NamedObject {
  A parent class definition containing common
  properties for use in named objects.
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String [0..1]</b>
  + description <b>: String [0..1]</b>
  + last_modified <b>: DateTime</b>
}

NamedObject --> "      1" NamedObject : self_uri (self)

class Job {
  A class representing an abstract job which has a
  formal specification represented by a JobSpec  
  instance as well as a JobStatus, which indicates,  
  for example, whether the job is running or 
  completed.  When constructed, a job is in the NEW 
  state.
---
  + native_id <b>: String</b>
  + status <b>: JobStatus</b>
  + spec <b>: JobSpec [0..1]</b>
  + resource_uri <b>: URI</b>
}

NamedObject <|-- Job

class JobStatus {
  A class containing details about job transitions to new states.
---
  + state <b>: JobStateType</b>
  + time <b>: DateTime [0..1]</b>
  + message <b>: String [0..1]</b>
  + exit_code <b>: Integer [0..1]</b>
  + metadata <b>: Map<String, Object> [0..1]</b>
}

Job *-- "0..1  " JobStatus : "  status"

enum JobStateType {
   An enumeration of possible job states.
---
    NEW,
    QUEUED,
    ACTIVE, 
    COMPLETED
    FAILED,
    CANCELED
}

JobStatus ..> JobStateType : "  state"

class JobSpec {
  A class that describes the details of a job.
---
  + executable <b>: String [0..1]</b>
  + arguments <b>: String[] [0..1]</b>
  + directory <b>: String [0..1]</b>
  + name <b>: String [0..1]</b>
  + inherit_environment <b>: Boolean = true</b>
  + environment <b>: Map<String, String> [0..1]</b>
  + stdin_path <b>: String [0..1]</b>
  + stdout_path <b>: String [0..1]</b>
  + stderr_path <b>: String [0..1]</b>
  + resources <b>: ResourceSpec [0..1]</b>
  + attributes <b>: JobAttributes [0..1]</b>
  + pre_launch <b>: String [0..1]</b>
  + post_launch <b>: String [0..1]</b>
  + launcher <b>: String [0..1]</b>
}

Job *-- "0..1   " JobSpec : "  spec" 

class ResourceSpec {
  An abstract base class for all possible 
  resource specifications.
---
  + node_count <b>: Integer [0..1]</b>
  + process_count <b>: Integer [0..1]</b>
  + processes_per_node <b>: Integer [0..1]</b>
  + cpu_cores_per_process <b>: Integer [0..1]</b>
  + gpu_cores_per_process <b>: Integer [0..1]</b>
  + exclusive_node_use <b>: Boolean = false</b>
  + memory <b>: Integer [0..1]</b>
}

JobSpec *-- "0..1   " ResourceSpec : "  resources"

class JobAttributes {
  A class containing ancillary job information
  that describes how a job is to be run.
---
  + duration <b>: Duration = "PT10M"</b>
  + queue_name <b>: String [0..1]</b>
  + account <b>: String [0..1]</b>
  + reservation_id <b>: String [0..1]</b>
  + custom_attributes <b>: Map<String, String> [0..1]</b>
}

JobSpec *-- "0..1    " JobAttributes : "  attributes"

@enduml
