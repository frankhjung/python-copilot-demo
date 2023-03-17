"""Test weekly_alpha_vantage module."""

import os
from typing import Dict
from unittest.mock import patch

import pandas as pd
import pytest as pt

from library.weekly_quotes import convert_to_dataframe, get_alphavantage_key


@patch.dict("os.environ", {"ALPHAVANTAGE_API_KEY": "my_api_key"})
def test_get_alphavantage_key_returns_api_key_when_set() -> None:
    """Test get_alphavantage_key()."""
    key = get_alphavantage_key()
    assert key == "my_api_key"


def test_get_alphavantage_key_returns_key_when_not_set() -> None:
    """Test get_alphavantage_key raises exception when key is not set."""
    os.environ.pop("ALPHAVANTAGE_API_KEY")
    with pt.raises(KeyError):
        get_alphavantage_key()


@pt.fixture(scope="module")
def mock_quotes() -> Dict[str, Dict[str, float]]:
    """Fixture: Mock weekly quotes."""
    return {
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
    }


@pt.fixture(scope="module")
def expected_df() -> pd.DataFrame:
    """Fixture: Mock dataframe with weekly quotes."""
    data = [[1.0, 2.0, 3.0, 4.0, 100.0], [5.0, 6.0, 7.0, 8.0, 100.0]]
    index = pd.date_range("20210207", periods=2, freq="W")
    columns = ["open", "high", "low", "close", "volume"]
    return pd.DataFrame(data=data, index=index, columns=columns)


# pylint: disable=redefined-outer-name
def test_convert_to_dataframe(
    mock_quotes: Dict[str, float], expected_df: pd.DataFrame
) -> None:
    """Test convert_to_dataframe()."""
    quotes_df = convert_to_dataframe(mock_quotes)
    assert quotes_df.equals(expected_df)
    pd.testing.assert_frame_equal(quotes_df, expected_df, check_like=True)
