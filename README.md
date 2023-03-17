# Read Stock Quotes Example

Use GitHub Copilot to write a small Python program to demonstrate how to read
stock quotes using the [Alpha Vantage](https://www.alphavantage.co/) API.

## Method

- get stock symbol from command line argument
- read `ALPHAVANTAGE_API_KEY` from environment variable
- call Alpha Vantage API to get stock quotes
- store stock quotes to a Pandas dataframe
- print dataframe to console
- plot stock quotes to a chart (closing price / date) using Matplotlib

## Example

```bash
./get_weekly_quotes.py MSFT
               open    high     low   close       volume
1999-11-12   84.810   90.75   84.37   89.19  270831600.0
1999-11-19   88.250   88.50   84.37   86.00  147891900.0
1999-11-26   89.620   93.37   88.37   91.12  121834600.0
1999-12-03   90.120   97.12   89.50   96.12  142022200.0
1999-12-10   95.250   97.19   91.44   93.87  115003700.0
...             ...     ...     ...     ...          ...
2023-02-10  257.440  276.76  254.78  263.10  196239002.0
2023-02-17  267.640  274.97  256.00  258.06  170244679.0
2023-02-24  254.480  256.84  248.10  249.22  105098500.0
2023-03-03  252.460  255.62  245.61  255.29  126840033.0
2023-03-10  256.425  260.12  247.60  248.59  117910562.0

[1218 rows x 5 columns]
```

## MSFT Stock Quote

![Alpha Vantage MSFT](./msft-alpha-vantage.png)

Compare with Google Finance:

![Google Finance MSFT](./msft-google-finance.png)

## Resources

* [Alpha Vantage API](https://www.alphavantage.co/documentation/)
* [Pandas](https://pandas.pydata.org/)
* [Python](https://python.org)
* [Matplotlib](https://matplotlib.org/)

## Other Tools

* [GitHub Copilot Labs](https://githubnext.com/projects/copilot-labs) provides
  additional Copilot features, including explain code, translate code, and write
  unit tests

* [OpenAI playground](https://platform.openai.com/playground) is a research
  project to experiment with different pre-trained AI models developed by OpenAI
  in natural language processing (NLP), computer vision, and other AI domains
