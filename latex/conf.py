source_suffix = [ '.rst', '.md', '.ipynb' ]

extensions = [
    'myst_nb',
    'sphinx_book_theme',
    'sphinxcontrib.bibtex',
]

project ="Epidemic modelling -- Some notes, maths, and code"
author = "Simon Dobson"
copyright = "Copyright (c) 2020"
version = "0.1"
master_doc = 'index'

jupyter_execute_notebooks = 'off'


# Latex

latex_elements = {
     'papersize': 'b5paper',
     'fontpkg': '',
     'fncychap': '',
     'maketitle': '\\maketitle\\backoftitlepage',
     'pointsize': '',
     'preamble': '\\include{style}',
     'passoptionstopackages': '',
     'releasename': "",
     'babel': '',
     'printindex': '',
     'fontenc': '',
     'inputenc': '',
     'classoptions': '',
     'utf8extra': '',
     
}

latex_additional_files = [ 'bibliography.bib', 'style.tex' ]

latex_documents = [
  ('latex', 'em-book.tex', project, author, 'tufte-book'),
]

latex_show_pagerefs = False
latex_domain_indices = False
latex_use_modindex = False
latex_logo = None
latex_show_urls = False


# Epub

epub_basename = 'em-book'
epub_title = project
epub_author = author
epub_copyright = "Copyright (c) 2020, Simon Dobson"
epub_publisher = "https://simoninireland.github.io/introduction-to-epidemics"
epub_scheme = 'URL'
epub_tocdepth = 2


