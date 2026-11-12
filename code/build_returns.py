"""Step 1: build monthly returns, Jan 1972 - Oct 2026, from the original files.
Main test uses monthly averages (Shiller, World Bank, FRED monthly series).
Output: data/work/returns.csv"""
import sys
import argparse
import numpy as np
import openpyxl
import pandas as pd
import xlrd
from common import RAW, WORK, START, END, read_fred, par_bond_return


def load_shiller():
    """Robert Shiller's ie_data.xls: monthly average S&P 500 price (P) and dividends (D)."""
    sheet = xlrd.open_workbook(RAW / "shiller" / "ie_data.xls").sheet_by_name("Data")
    rows = []
    for i in range(8, sheet.nrows):
        v = sheet.row_values(i)
        if not isinstance(v[0], float):
            continue
        year = int(v[0])
        month = int(round((v[0] - year) * 100))          # 2026.1 means October
        rows.append((pd.Timestamp(year, month, 1), v[1], v[2] if v[2] != "" else np.nan))
    return pd.DataFrame(rows, columns=["date", "P", "D"]).set_index("date")


def load_gold():
    """World Bank Pink Sheet, CMO-Historical-Data-Monthly.xlsx, 'Monthly Prices' sheet, Gold column."""
    wb = openpyxl.load_workbook(RAW / "worldbank" / "CMO-Historical-Data-Monthly.xlsx",
                                read_only=True, data_only=True)
    rows = list(wb["Monthly Prices"].iter_rows(values_only=True))
    header = next(i for i, r in enumerate(rows) if r and "Gold" in r)
    col = rows[header].index("Gold")
    out = {}
    for r in rows[header + 2:]:
        if r[0] and isinstance(r[col], (int, float)):
            out[pd.Timestamp(int(r[0][:4]), int(r[0][5:7]), 1)] = float(r[col])
    return pd.Series(out).sort_index()


def load_spy_tail():
    path = RAW / "eodhd" / "SPY.US_monthly.csv"
    if not path.exists():
        return None
    s = pd.read_csv(path, parse_dates=["date"])
    s.index = s["date"].dt.to_period("M").dt.to_timestamp()
    return s["adjusted_close"].astype(float).pct_change()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock-tail", choices=["spy", "shiller"], default="spy",
                        help="SPY month-end tail or Shiller averages with carried dividend")
    args = parser.parse_args()
    gs5, gs10, gs20, gs30 = (read_fred(s) for s in ("GS5", "GS10", "GS20", "GS30"))
    tb3, cpi = read_fred("TB3MS"), read_fred("CPIAUCSL")
    cpi = cpi.interpolate(limit=1)          # Oct 2025 has no CPI reading; fill halfway

    # 20-year yield; FRED has no 20-year series Jan 1987 - Sep 1993, so the 30-year fills the gap.
    lt = gs20.copy()
    gap = lt.isna() & (lt.index >= "1987-01-01") & (lt.index <= "1993-09-01")
    lt[gap] = gs30.reindex(lt.index)[gap]

    r = pd.DataFrame(index=gs10.index)
    r["lt_treas"] = par_bond_return(lt, 20)
    r["t10"] = par_bond_return(gs10, 10)
    r["t5"] = par_bond_return(gs5, 5)
    r["gfund"] = ((gs5 + gs10 + lt) / 3).shift(1) / 100 / 12   # G Fund model: no price risk
    r["cash"] = tb3.shift(1) / 100 / 12
    r["gold"] = load_gold().pct_change()

    sh = load_shiller()
    shd = sh[sh["D"] > 0]
    stocks = ((shd["P"] + shd["D"] / 12) / shd["P"].shift(1) - 1).reindex(r.index)
    last_div = shd.index.max()
    spy = load_spy_tail()
    tail = r.index[(r.index > last_div) & (r.index <= END)]
    if args.stock_tail == "spy" and spy is not None:
        stocks.loc[tail] = spy.reindex(tail)
        note = f"SPY total return after {last_div:%b %Y}"
    else:   # no EODHD key: Shiller price with the last known dividend carried forward
        p = sh["P"]
        stocks.loc[tail] = ((p + shd["D"].iloc[-1] / 12) / p.shift(1) - 1).reindex(tail)
        note = f"Shiller price with last dividend carried forward after {last_div:%b %Y} (no SPY file)"
    r["stocks"] = stocks
    r["cpi"] = cpi
    r["infl"] = cpi.pct_change()

    r = r.reindex(pd.date_range(START, END, freq="MS"))
    missing = r.isna().sum()
    if missing.sum():
        sys.exit(f"missing values:\n{missing[missing > 0]}")
    r.to_csv(WORK / "returns.csv")
    (WORK / "stock_source.txt").write_text(note + "\n")
    print(f"returns.csv: {len(r)} months, {r.index.min():%b %Y} to {r.index.max():%b %Y}; stocks: {note}")
