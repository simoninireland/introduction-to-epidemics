# Makefile for "Introduction to epidemics"
#
# Copyright (C) 2020 Simon Dobson <simon.dobson@st-andrews.ac.uk>
# 
# Licensed under the Creative Commons Attribution-Share Alike 4.0 
# International License (https://creativecommons.org/licenses/by-sa/4.0/).
#

# ----- Sources -----

# Text
INDEX = src/index.md
TEXT = \
	src/dedication.rst \
	src/preface.md \
	src/model.md \
	src/progress.md \
	src/notes.md \
	src/reading.md \
	src/zbibliography.md \
	src/acknowledgements.md \
	src/about.md \
	src/copyright.md

# Notebooks
NOTEBOOKS =  \
	src/continuous.ipynb \
	src/network.ipynb \
	src/er.ipynb \
	src/tracing.ipynb \
	src/thresholds.ipynb \
	src/hcn.ipynb \
	src/herd.ipynb \
	src/vaccination.ipynb \
	src/seir.ipynb \
	src/distancing.ipynb

# Extra print files
LATEX_EXTRAS = \
	latex/conf.py \
	latex/latex.rst \
	latex/rawbibliography.rst \
	latex/style.tex

# Image files
RAW_IMAGES = \
	src/sd.png \
	src/cc-by-nc-sa.png \
	src/disease-types.png \
	src/disease-periods.png

# Generated plots
GENERATED_IMAGES = \
	src/degree-distribution-er.png \
	src/network-same-beta-alpha.png \
	src/herd-finals.png \
	src/sir-er-rewiring.png \
	src/sir-phydist.png \
	src/physical-distancing.png

# Generated datasets
GENERATED_DATASETS = \
	src/datasets/threshold-er.json \
	src/datasets/threshold-plc.json \
	src/datasets/sier-er.json \
	src/datasets/sir-quarantine.json \
	src/datasets/seir-quarantine.json \
	src/datasets/sir-phydist.json

# Bibliography
BIBLIOGRAPHY = src/bibliography.bib

# License
LICENSE = LICENSE

# Structure
BOOK_CONFIG = _config.yml
BOOK_TOC = _toc.yml

# LaTeX Tufte template URL
LATEX_CLASS_ZIP_URL = http://www.latextemplates.com/templates/books/1/book_1.zip
LATEX_CLASS_ZIP = book_1.zip

# All content
CONTENT = \
	$(INDEX) \
	$(TEXT) \
	$(NOTEBOOKS) \
	$(RAW_IMAGES) $(GENERATED_IMAGES) \
	$(BIBLIOGRAPHY) \
	$(BOOK_CONFIG) $(BOOK_TOC)


# ----- Tools -----

# Root directory
ROOT = $(shell pwd)

# Base commands
PYTHON = python3.6            # specific sub-version for use with compute cluster
IPYTHON = ipython
JUPYTER = jupyter
JUPYTER_BOOK = jupyter-book
LATEX = pdflatex
BIBTEX = bibtex
SPHINX = sphinx-build
GHP_IMPORT = ghp-import
PIP = pip
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
RSYNC = rsync
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
MKDIR = mkdir -p
ZIP = zip -r
UNZIP = unzip
WGET = wget
ECHO = echo

# Datestamp
DATE = `date`

# Requirements and venv
VENV = venv3
REQUIREMENTS = requirements.txt

# Book construction
BUILD_DIR = _build
SRC_DIR = src
BOOK_DIR = bookdir
BOOK_BUILD_DIR = $(BOOK_DIR)/$(BUILD_DIR)
LATEX_BOOK_STEM = em-book
LATEX_BOOK = $(LATEX_BOOK_STEM).tex
LATEX_BUILD_DIR = $(BOOK_BUILD_DIR)/latex
LATEX_CLASS_DIR = $(LATEX_BUILD_DIR)/book_1
EPUB_BUILD_DIR = $(BOOK_BUILD_DIR)/epub

# Constructed commands
RUN_SERVER = PYTHONPATH=. $(JUPYTER) notebook
CREATE_BOOK = $(JUPYTER_BOOK) create $(BOOK_DIR)
BUILD_BOOK = $(JUPYTER_BOOK) build $(BOOK_DIR)
UPLOAD_BOOK = $(GHP_IMPORT) -n -p -f $(BOOK_BUILD_DIR)/html
BUILD_PRINT_BOOK = $(SPHINX) -b latex . _build/latex
BUILD_EPUB_BOOK = $(SPHINX) -b epub . _build/epub


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage


# Run the notebook server
live: env
	$(ACTIVATE)  && $(RUN_SERVER)


# Build HTML
book: env bookdir $(CONTENT)
	$(RM) $(BOOK_BUILD_DIR)/jupyter_execute
	$(RSYNC) $(CONTENT) $(BOOK_DIR)
	$(ACTIVATE) && $(BUILD_BOOK)

bookdir: $(BOOK_DIR)

$(BOOK_DIR): Makefile $(BOOK_CONFIG)
	$(RM) $(BOOK_DIR)
	$(ACTIVATE) && $(CREATE_BOOK)
	$(RM) $(BOOK_DIR)/*.ipynb $(BOOK_DIR)/*.md


# Upload book to public web site
upload: book
	$(ACTIVATE) && $(UPLOAD_BOOK)


# Build a PDF for printed copy
print: env bookdir $(LATEX_BUILD_DIR)
	$(RM) $(BOOK_BUILD_DIR)/jupyter_execute
	$(RSYNC) $(CONTENT) $(BOOK_DIR)
	$(RSYNC) $(LATEX_EXTRAS) $(BOOK_DIR)
	$(ACTIVATE) && $(CHDIR) $(BOOK_DIR) && $(BUILD_PRINT_BOOK)
	$(CP) $(LATEX_BUILD_DIR)/$(LATEX_BOOK) /tmp
	$(SED) -e 's/zbibliography://g' /tmp/$(LATEX_BOOK) >$(LATEX_BUILD_DIR)/$(LATEX_BOOK)
	$(RM) /tmp/$(LATEX_BOOK)
	-make latex
	-make bibtex
	-make latex
	-make latex

.PHONY: latex
latex:
	$(CHDIR) $(LATEX_BUILD_DIR) && $(LATEX) <<EOF \
	\\nonstopmode\\input{$(LATEX_BOOK_STEM)} \
	EOF

.PHONY: bibtex
bibtex:
	$(CHDIR) $(LATEX_BUILD_DIR) && $(BIBTEX) $(LATEX_BOOK_STEM)

$(LATEX_BUILD_DIR):
	$(MKDIR) $(LATEX_BUILD_DIR) $(LATEX_CLASS_DIR)
	$(CHDIR) $(LATEX_CLASS_DIR) && $(WGET) $(LATEX_CLASS_ZIP_URL) && $(UNZIP) $(LATEX_CLASS_ZIP)


# Build an Epub
epub: env bookdir
	$(RM) $(BOOK_BUILD_DIR)/jupyter_execute
	$(RSYNC) $(CONTENT) $(BOOK_DIR)
	$(RSYNC) $(LATEX_EXTRAS) $(BOOK_DIR)
	$(ACTIVATE) && $(CHDIR) $(BOOK_DIR) && $(BUILD_EPUB_BOOK)


# Build a development venv
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(REQUIREMENTS) $(VENV)/requirements.txt
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt


# Clean up the build
clean:
	$(RM) $(BOOK_DIR) $(LATEX_BUILD_DIR)

# Clean up everything, including the venv (which is quite expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Usage -----

define HELP_MESSAGE
Editing:
   make live         run the notebook server

Production:
   make book         build the book using Jupyter Book
   make upload       upload book to public web site
   make print        build a PDF of the book for printing

Maintenance:
   make env          create a virtual environment
   make clean        clean-up the build
   make reallyclean  delete the venv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"


