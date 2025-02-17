# MarkPub User Documentation

## Overview

MarkPub is a Python-based static site generator that converts collections of Markdown files into static HTML websites. It provides:

- Wiki-style, [[double bracket]] syntax,  linking between pages
- Automatic backlinks tracking
- Page transclusion
- Full-text search capability
- Git integration for tracking page changes
- Flexible theming system
- Support for YAML front matter

## Installation

There are two recommended ways to install MarkPub:

### Pre-requisites

- Python3 is installed
- You have a GitHub account
- You have a Netlify account

### Option 1: System-wide Installation

To install MarkPub globally on your system:

```shell
pip install markpub
```

### Option 2: Virtual Environment Installation (Recommended)

For isolated project-specific installations:

```bash
# Create project directory
mkdir my-document-collection
cd my-document-collection

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Update pip and install MarkPub
pip install --upgrade pip
pip install markpub
```

## Getting Started

### Initializing a New Site

After installation, initialize a new MarkPub site:
**TODO**: separate initialization of the current directory from initialization of a separate directory

```bash
markpub init my-document-collection
```

During initialization, you are prompted for:
- Website title
- Author name(s)
- Git repository URL (optional, for Edit button functionality)

This creates a directory structure:

```
my-document-collection/
├── .markpub/
│   ├── markpub.yaml           # Site configuration
│   ├── build-index.js         # Search functionality
│   ├── package.json           # Node.js dependencies
│   ├── package-lock.json      # Node.js dependency lock file
│   ├── requirements.txt       # Python dependencies
│   └── this-website-themes/   # Theme files
│       └── dolce/             # Default theme
├── Sidebar.md                 # Navigation sidebar content
├── .gitignore                # Git ignore patterns
└── netlify.toml              # Netlify deployment config
```

### Basic Configuration

The main configuration file is `.markpub/markpub.yaml`. Key settings include:

```yaml
wiki_title: "Your Wiki Title"
author: "Your name or names"
edit_url: "https://github.com/yourusername/yourrepo/edit/"
edit_branch: "main"
repo: '<a href="https://github.com/yourusername/yourrepo">github:yourrepo</a>'
license: '<a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>'
recent_changes_count: 5
sidebar: Sidebar.md
```

### Creating Content

1. Create Markdown files in your site directory
2. Use standard Markdown syntax
3. Add wiki-style links using `[[Page Name]]` syntax
4. Include YAML front matter if desired:
   ```yaml
   ---
   title: My Page
   date: 2024-01-19
   tags: [documentation, guide]
   ---
   ```

### Building the Site

Basic build command:
**TODO**: describe local build versus automated build

```bash
markpub build -i . -o output
```

Full build with all features:

```bash
markpub build -i . -o output --lunr --commits
```

Build options:
- `-i, --input`: Input directory containing Markdown files
- `-o, --output`: Output directory for generated HTML
- `--config`: Path to config file (default: ./markpub.yaml)
- `--templates`: Theme directory (default: ./this-website-themes/dolce)
- `--root`: Website root directory name
- `--lunr`: Enable full-text search
- `--commits`: Include Git commit information

### Search Functionality

To enable search:

1. Install Node.js dependencies:
```bash
cd .markpub
npm ci
```

2. Include the `--lunr` flag when building:
```bash
markpub build -i . -o output --lunr
```

### Git Integration

When using the `--commits` flag, MarkPub will:
- Track page modifications
- Show author information
- Display commit messages
- Include timestamps
- Enable sorting by last modified date

### Themes

MarkPub uses the "Dolce" theme by default. Theme files are in `.markpub/this-website-themes/dolce/`:

```
dolce/
├── _footer.html
├── _header.html
├── _javascript.html
├── all-pages.html
├── page.html
├── recent-pages.html
├── search.html
└── static/
    └── markpub-static/
        ├── css/
        │   ├── custom.css
        │   └── style.css
        └── js/
            └── script.js
```

To customize:
1. Copy the default theme directory
2. Modify the HTML templates and static assets
3. Use the `--templates` flag to specify your theme:
```bash
markpub build -i . -o output --templates /path/to/your/theme
```

### Deployment

#### Local Preview

Start a local server in your output directory:

```bash
cd output
python -m http.server
```

Visit `http://localhost:8000` in your browser.

#### Netlify Deployment

1. Include a `netlify.toml` in your root directory:
```toml
[build]
  ignore = "/bin/false"
  base = ".markpub"
  publish = "output"
  command = "markpub build -i .. -o ./output --lunr --commits"

[build.environment]
  PYTHON_VERSION = "3.8"
```

2. Connect your repository to Netlify
3. Configure build settings using the above configuration

## Advanced Features

### Wiki Links

- Basic link: `[[Page Name]]`
- Link with custom text: `[[Page Name|Display Text]]`
- Image embed: `![[image.png]]`
- Image with alt text: `![[image.png|Alt Text]]`
- Transclusion: `![[Note Name]]`

### Raw HTML

Use curly brackets and angle brackets for raw HTML:

```
{< div class="custom-class" >}
Content here
{< /div >}
```

### Debugging

Set the `LOGLEVEL` environment variable for detailed logging:

```bash
LOGLEVEL=DEBUG markpub build -i . -o output
```

## Troubleshooting

Common issues and solutions:

1. **Missing Lunr Index**
   - Ensure Node.js is installed
   - Run `npm ci` in the `.markpub` directory
   - Include `--lunr` flag when building

2. **Git Information Not Showing**
   - Verify the directory is a Git repository
   - Include `--commits` flag when building
   - Ensure files have been committed

3. **Theme Not Found**
   - Check theme path is correct
   - Verify theme directory structure
   - Ensure all required templates exist

## Best Practices

1. **Organization**
   - Keep related content in subdirectories
   - Use consistent naming conventions
   - Maintain a clear hierarchy

2. **Content**
   - Use descriptive file names
   - Include meaningful front matter
   - Add alt text to images
   - Write clear commit messages

3. **Development**
   - Test locally before deployment
   - Back up content regularly
   - Use version control
   - Customize CSS in `custom.css`

## Requirements

- Python 3.8 or higher
- Node.js (for search functionality)
- Git (for commit tracking)

## Resources

- [MarkPub GitHub Repository](https://github.com/MarkPub/markpub)
- [Bug Reports](https://github.com/MarkPub/markpub/issues)
- [License: MIT](LICENSE)

-----
## Extra documentation snippets



**Deploy to Netlify**:  
REQUIREMENTS: GitHub account, and 
**TODO**: Netlify specific wording of CI/CD connection  


Netlify deployment steps are governed by the included `netlify.toml`   
Netlify deployment:  
- Installs all required dependencies  
- Builds with full search functionality  
- Enables Git commit tracking for the Recent Changes page  
- Deploys to a public URL

After deployment with Netlify, there is a static website where:
- Changes are deployed automatically when pushed to GitHub
- Multiple contributors can edit via GitHub
- Fulltext search works out of the box
- Recent changes are tracked automatically

## Local Development

Netlify handles production web deployment.  
To preview changes locally:  

**Install node modules locally** - one-time only  
```shell
cd /full/path/to/myDocumentCollection/.markpub
npm ci
```

To deploy the current document collection locally:  
```shell
cd /full/path/to/myDocumentCollection/.markpub
markpub build -i .. -o output --lunr --commits
cd output && python -m http.server
```

Visit http://localhost:8000 to preview the website before pushing changes.

