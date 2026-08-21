# Codex Workflow for DOE-IRI Registry Work

> **Status:** Working guidance for repository contributors and Codex sessions.
> This document is operational guidance, not an IRI protocol or registry
> authority.

## Purpose

The repository uses bounded agent roles to keep context small and prevent
semantic, implementation, and validation work from collapsing into one long
session.

The preferred workflow is:

```text
Parent thread
    requirements and task boundary
        │
        ▼
registry_scout
    targeted evidence only
        │
        ▼
registry_architect
    one semantic decision when needed
        │
        ▼
Parent thread
    approves decision and creates compact work packet
        │
        ▼
registry_editor
    bounded implementation
        │
        ▼
registry_validator
    fresh read-only validation
```

Not every task requires all four agents.

Mechanical fixes with already-approved semantics can go directly to
`registry_editor`, followed by `registry_validator`.

## Why the Workflow Is Bounded

Large repository-wide prompts tend to combine several kinds of context:

- architecture history;
- current RFC rules;
- registry assignments;
- profile semantics;
- OpenAPI structures;
- search output;
- implementation diffs;
- validation output.

Most individual changes need only a small subset.

The workflow intentionally discards exploration noise between stages and
passes forward only the approved facts needed by the next role.

## Handoff Packet Template

```text
TASK
<one bounded outcome>

AUTHORITATIVE SOURCES
- <file>
- <file>

APPROVED DECISION
<semantic decision, or "No new semantic decision required">

FILES ALLOWED TO CHANGE
- <path>
- <path>

ACCEPTANCE CRITERIA
- <condition>
- <condition>

OUT OF SCOPE
- <adjacent concern>
- <adjacent concern>
```

Do not attach a complete previous transcript when this packet is sufficient.

## Example

```text
TASK
Correct HAL target profiles in storage Resource Definition examples.

AUTHORITATIVE SOURCES
- registry/relations/has-mount.md
- registry/relations/provides-filesystem.md
- registry/profiles/README.md

APPROVED DECISION
HAL Link Object profile identifies the target representation.

FILES ALLOWED TO CHANGE
- registry/profiles/resource-definition/storage/system.md
- registry/profiles/resource-definition/storage/filesystem.md
- registry/profiles/resource-definition/storage/mount.md

ACCEPTANCE CRITERIA
- iri:has-mount uses the storage/mount target profile
- iri:provides-filesystem uses the storage/filesystem target profile
- service-desc receives no IRI representation profile
- changed JSON examples parse
- git diff --check passes

OUT OF SCOPE
- RFC changes
- OpenAPI changes
- new relations
- unrelated formatting
```

## Recommended Task Size

Normal implementation chunks should generally stay within one semantic concern
and about six changed files.

Split work when it independently affects:

- URN taxonomy/registration;
- relation semantics;
- representation profile semantics;
- RFC rules;
- OpenAPI structural contract.

A repository-wide lexical migration may touch more files when the semantic
decision is already fixed and propagation is mechanical.

## Fresh Validation

Validation should normally run in a new read-only agent context.

The validator receives:

- changed files;
- diff;
- acceptance criteria;
- directly applicable authority sources.

It does not need the full discovery or implementation conversation.

## Runtime Model Policy

Project agent TOMLs intentionally do not pin `model` or
`model_reasoning_effort`.

The selected parent Codex session remains the runtime quality control. Provider,
credentials, model aliases, and user-local profiles belong outside the
repository.

## Verifying Instruction Discovery

Useful checks include:

```bash
codex --ask-for-approval never \
  "Summarize the current instructions and list their source files."
```

From a scoped directory:

```bash
codex --cd registry/profiles --ask-for-approval never \
  "Show which instruction files are active."
```

For ordinary profile work, this should load the root instructions plus
`registry/AGENTS.md` and `registry/profiles/AGENTS.md`, not unrelated RFC or
OpenAPI instruction files.
