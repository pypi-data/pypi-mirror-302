## Setup:
# pip install sphinx
# pip install sphinx-rtd-theme

# generate the initial sphinx stuff in a docs folder using `sphinx-quickstart`
# cd .. (out of docs)
# generate the rst files using `sphinx-apidoc -o docs .`
# this generates rst files
# change the conf.py theme to "sphinx_rtd_theme" or wtv theme u want
# add the following extensions: extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

# add the following to the start of conf.py:
"""
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

"""

# Usage:
# cd into the docs folder, and run:
# `.\make.bat html`
# output documentation is now in docs/_build/index.html
