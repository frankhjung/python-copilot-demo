# Migrate Project to uv and ruff

## 1. Create `pyproject.toml`

- [x] Add `[project]` metadata, dependencies, and dev groups
- [x] Add `[tool.ruff]` (replaces flake8, pylint, isort, black)
- [x] Add `[tool.pytest.ini_options]`, `[tool.coverage]`,
      `[tool.bandit]`

## 2. Update `Makefile`

- [x] Replace pip/virtualenv/black/isort/flake8/pylint with
      uv and ruff
- [x] Add ruff badge, remove flake8/pylint badges
- [x] Update help text

## 3. Update GitHub workflow

- [x] Use `actions/checkout@v6`, `astral-sh/setup-uv@v7`
- [x] Use `actions/upload-pages-artifact@v3` +
      `actions/deploy-pages@v4`
- [x] Replace pip/black/isort/flake8/pylint with uv/ruff

## 4. Update GitLab pipeline

- [x] Replace pip/virtualenv with uv, use Python 3.13
- [x] Replace old linters with ruff, add ruff badge

## 5. Update dependencies

- [x] All deps updated to latest versions in `pyproject.toml`
- [x] Removed obsolete deps (black, isort, flake8, pylint, etc.)

## 6. Cleanup

- [x] Removed `.flake8`, `.pylintrc`, `.coveragerc`,
      `.bandit.yaml`, `requirements.txt`
- [x] Updated `.gitignore` (added `.ruff_cache/`)
- [x] Updated `README.md` with quick start guide

## Verification

- [x] `uv sync` — 46 packages installed successfully
- [x] `ruff format --check` — passes (4 files formatted)
- [x] `pytest` — 1/1 test passes
- [x] `ruff check` — 10 lint warnings (UP035/UP006: deprecated
      `typing.Dict`), deferred to Python code phase
