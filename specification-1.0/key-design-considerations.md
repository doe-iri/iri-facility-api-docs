## 8.1 Key Design Considerations
The design of the Facility Status API follows REST principles with an emphasis on clarity, interoperability, and extensibility. The following key considerations guided its development:

 - Resource-Oriented Structure: The API is organized around core domain entities such as Facility, Site, Location, Resource, Incident, and Event, each represented as a top-level REST resource with unique URIs and structured responses.
 - Standardized Schemas: All request and response bodies use well-defined OpenAPI schemas, enabling validation, consistent documentation, and compatibility with client code generators.
 - Hypermedia Linking: Resources include typed links (with rel, href, and type) to enable navigation across related entities (e.g., from a resource to its parent site or active incidents), supporting a hypermedia-driven approach.
 - Temporal and State Tracking: Each object includes fields like lastModified to support detection of change and standard If-Modified-Since capabilities.  Resources have operational state, and associated incidents or events to provide time-sensitive insights.
 - Error Handling: A consistent error structure is provided for all endpoints, ensuring predictable responses and easier client-side error handling.
 - Extensibility and Forward Compatibility: The schema design anticipates future additions by reserving fields, avoiding breaking changes, and supporting optional metadata where appropriate.