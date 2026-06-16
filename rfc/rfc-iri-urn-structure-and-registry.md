# A URN Namespace for the DoE IRI Project

# Abstract

This document defines an extensible URN structure for DoE Integrated Research Infrastructure (IRI) identifiers, following the guidelines in \[RFC8141\].

The proposed format provides a stable, hierarchical identifier for resource and service type values without requiring the OpenAPI schema to be revised whenever a new subtype is introduced. It separates the stability of the data model from the evolution of the type taxonomy.

The URN structure defined by this document is intended to be referenced by other IRI specifications, including the IRI `ResourceType` data-model definition. The URN structure can be extended to cover other IRI schema usages as required.

# Status of This Memo

This document defines a proposed URN structure for identifying typed IRI concepts, including resource and service types.

This memo is intended for discussion and adoption within the DOE IRI specification and reference implementations.

| Revision | Author | Date | Notes |
| :---- | :---- | :---- | :---- |
| 0.1 | ChatGPT | Apr 23, 2026 | Initial version from John’s dank prompt. |
| 0.2 | John MacAuley | Apr 23, 2026 | Revised based on initial thoughts. |
| 0.3 | John MacAuley | May 7, 2026 | Split URN structure into a dedicated document. |
| 0.4 | John MacAuley | May 12, 2026 | Modified URN structure based on feedback. |
| 0.5 | John MacAuley | Jun 15, 2026 | Incorporated feedback. |
| 1.0 | John MacAuley | Jun 15, 2026 | Minted version 1.0. |

# 

# Table of Contents

[Abstract](#abstract)

[Status of This Memo](#status-of-this-memo)

[Table of Contents](#table-of-contents)

[**1. Introduction**](#1-introduction)

[1.1. Requirements Language](#1-1-requirements-language)

[**2. URN Specification for "doe-iri" Namespace ID (NID)**](#2-urn-specification-for-"doe-iri"-namespace-id-\(nid\))

[2.1 Namespace ID](#2-1-namespace-id)

[2.2. Terminology](#2-2-terminology)

[2.3. Design Goals](#2-3-design-goals)

[2.4. Declaration of Syntactic Structure](#2-4-declaration-of-syntactic-structure)

[2.5 Domain Values](#2-5-domain-values)

[2.6 Domain Specific String Values](#2-6-domain-specific-string-values)

[2.7. Hierarchical Semantics](#2-7-hierarchical-semantics)

[2.8. Comparison and Matching Rules](#2-8-comparison-and-matching-rules)

[2.8.1. Opaque Handling	](#2-8-1-opaque-handling)

[2.8.2. Exact Matching](#2-8-2-exact-matching)

[2.8.3. Prefix Matching	](#2-8-3-prefix-matching)

[**3. Initial Canonical URN Set**](#3-initial-canonical-urn-set)

[3.1. ResourceType URNs](#3-1-resourcetype-urns)

[3.2. AllocationUnit URNs](#3-2-allocationunit-urns)

[3.3. CompressionType URNs](#3-3-compressiontype-urns)

[**4. Facility-Local Extensions**](#4-facility-local-extensions)

[**5. Registry Model**](#5-registry-model)

[5.1. Registry Name](#5-1-registry-name)

[5.2. Registry Authority](#5-2-registry-authority)

[5.3. Registry Purpose](#5-3-registry-purpose)

[5.4. Registry Entry Template](#5-4-registry-entry-template)

[5.5. Registration Policy](#5-5-registration-policy)

[5.6. Deprecation](#5-6-deprecation)

[**6. Validation**](#6-validation)

[**7. Security Considerations**](#7-security-considerations)

[7.1 Semantic Label Only](#7-1-semantic-label-only)

[7.2 Malformed Input](#7-2-malformed-input)

[7.3 Unsafe Parsing](#7-3-unsafe-parsing)

[7.4 Over-Interpretation](#7-4-over-interpretation)

[**8. Backward Compatibility**](#8-backward-compatibility)

[**9. IANA Considerations**](#9-iana-considerations)

[**10. References**](#10.-references)

[Appendix A. Example Registry Entries](#appendix-a-example-registry-entries)

# 1. Introduction

IRI interfaces need stable identifiers for concepts that may evolve over time. Resource and service typing is one such area: facilities may need to identify broad infrastructure classes such as compute, storage, network, website, and system resources, while also representing more specific concepts such as GPUs, scratch filesystems, object storage, Globus DTN services, XRootD services, and inference services.

A closed enumeration is difficult to evolve because every new type requires a schema change, implementation update, and downstream client regeneration. A URN-based approach \[RFC8141\] allows the schema to remain stable while the type taxonomy evolves through a governed registry.

A Uniform Resource Name (URN) is a Uniform Resource Identifier (URI) \[RFC3986\] that is assigned under the "urn" URI scheme and a particular URN namespace, with the intent that the URN will be a persistent, location-independent resource identifier.  A URN namespace is a collection of such URNs, each of which is (1) unique, (2) assigned in a consistent and managed way, and (3) assigned according to a common definition.

This document defines the IRI URN namespace, with common URN structure, hierarchy rules, validation expectations, and registry process for IRI-type URNs.

## 1.1. Requirements Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

# 2. URN Specification for "doe-iri" Namespace ID (NID)

## 2.1 Namespace ID

"doe-iri" (where "doe-iri" is an acronym for "Department of Energy Integrated Research Infrastructure").

## 2.2. Terminology

For the purposes of this document:

* **IRI Type URN** means a URN that conforms to the syntax defined by this document.  
* **Domain** means the class of typed thing, such as `resource` or `service`.  
* **Domain specific string** means an additional narrowing segment within the URN hierarchy.  
* **Canonical URN** means a URN published by the IRI specification or registry as the preferred identifier for a type.  
* **Facility-local URN** means a syntactically valid URN used by a facility before, or without, inclusion in the shared IRI registry.  
* **Registry** means the governed list of canonical IRI Type URNs and their semantics.

## 2.3. Design Goals

The IRI Type URN structure is intended to satisfy the following goals:

1. Allow new type identifiers to be introduced without changing OpenAPI schemas.  
2. Preserve interoperability for clients that only understand broad parent categories.  
3. Support precise typing for facilities that need additional specificity.  
4. Provide a stable basis for long-term taxonomy governance.  
5. Allow clients to degrade gracefully when they encounter a syntactically valid but unknown type.  
6. Avoid coupling client code generation to a closed vocabulary.

## 2.4. Declaration of Syntactic Structure

The formal syntax definitions below are given in ABNF \[RFC5234\].

The namespace-specific string (NSS) in the `urn:doe-iri` names hierarchy begins with a domain identifier (**`DOMAIN`**), followed by a delimiter and a domain-dependent string:

```
DOE-IRI-URN = "urn:doe-iri:" DOMAIN ":" DOMAIN-SPECIFIC-STRING
```

Where:

* **`urn`** is the literal URN prefix.  
* **`doe-iri`** is the namespace identifier.  
* **`<DOMAIN>`** identifies the class of typed thing, and anchor for the domain-specific string.  
* **`<DOMAIN-SPECIFIC-STRING>`** is an MANDATORY sequence of one or more domain specific segments providing further qualification of the thing.

## 2.5 Domain Values

**`<DOMAIN>`** has the same syntax as a **\<NID\>** as defined in \[RFC8141\]:

```
DOMAIN = ( ALPHA / DIGIT )  *31( ALPHA / DIGIT / "-" )
```

**ALPHA** and **DIGIT** are defined in Appendix B of \[RFC5234\].

This document defines the following initial `DOMAIN` values:

| Domain | Meaning |
| :---- | :---- |
| `allocation` | In HPC an allocation model defines how a facility grants, tracks, limits, and accounts for user or project access to shared computing, storage, and related resources over a defined period. |
| `compression` | Compression related attributes used for compression or extraction of data. |
| `resource` | A physical, logical, or virtual infrastructure resource. |
| `service` | A service capability, endpoint, API, or functional service exposed to users, workflows, or systems. |

Future **`<DOMAIN>`** values MAY be defined by a subsequent revision of this document or through an approved registry process.

## 2.6 Domain Specific String Values

The syntax of **`<DOMAIN-SPECIFIC-STRING>`** is dependent on the **`<DOMAIN>`** and MUST be defined by the IRI Interfaces Technical Subcommittee.  This document does not pose any additional restrictions to the **`<DOMAIN-SPECIFIC-STRING>`** other than what is defined in the NSS  
syntax as defined by \[RFC8141\] or its successor:

```
DOMAIN-SPECIFIC-STRING = 1*<URN chars>
```

**`<URN chars>`** is defined in Section 2.2 of \[RFC8141\].

In addition, we provide the following guidance when defining the **`<DOMAIN-SPECIFIC-STRING>`** token:

* MUST be non-empty.  
* SHOULD be short, stable, and semantically meaningful.  
* SHOULD avoid implementation-specific product names unless the type is intentionally identifying a product- or protocol-specific capability.

## 2.7. Hierarchical Semantics

Each additional URN segment narrows the meaning of the type.

For example:

```
urn:doe-iri:resource:compute
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu
```

The second, third, and fourth values are a subtype of the first value.  Any relationship between the four URNs will be defined by the domain definition.

A producer MAY emit a parent type when a more specific subtype is unavailable, not applicable, sensitive, or intentionally hidden. A consumer SHOULD support fallback handling based on the nearest recognized parent type.

Clients MAY assume that intermediate hierarchy levels of a URN have meaning, if they have specific definitions on their own.

## 2.8. Comparison and Matching Rules

The following semantics are defined for comparison and matching rules.

### 2.8.1. Opaque Handling

By definition the IRI Type URN can be parsed for meaning, and therefore, is not opaque.

A generic client MUST treat IRI Type URNs as opaque unless it explicitly implements parsing or hierarchy-aware matching.

A client MUST NOT reject a syntactically valid URN solely because it is not present in the client's local code or generated model.

### 2.8.2. Exact Matching

Exact matching compares the full URN string.

Clients MAY use exact matching when they need subdomain-specific behavior.

### 2.8.3. Prefix Matching 

Clients MAY use hierarchy-aware prefix matching to identify parent categories.

A hierarchy-aware prefix match MUST compare complete colon-delimited segments. A client MUST NOT treat arbitrary string prefixes as semantic parent matches.

For example:

```
urn:doe-iri:resource:storage
```

is a semantic parent of:

```
urn:doe-iri:resource:storage:filesystem:scratch
```

But `urn:doe-iri:resource:stor` is not a valid semantic parent of any type.

# 3. Initial Canonical URN Set

The following initial values are RECOMMENDED for the shared IRI registry to cover the existing enumeration definition. Only those enum definitions that need the flexibility to be expanded in the future are converted to URN.

## 3.1. ResourceType URNs

ResourceType is the normalized classification field used to describe the kind of facility resource represented by a Resource object.  In IRI and HPC facility terms, this lets clients distinguish major resource domains such as supercomputing systems and partitions, filesystems and storage services, facility-hosted APIs or portals, operational services, and network infrastructure.

The existing enum values map to canonical IRI Type URNs as follows:

| Legacy enum | Canonical IRI Type URN |
| :---- | :---- |
| `website` | `urn:doe-iri:service:website` |
| `service` | `urn:doe-iri:service:generic` |
| `compute` | `urn:doe-iri:resource:compute` |
| `system` | `urn:doe-iri:resource:system` |
| `storage` | `urn:doe-iri:resource:storage` |
| `network` | `urn:doe-iri:resource:network` |
| `unknown` | `urn:doe-iri:resource:unknown` |

## 3.2. AllocationUnit URNs

AllocationUnit is the controlled unit vocabulary used to express what kind of resource quantity is being granted and consumed in an IRI allocation record. In HPC facility terms, this lets the same allocation model represent compute allocations such as node-hours, storage capacity allocations such as bytes, and filesystem namespace/file-count quotas such as inodes.

The existing enum values map to canonical IRI Type URNs as follows:

| Legacy enum | Canonical IRI Type URN |
| :---- | :---- |
| `node-hours` | `urn:doe-iri:allocation:compute:node-hours` |
| `bytes` | `urn:doe-iri:allocation:storage:bytes` |
| `inodes` | `urn:doe-iri:allocation:storage:inodes` |

## 3.3. CompressionType URNs

CompressionType specifies the compression method used to compress or extract files.

The existing enum values map to canonical IRI Type URNs as follows:

| Legacy enum | Canonical IRI Type URN |
| :---- | :---- |
| `none` | `urn:doe-iri:compression:none` |
| `bzip2` | `urn:doe-iri:compression:bzip2` |
| `gzip` | `urn:doe-iri:compression:gzip` |
| `xz` | `urn:doe-iri:compression:xz` |

# 4. Facility-Local Extensions

Facilities MAY define local extensions that conform to the syntax in Section 2\.

Facility-local extensions SHOULD use the nearest accurate registered parent type where possible. When a local extension becomes useful across multiple facilities, it SHOULD be proposed for inclusion in the shared registry.

This document does not define a separate local namespace. Facility-local values, therefore, MUST still conform to the same syntax and validation rules unless a future revision defines a formal extension namespace.

To minimize the risk of accidental collision before formal registration, it is RECOMMENDED that facilities prefix the local segment of facility-local URNs with a registered facility or project identifier.

For example, the following URN identifies a facility specific **`DOMAIN`** type:

`urn:doe-iri:<facility-code>:pdu:breaker`

The following is an example of a URN that is semantically defined as a `resource` but is a facility-specific type of resource.

`urn:doe-iri:resource:<facility-code>:scanner`

Lastly, the following is an example of a URN that is semantically defined as a compute `resource` but is a facility-specific type of compute resource.

`urn:doe-iri:resource:compute:<facility-code>:fpga`

# 5. Registry Model

## 5.1. Registry Name

The registry name SHOULD be:

**DOE-IRI URN Registry**

The registry SHOULD be located in the doe-iri GitHub repository:

`https://github.com/doe-iri`

## 5.2. Registry Authority

The registry SHOULD be maintained by the IRI Interfaces Technical Subcommittee as the IRI API governance body.

## 5.3. Registry Purpose

The registry provides:

* canonical shared URN values;  
* descriptions of type meaning;  
* parent-child relationships;  
* status information, such as active or deprecated;  
* replacement guidance when applicable;  
* examples of intended usage.

The registry SHOULD also manage the allocation of facility codes needed for Facility-Local Extensions.

## 5.4. Registry Entry Template

Each registry entry SHOULD include:

| Field | Description |
| :---- | :---- |
| URN | The canonical IRI Type URN. |
| Short name | A human-readable label. |
| Description | The semantic meaning of the type. |
| Parent URN | The parent type, if applicable. |
| Domain | The domain, such as `allocation`, `compression`, `resource` or `service`. |
| Status | The lifecycle state, such as active or deprecated. |
| Change controller | The organization or process responsible for changes. |
| Examples | Representative use cases or payload examples. |
| Notes | Additional usage guidance. |

## 5.5. Registration Policy

New shared URNs SHOULD be reviewed for:

* semantic clarity;  
* consistency with the existing hierarchy;  
* overlap with existing values;  
* cross-facility usefulness;  
* naming consistency;  
* backward compatibility with existing registered values.

Facility-local URNs MAY be used before registry inclusion, but reusable cross-facility values SHOULD be proposed for shared registration.

## 5.6. Deprecation

Registry entries MAY be marked deprecated.

A deprecated entry SHOULD include:

* the date or version in which it was deprecated;  
* the reason for deprecation;  
* a recommended replacement URN, if one exists;  
* migration guidance for producers and consumers.

# 6. Validation

Systems that accept IRI Type URNs as input SHOULD validate syntax using the rules in Section 2\.

Systems that publish IRI Type URNs SHOULD emit syntactically valid values.

Systems MAY enforce registry membership in contexts where only canonical shared values are allowed. However, general-purpose IRI clients SHOULD NOT require registry membership unless the applicable API contract explicitly requires it.

# 7. Security Considerations

This document does not introduce a new authentication, authorization, or transport security mechanism.

However, the following considerations apply.

## 7.1 Semantic Label Only

An IRI Type URN is a semantic label. It is not an authorization artifact, proof of capability, or trust assertion.

Access control decisions MUST NOT rely solely on a type URN unless the value is sourced from a trusted server-side system of record and evaluated as one input within a broader policy decision.

## 7.2 Malformed Input

Implementations that accept type URNs from clients SHOULD reject malformed values where validation is required by the application context.

## 7.3 Unsafe Parsing

Implementations SHOULD treat type URNs as data rather than executable input.

Systems that map URNs to database queries, policy rules, filesystem paths, class names, or code paths MUST treat URNs as untrusted user input, except when the value is sourced from a trusted system of record and conveyed in a manner resistant to tampering by all intermediate entities that handle it.

## 7.4 Over-Interpretation

A client MUST NOT assume that a previously unseen but syntactically valid subtype is invalid, malicious, or unusable solely because it is unfamiliar.

The correct behavior is to fall back to generic handling based on a known parent type or opaque-string handling.

# 8. Backward Compatibility

This document defines an extensible identifier structure. It does not, by itself, change any existing IRI API field.

Backward compatibility impacts are introduced only when another specification replaces a closed enumeration with an IRI Type URN string or otherwise requires use of this URN structure.

Specifications that adopt this document SHOULD describe their own migration and compatibility expectations.

# 9. IANA Considerations

This document does not require action by IANA, however, in the future the IRI Interfaces Technical Subcommittee SHOULD consider creating an RFC to officially register the “**`urn:doe-iri`**” URN namespace in the [IANA namespace registry](https://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml).

# 10. References

* RFC 2119, **Key words for use in RFCs to Indicate Requirement Levels**.  
* RFC 8174, **Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words**.  
* RFC 8141, **Uniform Resource Names (URNs).**  
* RFC3986, **Uniform Resource Identifier (URI): Generic Syntax.**  
* RFC5234, **Augmented BNF for Syntax Specifications: ABNF.**

# Appendix A. Example Registry Entries

| URN | Short name | Parent URN | Status | Description |
| :---- | :---- | :---- | :---- | :---- |
| `urn:doe-iri:resource:compute` | Compute | `urn:doe-iri:resource` | active | A compute resource or compute resource collection. |
| `urn:doe-iri:resource:compute:gpu` | GPU | `urn:doe-iri:resource:compute` | active | A graphics processing unit or GPU-backed compute resource. |
| `urn:doe-iri:resource:storage:filesystem:scratch` | Scratch filesystem | `urn:doe-iri:resource:storage:filesystem` | active | A filesystem intended for scratch or temporary workflow storage. |
| `urn:doe-iri:service:dtn:globus` | Globus DTN service | `urn:doe-iri:service:dtn` | active | A data transfer node service exposed through Globus. |

