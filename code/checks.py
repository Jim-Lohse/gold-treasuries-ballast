"""Step 3: checks.
- G Fund model vs the TSP's own published annual returns (always runs).
- Month-end rerun, Feb 1990 - Oct 2026, and long Treasury model vs VUSTX
  (run only if the EODHD files from fetch_eodhd.py are present).
Writes CSVs and checks.txt to results/."""
import re, html
import numpy as np
import pandas as pd
from common import (RAW, WORK, RESULTS, SLEEVES, read_fred, month_end, par_bond_return,
                    stats, sleeve_return, portfolio_return, window_return, find_drops, pct)

r = pd.read_csv(WORK / "returns.csv", index_col=0, parse_dates=True)
lines = []

# G Fund model vs TSP export (tsp.gov "Rates of return", G Fund, annual; saved as .xls, which is HTML inside)
text = (RAW / "tsp" / "g-fund-rates-of-return.xls").read_text(encoding="utf-8-sig")
cells = [[html.unescape(re.sub("<.*?>", "", c)).strip() for c in re.findall(r"<t[dh].*?>(.*?)</t[dh]>", row, re.S)]
         for row in re.findall(r"<tr.*?>(.*?)</tr>", text, re.S)]
tsp = pd.Series({int(a[4:]): float(b) / 100 for a, b in cells[1:] if a.startswith("Dec")})
model = (1 + r["gfund"]).groupby(r.index.year).prod() - 1
g = pd.DataFrame({"tsp": tsp, "model": model.reindex(tsp.index)})
g["gap"] = g["model"] - g["tsp"]
g.to_csv(RESULTS / "check_gfund_vs_tsp.csv", index_label="year")
lines.append(f"G FUND MODEL VS TSP, {g.index.min()}-{g.index.max()} ({len(g)} years): "
             f"average gap {g.gap.abs().mean()*100:.2f} points, largest {g.gap.abs().max()*100:.2f} ({g.gap.abs().idxmax()}), "
             f"correlation {g.tsp.corr(g.model):.3f}; compounded TSP {((1+g.tsp).prod()-1)*100:.1f}% vs model {((1+g.model).prod()-1)*100:.1f}%")

eod = RAW / "eodhd"
if (eod / "XAUUSD.FOREX_monthly.csv").exists():
    def eod_series(name, col="adjusted_close"):
        s = pd.read_csv(eod / f"{name}_monthly.csv", parse_dates=["date"])
        s.index = s["date"].dt.to_period("M").dt.to_timestamp()
        s = s[col].astype(float)
        return s[~s.index.duplicated(keep="last")].sort_index()

    d20, d30, d10, d5 = (month_end(read_fred(s)) for s in ("DGS20", "DGS30", "DGS10", "DGS5"))
    lt = d20.reindex(d10.index)
    lt[lt.isna()] = d30.reindex(lt.index)[lt.isna()]
    me = pd.DataFrame(index=d10.index)
    me["lt_treas"] = par_bond_return(lt, 20)
    me["t10"] = par_bond_return(d10, 10)
    me["gfund"] = ((d5 + d10 + lt) / 3).shift(1) / 100 / 12
    me["cash"], me["infl"] = r["cash"].reindex(me.index), r["infl"].reindex(me.index)
    me["gold"] = eod_series("XAUUSD.FOREX", "close").pct_change()
    # stocks: S&P 500 month-end close + Shiller dividend/12 until Jan 1993, SPY total return after
    from build_returns import load_shiller
    gspc = eod_series("GSPC.INDX", "close")
    div = load_shiller()["D"].reindex(gspc.index).ffill()
    stocks = (gspc + div / 12) / gspc.shift(1) - 1
    spy = eod_series("SPY.US").pct_change().dropna()
    stocks.loc[spy.index] = spy
    me["stocks"] = stocks
    me = me.loc["1990-02-01":"2026-10-01"]
    me.to_csv(WORK / "returns_monthend.csv")

    rows = []
    for peak, bottom, depth in find_drops(me["stocks"], -0.10):
        row = {"peak": f"{peak:%Y-%m}", "bottom": f"{bottom:%Y-%m}", "stocks": depth}
        for n in ["Gold + G Fund", "Gold + G Fund + long Treasury", "Gold + long Treasury"]:
            row[n] = window_return(sleeve_return(me, SLEEVES[n]), peak, bottom)
        rows.append(row)
    drops = pd.DataFrame(rows)
    drops.to_csv(RESULTS / "check_monthend_drops.csv", index=False)
    lines.append("\nMONTH-END PRICES, STOCK FALLS OF 10%+, FEB 1990 - OCT 2026 (%)\n"
                 + pct(drops, list(drops.columns[2:])).to_string(index=False))

    avg = r.loc[me.index]
    rows = []
    for n in ["Gold + G Fund", "Gold + G Fund + long Treasury", "Gold + long Treasury", "G Fund only", "Gold only", "Long Treasury only"]:
        a, m = stats(portfolio_return(avg, SLEEVES[n], 0.8), avg["infl"]), stats(portfolio_return(me, SLEEVES[n], 0.8), me["infl"])
        rows.append({"ballast": n, "avg_yearly_return": a["yearly_return"], "avg_worst_drawdown": a["worst_drawdown"],
                     "monthend_yearly_return": m["yearly_return"], "monthend_worst_drawdown": m["worst_drawdown"]})
    cmp_ = pd.DataFrame(rows)
    cmp_.to_csv(RESULTS / "check_monthend_vs_average_80_20.csv", index=False)
    lines.append("\nWHOLE PORTFOLIO 80/20, AVERAGE VS MONTH-END PRICES, FEB 1990 - OCT 2026 (%)\n"
                 + pct(cmp_, list(cmp_.columns[1:])).to_string(index=False))

    corr = me["stocks"].rolling(36).corr(me["lt_treas"])
    corr.rename("corr_36m").to_csv(RESULTS / "stock_longtreasury_corr36_monthend.csv")
    lines.append(f"\nMONTH-END 36-MONTH STOCK / LONG-TREASURY CORRELATION, latest ({corr.index[-1]:%b %Y}): {corr.iloc[-1]:.2f}; "
                 "year-ends: " + ", ".join(f"{y} {v:.2f}" for y, v in corr.groupby(corr.index.year).last().loc[2021:].items()))

    v = eod_series("VUSTX.US").pct_change()
    j = pd.concat([v.rename("vustx"), me["lt_treas"].rename("model")], axis=1, sort=True).dropna()
    yrs = len(j) / 12
    lines.append(f"\nLONG TREASURY MODEL VS VUSTX, {j.index.min():%b %Y}-{j.index.max():%b %Y} ({len(j)} months): "
                 f"correlation {j.corr().iloc[0,1]:.3f}; yearly return VUSTX {((1+j.vustx).prod()**(1/yrs)-1)*100:.2f}% vs model {((1+j.model).prod()**(1/yrs)-1)*100:.2f}%")
    for a, b in [("1998-06", "1998-08"), ("2000-08", "2002-09"), ("2007-10", "2009-02"), ("2019-12", "2020-03"), ("2021-12", "2022-09")]:
        lines.append(f"  {a} to {b}: VUSTX {window_return(j.vustx, a, b)*100:+.1f}% / model {window_return(j.model, a, b)*100:+.1f}%")
else:
    lines.append("\nMonth-end and VUSTX checks skipped: no EODHD files in data/raw/eodhd (see fetch_eodhd.py).")

(RESULTS / "checks.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
