import numpy as np
import pandas as pd
from src.ratios import compute_ratios


def make_inputs(**overrides):
    base = dict(revenue=100.0, cost_of_sales=40.0, gross_profit=60.0, rd_expense=10.0,
                sga_expense=20.0, operating_income=np.nan, net_income=15.0,
                current_assets=50.0, current_liabilities=25.0, equity=100.0,
                long_term_debt_noncurrent=30.0, debt_current=10.0)
    base.update(overrides)
    return pd.DataFrame([base], index=pd.to_datetime(["2025-12-28"]))


def test_ratios_match_hand_calculation():
    r = compute_ratios(make_inputs()).iloc[0]
    assert r["current_ratio"] == 2.0        # 50 / 25
    assert r["gross_margin"] == 0.6         # 60 / 100
    assert r["operating_margin"] == 0.3     # (60 - 10 - 20) / 100
    assert r["net_margin"] == 0.15          # 15 / 100
    assert r["debt_to_equity"] == 0.4       # (30 + 10) / 100
    assert r["roe"] == 0.15                 # 15 / 100
    assert r["operating_income_is_proxy"]


def test_reported_operating_income_beats_proxy():
    r = compute_ratios(make_inputs(operating_income=45.0)).iloc[0]
    assert r["operating_margin"] == 0.45
    assert not r["operating_income_is_proxy"]


def test_zero_equity_gives_nan_not_error():
    r = compute_ratios(make_inputs(equity=0.0)).iloc[0]
    assert np.isnan(r["roe"]) and np.isnan(r["debt_to_equity"])


def test_missing_gross_profit_is_derived():
    r = compute_ratios(make_inputs(gross_profit=np.nan)).iloc[0]
    assert r["gross_margin"] == 0.6


def test_bank_style_missing_inputs_give_nan():
    r = compute_ratios(make_inputs(current_assets=np.nan, current_liabilities=np.nan,
                                   cost_of_sales=np.nan, gross_profit=np.nan)).iloc[0]
    assert np.isnan(r["current_ratio"]) and np.isnan(r["gross_margin"])


from src.extract import get_inputs


def test_empty_filing_gives_empty_ratios():
    inputs = get_inputs({"facts": {"us-gaap": {}}})
    assert compute_ratios(inputs).empty
