#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Get weekly quotes from Alpha Vantage API.
"""

import sys

import library.weekly_quotes as wq


def main() -> None:
    """Main function."""
    # check command line arguments
    if len(sys.argv) != 2:
        print("Usage: get_weekly_quotes.py SYMBOL")
        sys.exit(1)
    # get symbol from command line
    symbol = sys.argv[1]
    # get API key
    try:
        key = wq.get_alphavantage_key()
    except KeyError:
        print("Error: API key not set")
        sys.exit(1)
    # retrieve weekly quotes from Alpha Vantage API
    data = wq.get_weekly_data(symbol, key)
    # get weekly quotes
    weekly_quotes = wq.get_weekly_quotes(data)
    # convert to dataframe
    quotes_df = wq.convert_to_dataframe(weekly_quotes)
    print(quotes_df)
    # plot weekly quotes
    wq.plot_weekly_quotes(symbol, quotes_df)


if __name__ == "__main__":
    main()
