
/**
 * This is the UML description for the IRI Facility Status Model version 1 circa 2025.
 */
@startuml

skinparam class {
  BackgroundColor D0E2F2
  ArrowColor Black
  BorderColor Black
}

class Incident {
  An Incident groups Events in time and 
  across Resources.
  ---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String [0..1]</b>
  + description <b>: String [0..1]</b>
  + last_modified <b>: DateTime</b>
  + status <b>: StatusType</b>
  + type <b>: IncidentType</b>
  + start <b>: DateTime</b>
  + end : <b>: DateTime</b>
  + resolution <b>: ResolutionType</b>
  + resource_uris <b>: Uri[]</b>
  + event_uris <b>: Uri[]</b>
}

Incident --> "      1" Incident : self_uri (self)

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

class Event {
  An Event defines a Resource-impacting event, 
  the resulting status of the impacted Resource,
  and the time the event occurred.
  ---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String [0..1]</b>
  + description <b>: String [0..1]</b>
  + last_modified <b>: DateTime</b>
  + status <b>: StatusType</b>
  + occurred_at <b>: DateTime</b>
  + resource_uri <b>: Uri</b>
  + incident_uri <b>: Uri</b>
}

Event --> "      1" Event : self_uri (self)
Event ..> StatusType : status

Event --> "  1" Incident : incident_uri (generatedBy)
Incident --> "0..*  " Event : event_uris (hasEvent)

class Resource {
  A Resource models a consumable resource, a 
  consumable service, or dependent infrastructure
  services exposed to the end user.  A Resource 
  has a reportable status, operational state, and 
  capabilities.
  ---
  + id <b>: String</b>
  + self_uri <b>: Uri</b>
  + name <b>: String [0..1]</b>
  + description <b>: String [0..1]</b>
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
Resource ..> StatusType : current_status

Event --> "1    " Resource : resource_uri (impacts)
Incident --> "0..*    " Resource : resource_uris (mayImpact)

class Facility {
  Reference to Facility model.
}

Resource --> "1    " Facility : member_of_uri (memberOf)

class Site {
  Reference to Facility model.
}

Resource --> "1    " Site : located_at_uri (locatedAt)

@enduml
