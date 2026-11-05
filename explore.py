import pandas as pd
from src.fetch import get_company_facts
from src.extract import get_inputs, get_annual_values
from src.ratios import compute_ratios
from src.companies import COMPANIES

pd.set_option("display.width", 200)
rows = {}
for t, cik in COMPANIES.items():
    r = compute_ratios(get_inputs(get_company_facts(cik))).iloc[-1]
    rows[t] = r.drop("operating_income_is_proxy").astype(float)
print(pd.DataFrame(rows).round(3))

print()
facts = get_company_facts(COMPANIES["MRK"])
for tag in sorted(facts["facts"]["us-gaap"]):
    if "ResearchAndDevelopment" in tag:
        s = get_annual_values(facts, tag)
        if not s.empty:
            print(f"{tag:90s} {len(s):2d} yrs, latest {s.index[-1].date()} = {s.iloc[-1]/1e9:,.2f}B")
