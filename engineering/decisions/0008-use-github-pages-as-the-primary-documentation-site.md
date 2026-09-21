# 0008: Use GitHub Pages as the primary documentation site

  - Status: Accepted
  - Date: 2026-09-20
  - Deciders: IRI documentation maintainers
  - Supersedes: None
  - Superseded by: None

  ## Context

  The project previously maintained closely related content in the documentation repository and a separate GitHub Wiki repository. Coordinated
  manual edits could drift, and the Wiki did not provide the same build validation, navigation, or API-reference integration as a generated
  documentation site.

  ## Decision

  Use `iri-facility-api-docs` as the only authoritative documentation source. Publish the public documentation from `docs/` as the repository’s
  GitHub Pages project site after changes reach the default branch.

  Build the site with Jekyll using `docs/Gemfile` and `docs/Gemfile.lock`. GitHub Pages publishes from `main:/docs`; generated `_site/` output
  is not committed.

  The former `iri-facility-api-docs.wiki` repository is retired. Do not edit or synchronize content to it, recreate a Wiki mirror, or restore
  the retired Wiki synchronization scripts.

  ## Consequences

  ### Positive

  - Public documentation changes use the repository’s pull-request workflow.
  - Documentation, links, and examples can be validated before publication.
  - Human and Codex contributors update one authoritative repository.
  - Navigation, search, styling, and API-reference presentation are configurable.
  - Documentation history remains alongside the specifications and supporting sources.

  ### Negative

  - Direct browser editing of the authoritative Wiki is discontinued.
  - Existing Wiki URLs may require external redirects or supersession notices.
  - The Pages build and its dependencies require ongoing maintenance.

  ## Alternatives considered

  ### Continue editing both repositories

  Rejected because coordinated commits cannot provide a truly atomic update and remain vulnerable to drift.

  ### Automatically mirror the documentation tree to the Wiki

  Rejected because Wiki rendering and navigation differ from the generated documentation site, and maintaining a second copy would add
  operational complexity without creating another authoritative source.

  ## Validation

  The migration is complete when:

  - `docs/` is the canonical source for human-oriented documentation.
  - GitHub Pages publishes the site from `main:/docs`.
  - The retired Wiki is no longer edited or synchronized.
  - Documentation changes pass:

    ```sh
    ruby scripts/validate-docs.rb
    BUNDLE_GEMFILE=docs/Gemfile bundle exec jekyll build --source docs --destination _site/iri-facility-api-docs
    BUNDLE_GEMFILE=docs/Gemfile bundle exec htmlproofer _site --disable-external
    ```
