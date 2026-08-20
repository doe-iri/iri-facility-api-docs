Read AGENTS.md first.

Audit current user-facing IRI v2 documentation and examples outside:

    registry/
    rfc/

Primary scope:

    README.md
    specification-v2/
    docs/

Exclude:

    docs/superpowers/
    specification-v1/

unless explicitly referenced as current normative documentation.

Goal:
Ensure every current HAL `_links` example uses target-representation profile
semantics consistently with the registry and RFCs.

Do not alter generated OpenAPI simply because a string appears in generated
content. If a generated artifact requires an update, modify its authoritative
source and regenerate using the repository's normal process.

===============================================================================
1. FIND EXAMPLES
===============================================================================

    rg -n '"_links"|_links:' \
      README.md \
      specification-v2 \
      docs \
      --glob '!docs/superpowers/**' \
      2>/dev/null || true

For every link object:

- identify target;
- identify target representation type;
- determine canonical target profile from the registry;
- add/correct `profile` where applicable.

Use exactly the same rules from the registry/RFC passes.

===============================================================================
2. ADD A REGRESSION RULE TO AGENTS.md
===============================================================================

Update AGENTS.md with a concise documentation-generation rule equivalent to:

### HAL Example Target Profiles

In documentation examples, the HAL Link Object `profile` member identifies the
profile of the LINK TARGET, not the relation or source representation.

When the target is an IRI representation with a known canonical profile,
documentation examples SHOULD include the target `profile`.

Examples:

`iri:has-mount`
    → `https://iri.science/profiles/resource-definition/storage/mount`

`iri:located-at`
    → `https://iri.science/profiles/facility/site`

`iri:has-capability`
    → `https://iri.science/profiles/account/capability`

For `_links.self`, use the profile applicable to the represented object. In a
Resource Definition Profile example, use the most-specific Resource Definition
Profile for that representation.

Do not add a representation `profile` merely because a link exists.

In particular, do not add an IRI representation profile to:
- `curies`;
- `service-desc`;
- ordinary external `help` targets;
- operation-affordance targets such as `iri:submit-job`.

For polymorphic relations such as `iri:attached-to` and `iri:hosted-on`,
determine the profile from the actual target type shown in the example.

The registered relation definition is authoritative for the target
classification.

===============================================================================
3. FINAL VALIDATION
===============================================================================

Search the complete current scope:

    rg -n '"_links"|_links:' \
      registry \
      rfc \
      specification-v2 \
      README.md \
      docs \
      --glob '!docs/superpowers/**' \
      2>/dev/null || true

    rg -n '"profile"\s*:' \
      registry \
      rfc \
      specification-v2 \
      README.md \
      docs \
      --glob '!docs/superpowers/**' \
      2>/dev/null || true

Also search for obsolete profile namespaces:

    rg -n \
      'https://iri\.science/profiles/(storage|compute/(system|node|cpu|gpu))' \
      registry \
      rfc \
      specification-v2 \
      README.md \
      docs \
      --glob '!docs/superpowers/**' \
      2>/dev/null || true

Run:

    git diff --check
    git status --short
    git diff --stat
    git diff

FINAL REVIEW REQUIREMENTS

Verify:

1. Every `profile` describes its link target.

2. No link uses a relation URI such as:
       https://iri.science/rels/has-mount
   as its profile.

3. No Resource Type URN is used as a HAL `profile`.

4. No `iri:submit-job` link incorrectly advertises:
       https://iri.science/profiles/compute/job

5. No service-desc link receives an IRI representation profile.

6. monitor links to Task use:
       https://iri.science/profiles/task

7. self links identify the profile of their current representation.

8. Fixed-type Resource relations use their Resource Definition Profile.

9. Generic Resource target relations use:
       https://iri.science/profiles/status/resource
   unless a more-specific target is explicitly established.

10. Polymorphic relation examples use the actual target type.

11. Arrays have the correct profile on each individual Link Object.

12. No historical docs were rewritten unintentionally.

Report:
- files changed;
- number of Link Objects updated;
- profiles added;
- profiles corrected;
- links where profile was intentionally omitted;
- unresolved cases, if any.

Do not commit or push.

