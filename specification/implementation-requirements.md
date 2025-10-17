# 5. Implementation Requirement

Implementation requirements are specific, actionable guidelines that define what needs to be done to develop, deploy, and successfully maintain a production instance of the Facility Status API.  These requirements are derived from high-level functional and non-functional requirements specified by stakeholders and IRI subcommittees that are to ensure the system meets its intended purpose.

1. Each facility status API deployment SHOULD implement OpenTelemetry to allow Jacques' IRI support teams to monitor/debug each API instance when performing troubleshooting activities, or for proactively identifying performance issues.

2. A JSON content type encoding must be made available as default output for the facility status API, with support for XML content type encodings as optional.

Security…

* Maintain up-to-date OS and software packages to reduce vulnerabilities.
* Firewall API server from critical resource infrastructure to reduce impact if server is compromised.