"""Get weekly quotes for a symbol using Alpha Vantage API."""
# pylint: disable=too-few-public-methods

from typing import Dict

import requests

from library.weekly_data_service import WeeklyDataService


class AlphaVantageService(WeeklyDataService):
    """An implementation of the weekly data service."""

    def __init__(self, key: str) -> None:
        """
        Parameters
        ----------
        key : str
            The Alpha Vantage API key.
        """
        self.key = key

    def get_weekly_data(self, symbol: str) -> Dict[str, Dict[str, float]]:
        """
        Get weekly quotes for a symbol using Alpha Vantage API.

        Parameters
        ----------
        symbol : str
            A stock symbol (e.g., MSFT).

        Returns
        -------
        Dict[str, Dict[str, float]]
            A dictionary with the weekly quotes for the symbol.
        """
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_WEEKLY",
            "symbol": symbol,
            "apikey": self.key,
        }
        response = requests.get(url, params=params, timeout=5)
        if not response.ok:
            raise RuntimeError(f"Error: {response.status_code}")
        return response.json()
