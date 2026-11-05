import numpy as np
import pandas as pd


def safe_div(a, b):
    """a / b, returning NaN where b is zero or missing."""
    return a / b.replace(0, np.nan)


def compute_ratios(inputs):
    """Turn the inputs table (one row per fiscal year) into the six ratios."""
    gross_profit = inputs["gross_profit"].fillna(inputs["revenue"] - inputs["cost_of_sales"])

    # Reported operating income if available, else proxy = gross profit - R&D - SG&A
    proxy = gross_profit - inputs["rd_expense"] - inputs["sga_expense"]
    operating_income = inputs["operating_income"].fillna(proxy)

    # Provisional debt definition: current debt + noncurrent long-term debt
    total_debt = inputs["debt_current"] + inputs["long_term_debt_noncurrent"]

    return pd.DataFrame({
        "current_ratio": safe_div(inputs["current_assets"], inputs["current_liabilities"]),
        "gross_margin": safe_div(gross_profit, inputs["revenue"]),
        "operating_margin": safe_div(operating_income, inputs["revenue"]),
        "net_margin": safe_div(inputs["net_income"], inputs["revenue"]),
        "debt_to_equity": safe_div(total_debt, inputs["equity"]),
        "roe": safe_div(inputs["net_income"], inputs["equity"]),
        "operating_income_is_proxy": inputs["operating_income"].isna(),
    })
