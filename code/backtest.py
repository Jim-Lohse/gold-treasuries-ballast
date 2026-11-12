"""Step 2: the main test on monthly averages, Jan 1972 - Oct 2026.
Crashes, inflation stretches, whole-portfolio results, rate regimes, walk-forward test and the
stock / long-Treasury correlation. Writes CSVs and summary.txt to results/."""
import numpy as np
import pandas as pd
from common import (WORK, RESULTS, SLEEVES, stats, sleeve_return, portfolio_return,
                    window_return, find_drops, pct)

r = pd.read_csv(WORK / "returns.csv", index_col=0, parse_dates=True)
infl = r["infl"]
ASSETS = ["gold", "lt_treas", "t5", "gfund", "cash"]
SHOW = ["Gold + G Fund", "Gold + G Fund + long Treasury", "Gold + long Treasury"]
lines = []


def section(title, df):
    lines.append(f"\n{title}\n" + df.to_string(index=False))


# Crashes: stock falls of 15% or more, and 10% to 15%
def crash_table(drops):
    rows = []
    for peak, bottom, depth in drops:
        row = {"peak": f"{peak:%Y-%m}", "bottom": f"{bottom:%Y-%m}", "stocks": depth,
               "inflation": window_return(infl, peak, bottom)}
        for a in ASSETS:
            row[a] = window_return(r[a], peak, bottom)
        for name, w in SLEEVES.items():
            row[name] = window_return(sleeve_return(r, w), peak, bottom)
        row["60/40"] = window_return(0.6 * r["stocks"] + 0.4 * r["t10"], peak, bottom)
        rows.append(row)
    return pd.DataFrame(rows)


big = crash_table(find_drops(r["stocks"], -0.15))
small = crash_table(find_drops(r["stocks"], -0.10, shallower_than=-0.15))
big.to_csv(RESULTS / "crashes_15pct.csv", index=False)
small.to_csv(RESULTS / "drops_10_to_15pct.csv", index=False)
num = [c for c in big.columns if c not in ("peak", "bottom")]
section("STOCK FALLS OF 15% OR MORE (%)", pct(big[["peak", "bottom", "stocks", *ASSETS, *SHOW]], ["stocks", *ASSETS, *SHOW]))
section("STOCK FALLS OF 10% TO 15% (%)", pct(small[["peak", "bottom", "stocks", *ASSETS, *SHOW]], ["stocks", *ASSETS, *SHOW]))

# Inflation stretches: CPI up 5%+ over 12 months, at least six months in a row
hot = r["cpi"].pct_change(12) >= 0.05
stretches, start, prev = [], None, None
for dt, h in hot.items():
    if h and start is None:
        start = dt
    if not h and start is not None:
        if (prev.year - start.year) * 12 + prev.month - start.month >= 5:
            stretches.append((start, prev))
        start = None
    prev = dt
if start is not None:
    stretches.append((start, prev))
rows = []
for a, b in stretches:
    s = r.loc[a:b]
    cpi_up = (1 + s["infl"]).prod() - 1
    real = lambda x: (1 + (1 + x.loc[a:b]).prod() - 1) / (1 + cpi_up) - 1
    row = {"start": f"{a:%Y-%m}", "end": f"{b:%Y-%m}", "prices_rose": cpi_up}
    for k in ["stocks", "gold", "lt_treas", "t10", "gfund", "cash"]:
        row[k] = real(r[k])
    for name, w in SLEEVES.items():
        row[name] = real(sleeve_return(r, w))
    row["60/40"] = real(0.6 * r["stocks"] + 0.4 * r["t10"])
    rows.append(row)
inf = pd.DataFrame(rows)
inf.to_csv(RESULTS / "inflation_stretches_real.csv", index=False)
cols = ["prices_rose", "stocks", "gold", "lt_treas", "gfund", *SHOW]
section("HIGH-INFLATION STRETCHES, RETURNS AFTER INFLATION (%)", pct(inf[["start", "end", *cols]], cols))

# Whole portfolio at 90/10, 80/20, 70/30
rows = []
for sw in (0.9, 0.8, 0.7):
    for name, w in SLEEVES.items():
        rows.append({"stock_weight": sw, "ballast": name, **stats(portfolio_return(r, w, sw), infl)})
rows.append({"stock_weight": 1.0, "ballast": "100% stocks", **stats(r["stocks"], infl)})
rows.append({"stock_weight": 0.6, "ballast": "60/40 (10-year Treasury)", **stats(0.6 * r["stocks"] + 0.4 * r["t10"], infl)})
port = pd.DataFrame(rows)
port.to_csv(RESULTS / "portfolio_stats.csv", index=False)
pc = ["yearly_return", "real_yearly_return", "volatility", "worst_drawdown"]
section("WHOLE PORTFOLIO, 1972-2026 (%)", pct(port, pc).round(2))

# Rate regimes at 80/20
REG = {"1972-1981 rates rising": ("1972-01", "1981-09"), "1981-2020 rates falling": ("1981-10", "2020-07"),
       "2020-2026 rates rising": ("2020-08", "2026-10")}
rows = [{"regime": k, "ballast": n, **stats(portfolio_return(r, w, 0.8).loc[a:b], infl)}
        for k, (a, b) in REG.items() for n, w in SLEEVES.items()]
reg = pd.DataFrame(rows)
reg.to_csv(RESULTS / "rate_regimes_80_20.csv", index=False)
section("RATE REGIMES, 80/20 (%)", pct(reg, pc).round(2))

# Walk-forward: each year pick the gold / G Fund / long Treasury mix (10% steps) with the best
# return-to-worst-drawdown ratio on earlier data only, hold it for the year.
GRID = [{"gold": g / 10, "gfund": f / 10, "lt_treas": (10 - g - f) / 10}
        for g in range(11) for f in range(11 - g)]
SW = 0.8


def walk_forward(lookback_years=None):
    picks, held = [], []
    for yr in range(1987, 2026):
        train = r.loc[:f"{yr - 1}-12"] if lookback_years is None else r.loc[f"{yr - lookback_years}-01":f"{yr - 1}-12"]
        best = max(GRID, key=lambda w: stats(portfolio_return(train, w, SW), infl)["return_to_drawdown"])
        picks.append({"year": yr, **best})
        held.append(portfolio_return(r.loc[f"{yr}-01":f"{yr}-12"], best, SW))
    return pd.concat(held), pd.DataFrame(picks)


wf_all, picks_all = walk_forward()
wf_15, picks_15 = walk_forward(15)
picks_all.to_csv(RESULTS / "walkforward_picks_all_history.csv", index=False)
picks_15.to_csv(RESULTS / "walkforward_picks_last15.csv", index=False)
rows = [{"approach": "Re-chosen yearly, all data since 1972", **stats(wf_all, infl)},
        {"approach": "Re-chosen yearly, last 15 years only", **stats(wf_15, infl)}]
rows += [{"approach": f"{n}, fixed", **stats(portfolio_return(r, SLEEVES[n], SW).loc[wf_all.index], infl)}
         for n in ["Gold + G Fund", "Gold + G Fund + long Treasury", "Gold + long Treasury", "G Fund only", "Gold only"]]
wf = pd.DataFrame(rows)
wf.to_csv(RESULTS / "walkforward_1987_2025.csv", index=False)
section("WALK-FORWARD 1987-2025, 80/20 (%)", pct(wf, pc).round(2))

# 36-month correlation of stock and long-Treasury returns
corr = r["stocks"].rolling(36).corr(r["lt_treas"])
corr.rename("corr_36m").to_csv(RESULTS / "stock_longtreasury_corr36_monthly_avg.csv")
ye = corr.groupby(corr.index.year).last().loc[1975:].round(2)
lines.append("\nSTOCK / LONG-TREASURY 36-MONTH CORRELATION AT YEAR-END (monthly averages)\n" + ye.to_string())

(RESULTS / "summary.txt").write_text("\n".join(lines).lstrip() + "\n")
print("\n".join(lines))
