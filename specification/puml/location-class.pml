/**
  * This is the UML description for the IRI Location class version 1 circa 2025.
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

class Location {
  A Location models the geographic, geopolitical, or
  spatial context associated with a Site that may
  contain zero or more Resources. It serves as a
  foundational concept for expressing where resources
  physically exist, are operated, or are logically
  grouped, enabling meaningful organization and
  visualization.  Locations are reusable entities that
  may be shared across multiple Sites or Facilities.
---
  + short_name <b>: String [0..1]</b>
  + country_name <b>: String [0..1]</b>
  + locality_name <b>: String [0..1]</b>
  + state_or_province_name <b>: String [0..1]</b>
  + street_address <b>: String [0..1]</b>
  + unlocode <b>: String [0..1]</b>
  + altitude <b>: Double [0..1]</b>
  + latitude <b>: Double [0..1]</b>
  + longitude <b>: Double [0..1]</b>
  + site_uris <b>: Uri[] [0..n]</b>
}

NamedObject <|-- Location

@enduml