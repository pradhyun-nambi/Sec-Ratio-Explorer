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
- Debt: still to settle. Need to check JNJ's balance sheet in the 10-K to see whether DebtCurrent already includes the current portion of long-term debt.

## Verification: JNJ fiscal 2025 (tool vs. 10-K)
| Line item | Tool (B) | 10-K (B) | Match? |
|---|---|---|---|
| Revenue (sales to customers) | 94.19 | | |
| Net earnings | 26.80 | | |
| Earnings before provision for taxes | 32.58 | | |
| Total current assets | 55.62 | | |
| Total current liabilities | 54.13 | | |
| Total shareholders' equity | 81.54 | | |
| Loans and notes payable (current debt) | 8.50 | | |
| Long-term debt (noncurrent) | 39.44 | | |
- MRK reports R&D as ResearchAndDevelopmentExpense (not the ExcludingAcquiredInProcessCost tag JNJ uses); it may include acquired IPR&D, so proxy operating margin is less comparable between MRK and JNJ.
- ROE uses year-end equity, not average equity.
- MRK reports R&D as ResearchAndDevelopmentExpense (not the ExcludingAcquiredInProcessCost tag JNJ uses); it may include acquired IPR&D, so proxy operating margin is less comparable between MRK and JNJ.
- ROE uses year-end equity, not average equity.
