# RFC: Persistent Services

## Abstract

The IRI Facility API currently focuses on batch compute, storage, and inference services. Many facilities also operate persistent container orchestration platforms, primarily Kubernetes (k8s), that enable users to deploy long-running services, interactive workloads, and custom applications. These platforms typically organize infrastructure hierarchically (servers/clusters, namespaces, projects) and expose a native Kubernetes API for workload management.

This RFC proposes a minimal IRI API extension for discovering and accessing facility-operated Kubernetes infrastructure in multi-cluster and multi-tenant environments. The IRI API provides navigation to available servers and clusters, namespace provisioning, and kubeconfig generation for authenticated access to the native Kubernetes API. The actual workload management (deployments, services, pods, volumes, etc.) remains the responsibility of the Kubernetes API itself.

This proposal does not change existing IRI resource types, batch job submission, or storage access patterns. It introduces a new `/api/v2/persistent_service` endpoint hierarchy with maturity status `planned`.

## Status of This Memo

**Status:** Draft / Proposed

**Target:** IRI Facility API v2 and DOE-IRI URN Registry

| Revision | Author | Date | Notes |
|---|---|---|---|
| 0.1 | Gabor Torok | Nov 10, 2026 | Initial draft. |

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Terminology](#3-terminology)
4. [API Overview](#4-api-overview)
5. [Server Discovery](#5-server-discovery)
6. [Cluster Discovery](#6-cluster-discovery)
7. [Project Discovery](#7-project-discovery)
8. [Namespace Provisioning](#8-namespace-provisioning)
9. [Kubeconfig Generation](#9-kubeconfig-generation)
10. [Authentication and Authorization](#10-authentication-and-authorization)
11. [Security Considerations](#11-security-considerations)
12. [Alternatives Considered](#12-alternatives-considered)
13. [Future Work](#13-future-work)
14. [Required Specification and Registry Changes](#14-required-specification-and-registry-changes)
15. [References](#15-references)
- [Appendix A. Examples](#appendix-a-examples)

## 1. Introduction

Department of Energy facilities increasingly operate Kubernetes platforms to support:

- **Persistent services**: Long-running applications, databases, web services, and APIs that complement batch workloads.
- **Interactive development**: Jupyter notebooks, IDEs, and interactive compute environments that remain available between sessions.
- **Custom tooling**: Facility-specific or experiment-specific tools that require persistent deployment.
- **Microservice architectures**: Distributed applications spanning multiple containers with complex networking and orchestration needs.

Unlike batch jobs submitted through the IRI job API, these workloads:

1. Run indefinitely until explicitly stopped.
2. Require direct interaction with the orchestration platform (scaling, service exposure, configuration updates).
3. Benefit from Kubernetes-native tooling (kubectl, Helm, operators).

The IRI API does not aim to replicate the full Kubernetes API. Instead, it addresses the **discovery and access** problem in multi-cluster, multi-tenant environments:

- **Which Kubernetes servers does this facility operate?**
- **Which clusters am I authorized to use?**
- **How do I obtain valid credentials for a specific cluster?**
- **How do I provision a new namespace within quota?**

Once a user has a kubeconfig, they interact with Kubernetes through its native API, tooling, and ecosystem.

## 2. Scope

In scope:

- Discovery of available Kubernetes servers and clusters.
- Discovery of existing projects (multi-tenancy groupings within clusters).
- Namespace creation for authorized users within a cluster.
- Kubeconfig file generation with time-limited, user-scoped credentials.
- Authentication delegation to the existing IRI token mechanism.
- Authorization enforcement based on facility policy (which users can access which clusters and namespaces).

Out of scope:

- Kubernetes workload submission, management, or lifecycle (deployments, pods, services, volumes, jobs, CronJobs).
- Kubernetes resource quota management (handled by Kubernetes RBAC and resource quota objects).
- Non-Kubernetes orchestration platforms (Docker Swarm, Nomad, etc.).
- Replacing or deprecating the existing batch job submission API.
- IRI v1 (this RFC targets IRI v2 only).
- HAL links or Resource representation for Kubernetes objects (clusters, namespaces, projects, and servers are accessed through dedicated endpoints, not the IRI Resource model).
- Project provisioning or management (projects are created and managed by facility administrators using facility-specific tools).

## 3. Terminology

- **Persistent service**: A long-running containerized workload deployed on a container orchestration platform, typically Kubernetes.
- **Server**: A Kubernetes API endpoint or logical grouping of clusters operated by a facility. May correspond to a single Kubernetes installation or a federated set of clusters.
- **Cluster**: A distinct Kubernetes cluster with its own control plane, typically identified by a unique name or context.
- **Namespace**: A Kubernetes namespace providing resource isolation and quota enforcement within a cluster.
- **Project**: A multi-tenancy abstraction layer above namespaces, similar to Rancher projects or OpenShift projects. Projects group and isolate resources for different teams or organizational units. Namespaces are created within projects. Facilities that do not implement a project system SHOULD return a default project for each user.
- **Kubeconfig**: A YAML configuration file containing cluster connection details, authentication credentials, and context definitions, used by kubectl and other Kubernetes clients.

## 4. API Overview

The persistent services API introduces the following endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v2/persistent_service/servers` | GET | List available Kubernetes servers. |
| `/api/v2/persistent_service/servers/{server_id}/clusters` | GET | List clusters within a server. |
| `/api/v2/persistent_service/servers/{server_id}/clusters/{cluster_id}/projects` | GET | List projects the user can access within a cluster. |
| `/api/v2/persistent_service/servers/{server_id}/clusters/{cluster_id}/namespaces` | POST | Create a new namespace within a cluster. |
| `/api/v2/persistent_service/servers/{server_id}/kubeconfig` | POST | Generate a kubeconfig file for accessing a server or specific clusters. |

All endpoints:

- Require authentication via the IRI bearer token mechanism (`HTTPBearer` security scheme).
- Return standard IRI problem responses for errors (4xx, 5xx).
- Use `x-iri.maturity: planned` to indicate evolving status.

## 5. Server Discovery

### 5.1. Endpoint

**GET** `/api/v2/persistent_service/servers`

### 5.2. Purpose

List Kubernetes servers operated by the facility that the authenticated user is authorized to access.

### 5.3. Response

Returns a `ServerList` containing zero or more server entries. Each server entry includes:

- `server_id`: Unique identifier for the server.
- `name`: Human-readable server name.
- `description` (optional): Additional information about the server's purpose, location, or capabilities.

### 5.4. Semantics

- A **server** represents a logical grouping of Kubernetes clusters. It may correspond to a single Kubernetes deployment, a federated cluster set, or a geographical region.
- Servers returned MUST be those for which the user has at least read access to one cluster.
- Facilities MAY organize clusters into servers by geography, security boundary, resource type, or administrative domain.

## 6. Cluster Discovery

### 6.1. Endpoint

**GET** `/api/v2/persistent_service/servers/{server_id}/clusters`

### 6.2. Purpose

List Kubernetes clusters within a given server that the authenticated user is authorized to access.

### 6.3. Path Parameters

- `server_id` (required): The identifier of the server returned from the `/servers` endpoint.

### 6.4. Response

Returns a `ClusterList` containing zero or more cluster entries. Each cluster entry includes:

- `cluster_id`: Unique identifier for the cluster within this server.
- `name`: Human-readable cluster name.
- `description` (optional): Additional information about the cluster's purpose, capacity, or policies.
- `endpoint` (optional): The Kubernetes API server URL for this cluster, if directly accessible.

### 6.5. Semantics

- A **cluster** represents a distinct Kubernetes control plane with its own namespaces, nodes, and resource quotas.
- Clusters returned MUST be those for which the user has authorization to view or create namespaces.
- The `endpoint` URL, if present, SHOULD match the server URL that will appear in the generated kubeconfig.

## 7. Project Discovery

### 7.1. Endpoint

**GET** `/api/v2/persistent_service/servers/{server_id}/clusters/{cluster_id}/projects`

### 7.2. Purpose

List projects the authenticated user can access within a specific cluster. Projects provide a multi-tenancy layer for organizing and isolating namespaces. Users must select a project before creating namespaces within it.

### 7.3. Path Parameters

- `server_id` (required): The server identifier.
- `cluster_id` (required): The cluster identifier within that server.

### 7.4. Response

Returns a `ProjectList` containing zero or more project entries. Each project entry includes:

- `project_id`: Unique identifier for the project within this cluster.
- `name`: Human-readable project name (often corresponding to a Kubernetes namespace name).
- `description` (optional): Additional information about the project.

### 7.5. Semantics

- A **project** is a multi-tenancy construct that groups and isolates namespaces, similar to Rancher projects or OpenShift projects.
- Projects returned MUST be those for which the user has been granted access by facility policy.
- For facilities that do not implement a project system, this endpoint SHOULD return a single default project (e.g., with `project_id: "default"`) for each user.
- This endpoint is informational; it does not provision new projects. Project provisioning is facility-specific and outside the scope of this RFC.

## 8. Namespace Provisioning

### 8.1. Endpoint

**POST** `/api/v2/persistent_service/servers/{server_id}/clusters/{cluster_id}/namespaces`

### 8.2. Purpose

Create a new Kubernetes namespace within a cluster, subject to facility authorization and quota policies.

### 8.3. Path Parameters

- `server_id` (required): The server identifier.
- `cluster_id` (required): The cluster identifier within that server.

### 8.4. Request Body

JSON object conforming to `NamespaceCreateRequest`:

- `project_id` (required): The project identifier within which to create the namespace. MUST be a valid project ID from the projects endpoint.
- `name` (required): The desired namespace name. MUST conform to Kubernetes namespace naming rules (lowercase alphanumeric, hyphens, max 63 characters).
- `description` (optional): Human-readable description for the namespace.
- Additional facility-specific fields MAY be accepted (such as quota requests, labels, or annotations).

### 8.5. Response

On success (HTTP 200), returns a `Namespace` object representing the newly created namespace:

- `namespace_id`: Unique identifier assigned by the facility.
- `name`: The namespace name.
- `cluster_id`: The cluster to which the namespace belongs.
- `status`: Current state (e.g., `active`, `pending`).
- Additional metadata as defined by the facility.

### 8.6. Semantics

- The facility MUST validate that the authenticated user is authorized to create namespaces in the specified project within the cluster.
- The facility MUST validate that the `project_id` is valid and accessible to the user.
- Namespaces created within a project inherit the project's policies, quotas, and access controls as defined by the facility's multi-tenancy implementation.
- The facility MAY enforce additional naming conventions, quotas, or approval workflows.
- Namespace creation MAY be synchronous or asynchronous. If asynchronous, the initial `status` should indicate `pending`.
- On conflict (namespace already exists in the project), the facility SHOULD return HTTP 409.

### 8.7. Authorization and Quotas

- The facility enforces who can create namespaces in which projects through its own authorization policy.
- Projects typically define resource quotas and limits that apply to all namespaces within them.
- Additional per-namespace quotas are typically managed through Kubernetes ResourceQuota and LimitRange objects, not through this API.

## 9. Kubeconfig Generation

### 9.1. Endpoint

**POST** `/api/v2/persistent_service/servers/{server_id}/kubeconfig`

### 9.2. Purpose

Generate a kubeconfig file containing credentials and connection details for accessing one or more clusters within a server.

### 9.3. Path Parameters

- `server_id` (required): The server identifier.

### 9.4. Request Body

JSON object conforming to `KubeconfigRequest`:

- `clusters` (optional): Array of cluster IDs for which to include configuration. If omitted, the facility MAY include all clusters the user is authorized to access within the server, or MAY return an error requiring explicit cluster selection.
- `validity` (optional): Requested credential validity duration (e.g., in seconds or ISO 8601 duration). The facility MAY ignore this and apply its own policy.

### 9.5. Response

On success (HTTP 200), returns a kubeconfig file in YAML format (`application/yaml`, `format: binary`).

The kubeconfig MUST contain:

- `clusters`: Cluster definitions with server URLs and certificate authority data.
- `users`: User authentication credentials (tokens, certificates, or external auth provider configuration).
- `contexts`: Named contexts associating clusters with users and optional default namespaces.
- `current-context` (optional): A default context for convenience.

### 9.6. Semantics

- Credentials SHOULD be **time-limited** and scoped to the authenticated user.
- The facility MAY use token-based authentication, client certificates, or external authentication plugins (such as OIDC or exec-based credential providers).
- Credentials SHOULD NOT be long-lived static tokens.
- The generated kubeconfig SHOULD be suitable for use with `kubectl`, Kubernetes client libraries, and other standard tooling.

### 9.7. Credential Lifecycle

- The facility MAY issue credentials valid for minutes, hours, or days, depending on security policy.
- Users SHOULD be able to request new kubeconfigs when credentials expire.
- The facility SHOULD document credential lifetime and renewal procedures.

## 10. Authentication and Authorization

### 10.1. IRI Token Authentication

All persistent services endpoints use the existing IRI bearer token authentication mechanism. Users obtain tokens through the standard IRI authentication flow and include them in the `Authorization: Bearer <token>` header.

### 10.2. Authorization Model

The facility determines:

- Which users can see which servers and clusters.
- Which users can create namespaces, and in which clusters.
- What permissions the generated kubeconfig grants within the Kubernetes cluster (via Kubernetes RBAC).

This RFC does not prescribe a specific authorization model. Facilities MAY use:

- IRI project membership.
- IRI allocations or capabilities.
- External systems (LDAP, institutional identity providers).
- Kubernetes-native RBAC bound to user identity.

### 10.3. Credential Scoping

Kubeconfig credentials SHOULD be scoped to:

- The authenticated IRI user.
- The requested clusters.
- A limited time window.

The facility SHOULD map the IRI user identity to a Kubernetes user or service account with appropriate RBAC bindings.

## 11. Security Considerations

### 11.1. Credential Lifetime

Long-lived static credentials pose a security risk. Facilities SHOULD issue time-limited credentials and support automated renewal.

### 11.2. Namespace Isolation

Kubernetes namespaces provide logical isolation but share a cluster-level control plane. Sensitive workloads SHOULD use dedicated clusters or additional isolation mechanisms (such as pod security policies, network policies, or sandboxing).

### 11.3. API Server Access

Exposing Kubernetes API servers to wide network access increases attack surface. Facilities SHOULD:

- Restrict API server access to authorized networks.
- Use TLS with valid certificates.
- Enforce authentication and RBAC on all API requests.

### 11.4. Quota Enforcement

Without resource quotas, users can exhaust cluster resources. Facilities SHOULD enforce Kubernetes ResourceQuota and LimitRange policies on all user-created namespaces.

### 11.5. Audit Logging

Kubernetes audit logs SHOULD be enabled to track API access and modifications. The IRI API SHOULD log namespace creation and kubeconfig generation events.

## 12. Alternatives Considered

### 12.1. Full Kubernetes API Integration

**Rejected.** Proxying the full Kubernetes API through the IRI API would duplicate functionality, complicate implementation, and prevent use of native Kubernetes tooling.

### 12.2. Extending IRI Job API for Persistent Workloads

**Rejected.** Persistent services have fundamentally different lifecycle semantics (indefinite runtime, interactive management, complex orchestration) that do not fit the batch job model.

### 12.3. HAL Links and Resource Model

**Considered but deferred.** Future work may integrate persistent services with the IRI Resource model and HAL links, but this RFC focuses on establishing the minimal access and provisioning API first.

### 12.4. Direct Kubeconfig Distribution

**Rejected.** Distributing static kubeconfigs out-of-band (email, web portals) does not integrate with IRI authentication, does not support dynamic credential issuance, and complicates automation.

## 13. Future Work

### 13.1. Resource Type and Profile Integration

The [DOE-IRI URN Registry](../registry/urns/README.md) records the following Resource Type URNs for persistent services (in `provisional` status while this RFC is under review):

- `urn:doe-iri:resource:persistent-service:kubernetes-server`
- `urn:doe-iri:resource:persistent-service:kubernetes-cluster`
- `urn:doe-iri:resource:persistent-service:project`

A future RFC may define:

- Resource Definition Profiles for these resource types.
- HAL links from servers to cluster lists, from clusters to project lists and kubeconfig generation, and from projects to namespace operations.

### 13.2. Allocation Unit for Persistent Services

Facilities may track persistent service consumption in pod-hours, memory-hours, or cluster time. A future RFC may register allocation units for these.

### 13.3. Multi-Cluster Federation

Some facilities operate federated Kubernetes environments (KubeFed, multi-cluster service mesh). Future work may extend the server/cluster model to reflect federation topology.

### 13.4. Interactive Workload Discovery

Future work may define how persistent services relate to interactive jobs, Jupyter environments, or other IRI-managed interactive workloads.

## 14. Required Specification and Registry Changes

### 14.1. OpenAPI Schema

The IRI v2 OpenAPI specification MUST add:

- Path items for the five endpoints defined in Section 4.
- Schema definitions for `ServerList`, `Server`, `ClusterList`, `Cluster`, `ProjectList`, `Project`, `NamespaceCreateRequest`, `Namespace`, and `KubeconfigRequest`.
- `x-iri.maturity: planned` tags on all persistent service operations.

### 14.2. URN Registry

The following Resource Type URNs are registered in the [DOE-IRI URN Registry](../registry/urns/resource-types.md) in `provisional` status while this RFC is under review:

- `urn:doe-iri:resource:persistent-service` (parent category)
- `urn:doe-iri:resource:persistent-service:kubernetes-server`
- `urn:doe-iri:resource:persistent-service:kubernetes-cluster`
- `urn:doe-iri:resource:persistent-service:project`

Approval of this RFC moves them to `active` status. The registry remains the assignment authority.

These URNs are **not** required for the initial API implementation. They support future Resource model integration and HAL link definitions.

### 14.3. Relation Registry

If HAL links are added in future work, the following relations may be required:

- `iri:persistent-service-servers` — Navigate to available Kubernetes servers from the API root or account context.
- `iri:persistent-service-clusters` — Navigate from a server to its clusters.
- `iri:persistent-service-projects` — Navigate from a cluster to accessible projects.
- `iri:persistent-service-kubeconfig` — Generate kubeconfig for a server or cluster.

These are **not** required for the initial implementation described in this RFC.

## 15. References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubeconfig File Specification](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
- [Kubernetes Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119)
- [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174)
- [IRI URN Structure and Registry](./rfc-iri-urn-structure-and-registry.md)
- [DOE-IRI URN Registry](../registry/urns/README.md)
- [DOE-IRI Resource Type URNs](../registry/urns/resource-types.md)
- [HAL `_links` for the IRI Facility API](./rfc-hal-links.md)

## Appendix A. Examples

### A.1. Server Discovery

**Request:**
```http
GET /api/v2/persistent_service/servers HTTP/1.1
Host: api.facility.example.org
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "servers": [
    {
      "server_id": "k8s-prod-01",
      "name": "Production Kubernetes",
      "description": "Primary production cluster for persistent services"
    },
    {
      "server_id": "k8s-dev-01",
      "name": "Development Kubernetes",
      "description": "Development and testing cluster"
    }
  ]
}
```

### A.2. Cluster Discovery

**Request:**
```http
GET /api/v2/persistent_service/servers/k8s-prod-01/clusters HTTP/1.1
Host: api.facility.example.org
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "clusters": [
    {
      "cluster_id": "prod-us-east",
      "name": "Production US East",
      "description": "East coast production cluster",
      "endpoint": "https://k8s-prod-east.facility.example.org:6443"
    },
    {
      "cluster_id": "prod-us-west",
      "name": "Production US West",
      "description": "West coast production cluster",
      "endpoint": "https://k8s-prod-west.facility.example.org:6443"
    }
  ]
}
```

### A.3. Project Discovery

**Request:**
```http
GET /api/v2/persistent_service/servers/k8s-prod-01/clusters/prod-us-east/projects HTTP/1.1
Host: api.facility.example.org
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "projects": [
    {
      "project_id": "proj-12345",
      "name": "research-team-alpha",
      "description": "Research team Alpha multi-tenancy project"
    },
    {
      "project_id": "proj-67890",
      "name": "shared-analysis",
      "description": "Shared analysis multi-tenancy project"
    }
  ]
}
```

### A.4. Namespace Creation

**Request:**
```http
POST /api/v2/persistent_service/servers/k8s-prod-01/clusters/prod-us-east/namespaces HTTP/1.1
Host: api.facility.example.org
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "project_id": "proj-12345",
  "name": "my-experiment-ns",
  "description": "Namespace for experiment workflow services"
}
```

**Response:**
```json
{
  "namespace_id": "ns-abc123",
  "name": "my-experiment-ns",
  "cluster_id": "prod-us-east",
  "status": "active",
  "created_at": "2026-11-10T15:30:00Z"
}
```

### A.5. Kubeconfig Generation

**Request:**
```http
POST /api/v2/persistent_service/servers/k8s-prod-01/kubeconfig HTTP/1.1
Host: api.facility.example.org
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "clusters": ["prod-us-east"],
  "validity": 3600
}
```

**Response:**
```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t...
    server: https://k8s-prod-east.facility.example.org:6443
  name: prod-us-east
contexts:
- context:
    cluster: prod-us-east
    user: user-jdoe
    namespace: my-experiment-ns
  name: prod-us-east-context
current-context: prod-us-east-context
users:
- name: user-jdoe
  user:
    token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### A.6. Error Response Example

**Request:**
```http
POST /api/v2/persistent_service/servers/k8s-prod-01/clusters/prod-us-east/namespaces HTTP/1.1
Host: api.facility.example.org
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "project_id": "proj-12345",
  "name": "my-experiment-ns"
}
```

**Response (namespace already exists):**
```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "type": "https://iri.science/problems/conflict",
  "title": "Namespace Already Exists",
  "status": 409,
  "detail": "Namespace 'my-experiment-ns' already exists in cluster 'prod-us-east'",
  "instance": "/api/v2/persistent_service/servers/k8s-prod-01/clusters/prod-us-east/namespaces"
}
```
