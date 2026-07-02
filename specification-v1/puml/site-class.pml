/**
  * This is the UML description for the IRI Site class version 1 circa 2025.
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

class Site {
  A Site represents the physical and administrative
  context in which a Resource is deployed and operated.
  It is associated with a geographic or network location
  where one or more resources reside and serves as the
  anchor point for associating these resources with their
  broader infrastructure and organizational relationships.

  A Site is location of a resource that has an associated
  physical location and an operating organization.
---
  + short_name <b>: String [0..1]</b>
  + operating_organization <b>: String</b>
  + location_uri <b>: Uri [0..1]</b>
  + resource_uris <b>: Uri[] [0..n]</b>
}

NamedObject <|-- Site

@enduml