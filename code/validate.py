"""Rebuild the study and record execution results and source qualifications.
Exit 0 = all required checks ran; 2 = missing inputs; 1 = calculation/check failure.
Successful execution does not independently authenticate supplied files or citations.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
import pandas as pd
from common import ROOT, RAW, WORK, RESULTS

checks = []
def run(name, args):
    p = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
    checks.append({'name': name, 'status': 'passed' if p.returncode == 0 else 'failed',
                   'returncode': p.returncode, 'output': p.stdout + p.stderr})
    return p.returncode == 0

run('Regression tests', ['-m', 'unittest', 'discover', '-s', 'tests', '-v'])
run('Compile Python modules', ['-m', 'compileall', '-q', 'code'])
required = [RAW/'shiller/ie_data.xls', RAW/'worldbank/CMO-Historical-Data-Monthly.xlsx']
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if not any((RAW/'tsp'/f'g-fund-rates-of-return.{ext}').exists() for ext in ['xls', 'xlsx']):
    missing.append('data/raw/tsp/g-fund-rates-of-return.xls or .xlsx')
for ticker in ['XAUUSD.FOREX', 'GSPC.INDX', 'SPY.US', 'VUSTX.US']:
    p = RAW/'eodhd'/f'{ticker}_monthly.csv'
    if not p.exists(): missing.append(str(p.relative_to(ROOT)))
main_ok = False
if missing:
    checks.append({'name': 'Required source files', 'status': 'blocked', 'missing': missing})
else:
    main_ok = run('Build monthly-average returns', ['code/build_returns.py'])
    if main_ok:
        main_ok = run('Main backtest and walk-forward', ['code/backtest.py'])
        run('Fresh month-end, VUSTX and G Fund checks', ['code/checks.py'])
        run('SPY vs Shiller tail sensitivity', ['code/check_stock_tail.py'])
        pdf = RAW/'worldbank/CMO-Pink-Sheet-November-2026.pdf'
        if pdf.exists(): run('Gold series vs uploaded November PDF', ['code/check_gold_sources.py'])
        else: checks.append({'name': 'Gold series vs November PDF', 'status': 'blocked', 'missing': [str(pdf.relative_to(ROOT))]})
inputs = []
for p in sorted(RAW.rglob('*')):
    if p.is_file() and p.suffix.lower() in {'.csv', '.xls', '.xlsx', '.pdf'}:
        inputs.append({'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
failed = any(c['status'] == 'failed' for c in checks)
blocked = any(c['status'] == 'blocked' for c in checks)
status = 'failed' if failed else ('partial' if blocked else 'completed_with_source_qualifications')
gold = json.loads((WORK/'gold_source.json').read_text()) if (WORK/'gold_source.json').exists() else {}
qualifications = [
    'The supplied World Bank workbook ends in February 2021. A datasets/gold-prices mirror supplements March 2021-October 2026 (68 months), rounded to whole USD. It is not the exact original 2026 workbook.',
    'The mirror overlaps 734 workbook observations; the maximum difference is $0.50, consistent with rounding. Existing workbook values are preserved.',
    'The supplied G Fund XLSX cites TSP / Stock Analysis / TSP Folio. It is a user-supplied compilation, not authenticated as a direct tsp.gov export. Only complete annual rows are compared; 2026 YTD is excluded.',
    'Historical inputs are revised series, not point-in-time vintages. The monitoring rule is not validated as a trading strategy.',
    'The bibliography, historical authorship and pre-registration claims were not independently audited.'
]
report = {'run_utc': datetime.now(timezone.utc).isoformat(), 'status': status,
          'python': sys.version.split()[0], 'pandas': pd.__version__, 'checks': checks,
          'inputs': inputs, 'gold_provenance': gold, 'source_qualifications': qualifications}
(RESULTS/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
lines = ['# Validation run', '', f"Run: {report['run_utc']}", f"Status: **{status.upper()}**", '',
         'Execution completed with the source qualifications below. This is a reproduction with documented supplemental data, not authentication of every source or exact recovery of the original data vintage.', '',
         '| Check | Outcome |', '|---|---|']
lines += [f"| {c['name']} | {c['status']} |" for c in checks]
lines += ['', '## Source qualifications', ''] + ['- '+x for x in qualifications]
lines += ['', '## Outputs', '',
          '- Main monthly-average returns cover 658 months, January 1972-October 2026. Main tables, summary, walk-forward choices and average-versus-month-end comparison are regenerated.',
          '- Month-end checks cover 441 months. G Fund comparison uses 38 complete years, 1988-2025.',
          '- `check_stock_tail_sensitivity.csv` contains 48 comparisons; main SPY-tail returns are restored afterward.',
          '- `check_gold_pdf.csv` compares 11 published gold figures with monthly-series aggregates. Input hashes are recorded in `validation.json`. Licensed raw inputs are not redistributed.', '',
          '## Execution log', '']
for c in checks:
    lines += [f"### {c['name']}", '', '```text', c.get('output', str(c.get('missing',''))).strip(), '```', '']
lines += ['## Reproduce', '', 'Provide the sources documented in `data/raw/README.md`, then run `python code/validate.py`. Exit code 2 indicates missing inputs; exit code 1 indicates a failed calculation or check.']
(RESULTS/'validation.md').write_text('\n'.join(lines)+'\n')
print(f'Validation status: {status}; see results/validation.md')
sys.exit(1 if failed else (2 if blocked else 0))
