---
name: industry
description: Generate a standalone industry analysis report for a given sector or for the industry of a named company. Can be run independently or as a preparatory step before a full Credit Memo.
---

# Command: /credit-memo:industry

## Purpose
Generate a standalone Industry Analysis report for a given sector or for the industry of a named company. Can be used independently or as a preparatory step before a full Credit Memo.

---

## Trigger
- `/credit-memo:industry`
- "Give me an industry snapshot for [industry / company]"
- "What's the industry outlook for [sector]?"
- "Run industry analysis for [Company]'s sector"
- "What does the [industry] landscape look like?"

---

## Required Inputs
- Either: Company Name (industry auto-detected) OR Industry Name directly
- [Optional] Geography focus (Global / US / India / APAC / EU)
- [Optional] Depth: Summary (1 page) or Detailed (3–5 pages)

---

## Execution Steps

### STEP 0 — Invoke Guardrails
Invoke `guardrails` skill (Layer 1: Session Initialization) before any data collection.

### STEP 1 — Industry Identification
If company name given → identify their primary industry/sector.
Confirm with user: *"I've identified [Company] operates in [Industry]. Is that correct?"*

### STEP 2 — Data Collection
Invoke `guardrails` skill (Layer 3: Data Provenance) after data collection — tag every data point with source name, confidence level, and data-as-of date.

Pull from:
- Spherical Insights: Market size, CAGR, forecast
- SerpApi: Analyst reports, industry news (use Google News endpoint if key configured)
- SEC EDGAR: Industry-wide 10-K filings for context
- Web: Competitor data, market share, industry associations

### STEP 3 — Analysis Output
Return in chat AND optionally generate a `.docx` section:

**Industry Overview**
- Sector definition and scope
- Market size (current year, 5-year forecast)
- CAGR and growth trajectory
- Key growth drivers and headwinds
- Industry lifecycle stage (Emerging / Growth / Mature / Declining)

**Competitive Landscape**
- Top 5–10 industry players with market share table
- Named company's market position (if applicable)
- Barriers to entry

**SWOT Analysis Table**
| Strengths | Weaknesses |
|---|---|
| ... | ... |

| Opportunities | Threats |
|---|---|
| ... | ... |

**Key Metrics**
- Market size (USD)
- YoY growth rate
- CAGR (3-year, 5-year)
- Seasonality patterns
- Regulatory environment summary

**Consumer & Demographic Trends**
- Demand shifts
- Demographics driving growth
- Behavioral changes

**Credit Implications**
- Is this a credit-favorable industry? (Low cyclicality, high visibility = better)
- Industry risks that could impair borrower repayment
- Suggested loan covenants tied to industry risk

---

## Output Format
- Chat summary (always)
- [If detailed requested] → `.docx` Industry Snapshot Report
- Filename: `Industry_Snapshot_[Sector]_[Date].docx`

---

## Notes
- Always invoke `guardrails` skill (Layer 5: Output Controls) before delivering any `.docx` report
- If generating a document, include the standard disclaimer page (see guardrails skill Layer 5)
- All market size figures are estimates from third-party research; tag confidence level per Layer 3 rules

---

> ⚠️ **AI-GENERATED RESEARCH AID — NOT FINANCIAL ADVICE**
> Industry data is AI-generated from publicly available reports and web search. It does not constitute financial advice, investment advice, or a credit recommendation. Market size figures are estimates and must be independently verified against primary sources before use in any credit presentation or lending decision. All outputs require review by a qualified credit professional.
