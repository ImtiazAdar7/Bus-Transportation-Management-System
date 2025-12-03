# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bus Transportation Management System'
copyright = '2025, Imtiaz Ahmed, Nahid Sarwar Ratul, Samiul Ahamed Fhyas, Sakibur Rahman Somoy'
author = 'Imtiaz Ahmed, Nahid Sarwar Ratul, Samiul Ahamed Fhyas, Sakibur Rahman Somoy'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Automatically generate documentation from docstrings
    'sphinx.ext.viewcode',     # Add links to source code
    'sphinx.ext.todo',         # Support for todo items
    'sphinx.ext.coverage',     # Documentation coverage reports
    'sphinx.ext.intersphinx',  # Link to other projects' documentation
    'sphinx.ext.napoleon',     # Support for Google/NumPy style docstrings
]

# Add sphinx-autodoc-typehints if available (optional)
# Uncomment the line below if you have installed: pip install sphinx-autodoc-typehints
# extensions.append('sphinx_autodoc_typehints')

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Use Read the Docs theme (requires: pip install sphinx-rtd-theme)
# If not installed, Sphinx will use alabaster as fallback
html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_member_order = 'bysource'  # Order members by source order
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': True,
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'flask': ('https://flask.palletsprojects.com/', None),
}
