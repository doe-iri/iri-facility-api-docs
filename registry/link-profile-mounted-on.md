# Link Profile: `iri:mounted-on`

This document defines the `iri:mounted-on` relationship used by the DOE-IRI storage resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:mounted-on` |
| Semantic meaning | Identifies the consuming compute system on which the filesystem represented by the mount resource is exposed. |
| Source representation type | `urn:doe-iri:resource:storage:mount` |
| Target representation type | `urn:doe-iri:resource:compute:system` |
| Cardinality | Exactly `1` target for a valid mount resource. |
| Target stability | Static resource representation. The target identifies the consuming compute system; current mount status is represented separately as state. |
| Authorization affects visibility | Yes. The target MAY be hidden when the requester is not authorized to discover the consuming system or topology. |
| Target classification | Resource |
| Relationship volatility | Relatively static configuration/topology. It changes when the mount is redefined for a different consuming system, not when mount health changes. |

## 2. Semantic Meaning

The `iri:mounted-on` relationship identifies the consuming compute system whose filesystem namespace contains the exposure represented by the source mount resource.

The mount's own attributes describe how the filesystem is exposed—for example, `mount_path`, access mode, or filesystem protocol—while `iri:mounted-on` identifies the system to which those characteristics apply.

## 3. Source and Target Representation

The relationship MUST originate from:

```text
urn:doe-iri:resource:storage:mount
```

and MUST target:

```text
urn:doe-iri:resource:compute:system
```

The target is the compute-system resource definition, not its state object and not an operation endpoint.

## 4. Cardinality

A mount resource represents one filesystem exposure on one consuming system. A valid mount resource therefore MUST identify exactly one `iri:mounted-on` target:

```text
Mount  -- iri:mounted-on -->  Compute System
  1              1
```

If the same filesystem is exposed on multiple compute systems, separate mount resources SHOULD be used.

## 5. Static and Dynamic Semantics

The relationship describes configured topology, not current operational state.

The presence of `iri:mounted-on` means that the mount resource is defined in relation to the identified compute system. It does not mean that the mount is currently active or usable.

Mounted/unmounted status, accessibility, errors, or degradation SHOULD be represented in the mount's state representation.

## 6. Authorization and Visibility

Authorization MAY affect visibility of the target compute system.

When the source mount is visible but the consuming system is not discoverable by the requester, the provider MAY omit or otherwise restrict the relationship according to facility authorization policy.

Because `iri:mounted-on` is required for the semantic completeness of a mount resource, implementations SHOULD prefer to hide the mount resource itself when exposing it without its target would produce an unusable or misleading representation.

## 7. HAL Representation

```json
{
  "_links": {
    "iri:mounted-on": {
      "href": "/api/v2/status/resources/perlmutter"
    }
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: mountedOn*
