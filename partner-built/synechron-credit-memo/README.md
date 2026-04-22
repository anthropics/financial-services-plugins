# Credit Memo Generation

*Partner plugin by [Synechron Technologies](https://www.synechron.com)*

Generate professional Credit Memorandums for commercial lending — from data collection through finished deliverable. Supports public and private companies with Word, PDF, and PowerPoint output including 10 embedded charts.

## Install

```
claude plugin install credit-memo@financial-services-plugins
```

Or install from [claude.com/plugins](https://claude.com/plugins/).

## What It Does

This plugin automates the end-to-end credit memo workflow that commercial lending teams perform for every deal:

- **Data Collection** — Pulls 3–5 years of financial data from SEC EDGAR, SerpApi, and public financial sources. Private companies are supported via document upload with web fallback.
- **Financial Analysis** — Income statement, balance sheet, and cash flow analysis with trend interpretation, ratio calculations, and industry benchmarking.
- **Risk Assessment** — External credit ratings (Moody's, S&P, Fitch), internal rating ingestion, liquidity, leverage, litigation, and operational risk scoring.
- **Repayment Analysis** — DSCR, cash conversion cycle, working capital, and stress-tested repayment schedules under base and downside scenarios.
- **Industry Analysis** — Market size, CAGR, competitive landscape, SWOT, regulatory environment, and credit implications.
- **Management Assessment** — Executive profiles, tenure, governance structure, track record, and strategic execution.
- **Document Generation** — Word (.docx) full memo (25–45 pages), PDF with CONFIDENTIAL watermark, and PowerPoint executive summary deck (15–20 slides) — all with 10 embedded charts.

## Commands

| Command | What it does |
|---|---|
| `/credit-memo:setup` | Validate API keys and check data source connectivity |
| `/credit-memo:generate` | Full Credit Memo — Word + PDF + PowerPoint with 10 charts |
| `/credit-memo:quick-risk` | 2-minute preliminary risk screen for initial deal screening |
| `/credit-memo:industry` | Standalone industry analysis report |
| `/credit-memo:refresh` | Re-fetch latest data and flag changes since last memo |

## Skills

| Skill | Triggers automatically when... |
|---|---|
| `data-collection` | Claude needs to gather financial data for a borrower |
| `financial-analysis` | Analyzing income, balance sheet, or cash flow data |
| `risk-assessment` | Evaluating credit risk, ratings, or default probability |
| `repayment-analysis` | Assessing loan repayment capacity or DSCR |
| `industry-analysis` | Analyzing sector context, market size, or competitive position |
| `management-assessment` | Evaluating management quality or governance |
| `visuals` | Financial data is ready to be charted (10 chart types) |
| `document-generation` | Analysis is complete and output files need to be produced |
| `guardrails` | Every command invocation — enforces 5-layer compliance |

## Charts Generated

Every full credit memo includes these 10 charts embedded in all output formats:

1. Revenue & EBITDA Trend (5-Year)
2. Profit Margins vs. Industry Benchmark
3. Cash Flow Waterfall
4. Balance Sheet Composition
5. Key Financial Ratios Dashboard (Traffic Light)
6. Credit Rating Scale Visual
7. Industry Market Size & Growth
8. SWOT Matrix (4-quadrant)
9. DSCR Stress Test (3 scenarios)
10. Management Tenure Timeline

## Data Sources

### Built-in (no configuration required)

| Source | Usage |
|---|---|
| SEC EDGAR | 10-K, 10-Q, 8-K filings (User-Agent header required) |
| SerpApi | Web, news, and finance search (free tier: 100 searches/month) |
| Stock Analysis | Financial statements and ratios |
| Macrotrends | 10-year historical data |
| DiscoverCI | Company intelligence |
| Spherical Insights | Market size and industry forecasts |

### Configurable premium sources

Add API keys to `config/config.local.md` to enable:

| Provider | What it unlocks |
|---|---|
| Bloomberg Terminal | Real-time data, full financials, ratings |
| Refinitiv / LSEG Eikon | Financial statements, estimates, news |
| FactSet | Standardized financials, estimates, ownership |
| S&P Capital IQ | Private company data, credit scores |
| PitchBook | Private company financials, VC/PE deal data |

## Setup

1. Copy `config/config.template.md` to `config/config.local.md`
2. Add your SerpApi key and SEC EDGAR User-Agent string
3. Run `/credit-memo:setup` to verify connectivity

The plugin works without API keys (lower rate limits, some endpoints restricted).

## Private Company Support

When a private company is detected, the plugin prompts for document uploads (financial statements, tax returns, bank statements) and falls back to web search for missing data. All data points are tagged with their source:

- `[FROM UPLOAD]` — extracted from uploaded documents
- `[WEB ESTIMATE]` — sourced from web search
- `[NOT AVAILABLE]` — not found from any source

## Customization

- **Swap data sources** — Edit `.mcp.json` to add your firm's internal systems or premium data providers
- **Add internal rating scales** — Configure your organization's rating taxonomy in `config/config.local.md`
- **Adjust thresholds** — Modify sector-specific ratio thresholds in the financial-analysis skill
- **Connect internal systems** — REST API, MCP, or CSV lookup for internal databases, CRM, and document management

## Guardrails

The plugin enforces a 5-layer compliance system that cannot be bypassed:

1. **Session Initialization** — Disclaimer display, config validation
2. **Input Validation** — Prevents injection, validates company identifiers
3. **Data Provenance** — Tags every data point with source, confidence, and retrieval date
4. **Financial Advice Boundaries** — Blocks definitive lending recommendations; all outputs framed as analytical aids
5. **Output Controls** — Enforces disclaimers, watermarks, and citation appendix on all deliverables

## Disclaimer

This plugin is an AI-assisted research tool. All Credit Memorandums, risk assessments, and analyst recommendations require review by a qualified credit professional before any lending decision. This plugin does not constitute financial advice.

See [DISCLAIMER.md](./DISCLAIMER.md) for full terms.

---

*Built by [Synechron Technologies](https://www.synechron.com) — BFSI technology consulting*
