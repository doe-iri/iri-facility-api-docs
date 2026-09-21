# DOE-IRI Controlled Attribute URNs

This is the authoritative registry and index of controlled DOE-IRI attribute
URNs used by Resource Definition profiles. It records controlled values only;
ordinary JSON attributes remain defined by the applicable profile. Every value
listed here has status `provisional`.

## Compute

| Vocabulary (semantic purpose) | Registered values | Used by |
|---|---|---|
| `system-capability` (stable system capabilities) | `batch-scheduling`, `interactive-access`, `container-execution`, `accelerator-support` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `node-role` (node's intended function) | `compute`, `login`, `service` | [Compute Node](../profiles/resource-definition/compute/node.md) |
| `cpu-architecture` (processor ISA family) | `x86-64`, `arm64`, `ppc64le`, `riscv64` | [CPU](../profiles/resource-definition/compute/cpu.md), [Compute System](../profiles/resource-definition/compute/system.md) |
| `gpu-programming-interface` (facility-supported GPU programming interface) | `cuda`, `hip`, `opencl`, `sycl` | [GPU](../profiles/resource-definition/compute/gpu.md), [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-runtime` (container engine that executes workloads) | `apptainer`, `singularity`, `podman`, `podman-hpc`, `shifter`, `docker` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-image-format` (accepted container image input representation) | `oci-image`, `docker-v2-image`, `oci-image-layout`, `oci-archive`, `docker-archive`, `sif`, `apptainer-sandbox` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-execution-format` (facility-native representation used to execute) | `sif`, `runtime-managed-image`, `oci-runtime-bundle`, `rootfs-directory` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-acquisition` (how a registry image becomes runnable) | `direct`, `pre-stage-required`, `not-supported` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-registry-auth` (private-registry authentication method) | `none`, `anonymous`, `user-login`, `facility-managed`, `pull-secret` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-uid-mode` (in-container execution identity model) | `host-user`, `userns`, `fakeroot`, `setuid-helper` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-gpu-injection` (how GPU and host libraries are exposed in the container) | `automatic`, `module`, `runtime-hook`, `host-library-bind` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-build` (where a user may build or convert images on facility compute) | `none`, `login-node`, `compute-node`, `batch`, `ci-service` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-mpi-model` (how a containerized MPI app obtains a working MPI) | `bind`, `hybrid`, `container-native`, `none` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-mpi-host-transfer` (how the host MPI stack reaches the container) | `bind-mount`, `library-injection`, `library-swap`, `launcher-only`, `none` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-mpi-abi` (ABI family the in-container MPI must match) | `mpich`, `open-mpi` | [Compute System](../profiles/resource-definition/compute/system.md) |
| `container-mpi-activation` (how the user enables host-MPI integration) | `automatic`, `flag`, `module`, `env`, `none` | [Compute System](../profiles/resource-definition/compute/system.md) |

Each row is a compact canonical-URN enumeration: concatenate its vocabulary and
each listed value as `urn:doe-iri:compute:<vocabulary>:<value>`. For example,
the CPU-architecture row registers
`urn:doe-iri:compute:cpu-architecture:x86-64`,
`urn:doe-iri:compute:cpu-architecture:arm64`,
`urn:doe-iri:compute:cpu-architecture:ppc64le`, and
`urn:doe-iri:compute:cpu-architecture:riscv64`.

## Storage

| Vocabulary (semantic purpose) | Registered values | Used by |
|---|---|---|
| `system-technology` | `lustre`, `spectrum-scale`, `ceph`, `beegfs`, `weka`, `vast`, `aws-efs`, `aws-fsx-openzfs`, `azure-files`, `gcp-filestore` | [Storage System](../profiles/resource-definition/storage/system.md) |
| `system-architecture` | `distributed`, `clustered` | [Storage System](../profiles/resource-definition/storage/system.md) |
| `system-capability` | `replication`, `erasure-coding`, `encryption-at-rest`, `snapshot`, `data-tiering` | [Storage System](../profiles/resource-definition/storage/system.md) |
| `filesystem-scope` | `local`, `network` | [Filesystem](../profiles/resource-definition/storage/filesystem.md) |
| `filesystem-architecture` | `distributed`, `clustered` | [Filesystem](../profiles/resource-definition/storage/filesystem.md) |
| `filesystem-capability` | `parallel-io`, `direct-io`, `asynchronous-io`, `data-striping`, `shared-namespace` | [Filesystem](../profiles/resource-definition/storage/filesystem.md) |
| `filesystem-technology` | `lustre`, `spectrum-scale`, `cephfs`, `beegfs` | [Filesystem](../profiles/resource-definition/storage/filesystem.md) |
| `filesystem-protocol` | `nfs`, `smb`, `webdav` | [Filesystem](../profiles/resource-definition/storage/filesystem.md), [Filesystem Mount](../profiles/resource-definition/storage/mount.md) |
| `mount-access-mode` | `read-only`, `read-write` | [Filesystem Mount](../profiles/resource-definition/storage/mount.md) |
| `block-scope` | `local`, `network` | [Block Storage](../profiles/resource-definition/storage/block.md) |
| `block-protocol` | `iscsi`, `fibre-channel`, `nvme-o-f` | [Block Storage](../profiles/resource-definition/storage/block.md) |
| `block-access-mode` | `exclusive`, `shared` | [Block Storage](../profiles/resource-definition/storage/block.md) |
| `block-provisioning` | `thin`, `thick` | [Block Storage](../profiles/resource-definition/storage/block.md) |
| `block-capability` | `snapshot`, `clone`, `multipath` | [Block Storage](../profiles/resource-definition/storage/block.md) |
| `object-api` | `s3`, `swift` | [Object Storage](../profiles/resource-definition/storage/object.md) |
| `object-technology` | `ceph-rgw`, `openstack-swift`, `amazon-s3` | [Object Storage](../profiles/resource-definition/storage/object.md) |
| `object-consistency` | `strong-read-after-write`, `eventual` | [Object Storage](../profiles/resource-definition/storage/object.md) |
| `object-capability` | `multipart-upload`, `versioning`, `object-lock` | [Object Storage](../profiles/resource-definition/storage/object.md) |
| `tier` (storage lifecycle/usage tier) | `home`, `project`, `scratch`, `campaign`, `archive` | [Filesystem](../profiles/resource-definition/storage/filesystem.md), [Block Storage](../profiles/resource-definition/storage/block.md), [Object Storage](../profiles/resource-definition/storage/object.md) |
| `media-type` | `magnetic-disk`, `solid-state`, `tape`, `optical` | [Storage System](../profiles/resource-definition/storage/system.md), [Filesystem](../profiles/resource-definition/storage/filesystem.md), [Block Storage](../profiles/resource-definition/storage/block.md), [Object Storage](../profiles/resource-definition/storage/object.md) |

Each row is a compact canonical-URN enumeration: concatenate its vocabulary and
each listed value as `urn:doe-iri:storage:<vocabulary>:<value>`. This is an
enumeration, not a template permitting unlisted values.

## Service

| Vocabulary (semantic purpose) | Registered values | Used by |
|---|---|---|
| `dtn-technology` (DTN implementation) | `globus`, `xrootd` | [DTN Service](../profiles/resource-definition/service/dtn.md) |
| `transfer-protocol` (DTN transfer interface) | `https`, `gridftp`, `xrootd`, `sftp` | [DTN Service](../profiles/resource-definition/service/dtn.md) |
| `inference-api` (inference invocation interface) | `openai`, `kserve-v2` | [Inference Service](../profiles/resource-definition/service/inference.md) |
| `inference-technology` (inference implementation) | `vllm`, `hugging-face-tgi`, `nvidia-triton`, `kserve` | [Inference Service](../profiles/resource-definition/service/inference.md) |

Each row is a compact canonical-URN enumeration: concatenate its vocabulary and
each listed value as `urn:doe-iri:service:<vocabulary>:<value>`. This is an
enumeration, not a template permitting unlisted values.

*DOE Integrated Research Infrastructure — URN Registry*
