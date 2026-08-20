# A URN Namespace for the DoE IRI Project

# Abstract

This document defines an extensible URN structure for DoE Integrated Research Infrastructure (IRI) identifiers, following the guidelines in \[RFC8141\].

The proposed format provides stable, hierarchical identifiers for resource types and controlled vocabulary values without requiring revisions to the OpenAPI schema whenever a new subtype or controlled value is introduced. It separates data-model stability from the evolution of registered taxonomies.

The URN structure defined by this document is intended to be referenced by other IRI specifications, including the IRI `ResourceType` data-model definition. The URN structure can be extended to cover other IRI schema usages as required.

# Status of This Memo

This document defines a proposed URN structure for identifying typed IRI concepts, including resource types and controlled service vocabulary values.

This memo is intended for discussion and adoption within the DOE IRI specification and reference implementations.

| Revision | Author | Date | Notes |
| :---- | :---- | :---- | :---- |
| 0.1 | ChatGPT | Apr 23, 2026 | Initial version from John’s dank prompt. |
| 0.2 | John MacAuley | Apr 23, 2026 | Revised based on initial thoughts. |
| 0.3 | John MacAuley | May 7, 2026 | Split URN structure into a dedicated document. |
| 0.4 | John MacAuley | May 12, 2026 | Modified URN structure based on feedback. |
| 0.5 | John MacAuley | Jun 15, 2026 | Incorporated feedback. |
| 1.0 | John MacAuley | Jun 15, 2026 | Minted version 1.0. |
| 1.1 | John MacAuley | Aug 14, 2026 | Modified the service resource type to be under the resource URN. |

# Table of Contents

[Abstract](#abstract)

[Status of This Memo](#status-of-this-memo)

[Table of Contents](#table-of-contents)

[**1. Introduction**](#1-introduction)

[1.1. Requirements Language](#11-requirements-language)

[**2. URN Specification for "doe-iri" Namespace ID (NID)**](#2-urn-specification-for-"doe-iri"-namespace-id-\(nid\))

[2.1 Namespace ID](#21-namespace-id)

[2.2. Terminology](#22-terminology)

[2.3. Design Goals](#23-design-goals)

[2.4. Declaration of Syntactic Structure](#24-declaration-of-syntactic-structure)

[2.5 Category Values](#25-category-values)

[2.6 Category-Specific String Values](#26-category-specific-string-values)

[2.7. Hierarchical Semantics](#27-hierarchical-semantics)

[2.8. Comparison and Matching Rules](#28-comparison-and-matching-rules)

[2.8.1. Opaque Handling	](#281-opaque-handling)

[2.8.2. Exact Matching](#282-exact-matching)

[2.8.3. Prefix Matching	](#283-prefix-matching)

[**3. Initial Canonical URN Set**](#3-initial-canonical-urn-set)

[3.1. ResourceType URNs](#31-resourcetype-urns)

[3.2. AllocationUnit URNs](#32-allocationunit-urns)

[3.3. CompressionType URNs](#33-compressiontype-urns)

[**4. Delegated Extensions**](#4-delegated-extensions)

[**5. Registry Model**](#5-registry-model)

[5.1. Registry Name](#51-registry-name)

[5.2. Registry Authority](#52-registry-authority)

[5.3. Registry Purpose](#53-registry-purpose)

[5.4. Registry Entry Template](#54-registry-entry-template)

[5.5. Registration Policy](#55-registration-policy)

[5.6. Deprecation](#56-deprecation)

[**6. Validation**](#6-validation)

[**7. Security Considerations**](#7-security-considerations)

[7.1 Semantic Label Only](#71-semantic-label-only)

[7.2 Malformed Input](#72-malformed-input)

[7.3 Unsafe Parsing](#73-unsafe-parsing)

[7.4 Over-Interpretation](#74-over-interpretation)

[**8. Backward Compatibility**](#8-backward-compatibility)

[**9. IANA Considerations**](#9-iana-considerations)

[**10. References**](#10.-references)

[Appendix A. Example Registry Entries](#appendix-a-example-registry-entries)

# 1. Introduction

IRI interfaces need stable identifiers for concepts that may evolve over time. Resource typing is one such area: facilities may need to identify broad infrastructure classes such as compute, storage, network, website, system, and service resources, while also representing more specific concepts such as GPUs, scratch filesystems, object storage, DTN services, and inference services. Controlled vocabularies separately identify standardized characteristics such as a DTN service's implementation technology.

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
* **Category** means the top-level DOE-IRI registry branch, such as `resource` for resource types or `service` for controlled service attribute values.
* **Category-root URN** means a registered top-level DOE-IRI category such as `urn:doe-iri:resource` or `urn:doe-iri:storage`.
* **Category-specific string** means an additional narrowing segment within a semantic URN hierarchy.
* **Canonical URN** means a URN published by the IRI specification or registry as the preferred identifier for a type.  
* **Extension URN** means a URN that syntactically conforms to the explicit `ext` form defined in Section 2.4. This syntax-only term does not imply a registered authority, active scope delegation, or local definition.
* **Authority code** means a registered, stable, lowercase identifier for the organization that controls an explicitly delegated extension scope.
* **Scope-authorized Extension URN** means an Extension URN whose authority code is reserved and has an active scope delegation for its exact registered parent-and-authority pair.
* **Locally defined Extension URN** means a scope-authorized Extension URN whose delegated authority has assigned and documented its local suffix.
* **Assigned DOE-IRI extension** means a locally defined Extension URN that satisfies syntactic validity, scope authorization, and local definition.
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

The namespace-specific string (NSS) in the `urn:doe-iri` names hierarchy begins with a category identifier. A category-root URN may stand alone; a semantic URN may add a category-specific path; and an Extension URN uses the explicit delegation form. The following are ABNF productions compatible with RFC 5234:

```
DOE-IRI-URN = ADMINISTRATIVE-CATEGORY-ROOT-URN / SEMANTIC-CATEGORY-ROOT-URN / SEMANTIC-URN / EXTENSION-URN
ADMINISTRATIVE-CATEGORY-ROOT-URN = "urn:doe-iri:" EXTENSION-MARKER
SEMANTIC-CATEGORY-ROOT-URN = "urn:doe-iri:" SEMANTIC-CATEGORY
SEMANTIC-URN = SEMANTIC-CATEGORY-ROOT-URN ":" SEMANTIC-PATH
EXTENSION-URN = EXTENSION-PARENT ":" EXTENSION-MARKER ":" AUTHORITY ":" LOCAL-PATH
EXTENSION-PARENT = "urn:doe-iri" / SEMANTIC-CATEGORY-ROOT-URN / SEMANTIC-URN
SEMANTIC-CATEGORY = "allocation" / "compression" / "compute" / "resource" / "service" / "storage"
EXTENSION-MARKER = %x65.78.74
AUTHORITY = NON-EXT-AUTHORITY
SEMANTIC-PATH = NON-EXT-SEGMENT *( ":" NON-EXT-SEGMENT )
LOCAL-PATH = NON-EXT-SEGMENT *( ":" NON-EXT-SEGMENT )
NON-EXT-SEGMENT = 1*2SEGMENT-CHAR / NON-EXT-THREE-SEGMENT / 4*SEGMENT-CHAR
NON-EXT-THREE-SEGMENT = NON-E-SEGMENT-CHAR SEGMENT-CHAR SEGMENT-CHAR / %x65 NON-X-SEGMENT-CHAR SEGMENT-CHAR / %x65 %x78 NON-T-SEGMENT-CHAR
NON-EXT-AUTHORITY = 1*2AUTHORITY-CHAR / NON-EXT-THREE-AUTHORITY / 4*AUTHORITY-CHAR
NON-EXT-THREE-AUTHORITY = NON-E-AUTHORITY-CHAR AUTHORITY-CHAR AUTHORITY-CHAR / %x65 NON-X-AUTHORITY-CHAR AUTHORITY-CHAR / %x65 %x78 NON-T-AUTHORITY-CHAR
SEGMENT-CHAR = ALPHA / DIGIT / "-" / "." / "_" / "~"
AUTHORITY-CHAR = LOWER / DIGIT / "-"
NON-E-SEGMENT-CHAR = %x41-5A / %x61-64 / %x66-7A / DIGIT / "-" / "." / "_" / "~"
NON-X-SEGMENT-CHAR = %x41-5A / %x61-77 / %x79-7A / DIGIT / "-" / "." / "_" / "~"
NON-T-SEGMENT-CHAR = %x41-5A / %x61-73 / %x75-7A / DIGIT / "-" / "." / "_" / "~"
NON-E-AUTHORITY-CHAR = %x61-64 / %x66-7A / DIGIT / "-"
NON-X-AUTHORITY-CHAR = %x61-77 / %x79-7A / DIGIT / "-"
NON-T-AUTHORITY-CHAR = %x61-73 / %x75-7A / DIGIT / "-"
LOWER = %x61-7A
```

Where:

* **`urn`** is the literal URN prefix.  
* **`doe-iri`** is the namespace identifier.  
* **`<SEMANTIC-CATEGORY>`** identifies a semantic class of typed thing and anchors its category-specific path.
* **`<SEMANTIC-PATH>`** is a nonempty sequence of non-`ext` semantic segments that provides further qualification of the thing.
* **`<EXTENSION-MARKER>`** is the exact lowercase reserved segment `ext`.
* **`<AUTHORITY>`** is one syntactic lowercase authority-code segment; its registration is evaluated separately during scope authorization.
* **`<LOCAL-PATH>`** is one or more nonempty syntactic local segments; their delegated definition is evaluated separately.

`EXTENSION-MARKER` uses hexadecimal terminal values because quoted RFC 5234 ABNF strings are case-insensitive; it therefore matches only lowercase `ext`. `NON-EXT-SEGMENT` and `NON-EXT-AUTHORITY` exclude a segment exactly equal to lowercase `ext`, so a syntactically conforming Extension URN cannot also parse as a semantic URN and contains exactly one `ext` marker. `urn:doe-iri:ext` is the valid administrative category-root exception, not an Extension URN and not an extension parent.

An Extension URN MUST insert `ext` only at the namespace root or immediately after a semantic category-root URN or semantic URN as defined by the grammar. An authority code and a nonempty local path are REQUIRED syntactic segments. Every exact registered canonical semantic DOE-IRI URN is structurally eligible as an extension parent; the registry does not maintain a separate extension-point approval record. Scope authorization requires an authority-code reservation and an active scope delegation for the exact registered parent and authority. Local definition then completes assignment as a DOE-IRI extension.

## 2.5 Category Values

The initial semantic category names used by the ABNF above are registered in the following table. `ext` is separately registered as the administrative category-root exception.

This document defines the following initial category values:

| Category | Meaning |
| :---- | :---- |
| `allocation` | In HPC an allocation model defines how a facility grants, tracks, limits, and accounts for user or project access to shared computing, storage, and related resources over a defined period. |
| `compression` | Compression-related attributes used for compression or extraction of data. |
| `compute` | Controlled attribute vocabulary used to describe compute resources, including attributes such as configured counts, memory capacity, vendor, product, model, version, or clock frequency. |
| `ext` | Administrative delegation branch for registered authority codes and exact scope delegations; it is not a semantic controlled vocabulary. |
| `resource` | Resource types for physical, logical, or virtual infrastructure resources, including website and consumable service resources. |
| `service` | Controlled attribute vocabulary used to describe service resources, including service technologies, protocols, and APIs. |
| `storage` | Controlled attribute vocabulary used to describe storage resources, including storage abstractions, tiers, technologies, protocols, and related characteristics. |

Future semantic categories require a corresponding revision of the governing grammar and registry records.

## 2.6 Category-Specific String Values

The syntax and meaning of a **`<SEMANTIC-PATH>`** are dependent on the **`<SEMANTIC-CATEGORY>`** and MUST be defined by the IRI Interfaces Technical Subcommittee. The grammar in Section 2.4 restricts the lexical segment form and reserves lowercase `ext`; individual category registries define allowed semantic refinements.

In addition, we provide the following guidance when defining a **`<SEMANTIC-PATH>`**:

* MUST be non-empty.  
* SHOULD be short, stable, and semantically meaningful.  
* SHOULD avoid implementation-specific product names unless the type is intentionally identifying a product- or protocol-specific capability.

## 2.7. Hierarchical Semantics

Each additional segment in a semantic URN narrows the meaning of the type. The administrative `ext` category root, the Extension URN marker, and its authority segment are exceptions: they express delegation structure rather than semantic refinement.

For example:

```
urn:doe-iri:resource:compute
urn:doe-iri:resource:compute:node
urn:doe-iri:resource:compute:cpu
urn:doe-iri:resource:compute:gpu
```

The second, third, and fourth values are a subtype of the first value. Any relationship between the four URNs will be defined by the applicable category definition.

A producer MAY emit a parent type when a more specific subtype is unavailable, not applicable, sensitive, or intentionally hidden. A consumer SHOULD support fallback handling based on the nearest recognized parent type.

Clients MAY assume that intermediate semantic hierarchy levels of a URN have meaning if they have specific definitions.

For an Extension URN, ordinary segments before `ext` form the shared semantic hierarchy. The `ext` marker and its authority code are structural delegation segments, not semantic subtype segments. Prefix fallback stops at the nearest recognized shared parent before `ext`; for example, an unfamiliar `urn:doe-iri:resource:compute:ext:nersc:fpga` falls back to `urn:doe-iri:resource:compute`. A root-scope extension has no category-specific shared parent and therefore supports only opaque fallback when its local meaning is unknown.

Prefixes ending in `:ext` or `:ext:<authority>` MUST NOT be treated as resource types, controlled values, or semantic parent types. The suffix hierarchy beneath an active scope is defined by the delegated authority's documentation.

## 2.8. Comparison and Matching Rules

The following semantics apply to comparison and matching rules.

### 2.8.1. Opaque Handling

By definition, the IRI Type URN can be parsed for meaning, and therefore, is not opaque.

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
urn:doe-iri:resource:storage:filesystem
```

But `urn:doe-iri:resource:stor` is not a valid semantic parent of any type.

# 3. Initial Canonical URN Set

The following initial values are RECOMMENDED for the shared IRI registry to cover the existing enumeration definition. Only those enum definitions that need the flexibility to be expanded in the future are converted to URN.

## 3.1. ResourceType URNs

ResourceType is the normalized classification field used to describe the kind of facility resource represented by a Resource object.  In IRI and HPC facility terms, this lets clients distinguish major resource domains such as supercomputing systems and partitions, filesystems and storage services, facility-hosted APIs or portals, operational services, and network infrastructure.

The existing enum values map to canonical IRI Type URNs as follows:

| Legacy enum | Canonical IRI Type URN |
| :---- | :---- |
| `website` | `urn:doe-iri:resource:website` |
| `service` | `urn:doe-iri:resource:service` |
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

# 4. Delegated Extensions

The explicit `ext` form in Section 2.4 is the sole canonical mechanism for facility- or project-controlled DOE-IRI extensions. A facility-local extension MUST use the nearest accurate registered shared parent where possible. Root placement is permitted only through an explicit root-scope delegation and SHOULD be used only when no accurate shared semantic parent exists.

The following are syntactic Extension URNs defined by the specification. They do not imply that the illustrated authority currently holds the required scope delegation or has documented the local suffix.

```text
urn:doe-iri:ext:nersc:pdu:breaker
urn:doe-iri:resource:ext:nersc:scanner
urn:doe-iri:resource:compute:ext:nersc:fpga
```

An organization MUST first obtain an authority-code reservation and an active exact scope delegation before publishing or claiming an assigned DOE-IRI extension. An authority-code reservation identifies the organization and its change controller; it does not grant an insertion point. A scope delegation identifies the authority, exact registered parent, assigned prefix, and permitted semantic scope. An active scope grants the full nonempty local suffix subtree beneath its assigned prefix, but grants neither an adjacent parent scope nor any other extension point. The delegated authority's assignment and documentation of the local suffix supplies the required local definition.

Individual local leaves beneath an active delegated prefix do not require central registration. The delegated authority MUST document their local meaning. When a local value becomes useful across facilities, a new shared URN SHOULD be proposed. Promotion creates a new shared URN and MAY deprecate the former extension with explicit replacement guidance; the old identifier MUST NOT be repurposed.

# 5. Registry Model

## 5.1. Registry Name

The registry name SHOULD be:

**DOE-IRI URN Registry**

The registry SHOULD be located in the doe-iri GitHub repository:

`https://github.com/doe-iri`

## 5.2. Registry Authority

The IRI Interfaces Technical Subcommittee SHOULD maintain the registry as the IRI API governance body.

## 5.3. Registry Purpose

The registry provides:

* canonical shared URN values;  
* descriptions of type meaning;  
* parent-child relationships;  
* status information, such as active or deprecated;  
* replacement guidance when applicable;  
* examples of intended usage.

The registry SHOULD maintain authority-code reservations and exact scope-delegation records for Delegated Extensions.

## 5.4. Registry Entry Template

Each registry entry SHOULD include:

| Field | Description |
| :---- | :---- |
| URN | The canonical IRI Type URN. |
| Short name | A human-readable label. |
| Description | The semantic meaning of the type. |
| Parent URN | The parent type, if applicable. |
| Category | The category, such as `allocation`, `compression`, `resource`, or `service`. |
| Status | The lifecycle state, such as `active` or `deprecated`. |
| Change controller | The organization or process responsible for changes. |
| Examples | Representative use cases or payload examples. |
| Notes | Additional usage guidance. |

An authority-code reservation entry SHOULD additionally identify the authority code, organization, change controller, lifecycle status, and reference. A scope-delegation entry SHOULD identify the authority code, exact registered parent, assigned prefix, permitted semantic scope, lifecycle status, and reference. Authority codes are permanent reservations and MUST NOT be reassigned, including after deprecation.

## 5.5. Registration Policy

New shared URNs SHOULD be reviewed for:

* semantic clarity;  
* consistency with the existing hierarchy;  
* overlap with existing values;  
* cross-facility usefulness;  
* naming consistency;  
* backward compatibility with existing registered values.

An authority-code reservation plus an active exact parent-and-authority scope delegation gives an Extension URN scope authorization. The delegated authority's assignment and documentation of the local suffix completes its status as an assigned DOE-IRI extension. Local leaves beneath an active scope do not require central registration, but reusable cross-facility values SHOULD be proposed for shared registration. A producer MUST NOT claim a scope-unauthorized or undocumented Extension URN as an assigned DOE-IRI extension.

## 5.6. Deprecation

Registry entries MAY be marked deprecated.

A deprecated entry SHOULD include:

* the date or version in which it was deprecated;  
* the reason for deprecation;  
* a recommended replacement URN, if one exists;  
* migration guidance for producers and consumers.

If a proven legacy direct-form deployment is discovered, the registry MAY record only that exact legacy prefix or value as deprecated and name an explicit `ext` replacement. Such mappings preserve exact-string identity and MUST NOT define equivalence or authorize heuristic rewriting of segments that happen to match an authority code.

# 6. Validation

Validation has three distinct layers:

1. **Syntactic validity:** the value conforms to the DOE-IRI grammar and, when applicable, the Extension URN production in Section 2.4.
2. **Scope authorization:** an Extension URN's authority code is reserved and has an active delegation for its exact registered parent and authority pair.
3. **Local definition:** the delegated authority assigns and documents the meaning of the local suffix.

Systems that accept IRI Type URNs as input SHOULD validate syntax using the rules in Section 2\. A syntactically valid Extension URN without scope authorization is scope-unauthorized. A scope-authorized Extension URN without a local definition is scope-authorized but undocumented. Only an Extension URN that satisfies all three layers is an assigned DOE-IRI extension. Systems that publish assigned DOE-IRI extensions MUST satisfy all three layers.

General-purpose clients SHOULD NOT reject an unfamiliar syntactically valid extension solely because it is scope-unauthorized or undocumented; they SHOULD use shared-parent fallback or opaque handling. An API contract that requires assigned DOE-IRI values MAY reject either state explicitly.

# 7. Security Considerations

This document does not introduce a new authentication, authorization, or transport security mechanism.

However, the following considerations apply.

## 7.1 Semantic Label Only

An IRI Type URN is a semantic label. It is not an authorization artifact, proof of capability, or trust assertion.

Access control decisions MUST NOT rely solely on a type URN unless the value comes from a trusted server-side system of record and is evaluated as one input within a broader policy decision.

## 7.2 Malformed Input

Implementations that accept type URNs from clients SHOULD reject malformed values when the application context requires validation.

## 7.3 Unsafe Parsing

Implementations SHOULD treat type URNs as data, not executable input.

Systems that map URNs to database queries, policy rules, filesystem paths, class names, or code paths MUST treat URNs as untrusted user input, except when the value is sourced from a trusted system of record and conveyed in a manner resistant to tampering by all intermediate entities that handle it.

## 7.4 Over-Interpretation

A client MUST NOT assume that a previously unseen but syntactically valid subtype is invalid, malicious, or unusable solely because it is unfamiliar.

The correct behavior is to fall back to generic handling based on a known parent type or opaque-string handling.

# 8. Backward Compatibility

This document defines an extensible identifier structure. It does not, by itself, change any existing IRI API field.

Backward compatibility impacts are introduced only when another specification replaces a closed enumeration with an IRI Type URN string or otherwise requires use of this URN structure.

Specifications that adopt this document SHOULD describe their own migration and compatibility expectations.

The canonical Extension URN form replaces direct authority-code placement as a second syntax. No alias is created by this specification. If evidence establishes a deployed direct-form identifier, it requires an explicit deprecated mapping with an exact `ext` replacement; producers and clients MUST NOT heuristically rewrite it.

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
| `urn:doe-iri:resource:storage:filesystem` | Filesystem | `urn:doe-iri:resource:storage` | provisional | A logical storage resource with files, directories, and filesystem access semantics. |
| `urn:doe-iri:resource:service:dtn` | DTN Service | `urn:doe-iri:resource:service` | provisional | A consumable data-transfer service. |
| `urn:doe-iri:resource:service:inference` | Inference Service | `urn:doe-iri:resource:service` | provisional | A consumable model-invocation service. |
| `urn:doe-iri:service:dtn-technology:globus` | Globus DTN technology | `urn:doe-iri:service:dtn-technology` | provisional | A controlled attribute value identifying Globus as the DTN service technology or implementation. |
