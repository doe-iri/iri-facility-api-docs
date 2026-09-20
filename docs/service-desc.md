---
layout: default
title: Understanding service-desc
parent: IRI 2.0
nav_order: 3
permalink: /service-desc/
---

# Understanding `service-desc`

The `service-desc` link relation provides a standard way for an IRI resource representation to advertise the machine-readable description of the API or service associated with that resource.

In an IRI HAL-style representation, `service-desc` is best understood as:

> **Where can a machine learn how this API works?**

It complements IRI-specific link relations, representation profiles, and relation-definition documents without replacing any of them.

> **Documentation status**
>
> This page is explanatory and its examples are illustrative rather than normative. Consult the governing IRI specification, OpenAPI description, registry entries, and RFCs for authoritative requirements.

---

## Canonical IRI OpenAPI vs. deployed OpenAPI

IRI distinguishes the portable API contract from the description of an actual
running service:

```text
                    Canonical IRI contract
             https://iri.science/api/v2/openapi.json
                            |
                    defines conformance
                            |
             +--------------+--------------+
             |                             |
             v                             v
        Facility A                    Facility B
             |                             |
        service-desc                   service-desc
             |                             |
             v                             v
      local OpenAPI                  local OpenAPI
```

The `iri.science` URL is the intended canonical publication URI for the IRI v2
contract; this documentation does not claim that it is already retrievable. A facility's
local OpenAPI document describes the service that is actually deployed.

The concise rule is:

```text
service-desc
    How does THIS deployed API work?

https://iri.science/api/v2/openapi.json
    What does IRI v2 define?
```

The deployed description matters because it can state the actual server URL,
deployed operations, security configuration, optional implemented
capabilities, facility extensions, actual version, and operational differences.
Those deployment details do not relax the canonical contract: an
implementation claiming IRI v2 conformance must still satisfy the applicable
canonical requirements.

An independently deployed facility therefore normally points `service-desc` at
its local OpenAPI description. The canonical document is appropriate only when
it accurately describes the service in that link context; linking to it does
not itself express conformance.

---

## 1. What is `service-desc`?

`service-desc` is a registered Web Linking relation defined by [RFC 8631](https://www.rfc-editor.org/rfc/rfc8631.html).

RFC 8631 defines `service-desc` as a relation that identifies a service description intended primarily for machine consumption. A typical target is an OpenAPI document.

For example:

```json
{
  "resource_id": "orion",
  "resource_type": "urn:doe-iri:resource:storage:filesystem",
  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/orion"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

The meaning of this link is:

> The API or service associated with this resource is described by the machine-readable document at `https://api.example.org/openapi.json`.

The `service-desc` link does **not** invoke an operation. It points to a description of the service.

---

## 2. How a client uses `service-desc`

Suppose a client retrieves:

```http
GET /api/v2/status/resources/orion
```

and receives a resource containing:

```json
{
  "_links": {
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

A capable client can:

1. Recognize `service-desc` as a standard registered link relation.
2. Follow the `href`.
3. Retrieve the service description.
4. Determine that the document is an OpenAPI description.
5. Parse the OpenAPI document.
6. Learn the API's paths, operations, HTTP methods, parameters, request schemas, response schemas, and security requirements.
7. Use that information when interacting with operation or resource links advertised by IRI representations.

Conceptually:

```text
IRI resource representation
          |
          | service-desc
          v
    OpenAPI document
          |
          +--> operations
          +--> HTTP methods
          +--> parameters
          +--> schemas
          +--> responses
          +--> security requirements
```

This is particularly useful for generic clients, workflow engines, MCP servers, and AI agents because they do not need prior knowledge of the facility's URL structure to locate the API contract.

---

## 3. `service-desc` is different from an operation link

An IRI resource may advertise operations through IRI-defined link relations:

```json
{
  "_links": {
    "iri:submit-job": {
      "href": "https://api.example.org/api/v2/compute/frontier/jobs"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

These links answer different questions.

| Link | Question answered |
|---|---|
| `iri:submit-job` | Where do I go to submit a job for this resource? |
| `service-desc` | Where can I learn the machine-readable contract for this API? |

`iri:submit-job` identifies an operational entry point.

`service-desc` identifies the description that explains how the API is used.

The two mechanisms are complementary.

---

## 4. `service-desc` is different from an IRI relation definition

IRI-specific link relations can use the IRI CURIE namespace:

```json
{
  "_links": {
    "curies": [
      {
        "name": "iri",
        "href": "https://iri.science/rels/{rel}",
        "templated": true
      }
    ],
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-orion-mount"
    }
  }
}
```

The CURIE:

```text
iri:has-mount
```

expands to a relation-definition URI such as:

```text
https://iri.science/rels/has-mount
```

That relation definition answers:

> **What does this relationship mean?**

By contrast:

```text
service-desc
      |
      v
https://api.example.org/openapi.json
```

answers:

> **How does the API associated with this resource work?**

These are separate layers:

```text
iri: relation definition
        |
        +--> semantics of the relationship

service-desc
        |
        +--> machine-readable API contract
```

---

## 5. `service-desc` is different from a representation profile

IRI links may also use a `profile` target attribute:

```json
{
  "_links": {
    "iri:has-mount": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-orion-mount",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/storage/mount"
    }
  }
}
```

The profile identifies the semantics or constraints of the representation expected at the link target.

This creates three distinct forms of machine-readable discovery:

| Mechanism | Purpose |
|---|---|
| IRI relation definition | Defines what a link relationship means |
| Target `profile` | Defines what the target representation means |
| `service-desc` | Describes how the surrounding API works |

Conceptually:

```text
                         IRI Resource
                             |
             +---------------+----------------+
             |               |                |
          iri:*            profile       service-desc
             |               |                |
             v               v                v
      Link semantics    Representation      OpenAPI
                            semantics       contract
```

This separation is useful because relationship semantics, representation semantics, and API mechanics are different concerns.

---

## 6. Why IRI should use the registered relation name

IRI representations should use:

```json
{
  "_links": {
    "service-desc": {
      "href": "https://api.example.org/openapi.json"
    }
  }
}
```

rather than defining an IRI-specific equivalent such as:

```json
{
  "_links": {
    "iri:service-desc": {
      "href": "https://api.example.org/openapi.json"
    }
  }
}
```

`service-desc` is already registered in the IANA Link Relation Type registry and has standardized semantics.

IRI-specific relation names should be reserved for relationships whose semantics are defined by IRI, for example:

```text
iri:has-mount
iri:submit-job
iri:provides-filesystem
```

Reusing registered relation types avoids creating unnecessary IRI-specific vocabulary and makes IRI representations easier for standards-aware generic clients to understand.

---

## 7. The `type` target attribute

A `service-desc` link can include a media-type hint:

```json
{
  "service-desc": {
    "href": "https://api.example.org/openapi.json",
    "type": "application/vnd.oai.openapi+json;version=3.1"
  }
}
```

The `type` value tells a client what representation it should expect when dereferencing the target.

The actual HTTP `Content-Type` returned by the server remains authoritative; the link's `type` attribute is a hint that allows a client to make a decision before retrieving the target.

For an AI agent or generic API client, this allows behavior such as:

```text
service-desc discovered
        |
        v
type indicates OpenAPI
        |
        v
retrieve description
        |
        v
parse OpenAPI
        |
        v
discover API operations and schemas
```

---

## 8. Where should `service-desc` appear?

A service can expose the same `service-desc` link from multiple resource representations.

For example:

```text
/storage/orion
      |
      +-- service-desc ----+
                           |
/compute/frontier          |
      |                    +----> /openapi.json
      +-- service-desc ----+
                           |
/network/esnet             |
      |                    |
      +-- service-desc ----+
```

This is consistent with RFC 8631, which allows `service-desc` to describe a resource or a set of resources.

For IRI, exposing `service-desc` directly from resource representations can be particularly useful because clients may discover or receive a resource URL without first visiting a facility-specific API root.

A client should not have to know that it must first navigate to a particular root endpoint merely to discover the machine-readable API contract.

Implementations may also expose `service-desc` from API roots, collection resources, or other appropriate entry points.

---

## 9. Example with several IRI links

A complete resource representation might look like:

```json
{
  "resource_id": "frontier",
  "name": "Frontier",
  "resource_type": "urn:doe-iri:resource:compute:system",

  "_links": {
    "self": {
      "href": "https://api.example.org/api/v2/status/resources/frontier"
    },

    "iri:has-node": {
      "href": "https://api.example.org/api/v2/status/resources/frontier-node-001",
      "type": "application/hal+json",
      "profile": "https://iri.science/profiles/resource-definition/compute/node"
    },

    "iri:submit-job": {
      "href": "https://api.example.org/api/v2/compute/job/frontier"
    },

    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

From this one representation, a client can discover:

- the canonical URI of the resource;
- related IRI resources;
- operation or interface entry points;
- representation profiles; and
- the machine-readable API description.

---

## 10. Why this matters for AI and MCP clients

One goal of hypermedia in IRI is to reduce the need for clients to construct or guess facility-specific URLs.

Without `service-desc`, an AI or MCP client might know that an operation link exists but still need out-of-band information describing:

- which HTTP method to use;
- what parameters are accepted;
- what request body is required;
- which schema applies;
- what authentication is required; and
- what responses or errors to expect.

With `service-desc`, the resource can advertise where that information is available.

For example:

```text
1. GET resource
        |
        v
2. Discover iri:submit-job
        |
        +------------------------------+
        |                              |
        v                              v
3. Operation URL                service-desc
                                       |
                                       v
                                OpenAPI contract
                                       |
                                       v
4. Determine method, request schema,
   authentication, and responses
        |
        v
5. Invoke advertised operation
```

This supports an important IRI design principle:

> Clients should discover operational paths and machine-readable contracts rather than infer or speculate about them.

---

## 11. `service-desc` versus `service-doc`

RFC 8631 also defines `service-doc`.

The distinction is based primarily on the intended consumer:

| Relation | Intended consumer | Typical target |
|---|---|---|
| `service-doc` | Human | HTML documentation, user guide |
| `service-desc` | Machine | OpenAPI or another structured service description |

An API may expose both:

```json
{
  "_links": {
    "service-doc": {
      "href": "https://docs.example.org/iri-api"
    },
    "service-desc": {
      "href": "https://api.example.org/openapi.json",
      "type": "application/vnd.oai.openapi+json;version=3.1"
    }
  }
}
```

This allows a human developer and a machine client to discover the documentation appropriate to each audience from the same resource representation.

---

## 12. Security considerations

Publishing a machine-readable service description makes systematic API discovery easier for both legitimate and malicious clients.

RFC 8631 therefore notes that service descriptions should expose only information necessary for use of the service and that consumers should not blindly trust service descriptions to be correct or current.

For IRI implementations:

- the OpenAPI description should accurately describe the deployed API;
- sensitive implementation details should not be exposed unnecessarily;
- authentication and authorization remain mandatory where required;
- discovering an operation does not imply authorization to perform it; and
- clients should continue to validate HTTP responses and server-provided media types.

`service-desc` improves discoverability; it does not replace normal API security controls.

---

## 13. Summary

For IRI, the role of `service-desc` can be summarized as:

```text
IRI relation
    --> What does this relationship mean?

profile
    --> What does this representation mean?

service-desc
    --> How does this API work?
```

Together, these mechanisms allow an IRI client to move from resource discovery to deterministic API interaction without depending on hard-coded facility URL conventions or out-of-band assumptions.

---

## References

- [RFC 8288 — Web Linking](https://www.rfc-editor.org/rfc/rfc8288.html)
- [RFC 8631 — Link Relation Types for Web Services](https://www.rfc-editor.org/rfc/rfc8631.html)
- [IANA Link Relation Types Registry](https://www.iana.org/assignments/link-relations/link-relations.xhtml)
- [HAL Specification](https://stateless.group/hal_specification.html)

## Related pages

- [Hypermedia and Discovery](hypermedia-and-discovery.md)
- [Core Concepts](core-concepts.md)
- [Implementation Guide](implementation-guide.md)
- [Examples](examples.md)
