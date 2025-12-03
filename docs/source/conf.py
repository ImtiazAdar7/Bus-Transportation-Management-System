# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bus Transportation Management System'
copyright = '2025, Imtiaz Ahmed, Nahid Sarwar Ratul, Samiul Ahamed Fhyas, Sakibur Rahman Somoy'
author = 'Imtiaz Ahmed, Nahid Sarwar Ratul, Samiul Ahamed Fhyas, Sakibur Rahman Somoy'
release = '1.0'

# -- Path setup --------------------------------------------------------------
# Add the project root to Python path so Sphinx can import your modules
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Automatically extract documentation from docstrings
    'sphinx.ext.viewcode',      # Add links to source code
    'sphinx.ext.napoleon',     # Support for Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
