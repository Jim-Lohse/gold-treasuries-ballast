"""Run validation and record exactly which parts were reproduced.
Run from any directory: python code/validate.py
Exit 0 = full pipeline; 2 = partial (missing source files); 1 = failed check.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
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
main_ok = False
if not missing:
    main_ok = run('Build monthly-average returns', ['code/build_returns.py'])
    if main_ok:
        main_ok = run('Main backtest and walk-forward', ['code/backtest.py'])
else:
    checks.append({'name': 'Main monthly-average backtest and walk-forward', 'status': 'blocked', 'missing': missing})
    # Never use an old returns file to label a comparison as freshly rebuilt.
    (WORK/'returns.csv').unlink(missing_ok=True)

before = {}
for name in ['check_monthend_drops.csv', 'stock_longtreasury_corr36_monthend.csv']:
    p = RESULTS/name
    if p.exists(): before[name] = pd.read_csv(p)
run('Fresh month-end, VUSTX and G Fund checks', ['code/checks.py'])
for name, old in before.items():
    p = RESULTS/name
    if not p.exists(): continue
    new = pd.read_csv(p)
    if old.shape == new.shape and old.columns.equals(new.columns):
        cols = new.select_dtypes('number').columns
        delta = float((new[cols] - old[cols]).abs().max().max())
        checks.append({'name': f'Fresh output vs previous {name}', 'status': 'passed' if delta < 1e-10 else 'changed',
                       'maximum_absolute_difference': delta})

# Capture provenance without redistributing licensed source files.
inputs = []
for p in sorted(RAW.rglob('*')):
    if p.is_file() and p.suffix.lower() in {'.csv', '.xls', '.xlsx'}:
        inputs.append({'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
failed = any(c['status'] == 'failed' for c in checks)
monthend_ok = all((RESULTS/name).exists() for name in ['check_monthend_drops.csv', 'check_vustx.csv', 'check_stock_spy.csv'])
status = 'failed' if failed else ('partial' if not main_ok or not monthend_ok or not (RAW/'tsp/g-fund-rates-of-return.xls').exists() else 'complete')
report = {'run_utc': datetime.now(timezone.utc).isoformat(), 'status': status,
          'python': sys.version.split()[0], 'pandas': pd.__version__, 'checks': checks, 'inputs': inputs,
          'tsp_reference': 'original export' if (RAW/'tsp/g-fund-rates-of-return.xls').exists() else 'previously committed reference; not independently verified',
          'stock_tail_sensitivity': 'not run; pending source workbook',
          'historical_outputs': 'Main tables regenerated.' if main_ok else 'Main tables and summary remain historical; original World Bank workbook unavailable.'}
(RESULTS/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
lines = ['# Validation run', '', f"Run: {report['run_utc']}", f"Status: **{status.upper()}**", '',
         '| Check | Outcome |', '|---|---|']
lines += [f"| {c['name']} | {c['status']} |" for c in checks]
lines += ['', '## Scope and limitations', '',
          '- FRED, Shiller and EODHD source files were retrieved for this validation. Source-file SHA-256 hashes are recorded in `validation.json`; source data are not redistributed.',
          ('- Main monthly-average backtest and walk-forward were regenerated.' if main_ok else '- The original World Bank workbook could not be downloaded in the November 12 reconciliation (HTTP 403). Main 1972–2026 results and walk-forward rankings remain historical until the missing source is supplied. The prior average-versus-month-end comparison is archived.'),
          f"- TSP reference source: {report['tsp_reference']}. G Fund proxy returns are recomputed from the FRED input files.",
          ('- The month-end rebuild covers 441 complete months. VUSTX and stock/SPY comparisons are exported as monthly CSVs.' if monthend_ok else '- Month-end validation is incomplete; inspect the check log.'),
          '- Corrected drawdown includes starting wealth. Five regression tests cover initial losses, later peaks, real compounding, invalid inputs, flat-yield bond returns and peak-month exclusion.',
          '- README rounding, rate-regime figures and walk-forward wording were reconciled to the historical CSVs. The inflation monitoring statement was corrected to acknowledge the positive 1990–91 long-Treasury real return.',
          '- SPY-tail sensitivity remains pending. The chronology of walk-forward training is not evidence of point-in-time data availability.',
          '- Bibliography, historical authorship and pre-registration claims were not independently audited.', '',
          '## Fresh check log', '', '```text', (RESULTS/'checks.txt').read_text().strip(), '```', '',
          '## Reproduce', '', 'Place the original sources at the paths in `data/raw/README.md`, fetch FRED/EODHD inputs, then run:', '',
          '```bash', 'python code/validate.py', '```', '',
          'Exit code 2 explicitly denotes partial validation, not a full pass.']
(RESULTS/'validation.md').write_text('\n'.join(lines)+'\n')
print(f'Validation status: {status}; see results/validation.md')
sys.exit(1 if failed else (0 if status == 'complete' else 2))
