"""Compare SPY month-end and carried-dividend Shiller average tails.
Both variants use identical January 1972-June 2026 returns. Main returns are restored.
"""
import subprocess
import sys
import pandas as pd
from common import ROOT, WORK, RESULTS, SLEEVES, stats, portfolio_return

path = WORK / 'returns.csv'
original = path.read_bytes()
source_path = WORK / 'stock_source.txt'
source = source_path.read_bytes()
base = pd.read_csv(path, index_col=0, parse_dates=True)
try:
    subprocess.run([sys.executable, 'code/build_returns.py', '--stock-tail', 'shiller'], cwd=ROOT, check=True)
    alternate = pd.read_csv(path, index_col=0, parse_dates=True)
    if not base.loc[:'2026-06'].equals(alternate.loc[:'2026-06']):
        raise ValueError('Sensitivity unexpectedly changed pre-tail data')
    rows = []
    for period, start in [('full_history', '1972-01'), ('recent_rate_regime', '2020-08')]:
        for name, weights in SLEEVES.items():
            for sw in [.7, .8, .9]:
                a = stats(portfolio_return(base, weights, sw).loc[start:], base['infl'])
                b = stats(portfolio_return(alternate, weights, sw).loc[start:], alternate['infl'])
                rows.append({'period': period, 'ballast': name, 'stock_weight': sw,
                             'spy_tail_cagr': a['yearly_return'], 'shiller_tail_cagr': b['yearly_return'],
                             'cagr_difference': b['yearly_return']-a['yearly_return'],
                             'spy_tail_drawdown': a['worst_drawdown'], 'shiller_tail_drawdown': b['worst_drawdown']})
    pd.DataFrame(rows).to_csv(RESULTS/'check_stock_tail_sensitivity.csv', index=False)
    print('Sensitivity passed: 48 portfolio/period comparisons; main returns restored.')
finally:
    path.write_bytes(original)
    source_path.write_bytes(source)
