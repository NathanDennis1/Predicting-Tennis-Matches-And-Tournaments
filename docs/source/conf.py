# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import sphinx

sys.path.insert(0, os.path.abspath('../../src/'))

#def skip_src_module_name(app, what, name, obj, skip, options):
#    if name.startswith("src."):
#        return name[4:]  # Strip "src." prefix from module names
#    return skip
#
# Connect the event to modify module names
#def setup(app):
#    app.connect("autodoc-skip-member", skip_src_module_name)

# Additional settings to clean up documentation

project = 'Team 19 Docs'
copyright = '2024, Nathan Dennis, Yiming Chen, John Breedis'
author = 'Nathan Dennis, Yiming Chen, John Breedis'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'English'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
