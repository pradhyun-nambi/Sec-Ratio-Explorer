import pandas as pd
from src.fetch import get_company_facts
from src.extract import get_inputs

pd.set_option("display.width", 200)
facts = get_company_facts(200406)
print((get_inputs(facts).tail(3).T / 1e9).round(2))
