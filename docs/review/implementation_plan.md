# Fix Type Mismatch in Weekly Quotes Service

The current implementation uses `dict[str, dict[str, float]]` to type hint the raw API response from Alpha Vantage. This is incorrect because the response contains "Meta Data" (which has string values) and "Weekly Time Series" (which is the actual nested dictionary). This leads to a type mismatch in `extract_weekly_series` where indexing into the dictionary returns a type that doesn't match the function's return type hint.

## Proposed Changes

### Quotes Module

#### [MODIFY] [weekly_data_service.py](file:///home/frank/dev/python/copilot-demo/quotes/weekly_data_service.py)

- Change `retrieve_weekly_data` return type to `dict[str, Any]`.
- Add `from typing import Any` import.

#### [MODIFY] [alpha_vantage_service.py](file:///home/frank/dev/python/copilot-demo/quotes/alpha_vantage_service.py)

- Update `retrieve_weekly_data` return type to `dict[str, Any]`.
- Add `from typing import Any` import.

#### [MODIFY] [weekly_quotes.py](file:///home/frank/dev/python/copilot-demo/quotes/weekly_quotes.py)

- Update `extract_weekly_series` input type to `dict[str, Any]`.
- Update `WeeklyQuotes.__init__` input type to `dict[str, Any]`.
- Add `from typing import Any` import.

### Tests

#### [MODIFY] [test_weekly_quotes.py](file:///home/frank/dev/python/copilot-demo/tests/test_weekly_quotes.py)

- Update fixture return types and function arguments to use `dict[str, Any]` where appropriate.
- Remove now-unnecessary `# type: ignore` comments.

## Verification Plan

### Automated Tests

- Run `uv run mypy` to ensure all type errors are resolved.
- Run `uv run pytest` to ensure the logic still works as expected.

```bash
uv run mypy quotes/ get_weekly_quotes.py tests/
uv run pytest
```
