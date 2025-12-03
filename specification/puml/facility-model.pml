/**
 * This is the UML description for the IRI Facility Model version 1 circa 2025.
 */
@startuml

skinparam class {
  BackgroundColor D0E2F2
  ArrowColor Black
  BorderColor Black
}

class Facility {
  A specialized research facility funded and operated by the U.S. Department 
  of Energy that provides unique scientific tools, expertise, and
  infrastructure for researchers from across academia, industry, and government.
  In a more general definition, a Facility offers Resources to scientific
  workflows for programmatic consumption.
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String</b>
  + description <b>: String</b>
  + last_modified <b>: DateTime</b>
  + short_name <b>: String</b>
  + organization_name <b>: String</b>
  + support_uri <b>: Uri</b>
  + site_uris <b>: Uri[]</b>
  + location_uris <b>: Uri[]</b>
  + resource_uris <b>: Uri[]</b>
  + event_uris <b>: Uri[]</b>
  + incident_uris <b>: Uri[]</b>
  + capability_uris <b>: Uri[]</b>
  + project_uris <b>: Uri[]</b>
  + project_allocation_uris <b>: Uri[]</b>
  + user_allocation_uris <b>: Uri[]</b>
}

Facility --> "      1" Facility : self_uri (self)

class Resource {
  A Resource models a consumable resource, a
  consumable service, or dependent infrastructure
  services exposed to the end user.  A Resource
  has a reportable status, operational state, and
  capabilities.
---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String</b>
  + description <b>: String</b>
  + last_modified <b>: DateTime</b>
  + resource_type <b>: ResourceType</b>
  + group <b>: String</b>
  + current_status <b>: StatusType</b>
  + capability_uris <b>: Uri[]</b>
  + located_at_uri <b>: Uri</b>
  + member_of_uri <b>: Uri</b>
}

Resource --> "      1" Resource : self_uri (self)

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
Facility --> "1..*  "  Resource : resource_uris (hasResource)
Resource --> "1    " Facility : member_of_uri (memberOf)

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
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String</b>
  + description <b>: String</b>
  + last_modified <b>: DateTime</b>
  + short_name <b>: String</b>
  + operating_organization <b>: String</b>
  + location_uri <b>: Uri</b>
  + resource_uris <b>: Uri[]</b>
} 

Site --> "      1" Site : self_uri (self)
Facility --> "0..n    " Site : site_uris (hostedAt)
Resource --> "0..1    " Site : located_at_uri (locatedAt)

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
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String</b>
  + description <b>: String</b>
  + last_modified <b>: DateTime</b>
  + short_name <b>: String</b>
  + country_name <b>: String</b>
  + locality_name <b>: String</b>
  + state_or_province_name <b>: String</b>
  + street_address <b>: String</b>
  + unlocode <b>: String</b>
  + altitude <b>: Double</b>
  + latitude <b>: Double</b>
  + longitude <b>: Double</b>
  + site_uris <b>: Uri[]</b>
}

Location --> "      1" Location : self_uri (self)
Facility --> "0..n    " Location : location_uris (hasLocation)
Site --> "1   " Location : location_uri (hasLocation)
Location --> "1..n   " Site : site_uris (hasSite)
Site --> "0..n   " Resource : resource_uris (hasResource)

@enduml
