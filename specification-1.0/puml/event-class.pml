/**
  * This is the UML description for the IRI Event class version 1 circa 2025.
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

enum StatusType {
  Possible status values for
  a resource.
  ---
	up,
	degraded,
	down,
	unknown
}

class Event {
  An Event defines a Resource-impacting event,
  the resulting status of the impacted Resource,
  and the time the event occurred.
---
  + status <b>: StatusType</b>
  + occurred_at <b>: DateTime</b>
  + resource_uri <b>: Uri</b>
  + incident_uri <b>: Uri</b>
}

Event ..> StatusType : status

NamedObject <|-- Event

@enduml