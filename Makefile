# Makefile for "Introduction to epidemics"
#
# Copyright (C) 2020 Simon Dobson
# 
# Licensed under the Creative Commons Attribution-Share Alike 4.0 
# International License (https://creativecommons.org/licenses/by-sa/4.0/).
#

# ----- Sources -----

# Notebooks
HEADER = index.ipynb
NOTEBOOKS =  \
	continuous.ipynb

# Image files
RAW_IMAGES = \
	cc-at-nc-sa.png \
	sd.jpg


# ----- Tools -----

# Base commands
PYTHON = python3
IPYTHON = ipython
JUPYTER = jupyter
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

# Constructed commands
RUN_SERVER = PYTHONPATH=. $(JUPYTER) notebook --port 1626


# ----- Top-level targets -----

# Default prints a help message
help:
	@make usage

# Run the notebook server
live: env
	$(ACTIVATE)  && $(RUN_SERVER)

# Build a development venv
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(CP) $(REQUIREMENTS) $(VENV)/requirements.txt
	$(ACTIVATE) && $(CHDIR) $(VENV) && $(PIP) install -r requirements.txt

# Clean up everything, including the computational environment (which is expensive to rebuild)
clean: clean
	$(RM) $(VENV)


# ----- Usage -----

define HELP_MESSAGE
Editing:
   make live         run the notebook server

Maintenance:
   make env          create a known-good development virtual environment
   make clean        clean-up the build

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"


