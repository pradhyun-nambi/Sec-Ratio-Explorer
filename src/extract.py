import pandas as pd


def get_annual_values(facts, tag, unit="USD"):
    """Annual (10-K, full-year) values for one us-gaap tag.

    Returns a Series indexed by period end date, one value per year.
    If a year was restated, the most recently filed value wins.
    """
    empty = pd.Series(dtype="float64", name=tag)
    try:
        rows = facts["facts"]["us-gaap"][tag]["units"][unit]
    except KeyError:
        return empty

    df = pd.DataFrame(rows)
    df = df[(df["form"] == "10-K") & (df["fp"] == "FY")]
    if df.empty:
        return empty

    df["end"] = pd.to_datetime(df["end"])
    # Income-statement items have a start date: keep only ~1-year periods.
    # Balance-sheet items have no start date: keep as is.
    if "start" in df.columns:
        days = (df["end"] - pd.to_datetime(df["start"])).dt.days
        df = df[days.isna() | days.between(350, 380)]

    df = df.sort_values("filed").drop_duplicates(subset="end", keep="last")
    return pd.Series(df["val"].astype(float).values, index=df["end"], name=tag).sort_index()

def get_series(facts, tags):
    """Try tags in priority order; later tags only fill years the earlier ones lack."""
    result = None
    for tag in tags:
        s = get_annual_values(facts, tag)
        if s.empty:
            continue
        result = s if result is None else result.combine_first(s)
    if result is None:
        return pd.Series(dtype="float64", index=pd.DatetimeIndex([]))
    return result.sort_index()


TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "cost_of_sales": ["CostOfGoodsAndServicesSold", "CostOfGoodsSold", "CostOfRevenue"],
    "gross_profit": ["GrossProfit"],
    "rd_expense": ["ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"],
    "sga_expense": ["SellingGeneralAndAdministrativeExpense"],
    "operating_income": ["OperatingIncomeLoss"],
    "pretax_income": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
    "net_income": ["NetIncomeLoss"],
    "current_assets": ["AssetsCurrent"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "total_assets": ["Assets"],
    "total_liabilities": ["Liabilities"],
    "equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "long_term_debt_noncurrent": ["LongTermDebtNoncurrent"],
    "debt_current": ["DebtCurrent"],
}


def get_inputs(facts):
    """One row per fiscal year-end, one column per ratio input."""
    return pd.DataFrame({name: get_series(facts, tags) for name, tags in TAGS.items()}).sort_index()
