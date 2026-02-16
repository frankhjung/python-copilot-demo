# Migrate Project to uv and ruff

Refactor the Python copilot-demo project to use
[uv](https://docs.astral.sh/uv/) for dependency/project management
and [ruff](https://docs.astral.sh/ruff/) for linting and formatting.
This replaces pip, virtualenv, black, isort, flake8, and pylint.

> [!IMPORTANT]
> Python source code will **not** be edited in this phase. Code
> changes (e.g. fixing new ruff lint warnings) will be done in a
> follow-up task after the project builds and tests successfully.

## User Review Required

> [!WARNING]
> **pandas 1.5 → 3.0** is a major version bump. The existing code
> uses `pd.DataFrame.T`, `pd.to_datetime`, and `pd.to_numeric`,
> which should be compatible, but runtime testing is recommended.

> [!IMPORTANT]
> **pytest-html 3.2 → 4.2** changed the `--self-contained-html`
> flag to `--self-contained-html` being the default in v4. This
> may require minor CLI flag adjustments. The plan accounts for
> this by removing the now-default flag.

> [!IMPORTANT]
> The GitHub workflow will switch from the third-party
> `JamesIves/github-pages-deploy-action` to the official
> `actions/upload-pages-artifact` + `actions/deploy-pages` approach.
> This requires enabling **GitHub Pages → Source: GitHub Actions**
> in the repository settings.

---

## Proposed Changes

### pyproject.toml (project configuration)

#### [NEW] [pyproject.toml](file:///home/frank/dev/python/copilot-demo/pyproject.toml)

Centralised project configuration replacing `requirements.txt`,
`.flake8`, `.pylintrc`, `.coveragerc`, and `.bandit.yaml`.

**`[project]`** — metadata and runtime dependencies:

- `name = "copilot-demo"`, `version = "0.1.0"`
- `requires-python = ">=3.11"`
- Runtime deps: `matplotlib ~= 3.10`, `pandas ~= 3.0`,
  `Pillow ~= 12.1`, `requests ~= 2.32`

**`[dependency-groups]`** — dev-only dependencies:

- `anybadge ~= 1.16`, `bandit ~= 1.8`, `genbadge[all] ~= 1.1`,
  `pdoc ~= 16.0`, `pytest ~= 9.0`, `pytest-cov ~= 7.0`,
  `pytest-html ~= 4.2`, `ruff ~= 0.11`

**`[tool.ruff]`** — replaces flake8 + pylint + isort + black:

- `line-length = 79`
- `target-version = "py311"`
- `lint.select` = `["E", "F", "W", "I", "B", "UP", "S", "C4",
  "SIM"]`
- `lint.per-file-ignores`: `"tests/*" = ["S101"]` (allow asserts
  in tests)
- `format.quote-style = "double"`, `indent-style = "space"`

**`[tool.pytest.ini_options]`** — pytest configuration:

- `testpaths = ["tests"]`
- `addopts` with coverage and HTML report flags

**`[tool.coverage]`** — migrated from `.coveragerc`

**`[tool.bandit]`** — migrated from `.bandit.yaml`

---

### Makefile

#### [MODIFY] [Makefile](file:///home/frank/dev/python/copilot-demo/Makefile)

- Remove `PIP`, `PYTHON` variables; add `UV := uv` and
  `RUFF := uv run ruff`
- **`format`**: replace `isort` + `black` + `sort-requirements`
  with `$(RUFF) format` and `$(RUFF) check --fix --select I`
- **`lint`**: replace `flake8` + `pylint` with `$(RUFF) check`;
  keep `bandit` (ruff's `S` rules supplement but don't fully
  replace bandit's HTML reporting)
- **`test`**: use `uv run pytest`
- **`doc`**: use `uv run pdoc`; remove pylint-report commands
- **`badge`**: remove flake8/pylint badge generation (these tools
  are removed); keep pytest badge
- **`run`**: use `uv run python`
- **`clean`**: add `uv.lock` awareness; remove references to
  `.venv` manual management
- **`help`**: update instructions to use `uv sync` instead of
  `pip install`

---

### GitHub Workflow

#### [MODIFY] [python.yml](file:///home/frank/dev/python/copilot-demo/.github/workflows/python.yml)

- Update `permissions` to include `pages: write`,
  `id-token: write`
- **Checkout**: `actions/checkout@v6`
- **Setup uv**: `astral-sh/setup-uv@v7` (replaces
  `actions/setup-python@v3`)
- **Install**: `uv sync` (replaces `pip install`)
- **Check**: `uv run ruff check` and `uv run ruff format --check`
- **Tests**: `uv run pytest ...`
- **Docs**: `uv run pdoc ...`
- **Publish**: Replace `JamesIves/github-pages-deploy-action@v4`
  with `actions/upload-pages-artifact@v3` +
  `actions/deploy-pages@v4` (official GitHub Pages deployment)

---

### GitLab Pipeline

#### [MODIFY] [.gitlab-ci.yml](file:///home/frank/dev/python/copilot-demo/.gitlab-ci.yml)

- Update image to `python:3.13-slim`
- Replace `pip install virtualenv` / `pip install -r
  requirements.txt` with:

  ```bash
  pip install uv
  uv sync
  ```

- Replace `isort`, `black`, `sort-requirements`, `flake8`,
  `pylint` commands with `uv run ruff check` and
  `uv run ruff format --check`
- Update test/doc/badge commands to use `uv run`
- Remove pylint-report and flake8 badge steps

---

### Cleanup — Remove Obsolete Files

#### [DELETE] [.flake8](file:///home/frank/dev/python/copilot-demo/.flake8)

#### [DELETE] [.pylintrc](file:///home/frank/dev/python/copilot-demo/.pylintrc)

#### [DELETE] [.coveragerc](file:///home/frank/dev/python/copilot-demo/.coveragerc)

#### [DELETE] [.bandit.yaml](file:///home/frank/dev/python/copilot-demo/.bandit.yaml)

#### [DELETE] [requirements.txt](file:///home/frank/dev/python/copilot-demo/requirements.txt)

#### [MODIFY] [.gitignore](file:///home/frank/dev/python/copilot-demo/.gitignore)

- Add `uv.lock` (optional — or track it; uv recommends tracking)
- Keep `.venv/` (uv creates `.venv` automatically)

---

## Verification Plan

### Automated Tests

1. **uv sync** — run `uv sync` to confirm all dependencies
   resolve and install correctly:

   ```bash
   cd /home/frank/dev/python/copilot-demo && uv sync
   ```

2. **ruff check** — run ruff to verify it loads config from
   `pyproject.toml`:

   ```bash
   cd /home/frank/dev/python/copilot-demo && uv run ruff check
   ```

3. **ruff format** — verify formatting check works:

   ```bash
   cd /home/frank/dev/python/copilot-demo \
     && uv run ruff format --check
   ```

4. **pytest** — run unit tests:

   ```bash
   cd /home/frank/dev/python/copilot-demo \
     && uv run pytest --verbose
   ```

5. **make targets** — verify key Makefile targets work:

   ```bash
   cd /home/frank/dev/python/copilot-demo && make lint
   cd /home/frank/dev/python/copilot-demo && make test
   ```

### Manual Verification

- Push to a feature branch and verify both GitHub and GitLab
  pipelines pass.
- Confirm GitHub Pages deploys correctly under the new
  `actions/deploy-pages` approach (requires enabling
  **Settings → Pages → Source: GitHub Actions** in the repository).
