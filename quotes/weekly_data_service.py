"""Service protocol for retrieving weekly stock quotes."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class WeeklyDataService(Protocol):
    """Protocol for weekly data retrieval services.

    Implementations should raise ``RuntimeError`` if the API
    call fails.

    """

    def retrieve_weekly_data(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """Retrieve weekly quotes for a stock symbol.

        Parameters
        ----------
        symbol : str
            A stock symbol (e.g., MSFT).

        Returns
        -------
        dict[str, dict[str, float]]
            A dictionary with the weekly quotes for the symbol.

        """
        ...
