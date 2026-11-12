# Source files

Put the source files here before running the code. None are included in this repository.

| Folder and file | What it is | Where to get it |
|---|---|---|
| `shiller/ie_data.xls` | Robert Shiller's monthly S&P 500 prices and dividends | https://shillerdata.com/ |
| `worldbank/CMO-Historical-Data-Monthly.xlsx` | World Bank Pink Sheet monthly commodity prices (gold) | https://www.worldbank.org/en/research/commodity-markets |
| `tsp/g-fund-rates-of-return.xls` or `.xlsx` | TSP G Fund annual returns, exported from the Rates of return page | https://www.tsp.gov/rates-return/ |
| `fred/*.csv` | Treasury yields and inflation from FRED | Run `python code/fetch_fred.py` |
| `eodhd/*_monthly.csv` | Month-end gold, S&P 500 index, SPY and VUSTX (optional; licensed) | Run `python code/fetch_eodhd.py` with your own `EODHD_API_KEY` |

Without the EODHD files, the main test still runs. The month-end and VUSTX checks are skipped, and stock returns for July to October 2026 use Shiller's price with the last known dividend carried forward.

## Validation inputs and provenance

The November 12 rerun uses the supplied `CMOHistoricalDataMonthly.xlsx`, copied without alteration to `worldbank/CMO-Historical-Data-Monthly.xlsx`. This workbook ends in February 2021. The following 68 months come from the public World Bank mirror at https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv, saved as `worldbank/gold_monthly_mirror.csv`. Existing workbook values are retained. The mirror is rounded to whole USD; its 734-month overlap agrees within $0.50.

The supplied November 2026 Pink Sheet is saved as `worldbank/CMO-Pink-Sheet-November-2026.pdf`. `code/check_gold_sources.py` checks 11 published figures within $1. It requires `pypdf`.

The supplied `tsp/g-fund-rates-of-return.xlsx` contains an `Annual Returns` sheet with years in column A and decimal returns in column B. Its heading cites TSP / Stock Analysis / TSP Folio. It is treated as a supplied compilation, not authenticated as a direct TSP export. Complete 1988-2025 rows are used; the YTD row is excluded. The older HTML-in-XLS export remains supported.

Run `python code/validate.py` to rebuild the backtest, walk-forward, month-end checks and SPY-tail sensitivity. The validator restores the primary SPY-tail returns after the sensitivity run. Input hashes and qualifications are saved in `results/validation.json`. Raw workbooks, PDFs and licensed EODHD prices are excluded from Git.
