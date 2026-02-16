#!/usr/bin/env python3

"""Retrieve and plot weekly quotes for stock using Alpha Vantage API."""

import os
import sys

import quotes.alpha_vantage_service as avs
import quotes.weekly_quotes as wq


def main() -> None:
    """Retrieve, display, and plot weekly stock quotes."""
    if len(sys.argv) != 2:
        print(
            f"Usage: {os.path.basename(__file__)} SYMBOL",
            file=sys.stderr,
        )
        sys.exit(0)

    symbol = sys.argv[1]

    key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if key is None:
        print(
            "Error: ALPHAVANTAGE_API_KEY not set",
            file=sys.stderr,
        )
        sys.exit(1)

    # retrieve → extract → convert → display
    service = avs.AlphaVantageService(key)
    data = service.retrieve_weekly_data(symbol)
    quotes = wq.WeeklyQuotes(data)
    print(quotes.as_dataframe())
    quotes.plot(symbol)


if __name__ == "__main__":
    main()
