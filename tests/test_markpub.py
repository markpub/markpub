#!/usr/bin/env python3

import subprocess
import pytest
import filecmp
import re
import shutil
import zipfile

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

def test_zip_build(tmp_path):
    """
    Builds with --zip from a copy of the fixture wiki (plus an unlisted page)
    and verifies the zip archive: dated filename, single top-level directory,
    contents equal to the published Markdown pages (sidebar included,
    unlisted pages excluded).
    """
    wiki = tmp_path / "test-input"
    shutil.copytree("tests/test-input", wiki)
    (wiki / "Unlisted Test Page.md").write_text("---\nunlisted: true\n---\n\nRendered but not collected.\n")
    output = tmp_path / "output"
    cmd = [
        "markpub",
        "build",
        "-c", str(wiki / ".markpub" / "markpub.yaml"),
        "-i", str(wiki),
        "-o", str(output),
        "--zip",
    ]
    subprocess.run(cmd, check=True)

    zips = list(output.glob("*.zip"))
    assert len(zips) == 1, "expected exactly one zip archive in output"
    # dated filename: {repo-name}-{YYYY-MM-DD-HHMM}Z.zip; the copied wiki has
    # no git remote, so the repo name falls back to slugified wiki_title
    assert re.fullmatch(r"markpub-test-website-\d{4}-\d{2}-\d{2}-\d{4}Z\.zip", zips[0].name)

    basename = zips[0].name.removesuffix(".zip")
    with zipfile.ZipFile(zips[0]) as zip_archive:
        names = zip_archive.namelist()
    assert names and all(n.startswith(f"{basename}/") for n in names), "all members must be inside one top-level directory named like the zip"

    expected = {
        p.relative_to(wiki).as_posix()
        for p in wiki.rglob("*.md")
        if not any(part.startswith(".") for part in p.relative_to(wiki).parts)
    } - {"Unlisted Test Page.md"}
    assert {n.removeprefix(f"{basename}/") for n in names} == expected
