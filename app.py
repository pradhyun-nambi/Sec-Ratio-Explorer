import pandas as pd
import streamlit as st

from src.companies import COMPANIES
from src.extract import get_inputs
from src.fetch import get_company_facts
from src.ratios import compute_ratios


@st.cache_data
def load_all():
    frames = {}
    for ticker, cik in COMPANIES.items():
        ratios = compute_ratios(get_inputs(get_company_facts(cik)))
        # Fiscal-year label: subtract 14 days so JNJ's Jan-3-2021 year-end counts as FY2020
        ratios.index = (ratios.index - pd.Timedelta(days=14)).year
        frames[ticker] = ratios
    return frames


st.title("SEC Filing Ratio Explorer")
st.caption("Public SEC EDGAR data (companyfacts). Educational only, not investment advice.")

frames = load_all()
years = sorted(set.intersection(*[set(f.index) for f in frames.values()]), reverse=True)
year = st.selectbox("Fiscal year", years)

table = pd.DataFrame({
    t: f.loc[year].drop("operating_income_is_proxy").astype(float) for t, f in frames.items()
})
st.dataframe(table.round(3))
st.caption("Blank = not reported or not applicable (e.g., JPM is a bank).")

ratio = st.selectbox("Chart this ratio", list(table.index))
st.bar_chart(table.loc[ratio].dropna())

st.subheader("Read this before drawing conclusions")
st.markdown(
    "- Operating margin is a **computed proxy** (gross profit - R&D - SG&A); none of these companies tags operating income.\n"
    "- ROE uses year-end equity, not average equity, so it differs from company-reported ROE.\n"
    "- JPM is a bank: current ratio, gross margin, and debt-to-equity are not meaningful for it.\n"
    "- One-time items (e.g., JNJ's 2023 net income) can distort a single year."
)
