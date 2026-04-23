---
name: credit-memo-financial-analysis
description: Performs deep financial analysis of a company for credit assessment purposes. Covers Income Statement Analysis, Balance Sheet Analysis, and Cash Flow Analysis over 3–5 years. Generates human-readable commentary, calculates key financial ratios, identifies trends, flags concerns, and benchmarks against industry-adjusted averages. Claude draws on this skill automatically when analyzing financials for a Credit Memo.
---

# Credit Memo — Financial Analysis Skill

## Overview
This skill defines how to analyze 3–5 years of financial data to assess creditworthiness. The output should be analytical, not just descriptive — interpret what the numbers mean for repayment risk.

---

## Guiding Principle
**Never just report numbers. Always interpret them.**
Instead of: *"Revenue was $5.2bn in 2023"*
Write: *"Revenue grew 12% YoY to $5.2bn in 2023, driven by [X], reflecting the company's ability to grow organically despite [macro headwind]. This trajectory supports adequate cash generation for debt service."*

---

## Sector-Specific Ratio Thresholds

Apply the appropriate industry benchmarks based on the company's primary sector. Do not apply manufacturing thresholds to a SaaS company, or retail thresholds to real estate.

### Manufacturing
| Ratio | Strong | Adequate | Watch | Risk |
|---|---|---|---|---|
| Current Ratio | >2.5x | 1.5–2.5x | 1.0–1.5x | <1.0x |
| Net Debt/EBITDA | <2.0x | 2.0–3.0x | 3.0–4.0x | >4.0x |
| Interest Coverage | >6x | 4–6x | 2–4x | <2x |
| EBITDA Margin | >20% | 12–20% | 8–12% | <8% |
| CapEx/Revenue | <5% | 5–10% | 10–15% | >15% |

### SaaS / Technology
| Ratio | Strong | Adequate | Watch | Risk |
|---|---|---|---|---|
| Current Ratio | >3.0x | 2.0–3.0x | 1.0–2.0x | <1.0x |
| Net Debt/EBITDA | <1.5x | 1.5–3.0x | 3.0–5.0x | >5.0x |
| Interest Coverage | >8x | 5–8x | 3–5x | <3x |
| EBITDA Margin | >30% | 15–30% | 5–15% | <5% |
| Rule of 40 (Rev Growth% + EBITDA%) | >50 | 40–50 | 30–40 | <30 |
| Gross Margin | >70% | 60–70% | 50–60% | <50% |

### Retail / Consumer
| Ratio | Strong | Adequate | Watch | Risk |
|---|---|---|---|---|
| Current Ratio | >2.0x | 1.2–2.0x | 0.8–1.2x | <0.8x |
| Net Debt/EBITDA | <2.5x | 2.5–3.5x | 3.5–5.0x | >5.0x |
| Interest Coverage | >5x | 3–5x | 1.5–3x | <1.5x |
| EBITDA Margin | >12% | 7–12% | 4–7% | <4% |
| Inventory Days (DIO) | <45 days | 45–75 days | 75–100 days | >100 days |
| Same-Store Sales Growth | >4% | 1–4% | 0–1% | <0% |

### Real Estate / REITs
| Ratio | Strong | Adequate | Watch | Risk |
|---|---|---|---|---|
| LTV (Loan-to-Value) | <40% | 40–55% | 55–65% | >65% |
| Debt Service Coverage | >2.0x | 1.5–2.0x | 1.2–1.5x | <1.2x |
| FFO/Debt | >20% | 12–20% | 8–12% | <8% |
| Interest Coverage | >3x | 2–3x | 1.5–2x | <1.5x |
| Occupancy Rate | >95% | 88–95% | 80–88% | <80% |
| Cap Rate vs. Borrowing Rate | Spread >200bps | 100–200bps | 50–100bps | <50bps |

### Healthcare
| Ratio | Strong | Adequate | Watch | Risk |
|---|---|---|---|---|
| Current Ratio | >2.5x | 1.5–2.5x | 1.0–1.5x | <1.0x |
| Net Debt/EBITDA | <2.5x | 2.5–4.0x | 4.0–5.5x | >5.5x |
| Interest Coverage | >5x | 3–5x | 2–3x | <2x |
| EBITDA Margin | >18% | 10–18% | 5–10% | <5% |
| Days Sales Outstanding (DSO) | <45 days | 45–65 days | 65–90 days | >90 days |

### Energy (Oil & Gas / Utilities)
| Ratio | Strong | Adequate | Watch | Risk |
|---|---|---|---|---|
| Net Debt/EBITDA | <2.0x | 2.0–3.5x | 3.5–5.0x | >5.0x |
| Interest Coverage | >5x | 3–5x | 2–3x | <2x |
| EBITDA Margin | >35% | 20–35% | 10–20% | <10% |
| Debt/Proved Reserves | <$10/BOE | $10–15/BOE | $15–20/BOE | >$20/BOE |
| Dividend Coverage (FCF/Dividends) | >2x | 1.5–2x | 1.0–1.5x | <1.0x |

**When sector is unclear or spans multiple categories:** Apply the more conservative thresholds of the two most relevant sectors and note the approach.

---

## Section 1: Financial Overview Summary

Lead with a concise 2–3 paragraph executive narrative covering:
- Overall financial health in plain English
- Most significant trends (positive and negative)
- Key ratios that matter most for credit decision
- Whether financials support the loan request

---

## Section 2: Income Statement Analysis

### Questions to Answer:
- What are the firm's revenue and profit trends over 3–5 years?
- What are gross profit margin, operating margin, and net margin?
- How does profitability compare to sector benchmarks?
- What is the EBITDA trajectory and what drives it?
- Are there significant cost structure changes?
- What are the historical growth rates in revenue and profit?

### Required Calculations:
```
Gross Profit Margin     = (Gross Profit / Revenue) × 100
Operating Margin        = (Operating Income / Revenue) × 100
Net Profit Margin       = (Net Income / Revenue) × 100
EBITDA Margin           = (EBITDA / Revenue) × 100
Revenue Growth (YoY)    = ((Current Revenue - Prior Revenue) / Prior Revenue) × 100
Cost of Revenue %       = (COGS / Revenue) × 100
SG&A as % of Revenue    = (SG&A / Revenue) × 100
R&D as % of Revenue     = (R&D / Revenue) × 100
```

> 📊 *[Embed: chart_revenue_ebitda.png — Revenue & EBITDA Margin (5-Year Trend)]*
> 📊 *[Embed: chart_margins.png — Gross / Operating / Net Margin Trend vs. Industry]*

### Required Table Format:
| Metric | FY2019 | FY2020 | FY2021 | FY2022 | FY2023 | Trend |
|---|---|---|---|---|---|---|
| Revenue ($M) | | | | | | ↑/↓/→ |
| Revenue Growth % | | | | | | |
| Gross Profit ($M) | | | | | | |
| Gross Margin % | | | | | | |
| EBITDA ($M) | | | | | | |
| EBITDA Margin % | | | | | | |
| Operating Income ($M) | | | | | | |
| Operating Margin % | | | | | | |
| Net Income ($M) | | | | | | |
| Net Margin % | | | | | | |
| Sector Avg Net Margin | | | | | | (benchmark) |

### Commentary Framework (5 sentences minimum):
1. Revenue trajectory and primary drivers
2. Margin trends and operational efficiency implications
3. Comparison to sector benchmarks — above/below and why
4. Any anomalies, one-time items, or accounting concerns
5. Direct implication for loan repayment capacity

---

## Section 3: Balance Sheet Analysis

### Required Calculations:
```
Current Ratio           = Current Assets / Current Liabilities
Quick Ratio             = (Current Assets - Inventory) / Current Liabilities
Cash Ratio              = Cash & Equivalents / Current Liabilities
Debt-to-Equity Ratio    = Total Debt / Total Shareholders' Equity
Net Debt                = Total Debt - Cash & Equivalents
Net Debt / EBITDA       = Net Debt / EBITDA
Interest Coverage       = EBIT / Interest Expense
Working Capital         = Current Assets - Current Liabilities
Asset Turnover          = Revenue / Average Total Assets
Return on Assets (ROA)  = Net Income / Average Total Assets
Return on Equity (ROE)  = Net Income / Average Shareholders' Equity
```

### Required Table Format:
| Metric | FY2021 | FY2022 | FY2023 | Sector Avg | Signal |
|---|---|---|---|---|---|
| Current Ratio | | | | [from sector table] | 🟢/🟡/🔴 |
| Quick Ratio | | | | [from sector table] | 🟢/🟡/🔴 |
| Total Debt ($M) | | | | | |
| Total Equity ($M) | | | | | |
| Debt/Equity | | | | | 🟢/🟡/🔴 |
| Net Debt ($M) | | | | | |
| Net Debt/EBITDA | | | | [from sector table] | 🟢/🟡/🔴 |
| Interest Coverage | | | | [from sector table] | 🟢/🟡/🔴 |
| ROA % | | | | | |
| ROE % | | | | | |

**Apply sector-specific thresholds from the table above for Signal column.**

---

## Section 4: Cash Flow Analysis

### Required Calculations:
```
Free Cash Flow (FCF)    = Operating Cash Flow - Capital Expenditures
FCF Margin              = FCF / Revenue × 100
CapEx Intensity         = CapEx / Revenue × 100
Cash Conversion         = Operating CF / Net Income  (>1 = good quality earnings)
Debt Service Coverage   = EBITDA / (Interest + Principal Repayments)
```

> 📊 *[Embed: chart_cashflow_waterfall.png — Cash Flow Waterfall (Latest Year)]*

### Required Table Format:
| Cash Flow Metric ($M) | FY2021 | FY2022 | FY2023 | Trend |
|---|---|---|---|---|
| Operating Cash Flow | | | | |
| CapEx | | | | |
| Free Cash Flow | | | | |
| Investing Activities | | | | |
| Financing Activities | | | | |
| Net Change in Cash | | | | |
| FCF Margin % | | | | |
| Cash & Equivalents (EoP) | | | | |

### Commentary Framework:
1. Quality of earnings: Is operating CF consistently above net income?
2. FCF trend and debt serviceability implications
3. Are investing outflows for growth or maintenance?
4. Are financing activities showing debt paydown or accumulation?
5. Can the company generate enough cash to service the proposed loan?

---

## Debt Service Coverage Analysis
```
Annual Debt Service     = Annual Interest Payment + Annual Principal Repayment
DSCR                    = Net Operating Income / Total Debt Service
```

Apply sector-adjusted DSCR thresholds:
- Standard: >1.5x = Strong; 1.25–1.5x = Adequate; 1.0–1.25x = Tight; <1.0x = Insufficient
- Real Estate: >2.0x = Strong; 1.5–2.0x = Adequate; 1.2–1.5x = Watch; <1.2x = Risk

Write a specific paragraph: *"Based on current EBITDA of $Xm and the proposed loan structure of $Xm at X% over X years, annual debt service would be approximately $Xm, resulting in a DSCR of X.Xx, which [is/is not] sufficient under [sector] benchmarks."*

---

## Red Flags — Call Out Explicitly
- Declining revenue for 2+ consecutive years
- EBITDA margin compression >3pp year-over-year
- Negative free cash flow for 2+ years
- Net Debt/EBITDA exceeding sector "Risk" threshold
- Interest coverage ratio below sector "Watch" threshold
- Qualified audit opinion or material weakness disclosure
- Significant related-party transactions
- Goodwill impairment charges
- Rapid inventory build without corresponding revenue growth
- Cash conversion ratio consistently <0.8x (earnings quality concern)
- Frequent changes in accounting policies
