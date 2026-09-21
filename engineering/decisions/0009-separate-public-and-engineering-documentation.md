# 0009: Separate public and engineering documentation

  - Status: Accepted
  - Date: 2026-09-20
  - Deciders: IRI documentation maintainers
  - Supersedes: None
  - Superseded by: None

  > This decision record is non-normative. It documents repository-maintenance
  > rationale and does not define IRI API, registry, or protocol requirements.

  ## Context

  GitHub Pages publishes the repository's public documentation from `main:/docs`,
  and the local and CI workflows build that tree with Jekyll. Repository
  maintenance material, including detailed Codex workflows and decision records,
  is not part of the public explanatory documentation and should not be included
  in the published site.

  A clear directory boundary reduces the risk of publishing internal process
  material and keeps public documentation distinct from engineering rationale.
  This decision complements
  [0008: Use GitHub Pages as the primary documentation site](0008-use-github-pages-as-the-primary-documentation-site.md).

  ## Decision

  Reserve `docs/` for public, human-oriented documentation and the minimum
  configuration needed to build and govern that documentation. Store
  repository-maintenance material under `engineering/`:

  - detailed Codex workflows in `engineering/codex/`; and
  - decision records in `engineering/decisions/`.

  Keep concise, automatically discovered Codex instructions in `AGENTS.md`
  files. The root `AGENTS.md` provides repository-wide entry instructions and
  references the detailed workflow. Scoped `AGENTS.md` files may remain beside
  the content they govern but must not be treated as public documentation or
  included in generated site output.

  Content under `docs/` remains explanatory and must not override the applicable
  specifications, RFCs, registries, profiles, relation definitions, or OpenAPI
  sources.

  ## Consequences

  ### Positive

  - The GitHub Pages publication boundary is obvious and auditable.
  - Detailed internal workflow and decision documents remain outside the public
    documentation tree.
  - Codex receives concise automatically discovered instructions while detailed
    guidance remains available on demand.
  - Public explanatory documentation remains distinct from normative and
    authoritative sources.

  ### Negative

  - Existing links to relocated workflow and decision files must be updated.
  - Contributors must understand the distinction between public documentation,
    engineering documentation, and normative sources.
  - Build configuration must continue to exclude any colocated operational
    metadata from generated site output.

  ## Alternatives considered

  ### Keep all files under `docs/` and exclude selected paths

  Rejected because an exclusion list is easier to misconfigure and makes the
  publication boundary less obvious.

  ### Store all Codex material under `.codex/`

  Rejected because `.codex/` may also hold tool and environment configuration.
  Human-governed engineering documentation is clearer in a visible,
  purpose-named directory.

  ## Validation

  - GitHub Pages must continue to publish from `main:/docs`.
  - Local and CI builds must use `docs/` as the Jekyll source tree.
  - `.github/workflows/docs-check.yml` must validate only the public
    documentation site.
  - Generated `_site/` output must not contain content from `engineering/` or
    scoped repository-maintenance instructions.
  - Reviews must reject detailed internal process or decision-record content
    added under `docs/`.
  - Documentation changes must pass:

    ```sh
    ruby scripts/validate-docs.rb
    BUNDLE_GEMFILE=docs/Gemfile bundle exec jekyll build --source docs --destination _site/iri-facility-api-docs
    BUNDLE_GEMFILE=docs/Gemfile bundle exec htmlproofer _site --disable-external

