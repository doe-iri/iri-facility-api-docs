Read AGENTS.md first.

Modify ONLY:

    rfc/rfc-hal-links.md
    registry/profiles/task.md

PART A — rfc/rfc-hal-links.md

1. Remove wording that assumes "dynamic state resources" are an established
IRI v2 architectural layer.

Focus the RFC on:
- related resources;
- topology;
- operation entry points;
- migration of URI-valued properties;
- service descriptions.

Do not invent a Resource State relation.

2. Remove the obsolete statement that current V2 ResourceType is a legacy enum
requiring later migration.

Current IRI v2 resource_type is an extensible string containing a DOE-IRI
Resource Type URN.

3. Ensure the mount profile is:

    https://iri.science/profiles/resource-definition/storage/mount

4. Change wording such as:

    consult the registered profile for each iri:* relation

to:

    consult the registered relation definition for each iri:* relation

5. Preserve:

    TaskSubmitResponse.task_uri -> monitor

PART B — registry/profiles/task.md

Align Task hypermedia semantics with the HAL RFC.

The relationship is:

    TaskSubmitResponse.task_uri
            ↓
    _links.monitor.href
            ↓
    Task representation
            ↓
    Task._links.self.href

Explain:

- `monitor` describes why TaskSubmitResponse links to the Task.
- `self` identifies the Task representation once retrieved.
- Their href values may be identical while their relation semantics differ.
- Do not invent `iri:monitor`.

A HAL-enabled TaskSubmitResponse example may use:

    {
      "task_id": "task-123",
      "task_uri": "https://api.example.org/api/v2/task/task-123",
      "_links": {
        "monitor": {
          "href": "https://api.example.org/api/v2/task/task-123",
          "type": "application/hal+json",
          "profile": "https://iri.science/profiles/task"
        }
      }
    }

Keep `_links.self` on the Task representation.

Validation:

    git diff --check
    git diff -- rfc/rfc-hal-links.md registry/profiles/task.md

Do not commit or push.

