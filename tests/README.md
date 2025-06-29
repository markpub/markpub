# Markpub Tests

test_markpub.py is a `pytest` script that is used to test the Python package Markpub  

The test script compares the known baseline files with the generated output files, and generates warning messages about anything that doesn't match.

In the Markpub repository:  

 -  `test_markpub.py` is called like this:
```shell
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install markpub
pytest tests
```

 - only if needed: to rebuild the `baseline` output directory:  
 ```shell
cd tests/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install markpub
markpub -c test-input/.markpub//markpub.yaml -w test-input -o baseline
```

When Markpub is installed test_markpub.py is called like this:

```shell
cd YOURWIKIDIR/.markpub
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install markpub
pytest tests
```

test_markpub.py exits with a return code of 0 for success, or non-zero if there is a fault.

A successful test output on a macOS system looks like this:

```shell
========================================= test session starts =========================================
platform darwin -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/band/Public/pkgs/markpub/markpub
rootdir: /LOCAL/FULL/PATH/TO/massivewikibuilder
configfile: pyproject.toml
collected 1 item

tests/test_markpub.py .                                                                          [100%]

========================================== 1 passed in 0.06s ==========================================
```
where `/LOCAL/FULL/PATH/TO/` is the full path to the Markpub repository on your system.  

## Scope and Limitations

The current test suite does not build or check the Lunr search files.

