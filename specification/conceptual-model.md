# 6. Conceptual Model
The IRI conceptual model is an ever expanding set of functionalities needed to provide users with access
to capabilities at the DoE User Facilities.  Initially targeting scientific workflows, and now expanded
to incorporate the needs of the American Science Cloud, the IRI conceptual model is the basis for 
development of programmatic interfaces into the DoE user facilities.  This section describes the 
conceptual model in its current state.

The IRI conceptual model currently consists of five interconnected models: Facility, Status, Allocation, 
Job, and Filesystem.  These classes serve as the foundational entities for describing physical 
infrastructure, service components, operational occurrences, administrative context, job 
distribution, and filesystem manipulation.

  - The <b>Facility model</b> defines the core structure for representing organizational information
(Facility, Resources, Sites, Locations) across the IRI distributed infrastructure.
  - The <b>Status model</b> defines
the core structure for representing operational information for a Facility (Incidents, Events, and impacted
Resources).
  - The <b>Allocation model</b> defines user and project allocations at a Facility allowing an
application to determine if, from an accounting perspective, can store data or run a job at a site
(UserAllocation, ProjectAllocation, Project, and Capability).
- The <b>Job model</b>
- The <b>Filesystem model</b>

Each class encapsulates key attributes and behaviors relevant to its domain. 

In addition to defining these object types, the model includes a set of well-defined relationships 
and cardinalities that govern how instances of these classes are interconnected. These relationships 
capture structural, functional, and temporal associations (e.g., a Resource belongs to a Site, an 
Event is part of an Incident, an Event impacts a Resource, a Facility is hosted at one or more Sites), 
enabling rich semantic navigation across the model. Cardinality constraints ensure precision in how 
many instances can or must participate in a given relationship, supporting both validation and query 
optimization.

## 6.1 NamedObject
The NamedObject is a foundational object class that defines a common set of descriptive and identifying
attributes shared by named object types (a named object is directly referencable through the API). It 
provides a consistent structure for naming, referencing, and describing objects across diverse facilities 
and systems. By standardizing these core properties, NamedObject ensures uniformity in how objects are 
identified, linked, and maintained within distributed infrastructures.

The NamedObject class has the following definition:

![NamedObject](./images/namedObject.png)
<div align="center"><b>Figure 1 - NamedObject class.</b></div>

The NamedObject class has the attribute definitions:

| Attribute | Type | Description | Required | Example                                                                                                                               |
| :---- | :---- | :---- |:---------|:--------------------------------------------------------------------------------------------------------------------------------------|
| id | String |The unique identifier for the object.  Typically a UUID or URN to provide global uniqueness across facilities. | yes      | 09a22593-2be8-46f6-ae54-2904b04e13a4                                                                                                  |
| self_uri | Uri | A “self” relationship link. | yes      | "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                   |
| name | String | The long name of the object. | no       | Lawrence Berkeley National Laboratory                                                                                                 |
| description | String | A description of the object. | no       | Lawrence Berkeley National Laboratory is charged with conducting unclassified research across a wide range of scientific disciplines. |
| last_modified | ISO 8601 standard with timezone offsets. | The date this object was last modified. | yes      | 2025-05-11T20:34:25.272Z                                                                                                              |

Any object that can be addressable directly through the API should inherit the attributes of this class.
The inheritance relationship is not shown in the remaining diagrams for simplicity, but the attributes
are included.

## 6.2 Facility Model
The Facility model (see Figure 1) defines the core structure for representing organizational information
across the IRI distributed infrastructure. It is composed of four primary classes of named objects:
Facility, Site, Location, and Resource.  Each class encapsulates key attributes and behaviors relevant 
to its domain. These classes serve as the foundational entities for describing physical infrastructure, 
service components, and administrative context.

![Facility Model](./images/facility-model.png)
<div align="center"><b>Figure 1 - Facility Model.</b></div>

These object definitions enable users and systems to traverse the Facility model dynamically, answering 
questions such as "Which resources of type xyx are hosted at this Facility?" or "Which resources are 
located at a specific site?"

The Facility model has a set of well-defined relationships and their cardinalities that allows
for navigation between objects based on relationship type.  The following table describes these
relationships.

| Source | Relationship | Destination | Description |
| :---- | :---- | :---- | :---- |
| Facility | hasLocation | Location | A Facility can be associated with one or more geographical Locations. |
| Facility | hostedAt | Site | A Facility can be hosted at one or more physical Sites. |
| Facility | hasResource | Resource | A Facility can host zero or more Resources. |
| Facility | self | Facility | A Facility has a reference to itself. |
| Resource | memberOf | Facility | A Resource is a member of one of more Facilities (allowing for a shared resource). |
| Resource | locatedAt | Site | A Resource is located at one Site. |
| Resource | dependsOn | Resource | A Resource can depend on zero or more Resources. |
| Resource | hasDependent | Resource | A Resource can have zero or more dependent Resources. |
| Resource | self | Resource | A Resource has a reference to itself. |
| Site | hasResource | Resource | A Site hosts zero or more Resources. |
| Site | locatedAt | Location | A Site is located at a geographic location. |
| Site | self | Site | A Site has a reference to itself. |
| Location | hasSite | Site | A Location can contain one or more Sites. |
| Location | self | Location | A Location has a reference to itself. |

## 6.2 Status Model
The Status model (see Figure 2) defines the core structure for representing operational information across 
the IRI distributed infrastructure. It is composed of three primary classes of named objects: Incident, 
Event, and Resource.  Each class encapsulates key attributes and behaviors relevant to the communication of
operational status. These classes serve as the foundational entities for describing a facility's operational 
impacts and administrative context on defined Resources.

![Status Model](./images/status-model.png)
<div align="center"><b>Figure 2 - Status Model.</b></div>

These object definitions enable users and systems to traverse the Status model dynamically, answering
questions such as "What incidents have affected this facility and which resources are impacted?", or 
"Which events were logged during a specific outage?”.

The Status model has a set of well-defined relationships and their cardinalities that allows
for navigation between objects based on relationship type.  The following table describes these
relationships.

| Source | Relationship | Destination | Description |
| :---- | :---- | :---- | :---- |
| Incident | hasEvent | Event | A Facility has one or more associated Events. |
| Incident | mayImpact | Resource | An Incident may impact one or more Resources. |
| Incident | self | Incident | An Incident has a reference to itself. |
| Event | generatedBy | Incident | An Event is generated by an Incident. |
| Event | impacts | Resource | An Event impacts a Resource. |
| Event | self | Event | An Event has a reference to itself. |
| Resource | impactedBy | Event | A Resource is impacted by zero or more Events. |
| Resource | hasIncident | Incident | A Resource is impacted by zero or more Incidents. |

## 6.3 Allocations Model

![Allocations Model](./images/allocation-model.png)
<div align="center"><b>Figure 4 - Allocation Model.</b></div>

## 6.4 Job Model

![Job Model](./images/job-model.png)
<div align="center"><b>Figure 5 - Job Model.</b></div>


## 6.5 Relationships

The Facility and Status model has a set of well-defined relationships and their cardinalities that allows
for navigation between objects based on relationship type.  The following table describes these
relationships.

| Source | Relationship | Destination | Description |
| :---- | :---- | :---- | :---- |
| Facility | hasLocation | Location | A Facility can be associated with one or more geographical Locations. |
| Facility | hostedAt | Site | A Facility can be hosted at one or more physical Sites. |
| Facility | hasIncident | Incident | A Facility can have zero or more Incidents. |
| Facility | hasEvent | Event | A Facility can have zero or more Events caused by Incidents. |
| Facility | hasResource | Resource | A Facility can host zero or more Resources. |
| Facility | self | Facility | A Facility has a reference to itself. |
| Incident | hasEvent | Event | A Facility has one or more associated Events. |
| Incident | mayImpact | Resource | An Incident may impact one or more Resources. |
| Incident | self | Incident | An Incident has a reference to itself. |
| Event | generatedBy | Incident | An Event is generated by an Incident. |
| Event | impacts | Resource | An Event impacts a Resource. |
| Event | self | Event | An Event has a reference to itself. |
| Resource | impactedBy | Event | A Resource is impacted by zero or more Events. |
| Resource | hasIncident | Incident | A Resource is impacted by zero or more Incidents. |
| Resource | memberOf | Facility | A Resource is a member of one of more Facilities (allowing for a shared resource). |
| Resource | locatedAt | Site | A Resource is located at one Site. |
| Resource | dependsOn | Resource | A Resource can depend on zero or more Resources. |
| Resource | hasDependent | Resource | A Resource can have zero or more dependent Resources. |
| Resource | self | Resource | A Resource has a reference to itself. |
| Site | hasResource | Resource | A Site hosts zero or more Resources. |
| Site | locatedAt | Location | A Site is located at a geographic location. |
| Site | self | Site | A Site has a reference to itself. |
| Location | hasSite | Site | A Location can contain one or more Sites. |
| Location | self | Location | A Location has a reference to itself. |
