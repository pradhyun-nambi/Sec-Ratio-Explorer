from src.fetch import get_company_facts
from src.extract import get_annual_values

facts = get_company_facts(200406)

print("--- operating income pieces ---")
for tag in ["ResearchAndDevelopmentExpense", "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost",
            "SellingGeneralAndAdministrativeExpense", "SellingAndMarketingExpense",
            "GeneralAndAdministrativeExpense", "OperatingExpenses", "CostsAndExpenses"]:
    s = get_annual_values(facts, tag)
    print(f"{tag:70s}", "-- none" if s.empty else f"{len(s):2d} yrs, latest {s.index[-1].date()} = {s.iloc[-1]/1e9:,.2f}B")

print("--- equity tags ---")
for tag in sorted(facts["facts"]["us-gaap"]):
    if "Equity" in tag:
        s = get_annual_values(facts, tag)
        if not s.empty:
            print(f"{tag:100s} {len(s):2d} yrs, latest {s.index[-1].date()} = {s.iloc[-1]/1e9:,.2f}B")
