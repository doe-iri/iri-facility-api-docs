# GitHub Pages documentation instructions

These instructions apply to all files under `docs/`.

## Source of truth

- `docs/` is the canonical source for the human-oriented IRI Facility API
  documentation published with GitHub Pages.
- Do not maintain or synchronize a second copy in a GitHub wiki repository.
- This site is explanatory. Versioned specifications, RFCs, registries,
  profiles, and OpenAPI sources remain authoritative for normative content.

## Page requirements

- Give each published Markdown page YAML front matter with `layout`, `title`,
  `nav_order`, and a stable `permalink`.
- Use `parent` and `has_children` to maintain the Just the Docs navigation
  hierarchy. A child's `parent` must exactly match its parent's `title`.
- Use repository-relative `.md` links between documentation pages. Do not add
  extensionless GitHub-wiki links.
- Keep JSON and YAML fenced examples syntactically parseable.
- Use fenced `mermaid` blocks for diagrams that Mermaid should render.
- Do not edit or commit generated `_site/` output.

## Validation

From the repository root, run:

```sh
ruby scripts/validate-docs.rb
BUNDLE_GEMFILE=docs/Gemfile bundle exec jekyll build --source docs --destination _site/iri-facility-api-docs
BUNDLE_GEMFILE=docs/Gemfile bundle exec htmlproofer _site --disable-external
```

GitHub Pages is configured separately to publish the `docs/` directory from
the `main` branch.
