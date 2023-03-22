"""Get weekly quotes for a symbol using Alpha Vantage API."""
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod
from typing import Dict


class WeeklyDataService(ABC):
    """
    An interface for getting weekly data.

    Raises
    ------
    RuntimeError
        If the API call fails.
    """

    @abstractmethod
    def get_weekly_data(self, symbol: str) -> Dict[str, Dict[str, float]]:
        """
        Abstract class to get weekly quotes for a symbol.

        Parameters
        ----------
        symbol : str
            A stock symbol (e.g., MSFT).

        Returns
        -------
        Dict[str, Dict[str, float]]
            A dictionary with the weekly quotes for the symbol.
        """
        raise NotImplementedError
