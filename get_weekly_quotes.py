#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Get weekly quotes from Alpha Vantage API.
"""

import os
import sys

import library.alpha_vantage_service as avs
import library.weekly_quotes as wq


def main() -> None:
    """Main function."""
    # check command line arguments
    if len(sys.argv) != 2:
        print("Usage: get_weekly_quotes.py SYMBOL")
        sys.exit(0)
    # get symbol from command line
    symbol = sys.argv[1]
    # get API key from environment
    try:
        key = os.environ["ALPHAVANTAGE_API_KEY"]
    except KeyError:
        print("Error: ALPHAVANTAGE_API_KEY not set")
        sys.exit(1)
    # get weekly quotes
    service = avs.AlphaVantageService(key)
    data = service.get_weekly_data(symbol)
    # load data into WeeklyQuotes object
    quotes = wq.WeeklyQuotes(data)
    # print quotes dataframe
    print(quotes.weekly_to_dataframe())
    # plot quotes
    quotes.plot(symbol)


if __name__ == "__main__":
    main()
