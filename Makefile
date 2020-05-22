# Makefile for "Introduction to epidemics"
#
# Copyright (C) 2020 Simon Dobson <simon.dobson@st-andrews.ac.uk>
# 
# Licensed under the Creative Commons Attribution-Share Alike 4.0 
# International License (https://creativecommons.org/licenses/by-sa/4.0/).
#

# ----- Sources -----

# Text
TEXT = \
	src/index.md \
	src/model.md \
	src/progress.md \
	src/notes.md \
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
	src/hcn.ipynb

# Image files
RAW_IMAGES = \
	src/sd.png \
	src/cc-by-nc-sa.png \
	src/disease-types.png \
	src/disease-periods.png

# Generated plots
GENERATED_IMAGES =

# Generated datasets
GENERATED_DATASETS = \
	src/datasets/threshold-er.json \
	src/datasets/threshold-plc.json

# Bibliography
BIBLIOGRAPHY = src/bibliography.bib

# License
LICENSE = LICENSE

# Structure
BOOK_CONFIG = _config.yml
BOOK_TOC = _toc.yml

# All content
CONTENT = \
	$(TEXT) \
	$(NOTEBOOKS) \
	$(RAW_IMAGES) \
	$(BIBLIOGRAPHY) \
	$(LICENSE) \
	$(BOOK_CONFIG) $(BOOK_TOC)


# ----- Tools -----

# Base commands
PYTHON = python3.6
IPYTHON = ipython
JUPYTER = jupyter
JUPYTER_BOOK = jupyter-book
GHP_IMPORT = ghp-import
PIP = pip
VIRTUALENV = $(PYTHON) -m venv
ACTIVATE = . $(VENV)/bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r
ECHO = echo

# Root directory
ROOT = $(shell pwd)

# Datestamp
DATE = `date`

# Requirements and venv
VENV = venv3
REQUIREMENTS = requirements.txt

# Book construction
BOOK_DIR = bookdir
BOOK_CONTENT = src

# Constructed commands
RUN_SERVER = PYTHONPATH=. $(JUPYTER) notebook
MAKE_DATESTAMP = $(ECHO) "(This version built $(DATE))" >>$(BOOK_DIR)/index.md
CREATE_BOOK = $(JUPYTER_BOOK) create $(BOOK_DIR)
BUILD_BOOK = $(JUPYTER_BOOK) build $(BOOK_DIR)
UPLOAD_BOOK = $(GHP_IMPORT) -n -p -f $(BOOK_DIR)/_build/html


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run the notebook server
live: env
	$(ACTIVATE)  && $(RUN_SERVER)

# Book building
book: $(BOOK_DIR)
	$(CP) $(CONTENT) $(BOOK_DIR)
	$(MAKE_DATESTAMP)
	$(ACTIVATE) && $(BUILD_BOOK)

$(BOOK_DIR): Makefile $(BOOK_CONFIG) $(BOOK_TOC) $(CONTENT) $(BIBLIOGRAPHY)
	$(RM) $(BOOK_DIR)
	$(ACTIVATE) && $(CREATE_BOOK)
	$(RM) $(BOOK_DIR)/*.ipynb $(BOOK_DIR)/*.md

# Upload book to public web site
upload:
	$(ACTIVATE) && $(UPLOAD_BOOK)

# Build a development venv
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(REQUIREMENTS) $(VENV)/requirements.txt
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Clean up the build
clean:
	$(RM) $(BOOK_DIR)

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

Maintenance:
   make env          create a virtual environment
   make clean        clean-up the build
   make reallyclean  delete the venv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"


