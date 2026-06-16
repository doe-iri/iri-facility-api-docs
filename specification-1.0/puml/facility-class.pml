/**
  * This is the UML description for the IRI Facility class version 1 circa 2025.
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

class Facility {
  A specialized research facility funded and operated by the U.S. Department
  of Energy that provides unique scientific tools, expertise, and
  infrastructure for researchers from across academia, industry, and government.
  In a more general definition, a Facility offers Resources to scientific
  workflows for programmatic consumption.
---
  + short_name <b>: String [0..1]</b>
  + organization_name <b>: String</b>
  + support_uri <b>: Uri [0..1]</b>
  + site_uris <b>: Uri[] [0..1]</b>
  + location_uris <b>: Uri[] [0..1]</b>
  + resource_uris <b>: Uri[] [0..1]</b>
  + event_uris <b>: Uri[] [0..1]</b>
  + incident_uris <b>: Uri[] [0..1]</b>
  + capability_uris <b>: Uri[] [0..1]</b>
  + project_uris <b>: Uri[] [0..1]</b>
  + project_allocation_uris <b>: Uri[] [0..1]</b>
  + user_allocation_uris <b>: Uri[] [0..1]</b>
}

NamedObject <|-- Facility

@enduml