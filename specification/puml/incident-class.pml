/**
  * This is the UML description for the IRI Incident class version 1 circa 2025.
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

class Incident {
  An Incident groups Events in time and
  across Resources.
---
  + status <b>: StatusType</b>
  + type <b>: IncidentType</b>
  + start <b>: DateTime</b>
  + end : <b>: DateTime</b>
  + resolution <b>: ResolutionType</b>
  + resource_uris <b>: Uri[]</b>
  + event_uris <b>: Uri[]</b>
}

NamedObject <|-- Incident

enum IncidentType {
  Possible incident types.
  ---
    planned,
    unplanned,
    reservation
}

enum ResolutionType {
  The type of incident resolution.
  ---
    unresolved,
    cancelled,
    completed,
    extended,
    pending
}

enum StatusType {
  Possible status values for
  a resource.
  ---
	up,
	degraded,
	down,
	unknown
}

Incident ..> StatusType : status
Incident ..> ResolutionType : resolution
Incident ..> IncidentType : type

@enduml