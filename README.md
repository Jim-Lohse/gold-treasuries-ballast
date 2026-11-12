# Gold, Treasuries or 60/40: which did its job when it counted?

Data through October 2026. Written November 2026.

**Validation status, November 12, 2026:** The full backtest, walk-forward test, month-end checks and stock-tail sensitivity were rerun. Source qualification: the supplied World Bank workbook ends in February 2021; March 2021-October 2026 uses a documented public mirror rounded to whole dollars, checked against the workbook overlap and the uploaded November 2026 Pink Sheet. The G Fund workbook is a supplied compilation citing TSP, Stock Analysis and TSP Folio, not authenticated as a direct TSP export. See [validation report](results/validation.md).

This note is research for discussion. It is not investment advice.

© 2026 Jaime "Jim" Lohse, all rights reserved; quoted/cited third-party material belongs to its owners.

"Ballast" here means the part of a portfolio that is supposed to hold its value when stocks fall, so the owner can rebalance into stocks at lower prices.

## The question

A common ballast mix is gold plus a fund that holds Treasuries but cannot lose value, such as the G Fund in the federal Thrift Savings Plan (TSP). The question tested here is whether adding long-term Treasuries to that mix would have helped, or whether the two-part mix already did the job.

## Summary

- Across six US stock drops of 15% or more since 1972, gold plus the G Fund rose in four. It was flat in 2020 (−0.1%) and fell 2.4% in 2022.
- Adding long-term Treasuries helped a little in drops driven by recession and fear, such as 2000–03, 2007–09 and 2020. It hurt badly in 2022, the one drop driven by inflation and rising rates. In that drop the three-way mix fell 11.7%.
- In the 1973–82 inflation, gold rose 93% after inflation and long Treasuries lost 37%. In the 2021–23 inflation, everything lost ground to inflation. The G Fund lost least (−7%) and long Treasuries lost most (−28%).
- In a portfolio of 80% stocks and 20% ballast, the gold and Treasury mixes all returned between 10.3% and 11.0% a year from 1972 to 2026, less than one point apart.
- A walk-forward test chose the best mix each year using earlier-dated observations. It showed little improvement over gold plus the G Fund in this sample; the 15-year version had a slightly higher return and smaller drawdown. The input data are revised historical series, not point-in-time vintages.
- Long Treasuries provided stronger crash protection in several growth scares, but failed during the 2022 rate shock. A negative trailing correlation alone does not guarantee protection in the next crash. That relationship has changed sign before, and it has been positive since 2023. On month-end prices, its 36-month reading was 0.39 in October 2026.
- The weak spot of gold plus the G Fund is a crash in which gold falls too. That happened in 1981–82, when gold fell 34% and the mix lost 12%. Long Treasuries would have cut that loss to about 5%.

## Terms used

- Correlation: a number from −1 to 1 that measures whether two returns move together. Below zero means they tend to move in opposite directions.
- Drawdown: the fall from a previous high to a low.
- G Fund: a TSP fund that holds special-issue Treasury securities. Its value cannot fall, and its interest rate resets monthly based on the yields of longer-term Treasuries. It is open only to TSP members.
- Long Treasury: a 20-year US government bond, rebuilt here from market yields (Appendix A).
- Walk-forward test: a test that picks a mix using only past data, holds it for the next year, then repeats. It shows whether a choice that looks good in hindsight would have worked in real time.
- 60/40: 60% stocks and 40% 10-year Treasuries, used as a benchmark.

## The test, set before any results

Each holding got one written job before any data was run.

| Holding | Its job |
|---|---|
| Gold | Keep pace with inflation in high-inflation stretches, and hold its value in stock crashes |
| Long Treasury | Rise when stocks fall |
| G Fund | Never lose value in a crash |
| Cash (3-month T-bills) | Never lose value in a crash, while slowly losing to inflation |
| 60/40 | Lose less than stocks alone in crashes, while keeping most of the gain |

Every holding and mix then went through the same episodes:

- every fall in the US stock market (S&P 500 with dividends) of 15% or more, measured from peak month to bottom month;
- every stretch of six months or more in which consumer prices rose 5% or more over the prior 12 months.

Eight ballast mixes were tested inside portfolios of 90/10, 80/20 and 70/30 stocks to ballast, rebalanced monthly. The results below use 80/20 unless stated.

## Results

### Stock crashes, January 1972 to October 2026 (monthly averages)

| Crash | Stocks | Gold | Long Treasury | G Fund | Gold + G Fund | Gold + G Fund + long Treasury |
|---|---|---|---|---|---|---|
| Jan 1973 – Dec 1974 | −39.2% | 182.1% | 2.7% | 15.1% | 85.1% | 53.2% |
| Aug 1987 – Dec 1987 | −26.0% | 5.4% | 1.7% | 3.0% | 4.3% | 3.5% |
| Aug 2000 – Feb 2003 | −41.6% | 30.8% | 31.7% | 13.2% | 22.0% | 25.3% |
| Oct 2007 – Mar 2009 | −49.0% | 22.5% | 21.5% | 5.2% | 14.4% | 17.2% |
| Feb 2020 – Mar 2020 | −18.9% | −0.3% | 9.8% | 0.1% | −0.1% | 3.2% |
| Dec 2021 – Oct 2022 | −19.3% | −7.0% | −28.2% | 2.2% | −2.4% | −11.7% |

Mixes are rebalanced monthly, so a mix's return is not the simple average of its parts.

Smaller drops (10% to 15%) tell the same story, with one exception. From April 1981 to March 1982, stocks fell 13.4%, gold fell 33.5% and long Treasuries rose 11.4%. Gold plus the G Fund lost 12.3%. With long Treasuries added, the loss was 4.6%.

### Scorecard against each job

| Holding | Job | Result |
|---|---|---|
| Gold | Hold value in crashes | 4 of 6 (fell in 2020 and 2022) |
| Gold | Keep pace with inflation | 1 of 3 (passed 1973–82; failed 1990–91 and 2021–23) |
| Long Treasury | Rise when stocks fall | 5 of 6 (lost 28.2% in 2022) |
| G Fund | Never lose value in a crash | 6 of 6 |
| Cash | Never lose value in a crash | 6 of 6 |
| 60/40 | Lose less than stocks | 6 of 6; kept 84% of the stock market's yearly return (9.4% vs 11.2%) |

### High-inflation stretches, returns after inflation

| Stretch | Prices rose | Stocks | Gold | Long Treasury | G Fund | Gold + G Fund | Gold + G Fund + long Treasury |
|---|---|---|---|---|---|---|---|
| Apr 1973 – Aug 1982 | 125.1% | −33.0% | 91.8% | −36.6% | 6.7% | 56.3% | 19.5% |
| Aug 1990 – Feb 1991 | 3.3% | −0.5% | −2.8% | 6.4% | 1.7% | −0.5% | 1.9% |
| Jun 2021 – Feb 2023 | 12.3% | −10.5% | −10.7% | −27.9% | −7.0% | −8.7% | −15.4% |

### Whole portfolio, 80% stocks and 20% ballast, January 1972 to October 2026

| Ballast | Yearly return | Worst drawdown |
|---|---|---|
| Gold + G Fund | 10.7% | −39.5% |
| Gold + G Fund + long Treasury | 10.6% | −39.2% |
| Gold + long Treasury | 10.7% | −38.5% |
| Gold + 5-year Treasury | 10.6% | −38.9% |
| G Fund only | 10.3% | −40.6% |
| Gold only | 11.0% | −38.4% |
| Long Treasury only | 10.4% | −38.7% |
| Cash only | 9.9% | −41.0% |
| 100% stocks | 11.2% | −49.0% |
| 60/40 (10-year Treasury) | 9.4% | −27.0% |

The results depend heavily on the rate cycle. Long Treasuries alone were the best ballast from October 1981 to July 2020, when rates mostly fell (11.6% a year at 80/20). They were the worst ballast in both periods when rates mostly rose: 1972–81 (5.3%) and August 2020 to October 2026 (11.4%, against 14.8% for gold plus the G Fund).

### Walk-forward test, 1987 to 2025

Each year, the test chose the mix of gold, G Fund and long Treasury (in 10% steps) with the best ratio of return to worst drawdown, using only earlier data. It held that mix for the next year.

| Approach | Yearly return | Worst drawdown |
|---|---|---|
| Re-chosen yearly, all data since 1972 | 10.2% | −39.1% |
| Re-chosen yearly, last 15 years only | 10.3% | −38.7% |
| Gold + G Fund, fixed | 10.2% | −39.5% |
| Gold + G Fund + long Treasury, fixed | 10.3% | −39.2% |
| Gold + long Treasury, fixed | 10.4% | −38.5% |

The 15-year version chased whatever had just worked. It held only long Treasuries from 1993 to 2009 and only gold from 2011 to 2023, and produced results close to the fixed mixes. Compared with fixed gold plus the G Fund, its annualized return was about 0.10 percentage point higher and its maximum drawdown about 0.8 percentage point smaller. This does not establish a robust advantage. The walk-forward test enforces chronological training windows but does not reproduce historical data-release timing or eliminate design-selection bias.

### How stocks and long Treasuries moved together

On monthly averages, the 36-month correlation of stock and long-Treasury returns was positive at every year-end from 1975 to 1997 (for example 0.47 in 1979 and 0.65 in 1990). It was negative at most year-ends from 1998 to 2021 (−0.77 in 2012 and −0.56 in 2020). On month-end prices it was 0.59 at the end of 2023, 0.69 in 2024, 0.63 in 2025 and 0.39 in October 2026.

### Check on month-end prices, February 1990 to October 2026

Monthly averages make crashes look smaller. The tests were rerun on month-end prices for the period when true month-end gold prices were available.

| Drop (month-end) | Stocks | Gold + G Fund | Gold + G Fund + long Treasury |
|---|---|---|---|
| May 1990 – Oct 1990 | −14.6% | +4.2% | +3.4% |
| Jun 1998 – Aug 1998 | −15.3% | −3.0% | −0.6% |
| Aug 2000 – Sep 2002 | −44.7% | +14.2% | +19.5% |
| Oct 2007 – Feb 2009 | −50.8% | +12.9% | +14.8% |
| Sep 2018 – Dec 2018 | −13.5% | +4.2% | +4.4% |
| Dec 2019 – Mar 2020 | −19.4% | +2.6% | +8.4% |
| Dec 2021 – Sep 2022 | −23.9% | −3.7% | −11.6% |

At 80/20, the freshly rebuilt month-end worst drawdowns were −41.4% for gold plus the G Fund and −41.2% with long Treasuries added. The regenerated average-versus-month-end comparison is in `results/check_monthend_vs_average_80_20.csv`; its prior version is archived.

## When to rerun this test

The proposed monitoring rule below is a research heuristic, not a validated trading strategy. Recent positive stock-bond correlation motivates reviewing the test if that relationship changes. The thresholds have not been tested out of sample as a timing rule.

- Check: at each quarter-end.
- Inputs: the 36-month correlation of month-end S&P 500 total returns and 20-year Treasury returns (FRED series DGS20), and the 12-month change in consumer prices (FRED series CPIAUCSL).
- Signal: two quarter-ends in a row.

| Reading | Action |
|---|---|
| Correlation above 0 | No rerun |
| Correlation 0 to −0.2, inflation under 3% | Watch; no rerun |
| Correlation below −0.2 and inflation under 3%, two quarter-ends in a row | Rerun this test |
| Inflation above 5% | Review inflation and rate-shock risk; long Treasuries lost real value in two of the three historical stretches, but gained 6.4% in 1990–91 |

The 3% inflation cut-off follows earlier work. Seydl and Manoukian (2024) put the inflation level that flips the stock-bond correlation at around 3%. Molenaar, Sénéchal, Swinkels and Wang (2024) find that inflation and real interest rates drive the correlation, and Robeco's summary of that study says it expects a negative correlation when inflation is under 3% and real rates are normal. Brixton et al. (2023) add that what matters is how uncertain inflation is relative to growth, not the level of inflation itself, so the cut-off is a simple, observable stand-in.

## How this fits earlier research

These findings line up with published work. Where they overlap, the earlier work came first.

- Gold as an inflation hedge. Erb and Harvey (2013) found that gold may hedge inflation over very long horizons, but over practical horizons they call it "an unreliable inflation hedge." The split result here, a large real gain in 1973–82 and a real loss in 2021–23, is consistent with that.
- Gold in crashes. Baur and Lucey (2010) distinguish a hedge (uncorrelated with stocks on average) from a safe haven (holds value in a market crash). They find gold acts as a safe haven for stocks but that the effect is short-lived. Baur and McDermott (2010) find gold was a strong safe haven for most developed markets at the peak of the 2008 crisis. The monthly crash windows here are a coarser view of the same question.
- The changing stock-bond relationship. Ilmanen (2003) documented that the stock-bond correlation was positive through most of the 1900s and negative in a few periods, including the years just before 2003. Campbell, Sunderam and Viceira (2017) model the changing covariance of Treasury and stock returns and note it was negative in the 2000–02 and 2007–09 downturns. Brixton et al. (2023) discuss the risk of a return to the positive correlation of the 1970s to 1990s. The 36-month readings and the rerun rule here build on that work.
- Inflation regimes. Neville et al. (2021) study how assets performed during inflation surges in the US, UK and Japan over 95 years. They report that inflation surprises have hurt both stocks and bonds. The inflation-stretch results here agree for long Treasuries.
- A closely similar practitioner study. Hamann (2026a) compares gold and long Treasuries crash by crash, finds that long bonds helped most in growth scares and failed when inflation was the problem, and reports gold's 46% fall in 1980–82. His white paper (Hamann 2026b), as summarized in that guide, finds that Treasuries protected best when stocks and bonds had moved in opposite directions over the prior three years, and offers a monthly indicator built on that idea. This note's crash comparison and its 36-month correlation rule closely parallel that work, which was published first (October 2026). This note was built without reference to it and found it during the originality search. It differs by testing a fund that cannot lose value (the G Fund), scoring each holding against a job written in advance, and adding a walk-forward test.
- Testing without hindsight. Bailey et al. (2014) show how easily a backtest can be overfit and why out-of-sample results matter. That is the reason for the walk-forward test.

## Files and how to rerun

- `code/` holds the Python scripts. `results/` holds every table above as a CSV file, plus `summary.txt` and `checks.txt`.
- Raw source data is not included. `data/raw/README.md` lists each file and where to get it.
- Download the Shiller, World Bank and TSP files listed in `data/raw/README.md` first. FRED fetching alone is insufficient. For the published SPY tail and all month-end checks, also obtain the EODHD files using your own key.
- To rerun, with Python 3.11 or later:

```
pip install -r requirements.txt
python code/fetch_fred.py        # Treasury yields and inflation from FRED
python code/fetch_eodhd.py        # requires EODHD_API_KEY; licensed data
python code/build_returns.py     # monthly returns, Jan 1972 - Oct 2026
python code/backtest.py          # crashes, inflation stretches, portfolios, walk-forward
python code/validate.py          # complete rebuild, checks, sensitivity and provenance
python -m unittest discover -s tests -v
```

## Appendix A: Method

- All returns are monthly and in US dollars, January 1972 to October 2026 (658 months). The US stopped exchanging dollars for gold in August 1971, so 1972 is the first full year after that.
- Stocks: S&P 500 monthly average price plus dividends from Robert Shiller's data through June 2026, then SPY (an S&P 500 fund) month-end total return from July to October 2026. This mixes measurement conventions. Run `python code/build_returns.py --stock-tail shiller` and rerun the backtest for a sensitivity check using monthly-average prices and the last known dividend carried forward; the completed sensitivity is in `results/check_stock_tail_sensitivity.csv`. Across 70/30, 80/20 and 90/10 portfolios, the alternate tail changes full-history CAGR by approximately 0.04-0.05 percentage points and August 2020-October 2026 CAGR by 0.31-0.42 percentage points.
- Gold: World Bank monthly average price from the supplied workbook through February 2021; a public World Bank mirror supplements the following 68 months through October 2026. The supplement is rounded to whole USD, not the exact original full-precision 2026 workbook.
- Long Treasury: a 20-year bond rebuilt each month. It is bought at par with a coupon equal to last month's yield, then repriced at this month's yield with 20 years minus one month left. Coupons are semiannual. FRED has no 20-year yield from January 1987 to September 1993, so the 30-year yield fills that gap.
- 5-year and 10-year Treasuries: rebuilt the same way from FRED's 5-year and 10-year yields.
- G Fund: earns, each month, last month's average of the 5-year, 10-year and 20-year Treasury yields, and its price never falls. This mirrors the G Fund's rule of paying a rate based on longer-term Treasury yields.
- Cash: last month's 3-month T-bill rate.
- Inflation: the Consumer Price Index for All Urban Consumers (CPIAUCSL). October 2025 has no reading, so it is filled halfway between September and November 2025.
- Mixes are rebalanced monthly. No trading costs, fees or taxes are included.
- The month-end check (February 1990 to October 2026) uses month-end gold prices, the S&P 500 month-end close plus Shiller dividends until January 1993, SPY after that, and the last daily Treasury yield of each month.

## Appendix B: Sources

Data

- [D1] Shiller, Robert J. Stock market data (ie_data.xls), downloaded November 2026. https://shillerdata.com/
- [D2] World Bank. Commodity Price Data (The Pink Sheet): supplied historical workbook updated March 2, 2021 (through February 2021), and supplied November 2026 Pink Sheet PDF. https://www.worldbank.org/en/research/commodity-markets
- [D3] Federal Reserve Bank of St. Louis, FRED: GS5, GS10, GS20, GS30, DGS5, DGS10, DGS20, DGS30, TB3MS, CPIAUCSL. https://fred.stlouisfed.org/
- [D4] EOD Historical Data (EODHD): gold month-end prices (XAUUSD), S&P 500 index (GSPC), SPY and Vanguard Long-Term Treasury Fund (VUSTX) month-end prices. Licensed data; not included in this repository.
- [D5] User-supplied G Fund XLSX compilation, labeled as of November 2026, citing TSP / Stock Analysis / TSP Folio. Complete annual rows 1988-2025 used; 2026 YTD excluded. The primary publication is: https://www.tsp.gov/rates-return/

- [D6] DataHub / datasets, public gold-price mirror (1960 onward attributed to World Bank Pink Sheet). Used only for March 2021-October 2026; values rounded to whole USD. https://github.com/datasets/gold-prices/blob/main/data/monthly.csv

Research

- [R1] Erb, C. B., and C. R. Harvey. 2013. "The Golden Dilemma." Financial Analysts Journal 69 (4): 10–42. https://doi.org/10.2469/faj.v69.n4.1
- [R2] Baur, D. G., and B. M. Lucey. 2010. "Is Gold a Hedge or a Safe Haven? An Analysis of Stocks, Bonds and Gold." The Financial Review 45 (2): 217–229. https://doi.org/10.1111/j.1540-6288.2010.00244.x
- [R3] Baur, D. G., and T. K. McDermott. 2010. "Is Gold a Safe Haven? International Evidence." Journal of Banking & Finance 34 (8): 1886–1898. https://doi.org/10.1016/j.jbankfin.2009.12.008
- [R4] Ilmanen, A. 2003. "Stock-Bond Correlations." Journal of Fixed Income 13 (2): 55–66. Citation as given in [R6].
- [R5] Campbell, J. Y., A. Sunderam, and L. M. Viceira. 2017. "Inflation Bets or Deflation Hedges? The Changing Risks of Nominal Bonds." Critical Finance Review 6 (2): 263–301. https://doi.org/10.1561/104.00000043
- [R6] Brixton, A., J. Brooks, P. Hecht, A. Ilmanen, T. Maloney, and N. McQuinn. 2023. "A Changing Stock–Bond Correlation: Drivers and Implications." The Journal of Portfolio Management 49 (4), starting page 64. https://www.pm-research.com/content/iijpormgmt/49/4/64
- [R7] Neville, H., T. Draaisma, B. Funnell, C. R. Harvey, and O. Van Hemert. 2021. "The Best Strategies for Inflationary Times." SSRN working paper. https://doi.org/10.2139/ssrn.3813202
- [R8] Bailey, D. H., J. M. Borwein, M. López de Prado, and Q. J. Zhu. 2014. "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance." Notices of the American Mathematical Society 61 (5), starting page 458. https://doi.org/10.1090/noti1105
- [R9] Molenaar, R., E. Sénéchal, L. Swinkels, and Z. Wang. 2024. "Empirical Evidence on the Stock–Bond Correlation." Financial Analysts Journal 80 (3): 17–36. https://doi.org/10.1080/0015198X.2024.2317333. Summary used: Robeco, "New research into the stock-bond correlation shows when they correlate – and when they don't," April 30, 2024. https://www.robeco.com/en-uk/insights/2024/05/new-research-into-the-stock-bond-correlation-shows-when-they-correlate-and-when-they-don-t
- [R10] Seydl, J., and J. Manoukian. 2024. "Bonds may play a renewed role in portfolios – are you ready?" J.P. Morgan Private Bank, March 11, 2024. https://privatebank.jpmorgan.com/nam/en/insights/markets-and-investing/ideas-and-insights/bonds-may-play-a-renewed-role-in-portfolios-are-you-ready
- [R11] Hamann, H. 2026a. "Gold vs bonds: which protects a portfolio better in a crash?" InvestWealth.com, October 18, 2026 (updated November 11, 2026). https://www.investwealth.com/learn/guides/gold-vs-bonds
- [R12] Hamann, H. 2026b. "When Bonds Stop Hedging: 150 Years of Stock–Bond Correlation Regimes." InvestWealth White Paper No. 1, version 1.2. https://doi.org/10.5281/zenodo.23588001 (full paper not reviewed; findings cited as summarized in [R11])

## Appendix C: Checks and limits

Checks

- Original-output reconciliation: the prior 80/20 cash-ballast CAGR was 9.9741%, matching the carried-dividend Shiller-tail sensitivity; the documented SPY-tail rerun is 9.9338%. This supports a stock-tail mismatch between the old narrative and outputs. All main tables now use the documented SPY tail consistently. Small gold differences also reflect the older workbook vintage and rounded supplemental series.

- Shiller data: the original file was compared with an earlier public copy. Prices matched in 666 of 669 months (January 1971 to September 2026), and dividends matched in all 630 months the copy covers (to June 2023). The test uses the original file.
- Gold: the supplied workbook has 734 overlapping months with the mirror, January 1960-February 2021. All agree within $0.50 per ounce, consistent with the mirror's whole-dollar rounding. The workbook values are retained. Eleven annual, quarterly and monthly figures in the uploaded November 2026 Pink Sheet match the reconstructed series within $1 (maximum $0.67). The supplement is therefore cross-checked but remains a third-party copy with less precision.
- G Fund rebuild against the supplied annual-return workbook, 1988-2025 (38 complete years): average absolute gap 0.10 percentage points; largest gap 0.33 points (2011); correlation 0.998. The reference compounds to 445.6% and the rebuild to 448.7%. The supplied workbook cites TSP / Stock Analysis / TSP Folio, so this compares the model with the supplied compilation; it does not authenticate it as a direct TSP export. The 2026 YTD row is excluded.
- Long Treasury rebuild against VUSTX, February 1990 to October 2026 (441 months, month-end): correlation 0.987; yearly return 5.57% for the rebuild vs 5.45% for the fund. In crash windows the two were within about one point, except 2022, when the fund lost 28.7% and the rebuild 26.0%. The rebuild therefore makes long Treasuries look slightly better than the fund did in a rate shock.
- Stocks: the fresh check compares compound annual growth rates over 405 overlapping months through October 2026. The S&P 500 index plus estimated dividends exceeded SPY by 0.07 percentage points a year. This replaces the previously stated 0.22%, whose calculation was not present in the original scripts.

Limits

- The main test uses monthly averages except for the disclosed SPY tail, which make crashes look smaller. For example, it shows the 2007–09 fall as −49%, against about −51% on month-end prices. Month-end gold prices were available only from 1990, so 1972 to 1989 rests on averages alone.
- Six crashes of 15% or more is a small sample.
- The test uses US stocks only. A portfolio with large international or sector-heavy holdings could behave differently.
- The G Fund is open only to TSP members. Its rebuild is a model, compared against the supplied annual-return compilation for 1988 to 2025 only.
- No trading costs, fund fees or taxes are included, except as already in SPY and VUSTX prices.

## Appendix D: How this was built

Jim Lohse directed this research. He chose the question and asked for a backtest with a walk-forward check. He approved the test design: each holding's job written down before any results, the same test for every option, and original sources for every figure. He obtained the original Shiller and World Bank files used to check the data. He then reviewed the month-end check, the check against a real Treasury fund, the review of earlier research and the originality search, and directed the corrections that followed. He made the editorial calls and is publishing this note.

Claude, an AI assistant made by Anthropic, was the research and coding tool. It wrote the code, pulled the data, ran the tests and checks, searched the earlier research, and drafted text under his direction.
