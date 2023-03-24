#!/usr/bin/env python3

"""Retrieve and plot weekly quotes for stock using Alpha Vantage API."""

import os
import sys

import quotes.alpha_vantage_service as avs
import quotes.weekly_quotes as wq


def main() -> None:
    """Main function."""
    # check command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(__file__)} SYMBOL")
        # print(f"Usage: {os.path.basename(sys.argv[0])} SYMBOL")
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
    data = service.retrieve_weekly_data(symbol)
    # load data into WeeklyQuotes object
    quotes = wq.WeeklyQuotes(data)
    # print quotes dataframe
    print(quotes.as_dataframe())
    # plot quotes
    quotes.plot(symbol)


if __name__ == "__main__":
    main()
