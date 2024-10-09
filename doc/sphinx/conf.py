# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'release-feed-mediola'
executable_name = 'release-feed-mediola'
author = 'Claudia Pellegrino <clau@tiqua.de>'
description = 'Atom feed for software product releases of Mediola AG'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

myst_enable_extensions = [
    'deflist',
]

templates_path = []
exclude_patterns = []

# Man page output

man_pages = [(
    'index',
    executable_name,
    description,
    [author],
    1,
)]
