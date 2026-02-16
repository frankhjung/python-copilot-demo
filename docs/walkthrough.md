# Walkthrough: Migration to uv and ruff

## Summary

Migrated the copilot-demo project from pip/virtualenv and
black/isort/flake8/pylint to
[uv](https://docs.astral.sh/uv/) +
[ruff](https://docs.astral.sh/ruff/).

## Changes Made

### New Files

| File | Purpose |
|------|---------|
| [pyproject.toml](file:///home/frank/dev/python/copilot-demo/pyproject.toml) | Centralised project config (deps, ruff, pytest, coverage, bandit) |

### Modified Files

| File | Changes |
|------|---------|
| [Makefile](file:///home/frank/dev/python/copilot-demo/Makefile) | uv/ruff commands, ruff badge, removed old tool references |
| [python.yml](file:///home/frank/dev/python/copilot-demo/.github/workflows/python.yml) | `setup-uv@v7`, `checkout@v6`, official Pages deployment |
| [.gitlab-ci.yml](file:///home/frank/dev/python/copilot-demo/.gitlab-ci.yml) | uv/ruff, Python 3.13, ruff badge |
| [.gitignore](file:///home/frank/dev/python/copilot-demo/.gitignore) | Added `.ruff_cache/` |
| [README.md](file:///home/frank/dev/python/copilot-demo/README.md) | Quick start guide, updated tool references |

### Deleted Files

`.flake8`, `.pylintrc`, `.coveragerc`, `.bandit.yaml`,
`requirements.txt`

## Dependency Upgrades

| Package | Old | New |
|---------|-----|-----|
| matplotlib | ~= 3.7 | ~= 3.10 |
| pandas | ~= 1.5 | ~= 3.0 |
| Pillow | ~= 10.3 | ~= 12.1 |
| requests | ~= 2.29 | ~= 2.32 |
| pytest | ~= 7.3 | ~= 9.0 |
| pytest-cov | ~= 4.0 | ~= 7.0 |
| pytest-html | ~= 3.2 | ~= 4.2 |
| pdoc | ~= 14.0 | ~= 16.0 |
| anybadge | ~= 1.14 | ~= 1.16 |
| bandit | ~= 1.7 | ~= 1.8 |
| **ruff** | *(new)* | ~= 0.11 |

**Removed:** black, isort, flake8, pylint, pylint-report,
pylance, sort-requirements

## Verification Results

| Check | Result |
|-------|--------|
| `uv sync` | ✅ 46 packages installed |
| `ruff format --check` | ✅ 4 files already formatted |
| `pytest --verbose` | ✅ 1/1 passed |
| `ruff check` | ⚠️ 10 warnings (UP035/UP006) |

## Outstanding Items

`ruff check` reports 10 lint warnings — all `UP035`/`UP006`
(deprecated `typing.Dict`, should use built-in `dict`). These
are auto-fixable with `ruff check --fix` and will be addressed
in the follow-up Python code phase as agreed.
