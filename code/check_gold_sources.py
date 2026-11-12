"""Check the supplemental gold series against the uploaded workbook and PDF."""
import re
import pandas as pd
from pypdf import PdfReader
from common import RAW, RESULTS
from build_returns import load_gold

s = load_gold()
path = RAW/'worldbank/CMO-Pink-Sheet-November-2026.pdf'
text = '\n'.join(p.extract_text() for p in PdfReader(path).pages)
line = next(x for x in text.splitlines() if x.startswith('Gold $/toz'))
values = [float(x.replace(',', '')) for x in re.findall(r'\b[\d,]+\b', line)]
windows = [('2023','2023'), ('2024','2024'), ('2025','2025'), ('2025-07','2025-09'),
           ('2025-10','2025-12'), ('2026-01','2026-03'), ('2026-04','2026-06'),
           ('2026-07','2026-09'), ('2026-08','2026-08'), ('2026-09','2026-09'), ('2026-10','2026-10')]
if len(values) != len(windows):
    raise ValueError('Unexpected Pink Sheet gold row format')
rows = []
for (a,b), expected in zip(windows, values):
    actual = float(s.loc[a:b].mean())
    rows.append({'start': a, 'end': b, 'pdf_price': expected, 'series_average': actual, 'gap_usd': actual-expected})
result = pd.DataFrame(rows)
result.to_csv(RESULTS/'check_gold_pdf.csv', index=False)
if result.gap_usd.abs().max() > 1:
    raise ValueError('Supplement disagrees with uploaded PDF by more than $1')
print(f'Gold PDF check passed: {len(rows)} observations, max gap ${result.gap_usd.abs().max():.2f}.')
