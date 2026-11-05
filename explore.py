from src.fetch import get_company_facts
from src.extract import get_annual_values

facts = get_company_facts(200406)
print(get_annual_values(facts, "NetIncomeLoss").tail(6))
