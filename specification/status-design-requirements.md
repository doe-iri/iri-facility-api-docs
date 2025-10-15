# 4. Design Requirements 

The choice of interface technology is primarily driven by requirement \[R1\] that dictates an end user need for simplicity of integration into their workflows, and utilization of a technology familiar to their community.  There are no near-realtime requirements for the facility status API, and no requirements for an event driven API supporting notifications.  As a result, the IRI Interfaces Subcommittee has chosen a RESTful API design for easy integration into any programming environment.

The following design requirements are defined by the IRI Interfaces Subcommittee to guide the specification of the facility status API:

1. The facility status API design MUST utilize RESTful API design patterns and best practices.

2. The facility status API SHOULD be self describing and self navigable.

3. The facility status API MUST be documented using the OpenAPI Description (OAD) format for public consumption.

# 5. Implementation Requirement

Implementation requirements are specific, actionable guidelines that define what needs to be done to develop, deploy, and successfully maintain a production instance of the Facility Status API.  These requirements are derived from high-level functional and non-functional requirements specified by stakeholders and IRI subcommittees that are to ensure the system meets its intended purpose.

1. Each facility status API deployment SHOULD implement OpenTelemetry to allow Jacques' IRI support teams to monitor/debug each API instance when performing troubleshooting activities, or for proactively identifying performance issues.  
     
2. A JSON content type encoding must be made available as default output for the facility status API, with support for XML content type encodings as optional.

Security…

* Maintain up-to-date OS and software packages to reduce vulnerabilities.  
* Firewall API server from critical resource infrastructure to reduce impact if server is compromised.

