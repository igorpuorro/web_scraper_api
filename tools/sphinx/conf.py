# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))

def setup(app):
    app.add_css_file('custom.css')

project = 'Web Scraper API'
copyright = '2023, Igor Puorro'
author = 'Igor Puorro'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
exclude_patterns = ['_build']
html_static_path = ['_static']
templates_path = ['_templates'] # https://stackoverflow.com/questions/59307596/how-to-add-inheritance-diagram-to-all-modules-in-sphinx

# Configurations for inheritance diagram
graphviz_output_format = "svg"
inheritance_graph_attrs = dict(rankdir="TB", size='"6.0, 8.0"', fontsize=14)
