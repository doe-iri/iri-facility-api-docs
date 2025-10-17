# 2. User Stories 

The following user stories are written in the context of the IRI Facility and Status functionalities.

[1] Jinnette is a Research Software Engineer (RSE) designing an application workflow to programmatically access resources within the ASCR Facilities Ecosystem through the new IRI Facility Status API.  Jinnette requires uninterrupted access to the API and its related services, and would like to programmatically determine:

* The ASCR Facility that is associated with an API instance.  
* The resources associated with a specific ASCR Facility.  
* If a specific resource at an ASCR Facility is currently available for use by the workflow.  
* If a specific resource at an ASCR Facility will be available for use by the workflow at a specific point in the future.  
* The start and end times of both scheduled and unscheduled outages for a resource.  
* If a workflow failure was caused by a specific resource outage.  
* Contact information for support staff at the ASCR Facility that could help troubleshoot a workflow related issue.

[2] Jean-Guy is an RSE tasked with designing an IRI visualization tool.  This tool will show a global map view containing all the ASCR Facilities contributing resources to the ecosystem, and the status of resources at these facilities.  He has been told about the new IRI Facility Status API and is excited to get started.  Jean-Guy would like to programmatically determine:

* A list of all the ASCR Facilities contributing resources, and basic information about each facility for visualization on the map.  Jean-Guy is interested in names of the facility, the operating organization, physical site locations associated with the facility, and resources located at each site.  
* Operational status of resources at the facility to visualize status on the map, and any active outage information if available.  
* A list of scheduled maintenance activities to visualize any pending downtimes.  
* A limited history of scheduled and unscheduled outages for display in an event history window.

[3] Jacques is a software engineer tasked with providing user support for the IRI Facility Status API across all ASCR facilities participating in the ecosystem.  His focus is on improving the user’s experience when using the IRI API, identifying and fixing possible issues before the user encounters a problem, and helping a user quickly solve any issues they do encounter.  Jacques needs the ability to:

* Monitor when an API at a facility becomes unavailable.  
* Determine when there are resource outages that could impact or have impacted users.  
* Perform distributed tracing across facility API instances to determine where a user’s workflow could have failed, and for what reason.  
* Perform metrics collection such as request counts, error rates, and operation latency to monitor API performance across the facilities and identify any hot spots for engineering followup.  
* Exchange application context information with facility engineers to assist in debugging application workflows within the facility itself.  
* Allow the linking of traces from different services, creating a unified view of the API call as it moves through microservices or other back-end systems.  
* Correlation between logs, traces, and metrics, providing a cohesive picture of what’s happening across the facility API.

[4] Sébastien is DoE facility security administrator who is concerned about vulnerability aspects of the IRI Facility Status API and wants to ensure the system is operational, is behaving correctly, and remains secure.  Sébastien is concerned with the following types of bad actors:

* A hacker attempting to gain unauthorized access to DoE facility resources through the IRI Facility Status API and steal resources or sensitive data.  
* A hacker attempting to perform denial-of-service attacks on DoE facility resources to disrupt service availability, impacting a researcher’s ability to perform their science.  
* A Research Software Engineer (RSE) at a DoE user facility that has project allocation and is trying to game the system to jump their compute jobs to the front of the queue at an HPC facility.  
* A Research Software Engineer (RSE) at a DoE user facility that has project allocation runs an inappropriate job on the system.

[5] Céline is DoE facility system administrator who has deployed an IRI Facility Status API onto production hardware within a DoE facility.  Céline would like to monitor the service, and troubleshoot the service when issues arise.  Céline is interested in the the following capabilities:

* Health endpoint to determine if the IRI Facility API service is up, healthy, and accepting traffic as per existing standards:  
  * UP — The component is working as expected.  
  * DOWN — The component isn’t working.  
  * OUT\_OF\_SERVICE — The component is out of service temporarily.  
  * UNKNOWN — The component state is unknown.  
* Access to telemetry data (metrics, logs, and traces) to troubleshoot failures and issues relating to latency of operations.  
* Administrator level access to the API allows for a complete view of data relating to the system.

The following user stories are written in the context of the IRI Facility Account functionalities.

[6]

The following user stories are written in the context of the IRI Facility Job Management functionalities.

[7]

The following user stories are written in the context of the IRI Facility File System functionalities.

[8]

