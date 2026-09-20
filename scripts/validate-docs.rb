#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "pathname"
require "psych"
require "uri"

ROOT = Pathname.new(__dir__).parent.expand_path
DOCS = ROOT.join("docs")

EXPECTED_PAGES = %w[
  agentic-discovery.md
  api-url-structure.md
  architecture.md
  contributing.md
  core-concepts.md
  examples.md
  getting-started.md
  hypermedia-and-discovery.md
  implementation-guide.md
  index.md
  iri-2.0.md
  object-model-reference.md
  registry.md
  resource-architecture-overview.md
  resource-model.md
  rfc-process.md
  semantic-registry-architecture.md
  service-desc.md
].freeze

OBSOLETE_PATHS = %w[
  wiki
  scripts/check-wiki-drift.sh
  scripts/sync-wiki.sh
].freeze

EXPECTED_MERMAID_BLOCKS = 7

errors = []
documents = {}

def relative(path)
  path.relative_path_from(ROOT).to_s
end

def parse_front_matter(path, errors)
  text = path.read
  match = text.match(/\A---\s*\n(.*?)^---\s*$\n?/m)
  unless match
    errors << "#{relative(path)}: missing YAML front matter"
    return [{}, text]
  end

  begin
    data = Psych.safe_load(match[1], aliases: true) || {}
  rescue Psych::SyntaxError => e
    errors << "#{relative(path)}: invalid front matter: #{e.message.lines.first.strip}"
    data = {}
  end

  unless data.is_a?(Hash)
    errors << "#{relative(path)}: front matter must be a mapping"
    data = {}
  end

  [data, text]
end

def local_link_target(raw_target)
  target = raw_target.strip
  target = target[1...target.index(">")].to_s if target.start_with?("<") && target.include?(">")
  target = target.split(/\s+/, 2).first.to_s
  return nil if target.empty? || target.start_with?("#", "//")
  return nil if target.match?(/\A[a-z][a-z0-9+.-]*:/i)

  target.split(/[?#]/, 2).first
end

def validate_links(path, text, errors)
  in_fence = false
  fence_marker = nil

  text.each_line.with_index(1) do |line, line_number|
    if (fence = line.match(/^\s*(```+|~~~+)/))
      marker = fence[1][0, 3]
      if in_fence && marker == fence_marker
        in_fence = false
        fence_marker = nil
      elsif !in_fence
        in_fence = true
        fence_marker = marker
      end
      next
    end
    next if in_fence

    line.scan(/!?\[[^\]]*\]\(([^)]+)\)/) do |match|
      raw_target = match.first
      target = local_link_target(raw_target)
      next unless target

      begin
        target = URI::DEFAULT_PARSER.unescape(target)
      rescue ArgumentError
        errors << "#{relative(path)}:#{line_number}: malformed link target #{raw_target.inspect}"
        next
      end

      if target.start_with?("/")
        errors << "#{relative(path)}:#{line_number}: use a repository-relative link instead of #{target.inspect}"
        next
      end

      destination = path.dirname.join(target).cleanpath
      if File.extname(target).empty? && !target.end_with?("/")
        errors << "#{relative(path)}:#{line_number}: extensionless local link #{target.inspect}"
      elsif target.end_with?("/")
        errors << "#{relative(path)}:#{line_number}: missing local link target #{target.inspect}" unless destination.join("index.md").file?
      elsif !destination.file?
        errors << "#{relative(path)}:#{line_number}: missing local link target #{target.inspect}"
      end
    end
  end
end

unless DOCS.directory?
  warn "docs/: directory not found"
  exit 1
end

expected_paths = EXPECTED_PAGES.map { |name| DOCS.join(name) }
expected_paths.each do |path|
  errors << "#{relative(path)}: expected migrated page is missing" unless path.file?
end

ignored_doc_roots = %w[.bundle .jekyll-cache .sass-cache _site vendor].freeze
published_pages = DOCS.glob("**/*.md").reject do |path|
  docs_relative = path.relative_path_from(DOCS)
  ignored_doc_roots.include?(docs_relative.each_filename.first) ||
    %w[AGENTS.md 404.md].include?(path.basename.to_s)
end
unexpected_pages = published_pages - expected_paths
unexpected_pages.each do |path|
  errors << "#{relative(path)}: unexpected published Markdown page"
end

mermaid_count = 0
json_count = 0
yaml_count = 0

expected_paths.select(&:file?).each do |path|
  front_matter, text = parse_front_matter(path, errors)
  documents[path] = front_matter

  %w[layout title nav_order permalink].each do |key|
    value = front_matter[key]
    errors << "#{relative(path)}: front matter #{key.inspect} is required" if value.nil? || value.to_s.empty?
  end
  errors << "#{relative(path)}: layout must be 'default'" unless front_matter["layout"] == "default"
  errors << "#{relative(path)}: nav_order must be an integer" unless front_matter["nav_order"].is_a?(Integer)

  permalink = front_matter["permalink"].to_s
  unless permalink.start_with?("/") && permalink.end_with?("/")
    errors << "#{relative(path)}: permalink must start and end with '/'"
  end

  errors << "#{relative(path)}: contains retired wiki terminology" if text.match?(/\bwiki\b/i)
  errors << "#{relative(path)}: contains retired GitHub wiki-link syntax" if text.match?(/\[\[[^\]]+\]\]/)
  validate_links(path, text, errors)

  text.scan(/^```([A-Za-z0-9_-]+)[^\n]*\n(.*?)^```\s*$/m) do |language, body|
    case language.downcase
    when "json"
      json_count += 1
      begin
        JSON.parse(body)
      rescue JSON::ParserError => e
        errors << "#{relative(path)}: invalid JSON fence ##{json_count}: #{e.message}"
      end
    when "yaml", "yml"
      yaml_count += 1
      begin
        Psych.parse_stream(body)
      rescue Psych::SyntaxError => e
        errors << "#{relative(path)}: invalid YAML fence ##{yaml_count}: #{e.message.lines.first.strip}"
      end
    when "mermaid"
      mermaid_count += 1
    end
  end
end

titles = {}
permalinks = {}
documents.each do |path, data|
  title = data["title"]
  permalink = data["permalink"]
  if title && titles.key?(title)
    errors << "#{relative(path)}: duplicate title #{title.inspect} (also in #{relative(titles[title])})"
  elsif title
    titles[title] = path
  end
  if permalink && permalinks.key?(permalink)
    errors << "#{relative(path)}: duplicate permalink #{permalink.inspect} (also in #{relative(permalinks[permalink])})"
  elsif permalink
    permalinks[permalink] = path
  end
end

sibling_orders = Hash.new { |hash, key| hash[key] = {} }
documents.each do |path, data|
  parent = data["parent"]
  if parent
    parent_path = titles[parent]
    if parent_path.nil?
      errors << "#{relative(path)}: parent #{parent.inspect} does not match a page title"
    elsif documents[parent_path]["has_children"] != true
      errors << "#{relative(parent_path)}: parent page must set has_children: true"
    end
  end

  order = data["nav_order"]
  next unless order.is_a?(Integer)

  if sibling_orders[parent].key?(order)
    other = sibling_orders[parent][order]
    errors << "#{relative(path)}: duplicate nav_order #{order} under #{parent || 'root'} (also in #{relative(other)})"
  else
    sibling_orders[parent][order] = path
  end
end

documents.each do |path, data|
  next unless data["has_children"] == true
  next if documents.any? { |_child_path, child_data| child_data["parent"] == data["title"] }

  errors << "#{relative(path)}: has_children is true but no children reference this page"
end

config_path = DOCS.join("_config.yml")
if config_path.file?
  begin
    config = Psych.safe_load(config_path.read, aliases: true) || {}
    errors << "docs/_config.yml: unexpected baseurl" unless config["baseurl"] == "/iri-facility-api-docs"
    errors << "docs/_config.yml: remote theme must be pinned" unless config["remote_theme"] == "just-the-docs/just-the-docs@v0.12.0"
  rescue Psych::SyntaxError => e
    errors << "docs/_config.yml: invalid YAML: #{e.message.lines.first.strip}"
  end
else
  errors << "docs/_config.yml: missing Jekyll configuration"
end

errors << "expected #{EXPECTED_MERMAID_BLOCKS} Mermaid fences, found #{mermaid_count}" unless mermaid_count == EXPECTED_MERMAID_BLOCKS

OBSOLETE_PATHS.each do |obsolete|
  errors << "#{obsolete}: obsolete wiki-mirroring path must be removed" if ROOT.join(obsolete).exist?
end

if errors.empty?
  puts "Documentation validation passed: #{documents.length} pages, #{json_count} JSON fences, #{yaml_count} YAML fences, #{mermaid_count} Mermaid fences."
else
  warn "Documentation validation failed with #{errors.length} error(s):"
  errors.each { |error| warn "- #{error}" }
  exit 1
end
