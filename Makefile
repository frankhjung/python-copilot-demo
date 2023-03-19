#!/usr/bin/env make

.PHONY: all check clean help run tags test version

.DEFAULT_GOAL := default

CTAGS	:= $(shell which ctags)
PIP	:= $(shell which pip3)
PYTHON	:= $(shell which python3)
SRCS	:= $(wildcard *.py **/*.py)

default: check test

all:	default run

help:
	@echo
	@echo "Default goal: ${.DEFAULT_GOAL}"
	@echo "  all:   check cover run test doc dist"
	@echo "  check: check style and lint code"
	@echo "  run:   run against test data"
	@echo "  clean: delete all generated files"
	@echo
	@echo "Initialise virtual environment (venv) with:"
	@echo
	@echo "pip3 install -U virtualenv; python3 -m virtualenv venv; source venv/bin/activate; pip3 install -Ur requirements.txt"
	@echo
	@echo "Start virtual environment (venv) with:"
	@echo
	@echo "source venv/bin/activate"
	@echo
	@echo "Deactivate with:"
	@echo
	@echo "deactivate"
	@echo

check:	tags style lint

tags:
ifdef CTAGS
	# build ctags for vim
	ctags --recurse -o tags $(SRCS)
endif

style:
	# sort imports
	isort $(SRCS)
	# format code to googles style
	black -q $(SRCS)

lint:
	# check with flake8
	flake8 $(SRCS)
	# check with pylint
	pylint $(SRCS)

test:
	# unit tests
	pytest -v tests/
 
run:
	$(PYTHON) get_weekly_quotes.py MSFT

clean:
	# clean generated artefacts
	-$(RM) -rf cover
	-$(RM) -rf .coverage
	-$(RM) -rf public
	-$(RM) -rf __pycache__ **/__pycache__
	-$(RM) -rf .pytest_cache
	-$(RM) -rf target
	-$(RM) -v MANIFEST
	-$(RM) -v **/*.pyc **/*.pyo **/*.py,cover
	-$(RM) -v *.pyc *.pyo *.py,cover
  