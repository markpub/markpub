# markpub  

![PyPI version](https://img.shields.io/pypi/v/markpub)  

MarkPub builds a static HTML website from a directory of Markdown files.  
The website supports wiki-links, transclusion, and provides full-text
search.  

MarkPub installs configuration files that GitHub Pages and Netlify can use to automatically publish the HTML files on the web.

## Requirements

- Python 3.12 or higher.

## Install

### Using pip
``` shell
pip install markpub
```

## Usage

### Overview

```shell
markpub [--version] <command> [options]
```

Available commands:
- `init` - Initialize a new MarkPub site
- `build` - Build HTML website from Markdown files

### Commands

#### `markpub init <directory>`

Initialize a new MarkPub site in the specified directory. This creates:
- `.markpub/markpub.yaml` - Site configuration file
- Configuration files for GitHub Pages/Netlify deployment
- `Sidebar.md` - Website navigation links displayed sidebar on webpages

**Example:**
```shell
markpub init my-wiki
```

#### `markpub build [options]`

Build a static website from Markdown files.

**Required options:**
- `-i, --input <directory>` - Input directory containing Markdown files
- `-o, --output <directory>` - Output directory for generated HTML files

**Optional options:**
- `--config, -c <file>` - Path to YAML config file (default: `./markpub.yaml`)
- `--root, -r <name>` - Website root directory name (needed for GitHub Pages hosting)
- `--lunr` - Create lunr search index (requires npm and lunr to be installed)
- `--commits` - Include Git commit messages and times in All Pages

**Examples:**
```shell
# Basic build
markpub build -i my-wiki -o my-wiki-site

# Build with search
markpub build -i my-wiki -o my-wiki-site --lunr

# Build for GitHub Pages with Git history
markpub build -i my-wiki -o my-wiki-site --root my-repo --commits
```

### Getting Help

Use `--help` with any command for detailed usage information:

```shell
markpub --help
markpub init --help
markpub build --help
```

### Markpub website themes

Markpub website themes are managed by the Python package [markpub-themes](https://pypi.org/project/markpub-themes/)  
Management and use of themes is documented there. This package is installed with `markpub`, and after installation, help information is available:  

```shell
markpub-themes -h
```

## Documentation  

- [Basic install instructions](https://markpub.org/documentation/markpub_basic_install)  
- [Install and Web-publish instructions](https://markpub.org/documentation/markpub_install_and_web-publish_steps)  

- Further documentation is under development.  



