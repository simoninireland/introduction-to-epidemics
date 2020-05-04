# Makefile for "Introduction to epidemics"
#
# Copyright (C) 2020 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Share Alike 4.0 
# International License (https://creativecommons.org/licenses/by-sa/4.0/).
#

# ----- Sources -----

# Notebooks
HEADER = src/index.ipynb
NOTEBOOKS =  \
	src/continuous.ipynb\
	src/network.ipynb \
	src/notes.ipynb \
	src/zbibliography.md

# Image files
RAW_IMAGES = \
	src/sd.jpg

# Bibliograohy
BIBLIOGRAPHY = src/bibliography.bib

# All content
CONTENT = \
	$(HEADER) \
	$(NOTEBOOKS) \
	$(RAW_IMAGES) \
	$(BIBLIOGRAPHY)

# License
LICENSE = LICENSE

# Structure
BOOK_CONFIG = _config.yml
BOOK_TOC = _toc.yml


# ----- Tools -----

# Base commands
PYTHON = python3
IPYTHON = ipython
JUPYTER = jupyter
JUPYTER_BOOK = jupyter-book
PIP = pip
VIRTUALENV = python3 -m venv
ACTIVATE = . $(VENV)/bin/activate
TR = tr
CAT = cat
SED = sed
RM = rm -fr
CP = cp
CHDIR = cd
ZIP = zip -r

# Root directory
ROOT = $(shell pwd)

# Requirements and venv
VENV = venv3
REQUIREMENTS = requirements.txt

# Book construction
BOOK_DIR = bookdir
BOOK_CONTENT = content

# Constructed commands
RUN_SERVER = PYTHONPATH=. $(JUPYTER) notebook
CREATE_BOOK = \
	$(JUPYTER_BOOK) create $(BOOK_DIR) \
	--overwrite \
	--license $(LICENSE) \
	--toc $(BOOK_TOC) \
	--config $(BOOK_CONFIG) \
	--content-folder $(BOOK_CONTENT)
BUILD_BOOK = \
	$(JUPYTER_BOOK) build $(BOOK_DIR)


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run the notebook server
live: env
	$(ACTIVATE)  && $(RUN_SERVER)

# Book building
book: $(BOOK_DIR)
	$(ACTIVATE) && $(BUILD_BOOK)

$(BOOK_DIR): Makefile $(BOOK_CONFIG) $(BOOK_TOC) $(CONTENT) $(BIBLIOGRAPHY)
	$(RM) $(BOOK_DIR)
	$(ACTIVATE) && $(CREATE_BOOK)

# Build a development venv
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(REQUIREMENTS) $(VENV)/requirements.txt
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Clean up the build
clean:
	$(RM) $(BOOKDIR)

# Clean up everything. including the venv
reallyclean: clean
	$(RM) $(VENV)


# ----- Usage -----

define HELP_MESSAGE
Editing:
   make live         run the notebook server
   make book         build the book using Jupyter Book

Maintenance:
   make env          create a known-good development virtual environment
   make clean        clean-up the build
   make reallyclean  delete the venv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"


