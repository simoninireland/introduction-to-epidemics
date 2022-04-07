# Makefile for "Introduction to epidemics"
#
# Copyright (C) 2020--2022 Simon Dobson <simon.dobson@st-andrews.ac.uk>
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
	src/conclusion.md \
	src/notes.md \
	src/reading.md \
	src/zbibliography.md \
	src/genindex.md \
	src/acknowledgements.md \
	src/about.md \
	src/copyright.md \
	src/print.md

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
	latex/latex.rst \
	latex/rawbibliography.rst \
	latex/style.tex
LATEX_CONFIG =	latex/conf.py

# Extra e-book files
EPUB_EXTRAS = \
	epub/epub.rst \
	epub/epublication.md
EPUB_CONFIG = epub/conf.py

# Image files
RAW_IMAGES = \
	src/sd.png \
	src/cc-by-nc-sa.png \
	src/disease-types.png \
	src/disease-periods.png \
	src/print-cover-small.png

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

# Video scenes
VIDEO = \
	video/epidemic-threshold/Header.mp4 \
	video/epidemic-threshold/RValue.mp4 \
	video/epidemic-threshold/Network.mp4 \
	video/epidemic-threshold/Topology.mp4 \
	video/epidemic-threshold/VaryDisease.mp4
VIDEO_UTILS = \
	video/epidemic-threshold/data.py

# Bibliography
BIBLIOGRAPHY = src/bibliography.bib

# License
LICENSE = LICENSE

# Structure
BOOK_CONFIG = _config.yml
BOOK_TOC = _toc.yml

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
PYTHON = python3.6                        # specific version for talking to compute cluster
IPYTHON = ipython
JUPYTER = jupyter
JUPYTER_BOOK = jupyter-book
MANIM = manim
LATEX = pdflatex
BIBTEX = bibtex
MAKEINDEX = makeindex
SPHINX = sphinx-build
GHP_IMPORT = ghp-import
GHOSTSCRIPT = gs
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
KNOWN_GOOD_REQUIREMENTS = known-good-requirements.txt

# Jupyter Book construction
BUILD_DIR = _build
SRC_DIR = src
BOOK_DIR = bookdir
BOOK_BUILD_DIR = $(BOOK_DIR)/$(BUILD_DIR)

# LaTeX construction
LATEX_BUILD_DIR = $(BOOK_BUILD_DIR)/latex
LATEX_BOOK_STEM = em-book
LATEX_BOOK = $(LATEX_BOOK_STEM).tex
LATEX_BOOK_PDF = $(LATEX_BOOK_STEM).pdf

# Epub construction
EPUB_BUILD_DIR = $(BOOK_BUILD_DIR)/epub

# Video construction -- manim quality flag and the sub-directory for assets
VIDEO_QUALITY = l
VIDEO_RESOLUTION = 480p15

# Video temporary asset directories
VIDEO_MEDIA = $(shell find video -type d -name media -print)

# Commands
RUN_SERVER = PYTHONPATH=. $(JUPYTER) notebook
CREATE_BOOK = $(JUPYTER_BOOK) create $(BOOK_DIR)
BUILD_BOOK = $(JUPYTER_BOOK) build $(BOOK_DIR)
UPLOAD_BOOK = $(GHP_IMPORT) -n -p -f $(BOOK_BUILD_DIR)/html
BUILD_PRINT_BOOK = $(SPHINX) -b latex -c $(ROOT)/latex . $(BUILD_DIR)/latex
BUILD_BIBLIOGRAPHY = $(BIBTEX) $(LATEX_BOOK_STEM)
BUILD_INDEX = $(MAKEINDEX) $(LATEX_BOOK_STEM)
BUILD_EPUB_BOOK = $(SPHINX) -b epub -c $(ROOT)/epub . $(BUILD_DIR)/epub


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


# Build a PDF for print copy
print: env bookdir
	$(RM) $(BOOK_BUILD_DIR)/jupyter_execute
	$(RSYNC) $(CONTENT) $(BOOK_DIR)
	$(RSYNC) $(LATEX_EXTRAS) $(BOOK_DIR)
	$(ACTIVATE) && $(CHDIR) $(BOOK_DIR) && $(BUILD_PRINT_BOOK)
	$(CP) $(LATEX_BUILD_DIR)/$(LATEX_BOOK) /tmp
	$(SED) -e 's/zbibliography://g' /tmp/$(LATEX_BOOK) >$(LATEX_BUILD_DIR)/$(LATEX_BOOK)
	-make latex
	$(CHDIR) $(LATEX_BUILD_DIR) && $(BUILD_BIBLIOGRAPHY)
	-make latex
	$(CP) $(LATEX_BUILD_DIR)/$(LATEX_BOOK_STEM).idx /tmp
	$(SED) -e 's/spxentry /spxentry/g' /tmp/$(LATEX_BOOK_STEM).idx >$(LATEX_BUILD_DIR)/$(LATEX_BOOK_STEM).idx
	$(CHDIR) $(LATEX_BUILD_DIR) && $(BUILD_INDEX)
	-make latex
	-make latex
	$(RM) /tmp/$(LATEX_BOOK) /tmp/$(LATEX_BOOK_STEM).idx
	$(CP) $(LATEX_BUILD_DIR)/$(LATEX_BOOK_PDF) $(LATEX_BOOK_PDF)

.PHONY: latex
latex:
	$(CHDIR) $(LATEX_BUILD_DIR) && $(LATEX) <<EOF \
	\\nonstopmode\\input{$(LATEX_BOOK_STEM)} \
	EOF


# Build the video scenes
.PHONY: video
video: $(VIDEO)


# Build an Epub
epub: env # bookdir
	$(RM) $(BOOK_BUILD_DIR)/jupyter_execute
	$(RSYNC) $(CONTENT) $(BOOK_DIR)
	$(RSYNC) $(EPUB_EXTRAS) $(BOOK_DIR)
	$(ACTIVATE) && $(CHDIR) $(BOOK_DIR) && $(BUILD_EPUB_BOOK)


# Build a development venv
.PHONY: env
env: $(VENV)

$(VENV):
	$(VIRTUALENV) $(VENV)
	$(ACTIVATE) && $(PIP) install -r $(KNOWN_GOOD_REQUIREMENTS)


# Clean up the build
clean:
	$(RM) $(BOOK_DIR) $(LATEX_BUILD_DIR) $(VIDEO) $(VIDEO_MEDIA)


# Clean up everything, including the venv (which is quite expensive to rebuild)
reallyclean: clean
	$(RM) $(VENV)


# ----- Implicit rules -----
.SUFFIXES: .py .mp4

.py.mp4:
	$(MANIM) -q$(VIDEO_QUALITY) $<
	$(CP) media/videos/$(shell basename $< .py)/$(VIDEO_RESOLUTION)/*.mp4 $(shell dirname $<)


# ----- Usage -----

define HELP_MESSAGE
Editing:
   make live         run the notebook server

Production:
   make book         build the book using Jupyter Book
   make upload       upload book to public web site
   make print        build a PDF of the book for printing
   make video        build all the video scenes

Maintenance:
   make env          create a virtual environment
   make clean        clean-up the build
   make reallyclean  delete the venv as well

endef
export HELP_MESSAGE

usage:
	@echo "$$HELP_MESSAGE"
