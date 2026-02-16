"""Retreive weekly quotes and plot."""

import matplotlib.pyplot as plt
import pandas as pd


class WeeklyQuotes:
    """Custom class to hold weekly quotes."""

    def __init__(self, data: dict[str, dict[str, float]]):
        """Initialize the class."""
        self.data = data
        self.quotes = self.get_weekly_quotes()
        self.quotes_df = self.as_dataframe()

    def get_weekly_quotes(self) -> dict[str, float]:
        """Get weekly quotes for a symbol returned by the Alpha Vantage API.

        Returns
        -------
        Dict[str, float]
            A dictionary with the weekly quotes for the symbol.
        """
        return self.data["Weekly Time Series"]

    def as_dataframe(self) -> pd.DataFrame:
        """Convert a dictionary of weekly quotes into a pandas dataframe.

        Returns
        -------
        pandas.DataFrame
            The dataframe representation of the weekly quotes.
        """
        quotes_df = pd.DataFrame(self.quotes).T
        quotes_df.index = pd.to_datetime(quotes_df.index)  # type: ignore
        quotes_df.columns = ["open", "high", "low", "close", "volume"]
        quotes_df = quotes_df.apply(pd.to_numeric)
        return quotes_df

    def plot(self, symbol: str) -> None:
        """Plot weekly quotes.

        Parameters
        ----------
        symbol : str
            A stock symbol to add to plot title.
        """
        self.quotes_df["close"].plot()
        plt.title(f"Weekly Quotes for {symbol}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price (USD)")
        plt.show()
