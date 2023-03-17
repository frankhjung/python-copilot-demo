"""Get weekly quotes for a symbol using Alpha Vantage API."""

import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import requests


def get_alphavantage_key() -> str:
    """
    Read the AlphaVantage API key from the environment variable.

    Returns
    -------
    str
        The API key for alphavantage as a string.
    Raises
    ------
    KeyError
        If the API key is not set.
    """
    return os.environ["ALPHAVANTAGE_API_KEY"]


def get_weekly_data(symbol: str, key: str) -> Dict[str, Dict[str, float]]:
    """
    Get weekly quotes for a symbol using Alpha Vantage API.

    Parameters
    ----------
    symbol : str
        A stock symbol (e.g., MSFT).
    key : str
        The Alpha Vantage API key.

    Returns
    -------
    Dict[str, Dict[str, float]]
        A dictionary with the weekly quotes for the symbol.

    Raises
    ------
    RuntimeError
        If the API call fails.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": key,
    }
    response = requests.get(url, params=params, timeout=5)
    if not response.ok:
        raise RuntimeError(f"Error: {response.status_code}")
    return response.json()


def get_weekly_quotes(data: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Get weekly quotes for a symbol returned by the Alpha Vantage API.

    Parameters
    ----------
    Dict[str, Dict[str, float]]
        The data returned by Alpha Vantage API.

    Returns
    -------
    Dict[str, float]
        A dictionary with the weekly quotes for the symbol.
    """
    return data["Weekly Time Series"]


def convert_to_dataframe(weekly_quotes: Dict[str, float]) -> pd.DataFrame:
    """
    Convert a dictionary of weekly quotes into a pandas dataframe.

    Parameters
    ----------
    data : Dict[str, float]
        A dictionary of weekly quotes.

    Returns
    -------
    pandas.DataFrame
        The dataframe representation of the weekly quotes.
    """
    quotes_df = pd.DataFrame(weekly_quotes).T
    quotes_df.index = pd.to_datetime(quotes_df.index)
    quotes_df.columns = ["open", "high", "low", "close", "volume"]
    quotes_df = quotes_df.apply(pd.to_numeric)
    return quotes_df


def plot_weekly_quotes(symbol: str, quotes_df: pd.DataFrame) -> None:
    """Plot weekly quotes.

    Parameters
    ----------
    symbol : str
        A stock symbol.
    quotes_df : pd.DataFrame
        A DataFrame containing weekly quotes.
    """
    quotes_df["close"].plot()
    plt.title(f"Weekly Quotes for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.show()
