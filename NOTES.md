# NOTES

## Companies
JNJ, PFE, MRK, LLY, JPM (JPM is a bank, so current ratio and gross margin will be N/A)

## Ratios
- Current ratio = current assets / current liabilities
- Gross margin = (revenue - cost of sales) / revenue
- Operating margin = operating income / revenue
- Net margin = net income / revenue
- Debt-to-equity = total debt / stockholders' equity (my definition: total debt = long-term debt + short-term borrowings and current portion of long-term debt)
- ROE = net income / stockholders' equity

## What went wrong
- SEC returned 403 until I used a real User-Agent. I moved it to an environment variable (SEC_USER_AGENT) so my email stays out of the public repo.

## JNJ tag choices (Day 3)
- Revenue: RevenueFromContractWithCustomerExcludingAssessedTax (only ~10 yrs of history)
- Cost of sales: CostOfGoodsAndServicesSold; older years use CostOfGoodsSold (JNJ switched tags)
- Operating income: OperatingIncomeLoss stops in 2014. JNJ has no operating income line, so I use a proxy: GrossProfit - R&D - SG&A. It excludes items like acquired in-process R&D and restructuring.
- Equity: StockholdersEquity is missing for JNJ. I use StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest (81.54B in 2025, matches assets minus liabilities).
- Debt: settled, see JNJ findings below (loans and notes payable + long-term debt).

## Verification: JNJ fiscal 2025 (tool vs. 10-K)
| Line item | Tool (B) | 10-K (B) | Match? |
|---|---|---|---|
| Revenue (sales to customers) | 94.19 | 94.193 | Yes |
| Net earnings | 26.80 | 26.804 | Yes |
| Earnings before provision for taxes | 32.58 | 32.581 | Yes |
| Total current assets | 55.62 | 55.624 | Yes |
| Total current liabilities | 54.13 | 54.126 | Yes |
| Total shareholders' equity | 81.54 | 81.544 (derived: assets - liabilities) | Yes |
| Loans and notes payable (current debt) | 8.50 | 8.495 | Yes |
| Long-term debt (noncurrent) | 39.44 | 39.438 | Yes |
- MRK reports R&D as ResearchAndDevelopmentExpense (not the ExcludingAcquiredInProcessCost tag JNJ uses); it may include acquired IPR&D, so proxy operating margin is less comparable between MRK and JNJ.
- ROE uses year-end equity, not average equity.


## JNJ findings
- Debt definition: loans and notes payable (includes the ~2.0B current portion of bonds) + long-term debt = 47.93B. No separate current-portion line on the balance sheet.
- 2023 net earnings (35.15B) include 21.8B from discontinued operations, so 2023 net margin and ROE are inflated.
- 2025 net earnings are boosted by 7.2B of other income (2024 had 4.7B of other expense). Single-year ratios are noisy.
