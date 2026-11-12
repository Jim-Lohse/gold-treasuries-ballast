"""Validate monthly-average models and independently rebuild month-end returns.
Missing inputs are reported explicitly. A skipped check never leaves stale output.
"""
import html
import re
import numpy as np
import pandas as pd
from common import (RAW, WORK, RESULTS, SLEEVES, read_fred, month_end,
                    par_bond_return, stats, sleeve_return, portfolio_return,
                    window_return, find_drops, pct)
from build_returns import load_shiller

lines = []
rpath = WORK / "returns.csv"
r = pd.read_csv(rpath, index_col=0, parse_dates=True) if rpath.exists() else None
cpi = read_fred("CPIAUCSL").interpolate(limit=1)
infl = cpi.pct_change(fill_method=None)
cash = read_fred("TB3MS").shift(1) / 1200

# Compute the G Fund proxy from newly fetched yields even when the gold file is missing.
y5, y10, y20, y30 = (read_fred(s) for s in ["GS5", "GS10", "GS20", "GS30"])
y20 = y20.fillna(y30.reindex(y20.index))
gmonthly = ((y5 + y10 + y20) / 3).shift(1) / 1200
text_path = RAW / "tsp" / "g-fund-rates-of-return.xls"
reference = RESULTS / "check_gfund_vs_tsp.csv"
if text_path.exists():
    text = text_path.read_text(encoding="utf-8-sig")
    cells = [[html.unescape(re.sub("<.*?>", "", c)).strip()
              for c in re.findall(r"<t[dh].*?>(.*?)</t[dh]>", row, re.S)]
             for row in re.findall(r"<tr.*?>(.*?)</tr>", text, re.S)]
    tsp = pd.Series({int(a[4:]): float(b) / 100 for a, b in cells[1:] if a.startswith("Dec")})
    source = "original TSP export"
elif reference.exists():
    tsp = pd.read_csv(reference, index_col="year")["tsp"]
    source = "previously committed TSP reference values; original export NOT independently verified"
else:
    tsp = None
    lines.append("G Fund check SKIPPED: no TSP export or committed reference.")
if tsp is not None:
    annual = (1 + gmonthly).groupby(gmonthly.index.year).prod() - 1
    counts = gmonthly.groupby(gmonthly.index.year).count()
    years = tsp.index.intersection(counts[counts == 12].index)
    g = pd.DataFrame({"tsp": tsp.loc[years], "model": annual.loc[years]})
    g["gap"] = g["model"] - g["tsp"]
    g.to_csv(reference, index_label="year")
    lines.append(f"G FUND MODEL VS TSP, {g.index.min()}-{g.index.max()} ({len(g)} years), source: {source}: "
                 f"average absolute gap {g.gap.abs().mean()*100:.2f} points; "
                 f"largest {g.gap.abs().max()*100:.2f} ({g.gap.abs().idxmax()}); "
                 f"correlation {g.tsp.corr(g.model):.3f}; "
                 f"compounded TSP {((1+g.tsp).prod()-1)*100:.1f}% vs model {((1+g.model).prod()-1)*100:.1f}%")

eod = RAW / "eodhd"
required = [eod / f"{t}_monthly.csv" for t in ["XAUUSD.FOREX", "GSPC.INDX", "SPY.US", "VUSTX.US"]]
missing = [p.name for p in required if not p.exists()]
outputs = ["check_monthend_drops.csv", "check_monthend_vs_average_80_20.csv",
           "stock_longtreasury_corr36_monthend.csv", "check_vustx.csv", "check_stock_spy.csv"]
for name in outputs:
    (RESULTS / name).unlink(missing_ok=True)
if missing:
    lines.append("Month-end/VUSTX SKIPPED: missing " + ", ".join(missing))
else:
    def eod_series(name, col="adjusted_close"):
        df = pd.read_csv(eod / f"{name}_monthly.csv", parse_dates=["date"])
        df.index = df["date"].dt.to_period("M").dt.to_timestamp()
        s = df[col].astype(float)
        if s.index.has_duplicates:
            raise ValueError(f"Duplicate months in {name}")
        return s.sort_index()

    d20, d30, d10, d5 = (month_end(read_fred(s)) for s in ["DGS20", "DGS30", "DGS10", "DGS5"])
    lt = d20.reindex(d10.index).fillna(d30.reindex(d10.index))
    me = pd.DataFrame(index=d10.index)
    me["lt_treas"] = par_bond_return(lt, 20)
    me["t10"] = par_bond_return(d10, 10)
    me["gfund"] = ((d5 + d10 + lt) / 3).shift(1) / 1200
    me["cash"], me["infl"] = cash.reindex(me.index), infl.reindex(me.index)
    me["gold"] = eod_series("XAUUSD.FOREX", "close").pct_change(fill_method=None)
    gspc = eod_series("GSPC.INDX", "close")
    div = load_shiller()["D"].reindex(gspc.index).ffill()
    index_return = (gspc + div / 12) / gspc.shift(1) - 1
    spy = eod_series("SPY.US").pct_change(fill_method=None).dropna()
    stocks = index_return.copy()
    stocks.loc[spy.index] = spy
    me["stocks"] = stocks
    me = me.reindex(pd.date_range("1990-02-01", "2026-10-01", freq="MS"))
    if not np.isfinite(me).all().all():
        raise ValueError("Month-end returns have gaps: " + str(me.isna().sum().to_dict()))
    me.to_csv(WORK / "returns_monthend.csv")
    lines.append(f"Month-end rebuild PASSED: {len(me)} complete months, Feb 1990-Oct 2026.")
    rows = []
    for peak, bottom, depth in find_drops(me["stocks"], -0.10):
        row = {"peak": f"{peak:%Y-%m}", "bottom": f"{bottom:%Y-%m}", "stocks": depth}
        for n in ["Gold + G Fund", "Gold + G Fund + long Treasury", "Gold + long Treasury"]:
            row[n] = window_return(sleeve_return(me, SLEEVES[n]), peak, bottom)
        rows.append(row)
    drops = pd.DataFrame(rows)
    drops.to_csv(RESULTS / "check_monthend_drops.csv", index=False)
    lines.append("\nMONTH-END STOCK FALLS OF 10%+ (%)\n" + pct(drops, list(drops.columns[2:])).to_string(index=False))
    if r is None:
        lines.append("Average-versus-month-end comparison SKIPPED: main returns unavailable; old comparison removed.")
    else:
        avg = r.loc[me.index]
        rows = []
        for n in ["Gold + G Fund", "Gold + G Fund + long Treasury", "Gold + long Treasury", "G Fund only", "Gold only", "Long Treasury only"]:
            a = stats(portfolio_return(avg, SLEEVES[n], .8), avg["infl"])
            m = stats(portfolio_return(me, SLEEVES[n], .8), me["infl"])
            rows.append({"ballast": n, "avg_yearly_return": a["yearly_return"], "avg_worst_drawdown": a["worst_drawdown"],
                         "monthend_yearly_return": m["yearly_return"], "monthend_worst_drawdown": m["worst_drawdown"]})
        pd.DataFrame(rows).to_csv(RESULTS / "check_monthend_vs_average_80_20.csv", index=False)
    corr = me["stocks"].rolling(36).corr(me["lt_treas"])
    corr.rename("corr_36m").to_csv(RESULTS / "stock_longtreasury_corr36_monthend.csv")
    lines.append(f"Month-end 36-month correlation, Oct 2026: {corr.iloc[-1]:.2f}")
    v = eod_series("VUSTX.US").pct_change(fill_method=None)
    j = pd.concat([v.rename("vustx"), me["lt_treas"].rename("model")], axis=1).reindex(me.index)
    if j.isna().any().any():
        raise ValueError("VUSTX comparison has missing months")
    j.to_csv(RESULTS / "check_vustx.csv")
    yrs = len(j) / 12
    lines.append(f"VUSTX check, {len(j)} months: correlation {j.corr().iloc[0,1]:.3f}; "
                 f"CAGR fund {((1+j.vustx).prod()**(1/yrs)-1)*100:.2f}% / model {((1+j.model).prod()**(1/yrs)-1)*100:.2f}%")
    for a, b in [("1998-06", "1998-08"), ("2000-08", "2002-09"), ("2007-10", "2009-02"), ("2019-12", "2020-03"), ("2021-12", "2022-09")]:
        lines.append(f"  {a} to {b}: VUSTX {window_return(j.vustx,a,b)*100:+.1f}% / model {window_return(j.model,a,b)*100:+.1f}%")
    comp = pd.concat([index_return.rename("index_plus_dividends"), spy.rename("spy")], axis=1).loc[:"2026-10"].dropna()
    comp.to_csv(RESULTS / "check_stock_spy.csv")
    annual_gap = (((1 + comp.index_plus_dividends).prod() ** (12/len(comp))) -
                  ((1 + comp.spy).prod() ** (12/len(comp))))
    lines.append(f"Index plus dividends vs SPY: CAGR gap {annual_gap*100:+.2f} percentage points ({len(comp)} months).")

(RESULTS / "checks.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
