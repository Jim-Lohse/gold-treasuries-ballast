# Source files

Put the source files here before running the code. None are included in this repository.

| Folder and file | What it is | Where to get it |
|---|---|---|
| `shiller/ie_data.xls` | Robert Shiller's monthly S&P 500 prices and dividends | https://shillerdata.com/ |
| `worldbank/CMO-Historical-Data-Monthly.xlsx` | World Bank Pink Sheet monthly commodity prices (gold) | https://www.worldbank.org/en/research/commodity-markets |
| `tsp/g-fund-rates-of-return.xls` | TSP G Fund annual returns, exported from the Rates of return page | https://www.tsp.gov/rates-return/ |
| `fred/*.csv` | Treasury yields and inflation from FRED | Run `python code/fetch_fred.py` |
| `eodhd/*_monthly.csv` | Month-end gold, S&P 500 index, SPY and VUSTX (optional; licensed) | Run `python code/fetch_eodhd.py` with your own `EODHD_API_KEY` |

Without the EODHD files, the main test still runs. The month-end and VUSTX checks are skipped, and stock returns for July to October 2026 use Shiller's price with the last known dividend carried forward.

## Validation provenance

`results/validation.json` records hashes of input files used in the latest validation. It does not contain licensed input prices. The November 12 run retrieved fresh FRED, Shiller and EODHD inputs, but could not retrieve the original World Bank workbook. TSP comparison values were reused from the previously committed reference CSV and are explicitly labeled as such. Supplying the original TSP export allows an independent source check.

Run `python code/validate.py` after placing the required files. Exit code 2 means partial validation. The original World Bank file is required to regenerate the main backtest and walk-forward results.
