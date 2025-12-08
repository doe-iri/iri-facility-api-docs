/**
  * This is the UML description for the IRI Project class version 1 circa 2025.
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

class Project {
  A project and its list of users at a facility.
---
  + user_ids <b>: String[]</b>
}

NamedObject <|-- Project

@enduml