from src.extract import get_annual_values


def make_facts(rows):
    return {"facts": {"us-gaap": {"NetIncomeLoss": {"units": {"USD": rows}}}}}


def row(end, val, filed, form="10-K", fp="FY", start=None):
    r = {"end": end, "val": val, "filed": filed, "form": form, "fp": fp}
    if start:
        r["start"] = start
    return r


def test_ignores_quarterly_filings():
    facts = make_facts([
        row("2024-12-29", 100, "2025-02-10", start="2024-01-01"),
        row("2024-09-29", 30, "2024-10-20", form="10-Q", fp="Q3", start="2024-07-01"),
    ])
    s = get_annual_values(facts, "NetIncomeLoss")
    assert len(s) == 1 and s.iloc[0] == 100


def test_restatement_keeps_latest_filing():
    facts = make_facts([
        row("2024-12-29", 100, "2025-02-10", start="2024-01-01"),
        row("2024-12-29", 110, "2026-02-10", start="2024-01-01"),
    ])
    assert get_annual_values(facts, "NetIncomeLoss").iloc[0] == 110


def test_ignores_short_periods_labeled_fy():
    facts = make_facts([row("2024-12-29", 25, "2025-02-10", start="2024-10-01")])
    assert get_annual_values(facts, "NetIncomeLoss").empty


def test_missing_tag_returns_empty():
    assert get_annual_values(make_facts([]), "DoesNotExist").empty
    

from src.extract import get_series


def test_get_series_fills_gaps_with_fallback_tag():
    facts = {"facts": {"us-gaap": {
        "NewTag": {"units": {"USD": [row("2024-12-29", 5, "2025-02-10", start="2024-01-01")]}},
        "OldTag": {"units": {"USD": [
            row("2023-12-31", 3, "2024-02-10", start="2023-01-01"),
            row("2024-12-29", 99, "2025-02-10", start="2024-01-01"),
        ]}},
    }}}
    s = get_series(facts, ["NewTag", "OldTag"])
    assert list(s) == [3, 5]
