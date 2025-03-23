# Configuration file for the Sphinx documentation builder.



import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
from fancytypes import __version__


project = 'FancyTypes'
copyright = '2024, hlatorrec'
author = 'hlatorrec'
version = __version__
release = __version__


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 
              'sphinx.ext.githubpages', 'sphinx_rtd_theme',]


autodoc_mock_imports = ['numpy']


add_module_names = False
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []


html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


html_theme_options = {'style_nav_header_background' : '#734f96'} # This is the Fortran logo color
