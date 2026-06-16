# 4. Design Requirements 

The choice of interface technology is primarily driven by requirement \[R1\] that dictates an end user need for simplicity of integration into their workflows, and utilization of a technology familiar to their community.  There are no near-realtime requirements for the facility status API, and no requirements for an event driven API supporting notifications.  As a result, the IRI Interfaces Subcommittee has chosen a RESTful API design for easy integration into any programming environment.

The following design requirements are defined by the IRI Interfaces Subcommittee to guide the specification of the facility status API:

1. The facility status API design MUST utilize RESTful API design patterns and best practices.

2. The facility status API SHOULD be self describing and self navigable.

3. The facility status API MUST be documented using the OpenAPI Description (OAD) format for public consumption.


