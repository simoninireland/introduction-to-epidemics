source_suffix = [ '.rst', '.md', '.ipynb' ]

extensions = [
    'myst_nb',
    'sphinx_book_theme',
    'sphinxcontrib.bibtex',
    'sphinx.ext.imgmath',
]

project ="Epidemic modelling -- Some notes, maths, and code"
author = "Simon Dobson"
copyright = "Copyright (c) 2020"
version = "0.1"

jupyter_execute_notebooks = 'off'


# Epub

master_doc = 'epub'
epub_basename = 'em-book'
epub_title = project
epub_author = author
epub_copyright = "Copyright (c) 2020, Simon Dobson"
epub_publisher = "https://simoninireland.github.io/introduction-to-epidemics"
epub_identifier = "XXX"
epub_scheme = "ISBN"
epub_pre_files = [ ("_static/epublication.html", "") ]
html_static_path = ["../epub/static"]
epub_cover = ("_static/ecover.png", "")
epub_tocdepth = 2
epub_show_urls = 'no'
epub_use_index = True


