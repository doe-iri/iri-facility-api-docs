/**
  * This is the UML description for the IRI Capability class version 1 circa 2025.
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
  + units <b>: AllocationUnit[]</b>
  + resource_uri <b>: Uri</b>
}

NamedObject <|-- Capability

@enduml