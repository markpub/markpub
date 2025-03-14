# MarkPub Basic Install

## Prerequisites for installation:  
- Python3 Version 3.12 (or higher) installed.  
- Facility and comfort with using a command-line or Terminal app.  

## Install `markpub` and build a website from a directory of Markdown files  
These steps assume the name of the directory or folder is “myDocumentCollection”.  

**Install `markpub`**:  
```shell
cd  # to home directory
pip install markpub
```

**Initialize the document collection**:
This step sets up the `markpub` configuration file and copies the HTML, CSS, and JS files needed to build a website.  
```shell
cd
markpub init /full/path/to/myDocumentCollection
```

MarkPub initialization issues terminal prompts for:  

- Website title: "My Document Collection"
- Author: "Your name or names"  

The terminal prompt for “Git repo:” can be ignored (just hit RETURN)  

**Build a website of the collection**:  

```shell
cd /full/path/to/myDocumentCollection/.markpub
markpub build -i .. -o ./output
```  

When the build completes, the web-site can be viewed using the following commands:  
```shell
cd ./output
python -m http.server
```  

Open a browser tab and enter 'localhost:8000' to view the home page for the document collection.  

