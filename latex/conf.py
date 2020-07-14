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
     'papersize': 'b5paper,twoside,nohyper',
     'fontpkg': '',
     'fncychap': '',
     'maketitle': '\\maketitlepage\\backoftitlepage',
     'pointsize': '',
     'preamble': '''
\\include{style}
\\forprint''',
     'passoptionstopackages': '\\PassOptionsToPackage{draft}{hyperref}',
     'releasename': "",
     'babel': '',
     'printindex': '',
     'fontenc': '',
     'inputenc': '',
     'classoptions': '',
     'utf8extra': '',
     
}

latex_additional_files = [ '../src/bibliography.bib', 'style.tex' ]

latex_documents = [
  ('latex', 'em-book.tex', project, author, 'tufte-book'),
]

latex_show_pagerefs = False
latex_domain_indices = False
latex_use_modindex = False
latex_logo = None
latex_show_urls = 'no'
latex_tocdepth = 1
