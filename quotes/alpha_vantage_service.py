"""Service to get weekly quotes from Alpha Vantage."""

from typing import Any

import requests

from quotes.weekly_data_service import WeeklyDataService


class AlphaVantageService(WeeklyDataService):
    """An implementation of the weekly data service."""

    def __init__(self, key: str) -> None:
        """Initialise with an Alpha Vantage API key.

        Parameters
        ----------
        key : str
            The Alpha Vantage API key.

        """
        self.key = key

    def retrieve_weekly_data(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Get weekly quotes for a symbol using Alpha Vantage API.

        Parameters
        ----------
        symbol : str
            A stock symbol (e.g., MSFT).

        Returns
        -------
        dict[str, dict[str, float]]
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
            msg = f"Error: {response.status_code} {response.reason}"
            raise RuntimeError(msg)
        return response.json()
