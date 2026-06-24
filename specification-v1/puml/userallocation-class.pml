/**
  * This is the UML description for the IRI UserAllocation class version 1 circa 2025.
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

AllocationEntry ..> "1   " AllocationUnit : unit

class UserAllocation {
  Defines a user's allocation in a project.
  This allocation is a piece of the project's
  allocation.
---
  + user_id <b>: String</b>
  + entries <b>: AllocationEntry[]</b>
  + project_allocation_uri <b>: Uri</b>
}

UserAllocation *-- "0..n   " AllocationEntry : "  entries"
NamedObject <|-- UserAllocation

@enduml