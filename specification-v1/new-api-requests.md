# 7. New API Requests

Any new API request goes through the maturity lifecycle within the Integrated Research Infrastructure (IRI) ecosystem.
Its goal is to prevent ambiguity about API maturity, stability, and implementation expectations across facilities.
Without an explicit maturity lifecycle, experimental endpoints can lead to inconsistent behavior, broken clients, and fragmentation across the federation.

---

## API Maturity Lifecycle Stages

An API progresses through the following stages:

| Stage            | Description                                     |
| ---------------- | ----------------------------------------------- |
| Undetermined     | To be defined/Unset. Used for new requests      |
| Planned          | In progress to define required API format/doc   |
| In Development   | Experimental ideas with no stability guarantees |
| Prototype        | Actively developed and stabilizing              |
| Beta Integration | Approved for upcoming adoption                  |
| Production Ready | Official stable specification                   |
| Retired          | Deprecated or discontinued                      |

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

### 1. Undetermined (undetermined)

**Purpose:** Submission state

Used when a proposal has been submitted but has not yet entered the formal lifecycle.

* Use the following form to submit a request and fill out all details. [Submit new request](https://github.com/doe-iri/iri-facility-api-docs/issues/new?template=newapi.yml).

### 2. Planned (planned)

**Purpose:** Early architectural idea.

Characteristics:

* RFC or proposal draft may exist
* Implementation may not exist
* Scope and semantics may change significantly

Typical uses:

* Early design proposals
* New architectural directions
* Conceptual capabilities

Requirements to enter:

* Initial review of the IRI team.
* Create a pull request to the concept directory with details related to the new API (directory name == issue id): document, proposal, or design document for this API.

### 3. In Development (in_development)

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

Requirements to enter:

* Specification draft exists
* Pass if at least 70% of the IRI team members with binding votes vote "In favor"

---

### 4. Prototype (prototype)

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

### 5. Beta Integration (beta)

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

### 6. Production Ready (production)

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

### 7. Retired (retired)

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
  maturity: production
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

### -> Undetermined

* Fill out the form with details

### Undetermined -> Planned

* Draft specification prepared

### Planned -> In Development

* Review completed

### In Development -> Prototype

* Initial implementation exists

### Prototype → Beta Integration

* Specification stabilized
* Community agreed on the usefulness
* Implementation experience documented

### Beta Integration → Production Ready

* Successful evaluation period
* No significant interoperability issues
* IRI governance formal approval

### Any Stage → Retired

* No adoption or active development
* Replaced by alternative
* Security or architectural concerns
* Other reasons

---

## Compliance Expectations

Facilities are expected to:

* Implement all Required Production APIs (with an exception of implementation level: optional, conditional. For not required, the facility can raise 501 Exception)
* Clearly advertise supported APIs
* Avoid presenting non-stable APIs as official endpoints
* Maintain backward compatibility for Production APIs

Clients SHOULD rely only on Production APIs unless explicitly opting into experimental features.