# 3. Requirements

In the following requirements the term “expose” is used to describe both the modeling of the specified resource and operations to retrieve the specified resource.

[R1] The facility status API SHOULD utilize technologies familiar to the end user community to help reduce barriers of adoption and simplify integration into their workflows.  
     
[R2] The facility status API MUST expose a discoverable resource describing the Facility that includes name, description, hosting organization, and contact information.  

[R3] The facility status API SHOULD expose site and geographic location information for the Facility to allow for application visualization.  

[R4] The facility status API MUST expose a managed Resource for each system offering a consumable service of interest to an end user (compute, storage, networking, etc.).  

[R5] The facility status API MAY expose a managed Resource that supports a resource offering a consumable service of interest, but does not itself provide the service (authentication, database, API controller, etc.).  

[R6] The facility status API MAY expose dependency relationships between managed Resources such that dependencies could be used to determine the availability of a consumable service.  

[R7] The facility status API MUST expose grouping of related managed Resources into a resource group permitting the modeling of more complex systems.  

[R8] The facility status API MUST expose the operational status of each managed Resource as either up, down, degraded, or unknown.  The unknown status is used when the facility status API is unable to accurately determine the state of a managed Resource.  

[R9] The facility status API MUST expose scheduled outages (start and end time), the managed Resources that will be impacted by the outage, the severity of the outage, and a notes attribute for providing additional information.  

[R10] The facility status API MUST expose unscheduled outages, the start and end time of the outage, the managed Resources impacted by the outage, the severity of the outage, and a notes attribute for providing additional information.  

[R11]  The facility status API MUST distinguish between planned and unplanned outages.  

[R12] The facility status API SHOULD support retrieval of managed Resources by resource groups.  

[R13] The facility status API SHOULD support retrieval of all dependencies of a managed Resource when dependency information is available.  

[R14] The facility status API MUST support efficient retrieval of the current status of a managed Resource.

[R15] The facility status API MUST support the retrieval of all scheduled outages for a specific managed Resource.

Gabor’s use cases for search.  
/resource  
 \- name \[done\]  
 \- current status \[done\]

/incidents  
 \- to/from date  
 \- resources (list of resources impacted) \[done\]  
 \- can optionally include list of events \[done\]

/events  
 \= single timestamp  
 \- single resource impacted \[done\]  
 \- single incident it belongs to \[done\]

Queries:  
/resource \= all resources and their statuses  
/resource/{name} \= a single resource and its status

/incidents?to={}\&from={}\&resources={} \= all incidents for a time period impacting certain resources

/events?to={}\&from={}\&resources={} \= all events for a time period impacting certain resources

