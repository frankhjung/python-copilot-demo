"""Retrieve weekly quotes and plot."""

from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

COLUMNS = ["open", "high", "low", "close", "volume"]


def extract_weekly_series(
    data: dict[str, Any],
) -> dict[str, dict[str, float]]:
    """Extract the weekly time series from API response data.

    Parameters
    ----------
    data : dict[str, dict[str, float]]
        The raw API response dictionary.

    Returns
    -------
    dict[str, dict[str, float]]
        The weekly time series dictionary.

    """
    return data["Weekly Time Series"]


def to_dataframe(
    series: dict[str, dict[str, float]],
) -> pd.DataFrame:
    """Convert a weekly time series dictionary to a DataFrame.

    Parameters
    ----------
    series : dict[str, dict[str, float]]
        A dictionary keyed by date string with OHLCV values.

    Returns
    -------
    pd.DataFrame
        The dataframe with datetime index and numeric columns.

    """
    df = pd.DataFrame(series).T
    df.index = pd.to_datetime(df.index)  # type: ignore[assignment]
    df.columns = pd.Index(COLUMNS)
    return df.apply(pd.to_numeric)


def plot_quotes(df: pd.DataFrame, symbol: str) -> None:
    """Plot weekly closing prices.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of weekly quotes.
    symbol : str
        A stock symbol to add to the plot title.

    """
    df["close"].plot()
    plt.title(f"Weekly Quotes for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.show()


class WeeklyQuotes:
    """Container for weekly quotes with conversion and plotting.

    Composes the pure functions above for convenience.
    """

    def __init__(
        self,
        data: dict[str, Any],
    ) -> None:
        """Initialise from raw API response data."""
        self.quotes = extract_weekly_series(data)
        self.quotes_df = to_dataframe(self.quotes)

    def as_dataframe(self) -> pd.DataFrame:
        """Return the weekly quotes as a DataFrame.

        Returns
        -------
        pd.DataFrame
            The dataframe representation of the weekly quotes.

        """
        return self.quotes_df

    def plot(self, symbol: str) -> None:
        """Plot weekly closing prices.

        Parameters
        ----------
        symbol : str
            A stock symbol to add to the plot title.

        """
        plot_quotes(self.quotes_df, symbol)
