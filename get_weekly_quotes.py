#!/usr/bin/env python3
# pylint: disable=invalid-name

"""
Get weekly quotes from Alpha Vantage API.
"""

import sys

import library.alphavantage_quotes as aq


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
        key = aq.get_alphavantage_key()
    except KeyError:
        print(f"Error: {aq.API_KEY} not set")
        sys.exit(1)
    # retrieve weekly quotes from Alpha Vantage API
    data = aq.get_weekly_data(symbol, key)
    # get weekly quotes and convert to dataframe
    weekly_quotes = aq.get_weekly_quotes(data)
    quotes_df = aq.weekly_to_dataframe(weekly_quotes)
    print(quotes_df)
    # plot weekly quotes
    aq.plot_weekly_quotes(symbol, quotes_df)


if __name__ == "__main__":
    main()
