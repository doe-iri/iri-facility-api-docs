# Contents
**[6. Conceptual Model](#6-conceptual-model)**
- **[6.1 NamedObject](#61-namedobject)**
- **[6.2 Facility Model](#62-facility-model)**
  - **[6.2.1 Facility](#621-facility)**
  - **[6.2.2 Resource](#622-resource)**
  - **[6.2.3 Site](#623-site)**
  - **[6.2.4 Location](#624-location)**
  - **[6.2.5 Relationships](#625-relationships)**
- **[6.3 Status Model](#63-status-model)**
  - **[6.3.1 Incident](#631-incident)**
  - **[6.3.2 Event](#632-event)**
  - **[6.3.3 Resource](#633-resource)**
  - **[6.3.4 Relationships](#634-relationships)**
- **[6.4 Allocation Model](#64-allocation-model)**
  - **[6.4.1 Project](#641-project)**
  - **[6.4.2 ProjectAllocation](#642-projectallocation)**
  - **[6.4.3 UserAllocation](#643-userallocation)**
  - **[6.4.4 Capability](#644-capability)**
  - **[6.4.5 Resource](#645-resource)**
  - **[6.4.6 Relationships](#646-relationships)**
- **[6.5 Job Model](#65-job-model)**
- **[6.6 Filesystem](#66-filesystem-model)**

# 6. Conceptual Model
The IRI conceptual model is an ever expanding set of functionalities needed to provide users with access
to capabilities at the DoE User Facilities.  Initially targeting scientific workflows, and now expanded
to incorporate the needs of the American Science Cloud (AmSC), the IRI conceptual model is the basis for 
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
- The <b>Job model</b> defines Job related classes (Job, JobSpec, JobStatus) for specification and 
management of the invocation of application executables on exascale machines.  This specification is
based off of the [ExWorks PSI/J](https://exaworks.org/) job management model.
- The <b>Filesystem model</b> defines asynchronous file system access (ls, head, cp, etc.) on HPC
machines through the use of a Task class.  Individual files are not modelled as resources in this mode.
This specification is based off of the 
[FireCrest RESTful Services Gateway](https://firecrest.readthedocs.io/en/latest/) which provides a RESTful 
API for High-Performance Computing (HPC) systems, offering file system operations like listing files (ls), 
creating directories (mkdir), moving files (mv), and managing permissions (chmod, chown) via standard HTTP 
requests.

Each class defined on these models encapsulates key attributes and behaviors relevant to its domain. 

In addition to defining these object classes, the model includes a set of well-defined relationships 
and cardinalities that govern how instances of these classes are interconnected. These relationships 
capture structural, functional, and temporal associations (e.g., a Resource belongs to a Site, an 
Event is part of an Incident, an Event impacts a Resource, a Facility is hosted at one or more Sites), 
enabling rich semantic navigation across the model. Cardinality constraints ensure precision in how 
many instances can or must participate in a given relationship, supporting both validation and query 
optimization.

---

## 6.1 NamedObject
The NamedObject is a foundational object class that defines a common set of descriptive and identifying
attributes shared by named object types (a named object is directly referencable through the API). It 
provides a consistent structure for naming, referencing, and describing objects across diverse facilities 
and systems. By standardizing these core properties, NamedObject ensures uniformity in how objects are 
identified, linked, and maintained within distributed infrastructures.

The NamedObject class has the following definition:

<div align="center">
    <img src="./images/namedObject.png" alt="NamedObject" sizes="">
</div>
<div align="center"><b>Figure 6.1 - NamedObject class.</b></div>

## 6.1.1 Attributes
The NamedObject class has the attribute definitions:

| Attribute     | Type                                     | Description                                                                                                    | Required | Cardinality | Example                                                                                                                   |
|:--------------|:-----------------------------------------|:---------------------------------------------------------------------------------------------------------------|:---------|:------------|:--------------------------------------------------------------------------------------------------------------------------------------|
| id            | String                                   | The unique identifier for the object.  Typically a UUID or URN to provide global uniqueness across facilities. | yes      | 1           | 09a22593-2be8-46f6-ae54-2904b04e13a4                                                                                                  |
| self_uri      | Uri                                      | Canonical "self" hyperlink to this instance.                                                                   | yes      | 1           | "https://iri.example.com/api/v1/facility"                                                                                             |
| name          | String                                   | The long name of the object.                                                                                   | no       | 0..1        | Lawrence Berkeley National Laboratory                                                                                                 |
| description   | String                                   | A description of the object.                                                                                   | no       | 0..1        | Lawrence Berkeley National Laboratory is charged with conducting unclassified research across a wide range of scientific disciplines. |
| last_modified | ISO 8601 standard with timezone offsets. | The date this object was last modified.                                                                        | yes      | 1           | 2025-05-11T20:34:25.272Z |

Any object that can be addressable directly through the API should inherit the attributes of this class.
The inheritance relationship is not shown in the consolidated model diagrams for simplicity, but the 
attributes are included.

## 6.1.2 Relationships
The NamedObject has a well-defined canonical "self" relationship that allows for navigation to the instance 
of the NamedObject.

| Source       | Relationship | Destination  | Cardinality | Description                              |
|:-------------|:-------------|:-------------|:------------|:-----------------------------------------|
| NamedObject  | self         | NamedObject  | 1           | A NamedObject has a reference to itself. |

---

## 6.2 Facility Model
The Facility model (see Figure 1) defines the core structure for representing organizational information
across the IRI distributed infrastructure. It is composed of four primary classes of named objects:
`Facility`, `Site`, `Location`, and `Resource`.  Each class encapsulates key attributes and behaviors relevant 
to its domain. These classes serve as the foundational entities for describing physical infrastructure, 
service components, and administrative context.

<div align="center">
    <img src="./images/facility-model.png" alt="Facility Model" width="800" />
</div>
<div align="center"><b>Figure 6.2 - Facility Model.</b></div>

These object definitions enable users and systems to traverse the Facility model dynamically, answering 
questions such as "Which resources of type xyx are hosted at this Facility?" or "Which resources are 
located at a specific site?"

### 6.2.1 Facility
A specialized research facility funded and operated by the U.S. Department of Energy that provides 
unique scientific tools, expertise, and infrastructure for researchers from across academia, 
industry, and government. In a more general definition, a `Facility` offers `Resources` to scientific
workflows for programmatic consumption.

<div align="center">
    <img src="./images/facility-class.png" alt="Facility class" width="450" />
</div>
<div align="center"><b>Figure 6.2.1 - Facility class.</b></div>

The `Facility` class has the following attribute definitions:

| Attribute                 | Type     | Description                                                | Required | Cardinality | Example                                                                                             |
|:--------------------------|:---------|:-----------------------------------------------------------|:---------|:------------|-----------------------------------------------------------------------------------------------------|
| `id`                      | String   | Unique identifier (UUID) for the `Facility`.               | yes      | 1           | `09a22593-2be8-46f6-ae54-2904b04e13a4`                                                              |
| `self_uri`                | URI      | Canonical hyperlink to this `Facility`.                    | yes      | 1           | `https://iri.example.com/api/v1/facility`                                                           |
| `name`                    | String   | Long name of the `Facility`.                               | yes      | 0..1        | `National Energy Research Scientific Computing Center`                                              |
| `description`             | String   | Human‑readable description for this `Facility`.            | no       | 0..1        | `NERSC is the mission scientific computing facility for the U…`                                     |
| `last_modified`           | DateTime | Timestamp (ISO 8601) when this Facility was last modified. | yes      | 1           | `2025-10-15T01:00:50.000Z`                                                                          |
| `short_name`              | String   | Common/short name of the `Facility`.                       | no       | 0..1        | `NERSC`                                                                                             |
| `organization_name`       | String   | Operating organization’s name.                             | no       | 0..1        | `Lawrence Berkeley National Laboratory`                                                             |
| `support_uri`             | URI      | Link to `Facility` support portal.                         | no       | 0..1        | `https://help.nersc.gov/`                                                                           |
| `site_uris`               | URI[]    | URIs of associated `Sites` (hasSite).                      | no       | 0..*        | [`https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45`]              |
| `location_uris`           | URI[]    | URIs of associated `Locations` (hasLocation).              | no       | 0..*        | [`https://iri.example.com/api/v1/facility/locations/b1c7773f-4624-4787-b1e9-46e1c78c3320`]          |
| `resource_uris`           | URI[]    | URIs of contained `Resources` (hasResource).               | no       | 0..*        | [`https://iri.example.com/api/v1/status/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc`]            |
| `event_uris`              | URI[]    | URIs of `Events` in this Facility (hasEvent).              | no       | 0..*        | [`https://iri.example.com/api/v1/status/events/f9d6e700-1807-45bd-9a52-e81c32d40c5a`]               |
| `incident_uris`           | URI[]    | URIs of `Incidents` in this Facility (hasIncident).        | no       | 0..*        | [`https://iri.example.com/api/v1/status/incidents/686efb0a-0f85-4cc9-86a3-f5713ee6ea44`]            |
| `capability_uris`         | URI[]    | URIs of `Capability` offered by the Facility.              | no       | 0..*        | [`https://iri.example.com/api/v1/account/capabilities/9b930fc2-7840-47b2-9268-42362b6fe9ee`]        |
| `project_uris`            | URI[]    | URIs of `Projects` associated to this Facility.            | no       | 0..*        | [`https://iri.example.com/api/v1/account/projects/d6bdb597-8393-4747-8f90-6db08ae018ac`]            |
| `project_allocation_uris` | URI[]    | URIs of `ProjectAllocation`.                               | no       | 0..*        | [`https://iri.example.com/api/v1/account/project_allocations/46dcde57-e88a-49a9-bf7a-c2120cf5a86b`] |
| `user_allocation_uris`    | URI[]    | URIs of `UserAllocation`.                                  | no       | 0..*        | [`https://iri.example.com/api/v1/account/user_allocations/be91d9c1-99bc-47c1-aaa9-3ee82bb8a7d0`]    |

### 6.2.2 Resource
A `Resource` models a consumable resource, a consumable service, or dependent infrastructure
services exposed to the end user.  A `Resource` has a reportable status, operational state, and
capabilities.

<div align="center">
    <img src="./images/resource-class.png" alt="Resource class" width="400" />
</div>
<div align="center"><b>Figure 6.2.2 - Resource class.</b></div>

The `Resource` class has the following attribute definitions:

| Attribute            | Type         | Description                                                                                                                                                                                                        | Required | Cardinality | Example                                                                                                                                       |
|:---------------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                 | String       | The unique identifier for the `Resource`.  Typically a UUID or URN to provide global uniqueness across facilities.                                                                                                 | yes      | 1           | "09a22593-2be8-46f6-ae54-2904b04e13a4"                                                                                                        |
| `self_uri`           | URI          | A hyperlink reference (URI) to this `Resource` (self). Canonical hyperlink to this `Resource`.                                                                                                                                                            | yes      | 1           | "https://iri.example.com/api/v1/status/resources/09a22593-2be8-46f6-ae54-2904b04e13a4"                                                        |
| `name`               | String       | The long name of the `Resource`.                                                                                                                                                                                   | no       | 0..1        | "Data Transfer Nodes"                                                                                                                         |
| `description`        | String       | A description of the `Resource`.                                                                                                                                                                                   | no       | 0..1        | "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS." |
| `last_modified`      | DateTime     | The date this `Resource` was last modified.  ISO 8601 standard with timezone offsets.                                                                                                                              | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                                                                    |
| `resource_type`      | ResourceType | The type of `Resource` based on string ENUM values.                                                                                                                                                                | yes      | 1           | "compute"                                                                                                                                     |
| `group`              | String       | The member `Resource` group.                                                                                                                                                                                       | no       | 0..1        | "perlmutter" |
| `current_status`     | StatusType   | The current status of this `Resource` at time of query based on string ENUM values. If there is no last Event associated with the resource to indicate a current status, then currentStatus defaults to "unknown". | yes      | 1           | "up"                                                                                                                                          |
| `capability_uris`    | String[]     | Hyperlink references (URIs) to capabilities this `Resource` provides (hasCapability).                                                                                                                              | no       | 0..*        | ["https://iri.example.com/api/v1/account/capabilities/b1ce8cd1-e8b8-4f77-b2ab-152084c70281"]                                                  |
| `located_at_uri`     | URI          | A hyperlink reference (URI) to the `Site` containing this `Resource` (locatedAt).                                                                                                                                  | no       | 0..1        | "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                          |
| `member_of_uri`      | URI          | A hyperlink reference (URI) to `Facility` managing this `Resource` (memberOf).                                                                                                                                         | no       | 0..1        | "https://iri.example.com/api/v1/facility"                                                                                                     |

The `ResourceType` is an enumeration to identify the type of `Resource`.  This
is a broad classification and may not provide enough detail to make job
submission decisions.

| ENUM        | Description                           |
|:------------|:--------------------------------------|
| `website`   | This `Resource` is of type `website`. |
| `service`   | This `Resource` is of type `service`. |
| `compute`   | This `Resource` is of type `compute`. |
| `system`    | This `Resource` is of type `system`.  |
| `storage`   | This `Resource` is of type `storage`. |
| `network`   | This `Resource` is of type `network`. |
| `unknown`   | This `Resource` is of type `unknown`. |

The `StatusType` is an enumeration of the possible status values for a `Resource`.

| ENUM       | Description                                                                             |
|:-----------|:----------------------------------------------------------------------------------------|
| `up`       | The `Resource` is `up` and available for use.                                           |
| `degraded` | The `Resource` is `degraded` and although available, may not be providing full service. |
| `down`     | The `Resource` is `down` and unavailable for use.                                       |
| `unknown`  | The `Resource` is in an `unknown` state and should be considered unavailable.           |

### 6.2.3 Site
A `Site` represents the physical and administrative context in which a `Resource` is deployed and operated.
It is associated with a geographic or network location  where one or more resources reside and serves as the
anchor point for associating these resources with their broader infrastructure and organizational relationships.

A `Site` is a managed location that has an associated physical location and an operating organization.  A `Site`
can host zero or more `Resource`.

<div align="center">
    <img src="./images/site-class.png" alt="Site class" width="400" />
</div>
<div align="center"><b>Figure 6.2.3 - Site class.</b></div>

The `Site` class has the following attribute definitions:

| Attribute                            | Type     | Description                                                                                                                                                   | Required | Cardinality | Example                                                                                                                              |
|:-------------------------------------|:---------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:-------------------------------------------------------------------------------------------------------------------------------------|
| `id`                                 | String   | The unique identifier for the `Site`.  Typically a UUID or URN to provide global uniqueness across facilities.                                                | yes      | 1           | "ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                                                               |
| `self_uri`                           | URI      | A hyperlink reference (URI) to this `Shelf` (self). Canonical hyperlink to this `Shelf`.                                                                      | yes      | 1           | "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                 |
| `name`                               | String   | The long name of the `Site`.                                                                                                                                  | no       | 0..1        | "Lawrence Berkeley National Laboratory Building 59"                                                                                  |
| `description`                        | String   | A description of the `Site`.                                                                                                                                  | no       | 0..1        | "Level3 CLLI BKLYCACE, ESNETWEST at LBNL59."                                                                                         |
| `last_modified`                      | DateTime | The date this `Site` object was last modified, including modification of any attributes or links. Format follows the ISO 8601 standard with timezone offsets. | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                                                           |
| `short_name`                         | String   | Common/short name of the `Site`.                                                                                                                              | no       | 0..1        | "LBNL59"                                                                                                                              |
| `operating_organization`             | String   | The name of the organization operating the `Site`.                                                                                                            | yes      | 1           | "Lawrence Berkeley National Laboratory"                                                                                              |
| `location_uri`                       | URI      | A hyperlink reference (URI) to the `Location` containing this Site (hasLocation).                                                                             | no       | 0..1        | "https://iri.example.com/api/v1/facility/locations/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                             |
| `resource_uris`                      | URI[]    | A hyperlink reference (URI) to the `Resource` located at this `Site` (hasResource).                                                                           | no       | 0..*        | "https://iri.example.com/api/v1/facility/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc"                                             |

### 6.2.4 Location
A `Location` models the geographic, geopolitical, or spatial context associated with a `Site` that may
contain zero or more `Resources`. It serves as a foundational concept for expressing where resources
physically exist, are operated, or are logically grouped, enabling meaningful organization and
visualization.  `Location`s are reusable entities that may be shared across multiple `Sites` or `Facilities`.

<div align="center">
    <img src="./images/location-class.png" alt="Location class" width="400" />
</div>
<div align="center"><b>Figure 6.2.4 - Location class.</b></div>

The `Location` class has the following attribute definitions:

| Attribute                | Type     | Description                                                                                                                                                   | Required | Cardinality | Example                                                                                  |
|:-------------------------|:---------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:-----------------------------------------------------------------------------------------|
| `id`                     | String   | The unique identifier for the `Location`.  Typically a UUID or URN to provide global uniqueness across facilities.  | yes      | 1           | "ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                   |
| `self_uri`               | URI      | A hyperlink reference (URI) to this `Location` (self). Canonical hyperlink to this `Location`.  | yes      | 1           | "https://iri.example.com/api/v1/status/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"       |
| `name`                   | String   | The long name of the `Location`. | no       | 0..1        | "Lawrence Berkeley National Laboratory"                                                                    |
| `description`            | String   | A description of the `Location`. | no    | 0..1        | "Lawrence Berkeley National Laboratory is charged with conducting unclassified research across a wide range of scientific disciplines."                                             |
| `last_modified`          | DateTime | The date this `Location` object was last modified, including modification of any attributes or links. Format follows the ISO 8601 standard with timezone offsets. | no    | 0..1        | "2025-07-24T02:31:13.000Z"                                                               |
| `short_name`             | String   | Common/short name of the `Location`. | no       | 0..1        | `LBNL59` |
| `country_name`           | String   | The country name of the `Location`. | no       | 0..1        | `United States of America` |
| `locality_name`          | String   | The city or locality name of the `Location`. | no       | 0..1        | `Berkeley` |
| `state_or_province_name` | String   | The state or province name of the `Location`. | no       | 0..1        | `California` |
| `street_address`         | String   | The street address of the `Location`. | no       | 0..1        | `1 Cyclotron Rd, Building 59 Room 2102` |
| `unlocode`               | String   | The United Nations code for trade and transport `Location`. | no       | 0..1        | `US JBK` |
| `altitude`               | Float   | The altitude of the `Location`. | no       | 0..1        | 240 |
| `latitude`               | Float   | The latitude of the `Location`. | no       | 0..1        | 37.87492 |
| `longitude`              | Float   | The longitude of the `Location`. | no       | 0..1        | -122.2529 |
| `site_uris`              | URI[]    | A hyperlink reference (URI) to the `Resource` located at this `Site` (hasResource). | no    | 0..*   | ["http://localhost:8081/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"]                                               |

### 6.2.5 Relationships
The Facility model has a set of well-defined relationships and their cardinalities that allows
for navigation between objects based on relationship type.  The following table describes these
relationships.

| Source      | Relationship  | Destination  | Cardinality | Description                                                                        |
|:------------|:--------------|:-------------|:------------|:-----------------------------------------------------------------------------------|
| `Facility`   | hasLocation   | `Location`    | 0..*        | A Facility can be associated with one or more geographical Locations.              |
| `Facility`   | hostedAt      | `Site`        | 0..*        | A Facility can be hosted at one or more physical Sites.                            |
| `Facility`   | hasResource   | `Resource`   | 1..*        | A Facility can host zero or more Resources.                                        |
| `Facility`   | self          | `Facility`   | 1           | A Facility has a reference to itself.                                              |
| `Resource`   | memberOf      | `Facility`   | 1           | A Resource is a member of one of more Facilities (allowing for a shared resource). |
| `Resource`   | locatedAt     | `Site`       | 0..1        | A Resource is located at one Site.                                                 |
| `Resource`   | self          | `Resource`   | 1           | A Resource has a reference to itself.                                              |
| `Site`      | hasResource   | `Resource`   | 0..*        | A Site hosts zero or more Resources.                                               |
| `Site`      | locatedAt     | `Location`   | 0..1        | A Site is located at a geographic location.                                        |
| `Site`      | self          | `Site`       | 1           | A Site has a reference to itself.                                                  |
| `Location`  | hasSite       | `Site`       | 1..*        | A Location can contain one or more Sites.                                          |
| `Location`  | self          | `Location`   | 1           | A Location has a reference to itself.                                              |

---

## 6.3 Status Model
The Status model (see Figure 6.3) defines the core structure for representing operational information across 
the IRI distributed infrastructure. It is composed of three primary classes of named objects: `Incident`, 
`Event`, and `Resource`.  Each class encapsulates key attributes and behaviors relevant to the communication of
operational status. These classes serve as the foundational entities for describing a facility's operational 
impacts and administrative context on defined Resources.

<div align="center">
    <img src="./images/status-model.png" alt="Status Model" width="950" />
</div>
<div align="center"><b>Figure 6.3 - Status Model.</b></div>

These object definitions enable users and systems to traverse the Status model dynamically, answering
questions such as "What incidents have affected this facility and which resources are impacted?", or 
"Which events were logged during a specific outage?”.

### 6.3.1 Incident
An `Incident` represents a discrete occurrence, planned or unplanned, that actually or potentially affects 
the availability, performance, integrity, or security of one or more `Resource`s at a given Facility. It 
serves as a high-level grouping construct for aggregating and tracking related `Event`s over time and across
`Resources`.

<div align="center">
    <img src="./images/incident-class.png" alt="Incident class"  width="450" />
</div>
<div align="center"><b>Figure 6.3.1 - Incident class.</b></div>

The `Incident` class has the following attribute definitions:

| Attribute         | Type           | Description                                                                     | Required | Cardinality | Example                                                                                    |
|:------------------|:---------------|:--------------------------------------------------------------------------------|:---------|:------------|--------------------------------------------------------------------------------------------|
| `id`              | String         | Unique identifier (UUID) for the `Incident`.                                    | yes      | 1           | "05dcf051-8e9f-4806-8af0-125782ec2799`                                                     |
| `self_uri`        | URI            | Canonical hyperlink to this `Incident`.                                         | yes      | 1           | "https://iri.example.com/api/v1/status/incidents/05dcf051-8e9f-4806-8af0-125782ec2799"     |
| `name`            | String         | The long name of the `Incident`.                                                | no       | 0..1        | "Unplanned outage on resource group websites"                                              |
| `description`     | String         | Human‑readable description for this `Incident`.                                 | no       | 0..1        | "Unplanned outage on resource group websites."                                             |
| `last_modified`   | DateTime       | Timestamp (ISO 8601) when this `Incident` was last modified.                    | yes      | 1           | "2025-06-29T02:34:25.000Z"                                                                 |
| `status`          | StatusType     | The status of the resources associated with this `Incident`.                    | yes      | 1           | "down"                                                                 |
| `type`            | IncidentType   | The type of Incident.                                                           | yes      | 1           | "unplanned"                                                                 |
| `start`           | DateTime       | Timestamp (ISO 8601) of when this `Incident` started, or is predicted to start. | yes      | 1           | "2025-06-28T18:34:25.272Z"                                                                 |
| `end`             | DateTime       | Timestamp (ISO 8601) of when this `Incident` ended, or is predicted to end.     | no       | 0..1        | "2025-06-29T02:34:25.278Z"                                                                 |
| `resolution`      | ResolutionType | The resolution for this `Incident`.                                              | yes      | 1           | "unresolved" |
| `resource_uris`   | URI[]          | URIs of `Resource`s that maybe impacted by this `Incident` (mayImpact).         | no       | 0..*        | [`https://iri.example.com/api/v1/facility/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc`] |
| `event_uris`      | URI[]          | URIs of `Event`s generated by this `Incident` (hasEvent).                       | no       | 0..*        | [`https://iri.example.com/api/v1/status/events/f9d6e700-1807-45bd-9a52-e81c32d40c5a`]      |

### 6.3.2 Event
An `Event` represents a discrete, timestamped occurrence that reflects a change in state, condition, or behavior 
of a `Resource`, typically within the context of an ongoing `Incident`. `Event`s provide the fine-grained details 
necessary to understand the progression and impact of an `Incident`, serving as both diagnostic data and a 
lightweight status log of relevant activity.

<div align="center">
    <img src="./images/event-class.png" alt="Event class"  width="400" />
</div>
<div align="center"><b>Figure 6.3.2 - Event class.</b></div>

The `Event` class has the following attribute definitions:

| Attribute       | Type       | Description                                                   | Required | Cardinality | Example                                                                                    |
|:----------------|:-----------|:--------------------------------------------------------------|:---------|:------------|--------------------------------------------------------------------------------------------|
| `id`            | String     | Unique identifier (UUID) for the `Event`.                     | yes      | 1           | "0108be78-8771-4507-abfd-5823f265708d`                                                     |
| `self_uri`      | URI        | Canonical hyperlink to this `Event`.                          | yes      | 1           | "https://iri.example.com/api/v1/status/event/0108be78-8771-4507-abfd-5823f265708d"         |
| `name`          | String     | The long name of the `Event`.                                 | no       | 0..1        | "HPSS Archive (User)"                                                                      |
| `description`   | String     | Human‑readable description for this `Event`.                  | no       | 0..1        | "archive is UP."                                                                           |
| `last_modified` | DateTime   | Timestamp (ISO 8601) when this `Event` was last modified.     | yes      | 1           | "2025-07-24T02:31:13.000Z"                                                                 |
| `status`        | StatusType | The status of the resources associated with this `Event`.     | yes      | 1           | "up"                                                                                       |
| `occurred_at`   | DateTime   | Timestamp (ISO 8601) of when this `Event` occured.            | yes      | 1           | "2025-07-24T02:31:13.794Z"                                                                 |
| `resource_uri`  | URI        | URI of `Resource` that is impacted by this `Event` (impacts). | yes      | 1           | [`https://iri.example.com/api/v1/facility/resources/289d38f2-e93c-4840-b037-8b78d8ec36cc`] |
| `incident_uri`  | URI        | URI of `Incident` that generated this `Event` (generatedBy).  | yes      | 1           | [`https://iri.example.com/api/v1/status/incident/f9d6e700-1807-45bd-9a52-e81c32d40c5a`]    |

### 6.3.3 Resource
A `Resource` (see 6.2.2 Resource) models a consumable resource, a consumable service, or dependent infrastructure 
services exposed to the end user. In the context of the Status model, an `Incident` and `Event` reference
a `Resource` providing previous, current, or future status information.

<div align="center">
    <img src="./images/resource-class.png" alt="Resource class"  width="400" />
</div>
<div align="center"><b>Figure 6.3.3 - Resource class.</b></div>

The `Resource` class has the following attribute definitions:

| Attribute            | Type         | Description                                                                                                                                                                                                        | Required | Cardinality | Example                                                                                                                                       |
|:---------------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                 | String       | The unique identifier for the `Resource`.  Typically a UUID or URN to provide global uniqueness across facilities.                                                                                                 | yes      | 1           | "09a22593-2be8-46f6-ae54-2904b04e13a4"                                                                                                        |
| `self_uri`           | URI          | A hyperlink reference (URI) to this `Resource` (self). Canonical hyperlink to this `Resource`.                                                                                                                                                            | yes      | 1           | "https://iri.example.com/api/v1/status/resources/09a22593-2be8-46f6-ae54-2904b04e13a4"                                                        |
| `name`               | String       | The long name of the `Resource`.                                                                                                                                                                                   | no       | 0..1        | "Data Transfer Nodes"                                                                                                                         |
| `description`        | String       | A description of the `Resource`.                                                                                                                                                                                   | no       | 0..1        | "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS." |
| `last_modified`      | DateTime     | The date this `Resource` was last modified.  ISO 8601 standard with timezone offsets.                                                                                                                              | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                                                                    |
| `resource_type`      | ResourceType | The type of `Resource` based on string ENUM values.                                                                                                                                                                | yes      | 1           | "compute"                                                                                                                                     |
| `group`              | String       | The member `Resource` group.                                                                                                                                                                                       | no       | 0..1        | "perlmutter" |
| `current_status`     | StatusType   | The current status of this `Resource` at time of query based on string ENUM values. If there is no last Event associated with the resource to indicate a current status, then currentStatus defaults to "unknown". | yes      | 1           | "up"                                                                                                                                          |
| `capability_uris`    | String[]     | Hyperlink references (URIs) to capabilities this `Resource` provides (hasCapability).                                                                                                                              | no       | 0..*        | ["https://iri.example.com/api/v1/account/capabilities/b1ce8cd1-e8b8-4f77-b2ab-152084c70281"]                                                  |
| `located_at_uri`     | URI          | A hyperlink reference (URI) to the `Site` containing this `Resource` (locatedAt).                                                                                                                                  | no       | 0..1        | "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                          |
| `member_of_uri`      | URI          | A hyperlink reference (URI) to `Facility` managing this `Resource` (memberOf).                                                                                                                                         | no       | 0..1        | "https://iri.example.com/api/v1/facility"                                                                                                     |

The `ResourceType` is an enumeration to identify the type of `Resource`.  This
is a broad classification and may not provide enough detail to make job
submission decisions.

| ENUM        | Description                           |
|:------------|:--------------------------------------|
| `website`   | This `Resource` is of type `website`. |
| `service`   | This `Resource` is of type `service`. |
| `compute`   | This `Resource` is of type `compute`. |
| `system`    | This `Resource` is of type `system`.  |
| `storage`   | This `Resource` is of type `storage`. |
| `network`   | This `Resource` is of type `network`. |
| `unknown`   | This `Resource` is of type `unknown`. |

The `StatusType` is an enumeration of the possible status values for a `Resource`.

| ENUM       | Description                                                                             |
|:-----------|:----------------------------------------------------------------------------------------|
| `up`       | The `Resource` is `up` and available for use.                                           |
| `degraded` | The `Resource` is `degraded` and although available, may not be providing full service. |
| `down`     | The `Resource` is `down` and unavailable for use.                                       |
| `unknown`  | The `Resource` is in an `unknown` state and should be considered unavailable.           |

### 6.3.4 Relationships
The Status model has a set of well-defined relationships and their cardinalities that allows
for navigation between objects based on relationship type.  The following table describes these
relationships.

| Source   | Relationship | Destination | Description                                       |
|:---------|:-------------|:------------|:--------------------------------------------------|
| `Incident` | hasEvent     | `Event`     | A Facility has one or more associated Events.     |
| `Incident` | mayImpact    | `Resource`  | An Incident may impact one or more Resources.     |
| `Incident` | self         | `Incident`  | An Incident has a reference to itself.            |
| `Event`    | generatedBy  | `Incident`  | An Event is generated by an Incident.             |
| `Event`    | impacts      | `Resource`  | An Event impacts a Resource.                      |
| `Event`    | self         | `Event`     | An Event has a reference to itself.               |
| `Resource` | impactedBy   | `Event`     | A Resource is impacted by zero or more Events.    |
| `Resource` | hasIncident  | `Incident`  | A Resource is impacted by zero or more Incidents. |

---

## 6.4 Allocation Model
The Allocation model (Figure 6.4) defines the core structure for representing project and user 
allocations at a `Facility`. An allocation is a project-specific, time-bounded budget of facility 
resources, granted through the facility’s proposal and review process and tracked by the facility 
for the duration of the allocation period.

The Allocation model is composed of four primary classes of named objects: `Project`, 
`ProjectAllocation`, `UserAllocation`, and `Capability`. Each class encapsulates key 
attributes and behaviors relevant to the management of allocations.

<div align="center">
    <img src="./images/allocation-model.png" alt="Allocations Model"  width="900" />
</div>
<div align="center"><b>Figure 6.4 - Allocation Model.</b></div>

### 6.4.1 Project
A `Project` is the allocation account (also called a repository) that represents a specific DOE Office 
of Science research effort, owned by a single PI, to which compute and storage resources are awarded 
and against which all jobs and data usage by that project’s members are charged.  In the Allocation
model a project is a named object that associates a list of users to an allocation at the facility.

<div align="center">
    <img src="./images/project-class.png" alt="Project class" width="400" />
</div>
<div align="center"><b>Figure 6.4.1 - Project Class.</b></div>

The `Project` class has the following attribute definitions:

| Attribute                  | Type     | Description                                                                                                                             | Required | Cardinality | Example                                                                                                 |
|:---------------------------|:---------|:----------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:--------------------------------------------------------------------------------------------------------|
| `id`                       | String   | The unique identifier for the `Project`.  Typically a UUID or URN to provide global uniqueness across facilities.                       | yes      | 1           | "863a48f9-447e-4c22-82fb-72bcc6686d4c"                                                                  |
| `self_uri`                 | URI      | A hyperlink reference (URI) to this `Project` (self). Canonical hyperlink to this `Project`.                                            | yes      | 1           | "https://iri.example.com/api/v1/account/projects/863a48f9-447e-4c22-82fb-72bcc6686d4c"                  |
| `name`                     | String   | The long name of the `Project`.                                                                                                         | no       | 0..1        | "Staff research project"                                                                                |
| `description`              | String   | A description of the `Project`.                                                                                                         | no       | 0..1        | "Compute and storage allocation for staff research use"                                                 |
| `last_modified`            | DateTime | The date this `Project` was last modified.  ISO 8601 standard with timezone offsets.                                                    | no       | 0..1        | "2025-06-03T10:04:25.000Z"                                                                              |
| `user_ids`                 | String[] | The list of user identifiers associated with this `Project`.                                                                            | no       | 0..*        | [ "gtorok", "hacksaw", "bubbles" ]                                                                      |
| `project_allocation_uris`  | URI[]    | A list of hyperlink references (URI) to instances of `ProjectAllocation` associated with this this `Project` (hasProjectAllocation).    | no       | 0..*        | [ "https://iri.example.com/api/v1/allocation/project_allocations/ed25c679-0d1e-4c99-817c-0475694fde31" ] |

### 6.4.2 ProjectAllocation
A `ProjectAllocation` is an accounting object that represents the pool of `Resource`s awarded to a 
specific `Project`. In practical terms, it’s the record that ties a `Project` to its compute and storage
allocation at an HPC facility. For example, how much was awarded, how much has been used, and how much 
remains, for the current allocation period.

<div align="center">
    <img src="./images/projectallocation-class.png" alt="ProjectAllocation class" width="400" />
</div>
<div align="center"><b>Figure 6.4.2 - ProjectAllocation Class.</b></div>

The `ProjectAllocation` class has the following attribute definitions:

| Attribute                | Type              | Description                                                                                                                              | Required | Cardinality | Example                                                                                              |
|:-------------------------|:------------------|:-----------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:-----------------------------------------------------------------------------------------------------|
| `id`                     | String            | The unique identifier for the `ProjectAllocation`.  Typically a UUID or URN to provide global uniqueness across facilities.              | yes      | 1           | "ed25c679-0d1e-4c99-817c-0475694fde31"                                                               |
| `self_uri`               | URI               | A hyperlink reference (URI) to this `ProjectAllocation` (self). Canonical hyperlink to this `ProjectAllocation`.                                   | yes      | 1           | "https://iri.example.com/api/v1/allocation/project_allocations/ed25c679-0d1e-4c99-817c-0475694fde31" |
| `name`                   | String            | The long name of the `ProjectAllocation`.                                                                                                | no       | 0..1        | "Perlmutter allocation"                                                                              |
| `description`            | String            | A description of the `ProjectAllocation`.                                                                                                | no       | 0..1        | "Perlmutter allocation for staff research project"                                                   |
| `last_modified`          | DateTime          | The date this `ProjectAllocation` was last modified.  ISO 8601 standard with timezone offsets.                                           | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                           |
| `entries`                | AllocationEntry[] | The list of numerical allocations associated with a `ProjectAllocation`.                                                                 | no       | 0..*        | [ ]                                                                                                  |
| `project_uri`            | URI               | A hyperlink reference (URI) to the `Project` associated with this this `ProjectAllocation` (hasProject).                                 | yes      | 1           | "https://iri.example.com/api/v1/allocation/projects/d1dfbe36-c00a-40bd-8960-5a87ceb6a1ba"            |
| `capability_uri`         | URI               | A hyperlink reference (URI) to the `Capability` associated with this this `ProjectAllocation` (hasCapability).                           | no       | 0..*        | "https://iri.example.com/api/v1/allocation/capabilities/2783f4b6-a4f4-4385-8fd6-8a546e3f2209"        |
| `user_allocation_uris`   | URI[]             | A list of hyperlink references (URI) to instances of `UserAllocation` associated with this `ProjectAllocation` (hasUserAllocation).      | no       | 0..*        | "https://iri.example.com/api/v1/allocation/user_allocations/b70fbc23-e265-45c9-8de2-491fcc3f8c0"     |

`AllocationEntry` is a non-named object class (is not directly referencable through the API) that augments the
`ProjectAllocation` class with numerical allocation data.  The `AllocationEntry` class has the following attribute 
definitions:

| Attribute     | Type           | Description                                        | Required | Cardinality | Example            |
|:--------------|:---------------|:---------------------------------------------------|:---------|:------------|:-------------------|
| `allocation`  | Float          | The total amount of the `Resource` allocated.      | yes      | 1           | 597.0710332588748  |
| `usage`       | Float          | The amount of allocation already consumed.         | yes      | 1           | 168.51791796212257 |
| `unit`        | AllocationUnit | The unit of measurement the allocation represents. | yes      | 1           | "node_hours"       |

The `AllocationUnit` is an enumeration that models the technology unit of measure.  For example, compute is
allocated based on `node_hours`.

| ENUM         | Description                                              |
|:-------------|:---------------------------------------------------------|
| `node_hours` | HPC compute resources are tracked based on `node_hours`. |
| `bytes`      | Storage resources are tracked based on `bytes`.          |
| `inodes`     | Storage resources are tracked based on `inodes`.         |

### 6.4.3 UserAllocation
UserAllocation is the per-user slice of a project’s allocation: how much compute and storage a 
specific user is allowed to spend from a given project.  This can never exceed limits placed
on the associated `ProjectAllocation`.

<div align="center">
    <img src="./images/userallocation-class.png" alt="UserAllocation class" width="400" />
</div>
<div align="center"><b>Figure 6.4.3 - UserAllocation Class.</b></div>

The `UserAllocation` class has the following attribute definitions:

| Attribute                 | Type              | Description                                                                                                                         | Required | Cardinality | Example                                                                                              |
|:--------------------------|:------------------|:------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:-----------------------------------------------------------------------------------------------------|
| `id`                      | String            | The unique identifier for the `UserAllocation`.  Typically a UUID or URN to provide global uniqueness across facilities.            | yes      | 1           | "ed25c679-0d1e-4c99-817c-0475694fde31"                                                               |
| `self_uri`                | URI               | A hyperlink reference (URI) to this `UserAllocation` (self). Canonical hyperlink to this `UserAllocation`.                                 | yes      | 1           | "https://iri.example.com/api/v1/allocation/user_allocations/ed25c679-0d1e-4c99-817c-0475694fde31"    |
| `name`                    | String            | The long name of the `UserAllocation`.                                                                                              | no       | 0..1        | "Bubble's user allocaton"                                                                            |
| `description`             | String            | A description of the `UserAllocation`.                                                                                              | no       | 0..1        | "Bubble's user allocaton for staff research project"                                                 |
| `last_modified`           | DateTime          | The date this `UserAllocation` was last modified.  ISO 8601 standard with timezone offsets.                                         | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                           |
| `user_id`                 | String            | The user identifier associated with this `UserAllocation`.                                                                          | yes      | 1           | "bubbles"                                                                                            |
| `entries`                 | AllocationEntry[] | The list of numerical allocations associated with the `UserAllocation`.                                                             | no       | 0..*        | [ ]                                                                                                  |
| `project_allocation_uri`  | URI               | A hyperlink reference (URI) to an instance of `ProjectAllocation` associated with this `UserAllocation` (hasProjectAllocation).     | yes      | 1           | "https://iri.example.com/api/v1/allocation/project_allocations/ed25c679-0d1e-4c99-817c-0475694fde31" |

`AllocationEntry` is a non-named object class (is not directly referencable through the API) that augments the
`UserAllocation` class with numerical allocation data.  The `AllocationEntry` class has the following attribute
definitions:

| Attribute     | Type           | Description                                        | Required | Cardinality | Example            |
|:--------------|:---------------|:---------------------------------------------------|:---------|:------------|:-------------------|
| `allocation`  | Float          | The total amount of the `Resource` allocated.      | yes      | 1           | 597.0710332588748  |
| `usage`       | Float          | The amount of allocation already consumed.         | yes      | 1           | 168.51791796212257 |
| `unit`        | AllocationUnit | The unit of measurement the allocation represents. | yes      | 1           | "node_hours"       |

The `AllocationUnit` is an enumeration that models the technology unit of measure.  For example, compute is
allocated based on `node_hours`.

| ENUM         | Description                                              |
|:-------------|:---------------------------------------------------------|
| `node_hours` | HPC compute resources are tracked based on `node_hours`. |
| `bytes`      | Storage resources are tracked based on `bytes`.          |
| `inodes`     | Storage resources are tracked based on `inodes`.         |

### 6.4.4 Capability
Defines an aspect of a resource (facility service or resource) that can be allocated.
For example, Examples in practice would map to things like:
* “Perlmutter CPU core-hours”
* “Perlmutter GPU core-hours”
* “Project directory space on global_common”
* “Archive (HPSS) space/operations”
* “Data-transfer service on DTNs”

For some resources at a facility, this will be 1 to 1 with the resource. It is
a way to subdivide a resource into allocatable sub-resources further.  The word 
"capability" is also known to users as something they need for a job to run.

<div align="center">
    <img src="./images/capability-class.png" alt="Capability class" width="400" />
</div>
<div align="center"><b>Figure 6.4.4 - Capability Class.</b></div>

The `Capability` class has the following attribute definitions:

| Attribute         | Type             | Description                                                                                                          | Required | Cardinality | Example                                                                                       |
|:------------------|:-----------------|:---------------------------------------------------------------------------------------------------------------------|:---------|:------------|:----------------------------------------------------------------------------------------------|
| `id`              | String           | The unique identifier for the `Capability`.  Typically a UUID or URN to provide global uniqueness across facilities. | yes      | 1           | "ed25c679-0d1e-4c99-817c-0475694fde31"                                                        |
| `self_uri`        | URI              | A hyperlink reference (URI) to this `Capability` (self). Canonical hyperlink to this `UserAllocation`.               | yes      | 1           | "https://iri.example.com/api/v1/allocation/capabilities/ed25c679-0d1e-4c99-817c-0475694fde31" |
| `name`            | String           | The long name of the `Capability`.                                                                                   | no       | 0..1        | "Perlmutter GPU"                                                                              |
| `description`     | String           | A description of the `Capability`.                                                                                   | no       | 0..1        | "Perlmutter GPU capability"                                                                   |
| `last_modified`   | DateTime         | The date this `Capability` was last modified.  ISO 8601 standard with timezone offsets.                              | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                    |
| `units`           | AllocationUnit[] | A list of units of measurement that apply to the capability provided by the `Resource`.                              | yes      | 1           | "node_hours"                                                                                  |
| `resource_uri`    | URI              | A hyperlink reference (URI) to an instance of `Resource` that this `Capability` is associated with (hasResource).    | yes      | 1           | "https://iri.example.com/api/v1/facility/resources/8b61b346-b53c-4a8e-83b4-776eaa14cc67"      |

The `AllocationUnit` is an enumeration that models the technology unit of measure.  For example, compute is
allocated based on `node_hours`.

| ENUM         | Description                                              |
|:-------------|:---------------------------------------------------------|
| `node_hours` | HPC compute resources are tracked based on `node_hours`. |
| `bytes`      | Storage resources are tracked based on `bytes`.          |
| `inodes`     | Storage resources are tracked based on `inodes`.         |

### 6.4.5 Resource
A `Resource` (see 6.2.2 Resource) models a consumable resource, a consumable service, or 
dependent infrastructure services exposed to the end user.  A `Resource` in the context
of the Allocation model is referenced by `Capability` to describe the `Resource`s 
available for use by the user/project in the associated `Allocation`.

<div align="center">
    <img src="./images/resource-class.png" alt="Resource class" width="400" />
</div>
<div align="center"><b>Figure 6.4.5 - Resource class.</b></div>

The `Resource` class has the following attribute definitions:

| Attribute            | Type         | Description                                                                                                                                                                                                        | Required | Cardinality | Example                                                                                                                                       |
|:---------------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                 | String       | The unique identifier for the `Resource`.  Typically a UUID or URN to provide global uniqueness across facilities.                                                                                                 | yes      | 1           | "09a22593-2be8-46f6-ae54-2904b04e13a4"                                                                                                        |
| `self_uri`           | URI          | A hyperlink reference (URI) to this `Resource` (self). Canonical hyperlink to this `Resource`.                                                                                                                                                            | yes      | 1           | "https://iri.example.com/api/v1/status/resources/09a22593-2be8-46f6-ae54-2904b04e13a4"                                                        |
| `name`               | String       | The long name of the `Resource`.                                                                                                                                                                                   | no       | 0..1        | "Data Transfer Nodes"                                                                                                                         |
| `description`        | String       | A description of the `Resource`.                                                                                                                                                                                   | no       | 0..1        | "The NERSC data transfer nodes provide access to Global Homes, Global Common, the Community File System (CFS), Perlmutter Scratch, and HPSS." |
| `last_modified`      | DateTime     | The date this `Resource` was last modified.  ISO 8601 standard with timezone offsets.                                                                                                                              | no       | 0..1        | "2025-07-24T02:31:13.000Z"                                                                                                                    |
| `resource_type`      | ResourceType | The type of `Resource` based on string ENUM values.                                                                                                                                                                | yes      | 1           | "compute"                                                                                                                                     |
| `group`              | String       | The member `Resource` group.                                                                                                                                                                                       | no       | 0..1        | "perlmutter" |
| `current_status`     | StatusType   | The current status of this `Resource` at time of query based on string ENUM values. If there is no last Event associated with the resource to indicate a current status, then currentStatus defaults to "unknown". | yes      | 1           | "up"                                                                                                                                          |
| `capability_uris`    | String[]     | Hyperlink references (URIs) to capabilities this `Resource` provides (hasCapability).                                                                                                                              | no       | 0..*        | ["https://iri.example.com/api/v1/account/capabilities/b1ce8cd1-e8b8-4f77-b2ab-152084c70281"]                                                  |
| `located_at_uri`     | URI          | A hyperlink reference (URI) to the `Site` containing this `Resource` (locatedAt).                                                                                                                                  | no       | 0..1        | "https://iri.example.com/api/v1/facility/sites/ce2bbc49-ba63-4711-8f36-43b74ec2fe45"                                                          |
| `member_of_uri`      | URI          | A hyperlink reference (URI) to `Facility` managing this `Resource` (memberOf).                                                                                                                                         | no       | 0..1        | "https://iri.example.com/api/v1/facility"                                                                                                     |

The `ResourceType` is an enumeration to identify the type of `Resource`.  This
is a broad classification and may not provide enough detail to make job
submission decisions.

| ENUM        | Description                           |
|:------------|:--------------------------------------|
| `website`   | This `Resource` is of type `website`. |
| `service`   | This `Resource` is of type `service`. |
| `compute`   | This `Resource` is of type `compute`. |
| `system`    | This `Resource` is of type `system`.  |
| `storage`   | This `Resource` is of type `storage`. |
| `network`   | This `Resource` is of type `network`. |
| `unknown`   | This `Resource` is of type `unknown`. |

The `StatusType` is an enumeration of the possible status values for a `Resource`.

| ENUM       | Description                                                                             |
|:-----------|:----------------------------------------------------------------------------------------|
| `up`       | The `Resource` is `up` and available for use.                                           |
| `degraded` | The `Resource` is `degraded` and although available, may not be providing full service. |
| `down`     | The `Resource` is `down` and unavailable for use.                                       |
| `unknown`  | The `Resource` is in an `unknown` state and should be considered unavailable.           |

### 6.4.6 Relationships
The Allocation model has a set of well-defined relationships and their cardinalities that allows
for navigation between objects based on relationship type.  The following table describes these
relationships.

| Source              | Relationship            | Destination         | Cardinality | Description                                                             |
|:--------------------|:------------------------|:--------------------|:------------|:------------------------------------------------------------------------|
| `Project`           | self                    | `Project`           | 1           | A `Project` has a reference to itself.                                  |
| `Project`           | hasProjectAllocation    | `ProjectAllocation` | 0..*        | A `Project` has zero or more `ProjectAllocation`.                       |
| `ProjectAllocation` | self                    | `ProjectAllocation` | 1           | A `ProjectAllocation` has a reference to itself.                        |
| `ProjectAllocation` | hasProject              | `Project`           | 1           | A `ProjectAllocation` is associated with single `Project`.              |
| `ProjectAllocation` | hasUserAllocation       | `UserAllocation`    | 0..*        | A `ProjectAllocation` is associated with zero or more `UserAllocation`. |
| `ProjectAllocation` | hasCapability           | `Capability`        | 0..*        | A `ProjectAllocation` is associated with zero or more `Capability`.     |
| `UserAllocation`    | self                    | `UserAllocation`    | 1           | A `UserAllocation` has a reference to itself.                           |
| `UserAllocation`    | hasProjectAllocation    | `ProjectAllocation` | 1           | A `UserAllocation` is associated with a single `ProjectAllocation`.     |
| `Capability`        | self                    | `Capability`        | 1           | A `Capability` has a reference to itself.                               |
| `Capability`        | hasResource             | `Resource`          | 1           | A `Capability` is associated with a single `Resource`.                  |
| `Resource`          | self                    | `Resource`          | 1           | A `Resource` has a reference to itself.                                 |
| `Resource`          | providesCapability      | `Capability`        | 0..*        | A `Resource` his associated with zero or more `Capability`.             |

---

## 6.5 Job Model
The Job model (Figure 6.5) defines encapsulates all of the information needed to run and 
manage a job at a Facility. This model definition is based off of the ExaWorks PSI/J job 
specification.  The PSI/J Job class represents a concrete, scheduler-aware unit of work 
and is the primary abstraction through which applications interact with underlying batch 
or resource managers. It encapsulates the full lifecycle of a job from creation and 
configuration using a job description, through submission and state transitions, to 
completion, cancellation, and error handling while insulating callers from 
scheduler-specific details.

The Job model is composed of a single named class called `Job`, four supporting classes
`JobSpec`, `ResourceSpec`, `JobAttributes`, and `JobStatus`, along with the `JobState`
enumeration.

<div align="center">
    <img src="./images/job-model.png" alt="Job Model" width="900" />
</div>
<div align="center"><b>Figure 6.5 - Job Model.</b></div>

### 6.5.1 Job


---

## 6.6 Relationships

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
