import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from common import stats, par_bond_return, window_return

class MathTests(unittest.TestCase):
    def test_initial_loss_counts_as_drawdown(self):
        x = pd.Series([-.2, .1], index=pd.date_range('2000-01-01', periods=2, freq='MS'))
        self.assertAlmostEqual(stats(x, x*0)['worst_drawdown'], -.2)

    def test_later_peak_and_real_compounding(self):
        x = pd.Series([.1, -.2, .05], index=pd.date_range('2000-01-01', periods=3, freq='MS'))
        inflation = pd.Series(.01, index=x.index)
        s = stats(x, inflation)
        self.assertAlmostEqual(s['worst_drawdown'], -.2)
        self.assertAlmostEqual(s['real_yearly_return'], ((1.1*.8*1.05)/(1.01**3))**4-1)

    def test_missing_month_is_rejected(self):
        x = pd.Series([.1, np.nan], index=pd.date_range('2000-01-01', periods=2, freq='MS'))
        with self.assertRaises(ValueError): stats(x, x.fillna(0)*0)

    def test_flat_yield_earns_coupon(self):
        y = pd.Series([6., 6.])
        self.assertAlmostEqual(par_bond_return(y, 20).iloc[1], .005)

    def test_peak_month_is_excluded(self):
        x = pd.Series([.5, -.2, .1], index=pd.date_range('2000-01-01', periods=3, freq='MS'))
        self.assertAlmostEqual(window_return(x, '2000-01', '2000-03'), -.12)

if __name__ == '__main__': unittest.main()
