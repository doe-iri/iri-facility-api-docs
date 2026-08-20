Read AGENTS.md and the current:

    rfc/rfc-type-specific-attributes.md

Then update ONLY:

    registry/profiles/status/resource.md

Do not modify other files.

1. Add attributes to the Structural Contract property table.

The current V2 OpenAPI Resource schema defines attributes as optional and
nullable.

Use semantic wording equivalent to:

    | `attributes` | No | Optional type-specific metadata whose semantics are
      defined by the applicable Resource Definition Profile selected by
      `resource_type`. |

Make clear that OpenAPI remains authoritative for:
- optionality;
- nullability;
- JSON structure;
- additionalProperties behavior.

2. Align Resource Definition Profile semantics with the new RFC.

A Resource Definition Profile:
- supplements the common Resource profile;
- is selected through the registered mapping associated with resource_type;
- defines type-specific semantics;
- may define attributes, relationships, and operation affordances;
- does not replace the common Resource representation;
- does not create a separate IRI v2 Resource Definition API object.

3. Remove blanket language saying Resource Definition Profiles can contain only
"relatively stable" attributes if that language conflicts with the new RFC.

Do not introduce a separate Resource State architecture.

4. Preserve current_status.

Keep the distinction:

    Resource.current_status
        current reported Resource condition

    Event.status
        historical condition associated with Event.occurred_at

5. Do not reintroduce:

    urn:doe-iri:resource:storage:filesystem:scratch

Validation:

    git diff --check
    git diff -- registry/profiles/status/resource.md

Report the semantic changes made.

Do not commit or push.

