#!/usr/bin/env make

.PHONY: all badge clean default doc format help lint preen report run tags test

.DEFAULT_GOAL	:= default
CTAGS		:= $(shell which ctags)
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
	@echo "  format: format code and sort imports"
	@echo "  lint:   check code"
	@echo "  test:   run unit tests"
	@echo "  doc:    document module"
	@echo "  clean:  delete all generated files"
	@echo
	@echo "Initialise virtual environment with:"
	@echo
	@echo "  uv sync"
	@echo
	@echo "Run a command in the virtual environment with:"
	@echo
	@echo "  uv run <command>"
	@echo

preen:	format tags lint

format:
	# format code and sort imports
	@uv run ruff format $(SRCS)
	@uv run ruff check --fix --select I $(SRCS)

tags:
ifdef CTAGS
	# build ctags for vim
	@ctags --recurse -o tags $(SRCS)
endif

lint:
	# check with ruff
	@uv run ruff check $(PROJECT)
	# security checks with bandit
	@uv run bandit --configfile pyproject.toml --recursive $(PROJECT)

test:
	# unit tests with coverage report
	@uv run pytest --verbose --cov --cov-report=html \
	  --html=public/pytest_report.html

report:	doc badge

doc:
	# generate documentation to public directory
	@uv run pdoc --output-directory public $(PROJECT)
	@uv run bandit --configfile pyproject.toml --recursive \
	  --format html --output public/bandit_report.html $(PROJECT)

badge:
	# generate badges
	# ruff
	@uv run ruff check --exit-zero --output-format json \
	  --output-file public/ruff_report.json $(PROJECT)
	@uv run python -c "\
	  import json, sys; \
	  data = json.load(open('public/ruff_report.json')); \
	  count = len(data); \
	  print(f'ruff: {count} issues'); \
	  import anybadge; \
	  badge = anybadge.Badge('ruff', \
	    value='pass' if count == 0 else f'{count} issues', \
	    default_color='green' if count == 0 else 'orange'); \
	  badge.write_badge('public/ruff.svg', overwrite=True)"
	# pytest
	@uv run pytest --junitxml=public/pytest_report.xml
	@uv run genbadge tests \
	  --input-file public/pytest_report.xml \
	  --output-file public/tests.svg

run:
	# get quotes for microsoft
	@uv run python get_weekly_quotes.py MSFT

clean:
	# clean generated artefacts
	$(RM) $(PROJECT)/__pycache__/ $(PROJECT)/*/__pycache__/
	$(RM) .coverage
	$(RM) .hypothesis/
	$(RM) .pytest_cache/
	$(RM) .ruff_cache/
	$(RM) public/
	$(RM) tags
	$(RM) tests/__pycache__/

distclean: clean
	# clean development environment
	$(RM) .idea/
	$(RM) .venv/
	$(RM) .vscode/
