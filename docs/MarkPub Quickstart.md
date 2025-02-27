# MarkPub Quickstart

## Assumptions and pre-requisites:

These instructions assume the following:
- The primary goal is to build a static website from a collection of Markdown files.
- The Markdown documents are in a GitHub repository.
- Web publishing is hosted by GitHub pages (or Netlify).

### Prerequisites for deployment:  
- Python3 (Version 3.9 or higher) installed.  
- Facility with using a command-line or Terminal app.  
- Know how to use a GitHub repository.
- Know how to deploy GitHub Pages, or  
- Know how to deploy on Netlify, or   
- Know how to get assistance with such deployments.  

## Basic installation and use  

Assuming the local folder name, and the GitHub repository name of the Markdown collection is "myDocumentCollection" these commands initialize and deploy those documents to a GitHub Pages hosted website.

**Install MarkPub**:
```shell
cd
pip install markpub
```

**Initialize the document collection**:
```shell
markpub init /full/path/to/myDocumentCollection
```

MarkPub initialization prompts for:  

- Website title: "My Document Collection"
- Author: "Your name or names"
- Git repo: github.com/YourGitHubAccountName/myDocumentCollection  

**Web-publish the collection as a GitHub Pages website**:  

```shell
cd /full/path/to/myDocumentCollection
git commit -am "MarkPub installation updates"
git push
```

Log into GitHub, and for this repository's "Pages" settings, set "Build and deployment" "Branch" to "gh-pages" in the drop-down menu, and select "Save".
 - Saving that setting triggers a "pages build and deployment" workflow under the "Actions" tab  
 - Select the repository's "Actions" tab;
 - when the "pages build and deployment" workflow is finished (shows a green checkmark) select that workflow;
 - from the "pages-build-deployment" graph select the green checkmark
          "deploy" link to see the deployed website.
 - when completed the website is available at:  
  <https://YourGitHubAccountName.github.io/myDocumentCollection>  
  
For Netlify deployment, MarkPub provides a `netlify.toml` configuration file automatically during initialization. You can use this to deploy your site on Netlify instead of GitHub Pages.
  
### Configuration  
Edit `.markpub/markpub.yaml` to change:
- Site title
- Author names
- License
- Number of recent changes shown
- Other site-wide settings
