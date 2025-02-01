# MarkPub User Guide

This guide walks through three common use cases for MarkPub:
1. A simple personal website
2. A blog-style website
3. A small wiki

For each use case, setup, content organization, and special considerations are described.

## Prerequisites for all use cases

First, install MarkPub. Using a virtual environment is recommended:

```bash
# Create and enter project directory
mkdir my-website
cd my-website

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install MarkPub
pip install --upgrade pip
pip install markpub
```

## Use Case 1: Simple Personal Website

This example creates a basic personal website with a home page with a Sidebar.

### Setup
TODO: clarify the working directory for these commands

```bash
# Initialize the site
markpub init personal-site
cd personal-site
```

When prompted:
- Website title: "Jane Smith - Personal Website"
- Author: "Jane Smith"
- Git repo: (optional, leave blank for now)

### Content Structure

```
personal-site/
├── README.md              # Home page
└── Sidebar.md          # Navigation
```

### Example Content
TODO: update this to reflect what MarkPub produces

`README.md` (Home Page):
```markdown
# Welcome to My Personal Site

I'm Jane Smith, a software developer based in Portland. This site showcases my work and thoughts on technology.

## Recent Projects
- [[projects/project1|Building a Chat Bot]]
- [[projects/project2|Machine Learning Explorer]]

[[about|Learn more about me]] or [[contact|get in touch]].
```

`Sidebar.md`:
```markdown
### Navigation

{< div class="navlinks" >}
- [[README|Home]]
- [[about|About Me]]
- [[contact|Contact]]
- [Projects](/projects/)
{< /div >}
```

### Deploy to Netlify
REQUIREMENTS: Netlify account, GitHub account

1. Create a GitHub repository for your site and push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/personal-site.git
git push -u origin main
```

2. Go to [Netlify](https://netlify.com) and sign in with your GitHub account
TODO: these instructions assume a specific Netlify setup. Do they belong in this document?

3. Click "Add new site" > "Import an existing project"

4. Select your GitHub repository

5. Netlify will automatically detect MarkPub's configuration in `netlify.toml`. The defaults will work, but you can review them:
- Build command: `markpub build -i .. -o ./output --lunr --commits`
- Publish directory: `output`
- Base directory: `.markpub`

6. Click "Deploy site"

Netlify will automatically build and deploy your site whenever changes are pushed to GitHub.

QUESTION: do we care about documenting these use cases?

## Use Case 2: Blog-Style Website

This example creates a blog with posts organized by date and category.

### Setup

```bash
markpub init tech-blog
cd tech-blog
```

When prompted:
- Website title: "Tech Musings"
- Author: "John Developer"
- Git repo: (add your GitHub repo if you want the Edit button)

### Content Structure

```
tech-blog/
├── README.md                    # Home/latest posts
├── posts/                       # Blog posts by date
│   ├── 2024/
│   │   ├── 01-19-docker.md
│   │   └── 01-15-python.md
│   └── 2023/
│       └── 12-31-year-review.md
├── categories/                  # Category index pages
│   ├── docker.md
│   ├── python.md
│   └── reviews.md
└── Sidebar.md                  # Navigation + categories
```

### Example Content

Post template (`posts/2024/01-19-docker.md`):
```markdown
---
title: "Getting Started with Docker"
date: 2024-01-19
categories: [docker, tutorials]
---

# Getting Started with Docker

Docker makes containerization accessible to everyone. In this post...
```

Category page (`categories/docker.md`):
```markdown
# Docker Posts

A collection of all posts about Docker:

- [[posts/2024/01-19-docker|Getting Started with Docker]]
- (more posts will be listed here)
```

`Sidebar.md`:
```markdown
### Navigation

{< div class="navlinks" >}
- [[README|Home]]
- [RECENT POSTS](/recent-pages.html)
- [ALL POSTS](/all-pages.html)
{< /div >}

### Categories
{< div class="navlinks" >}
- [[categories/docker|Docker]]
- [[categories/python|Python]]
- [[categories/reviews|Reviews]]
{< /div >}
```

### Deploy to Netlify

Follow the same Netlify deployment steps as in Use Case 1, but when reviewing the build settings, note that the `netlify.toml` configuration will automatically include the `--commits` and `--lunr` flags for the blog features.

## Use Case 3: Small Wiki

This example creates a collaborative knowledge base about gardening.

### Setup

```bash
markpub init garden-wiki
cd garden-wiki
```

When prompted:
- Website title: "Community Garden Wiki"
- Author: "Garden Collective"
- Git repo: (add your GitHub repo for collaborative editing)

### Content Structure

```
garden-wiki/
├── README.md                     # Wiki home/overview
├── plants/                       # Plant information
│   ├── vegetables/
│   │   ├── tomatoes.md
│   │   └── peppers.md
│   └── herbs/
│       ├── basil.md
│       └── mint.md
├── techniques/                   # Gardening techniques
│   ├── composting.md
│   └── companion-planting.md
├── seasons/                      # Seasonal guides
│   ├── spring.md
│   └── summer.md
└── Sidebar.md                   # Navigation
```

### Example Content

Plant page (`plants/vegetables/tomatoes.md`):
```markdown
# Growing Tomatoes

Tomatoes are a beloved garden vegetable that...

## Quick Facts
- Season: [[seasons/summer|Summer]]
- Companion Plants: [[plants/herbs/basil|Basil]]
- Technique: [[techniques/companion-planting|Companion Planting]]

## Growing Guide
1. Start seeds indoors...
```

Technique page (`techniques/companion-planting.md`):
```markdown
# Companion Planting

Companion planting is the practice of growing plants together...

## Common Combinations
- [[plants/vegetables/tomatoes|Tomatoes]] + [[plants/herbs/basil|Basil]]
- (more combinations...)

![[plants/vegetables/tomatoes]] 
```

`Sidebar.md`:
```markdown
### Navigation

{< div class="navlinks" >}
- [[README|Home]]
- [SEARCH](/search.html)
- [ALL PAGES](/all-pages.html)
- [RECENT CHANGES](/recent-pages.html)
{< /div >}

### Categories
{< div class="navlinks" >}
- [[plants/vegetables/|Vegetables]]
- [[plants/herbs/|Herbs]]
- [[techniques/|Techniques]]
- [[seasons/|Seasonal Guides]]
{< /div >}
```

### Deploy to Netlify

The wiki use case follows the same Netlify deployment steps. The included `netlify.toml` configuration automatically:
- Installs all required dependencies
- Builds with full search functionality
- Enables Git commit tracking for the Recent Changes page
- Deploys to a public URL

After connecting to Netlify, you'll have a collaborative wiki where:
- Changes are deployed automatically when pushed to GitHub
- Multiple contributors can edit via GitHub
- Search works out of the box
- Recent changes are tracked automatically

## Local Development

While Netlify handles production deployment, you can preview changes locally:

```bash
cd .markpub
markpub build -i .. -o output --lunr --commits
python -m http.server
```

Visit http://localhost:8000 to preview your site before pushing changes.

## Common Customizations

For all use cases, you can customize:

### Theme Colors
Edit `.markpub/this-website-themes/dolce/static/markpub-static/css/custom.css`:

```css
/* Example: Change header color */
#header {
    background: #3298dc;  /* Your preferred color */
}

/* Example: Change link colors */
#side-column .navlinks a {
    background-color: #d6eaf8;  /* Your preferred color */
}
```

### Page Layout
Edit templates in `.markpub/this-website-themes/dolce/`:
- `_header.html`: Page header
- `_footer.html`: Page footer
- `page.html`: Main content template

### Configuration
Edit `.markpub/markpub.yaml` to change:
- Site title
- Author
- License
- Number of recent changes shown
- Other site-wide settings

## Best Practices

1. **Use Clear File Names**
   - Use lowercase
   - Replace spaces with hyphens
   - Include dates for blog posts

2. **Organize Content**
   - Group related content in directories
   - Use consistent category names
   - Keep URLs human-readable

3. **Link Generously**
   - Cross-reference related content
   - Use descriptive link text
   - Create category index pages

4. **Maintain Navigation**
   - Keep sidebar current
   - Organize by importance
   - Include search for larger sites

Remember that MarkPub is flexible - these examples can be mixed and matched to create the exact site structure you need.
