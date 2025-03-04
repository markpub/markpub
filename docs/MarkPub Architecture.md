# MarkPub Architecture

## Overview

MarkPub is a static site generator that transforms Markdown files into HTML websites with wiki-like features. It uses a custom Mistletoe renderer to handle wiki-style syntax, maintains a backlink system to track relationships between pages, and provides full-text search capabilities.

This file was generated automatically by Claude 3.7 Sonnet on 2025-02-25, based on MarkPub `fbf733b07f1a2ddef61563457cb524058bc63464` of 2024-02-25. It is believed to be useful, but it has been not been comprehensively reviewed by humans yet.

## Core Components

MarkPub's architecture consists of these components:

### 1. Command-Line Interface

The CLI provides two main commands:
- `init`: Sets up a new MarkPub site with necessary configuration and template files
- `build`: Converts Markdown files to HTML and generates a complete website

The CLI is implemented in `markpub.py`, using Python's `argparse` module to handle command-line arguments.

### 2. Site Configuration

Configuration is managed through a YAML file (`.markpub/markpub.yaml`), which controls:
- Website metadata (title, author, license)
- Git integration settings
- Theme selection
- Navigation and sidebar configuration
- Directory exclusion rules

### 3. Markdown Processing

#### Custom Mistletoe Renderer

MarkPub extends the Mistletoe Markdown parser with a custom renderer (`MassiveWikiRenderer`) that adds:
- Wiki-style links (`[[Page Name]]`)
- Transclusion (`![[Page Name]]`)
- Image embedding (`![[image.png]]`)
- Raw HTML support (`{< html >}`)
- Link modification based on site structure (WLA note: what does this refer to, or mean?)

#### Front Matter Parser

The system extracts and processes YAML front matter from Markdown files to:
- Add metadata to pages
- Control page-specific features
- Support custom fields like publication dates or categories

### 4. Templating System

MarkPub uses Jinja2 for HTML templates with these key files:
- `page.html`: Main template for content pages
- `all-pages.html`: Site index listing all pages
- `recent-pages.html`: Shows recent changes
- `search.html`: Search interface
- Reusable partials like `_header.html` and `_footer.html`

Templates have access to:
- Page content
- Front matter metadata
- Configuration values
- Navigation elements
- Backlinks data

### 5. Link Management

A link management system:
- Maintains a `wiki_pagelinks` dictionary to track relationships between files
- Converts wiki-style links to proper HTML hyperlinks
- Builds a backlinks graph to show what pages link to the current page
- Handles file path and URL normalization

### 6. Search Functionality

When enabled with `--lunr`:
- Extracts content from all pages
- Uses Node.js to build a Lunr.js search index
- Generates client-side search functionality
- Outputs index files for browser-based search

### 7. Git Integration

When enabled with `--commits`:
- Extracts Git commit information for pages
- Shows modification dates and authors
- Displays commit messages
- Enables chronological sorting of pages

### 8. Static Asset Management

- Copies theme files and static assets to output directory
- Maintains directory structure
- Handles special files like README.md → index.html conversion

## Data Flow (WLA note: this is a nice DFD, and also not accurate; does it matter?)

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│ Input Directory │────▶│ Markdown Parser  │────▶│ HTML Generation   │
│ (Markdown)      │     │ + Front Matter   │     │ + Template Apply  │
└─────────────────┘     └──────────────────┘     └───────────────────┘
                               │  ▲                       │
                               ▼  │                       ▼
                        ┌──────────────────┐     ┌───────────────────┐
                        │ Wiki Links &     │     │ Output Directory  │
                        │ Backlinks System │     │ (Static Website)  │
                        └──────────────────┘     └───────────────────┘
```

## Dependencies

MarkPub relies on these dependencies:
- `mistletoe`: Markdown parsing
- `Jinja2`: HTML templating
- `PyYAML`: Configuration handling
- `python-dateutil`: Date handling
- `Git`: Commit information (optional)
- `Node.js`/`lunr.js`: Search indexing (optional)

## Performance Considerations

- Files are processed in multiple passes to build the link graph before rendering
- Search indexing can be resource-intensive for large sites
- Git operations add overhead when tracking history
- Templating is optimized to reuse common elements

## Security Model

- YAML loading uses `safe_load` to prevent code execution
- Path handling prevents directory traversal
- HTML is sanitized by the templating system
- Subprocess calls are carefully restricted

## Extensibility

The architecture allows for:
- Custom themes through the template system
- Extended Markdown syntax via renderer customization
- Additional metadata through front matter
- Integration with external services through extension points (WlA note: what does this refer to?)
