# Code Review

Code review of the copilot-demo project after migration to
[uv](https://docs.astral.sh/uv/) and
[ruff](https://docs.astral.sh/ruff/).

## Ruff Diagnostics

Running `ruff check --select ALL` reported 34 issues across all
Python files. The key categories:

| Category | Rule | Count | Description |
|----------|------|-------|-------------|
| Docstrings | D212, D413, D104 | 12 | Formatting, missing blank lines |
| Style | COM812, RET504 | 3 | Trailing commas, unnecessary assignment |
| Type annotations | ANN204, PGH003 | 4 | Missing return type, unspecific `# type: ignore` |
| Exceptions | TRY003, EM102 | 2 | f-string in exception, long message |
| Imports | PT013 | 1 | `import pytest as pt` non-standard |
| File metadata | EXE002 | 2 | Missing shebang on non-executable files |
| Legacy | — | 2 | Stale `# pylint: disable` comments |

## Decisions

### Applied Fixes

1. **Remove stale `# pylint: disable` comments** — pylint is no
   longer used; these comments are dead code.

2. **Fix docstring typo** — `weekly_quotes.py` line 1 has
   "Retreive" → "Retrieve".

3. **Fix docstring formatting (D212, D413)** — ensure multi-line
   docstrings start on the first line after `"""` and have a blank
   line after the last section.

4. **Add missing `-> None` return type** on `WeeklyQuotes.__init__`.

5. **Replace `import pytest as pt`** with `import pytest` — the
   `pt` alias is non-standard and harms readability.

6. **Replace generic `# type: ignore`** with specific codes
   (`# type: ignore[assignment]`) or remove where unnecessary.

7. **Extract exception message to variable** (EM102) — assign
   f-string to a variable before raising.

8. **Add trailing commas** where appropriate for diff-friendliness.

### Functional Programming Improvements

1. **Decompose `WeeklyQuotes` into pure functions** — the class
   has no meaningful state beyond the initial data. Replace with:
   - `extract_weekly_series(data)` — pure function to extract
     the time series dictionary
   - `to_dataframe(series)` — pure function to convert to a
     pandas DataFrame
   - `plot_quotes(df, symbol)` — side-effecting function,
     clearly separated

2. **Refactor `main()` to use a pipeline** — compose the above
    functions: `retrieve → extract → convert → display`. Use
    `os.environ.get()` instead of try/except for cleaner flow.

3. **Replace `WeeklyDataService` ABC with a `Protocol`** — a
    `Protocol` is more Pythonic for structural subtyping and
    aligns with functional style (no inheritance needed).

4. **Use `raise` without `NotImplementedError`** in the
    protocol — protocols don't need a body.

### Not Applied (Deferred)

- **D104** (missing docstring in `tests/__init__.py`) — empty
  `__init__.py` files don't need docstrings. Added to ruff
  per-file-ignores.
- **EXE002** (missing shebang) — library modules should not be
  executable. No action needed — added to ruff ignore list.
