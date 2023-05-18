#!/usr/bin/env make

.PHONY: all clean default doc format help lint preen run tags test

.DEFAULT_GOAL	:= test
CTAGS		:= $(shell which ctags)
PIP		:= $(shell which pip3)
PYTHON		:= $(shell which python3)

PROJECT		:= quotes
SRCS		:= $(wildcard *.py $(PROJECT)/*.py tests/*.py)
LINE_LENGTH	:= 79	# PEP-8 Standards suggest a line-length of 79
			# so we ensure the styling tools all follow this

all:	preen test doc run
default: check test

help:
	@echo
	@echo "Default goal: ${.DEFAULT_GOAL}"
	@echo
	@echo "  all:    style and test"
	@echo "  preen:  format and lint"
	@echo "  format: format code, sort imports and requirements"
	@echo "  lint:   check code"
	@echo "  test:   run unit tests"
	@echo "  docs:   document module"
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
	@echo "Deactivate with:"
	@echo
	@echo "  deactivate"
	@echo

preen:	format tags lint

format:
	# sort imports
	isort --line-length $(LINE_LENGTH) --profile black $(SRCS)
	# format code to googles style
	black -q $(SRCS)
	# sort requirements
	sort-requirements requirements.txt

tags:
ifdef CTAGS
	# build ctags for vim
	ctags --recurse -o tags $(SRCS)
endif

lint:
	# check with flake8
	flake8 --verbose $(SRCS)
	# check with pylint
	pylint --verbose $(SRCS)

test:	preen
	# unit tests with coverage report
	pytest --verbose \
	  --html=html/unittests.html --self-contained-html \
	  --cov-report=html --cov=$(PROJECT)

doc:
	# generate code documentation
	pdoc quotes -o html/

run:
	$(PYTHON) get_weekly_quotes.py MSFT

clean:
	# clean generated artefacts
	$(RM) -rf .coverage
	$(RM) -rf html/
	$(RM) -rf .hypothesis/
	$(RM) -rf __pycache__/ $(PROJECT)/__pycache__/
	$(RM) -rf .pytest_cache/

cleanall: clean
	# clean development environment
	$(RM) -r .venv/
	$(RM) -r .idea/
