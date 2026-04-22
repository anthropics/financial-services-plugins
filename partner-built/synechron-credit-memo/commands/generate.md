---
name: generate
description: Generate a complete Credit Memorandum with full financial, risk, repayment, industry, and management analysis. Outputs Word (.docx), PDF, and PowerPoint files with 10 embedded charts. Supports public and private companies.
---

# Command: /credit-memo:generate

## Purpose
Generate a complete, professional Credit Memorandum. Outputs three files: Word (.docx), PDF, and PowerPoint (.pptx). Includes rich visuals, charts, and tables. Supports both public and private companies. Uses authenticated API calls when SERP and SEC keys are configured.

---

## Trigger
- `/credit-memo:generate`
- "Generate a credit memo for [Company]"
- "Run credit analysis for [Company], loan amount $X"
- "Create a credit memorandum for [Company]"

---

## STEP 0 — Invoke Guardrails
Before anything else, invoke the `guardrails` skill (Layer 1: Session Initialization).

---

## STEP 1 — Read API Configuration
Check for `config/config.local.md` in the plugin folder.
- If found → extract SERPAPI_KEY and SEC_EDGAR_KEY and use in all data calls
- If not found → proceed without keys (lower rate limits, some endpoints restricted)
- Never expose key values in output or logs — only confirm presence

---

## STEP 2 — Collect Basic Inputs

Ask the user:
```
📋 CREDIT MEMO — Quick Setup
─────────────────────────────────────────
1. Company name (full legal name preferred)
2. Loan amount required (USD)
3. Purpose of loan
4. [Optional] Loan tenor / repayment period
5. [Optional] Collateral offered
6. [Optional] Internal credit rating (if your org has rated this borrower)
─────────────────────────────────────────
Is this company publicly listed? (Yes / No / Not sure)
```

*Invoke `guardrails` skill (Layer 2: Input Validation) on collected inputs.*

---

## STEP 3 — Public vs. Private Company Routing

### If PUBLIC company:
Proceed directly to Step 4 — full automated data collection.

### If PRIVATE company:
Display this message:
```
⚠️  PRIVATE COMPANY DETECTED
──────────────────────────────────────────────────────────
For private companies, financial data is not publicly filed.
To generate the most accurate Credit Memo, please upload
any available documents:

HIGHLY RECOMMENDED:
  📄 Audited Financial Statements (last 3 years)
  📄 Management Accounts / Unaudited Financials
  📄 Tax Returns (last 2–3 years)
  📄 Bank Statements (last 12 months)
  📄 Business Plan or Investor Deck
  📄 Existing loan agreements or debt schedule
  📄 Accounts Receivable / Payable aging report

OPTIONAL BUT USEFUL:
  📄 Industry reports or market research
  📄 Any existing credit assessments
  📄 Org chart / management bios

──────────────────────────────────────────────────────────
🔒 DATA PRIVACY NOTICE
Uploaded documents are processed within your Cowork session
and are not transmitted to third parties. Handle all uploads
in accordance with your organization's data classification
policies. Do not upload documents marked SECRET or above
your organization's permitted sharing threshold.
──────────────────────────────────────────────────────────
Upload what you have, then type CONTINUE.
For any missing data, I will search the web and flag gaps.
──────────────────────────────────────────────────────────
```

**After user uploads or types CONTINUE:**
- Ingest all uploaded documents (PDFs, Excel, Word, CSV)
- Extract financial data from uploaded files
- For any missing data point → attempt web search fallback
- Tag every data point: `[FROM UPLOAD]` or `[WEB ESTIMATE]` or `[NOT AVAILABLE]`
- Add disclaimer: *"This analysis is based on management-provided financials and/or web-sourced estimates. Independent verification is strongly recommended before credit approval."*

---

## STEP 4 — Data Collection
*(Invoke `data-collection` skill)*

Show live progress:
```
🔍 COLLECTING DATA — [Company Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SEC EDGAR        — 10-K (2019–2023), 10-Q Q3 2024, 3× 8-K
✅ Stock Analysis   — 5-year income stmt, balance sheet, cash flow
✅ Macrotrends      — 10-year revenue & margin history
✅ Moody's          — Baa2 (Stable) as of Nov 2023
✅ S&P Global       — BBB (Stable) as of Oct 2023
✅ Fitch            — BBB- (Negative Watch) as of Sep 2023
✅ SerpApi/News     — 52 articles, 3 risk flags identified
✅ Spherical Insights — Industry: $142bn market, 8.3% CAGR
⚠️  Refinitiv        — Key not configured (skipped)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Data collection complete. Running analysis...
```

*Invoke `guardrails` skill (Layer 3: Data Provenance Check) on collected data.*

---

## STEP 5 — Run All Analysis Skills in Parallel
Invoke simultaneously:
1. `financial-analysis` skill — 3–5 year Income, Balance Sheet, Cash Flow
2. `risk-assessment` skill — Ratings, liquidity, leverage, legal, internal rating
3. `repayment-analysis` skill — DSCR, CCC, stress testing
4. `industry-analysis` skill — SWOT, market size, CAGR, competitors
5. `management-assessment` skill — Exec profiles, governance
6. `visuals` skill — Generate all 10 charts

---

## STEP 6 — Generate Three Output Files
*(Invoke `document-generation` skill)*

Generate in this order:
1. **Word (.docx)** — Full detailed memo, all sections, all tables, embedded charts
2. **PDF** — Converted from Word; CONFIDENTIAL diagonal watermark; editing locked
3. **PowerPoint (.pptx)** — Executive summary deck, 15–20 slides, visual-first

File naming:
```
Credit_Memo_[CompanyName]_[YYYY-MM-DD].docx
Credit_Memo_[CompanyName]_[YYYY-MM-DD].pdf
Credit_Memo_[CompanyName]_[YYYY-MM-DD]_Deck.pptx
```

*Invoke `guardrails` skill (Layer 5: Output Controls) before delivering files.*

---

## STEP 7 — Deliver

Present all three files and show key findings summary:
```
✅ CREDIT MEMO COMPLETE — [Company Name]
══════════════════════════════════════════════════════════
DEAL SNAPSHOT
  Loan Request   : USD [Amount] | [Purpose]
  Tenor          : [X years]

KEY METRICS
  Revenue (LTM)  : $X.Xbn  (+X.X% YoY)
  EBITDA Margin  : X.X%
  Net Debt/EBITDA: X.Xx
  DSCR           : X.Xx  [✅ Above 1.25x threshold]

CREDIT RATINGS
  Moody's        : Baa2  (Stable)
  S&P            : BBB   (Stable)
  Fitch          : BBB-  (Negative Watch)  ⚠️
  Internal Rating: [If provided]

AI-ASSISTED PRELIMINARY ASSESSMENT
  ✅ SUPPORTIVE / 🟡 CONDITIONAL / ❌ CONCERNS IDENTIFIED

⚠️  DISCLAIMER ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This Credit Memorandum is AI-generated and intended solely
as a research and analytical aid. It does NOT constitute
financial advice or a credit recommendation. All outputs
must be reviewed and approved by a qualified credit
professional before any lending decision is made.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OUTPUTS
  📄 Word  : Credit_Memo_[Company]_[Date].docx
  📄 PDF   : Credit_Memo_[Company]_[Date].pdf
  📊 Deck  : Credit_Memo_[Company]_[Date]_Deck.pptx
══════════════════════════════════════════════════════════
```
