# Markpub Tests

TODO: Clean up tests/ data `.massivewikibuilder` references

test_markpub.py is a `pytest` script that is used to test markpub.py.

The test script compares the known baseline files with the generated output files, and generates warning messages about anything that doesn't match.

In the Massive Wiki Builder repository:  
 -  `test_markpub.py` is called like this:
```shell
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../../requirements.txt
pytest tests
```

 - only if needed: to rebuild the `baseline` output directory:  
 ```shell
cd tests/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt
markpub. -c test-input/.markpub//markpub.yaml -w test-input -o baseline
```

When Markpub is installed in a wiki, test_markpub.py is called like this:

```shell
cd YOURWIKIDIR/.markpub
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest tests
```

test_markpub.py exits with a return code of 0 for success, or non-zero if there is a fault.

A successful test output on a macOS system looks like this:

```shell
========================================= test session starts =========================================
platform darwin -- Python 3.12.2, pytest-8.1.1, pluggy-1.4.0
rootdir: /LOCAL/FULL/PATH/TO/massivewikibuilder
collected 1 item                                                                                      

tests/test_markpub.py .                                                                             [100%]

========================================== 1 passed in 0.31s ==========================================
```
where `/LOCAL/FULL/PATH/TO/` is the full path to the Markpub repository on your system.  

## Scope and Limitations

The current test suite does not build or check the Lunr search files.
