#!/usr/bin/env python3

import subprocess
import pytest
import filecmp

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_markpub():
    """
    Runs markpub with the provided input directory and an output directory at the same level.
    Captures stdout and stderr, checks return code for success/fail.
    """
    try:
        cmd = [
            "markpub",
            "build",
            "-c", "tests/test-input/.markpub/markpub.yaml",
            "-i", "tests/test-input",
            "-o", "tests/test-output",
            "-t", "tests/test-input/.markpub/this-website-themes/dolce"
        ]

        subprocess.run(cmd, check=True)

    except OSError as e:
        # OSError could be raised for issues related to file paths, directories, or if markpub not installed
        logging.error(f"OS Error (file paths, directories, markput not installed?): {e}")
        return False
    except subprocess.CalledProcessError as e:
        # This will be raised if the called process returns a non-zero return code
        logging.error(f"CalledProcessError (called process returned a non-zero return code): {e}")
        return False
    except Exception as e:
        # Generic error handler for any other exceptions
        logging.error(f"Unexpected error occurred: {e}")
        return False

def compare_markpub_directories(output, baseline):
    comparison = filecmp.dircmp(output, baseline)
    if comparison.left_only or comparison.right_only or not ('build-results.json' in comparison.diff_files and len(comparison.diff_files) == 1):
        return False
    else:
        return True

@pytest.fixture(scope="module")
def run_and_verify():
    run_markpub()

def test_compare_output_with_baseline(run_and_verify):
    assert compare_markpub_directories("tests/test-output/", "tests/baseline/"), "Directory contents do not match."
