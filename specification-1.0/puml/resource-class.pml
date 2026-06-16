/**
  * This is the UML description for the IRI Resource class version 1 circa 2025.
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

class Resource {
  A Resource models a consumable resource, a
  consumable service, or dependent infrastructure
  services exposed to the end user.  A Resource
  has a reportable status, operational state, and
  capabilities.
---
  + resource_type <b>: ResourceType</b>
  + group <b>: String [0..1]</b>
  + current_status <b>: StatusType</b>
  + capability_uris <b>: Uri[] [0..1]</b>
  + located_at_uri <b>: Uri [0..1]</b>
  + member_of_uri <b>: Uri</b>
}

NamedObject <|-- Resource

enum ResourceType {
  The type of Resource.
---
    website,
    service,
    compute,
    system,
    storage,
    network,
    unknown
}

Resource ..> ResourceType : resource_type

enum StatusType {
  Possible status values for
  a resource.
---
    up,
    degraded,
    down,
    unknown
}

Resource ..> StatusType : current_status

@enduml