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