# RFC: Container Execution Capability Discovery for IRI Compute Systems

## Abstract

The DOE Integrated Research Infrastructure (IRI) Facility API describes a containerized workload with a single `image` string on the compute `Container` schema. That string does not tell a client which container runtimes a system accepts, which image formats it can execute, whether an image can be pulled directly from a registry or must be pre-staged and converted first, which registries are permitted, how private-registry authentication works, how GPU and host-library integration is wired, whether rootless or unprivileged execution is required, whether a build environment is available, or which CPU architectures are supported.

This RFC defines a read-only, structured **capability-discovery** contract for that information. It adds a `container_runtimes` attribute to the IRI Compute System Resource Definition Profile. Each entry describes one facility container execution option: runtime, accepted image formats, native execution format, registry-pull support, registry policy, private-registry authentication model, execution identity and privilege policy, GPU integration, MPI integration, build availability, and architecture.

This RFC is deliberately limited to a description of capabilities. It defines no new endpoint, no image-acquisition operation, and no change to the `Container` job schema. It reuses three existing IRI mechanisms without modifying them: the type-specific `attributes` property and Resource Definition Profile model ([RFC: Type-Specific Attributes](./rfc-type-specific-attributes.md)), the DOE-IRI URN namespace and registry ([RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md)), and HAL `_links` ([RFC: HAL `_links` for the IRI Facility API](./rfc-hal-links.md)).

A normalized image runtime and reuse (facility pre-stage, immutable facility-scoped references, and a normalized job schema) is explicitly out of scope and is left to a future RFC. See Section 15.

## Status of This Memo

This document is a proposed IRI Facility API extension intended for adoption within specification version 2.0 and its reference implementations.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

| Revision | Author | Date | Notes |
|---|---|---|---|
| 0.1 | Justas Balcas/Claude (Sonnet 5) | Aug 26, 2026 | Initial capability-discovery draft, scoped to metadata only, split out of the combined container acquisition draft. Based on the [doe-iri/iri-facility-api-docs#21](https://github.com/doe-iri/iri-facility-api-docs/issues/21) facility survey. |
| 0.2 | Justas Balcas | Aug 28, 2026 | Full review and sections rewrite. |
| 0.3 | Justas Balcas | Aug 28, 2026 | Dropped the Compute System profile `1.1.0` version bump; `container_runtimes` is added as an OPTIONAL attribute on the in-progress `1.0.0` profile. |
| 0.4 | Justas Balcas | Aug 28, 2026 | Added `ContainerMpiSupport` (`mpi` on `ContainerRuntimeProfile`) and the `container-mpi-*` vocabularies, from a survey of NERSC (Podman-HPC, Shifter), OLCF (Apptainer), and ALCF (Polaris, Aurora) container MPI documentation. |

## Table of Contents

1. Introduction
2. Scope
3. Terminology
4. Relationship to Existing IRI Mechanisms
5. Compute System Profile Extension
6. Controlled URN Registrations
7. HAL Links
8. OpenAPI Requirements
9. Validation
10. Backward Compatibility and Rollout
11. Producer Requirements
12. Consumer Requirements
13. Security Considerations
14. Conformance and Verification
15. Future Work
16. IANA Considerations
17. References
- Appendix A. End-to-End Examples
- Appendix B. Facility Survey Summary

# 1. Introduction

The current IRI v2 `Container` schema contains one `image` parameter and an optional list of volume mounts. A facility information about container capabilities is available on each labs websites. From that, a portable workflow cannot determine easily:

```text
Which runtime or runtimes will execute the workload?
Which image formats does the system support?
Is the accepted input executed directly, or converted first?
Can the workflow reference a registry image at submission time, or must the image be pulled and converted?
Which registries are permitted, and how is a private repository authenticated?
How are GPUs and host libraries exposed inside the container?
How does MPI work inside the container: does it need an ABI-compatible MPICH, and is the host MPI bind-mounted or swapped in?
Is rootless or unprivileged execution the only supported method?
Is there a way to build or convert an image using facility compute, login nodes?
Which CPU architectures are supported?
```

Facility responses on [doe-iri/iri-facility-api-docs#21](https://github.com/doe-iri/iri-facility-api-docs/issues/21) establish that these answers differ by facility and often by system:

- **NERSC** uses Podman-HPC and Shifter on Perlmutter; both consume OCI images but flatten or migrate them into a facility-managed representation, and an image is normally pulled to a login node before a job runs. NERSC operates a Harbor instance. There is currently no programmatic API to discover this.
- **OLCF** uses Apptainer across production systems. The native artifact is SIF; Docker/OCI images are usable as a source but must be converted to SIF before a job runs. Users can perform that conversion themselves.
- **ALCF** support varies by system. Apptainer is the primary supported engine, with rootless Podman available on some systems via modules. OCI images are accepted but Apptainer still requires conversion to SIF. ALCF operates its own container registries.

All three facilities confirmed that this information is already public and that exposing it through IRI so users can discover requirements before submission is reasonable. ALCF additionally noted that placing it behind the authenticated API is useful so a user sees the information relevant to the systems they can run on.

The portable near-term need is therefore a normalized way to *describe* each facility's container capabilities, so a client can choose or prepare a compatible image and know whether pre-staging is required before it submits a job.

# 2. Scope

This RFC:

1. Extends the `urn:doe-iri:resource:compute:system` Resource Definition Profile with a `container_runtimes` attribute.
2. Defines an array of behavior-oriented `ContainerRuntimeProfile` entries rather than treating a runtime product name as a complete description.
3. Registers DOE-IRI URN for runtime, image format, acquisition, registry authentication, execution UID mode, GPU injection mechanism, and build availability, all in `provisional` status.
4. Defines producer and consumer processing requirements, backward-compatibility behavior, security considerations, and a conformance plan.

`container_runtimes` is added to the existing Compute System Attribute Profile as an OPTIONAL attribute. The profile stays at `schema_version` `1.0.0` while it is in draft; this RFC mints no new profile version. A v2 producer that supports this RFC SHOULD publish `container_runtimes` for every `urn:doe-iri:resource:compute:system` resource it exposes. A non-empty `container_runtimes` array means containerized execution is supported and described. An empty array explicitly means containerized execution is not supported. Absence of the attribute means only that structured information has not been published; it is **unknown**, never a negative capability assertion.

This RFC does **not**:

1. Define an image-preparation, pre-stage, conversion, or caching operation.
2. Define facility-scoped image references (`image_ref`) or a normalized `Container` job schema. The existing `Container.image` path is unchanged.
3. Standardize a container build or image-conversion *submission* API.
4. Standardize how a user establishes a private-registry credential with a facility, or define a credential-exchange protocol.
5. Expose native runtime flags, native commands, internal cache paths, CVMFS repository paths, registry mirror internals, or registry credentials.
6. Define detailed CUDA/ROCm/oneAPI, driver, MPI ABI, or host-library version compatibility discovery.
7. Guarantee that an arbitrary OCI/Docker workload behaves identically under different runtime semantics. Entrypoint, MPI ABI, writable-root, networking, and host-library constraints remain facility- and runtime-specific.
8. Define filtering or query semantics over `container_runtimes` members.
9. Define authorization or entitlement decisions from any advertised value.

# 3. Terminology

**Container runtime profile**
: One entry in `container_runtimes` describing a single facility container execution path: its runtime, accepted input formats, native execution format, acquisition behavior, registry policy, execution policy, GPU integration, MPI integration, build availability, and architecture.

**Accepted image format**
: An input representation the execution path can consume, such as an OCI image, a Docker image, an OCI image layout, an OCI or Docker archive, a SIF, or an Apptainer sandbox directory.

**Native execution format**
: The representation actually used to execute the workload, such as SIF, a runtime-managed image store entry, or an OCI runtime.

**Acquisition behavior**
: Whether a registry image can be referenced directly at job submission (`direct`), whether it must be pulled and/or converted before the job (`pre-stage-required`), or whether registry pull is not available at all (`not-supported`).

**Registry policy**
: The declared state of outbound registry access for an execution path: any registry, an explicit allowlist, deny-all, or unknown.

**MPI integration model**
: How an MPI application inside a container obtains a working MPI at run time. In the *bind* model the container carries no MPI and the host MPI is bind-mounted in. In the *hybrid* (host-MPI) model the container carries an ABI-compatible MPI and the host supplies the launcher and, for native performance, its optimized libraries (by bind-mount or by runtime replacement). In the *container-native* model the container's own MPI (for example Open MPI with PMIx) is used with no host MPI. Every non-native model requires ABI compatibility between the in-container MPI and the host MPI, commonly the MPICH ABI. This behaviour differs sharply between facilities and is not implied by the runtime product name.

**Controlled value**
: A registered DOE-IRI URN whose meaning and lifecycle are governed by the DOE-IRI URN Registry, per [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md).

# 4. Relationship to Existing IRI Mechanisms

This RFC introduces no new mechanism. It uses three existing ones.

## 4.1. Type-Specific Attributes and Resource Definition Profiles

Per [RFC: Type-Specific Attributes](./rfc-type-specific-attributes.md), a Resource's `resource_type` selects an applicable Resource Definition Profile, and type-specific data is carried in the Resource's optional, nullable, open `attributes` object. `urn:doe-iri:resource:compute:system` is already associated with the [IRI Compute System Resource Definition Profile](../registry/profiles/resource-definition/compute/system.md).

This RFC adds the `container_runtimes` attribute to that profile. It does not add a `ResourceAttributes` component, a Resource Definition API object, or a Resource State API object. The wire-level structural contract for `attributes` is unchanged and remains authoritative in the IRI v2 OpenAPI `Resource` schema.

`container_runtimes` describes relatively stable configuration and capability of the compute system. Consistent with the base profile, dynamic operational information (current queue container policy exceptions, per-job overrides, live registry reachability) is out of scope and belongs to resource-state mechanisms.

## 4.2. DOE-IRI URN Namespace and Registry

Per [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md), controlled vocabulary values are registered DOE-IRI URNs in the `compute` semantic category, and facilities MAY define local values through the delegated `ext` mechanism. This RFC registers new `compute`-category vocabularies (Section 6) and reuses two existing ones unchanged: `urn:doe-iri:compute:cpu-architecture:*` and `urn:doe-iri:compute:gpu-programming-interface:*` (see [Controlled Attribute URNs](../registry/urns/attributes.md)).

Consumers MUST treat these URNs as data and MUST NOT reject a Resource solely because a syntactically valid URN value is unfamiliar. Hierarchy-aware fallback to the nearest recognized parent, or opaque handling, is the required behavior.

## 4.3. HAL `_links`

Per [RFC: HAL `_links` for the IRI Facility API](./rfc-hal-links.md), a compute system Resource MAY already advertise `iri:submit-job`, `self`, `help`, and `service-desc`. This RFC does not register a new link relation. Facility-specific human documentation pointers are carried as optional `*_docs_uri` string attributes inside `container_runtimes` entries (Section 5) rather than as link relations; a future revision MAY promote a documentation pointer to a registered `iri:*` relation once its cardinality and visibility rules are settled.

# 5. Compute System Profile Extension

## 5.1. Attribute Placement and Presence

`container_runtimes` is added to the Compute System Attribute Profile as an OPTIONAL attribute. The profile's `schema_version` is unchanged (`1.0.0` while the profile is in draft); this RFC does not mint a new profile version and introduces no version-discriminated schema. All existing Compute System attributes (`system_capabilities`, `configured_node_count`, `configured_cpu_core_count`, `configured_gpu_count`, `configured_memory_gib`, `vendor`, `product`, `version`) are unchanged.

Presence semantics:

- `container_runtimes` absent: the facility has not published structured container information; container capability is **unknown**.
- `container_runtimes` present and empty (`[]`): containerized execution is explicitly not supported, and `urn:doe-iri:compute:system-capability:container-execution` MUST NOT appear in `system_capabilities`.
- `container_runtimes` present and non-empty: containerized execution is supported and described, and `urn:doe-iri:compute:system-capability:container-execution` MUST appear in `system_capabilities`.

## 5.2. `container_runtimes`

`container_runtimes` is an array of `ContainerRuntimeProfile` objects. Each object describes one execution path. Order MUST NOT be significant. When the array is non-empty, exactly one entry MUST have `default: true`.

Two entries MUST NOT have the same `runtime` value unless their `applies_to_queues` sets are disjoint. A profile that violates this MUST NOT be advertised.

### 5.3. `ContainerRuntimeProfile`

| Property | Type | Required | Description |
|---|---|---|---|
| `runtime` | ContainerRuntimeUrn | Yes | The container runtime/engine for this path, e.g. `urn:doe-iri:compute:container-runtime:apptainer`. |
| `runtime_version` | string | No | Deployed or default runtime version. Informational only. |
| `default` | boolean | Yes | Whether this is the default path among otherwise matching entries. Exactly one `true` per non-empty array. |
| `applies_to_queues` | array of string | No | Exact, resource-local queue names this entry applies to, corresponding to `JobAttributes.queue_name`. Absent means all queues represented by the resource. Non-empty and unique when present. |
| `accepted_image_formats` | array of ContainerImageFormatUrn | Yes, ≥ 1 | Input representations this path can consume. Unique. |
| `native_execution_format` | ContainerImageFormatUrn or ContainerExecutionFormatUrn | No | Representation actually executed. When it differs from an accepted input format, conversion occurs in this path. |
| `registry_pull` | ContainerAcquisitionUrn | Yes | `direct`, `pre-stage-required`, or `not-supported`. |
| `pull_actor` | string enum | No | `user`, `facility`, or `runtime`. Which actor performs the pull and any conversion. Informational. |
| `registry_policy_mode` | string enum | Conditional | `any`, `allowlist`, `deny-all`, or `unknown`. REQUIRED when `registry_pull` is not `not-supported`. |
| `allowed_registries` | array of string | Conditional | Exact HTTPS origins (scheme + authority only). REQUIRED and non-empty when `registry_policy_mode` is `allowlist`; MUST be absent otherwise. |
| `private_registry_auth` | array of ContainerRegistryAuthUrn | No | Authentication methods available for private repositories on this path. Unique. |
| `auth_docs_uri` | string (URI) | No | Human documentation for establishing private-registry access. |
| `rootless_required` | boolean | No | Whether containers must run rootless. |
| `privileged_allowed` | boolean | No | Whether `--privileged`-equivalent execution is permitted. |
| `uid_mode` | ContainerUidModeUrn | No | Execution identity model, e.g. `host-user`, `userns`, `fakeroot`, `setuid-helper`. |
| `gpu_integration` | GpuIntegration | No | GPU and host-library integration for this path. |
| `mpi` | ContainerMpiSupport | No | How MPI works inside containers on this path (Section 5.4). |
| `cpu_architectures` | array of CpuArchitectureUrn | No | Supported CPU architectures for container execution on this path. Reuses the existing CPU-architecture vocabulary. Unique. |
| `build_support` | ContainerBuildUrn | No | Where a user may build or convert an image using facility compute, e.g. `none`, `login-node`, `compute-node`, `batch`, `ci-service`. |
| `build_docs_uri` | string (URI) | No | Human documentation for the build/convert workflow. |
| `image_scanning` | string enum | No | `required`, `optional`, `not-supported`, or `unknown`. |
| `signature_verification` | string enum | No | `required`, `optional`, `not-supported`, or `unknown`. |
| `network_modes` | array of string enum | No | Non-empty unique subset of `host`, `none`, `isolated`. |
| `default_network_mode` | string enum | Conditional | One member of `network_modes`. REQUIRED when `network_modes` is present. |
| `max_image_bytes` | integer | No | Maximum accepted source/compressed image size when the facility enforces one. Greater than zero. |
| `notes` | string | No | Human-readable clarification. Not machine-interpreted. |

Runtime identity is informational. It MUST NOT be used to infer accepted formats, native execution format, acquisition behavior, registry policy, architecture, or execution policy; those are stated explicitly by the entry.

`native_execution_format` is descriptive. This RFC does not require the facility to perform conversion through any IRI operation; it only tells the client that the accepted input is not what ultimately executes. How conversion happens (user `apptainer pull`, facility import, runtime auto-pull) is indicated coarsely by `pull_actor` and, where relevant, `build_support`.

`allowed_registries`, when present, is an informational discovery aid. It is not an authorization statement and MUST NOT be treated as one (Section 13).

### 5.4. `ContainerMpiSupport`

MPI behaviour inside a container is the sharpest difference between facilities and is not implied by `runtime`. Across DOE facilities the common pattern is that a containerized MPI application carries an ABI-compatible MPICH and the facility supplies its optimized host MPI (HPE Cray MPICH, Aurora MPICH) at run time — bind-mounted into the container at OLCF and ALCF, or swapped/injected over the container's own MPICH by a runtime option at NERSC (`podman-hpc --mpi`, Shifter `--module=mpich`). A container-native Open MPI built with PMIx is the portable but non-optimized alternative. `ContainerMpiSupport` states this explicitly.

| Property | Type | Required | Description |
|---|---|---|---|
| `models` | array of ContainerMpiModelUrn | Yes, ≥ 1 | Supported MPI integration models: `bind`, `hybrid`, `container-native`, or `none`. Unique. |
| `default_model` | ContainerMpiModelUrn | Conditional | Model the facility recommends. REQUIRED and a member of `models` when `models` has more than one entry and does not consist solely of `none`. |
| `host_transfer` | ContainerMpiHostTransferUrn | No | How the host MPI stack reaches the container for a non-native model: `bind-mount`, `library-injection`, `library-swap`, `launcher-only`, or `none`. |
| `host_mpi` | string | No | Host MPI stack the container integrates with, e.g. `"HPE Cray MPICH 8"` or `"Aurora MPICH"`. Informational. |
| `abi` | ContainerMpiAbiUrn | No | ABI family the in-container MPI must conform to for a non-native model: `mpich` or `open-mpi`. |
| `required_container_mpi` | string | No | The in-container MPI the facility requires for ABI-compatible operation, e.g. `"MPICH 3.4.2 or 3.4.3"` or `"MPICH ABI, shared libraries, built from source"`. |
| `gpu_aware` | string enum | No | `supported`, `not-supported`, or `unknown`. Whether GPU-aware (CUDA / ROCm / Level Zero) MPI is available from within the container. |
| `process_managers` | array of string enum | No | Process-manager interfaces the host launcher offers the container: `pmi1`, `pmi2`, `pmix`. Non-empty unique when present. |
| `activation` | ContainerMpiActivationUrn | No | How the user enables host-MPI integration: `automatic`, `flag`, `module`, `env`, or `none`. |
| `mpi_docs_uri` | string (URI) | No | Human documentation for running MPI in containers on this path. |
| `notes` | string | No | Human clarification, e.g. exact bind paths, module names, or environment variables. Not machine-interpreted. |

`models`, `host_transfer`, `abi`, and `required_container_mpi` are descriptive. This RFC defines no MPI-setup operation and does not guarantee that a given image will achieve native MPI performance; it only tells the client what the facility expects a containerized MPI build to look like.

# 6. Controlled URN Registrations

This RFC proposes the following controlled URNs under the `compute` semantic category. All values begin in `provisional` status. Each row is a compact canonical-URN enumeration: concatenate the vocabulary and each value as `urn:doe-iri:compute:<vocabulary>:<value>`.

| Vocabulary | Registered values |
|---|---|
| `container-runtime` | `apptainer`, `singularity`, `podman`, `podman-hpc`, `shifter`, `docker` |
| `container-image-format` | `oci-image`, `docker-v2-image`, `oci-image-layout`, `oci-archive`, `docker-archive`, `sif`, `apptainer-sandbox` |
| `container-execution-format` | `sif`, `runtime-managed-image`, `oci-runtime-bundle`, `rootfs-directory` |
| `container-acquisition` | `direct`, `pre-stage-required`, `not-supported` |
| `container-registry-auth` | `none`, `anonymous`, `user-login`, `facility-managed`, `pull-secret` |
| `container-uid-mode` | `host-user`, `userns`, `fakeroot`, `setuid-helper` |
| `container-gpu-injection` | `automatic`, `module`, `runtime-hook`, `host-library-bind` |
| `container-build` | `none`, `login-node`, `compute-node`, `batch`, `ci-service` |
| `container-mpi-model` | `bind`, `hybrid`, `container-native`, `none` |
| `container-mpi-host-transfer` | `bind-mount`, `library-injection`, `library-swap`, `launcher-only`, `none` |
| `container-mpi-abi` | `mpich`, `open-mpi` |
| `container-mpi-activation` | `automatic`, `flag`, `module`, `env`, `none` |

For example:

```text
urn:doe-iri:compute:container-runtime:apptainer
urn:doe-iri:compute:container-image-format:sif
urn:doe-iri:compute:container-acquisition:pre-stage-required
urn:doe-iri:compute:container-gpu-injection:host-library-bind
```

This RFC reuses, without change:

- `urn:doe-iri:compute:cpu-architecture:{x86-64,arm64,ppc64le,riscv64}` for `cpu_architectures`;
- `urn:doe-iri:compute:gpu-programming-interface:{cuda,hip,opencl,sycl}` for `gpu_integration.programming_interfaces`;
- `urn:doe-iri:compute:system-capability:container-execution` as the pairing system capability.

Notes on modeling choices:

- `docker://` and `oras://` are transport schemes, not formats, and are not registered here.
- `singularity` is registered alongside `apptainer` only to describe deployments that still present the SingularityCE command; a facility SHOULD advertise the runtime its users actually invoke.
- `container-execution-format` overlaps `container-image-format` on `sif` intentionally: a path whose accepted input and native execution are both SIF advertises `sif` in both places, signalling that no conversion occurs.

Facility-local values MUST use the delegated-extension process in [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md), including an authority-code reservation, an active scope delegation under the exact shared parent, and a documented local definition. A syntactically valid but unregistered value is not an assigned DOE-IRI value; a general-purpose consumer still MUST NOT reject it and SHOULD fall back to the nearest recognized parent.

# 7. HAL Links

No new link relation is registered by this RFC.

A `urn:doe-iri:resource:compute:system` Resource MAY carry the standard `help` relation for facility support documentation and `service-desc` for the machine-readable API description, as already permitted by [RFC: HAL `_links` for the IRI Facility API](./rfc-hal-links.md). Those links do not grant authorization and do not describe container capability.

Container-specific human documentation is advertised through the optional `auth_docs_uri` and `build_docs_uri` string attributes on a `ContainerRuntimeProfile`. These are plain URIs for human/agent consumption. A client MUST NOT dereference them automatically as part of processing the Resource representation and MUST treat their targets as untrusted.

# 8. OpenAPI Requirements

Implementations of this RFC MUST update the v2 component and status OpenAPI sources and regenerate the published specification.

## 8.1. Attribute Addition

`ComputeSystemAttributes` gains one OPTIONAL property, `container_runtimes`: an array (`minItems: 0`) of `ContainerRuntimeProfile`. `schema_version` is unchanged and no `oneOf`/version-discriminated split is introduced. A representation MAY omit the property entirely.

## 8.2. New Components

The OpenAPI changes MUST define:

- `ContainerRuntimeProfile` and its nested `GpuIntegration` and `ContainerMpiSupport` objects, all with `additionalProperties: false`;
- vocabulary-constrained URN string schemas that accept the registered canonical values and syntactically valid authorized extension values under the exact shared parent: `ContainerRuntimeUrn`, `ContainerImageFormatUrn`, `ContainerExecutionFormatUrn`, `ContainerAcquisitionUrn`, `ContainerRegistryAuthUrn`, `ContainerUidModeUrn`, `ContainerGpuInjectionUrn`, `ContainerBuildUrn`, `ContainerMpiModelUrn`, `ContainerMpiHostTransferUrn`, `ContainerMpiAbiUrn`, `ContainerMpiActivationUrn`, plus reuse of the existing `CpuArchitectureUrn` and GPU programming-interface URN schema (introducing a shared `DoeIriUrn` base component if one does not yet exist);
- string enums for `pull_actor`, `registry_policy_mode`, `image_scanning`, `signature_verification`, `mpi.gpu_aware`, `mpi.process_managers`, and the network mode values.

Set-like arrays (`accepted_image_formats`, `cpu_architectures`, `private_registry_auth`, `network_modes`, `applies_to_queues`, `gpu_integration.programming_interfaces`, `mpi.models`, `mpi.process_managers`) MUST carry `uniqueItems: true`, and the required ones MUST carry `minItems: 1`.

`GpuIntegration` contains:

- `programming_interfaces`: unique array of GPU programming-interface URNs;
- `injection_mechanism`: `ContainerGpuInjectionUrn`.

It MUST NOT contain native runtime flags.

## 8.3. No New Paths

This RFC adds no path, operation, parameter, or request body. `Container`, `VolumeMount`, and all compute job operations are unchanged.

# 9. Validation

Because this RFC defines no request, there is no new synchronous RFC 9457 error contract. Validation is producer-side, applied before a Resource representation is advertised. A conforming producer MUST enforce:

1. `container_runtimes`, when present, is a JSON array; an empty array is permitted and `schema_version` is unaffected.
2. Exactly one `default: true` entry when `container_runtimes` is non-empty; none when empty.
3. `container-execution` system capability present iff `container_runtimes` is present and non-empty.
4. `runtime` uniqueness across entries, unless `applies_to_queues` sets are disjoint.
5. `accepted_image_formats` non-empty and unique per entry.
6. `registry_policy_mode` present when `registry_pull` is not `not-supported`.
7. `allowed_registries` present and non-empty iff `registry_policy_mode` is `allowlist`; each value an exact HTTPS origin with no userinfo, path, query, or fragment.
8. `default_network_mode` present and a member of `network_modes` whenever `network_modes` is present.
9. `mpi.models`, when `mpi` is present, is non-empty and unique; `mpi.default_model` is present and a member of `mpi.models` whenever `mpi.models` has more than one entry and is not solely `none`.
10. Every controlled value is a registered canonical URN or a scope-authorized, documented `ext` value under the exact shared parent.
11. No credential, token, secret, or private key appears in any attribute value.

A consumer MUST NOT reject a Resource solely because it carries an unfamiliar controlled URN, an unfamiliar `pull_actor`, or an unrecognized enum value it does not need; it SHOULD ignore what it cannot use and process the rest.

# 10. Backward Compatibility and Rollout

This is an additive change.

1. The IRI v2 `Resource.attributes` property is already optional, nullable, and open; no wire-level schema change is required to carry `container_runtimes`.
2. A consumer that does not recognize `container_runtimes` treats it as opaque type-specific data and continues to process the common Resource representation.
3. `Container.image` and all compute job operations are unchanged. A workflow that ignores `container_runtimes` behaves exactly as before.
4. A producer that supports this RFC SHOULD publish `container_runtimes` for every `compute:system` resource, using an empty array where containerized execution is not supported.
5. Removing a previously advertised value, changing the meaning of a field, narrowing an accepted enum, or changing the presence/pairing rules requires a compatibility review and, once the Compute System profile leaves draft, a new profile `schema_version`.
6. Unknown response-side properties and URNs remain forward-compatible.

# 11. Producer Requirements

A conforming producer:

1. MUST conform to the governing IRI v2 OpenAPI `Resource` schema and the base [IRI Status Resource Profile](../registry/profiles/status/resource.md).
2. SHOULD publish `container_runtimes` for every `urn:doe-iri:resource:compute:system` resource it exposes.
3. MUST, when publishing the attribute, emit it as an array, using `[]` to state that containerized execution is unsupported.
4. MUST pair a non-empty `container_runtimes` with the `container-execution` system capability, and MUST NOT declare that capability with an empty array.
5. MUST use registered canonical DOE-IRI URNs, or scope-authorized documented `ext` values, for every controlled property.
6. MUST NOT place credentials, tokens, secrets, private keys, or protected personal information in any attribute.
7. MUST NOT expose native runtime flags, native command lines, internal cache paths, CVMFS repository paths, or registry mirror internals.
8. MUST enforce the Section 9 validation rules before advertising.
9. MUST update `last_modified` when advertised `container_runtimes` content changes materially, consistent with the governing Resource modification semantics.
10. SHOULD advertise the runtime its users actually invoke, and SHOULD keep `notes`, `auth_docs_uri`, and `build_docs_uri` current.

# 12. Consumer Requirements

A conforming consumer:

1. MUST process the common Resource representation independently of whether it understands `container_runtimes`.
2. MUST treat absence of `container_runtimes` as unknown, never as unsupported.
3. MUST treat an empty `container_runtimes` array as an explicit statement that containerized execution is unsupported.
4. MUST tolerate unfamiliar controlled URNs and enum values, falling back to the nearest recognized parent or opaque handling.
5. SHOULD select an image format and acquisition approach only from an advertised `ContainerRuntimeProfile` entry.
6. SHOULD honor `applies_to_queues` when choosing a profile for an intended queue, and SHOULD use the `default: true` entry when no queue is specified.
7. MUST NOT treat `allowed_registries`, capability URNs, or any advertised value as authorization, entitlement, allocation, or a guarantee of current availability.
8. MUST NOT automatically dereference `auth_docs_uri` or `build_docs_uri` as part of processing the Resource, and MUST treat their targets as untrusted.
9. MUST NOT execute or instantiate code based on any advertised value.

# 13. Security Considerations

Advertised container capability data is descriptive. It is not an authorization credential, proof of entitlement, proof of allocation, or proof of current availability.

- `allowed_registries` is a discovery aid only. A facility's actual egress and pull authorization decisions are made server-side and are not derivable from this list. A client MUST NOT infer that any listed origin is reachable for its identity, project, or allocation.
- Controlled URNs, enum values, profile identifiers, and documentation URIs MUST be treated as data, never as executable instructions or as class/path/query selectors without independent validation, consistent with [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md) Section 7 and [RFC: Type-Specific Attributes](./rfc-type-specific-attributes.md) Section 14.
- Producers MUST NOT place credentials, tokens, pull secrets, or private keys in any `container_runtimes` value. `private_registry_auth` names *methods*, not material.
- Producers SHOULD avoid disclosing internal topology or operational detail through `notes` or origin lists when disclosure is not authorized.
- `auth_docs_uri` and `build_docs_uri` targets are untrusted. Consumers, including AI and MCP clients, MUST NOT auto-fetch them or act on their content as instructions.
- Images referenced by a workflow remain untrusted input. This RFC does not change any facility's responsibility for rootless/user mapping, privilege restrictions, mount and network policy, signature verification, scanning, and runtime hardening.

# 14. Conformance and Verification

Acceptance requires:

1. Positive and negative JSON Schema examples for `ContainerRuntimeProfile` and `GpuIntegration`, including each Section 9 rule.
2. An optional-attribute test: representations with `container_runtimes` omitted, with `[]`, and with populated entries all validate, and `schema_version` is unaffected in each case.
3. Pairing tests: non-empty array without the `container-execution` capability is rejected; empty array with the capability is rejected.
4. `default`-cardinality tests: zero or multiple `default: true` entries in a non-empty array are rejected.
5. `runtime` uniqueness and `applies_to_queues` disjointness tests.
6. Registry-policy tests: `allowlist` without `allowed_registries` rejected; `allowed_registries` present for any non-`allowlist` mode rejected; non-origin strings rejected.
7. `default_network_mode` membership test.
8. Unknown-URN tolerance tests on the consumer side, including `ext` values.
9. Reference-implementation model round-trip tests and OpenAPI lint/build/validation.
10. Demo-adapter fixture emitting a non-empty `container_runtimes` array, plus Schemathesis coverage.
11. NERSC (Podman-HPC + Shifter), OLCF (Apptainer/SIF), and ALCF (Apptainer + rootless Podman) fixtures derived from Appendix B, confirmed with each facility before any associated value is promoted from `provisional` to `active`.

The implementation pull request should update at least:

- `registry/profiles/resource-definition/compute/system.md`;
- `registry/urns/attributes.md`;
- the v2 component and status OpenAPI sources and the generated specification;
- the Python reference implementation compute-system attribute models and URN scalars;
- the demo adapter;
- conformance and integration tests.

# 15. Future Work

1. A companion RFC defining normalized image acquisition and reuse: facility pre-stage of an OCI reference, conversion into the facility-native representation, an immutable facility-scoped `image_ref`, and a normalized `Container` job branch that submits the reference instead of re-pulling per job. A combined draft covering this already exists and is retained as the starting point for that work.
2. A container build/convert *submission* contract (interactive, batch, or CI-driven), building on `build_support`.
3. Advertisement detail for CVMFS-backed distribution and registry pull-through mirrors as backends beneath the acquisition contract.
4. Detailed CUDA/ROCm/oneAPI, driver, MPI ABI, and host-library version compatibility discovery.
5. Resumable large-image upload for users who cannot place SIF/archive content through an existing facility transfer mechanism.
6. Promotion of `auth_docs_uri` / `build_docs_uri` to registered `iri:*` link relations once cardinality and visibility rules are settled.

# 16. IANA Considerations

This document requires no IANA action. Section 6 describes DOE-IRI registry actions only.

# 17. References

- RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*.
- RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.
- RFC 8141, *Uniform Resource Names (URNs)*.
- RFC 6906, *The 'profile' Link Relation Type*.
- RFC 8288, *Web Linking*.
- [RFC: Type-Specific Attributes for IRI Resource Objects](./rfc-type-specific-attributes.md).
- [RFC: A URN Namespace for the DoE IRI Project](./rfc-iri-urn-structure-and-registry.md).
- [RFC: HAL `_links` for the IRI Facility API](./rfc-hal-links.md).
- [IRI Compute System Resource Definition Profile](../registry/profiles/resource-definition/compute/system.md).
- [DOE-IRI Controlled Attribute URN Registry](../registry/urns/attributes.md).
- [DOE-IRI Resource Type URNs](../registry/urns/resource-types.md).
- [doe-iri/iri-facility-api-docs#21](https://github.com/doe-iri/iri-facility-api-docs/issues/21).
- [OCI Image Specification](https://github.com/opencontainers/image-spec/blob/main/spec.md).
- [Apptainer Docker/OCI Support](https://apptainer.org/docs/user/latest/docker_and_oci.html).
- [Apptainer and MPI Applications (bind and hybrid models)](https://apptainer.org/docs/user/latest/mpi.html).
- [MPICH ABI Compatibility Initiative](https://www.mpich.org/abi/).
- [NERSC Podman-HPC Documentation](https://docs.nersc.gov/development/containers/podman-hpc/overview/).
- [NERSC Shifter Documentation](https://docs.nersc.gov/development/containers/shifter/).
- [OLCF Containers on Frontier Documentation](https://docs.olcf.ornl.gov/software/containers_on_frontier.html).
- [ALCF Containers on Polaris Documentation](https://docs.alcf.anl.gov/polaris/containers/containers/).
- [ALCF Containers on Aurora Documentation](https://docs.alcf.anl.gov/aurora/containers/containers/).

# Appendix A. End-to-End Examples

The examples are illustrative. The governing OpenAPI specification is authoritative for the complete JSON structure.

## A.1. Apptainer / SIF Compute System

```json
{
  "id": "frontier",
  "name": "Frontier",
  "description": "Facility compute system",
  "last_modified": "2026-08-28T15:00:00Z",
  "current_status": "up",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "self_uri": "https://api.example.org/api/v2/status/resources/frontier",
  "site_uri": "https://api.example.org/api/v2/facility/sites/example-olcf",
  "capability_uris": [],
  "attributes": {
    "schema_version": "1.0.0",
    "system_capabilities": [
      "urn:doe-iri:compute:system-capability:batch-scheduling",
      "urn:doe-iri:compute:system-capability:container-execution",
      "urn:doe-iri:compute:system-capability:accelerator-support"
    ],
    "container_runtimes": [
      {
        "runtime": "urn:doe-iri:compute:container-runtime:apptainer",
        "runtime_version": "1.3.6",
        "default": true,
        "accepted_image_formats": [
          "urn:doe-iri:compute:container-image-format:oci-image",
          "urn:doe-iri:compute:container-image-format:docker-v2-image",
          "urn:doe-iri:compute:container-image-format:sif"
        ],
        "native_execution_format": "urn:doe-iri:compute:container-image-format:sif",
        "registry_pull": "urn:doe-iri:compute:container-acquisition:pre-stage-required",
        "pull_actor": "user",
        "registry_policy_mode": "any",
        "private_registry_auth": [
          "urn:doe-iri:compute:container-registry-auth:anonymous",
          "urn:doe-iri:compute:container-registry-auth:user-login"
        ],
        "rootless_required": true,
        "privileged_allowed": false,
        "uid_mode": "urn:doe-iri:compute:container-uid-mode:fakeroot",
        "gpu_integration": {
          "programming_interfaces": [
            "urn:doe-iri:compute:gpu-programming-interface:hip"
          ],
          "injection_mechanism": "urn:doe-iri:compute:container-gpu-injection:host-library-bind"
        },
        "mpi": {
          "models": [
            "urn:doe-iri:compute:container-mpi-model:hybrid",
            "urn:doe-iri:compute:container-mpi-model:bind",
            "urn:doe-iri:compute:container-mpi-model:container-native"
          ],
          "default_model": "urn:doe-iri:compute:container-mpi-model:hybrid",
          "host_transfer": "urn:doe-iri:compute:container-mpi-host-transfer:bind-mount",
          "host_mpi": "HPE Cray MPICH 8",
          "abi": "urn:doe-iri:compute:container-mpi-abi:mpich",
          "required_container_mpi": "MPICH 3.4.2 or 3.4.3, ABI-compatible with the cray-mpich-abi module",
          "gpu_aware": "supported",
          "process_managers": ["pmi2", "pmix"],
          "activation": "urn:doe-iri:compute:container-mpi-activation:module",
          "mpi_docs_uri": "https://docs.example-olcf.org/containers/apptainer-mpi",
          "notes": "Load olcf-container-tools plus apptainer-enable-mpi and apptainer-enable-gpu at run time to bind the host Cray MPICH and ROCm libraries; do not load them before 'apptainer build'."
        },
        "cpu_architectures": [
          "urn:doe-iri:compute:cpu-architecture:x86-64"
        ],
        "build_support": "urn:doe-iri:compute:container-build:compute-node",
        "build_docs_uri": "https://docs.example-olcf.org/containers/build",
        "image_scanning": "not-supported",
        "signature_verification": "optional",
        "network_modes": ["host", "none"],
        "default_network_mode": "host",
        "notes": "Docker/OCI sources must be converted to SIF with 'apptainer pull' before job submission."
      }
    ]
  }
}
```

## A.2. Podman-HPC + Shifter Compute System

```json
{
  "id": "perlmutter",
  "resource_type": "urn:doe-iri:resource:compute:system",
  "self_uri": "https://api.example.org/api/v2/status/resources/perlmutter",
  "site_uri": "https://api.example.org/api/v2/facility/sites/example-nersc",
  "capability_uris": [],
  "attributes": {
    "schema_version": "1.0.0",
    "system_capabilities": [
      "urn:doe-iri:compute:system-capability:batch-scheduling",
      "urn:doe-iri:compute:system-capability:container-execution",
      "urn:doe-iri:compute:system-capability:accelerator-support"
    ],
    "container_runtimes": [
      {
        "runtime": "urn:doe-iri:compute:container-runtime:podman-hpc",
        "default": true,
        "accepted_image_formats": [
          "urn:doe-iri:compute:container-image-format:oci-image",
          "urn:doe-iri:compute:container-image-format:docker-v2-image"
        ],
        "native_execution_format": "urn:doe-iri:compute:container-execution-format:runtime-managed-image",
        "registry_pull": "urn:doe-iri:compute:container-acquisition:pre-stage-required",
        "pull_actor": "user",
        "registry_policy_mode": "any",
        "private_registry_auth": [
          "urn:doe-iri:compute:container-registry-auth:user-login"
        ],
        "rootless_required": true,
        "privileged_allowed": false,
        "uid_mode": "urn:doe-iri:compute:container-uid-mode:userns",
        "gpu_integration": {
          "programming_interfaces": [
            "urn:doe-iri:compute:gpu-programming-interface:cuda"
          ],
          "injection_mechanism": "urn:doe-iri:compute:container-gpu-injection:module"
        },
        "mpi": {
          "models": [
            "urn:doe-iri:compute:container-mpi-model:hybrid",
            "urn:doe-iri:compute:container-mpi-model:container-native"
          ],
          "default_model": "urn:doe-iri:compute:container-mpi-model:hybrid",
          "host_transfer": "urn:doe-iri:compute:container-mpi-host-transfer:library-injection",
          "host_mpi": "HPE Cray MPICH 8",
          "abi": "urn:doe-iri:compute:container-mpi-abi:mpich",
          "required_container_mpi": "A standard MPICH built from source with shared libraries (not the distro package)",
          "gpu_aware": "supported",
          "process_managers": ["pmi2", "pmix"],
          "activation": "urn:doe-iri:compute:container-mpi-activation:flag",
          "notes": "podman-hpc --mpi inserts the optimized Cray MPICH over the container's MPICH at run time; --cuda-mpi (with --gpu) selects CUDA-aware Cray MPICH. A container-native Open MPI built --with-slurm is also supported via --openmpi-pmi2 / --openmpi-pmix."
        },
        "cpu_architectures": [
          "urn:doe-iri:compute:cpu-architecture:x86-64"
        ],
        "build_support": "urn:doe-iri:compute:container-build:login-node",
        "image_scanning": "unknown",
        "signature_verification": "unknown",
        "notes": "Images are squashed into a single-layer runtime store entry. Manual pre-pull on a login node is recommended."
      },
      {
        "runtime": "urn:doe-iri:compute:container-runtime:shifter",
        "default": false,
        "accepted_image_formats": [
          "urn:doe-iri:compute:container-image-format:oci-image",
          "urn:doe-iri:compute:container-image-format:docker-v2-image"
        ],
        "native_execution_format": "urn:doe-iri:compute:container-execution-format:runtime-managed-image",
        "registry_pull": "urn:doe-iri:compute:container-acquisition:pre-stage-required",
        "pull_actor": "facility",
        "registry_policy_mode": "any",
        "rootless_required": false,
        "privileged_allowed": false,
        "uid_mode": "urn:doe-iri:compute:container-uid-mode:setuid-helper",
        "gpu_integration": {
          "programming_interfaces": [
            "urn:doe-iri:compute:gpu-programming-interface:cuda"
          ],
          "injection_mechanism": "urn:doe-iri:compute:container-gpu-injection:automatic"
        },
        "mpi": {
          "models": [
            "urn:doe-iri:compute:container-mpi-model:hybrid"
          ],
          "host_transfer": "urn:doe-iri:compute:container-mpi-host-transfer:library-swap",
          "host_mpi": "HPE Cray MPICH 8",
          "abi": "urn:doe-iri:compute:container-mpi-abi:mpich",
          "required_container_mpi": "MPICH 3.4.3 built from source with the ch4:ofi device",
          "gpu_aware": "supported",
          "process_managers": ["pmi2"],
          "activation": "urn:doe-iri:compute:container-mpi-activation:module",
          "notes": "--module=mpich (default) swaps the container MPICH for Cray MPICH at run time; --module=cuda-mpich with MPICH_GPU_SUPPORT_ENABLED=1 selects CUDA-aware Cray MPICH. The image glibc must be at least the mpich module's glibc."
        },
        "cpu_architectures": [
          "urn:doe-iri:compute:cpu-architecture:x86-64"
        ],
        "build_support": "urn:doe-iri:compute:container-build:none",
        "notes": "The image manager imports and flattens registry images before jobs reference them. Deprecation expected on the next system generation."
      }
    ]
  }
}
```

## A.3. Compute System Without Container Support

```json
{
  "attributes": {
    "schema_version": "1.0.0",
    "system_capabilities": [
      "urn:doe-iri:compute:system-capability:batch-scheduling"
    ],
    "container_runtimes": []
  }
}
```

# Appendix B. Facility Survey Summary

The table records only what the [issue #21](https://github.com/doe-iri/iri-facility-api-docs/issues/21) responses established. "Unknown" means the response did not establish IRI adapter behavior; it is not a negative capability statement. Facility behavior changes over time; fixtures MUST be confirmed by each facility before any associated value is promoted from `provisional` to `active`.

| Facility / system | Runtime(s) | Accepted source | Native execution format | Registry pull | Execution identity | Build | MPI in containers |
|---|---|---|---|---|---|---|---|
| NERSC Perlmutter / Podman-HPC | Podman-HPC (Podman core) | OCI / Docker registry images | Squashed single-layer runtime-managed store entry | Pre-pull to a login node recommended; `run` auto-pulls | Rootless; Linux user namespaces; 65,535 subuid/subgid per user | Login nodes (non-dedicated), node-local NVMe build cache | Hybrid. Container ships a source-built shared-library MPICH; `--mpi` inserts optimized Cray MPICH at run time, `--cuda-mpi` (with `--gpu`) for CUDA-aware. Container-native Open MPI `--with-slurm` also works (`--openmpi-pmi2` / `--openmpi-pmix`). |
| NERSC Perlmutter / Shifter | Shifter + image manager | OCI / Docker registry images | Flattened runtime-managed image | Facility import/flatten before job use | setuid execution model; primary app runs as host user | None dedicated; deprecation expected for N10 | Hybrid via library swap. Image built against MPICH 3.4.3 (ch4:ofi); `--module=mpich` (default) swaps in Cray MPICH, `--module=cuda-mpich` + `MPICH_GPU_SUPPORT_ENABLED=1` for CUDA-aware. Image glibc ≥ module glibc. |
| OLCF production systems | Apptainer (uniform) | Docker/OCI as base; SIF required for jobs | SIF | User pulls/converts to SIF before submission (`apptainer pull`) | Rootless; `--rocm` / `--nv` for GPUs | Build on any node, interactive or batch; CI restricted to approved UMS projects | Hybrid / bind. Image needs MPICH 3.4.2 or 3.4.3, ABI-compatible with `cray-mpich-abi`; `olcf-container-tools` + `apptainer-enable-mpi` + `apptainer-enable-gpu` bind the host Cray MPICH and ROCm libraries at run time. GPU-aware supported. |
| ALCF Polaris / Apptainer | Apptainer (`--fakeroot`, compute-node only) | OCI / Apptainer formats; DockerHub usable; ALCF GitHub / GitLab-CI registries | SIF | Apptainer can pull directly to the filesystem; conversion still required; large-scale caching is an open problem | Rootless required; `--privileged` disallowed; fakeroot for builds | Apptainer and Podman builds on compute nodes; outbound proxy needed for web fetches | Bind / hybrid. `module load cray-mpich-abi`; bind `-B /opt -B /var/run/palsd/` and set `APPTAINERENV_LD_LIBRARY_PATH` to `$CRAY_LD_LIBRARY_PATH` plus the PALS lib dir; MPICH-4 ABI base image (`libmpi.so.*` must resolve). |
| ALCF Aurora / Apptainer | Apptainer (`--fakeroot`) | OCI / Apptainer formats; Argonne GitHub Container Registry | SIF | Convert Docker/OCI to SIF on a compute node | Rootless; `--fakeroot` | Build on compute nodes; outbound proxy required | Hybrid. Container builds an ABI-compatible MPICH (Aurora MPICH); host oneAPI / Level-Zero and MPI libraries provided at run time. GPU-aware over Intel PVC XPUs. |

NERSC Spin (Kubernetes / native Docker) is excluded from this batch-compute summary. Its registry allow-list statements apply to Spin and MUST NOT be attributed to Perlmutter Podman-HPC without separate confirmation. MPICH ABI compatibility across all rows follows the MPICH ABI Compatibility Initiative.
