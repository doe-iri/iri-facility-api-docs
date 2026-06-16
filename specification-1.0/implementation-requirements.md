# 5. Implementation Requirement

Implementation requirements are specific, actionable guidelines that define what needs to be done to develop, deploy, and successfully maintain a production instance of the Facility Status API.  These requirements are derived from high-level functional and non-functional requirements specified by stakeholders and IRI subcommittees that are to ensure the system meets its intended purpose.

1. Each facility status API deployment SHOULD implement OpenTelemetry to allow Jacques' IRI support teams to monitor/debug each API instance when performing troubleshooting activities, or for proactively identifying performance issues.

2. A JSON content type encoding must be made available as default output for the facility status API, with support for XML content type encodings as optional.

Security…

* Maintain up-to-date OS and software packages to reduce vulnerabilities.
* Firewall API server from critical resource infrastructure to reduce impact if server is compromised.

Performance requirements for an IRI API implementations:

   [P1] A Facility IRI API implementation MUST support at least 100 unique active user sessions.

   [P2] A Facility IRI API implementation MUST support a minimum of 1,000 query requests per second across the job status, filesystem, and facility status API operations.
   
   [P3] A Facility IRI API implementation MUST support at least 5 job creation requests per second per unique system unless the underlying job scheduling system cannot support this sustained rate.
   
   [P4] A Facility IRI API implementation MUST support 90% of query requests ≤ 200 ms and 99% ≤ 500 ms across the job status, filesystem, and facility status API operations.
   
   [P5] The Facility IRI API SHOULD implement an asynchronous API for requests that exceed 15 seconds to reduce system resource utilization.
