#!/usr/bin/env make

.PHONY: all clean default doc format help lint preen report run tags test update

.DEFAULT_GOAL	:= default
CTAGS		:= $(shell which ctags)
RM		:= rm -rf

PROJECT		:= quotes
SRCS		:= $(wildcard *.py $(PROJECT)/*.py tests/*.py)

all:	preen test report run ## run all checks, tests, generate reports and run the application
default: preen test ## run preen and test targets

help: ### show this help message
	@echo ""
	@echo "Default goal: ${.DEFAULT_GOAL}"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "To initialize and install dependencies managed by uv:"
	@echo ""
	@echo "  uv sync"
	@echo ""
	@echo "To run commands in the virtual environment:"
	@echo ""
	@echo "  uv run <command>"
	@echo ""
	@echo "To get weekly quotes for Microsoft:"
	@echo ""
	@echo "  uv run python get_weekly_quotes.py MSFT"
	@echo ""

preen:	format tags lint ## run format, tags, and lint targets

format: ## format and sort imports
	# format code and sort imports
	@uv run ruff format $(SRCS)
	@uv run ruff check --fix --select I $(SRCS)

tags: ## build ctags for vim
ifdef CTAGS
	# build ctags for vim
	@ctags --recurse -o tags $(SRCS)
endif

lint: ## run lint checks
	# check with ruff
	@uv run ruff check $(PROJECT)
	# security checks with bandit
	@uv run bandit --configfile pyproject.toml --recursive $(PROJECT)

test: ## run tests
	# unit tests with coverage report
	@uv run pytest --verbose --cov --cov-report=html \
	  --html=public/pytest_report.html

report:	doc ## generate documentation and security reports

doc: ## generate documentation and security reports
	# generate documentation to public directory
	# generate documentation to public directory
	@uv run pdoc --output-directory public $(PROJECT)
	@uv run bandit --configfile pyproject.toml --recursive \
	  --format html --output public/bandit_report.html $(PROJECT)

run: ## run the application
	# get quotes for microsoft
	@uv run python get_weekly_quotes.py MSFT

update: ## check for and sync package updates
	# check for outdated packages
	@uv pip list --outdated
	@uv sync --upgrade

clean: ## clean generated artefacts
	# clean generated artefacts
	$(RM) $(PROJECT)/__pycache__/ $(PROJECT)/*/__pycache__/
	$(RM) .coverage
	$(RM) .hypothesis/
	$(RM) .pytest_cache/
	$(RM) .ruff_cache/
	$(RM) public/
	$(RM) tags
	$(RM) tests/__pycache__/

distclean: clean ## clean generated artefacts and development environment
	# clean development environment
	$(RM) .idea/
	$(RM) .venv/
	$(RM) .vscode/
