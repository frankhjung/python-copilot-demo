#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Get weekly quotes from Alpha Vantage API.
"""

import os
import sys
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import requests


def get_alphavantage_key() -> str:
    """Get the Alpha Vantage API key from the environment variables.
    The key is used to access the Alpha Vantage API.

    Returns:
        Alpha Vantage API key
    """
    try:
        key = os.environ["ALPHAVANTAGE_API_KEY"]
    except KeyError:
        print("ALPHAVANTAGE_API_KEY not found in environment variables")
        sys.exit(1)
    return key


def get_weekly_quotes(key: str, symbol: str) -> dict[Any, Any]:
    """Get weekly quotes from Alpha Vantage API

    Args:
        key: Alpha Vantage API key
        symbol: Stock symbol

    Returns:
        A dictionary of quotes for symbol
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": symbol,
        "apikey": key,
    }
    response = requests.get(url, params=params, timeout=5)  # 5 second timeout
    if response.status_code != 200:
        print(f"Error: status code {response.status_code}")
        sys.exit(1)
    return response.json()


def convert_to_dataframe(quotes: dict[Any, Any]) -> pd.DataFrame:
    """Convert a list of quotes to a pandas DataFrame

    Args:
        quotes: A list of quotes to be converted

    Returns:
        A Pandas DataFrame
    """
    # get data
    data = quotes["Weekly Time Series"]
    # convert to dataframe
    df = pd.DataFrame(data).T
    # set index to datetime
    df.index = pd.to_datetime(df.index)
    # rename columns
    df.columns = ["open", "high", "low", "close", "volume"]
    # convert columns to floating numeric types
    df = df.astype(float)
    # sort by index date
    df = df.sort_index()
    return df


def plot_weekly_quotes(symbol: str, df: pd.DataFrame):
    """Plot closing price by date.

    Args:
        symbol: Stock symbol
        df: Dataframe containing the stock history for symbol
    """
    df["close"].plot()
    # label title with symbol
    plt.title(f"{symbol} Weekly Closing Price")
    # label axes
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.show()


def main():
    """Get weekly quotes from Alpha Vantage API.

    Usage: get_weekly_quotes.py <symbol>

    Args:
        symbol: Stock symbol

    Environment Variables:
        ALPHAVANTAGE_API_KEY: Alpha Vantage API key
    """
    # check command line arguments
    if len(sys.argv) != 2:
        print("Usage: get_weekly_quotes.py <symbol>")
        sys.exit(1)
    # get symbol from command line
    symbol = sys.argv[1]
    # read alpha key from environment variable
    key = get_alphavantage_key()
    # get weekly quotes
    quotes = get_weekly_quotes(key, symbol)
    # convert to dataframe
    df = convert_to_dataframe(quotes)
    print(df)
    # plot
    plot_weekly_quotes(symbol, df)


if __name__ == "__main__":
    main()
