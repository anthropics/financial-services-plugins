---
name: credit-memo-repayment-analysis
description: Analyzes a borrower's capacity to repay a proposed loan. Covers cash conversion cycle, working capital analysis, Days Sales Outstanding (DSO), Days Payable Outstanding (DPO), debt-to-income ratio, existing debt obligations, macroeconomic factors, and detailed repayment schedule modeling. Claude uses this skill automatically when assessing loan repayment viability.
---

# Credit Memo — Repayment Analysis Skill

## Overview
The central question of repayment analysis is: **Can this borrower comfortably service the proposed debt from operating cash flows, even under stress conditions?** Every calculation must be tied back to this question.

---

## Guiding Principle
Present both a base case and stress case repayment analysis. Lenders need to know not just whether repayment works under normal conditions, but whether the borrower can survive a 20–30% revenue decline or margin compression.

---

## Section 1: Working Capital & Cash Cycle Analysis

### Required Calculations:
```
DSO (Days Sales Outstanding)     = (Accounts Receivable / Revenue) × 365
DIO (Days Inventory Outstanding) = (Inventory / COGS) × 365
DPO (Days Payable Outstanding)   = (Accounts Payable / COGS) × 365
CCC (Cash Conversion Cycle)      = DSO + DIO - DPO
Working Capital                  = Current Assets - Current Liabilities
Working Capital as % Revenue     = Working Capital / Revenue × 100
```

### Required Table:
| Working Capital Metric | FY2021 | FY2022 | FY2023 | Industry Avg | Trend |
|---|---|---|---|---|---|
| Accounts Receivable ($M) | | | | | |
| DSO (days) | | | | ~30–45 days | ↑/↓/→ |
| Inventory ($M) | | | | | |
| DIO (days) | | | | | |
| Accounts Payable ($M) | | | | | |
| DPO (days) | | | | ~30–45 days | |
| Cash Conversion Cycle (days) | | | | | |
| Working Capital ($M) | | | | | |

### Interpretation Framework:
- **Short CCC (< 30 days):** Company converts sales to cash quickly — positive for repayment
- **Long CCC (> 60 days):** Cash is tied up in operations — monitor for liquidity strain at loan drawdown
- **Rising DSO:** Customers paying slower — potential collection issues or revenue quality concern
- **Rising DIO:** Inventory building up — potential demand softness
- **Falling DPO:** Paying suppliers faster — may pressure near-term cash

Write a paragraph interpreting the CCC trend and what it implies for the borrower's liquidity cycle relative to loan repayment timing.

---

## Section 2: Income & Cash Flow Repayment Capacity

### Key Metrics:
```
LTM Revenue                = Last Twelve Months Revenue
LTM EBITDA                 = Last Twelve Months EBITDA
LTM Free Cash Flow         = LTM Operating CF - LTM CapEx
LTM Interest Expense       = Interest paid in last 12 months
Existing Annual Debt Service = Existing annual interest + principal repayments

Proposed Annual Payment    = [Calculated from loan amount, rate, tenor]
Total Debt Service (post-loan) = Existing service + Proposed payment

DSCR (existing)            = EBITDA / Existing Debt Service
DSCR (post-loan)           = EBITDA / Total Debt Service (post-loan)
Fixed Charge Coverage      = (EBITDA - CapEx) / (Interest + Lease + Principal)
```

### Repayment Capacity Table:
| Repayment Metric | Value | Threshold | Assessment |
|---|---|---|---|
| LTM EBITDA | $Xm | — | — |
| LTM Free Cash Flow | $Xm | — | — |
| Existing Annual Debt Service | $Xm | — | — |
| DSCR (pre-proposed loan) | X.Xx | >1.5x | ✅/🟡/❌ |
| Proposed Annual Loan Payment | $Xm | — | — |
| DSCR (post-proposed loan) | X.Xx | >1.25x | ✅/🟡/❌ |
| Fixed Charge Coverage | X.Xx | >1.2x | ✅/🟡/❌ |
| Loan / EBITDA Multiple | X.Xx | <3.0x | ✅/🟡/❌ |

### Loan Amortization Schedule (Base Case):
| Year | Opening Balance | Interest | Principal | Closing Balance | Annual Payment |
|---|---|---|---|---|---|
| Year 1 | $Xm | $Xm | $Xm | $Xm | $Xm |
| Year 2 | | | | | |
| Year 3 | | | | | |
| [etc.] | | | | | |
| **Total** | — | **$Xm** | **$Xm** | — | **$Xm** |

---

## Section 3: Debt & Credit Profile

### Required Calculations:
```
Debt-to-Income Ratio     = Total Annual Debt Service / Gross Annual Income
Total Debt / Revenue     = Total Debt / LTM Revenue
Net Debt / EBITDA        = Net Debt / LTM EBITDA
Interest Coverage Ratio  = EBIT / Interest Expense
```

### Existing Debt Summary:
| Facility | Outstanding | Maturity | Annual Service | Rate | Priority |
|---|---|---|---|---|---|
| Facility A | $Xm | YYYY | $Xm | X.X% | Senior Secured |
| Facility B | $Xm | YYYY | $Xm | X.X% | Unsecured |
| **Total Existing** | **$Xm** | — | **$Xm** | — | — |
| **Proposed Loan** | **$Xm** | **YYYY** | **$Xm** | **X.X%** | **TBD** |
| **Pro-forma Total** | **$Xm** | — | **$Xm** | — | — |

---

## Section 4: Macro & Market Sensitivity

### Macro Factors to Assess:
1. **Interest Rate Environment:** Is proposed loan fixed or floating? If floating, stress test +200bps
2. **Inflation Impact:** What % of costs are inflation-sensitive? How does margin compress?
3. **Currency Risk:** If company has foreign revenue/costs, assess FX exposure
4. **Economic Cycle Sensitivity:** How cyclical is the company's revenue?
5. **Sector Tailwinds/Headwinds:** Current sector health and near-term outlook

### Stress Test Analysis:

> 📊 *[Embed: chart_dscr_stress.png — DSCR Stress Test: Base / Downside / Severe]*

| Scenario | Revenue Assumption | EBITDA Margin | Annual Debt Service | DSCR | Verdict |
|---|---|---|---|---|---|
| **Base Case** | LTM flat to +5% | Current margin | $Xm | X.Xx | ✅ Serviceable |
| **Downside Case** | -15% decline | -2pp margin compression | $Xm | X.Xx | 🟡 Tight |
| **Severe Stress** | -30% decline | -5pp margin compression | $Xm | X.Xx | ❌ Breach |

Write a specific narrative paragraph: *"Under the base case, the proposed loan can comfortably be serviced with a DSCR of X.Xx. However, if revenue were to decline by 30% (consistent with [2008 GFC / COVID-2020 / relevant benchmark]), DSCR would fall to X.Xx, below the 1.0x threshold. [Mitigants: cash buffer on balance sheet / covenant trigger mechanism / management response plan]."*

---

## Section 5: Repayment Risk Summary

### Final Repayment Opinion:
State clearly:
1. Whether current cash flows are sufficient to service proposed debt
2. The cushion margin (how far DSCR is above/below threshold)
3. Key conditions that could threaten repayment
4. Recommended structural protections

### Recommended Loan Covenants:
| Covenant | Threshold | Rationale |
|---|---|---|
| Minimum DSCR | >1.25x (test quarterly) | Ensures adequate repayment buffer |
| Maximum Net Debt/EBITDA | <3.5x | Limits re-leveraging post-close |
| Minimum Cash Balance | $Xm | Protects against short-term liquidity stress |
| Dividend Restriction | If DSCR <1.5x | Protects cash for debt service priority |
| Annual Financial Reporting | Within 120 days of FYE | Lender monitoring |
| Quarterly Management Accounts | Within 45 days of quarter end | Early warning |
| Material Event Notification | Within 5 business days | Covenant breach, M&A, litigation, leadership change |
| CapEx Cap | $Xm per year without lender consent | Prevents unplanned cash drain |
