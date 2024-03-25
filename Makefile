#!/usr/bin/env make

.PHONY: all badge clean default doc format help lint preen report run tags test

.DEFAULT_GOAL	:= default
CODE_COVERAGE	:= 90	# minimum percentage for code coverage
CTAGS		:= $(shell which ctags)
LINE_LENGTH	:= 79	# PEP-8 standards ensure styling tools use this too
PIP		:= $(shell which pip3)
PYTHON		:= $(shell which python3)
RM		:= rm -rf

PROJECT		:= quotes
SRCS		:= $(wildcard *.py $(PROJECT)/*.py tests/*.py)

all:	preen test report run
default: preen test

help:
	@echo
	@echo "Default goal: ${.DEFAULT_GOAL}"
	@echo
	@echo "  all:    style and test"
	@echo "  preen:  format and lint"
	@echo "  format: format code, sort imports and requirements"
	@echo "  lint:   check code"
	@echo "  test:   run unit tests"
	@echo "  doc:    document module"
	@echo "  clean:  delete all generated files"
	@echo
	@echo "Initialise virtual environment (.venv) with:"
	@echo
	@echo "  pip3 install -U virtualenv; python3 -m virtualenv .venv; source .venv/bin/activate; pip3 install -Ur requirements.txt"
	@echo
	@echo "Start virtual environment (.venv) with:"
	@echo
	@echo "  source .venv/bin/activate"
	@echo
	@echo Deactivate with:
	@echo
	@echo "  deactivate"
	@echo

preen:	format tags lint

format:
	# sort imports
	@isort --line-length $(LINE_LENGTH) --profile black $(PROJECT)
	# format code to googles style
	@black --line-length $(LINE_LENGTH) $(PROJECT)
	# sort requirements
	@sort-requirements requirements.txt

tags:
ifdef CTAGS
	# build ctags for vim
	@ctags --recurse -o tags $(SRCS)
endif

lint:
	# check with flake8
	@flake8 $(PROJECT)
	# lint with pylint
	@pylint $(PROJECT)
	# security checks with bandit
	@bandit --configfile .bandit.yaml --recursive $(PROJECT)

test:
	# unit tests with coverage report
	@pytest --verbose --cov --cov-report=html \
	  --self-contained-html --html=public/pytest_report.html

report:	doc badge

doc:
	# generate documentation and public directory
	@pdoc --output-directory public $(PROJECT)
	@bandit --configfile .bandit.yaml --recursive \
	  --format html --output public/bandit_report.html $(PROJECT)
	@pylint $(PROJECT) --exit-zero --load-plugins=pylint_report \
	  --output-format=pylint_report.CustomJsonReporter:public/pylint_report.json
	@pylint_report -o public/pylint_report.html public/pylint_report.json

badge:
	# generate badges
	# flake8
	@flake8 --statistics --exit-zero --format=html --htmldir public/flake8 \
	  --output-file public/flake8stats.txt $(PROJECT)
	@genbadge flake8 --input-file public/flake8stats.txt \
	  --output-file public/flake8.svg
	# pylint
	@$(RM) public/pylint.svg
	@anybadge \
	  --value=$(shell pylint $(PROJECT) | sed -n 's/^Your code has been rated at \([^\/]*\).*/\1/p') \
	  --file=public/pylint.svg \
	  --label pylint
	# pytest
	@pytest --junitxml=public/pytest_report.xml
	@genbadge tests \
	  --input-file public/pytest_report.xml \
	  --output-file public/tests.svg

run:
	# get quotes for microsoft
	@$(PYTHON) get_weekly_quotes.py MSFT

clean:
	# clean generated artefacts
	$(RM) $(PROJECT)/__pycache__/ $(PROJECT)/*/__pycache__/
	$(RM) .coverage
	$(RM) .hypothesis/
	$(RM) .pytest_cache/
	$(RM) public/
	$(RM) tags

distclean: clean
	# clean development environment
	$(RM) .idea/
	$(RM) .venv/
	$(RM) .vscode/

