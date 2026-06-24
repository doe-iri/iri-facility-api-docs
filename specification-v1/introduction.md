# 1. Facility Status

The Facility Status API offers users programmatic access to information on the operational status of various resources within a facility, scheduled maintenance/outage events, and a limited historical record of these events.  Designed for quick and efficient status checks of current and future (scheduled) operational status, this API allows developers to integrate facility information into applications or workflows, providing a streamlined way to programmatically access data without manual intervention.

It should be noted that the operational status of a resource is not an indication of a commitment to provide service, only that the resource is in the described operational state.

The Facility Status API is not intended for reporting or monitoring purposes; it does not support asynchronous logging or alerting capabilities, and should not be used to derive any type of up or downtime metrics.  Instead, its primary focus is on delivering simple, on-demand access to facility resource status, and scheduled maintenance events.

# 1.1 Terminology

Object  
 - An object is any identifiable entity that can be accessed or manipulated over the API and represents a particular thing.

Facility  
 - A specialized research facility funded and operated by the U.S. Department of Energy that provides unique scientific tools, expertise, and infrastructure for researchers from across academia, industry, and government.   In a more general definition, a Facility offers Resources to scientific workflows for programmatic consumption.

Resource  
 - A Resource is an entity that either directly delivers a service to an end user or application (e.g., a compute node, virtual machine, network endpoint, storage instance), or indirectly supports the delivery of such a service by enabling, hosting, or connecting other resources (e.g., authentication server, routers, switches, power supplies).  Resources are typed, managed, and monitored objects that represent the components making up a system’s operational fabric. They are central to service modeling, observability, and incident response.

Consumable Service  
 - A service offered by the Facility for use by an end user workflow such as compute nodes to run jobs, or storage to hold experimental data, etc.  This is modelled as a Resource.

Site  
 - A Site represents the physical and administrative context in which a Resource is deployed and operated. It is associated with a geographic or network location where one or more resources reside and serves as the anchor point for associating these resources with their broader infrastructure and organizational relationships.

Location  
 - A Location models the geographic, geopolitical, or spatial context associated with a Site in which one or more Resources. It serves as a foundational concept for expressing where resources physically exist, are operated, or are logically grouped, enabling meaningful organization and visualization.  Locations are reusable entities that may be shared across multiple Sites or Facilities.

Incident  
 - An Incident represents a discrete occurrence, planned or unplanned, that actually or potentially affects the availability, performance, integrity, or security of one or more Resources at a given Facility. It serves as a high-level grouping construct for aggregating and tracking related Events over time and across multiple system components.

Event  
 - An Event represents a discrete, timestamped occurrence that reflects a change in state, condition, or behavior of a Resource, typically within the context of an ongoing Incident. Events provide the fine-grained details necessary to understand the progression and impact of an Incident, serving as both diagnostic data and a lightweight status log of relevant activity.

Research Software Engineer (RSE)  
 - A Research Software Engineer (RSE) is a professional who combines expertise in software engineering and research to support and advance scientific research.
