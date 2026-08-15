# Service Resource Types Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Register DTN and inference service resource types with complete attributes, controlled vocabularies, relationships, navigation, state guidance, and governing-specification alignment.

**Architecture:** Add a focused Service domain alongside the existing Compute and Storage registries. Resource classification uses `urn:doe-iri:resource:service:*`, controlled characteristics use `urn:doe-iri:service:*`, topology uses `iri:hosted-on` and `iri:accesses-mount`, and live inference model activation stays in a companion state schema rather than the resource definition.

**Tech Stack:** Markdown registry documents, OpenAPI-compatible YAML schema fragments, JSON and HAL examples, shell-based repository checks.

**Spec:** `docs/superpowers/specs/2026-08-13-service-resource-types-design.md`

## Global Constraints

- Treat repository contents as authoritative and preserve the semantic classification, attribute, relationship, and state separation in `AGENTS.md`.
- Keep `urn:doe-iri:resource:service` active; register both refined resource types, all new controlled values, and both new relations as provisional.
- Use `urn:doe-iri:resource:service:*` only for resource types and `urn:doe-iri:service:*` only for service controlled vocabulary values.
- Keep DTN and inference endpoint URLs as structured attributes, not independent resources.
- Keep `served_models` in the inference definition and `active_models` in the companion operational-state schema.
- Do not modify the Facility API OpenAPI as part of this change.
- Preserve existing and user-owned changes; never revert unrelated work.
- Follow the established profile schema conventions: `type: object`, required `schema_version`, version `"1.0.0"`, reusable `IriUrn`, and `uniqueItems: true` for URN and model-ID arrays.
- Use `registry_editor` for Tasks 1-6 and `registry_maintainer` for Task 7, with write-heavy work performed sequentially.

---

### Task 1: Service Domain Registry and Consolidated Taxonomy

**Files:**
- Create: `registry/urn-registry-type-service.md`
- Create: `registry/urn-registry-type-service-taxonomy.md`
- Reference: `registry/urn-registry-type-compute.md`
- Reference: `registry/urn-registry-type-compute-taxonomy.md`
- Reference: `docs/superpowers/specs/2026-08-13-service-resource-types-design.md`

**Interfaces:**
- Consumes: Approved resource types, controlled values, and relations from the design specification.
- Produces: Canonical Service domain entry points and indexes used by profile, link, root-registry, and README tasks.

- [ ] **Step 1: Run the pre-implementation checks**

```bash
test ! -e registry/urn-registry-type-service.md
test ! -e registry/urn-registry-type-service-taxonomy.md
```

Expected: both commands succeed because the new documents do not exist.

- [ ] **Step 2: Create the Service type registry metadata and conceptual model**

Mirror `urn-registry-type-compute.md`, using this exact hierarchy and lifecycle:

```text
urn:doe-iri:resource:service
├── dtn         provisional
└── inference   provisional
```

Document that the active parent represents a generic consumable service resource; a DTN is not its host node; an inference service is not a model, deployment, endpoint, replica, or accelerator; and physical topology is expressed by links.

- [ ] **Step 3: Add resource-type, attribute-profile, vocabulary, and relationship indexes**

The Service type registry must link to both profile documents and enumerate these controlled families:

```text
urn:doe-iri:service:dtn-technology
urn:doe-iri:service:transfer-protocol
urn:doe-iri:service:inference-api
urn:doe-iri:service:inference-technology
```

Index `iri:hosted-on` for both service types and `iri:accesses-mount` for DTN only. State explicitly that endpoints are attributes and that operational state is separate.

- [ ] **Step 4: Create the consolidated taxonomy and exact URN index**

Include the resource tree and all 12 provisional controlled values:

```text
urn:doe-iri:service:dtn-technology:globus
urn:doe-iri:service:dtn-technology:xrootd
urn:doe-iri:service:transfer-protocol:https
urn:doe-iri:service:transfer-protocol:gridftp
urn:doe-iri:service:transfer-protocol:xrootd
urn:doe-iri:service:transfer-protocol:sftp
urn:doe-iri:service:inference-api:openai
urn:doe-iri:service:inference-api:kserve-v2
urn:doe-iri:service:inference-technology:vllm
urn:doe-iri:service:inference-technology:hugging-face-tgi
urn:doe-iri:service:inference-technology:nvidia-triton
urn:doe-iri:service:inference-technology:kserve
```

Add a relationship table whose source, target, cardinality, stability, visibility, and description agree exactly with Task 4.

- [ ] **Step 5: Verify domain-document completeness**

```bash
rg -n 'resource:service:(dtn|inference)|service:(dtn-technology|transfer-protocol|inference-api|inference-technology)|iri:(hostedOn|accessesMount)' registry/urn-registry-type-service.md registry/urn-registry-type-service-taxonomy.md
```

Expected: both resource types, four controlled families, and both relations appear in the appropriate documents.

- [ ] **Step 6: Commit the service domain documents**

```bash
git add registry/urn-registry-type-service.md registry/urn-registry-type-service-taxonomy.md
git commit -m "docs: add service resource type registry"
```

---

### Task 2: DTN Attribute Profile

**Files:**
- Create: `registry/urn-registry-attributes-service-dtn.md`
- Reference: `registry/urn-registry-attributes-storage-object.md`
- Reference: `registry/urn-registry-type-service-taxonomy.md`

**Interfaces:**
- Consumes: The DTN type and controlled values indexed by Task 1.
- Produces: `DtnServiceAttributes` and `TransferEndpoint` schemas, examples, and definitions linked by later navigation tasks.

- [ ] **Step 1: Run the failing profile-content check**

```bash
test -e registry/urn-registry-attributes-service-dtn.md
```

Expected: failure because the DTN profile does not exist.

- [ ] **Step 2: Create metadata, introduction, taxonomy, and attribute table**

Use the title:

```text
# Attribute Profile: `urn:doe-iri:resource:service:dtn`
```

The attribute table must define `schema_version`, `dtn_technology`, `technology_version`, `transfer_protocols`, and `transfer_endpoints`. Only `schema_version` is mandatory. Explain technology-versus-protocol semantics and omission instead of guessing.

- [ ] **Step 3: Define the two controlled vocabularies**

Give concise, implementation-independent definitions for Globus, XRootD technology, HTTPS, GridFTP, XRootD protocol, and SFTP. Explicitly distinguish the XRootD technology from its protocol and explain that a DTN may advertise several protocols regardless of technology.

- [ ] **Step 4: Define `TransferEndpoint` semantics**

Use this interface:

```yaml
TransferEndpoint:
  type: object
  required:
    - url
    - protocol
  properties:
    url:
      type: string
      format: uri
    protocol:
      $ref: '#/components/schemas/IriUrn'
    name:
      type: string
```

State that `protocol` must come from `urn:doe-iri:service:transfer-protocol:*` and that the endpoint is configured access information, not a reachability claim.

- [ ] **Step 5: Add the complete OpenAPI-compatible schema**

Define `IriUrn`, `TransferEndpoint`, and `DtnServiceAttributes`. Require `schema_version: "1.0.0"`; use `uniqueItems: true` for `transfer_protocols`; and reference `TransferEndpoint` from `transfer_endpoints`.

- [ ] **Step 6: Add two consistent JSON examples and state exclusions**

The Globus example must advertise HTTPS and GridFTP. The XRootD example must use XRootD technology and expose XRootD and HTTPS endpoints. Explain that endpoint health, active transfers, queues, throughput, credentials, and current availability are excluded from the stable definition.

- [ ] **Step 7: Verify DTN profile coverage**

```bash
rg -n 'dtn_technology|technology_version|transfer_protocols|transfer_endpoints|dtn-technology:(globus|xrootd)|transfer-protocol:(https|gridftp|xrootd|sftp)|uniqueItems: true|format: uri' registry/urn-registry-attributes-service-dtn.md
```

Expected: all five attributes, all six controlled values, URI validation, and array uniqueness appear.

- [ ] **Step 8: Commit the DTN profile**

```bash
git add registry/urn-registry-attributes-service-dtn.md
git commit -m "docs: define DTN service attributes"
```

---

### Task 3: Inference Attribute and Companion State Profile

**Files:**
- Create: `registry/urn-registry-attributes-service-inference.md`
- Reference: `registry/urn-registry-attributes-storage-object.md`
- Reference: `registry/urn-registry-type-service-taxonomy.md`

**Interfaces:**
- Consumes: The inference type and controlled values indexed by Task 1.
- Produces: `InferenceServiceAttributes`, `InferenceEndpoint`, `ServedModel`, and companion `InferenceServiceState` schemas.

- [ ] **Step 1: Run the failing profile-content check**

```bash
test -e registry/urn-registry-attributes-service-inference.md
```

Expected: failure because the inference profile does not exist.

- [ ] **Step 2: Create metadata, introduction, taxonomy, and definition attribute table**

Use the title:

```text
# Attribute Profile: `urn:doe-iri:resource:service:inference`
```

Define `schema_version`, `inference_technology`, `technology_version`, `inference_apis`, `inference_endpoints`, and `served_models`. Only `schema_version` is mandatory. State that the resource is a consumable invocation service and that models, deployments, endpoints, replicas, hosts, and accelerators are not independent resource types in this profile.

- [ ] **Step 3: Define inference API and technology vocabularies**

Register and describe OpenAI, KServe V2, vLLM, Hugging Face TGI, NVIDIA Triton, and KServe. Keep API and implementation meanings separate, and prohibit inferring APIs or availability solely from technology.

- [ ] **Step 4: Define the structured endpoint and model interfaces**

Use these interfaces:

```yaml
InferenceEndpoint:
  type: object
  required:
    - url
    - api
  properties:
    url:
      type: string
      format: uri
    api:
      $ref: '#/components/schemas/IriUrn'
    name:
      type: string

ServedModel:
  type: object
  required:
    - id
    - name
  properties:
    id:
      type: string
    name:
      type: string
    version:
      type: string
    model_uri:
      type: string
      format: uri
```

Document the semantic uniqueness requirement for `ServedModel.id` and the exact `inference-api` family required by endpoint `api`.

- [ ] **Step 5: Add the definition schema**

Define `IriUrn`, `InferenceEndpoint`, `ServedModel`, and `InferenceServiceAttributes`. Require `schema_version: "1.0.0"`; use `uniqueItems: true` for `inference_apis`; and reference the two structured schemas from their arrays.

- [ ] **Step 6: Add the companion operational-state schema**

Keep it in a clearly separate section and use this contract:

```yaml
InferenceServiceState:
  type: object
  required:
    - schema_version
  properties:
    schema_version:
      type: string
      enum:
        - "1.0.0"
    active_models:
      type: array
      uniqueItems: true
      items:
        type: string
```

State that each `active_models` item references a `served_models.id`; omission means unknown or unreported; an empty array means the service reports no active models. Do not imply integration with the core Facility API OpenAPI.

- [ ] **Step 7: Add consistent definition and state examples**

Show a vLLM service with an OpenAI-compatible endpoint, at least two `served_models` entries, and a separate state instance listing one active ID. Ensure the state ID exactly matches a catalog ID.

- [ ] **Step 8: Verify inference profile coverage and separation**

```bash
rg -n 'inference_technology|technology_version|inference_apis|inference_endpoints|served_models|active_models|inference-api:(openai|kserve-v2)|inference-technology:(vllm|hugging-face-tgi|nvidia-triton|kserve)|InferenceServiceState' registry/urn-registry-attributes-service-inference.md
```

Expected: all definition attributes, all six controlled values, and the separate state contract appear.

- [ ] **Step 9: Commit the inference profile**

```bash
git add registry/urn-registry-attributes-service-inference.md
git commit -m "docs: define inference service attributes and state"
```

---

### Task 4: Service Relationship Profiles

**Files:**
- Create: `registry/link-profile-hosted-on.md`
- Create: `registry/link-profile-accesses-mount.md`
- Reference: `registry/link-profile-has-node.md`
- Reference: `registry/link-profile-mounted-on.md`

**Interfaces:**
- Consumes: Service resource types from Task 1, compute and mount target types, and link semantics from the design.
- Produces: Normative semantic contracts for relationship indexes and HAL examples.

- [ ] **Step 1: Run the failing link-profile checks**

```bash
test -e registry/link-profile-hosted-on.md
test -e registry/link-profile-accesses-mount.md
```

Expected: both checks fail because neither link profile exists.

- [ ] **Step 2: Create `iri:hosted-on` metadata and semantics**

Use source types DTN or inference service, target types compute system or compute node, cardinality `0..*`, target classification Resource, relatively static topology, and authorization-filtered visibility. Explain that the link does not represent current routing, live replica placement, health, or availability.

- [ ] **Step 3: Add `iri:hosted-on` HAL examples**

Include a singular system target and plural node targets:

```json
{
  "_links": {
    "iri:hosted-on": [
      { "href": "/api/v2/status/resources/node-001" },
      { "href": "/api/v2/status/resources/node-002" }
    ]
  }
}
```

- [ ] **Step 4: Create `iri:accesses-mount` metadata and semantics**

Use DTN service as the only source, filesystem mount as the target, cardinality `0..*`, target classification Relationship Resource, relatively static configured access topology, and authorization-filtered visibility. State that the link does not imply current mount availability, endpoint reachability, credential validity, unrestricted access, or active transfer activity.

- [ ] **Step 5: Add `iri:accesses-mount` HAL examples and cross-relation guidance**

Include plural mount targets. Explain why the mount is more precise than a direct filesystem target, why `hostedOn` plus `mountedOn` must not be used to infer DTN access, and why no inverse is initially registered.

- [ ] **Step 6: Verify link-profile contract fields**

```bash
rg -n 'Source representation type|Target representation type|Cardinality|Target stability|Authorization affects visibility|Target classification|Relationship volatility|_links' registry/link-profile-hosted-on.md registry/link-profile-accesses-mount.md
```

Expected: every required link-profile field and HAL representation is present in both documents.

- [ ] **Step 7: Commit both link profiles**

```bash
git add registry/link-profile-hosted-on.md registry/link-profile-accesses-mount.md
git commit -m "docs: define service topology relationships"
```

---

### Task 5: Root, Navigation, and Cross-Domain Integration

**Files:**
- Modify: `registry/urn-registry-root.md`
- Modify: `registry/README.md`
- Modify: `registry/urn-registry-type-compute.md`
- Modify: `registry/urn-registry-type-compute-taxonomy.md`
- Modify: `registry/urn-registry-type-storage.md`
- Modify: `registry/urn-registry-type-storage-taxonomy.md`

**Interfaces:**
- Consumes: All Service registry, profile, and link documents from Tasks 1-4.
- Produces: Complete discovery paths from the root and all affected domain indexes.

- [ ] **Step 1: Capture the current overlapping-file state**

```bash
git status --short
git diff -- registry/README.md registry/urn-registry-type-compute.md registry/urn-registry-type-storage.md
```

Expected: any user-owned changes are visible and must remain intact.

- [ ] **Step 2: Update the root registry**

Link `urn:doe-iri:resource:service` to `urn-registry-type-service.md`, show `dtn` and `inference` beneath it in the resource taxonomy, register `urn:doe-iri:service` as the service controlled-vocabulary branch, and delegate detailed values to the Service registry.

- [ ] **Step 3: Add complete Service navigation to the registry README**

Add Service beside Storage and Compute in the documentation tree. Add entry points, both resource attribute profiles, both relationship profiles, the service controlled-vocabulary branch, and appropriate “Where do I start?” navigation.

- [ ] **Step 4: Add incoming `iri:hosted-on` references to Compute**

Update the compute type registry and taxonomy relationship sections to identify service source types, compute-system-or-node targets, `0..*` service-side cardinality, relative stability, authorization filtering, and the link-profile document. Do not alter existing `iri:has-node`, `iri:has-cpu`, or `iri:has-gpu` semantics.

- [ ] **Step 5: Add incoming `iri:accesses-mount` references to Storage**

Update the storage type registry and taxonomy relationship sections to identify DTN source, mount target, `0..*` DTN-side cardinality, relative stability, authorization filtering, and the link-profile document. Do not alter `iri:has-mount` or `iri:mounted-on` semantics.

- [ ] **Step 6: Verify navigation and cross-domain consistency**

```bash
rg -n 'urn-registry-type-service|attributes-service-(dtn|inference)|link-profile-(hosted-on|accesses-mount)' registry/README.md registry/urn-registry-root.md
rg -n 'iri:hosted-on' registry/urn-registry-type-compute.md registry/urn-registry-type-compute-taxonomy.md
rg -n 'iri:accesses-mount' registry/urn-registry-type-storage.md registry/urn-registry-type-storage-taxonomy.md
```

Expected: root navigation includes the Service domain and both incoming cross-domain relationships are indexed by their target domains.

- [ ] **Step 7: Commit integration changes without unrelated files**

```bash
git add registry/urn-registry-root.md registry/README.md registry/urn-registry-type-compute.md registry/urn-registry-type-compute-taxonomy.md registry/urn-registry-type-storage.md registry/urn-registry-type-storage-taxonomy.md
git commit -m "docs: integrate service types across registry indexes"
```

---

### Task 6: Governing RFC and Project-Context Reconciliation

**Files:**
- Modify: `rfc/rfc-iri-urn-structure-and-registry.md`
- Modify: `rfc/rfc-type-specific-attributes.md`
- Modify: `docs/ai-project-context.md`

**Interfaces:**
- Consumes: Canonical namespace decisions and completed registry documents.
- Produces: Specifications and future-agent context consistent with the active registry.

- [ ] **Step 1: Record the stale resource-type references before editing**

```bash
rg -n 'urn:doe-iri:service:(generic|website|dtn(:globus)?)' rfc/rfc-iri-urn-structure-and-registry.md rfc/rfc-type-specific-attributes.md
```

Expected: existing draft uses of `service:*` as ResourceType values are reported.

- [ ] **Step 2: Reconcile the governing URN specification**

Revise the domain descriptions so `resource` owns resource typing and `service` owns service controlled vocabularies. Change the legacy mappings to:

```text
website -> urn:doe-iri:resource:website
service -> urn:doe-iri:resource:service
```

Replace service resource examples with `urn:doe-iri:resource:service:dtn` or `urn:doe-iri:resource:service:inference`. Replace the Globus draft type example with `urn:doe-iri:service:dtn-technology:globus` and describe it as a controlled attribute value.

- [ ] **Step 3: Reconcile the type-specific-attributes RFC**

Change Resource `resource_type` examples from `urn:doe-iri:service:*` to canonical `urn:doe-iri:resource:service:*`. Do not change controlled service vocabulary examples to the resource branch.

- [ ] **Step 4: Extend the AI project context**

Add the Service domain model, exact controlled values, definition/state split, and both link semantics. Record that `urn:doe-iri:resource:service:*` is resource classification and `urn:doe-iri:service:*` is controlled vocabulary. Include DTN-to-mount reasoning and inference `served_models` versus `active_models` guidance.

- [ ] **Step 5: Verify stale-reference removal and intended vocabulary retention**

```bash
if rg -n 'urn:doe-iri:service:(generic|website|dtn:globus)' rfc/rfc-iri-urn-structure-and-registry.md rfc/rfc-type-specific-attributes.md; then exit 1; fi
rg -n 'urn:doe-iri:resource:service:(dtn|inference)|urn:doe-iri:service:dtn-technology:globus' rfc/rfc-iri-urn-structure-and-registry.md rfc/rfc-type-specific-attributes.md docs/ai-project-context.md
```

Expected: the first command finds no obsolete resource-type forms; the second finds canonical resource types and the controlled Globus technology value.

- [ ] **Step 6: Commit specification and context reconciliation**

```bash
git add rfc/rfc-iri-urn-structure-and-registry.md rfc/rfc-type-specific-attributes.md docs/ai-project-context.md
git commit -m "docs: align service namespaces and registry context"
```

---

### Task 7: Mechanical Validation and Final Review

**Files:**
- Validate: all files created or modified in Tasks 1-6
- Modify only if required: files with deterministic link, formatting, or index defects found during validation

**Interfaces:**
- Consumes: Complete implementation from Tasks 1-6.
- Produces: Evidence that links, taxonomies, profiles, examples, and namespace references are mechanically consistent.

- [ ] **Step 1: Check whitespace and patch integrity**

```bash
git diff --check HEAD~6..HEAD
```

Expected: no whitespace errors. If commit count differs because a task did not require a commit, use the design commit `28759dd` as the lower bound.

- [ ] **Step 2: Check all local Markdown links in changed documents**

Run this repository-local link scan. It extracts Markdown targets, skips URI and pure-anchor targets, removes target anchors, resolves paths relative to each source document, and fails if a target does not exist:

```bash
ruby -e 'missing=[]; ARGV.each { |file| text=File.read(file); text.scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each { |raw| target=raw.sub(/^</, "").sub(/>$/, ""); next if target =~ /\A(?:[a-z][a-z0-9+.-]*:|#)/i; path=target.split("#", 2).first; next if path.empty?; resolved=File.expand_path(path, File.dirname(file)); missing << "#{file}: #{target}" unless File.exist?(resolved) } }; abort(missing.join("\n")) unless missing.empty?' \
  registry/README.md \
  registry/urn-registry-root.md \
  registry/urn-registry-type-service.md \
  registry/urn-registry-type-service-taxonomy.md \
  registry/urn-registry-attributes-service-dtn.md \
  registry/urn-registry-attributes-service-inference.md \
  registry/link-profile-hosted-on.md \
  registry/link-profile-accesses-mount.md \
  registry/urn-registry-type-compute.md \
  registry/urn-registry-type-compute-taxonomy.md \
  registry/urn-registry-type-storage.md \
  registry/urn-registry-type-storage-taxonomy.md \
  rfc/rfc-iri-urn-structure-and-registry.md \
  rfc/rfc-type-specific-attributes.md \
  docs/ai-project-context.md
```

Validate this exact set:

```text
registry/README.md
registry/urn-registry-root.md
registry/urn-registry-type-service.md
registry/urn-registry-type-service-taxonomy.md
registry/urn-registry-attributes-service-dtn.md
registry/urn-registry-attributes-service-inference.md
registry/link-profile-hosted-on.md
registry/link-profile-accesses-mount.md
registry/urn-registry-type-compute.md
registry/urn-registry-type-compute-taxonomy.md
registry/urn-registry-type-storage.md
registry/urn-registry-type-storage-taxonomy.md
rfc/rfc-iri-urn-structure-and-registry.md
rfc/rfc-type-specific-attributes.md
docs/ai-project-context.md
```

Expected: zero missing local targets.

- [ ] **Step 3: Compare the service taxonomy and profile values**

```bash
for value in \
  dtn-technology:globus dtn-technology:xrootd \
  transfer-protocol:https transfer-protocol:gridftp transfer-protocol:xrootd transfer-protocol:sftp \
  inference-api:openai inference-api:kserve-v2 \
  inference-technology:vllm inference-technology:hugging-face-tgi inference-technology:nvidia-triton inference-technology:kserve; do
  rg -q "urn:doe-iri:service:$value" registry/urn-registry-type-service-taxonomy.md || exit 1
done
```

Run the corresponding exact profile checks:

```bash
for value in \
  dtn-technology:globus dtn-technology:xrootd \
  transfer-protocol:https transfer-protocol:gridftp transfer-protocol:xrootd transfer-protocol:sftp; do
  rg -q "urn:doe-iri:service:$value" registry/urn-registry-attributes-service-dtn.md || exit 1
done
for value in \
  inference-api:openai inference-api:kserve-v2 \
  inference-technology:vllm inference-technology:hugging-face-tgi inference-technology:nvidia-triton inference-technology:kserve; do
  rg -q "urn:doe-iri:service:$value" registry/urn-registry-attributes-service-inference.md || exit 1
done
```

Expected: every registered value is present in the consolidated taxonomy and exactly one applicable profile.

- [ ] **Step 4: Check relationship agreement**

```bash
rg -n 'iri:(hostedOn|accessesMount)' registry/README.md registry/urn-registry-type-service.md registry/urn-registry-type-service-taxonomy.md registry/urn-registry-type-compute.md registry/urn-registry-type-compute-taxonomy.md registry/urn-registry-type-storage.md registry/urn-registry-type-storage-taxonomy.md registry/link-profile-hosted-on.md registry/link-profile-accesses-mount.md
```

Expected: `hostedOn` appears in Service and Compute indexes; `accessesMount` appears in Service and Storage indexes; source and target types agree with the link profiles.

- [ ] **Step 5: Check definition/state separation and examples**

Confirm by inspection and search that `served_models` appears in `InferenceServiceAttributes`, `active_models` appears only in the companion state section/schema/example, all active IDs exist in the example catalog, and no DTN definition attribute encodes current transfer or endpoint state.

- [ ] **Step 6: Search for namespace regressions**

```bash
rg -n 'urn:doe-iri:service:(generic|website|dtn:globus)' registry rfc docs
rg -n 'urn:doe-iri:resource:service:(dtn|inference)' registry rfc docs
```

Expected: no stale service-as-resource matches from the first command; broad canonical coverage from the second. Any historical mention must be clearly labeled as superseded rather than presented as registered.

- [ ] **Step 7: Review the final diff and repository status**

```bash
git diff 28759dd..HEAD --stat
git diff 28759dd..HEAD
git status --short
```

Expected: only approved implementation and mechanical corrections are committed; untracked or unrelated user files remain untouched.

- [ ] **Step 8: Commit mechanical corrections if any**

```bash
git add \
  registry/README.md \
  registry/urn-registry-root.md \
  registry/urn-registry-type-service.md \
  registry/urn-registry-type-service-taxonomy.md \
  registry/urn-registry-attributes-service-dtn.md \
  registry/urn-registry-attributes-service-inference.md \
  registry/link-profile-hosted-on.md \
  registry/link-profile-accesses-mount.md \
  registry/urn-registry-type-compute.md \
  registry/urn-registry-type-compute-taxonomy.md \
  registry/urn-registry-type-storage.md \
  registry/urn-registry-type-storage-taxonomy.md \
  rfc/rfc-iri-urn-structure-and-registry.md \
  rfc/rfc-type-specific-attributes.md \
  docs/ai-project-context.md
git commit -m "docs: fix service registry consistency"
```

If validation requires no corrections, do not create an empty commit.
