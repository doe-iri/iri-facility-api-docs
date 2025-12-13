![Department of Energy - Office of Science](images/doe-logo.jpg)

**IRI Facility Interface Design Document**
---

**I2SC-02**  
**Draft**  
**October 2025**

Editor: John MacAuley

Contributors: Ilya Baldin, Bjoern Enders, Carol Hawk, Gabor Torok, Justas Balcas, Addi Malviya Thakur, Paul Rich, Scott Campbell, Xi Yang, Thomas Uram, Tyler J. Skluzacek

# OpenAPI specification for the Facility API suite **[openapi/](./openapi/)**

OpenAPI 3.1 was chosen for documentation of the REST API because it is fully compatible with JSON Schema 2020-12, 
which improves interoperability and validation in tooling. ([OpenAPI Initiative Publications][1])

Here is the OpenAPI definitions for the IRI Facility API (current agreed specifications):
- openapi_iri_facility_api_v1.json **[JSON](./openapi/openapi_iri_facility_api_v1.json)**
- openapi_iri_facility_api_v1.yaml **[YAML](./openapi/openapi_iri_facility_api_v1.yaml)**

Here is a draft OpenAPI definitions for the job submission and filesystem operations from NERSC:
- nersc-openapi-job-draft.json **[JSON](./openapi/nersc-openapi-job-draft.json)**

# Design Documentation

 - **[1. Introduction](./introduction.md)**
 - **[2. User Stories](./user-stories.md)**
 - **[3. User Requirements](./requirements.md)**
 - **[4. Design Requirements](design-requirements.md)**
 - **[5. Implementation Requirements](implementation-requirements.md)**
 - **[6. Conceptual Model](./conceptual-model.md)**
     - **[6.1 NamedObject](./conceptual-model.md#61-namedobject)**
     - **[6.2 Facility Model](./conceptual-model.md#62-facility-model)**
       - **[6.2.1 Facility](./conceptual-model.md#621-facility)**
       - **[6.2.2 Resource](./conceptual-model.md#622-resource)**
       - **[6.2.3 Site](./conceptual-model.md#623-site)**
       - **[6.2.4 Location](./conceptual-model.md#624-location)**
       - **[6.2.5 Relationships](./conceptual-model.md#625-relationships)**
     - **[6.3 Status Model](./conceptual-model.md#63-status-model)**
       - **[6.3.1 Incident](./conceptual-model.md#631-incident)**
       - **[6.3.2 Event](./conceptual-model.md#632-event)**
       - **[6.3.3 Resource](./conceptual-model.md#633-resource)**
       - **[6.3.4 Relationships](./conceptual-model.md#634-relationships)**
     - **[6.4 Allocation Model](./conceptual-model.md#64-allocation-model)**
       - **[6.4.1 Project](./conceptual-model.md#641-project)**
       - **[6.4.2 ProjectAllocation](./conceptual-model.md#642-projectallocation)**
       - **[6.4.3 UserAllocation](./conceptual-model.md#643-userallocation)**
       - **[6.4.4 Capability](./conceptual-model.md#644-capability)**
       - **[6.4.5 Resource](./conceptual-model.md#645-resource)**
       - **[6.4.6 Relationships](./conceptual-model.md#646-relationships)**
     - **[6.5 Job Model](./conceptual-model.md#65-job-model)**
     - **[6.6 Filesystem](./conceptual-model.md#66-filesystem-model)**

# REST API Specification

## 7. Facility Model
  - ### 7.1 Facility **[facility-facility.md](./facility-facility.md)**
  - ### 7.2 Sites **[facility-sites.md](./facility-sites.md)**
  - ### 7.3 Locations **[facility-locations.md](./facility-locations.md)**
  - ### 7.4 Resources **[status-resources.md](./status-resources.md)**
## 8. Status Model
   - ### 8.1 Events **[status-events.md](./status-events.md)**
   - ### 8.2 Incidents **[status-incidents.md](./status-incidents.md)**
## 9. Allocation Models **[account-model.md](./account-model.md)**
   - ### 9.1 Project **[account-projects.md](./account-projects.md)**
## 10. Job Model
  - ### **[10.1 DRAFT: Job](./job-job.md)**
## 11. Filesystem Model
  - ### **[11.1 DRAFT: Filesystem](./filesystem-filesystem.md)**

# Supporting Materials

## Images used within the document [images/](./images/)

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

*Last Updated: October 24, 2025*
