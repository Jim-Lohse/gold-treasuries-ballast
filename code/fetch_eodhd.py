"""Optional: download the month-end series used only for the robustness checks
(month-end gold, S&P 500 index, SPY, VUSTX) from EOD Historical Data.
Needs your own EODHD API key: set EODHD_API_KEY in your environment.
This is licensed data, so it is not included in the repository."""
import csv, json, os, urllib.request
from common import RAW

TICKERS = {"XAUUSD.FOREX": "1990-01-01", "GSPC.INDX": "1989-12-01",
           "SPY.US": "1993-01-01", "VUSTX.US": "1986-01-01"}
URL = "https://eodhd.com/api/eod/{t}?api_token={k}&period=m&fmt=json&from={f}"

if __name__ == "__main__":
    key = os.environ["EODHD_API_KEY"]
    out = RAW / "eodhd"
    out.mkdir(parents=True, exist_ok=True)
    for t, f in TICKERS.items():
        with urllib.request.urlopen(URL.format(t=t, k=key, f=f)) as resp:
            rows = json.load(resp)
        path = out / f"{t}_monthly.csv"
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date", "close", "adjusted_close"])
            for r in rows:
                w.writerow([r["date"], r["close"], r["adjusted_close"]])
        print("saved", path, len(rows), "rows")
