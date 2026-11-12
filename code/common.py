"""Shared helpers: paths, bond rebuild, portfolio math, crash finder."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WORK = ROOT / "data" / "work"
RESULTS = ROOT / "results"
for p in (WORK, RESULTS):
    p.mkdir(parents=True, exist_ok=True)

START, END = "1972-01-01", "2026-10-01"

# Ballast mixes tested (weights inside the ballast sleeve).
SLEEVES = {
    "Gold + G Fund": {"gold": 0.5, "gfund": 0.5},
    "Gold + G Fund + long Treasury": {"gold": 1 / 3, "gfund": 1 / 3, "lt_treas": 1 / 3},
    "Gold + long Treasury": {"gold": 0.5, "lt_treas": 0.5},
    "Gold + 5-year Treasury": {"gold": 0.5, "t5": 0.5},
    "G Fund only": {"gfund": 1.0},
    "Gold only": {"gold": 1.0},
    "Long Treasury only": {"lt_treas": 1.0},
    "Cash only": {"cash": 1.0},
}


def read_fred(series):
    """Read a FRED CSV saved from fredgraph.csv (header DATE or observation_date)."""
    df = pd.read_csv(RAW / "fred" / f"{series}.csv")
    date_col = df.columns[0]
    s = pd.to_numeric(df[series], errors="coerce")
    s.index = pd.to_datetime(df[date_col])
    return s


def month_end(s):
    """Last available value in each month, labeled by the first day of the month."""
    s = s.dropna()
    out = s.groupby(s.index.to_period("M")).last()
    out.index = out.index.to_timestamp()
    return out


def par_bond_return(y, years):
    """Monthly total return of a constant-maturity par bond rebuilt each month.
    Bought at par with a coupon equal to last month's yield, repriced one month later at
    this month's yield with (years - 1/12) left. Semiannual coupons. y is in percent."""
    y = y / 100.0
    out = pd.Series(np.nan, index=y.index)
    n = 2 * (years - 1 / 12)
    for i in range(1, len(y)):
        c, yn = y.iloc[i - 1], y.iloc[i]
        if np.isnan(c) or np.isnan(yn):
            continue
        k = yn / 2
        price = (c / 2) * (1 - (1 + k) ** -n) / k + (1 + k) ** -n
        out.iloc[i] = price - 1 + c / 12
    return out


def sleeve_return(r, weights):
    return sum(r[k] * w for k, w in weights.items())


def portfolio_return(r, weights, stock_weight):
    """Stocks plus a ballast sleeve, rebalanced monthly."""
    return stock_weight * r["stocks"] + (1 - stock_weight) * sleeve_return(r, weights)


def stats(x, infl):
    idx = (1 + x).cumprod()
    years = len(x) / 12
    cagr = idx.iloc[-1] ** (1 / years) - 1
    dd = (idx / idx.cummax() - 1).min()
    real = (1 + x) / (1 + infl.loc[x.index]) - 1
    real_cagr = (1 + real).prod() ** (1 / years) - 1
    return {"yearly_return": cagr, "real_yearly_return": real_cagr,
            "volatility": x.std() * np.sqrt(12), "worst_drawdown": dd,
            "return_to_drawdown": cagr / -dd if dd < 0 else np.nan}


def window_return(s, start, end):
    """Return from the end of the start month to the end of the end month."""
    return (1 + s.loc[start:end].iloc[1:]).prod() - 1


def find_drops(stock_returns, deeper_than, shallower_than=-1.0):
    """Peak-to-bottom falls in a total-return index between the two thresholds.
    A drop ends when the index recovers its previous peak."""
    idx = (1 + stock_returns).cumprod()
    v, ix = idx.values, idx.index
    out, peak, i = [], 0, 0
    while i < len(v):
        if v[i] >= v[peak]:
            peak = i
            i += 1
            continue
        j = bottom = i
        while j < len(v) and v[j] < v[peak]:
            if v[j] < v[bottom]:
                bottom = j
            j += 1
        depth = v[bottom] / v[peak] - 1
        if shallower_than < depth <= deeper_than:
            out.append((ix[peak], ix[bottom], depth))
        peak = j if j < len(v) else peak
        i = j + 1
    return out


def pct(df, cols):
    df = df.copy()
    df[cols] = (df[cols] * 100).round(1)
    return df
