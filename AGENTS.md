# DOE-IRI Facility API Documentation — Repository Instructions

Do not spawn subagents or use collaboration tools.

Perform all work in the current agent/thread.

These instructions apply repository-wide. More-specific `AGENTS.md` files under
`registry/`, `rfc/`, and `specification-v2/` add rules for those areas.

Keep this root file intentionally small. Do not move domain-specific rules back
here unless they apply to the entire repository.

## 1. Source-of-Truth Precedence

Resolve authority by concern:

```text
Checked-out IRI v2 OpenAPI
    Structural API contract: properties, types, required/nullable rules,
    formats, operation shapes, and structural validation.

Governing DOE-IRI URN specification
    Namespace syntax, hierarchy matching, registration procedure, delegation,
    extension rules, and conformance.

registry/urns/
    Assigned DOE-IRI URNs, controlled values, parentage, and lifecycle status.

registry/relations/
    Registered IRI link-relation names and complete relation semantics.

rfc/rfc-hal-links.md
    HAL wire conventions, legacy URI-property migration, and common hypermedia
    mappings.

registry/profiles/
    Semantic and interoperability conventions for API representations.

docs/decisions/
    Architectural rationale only; non-normative.

docs/ai-project-context.md
    Architectural and historical context only; non-normative.
```

When authorities for different concerns appear to disagree, identify whether
the mismatch is structural, semantic, registry-related, or stale documentation.
Do not silently choose one source and rewrite another.

## 2. IRI v2 Modeling Scope

IRI v2 does not define or require separate Resource Definition and Resource
State representations, endpoints, or conformance models.

Resource Definition Profiles specialize the existing IRI v2 `Resource`
representation according to `resource_type`.

Do not introduce a separate `ResourceDefinition`, `ResourceState`, state
endpoint, or state relation unless explicitly working on a future IRI version.

Preserve valid v2 distinctions such as:

- `Resource.current_status` versus historical `Event.status`;
- configured topology versus current reachability;
- capability support versus current availability;
- relationship existence versus target health;
- Job and Task lifecycle state.

## 3. Identifier Roles

Keep these concepts distinct:

```text
Resource Type URN
    WHAT kind of Resource is this?

Representation Profile URI
    WHAT semantic representation contract applies?

Link relation
    WHY is a target related or applicable?

href / instance URI
    WHERE is the target representation or operation entry point?

OpenAPI
    HOW are the JSON representation and operations structurally defined?
```

Do not derive API paths from Resource Type URNs or profile identifiers.

## 4. Scoped Instructions

Before changing files under one of these areas, apply the closest local
`AGENTS.md`:

```text
registry/AGENTS.md
registry/urns/AGENTS.md
registry/profiles/AGENTS.md
registry/relations/AGENTS.md
rfc/AGENTS.md
specification-v2/AGENTS.md
```

Do not load unrelated scoped instruction files into a task packet.

## 5. Agent Workflow

Use named agents only for bounded tasks.

Preferred sequence:

```text
targeted discovery
    ↓
semantic decision when needed
    ↓
bounded implementation
    ↓
fresh read-only validation
```

Available project agents:

- `registry_scout` — bounded read-only discovery.
- `registry_architect` — one bounded semantic decision.
- `registry_editor` — one approved bounded implementation.
- `registry_validator` — fresh read-only validation of one completed chunk.

Do not run overlapping write-heavy agents in parallel.

If custom agents are unavailable, preserve the same stages in the parent
thread rather than skipping semantic review or validation.

## 6. Context and Task-Size Rules

Keep the parent thread focused on requirements, decisions, and concise
handoffs. Exploration logs, long grep output, and full file contents should not
be copied forward unless required.

A normal implementation task SHOULD affect no more than about six files.
Mechanically inseparable propagation may exceed this, but do not combine
multiple independent semantic concerns into one task.

When work crosses multiple authority domains such as URNs, relations, profiles,
RFCs, and OpenAPI, split it into ordered chunks unless the changes are
mechanically inseparable.

If a task expands materially beyond its approved scope:

1. stop the current bounded task;
2. report the newly discovered concern;
3. create a separate work item.

## 7. Handoff Packet

Pass only the context required by the next agent:

```text
TASK
One bounded goal.

AUTHORITATIVE SOURCES
Only the sources needed for this decision/change.

APPROVED DECISION
The semantic outcome already agreed, if applicable.

FILES ALLOWED TO CHANGE
Explicit paths or a narrowly defined directory.

ACCEPTANCE CRITERIA
Concrete conditions for success.

OUT OF SCOPE
Adjacent work that must not be absorbed into this task.
```

Do not pass raw prior transcripts as the default handoff mechanism.

## 8. Change Discipline

- Make the smallest coherent change.
- Preserve unrelated user edits.
- Do not perform opportunistic cleanup outside the approved scope.
- Do not invent URNs, relations, profile URIs, or OpenAPI fields.
- Do not change lifecycle status silently.
- Do not commit, push, create branches, or open PRs unless explicitly asked.
- Prefer targeted validation over repository-wide scans for every small edit.
- Use repository-wide validation only when the task genuinely has repository-wide scope.

## 9. Documentation Classes

Normative or authoritative documentation belongs in the appropriate RFC,
registry, profile, relation, or OpenAPI source.

`docs/decisions/` records accepted architectural rationale and MUST identify
itself as non-normative. If a decision record disagrees with current normative
material, the normative source wins and the decision record should be updated
or marked superseded.

Do not retain completed AI/Codex execution plans as current design authority.
Git history provides implementation history.

## 10. Runtime Configuration Boundary

Repository configuration must not contain:

- API keys or credentials;
- CBORG provider secrets;
- machine-specific endpoints;
- a pinned model merely to override the user's selected runtime profile.

Project agents intentionally omit `model` and `model_reasoning_effort` so they
inherit the selected parent Codex session unless an explicit spawn override is
used.

Use user-level Codex configuration for provider, credentials, model aliases,
and runtime quality profiles.
