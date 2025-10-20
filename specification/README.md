![Department of Energy - Office of Science](images/doe-logo.jpg)

**IRI Facility Interface Design Document**
---

**I2SC-02**  
**Version 0.1**  
**November 2024**

Editor: John MacAuley

Contributors: Ilya Baldin, Bjoern Enders, Carol Hawk, Gabor Torok, Justas Balcas, Addi Malviya Thakur, Paul Rich, Scott Campbell, Xi Yang, Thomas Uram, Tyler J. Skluzacek

# OpenAPI specification for the Facility API suite **[openapi/](./openapi/)**

OpenAPI 3.1 was chosen for documentation of the REST API because it is fully compatible with JSON Schema 2020-12, 
which improves interoperability and validation in tooling. ([OpenAPI Initiative Publications][1])

Here is the OpenAPI definitions for the IRI Facility API:
- openapi_iri_facility_api_v1.json **[JSON](./openapi/openapi_iri_facility_api_v1.json)**
- openapi_iri_facility_api_v1.yaml **[YAML](./openapi/openapi_iri_facility_api_v1.yaml)**

# Contents

## 1. Introduction **[introduction.md](./introduction.md)**
## 2. User Stories **[user-stories.md](./user-stories.md)**
## 3. User Requirements **[requirements.md](./requirements.md)**
## 4. Design Requirements **[design-requirements.md](design-requirements.md)**
## 5. Implementation Requirements **[implementation-requirements.md](implementation-requirements.md)**
## 6. Facility and Status Models **[model.md](./model.md)**
   - ### 6.1 Resources **[status-resources.md](./status-resources.md)**
   - ### 6.2 Events **[status-events.md](./status-events.md)**
   - ### 6.3 Incidents **[status-incidents.md](./status-incidents.md)**
   - ### 6.4 Facility **[facility-facility.md](./facility-facility.md)**
   - ### 6.5 Sites **[facility-sites.md](./facility-sites.md)**
   - ### 6.6 Locations **[facility-locations.md](./facility-locations.md)**
## 7. Account Models **[account-model.md](./account-model.md)**
   - ### 7.1 Project **[account-projects.md](./account-projects.md)**

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

*Last Updated: October 14, 2025*
