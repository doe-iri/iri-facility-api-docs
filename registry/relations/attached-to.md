# IRI Link Relation: `attached-to`

**Relation URI:** `https://iri.science/rels/attached-to`<br>
**CURIE:** `iri:attached-to`<br>
**Status:** Draft<br>
**Version:** 1.0.0<br>
**Source representation type:** `urn:doe-iri:resource:storage:block`<br>
**Target representation type:** `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node`<br>
**Target representation profile:** `https://iri.science/profiles/resource-definition/compute/system` or `https://iri.science/profiles/resource-definition/compute/node`


This document defines the `iri:attached-to` relationship used by the DOE-IRI storage resource model.

The canonical relation URI is `https://iri.science/rels/attached-to`. With the
canonical IRI CURIE template `https://iri.science/rels/{rel}`,
`iri:attached-to` expands to that URI. The relation URI identifies the
semantics of this link relation; it is distinct from any RFC 6906 profile URI
associated with a target representation.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:attached-to` |
| Relation URI | `https://iri.science/rels/attached-to` |
| Semantic meaning | Indicates that a logical block-storage resource is configured to be presented or attached to the identified consuming compute resource. |
| Source representation type | `urn:doe-iri:resource:storage:block` |
| Target representation type | `urn:doe-iri:resource:compute:system` or `urn:doe-iri:resource:compute:node` |
| Cardinality | `0..1` for an `exclusive` block resource; `0..*` for a `shared` block resource. |
| Target stability | Static resource representation. The target identifies the consuming compute resource. Current attachment state is dynamic and MUST be represented separately. |
| Authorization affects visibility | Yes. Attachment topology MAY be filtered when the requester is not authorized to discover the consuming compute resource. |
| Target classification | Resource |
| Relationship volatility | Configuration/topology. This profile treats the link as configured/presented attachment, not as a live attached/detached state indicator. |

## 2. Semantic Meaning

The `iri:attached-to` relationship indicates that the source logical block-storage resource is configured to be presented or attached to the identified consuming compute system or compute node.

The relationship deliberately describes configured topology rather than current attachment state. This preserves the separation between relatively stable resource relationships and dynamic operational state.

Host-specific presentation details such as a local device path, device identifier, multipath status, or current attachment health do not belong on the target compute resource and SHOULD be represented through an attachment-specific representation or state mechanism if required.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:block
```

The relationship MAY target either:

```text
urn:doe-iri:resource:compute:system
```

or:

```text
urn:doe-iri:resource:compute:node
```

The target is the consuming compute resource definition, not a state object or operation entry point.

If future use cases require attachment-specific identity, configuration, lifecycle, or state, a dedicated block-attachment relationship resource SHOULD be introduced rather than overloading either the block or compute resource.

## 4. Cardinality

Cardinality depends on the block resource's `block_access_mode`.

For:

```text
urn:doe-iri:storage:block-access-mode:exclusive
```

the resource SHOULD have at most one configured consuming target:

```text
Block Storage  -- iri:attached-to -->  Compute Resource
      1                    0..1
```

For:

```text
urn:doe-iri:storage:block-access-mode:shared
```

the resource MAY identify multiple consuming targets:

```text
Block Storage  -- iri:attached-to -->  Compute Resource
      1                    0..*
```

A shared access mode indicates that multiple attachments are supported; it does not imply that arbitrary concurrent writes are safe.

## 5. Static and Dynamic Semantics

This link-relation definition defines `iri:attached-to` as configured or intended presentation topology.

The link MUST NOT be interpreted as a live assertion that the block device is currently attached, logged in, mapped, healthy, or accessible.

Current attachment status, active paths, device mapping, and I/O health are dynamic information and SHOULD be represented through the applicable state mechanism.

## 6. Authorization and Visibility

Authorization MAY affect attachment visibility because the relationship can reveal compute topology and storage-to-host associations.

A provider MAY omit targets that the requester is not authorized to discover. Absence of visible targets MUST NOT be interpreted as proof that the block resource has no configured attachments.

## 7. HAL Representation

Exclusive attachment example:

```json
{
  "_links": {
    "iri:attached-to": [
      { "href": "/api/v2/status/resources/compute-node-123" }
    ]
  }
}
```

Shared attachment example:

```json
{
  "_links": {
    "iri:attached-to": [
      { "href": "/api/v2/status/resources/compute-node-123" },
      { "href": "/api/v2/status/resources/compute-node-124" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Relation: attached-to*
