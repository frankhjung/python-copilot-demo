"""Service to get weekly quotes from Alpha Vantage."""

# pylint: disable=too-few-public-methods

import requests

from quotes.weekly_data_service import WeeklyDataService


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

    def retrieve_weekly_data(self, symbol: str) -> dict[str, dict[str, float]]:
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
            raise RuntimeError(
                f"Error: {response.status_code} {response.reason}"
            )
        return response.json()
