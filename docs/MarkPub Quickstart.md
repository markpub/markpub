# MarkPub Quickstart

## Assumptions and pre-requisites:

These instructions assume the following:
- The primary goal is to build a website from a collection of Markdown files.
- The Markdown documents are in a GitHub repository.
- Web publishing is hosted by Netlify or GitHub pages.

### Prerequisites for deployment:  
- Python3 (Version 3.9 or higher) installed.  
- Facility with using a command-line terminal app.  

- Know how to deploy on Netlify from GitHub, or   
- Know how to deploy GitHub Pages, or  
- Know how to get assistance with such deployments.  

## Basic installation and use  

First, install MarkPub.  
```shell
pip install markpub
```

Assuming the local folder, and GitHub repository, name of the Markdown collection is “myDocumentCollection” these commands will initialize and deploy those documents to a Netlify hosted website.

**Initialize the document collection**:  

```shell
# Initialize the site
markpub init /full/path/to/myDocumentCollection
```

Initialization will prompt for:  

- Website title: "My Document Collection”
- Author: “Your name or names”
- Git repo: github.com/YourGitHubAccountName/myDocumentCollection

**Deploy to Netlify**:  
REQUIREMENTS: GitHub account, and 
**TODO**: Netlify specific wording of CI/CD connection  

```shell
cd /full/path/to/myDocumentCollection
git commit -am "MarkPub installation updates"
git push
```

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

### Configuration
Edit `.markpub/markpub.yaml` to change:
- Site title
- Author
- License
- Number of recent changes shown
- Other site-wide settings

