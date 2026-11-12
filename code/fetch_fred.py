"""Step 0: download the FRED series this study uses into data/raw/fred/.
Public data, no key needed. Run once: python code/fetch_fred.py"""
import urllib.request
from common import RAW

SERIES = ["GS5", "GS10", "GS20", "GS30", "TB3MS", "CPIAUCSL", "DGS5", "DGS10", "DGS20", "DGS30"]
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"

if __name__ == "__main__":
    out = RAW / "fred"
    out.mkdir(parents=True, exist_ok=True)
    for s in SERIES:
        path = out / f"{s}.csv"
        urllib.request.urlretrieve(URL.format(s), path)
        print("saved", path)
