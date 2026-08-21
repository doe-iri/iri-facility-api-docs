# Model Selection Guidance

The repository intentionally does not pin model IDs.

Choose models in the Codex UI/CLI according to what is actually available to
the current account and workspace.

Suggested intent:

| Work | Preferred capability |
|---|---|
| Ontology, taxonomy, compatibility, new semantics | Strongest available reasoning model; high reasoning |
| Implementing an already-approved design | Balanced available coding model; medium reasoning |
| Mechanical link/format/index maintenance | Efficient available model; low/medium reasoning |

The custom agent files define role and sandbox boundaries but inherit the
parent session's model and reasoning configuration.

This avoids failures caused by a project file pinning a model that is not
available to a particular account, workspace, client version, or rollout.
