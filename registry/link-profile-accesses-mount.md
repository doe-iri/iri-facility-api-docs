# Link Profile: `iri:accessesMount`

This document defines the `iri:accessesMount` relationship used by the DOE-IRI service resource model.

## 1. Relationship Metadata

| Field | Definition |
|---|---|
| Relationship | `iri:accessesMount` |
| Semantic meaning | Indicates that the source DTN service is configured to access a filesystem through the identified mount relationship resource for transfer operations. |
| Source representation type | `urn:doe-iri:resource:service:dtn` |
| Target representation type | `urn:doe-iri:resource:storage:mount` |
| Cardinality | `0..*` targets from a DTN service resource. |
| Target stability | Relatively static relationship resource. The target identifies configured filesystem access topology, not current mount availability, endpoint reachability, credential validity, unrestricted access, or transfer activity. |
| Authorization affects visibility | Yes. The relationship or individual mount targets MAY be omitted when the requester is not authorized to discover the configured access topology. |
| Target classification | Relationship resource |
| Relationship volatility | Relatively static configured access topology. Changes when DTN access configuration changes; operational mount and transfer state is separate. |

## 2. Semantic Meaning

The `iri:accessesMount` relationship indicates that the source DTN service is configured to access a filesystem through the identified mount relationship resource for transfer operations.

The target is a mount rather than a direct filesystem because the mount identifies the particular filesystem exposure and configuration through which the filesystem is accessed. It can carry information such as the mount path, access mode, protocol, mount options, and consuming-system relationship that does not belong solely to the filesystem resource.

The relationship MUST NOT be interpreted as indicating current mount availability, endpoint reachability, credential validity, unrestricted read or write access, or active transfer activity.

## 3. Source and Target Representation

The relationship MUST originate from a resource whose `resource_type` is:

```text
urn:doe-iri:resource:service:dtn
```

The relationship MUST target a resource whose `resource_type` is:

```text
urn:doe-iri:resource:storage:mount
```

The mount target is a relationship resource representing configured filesystem exposure. It is not a direct filesystem target, state object, operation entry point, or endpoint.

## 4. Cardinality

A DTN service MAY identify zero, one, or multiple mount resources:

```text
DTN Service  -- iri:accessesMount -->  Filesystem Mount
     1                   0..*
```

The use of `0..*` permits facilities to represent a DTN service without exposing configured mount access and to represent access to multiple filesystem exposures.

No inverse relation is initially registered. A visible mount does not by itself identify every service that can access it, and any future inverse relation requires a separate registration decision.

## 5. Static and Dynamic Semantics

`iri:accessesMount` describes relatively static configured access topology. The relationship SHOULD remain present across ordinary operational state changes such as temporary mount unavailability, endpoint failure, credential expiration, authorization changes, or periods without transfer activity.

Current mount status, endpoint reachability, credential validity, authorization outcomes, and active transfer activity SHOULD be represented through the applicable resource-state or transfer-state mechanisms.

## 6. Authorization and Visibility

Authorization MAY affect visibility of configured DTN access topology. A provider MAY expose a DTN service while omitting individual `iri:accessesMount` targets for requesters that are not permitted to discover the relevant mount or access configuration.

The absence of visible targets MUST NOT be interpreted as proof that the DTN service has no configured mount access.

## 7. Cross-Relation Guidance

Clients MUST use `iri:accessesMount` to discover configured DTN access to a filesystem exposure. The combination of `iri:hostedOn` and a mount resource's `iri:mountedOn` relationship MUST NOT be used to infer that a DTN service can access the mount, even when the service and mount are associated with the same compute infrastructure.

The mount target is more precise than a direct filesystem target because it identifies the particular exposure through which the DTN is configured to access the filesystem. A filesystem can have multiple mount relationship resources with different paths, protocols, access modes, or consuming systems.

## 8. HAL Representation

```json
{
  "_links": {
    "iri:accessesMount": [
      { "href": "/api/v2/status/resources/perlmutter-scratch-mount" },
      { "href": "/api/v2/status/resources/analysis-home-mount" }
    ]
  }
}
```

---

*DOE Integrated Research Infrastructure — Link Profile: accessesMount*
