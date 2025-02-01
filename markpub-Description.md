# markpub Description

**markpub** is a static site generator for turning collections of Markdown documents into static HTML websites.  

**markpub** supports wiki links and back links, transclusion, full-text search, as well as standard Markdown features. There is no required organization of the markdown files in the document collection directory or subdirectories.

Using **markpub** to initialize a document collection installs a website theme that can be altered or replaced.

For document collections that are versioned with Git, the generated website can display a table of all pages in the collection that can be sorted by file name or time of most recent change.

/ basic use case is web publish a collection of Markdown files //
/ assumption: documents are in a Git repository //
/ assumption: web publishing is hosted by Netlify or GitHub pages //
/ prerequisites for deployment: know how to deploy on Netlify from GitHub, or how to deploy GitHub Pages, or know how to get assistance with these deployments //

/ two deployment use cases: (1) add MarkPub to the repository to support automated CI/CD; (2) install MarkPub to support local deployment as well as repository CI/CD //  

/ Quickstart: document prerequisites and one or two ways to deploy a MarkPub website //
/ information on how to exclude directories and support BlueSky comments in a separate document //
/ put all other detail information about directory structures and theme management in another document //



## Typical Installation Directory Structure

Once installed there is a `.markpub` subdirectory of the document collection directory that contains a configuration file, the Python and Javascript files, and the website theme files and directories.

**markpub** ignores dotfiles and dot-directories, so as it builds, it ignores anything inside (for instance) `.obsidian` or `.markpub` directories. An initialized directory has the following structure:  

```
. # root directory of the document collection
├── .markpub  # MARKPUB workspace
│   ├── markpub.yaml # configuration file for the website
│   ├── build-index.js # full-text search Javascript code
│   ├── package-lock.json # node package info
│   ├── package.json # node package info
│   ├── requirements.txt # Python package dependencies
│   └── this-website-themes
│       └── dolce # the default theme; may be customized
├── Sidebar.md # default webpage sidebar
├── .gitignore # files and directories ignored by Git
└── netlify.toml # website build instructions for netlify service
```

## Theme Files

The default theme for MARKPUB websites is called “Dolce”. MARKPUB uses the Python package templating engine  [Jinja](https://pypi.org/project/Jinja2/ ). The directory `this-website-themes` has the following structure and content.

```shell
this-website-themes
└── dolce
    ├── LICENSE
    ├── README.md
    ├── _footer.html
    ├── _header.html
    ├── _javascript.html
    ├── all-pages.html
    ├── page.html
    ├── recent-pages.html
    ├── search.html
    └── static
        └── markpub-static
            ├── css
            │   ├── custom.css
            │   └── style.css
            └── js
                └── script.js
```

## Install

You can install `markpub` globally or in a virtual environment.

Global install:

```shell
pip3 install markpub
```

Virtual environment creation and installation:

```shell
mkdir my-new-website
cd my-new-website
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install markpub
markpub init .
```

## Running markpub

`markpub` provides two operations:

1. initialization of a new empty directory or a directory containing Markdown files; and
2. building a static website from an initialized directory

You can get help with `markpub` with the `-h` or `--help` flag:

```shell
markpub -h
```

### Initialization

```shell
markpub init directory-name
```

If `./directory-name` does not exist, it is created and populated with the MARKPUB default software. If there is a directory of that name in the current directory, then the MARKPUB files are installed there.

Initialization requests website information on the Terminal command line; viz.:
```shell
Enter the website title: # the title at the top of every webpage
Enter the author name(s): # name(s) shown in page footer; optional
Enter Git repository url (for Edit page button; optional): # e.g., github.com/band/directory-name
```

### Build

In `.markpub/`:

```shell
markpub build -i .. -o output --lunr --commits
```
This command builds html pages for all Markdown pages rooted in the parent directory, and writes them to the `./output` directory. A Lunr search index is created, and information from the latest commit of each file is used to populate “All Pages” and “Recent Pages” web pages.


Note that MARKPUB removes (if necessary) and recreates the `output` directory each time `markpub build` is run.

If you want to print a log what is happening during the build, set the `LOGLEVEL` environment variable to `DEBUG`.

On the command line, do:

```shell
LOGLEVEL=DEBUG markpub build -i .. -o output --lunr --commits
```

or:

```shell
export LOGLEVEL=DEBUG
markpub build -i .. -o output --lunr --commits
```

In `netlify.toml`, do:

```toml
[build.environment]
  LOGLEVEL = "DEBUG"
```

## Git Commits

To output authors, commit messages, and timestamps for each page in the All Pages page, include the `--commits` flag:

```shell
markpub build -i .. -o output --commits
```

In the `all-pages.html` template (template may have a different file name), the following variables are available when `--commits` is active:

- `page.author` - the author name of the most recent commit for this page
- `page.change` - the commit message for the most recent commit for this page
- `page.date` - the timestamp for the most recent commit for this page

If `--commits` is not active, each of those variables is set to empty string `''`.

## Lunr

To build an index for the [Lunr](https://lunrjs.com/) search engine, include the `--lunr` flag:

```shell
markpub build -i .. -o output --lunr
```

Lunr is a JavaScript library, so Node.js (`node`) and the Lunr library must be installed.

To install Node, see <https://nodejs.org/en/download/>. On Mac, you may want to do `brew install node`.

To install Lunr, in `.markpub` do:

```shell
npm ci # reads package.json and package-lock.json
```

When MARKPUB runs, the Lunr indexes are generated at the root of the output directory, named like this (numbers change every microsecond): `lunr-index-1656193058.85086.js` (the reverse index) and `lunr-posts-1656193058.85086.js` (relates filepaths used by Lunr as keys, to human-readable page names).

Two template variables, `lunr_index_sitepath` and  `lunr_posts_sitepath`, containing the website paths to the generated index JavaScript files, are passed to templates as the pages are built.

In templates, loading the indexes is done like this:

```
{% if lunr_index_sitepath != '' %}
<script src="{{lunr_index_sitepath}}"></script>
{% endif %}
{% if lunr_posts_sitepath != '' %}
<script src="{{lunr_posts_sitepath}}"></script>
{% endif %}
```

which results in this on the generated webpage:

```html
<script src="/lunr-index-1656193058.85086.js"></script>
<script src="/lunr-posts-1656193058.85086.js"></script>
```

Add the rest of the code to the `<script>` sections of your pages to enable Lunr:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.9/lunr.min.js"></script>
<script>var index = lunr.Index.load(lunr_index)</script>
// ...
const searchResultList = index.search(searchString).map((item) => {
              return lunr_posts.find((post) => item.ref === post.link)
          })
// ...
```



## Deploy (Netlify)

For Netlify deploys, you can include a `netlify.toml` file like this at the root of your repo:

```toml
[build]
  ignore = "/bin/false"
  base = ".markpub"
  publish = "output"
  command = "markpub build -i ../.. -o ../output --lunr --commits
[build.environment]
  PYTHON_VERSION = "3.8"
```

It is recommended that you make a copy of `massive-wiki-themes` called `this-wiki-themes` at the same directory level, then customize your themes inside of `this-wiki-themes`.

The build command would then be (substitute your theme name instead of `alto` as necessary:

```shell
markpub build -i ../.. -o ../output -t ../this-wiki-themes/alto
```

 

## Develop

Because static assets have an absolute path, you may want to start a local web server while you're developing and testing.  Change to the output directory and run this command:

```
python3 -m http.server
```

## Themes

MARKPUB uses a simple theming system.  All the files for one theme are placed in a subdirectory in the themes directory, the default location is `document-collection/.markpub/this-website-themes`. The default installed them is in `this-website-themes/dolce`.  Other themes can be added to this directory and used in the build command by passing the `--themes` argument. For example, to use a theme installed in `this-website-themes/alto`, the build command is:
```shell
(venv)$ markpub build -i .. -o output -t this-website-themes/alto --lunr --commits
```

MARKPUB builds the pages with the Jinja2 templating enging, so you can use Jinja2 directives within the HTML files to include document metadata and markdown content.  You can also use the Jinja2 `include` functionality to extract reused parts of the page to HTML "partial" files.

A collection of themes are in a separate repo, [github/peterkaminski/massive-wiki-themes](https://github.com/peterkaminski/massive-wiki-themes). For Massive Wiki Builder v2.2.0, you should use Massive Wiki Themes version 2023-02-09-001 or later. TODO: update this


## Static Files

After the HTML pages are built from the Markdown files, if a directory named `static` exists at the top level of the theme, all the files and directories within it are copied to the root of the output directory.  By convention, static files such as CSS, JavaScript, and images are put in a directory inside `static` called `markpub-static`. Favicon files and other files that should be at the root of the website are put at the root of `static`.

The name `static` is used in the theme because it is descriptive, and will not collide with anything in the wiki. (The _content_ of `static` is copied, but not `static` itself.)

The `markpub-static` directory contains static files used by the website. It is named `markpub-static` to be less likely to collide with a website directory with the same name. (`markpub-static` itself _is_ copied to the output directory, where all the published website files and directories live.)

In the theme:

```
dolce
├── LICENSE
├── README.md
├── _footer.html
├── _header.html
├── _javascript.html
├── all-pages.html
├── page.html
├── recent-pages.html
├── search.html
└── static
    └── markpub-static
        ├── css
        │   ├── custom.css
        │   └── style.css
        └── js
            └── script.js
```


Results in the output website:
```
output
├── 
├── markpub-static
│   ├── css
│   │   ├── custom.css
│   │   └── style.css
│   └── js
│       └── script.js
├──
├── 
└── 
```

Side note about favicon files; it is suggested to use a favicon generator such as [RealFaviconGenerator](https://realfavicongenerator.net/) to create the various icon files needed for different platforms. This note is meant for informational purposes, and does not represent an endorsement of RealFaviconGenerator in particular.
