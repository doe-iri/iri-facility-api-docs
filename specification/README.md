![Department of Energy - Office of Science](images/doe-logo.jpg)

**IRI Facility Interface Design Document**
---

**I2SC-02**  
**Version 0.1**  
**November 2024**

Editor: John MacAuley

Contributors: Ilya Baldin, Bjoern Enders, Carol Hawk, Gabor Torok, Justas Balcas, Addi Malviya Thakur, Paul Rich, Scott Campbell, Xi Yang, Thomas Uram, Tyler J. Skluzacek


# Document Organization

The specification follows a logical progression:

1. **Introduction** (Section 1) - Provides an introduction to the problem.
2. **User Stories** (Section 2) - Establishes stakeholder needs and use cases
3. **Requirements** (Section 3) - Defines functional requirements derived from user stories
4. **Design Requirements** (Section 4) - Specifies architectural and design patterns
5. **Implementation Requirements** (Section 5) - Provides deployment and operational guidelines
6. **Model** (Section 6) - Details the data model and relationships
7. **Resource Specification** (Section 7) - Provides complete technical specification for the API `/resources`

# Contents

### 1. Introduction **[introduction.md](./status-user-stories.md)**

Introduction to the Facility Status API explaining its purpose and scope:
- Overview of programmatic access to facility operational status
- Information on scheduled maintenance/outage events
- Limited historical record capabilities
- Clarification on intended use cases (status checks vs. monitoring/reporting)

**1.1 Terminology**

Definitions of key terms used throughout the specification.

### 2. User Stories **[status-user-stories.md](./status-user-stories.md)**

User stories describing how different stakeholders interact with the IRI Facility Status API:
- Jinnette - Research Software Engineer designing application workflows
- Jean-Guy - RSE designing IRI visualization tool
- Jacques - Software engineer providing user support
- Sébastien - DoE facility security administrator
- Céline - DoE facility system administrator

### 3. Requirements **[status-requirements.md](./status-requirements.md)**

Detailed functional requirements for the facility status API including:
- API technology and resource exposure requirements [R1-R15]
- Search and query use cases
- Resource retrieval patterns

### 4. Design Requirements **[status-design-requirements.md](./status-design-requirements.md)**

- RESTful API design patterns
- Self-describing and navigable API
- OpenAPI documentation requirements

### 5. Implementation Requirements **[status-design-requirements.md](./status-design-requirements.md)**
- OpenTelemetry implementation
- Content type encodings (JSON/XML)
- Security guidelines

### 6. Facility and Status Models **[model.md](./model.md)**

The Facility and Status model defining core structure for IRI distributed infrastructure:
- Core object classes: Facility, Site, Location, Incident, Event, Resource
- Object relationships and cardinalities
- Model navigation and querying

**6.1 Relationships**
- Detailed relationship table between model objects
- Source/destination mappings
- Cardinality definitions

### 7. Resource **[status-resources.md](./status-resources.md)**

Comprehensive specification for Resource objects including:
- Resource overview and definition
- Attribute specifications and data types
- ENUM definitions (ResourceType, StatusType)
- Relationship mappings to other resources
- REST endpoint definitions
- Request/response semantics
- HTTP headers and parameters
- Query parameters and filtering
- Security model (OAuth 2.0)
- Example requests and responses
- Error handling (RFC 9457 Problem Details)
- OpenAPI 3.1 specification snippet
- Standards references and changelog

## Supporting Materials

### OpenAPI specification for the Facility API suite **[openapi/](./openapi/)**

 - openapi_iri_facility_api_v1.json **[JSON](./openapi/openapi_iri_facility_api_v1.json)**
 - openapi_iri_facility_api_v1.yaml **[YAML](./openapi/openapi_iri_facility_api_v1.yaml)**

### Images used within the document [images/](./images/)

Directory containing supporting images:
- `doe-logo.jpg` - DOE logo (JPEG format)
- `doe-logo.png` - DOE logo (PNG format)
- `facility-status-model.png` - Facility and Status Model diagram

## Standards Referenced

The specification references and adheres to the following standards:
- OpenAPI 3.1.0 (alignment with JSON Schema 2020-12)
- JSON Schema 2020-12
- RFC 9457 - Problem Details for HTTP APIs
- RFC 9110 - HTTP Semantics
- RFC 8288 - Web Linking
- RFC 6750 - OAuth 2.0 Bearer Token Usage
- ISO 8601 - Date and time format

---

*Last Updated: October 14, 2025*
