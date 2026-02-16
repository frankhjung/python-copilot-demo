"""Test weekly quotes module."""

from typing import Any

import pandas as pd
import pytest

import quotes.weekly_quotes as wq


@pytest.fixture(scope="module", name="mock_quotes")
def fixture_mock_quotes() -> dict[str, Any]:
    """Fixture: Mock weekly quotes."""
    return {
        "Meta Data": {
            "1. Information": (
                "Weekly Prices (open, high, low, close) and Volumes"
            ),
            "2. Symbol": "MSFT",
            "3. Last Refreshed": "2023-03-21",
            "4. Time Zone": "US/Eastern",
        },
        "Weekly Time Series": {
            "2021-02-07": {
                "1. open": 1.0,
                "2. high": 2.0,
                "3. low": 3.0,
                "4. close": 4.0,
                "5. volume": 100.0,
            },
            "2021-02-14": {
                "1. open": 5.0,
                "2. high": 6.0,
                "3. low": 7.0,
                "4. close": 8.0,
                "5. volume": 100.0,
            },
        },
    }


@pytest.fixture(scope="module", name="expected_df")
def fixture_expected_df() -> pd.DataFrame:
    """Fixture: Mock dataframe with weekly quotes."""
    data = [
        [1.0, 2.0, 3.0, 4.0, 100.0],
        [5.0, 6.0, 7.0, 8.0, 100.0],
    ]
    index = pd.date_range("20210207", periods=2, freq="W")
    columns = ["open", "high", "low", "close", "volume"]
    return pd.DataFrame(data=data, index=index, columns=columns)


def test_convert_to_dataframe(
    mock_quotes: dict[str, Any],
    expected_df: pd.DataFrame,
) -> None:
    """Get weekly time series and convert to dataframe."""
    quotes = wq.WeeklyQuotes(mock_quotes)
    quotes_df = quotes.as_dataframe()
    pd.testing.assert_frame_equal(
        quotes_df,
        expected_df,
        check_like=True,
    )
