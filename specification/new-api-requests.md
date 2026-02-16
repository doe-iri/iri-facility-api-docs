# 7. New API Requests

Any new API request goes through the maturity lifecycle within the Integrated Research Infrastructure (IRI) ecosystem.
Its goal is to prevent ambiguity about API maturity, stability, and implementation expectations across facilities.
Without an explicit maturity lifecycle, experimental endpoints can lead to inconsistent behavior, broken clients, and fragmentation across the federation.

---

## API Maturity Lifecycle Stages

An API progresses through the following stages:

| Stage     | Description                                     |
| --------- | ----------------------------------------------- |
| Sandbox   | Experimental ideas with no stability guarantees |
| Incubator | Actively developed and stabilizing              |
| Candidate | Approved for upcoming adoption                  |
| Graduated | Official stable specification                   |
| Archived  | Deprecated or discontinued                      |

## IRI API Vote process

Maturity lifecycle transitions for APIs in the IRI ecosystem are approved through a public vote using GitVote on the corresponding proposal issue/pull request.

* The start of the vote can be initiated by the IRI Committee.
* Only votes from designated IRI committee with binding voting rights are counted.
* Votes remain open for **30 calendar days** from the time the vote is initiated.
* The voting period may be extended if additional discussion or participation is needed.
* Voting may close early if: 1)the majority of voters have voted. 2) Closed early by the IRI Chair/Co-Chair.
* Votes use GitHub reactions on the issue/pull request:

| Reaction | Meaning   |
|----------|-----------|
| 👍       | In favor  |
| 👎       | Against   |
| 😕       | Abstain   |

A proposal passes if:

* At least **70% of counted votes are in favor**
* Abstentions do not count toward the percentage

---

### 1. Sandbox

**Purpose:** Innovation zone for new ideas and experimental capabilities.

Characteristics:

* May exist at zero or more facilities
* No stability guarantees
* Breaking changes allowed without notice
* Not intended for production use
* May never progress further

Typical uses:

* Novel capabilities
* Research prototypes
* Facility-specific experiments
* New architectural approaches

Requirements:

* Use the following form to submit a request and fill out all details. [Submit new request](https://github.com/doe-iri/iri-facility-api-docs/issues/new?template=newapi.yml).
* Create a pull request to the sandbox directory with details related to the new API: document, proposal, or design document for this API.

---

### 2. Incubator

**Purpose:** Refinement and validation of progressed APIs.

Characteristics:

* Specification draft exists
* At least one working implementation
* Behavior being validated across environments
* Optional for facilities
* Breaking changes allowed with spec update

Requirements to enter:

* Pass if at least 70% of the IRI team members with binding votes vote "In favor"
* Demonstrated usefulness
* Initial implementation
* Design review completed
* Community feedback incorporated

Goals:

* Resolve ambiguities
* Improve interoperability
* Validate real-world example

---

### 3. Candidate

**Purpose:** Preparation for broad adoption across all facilities.

Characteristics:

* Pass if at least 70% of the IRI team members with binding votes vote "In favor"
* Specification stable
* Agreement from IRI governance
* Facilities are encouraged to prepare implementations
* Only non-breaking changes expected
* Migration guidance provided if needed

Requirements to enter:

* Consensus that API should become official
* Multiple implementations or strong justification
* Test coverage and validation available
* Documentation complete

---

### 4. Graduated

**Purpose:** Official, stable IRI API.

Characteristics:

* Pass if at least 70% of the IRI team members with binding votes vote "In favor"
* Considered production-ready
* Backward compatibility expected
* Changes will follow versioning policy
* Suitable for long-term client development
* It is Official IRI specification

Graduated APIs may still be optional if not all facilities can implement this. See "Specification Metadata" section. TODO

Requirements to enter:

* Successful Candidate period
* No major unresolved issues
* Governance approval
* Clear operational semantics

---

### 5. Archived

**Purpose:** Retirement of obsolete or unsuccessful APIs.

Characteristics:

* Pass if at least 70% of the IRI team members with binding votes vote "In favor"
* No longer recommended for use
* May remain implemented at some facilities
* No maintenance guarantees
* Replacement (if any) documented

Reasons for archival:

* Lack of adoption
* Superseded by newer API
* Security or design limitations
* Maintenance issues
* Other

---

## Implementation Status

Maturity Lifecycle stage describes API maturity, not deployment obligation.

Each API operation MUST declare its implementation status:

| Status      | Meaning                                              |
| ----------- | ---------------------------------------------------- |
| Required    | All facilities must implement                        |
| Optional    | Implement if applicable                              |
| Conditional | Required only when specific capabilities are present |

---

## Capability-Based Requirements

Some APIs apply only to facilities with specific capabilities.

Examples:

* GPU, DPU available
* Specialized storage systems
* Cloud capability
* Experimental hardware

Conditional requirement example: **Required if facility advertises capability: dpu-compute**

---

## Maturity lifecycle and capability implementation

Maturity lifecycle and implementation status SHOULD be encoded as OpenAPI extensions:

```yaml
x-iri:
  maturity: graduated
  implementation:
    level: optional
```

Optional extended form:

```yaml
x-iri:
  maturity: candidate
  implementation:
    level: conditional
    required_if_capability: dpu-compute
```

This enables automated validation and discovery.

---

## Advancement Criteria

Transitions between stages require approval from the IRI governance.

### -> Sandbox

* Fill out the form with details

### Sandbox -> Incubator

* Draft specification prepared
* Initial implementation exists
* Review completed

### Incubator → Candidate

* Specification stabilized
* Community agreed on usefulness
* Implementation experience documented

### Candidate → Graduated

* Successful evaluation period
* No significant interoperability issues
* IRI governance formal approval

### Any Stage → Archived

* No adoption or active development
* Replaced by alternative
* Security or architectural concerns
* Other reasons

---

## Compliance Expectations

Facilities are expected to:

* Implement all Required Graduated APIs (with an exception of implementation level: optional, conditional. For not required, the facility can raise 501 Exception)
* Clearly advertise supported APIs
* Avoid presenting non-stable APIs as official endpoints
* Maintain backward compatibility for Graduated APIs

Clients SHOULD rely only on Graduated APIs unless explicitly opting into experimental features.
