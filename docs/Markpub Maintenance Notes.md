# Markpub Maintenance Notes

Notes and suggested work practices for maintaining MarkPub software,
Python Packaging, and software testing.  

## Python Packaging

### Current setup and practices:  

#### Install pipx
	- cf. <https://github.com/pypa/pipx>  

- on macOS systems:
```shell
brew install pipx
pipx ensurepath
```

#### Using `uv` for Python packaging maintenance: building, testing, and publishing.
  - cf. <https://docs.astral.sh/uv/>  

- Installing `uv`: recommended setup
  - use `pipx` to install `uv`
```shell
pipx install uv
```  
	
##### Package building:  
- synchronize `pyproject.toml` with current setup
  ```shell
  uv sync
  ```  
- to change the version number of this package:  
```shell
uv version --bump [major|minor|patch]
```  
- to build the current version of this package:  
```shell
  uv build
```  

- Package testing (prior to publishing):  
	- one recommended way to test the latest built version:  
	```shell
	cd /some/test/directory
	python3 -m venv venv  # install Python virtual environment
	source venv/bin/activate
	pip install --upgrade pip # always a good idea
	# in next command replace "1.1.0" with the version number being tested
	pip install	/full/path/to/markpub/dist/markpub-1.1.0-py3-none-any.whl 
	# test install
	markpub -V  # displays the version number being tested
	```  

  - from "/some/test/directory" test `markpub` "init", "build”, "theme-install" commands
	  E.g. (assume "/some/test/markdown/documents" is a collection of Markdown files):
	```shell
	# initialize a document collection
	markpub init /some/test/markdown/documents
	# provide a website and author name in response to Terminal
	prompts; enter CR for github prompt
	# build a website
	markpub build -i /some/test/markdown/documents -o ./output -c /some/test/markdown/documents/.markpub/markpub.yaml
	# to view the website
	cd output
	python -m http.server
	# and open a browser at <http://localhost:8000>
	```  

##### Package publishing:  
- bump package version; git commit “version bump”; re-build(?); then publish
- (TODO: document how to authenticate for publishing)

```shell
uv publish
```  



	  

