# Validation run

Run: 2026-11-12T21:23:58.971256+00:00
Status: **PARTIAL**

| Check | Outcome |
|---|---|
| Regression tests | passed |
| Compile Python modules | passed |
| Main monthly-average backtest and walk-forward | blocked |
| Fresh month-end, VUSTX and G Fund checks | passed |
| Fresh output vs previous check_monthend_drops.csv | passed |
| Fresh output vs previous stock_longtreasury_corr36_monthend.csv | passed |

## Scope and limitations

- FRED, Shiller and EODHD source files were retrieved for this validation. Source-file SHA-256 hashes are recorded in `validation.json`; source data are not redistributed.
- The original World Bank workbook could not be downloaded in the November 12 reconciliation (HTTP 403). Main 1972–2026 results and walk-forward rankings remain historical until the missing source is supplied. The prior average-versus-month-end comparison is archived.
- TSP reference source: previously committed reference; not independently verified. G Fund proxy returns are recomputed from the FRED input files.
- The month-end rebuild covers 441 complete months. VUSTX and stock/SPY comparisons are exported as monthly CSVs.
- Corrected drawdown includes starting wealth. Five regression tests cover initial losses, later peaks, real compounding, invalid inputs, flat-yield bond returns and peak-month exclusion.
- README rounding, rate-regime figures and walk-forward wording were reconciled to the historical CSVs. The inflation monitoring statement was corrected to acknowledge the positive 1990–91 long-Treasury real return.
- SPY-tail sensitivity remains pending. The chronology of walk-forward training is not evidence of point-in-time data availability.
- Bibliography, historical authorship and pre-registration claims were not independently audited.

## Fresh check log

```text
G FUND MODEL VS TSP, 2003-2025 (23 years), source: previously committed TSP reference values; original export NOT independently verified: average absolute gap 0.10 points; largest 0.33 (2011); correlation 0.995; compounded TSP 99.1% vs model 101.6%
Month-end rebuild PASSED: 441 complete months, Feb 1990-Oct 2026.

MONTH-END STOCK FALLS OF 10%+ (%)
   peak  bottom  stocks  Gold + G Fund  Gold + G Fund + long Treasury  Gold + long Treasury
1990-05 1990-10   -14.6            4.2                            3.4                   3.3
1998-06 1998-08   -15.3           -3.0                           -0.6                  -1.3
2000-08 2002-09   -44.7           14.2                           19.5                  23.7
2007-10 2009-02   -50.8           12.9                           14.8                  19.2
2018-09 2018-12   -13.5            4.2                            4.4                   6.2
2019-12 2020-03   -19.4            2.6                            8.4                  12.5
2021-12 2022-09   -23.9           -3.7                          -11.6                 -17.9
Average-versus-month-end comparison SKIPPED: main returns unavailable; old comparison removed.
Month-end 36-month correlation, Oct 2026: 0.39
VUSTX check, 441 months: correlation 0.987; CAGR fund 5.45% / model 5.57%
  1998-06 to 1998-08: VUSTX +4.3% / model +4.3%
  2000-08 to 2002-09: VUSTX +30.5% / model +29.9%
  2007-10 to 2009-02: VUSTX +15.6% / model +16.8%
  2019-12 to 2020-03: VUSTX +20.8% / model +20.6%
  2021-12 to 2022-09: VUSTX -28.7% / model -26.0%
Index plus dividends vs SPY: CAGR gap +0.07 percentage points (405 months).
```

## Reproduce

Place the original sources at the paths in `data/raw/README.md`, fetch FRED/EODHD inputs, then run:

```bash
python code/validate.py
```

Exit code 2 explicitly denotes partial validation, not a full pass.
