import pandas as pd
from src.fetch import get_company_facts
from src.extract import get_inputs
from src.ratios import compute_ratios

pd.set_option("display.width", 200)
facts = get_company_facts(200406)
print(compute_ratios(get_inputs(facts)).tail(4).T.round(3))
