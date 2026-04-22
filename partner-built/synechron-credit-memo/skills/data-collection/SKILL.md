---
name: credit-memo-data-collection
description: Orchestrates data collection for Credit Memo generation. Reads API keys from config.local.md and uses them for authenticated calls to SerpApi and SEC EDGAR. Handles both public companies (automated collection) and private companies (upload ingestion + web fallback). Always collects 3-5 years of financial data minimum.
---

# Data Collection Skill

## Overview
This skill defines where to get data, how to authenticate, how to handle private companies, and how to tag data confidence. Always collect **minimum 3 years, target 5 years** of financial history. Every data point must be tagged with source and confidence level before being passed to analysis skills.

---

## API Key Usage

### Reading Keys
At session start, read `config/config.local.md` if it exists:
```
SERPAPI_KEY     → use in all SerpApi calls as &api_key={value}
SEC_EDGAR_KEY   → use as User-Agent header in all EDGAR requests
```
If keys are not found or are placeholders, proceed without them and note rate limit restrictions.

**Never echo or log key values — only confirm presence.**

### SEC EDGAR User-Agent — Important Format Note
The SEC EDGAR key is **not a traditional API key or password**. It is a courtesy User-Agent string that the SEC requires for higher-rate access. The correct format is:

```
User-Agent: OrganizationName contact@youremail.com
```

Example: `User-Agent: Acme Credit Team analyst@acmebank.com`

If the configured value looks like a hex string (no space, no `@`), warn the user before making EDGAR calls:
```
⚠️ SEC_EDGAR_KEY format appears incorrect.
Expected format: "OrganizationName contact@email.com"
Current value looks like a hash or token — EDGAR may reject this.
Please update config.local.md and run /credit-memo:setup.
Proceeding with standard rate limits.
```

### With SERPAPI_KEY (authenticated):
- Rate limit: up to 15,000 searches/month depending on plan
- Access: Google Finance, Google News, Google Scholar, Bing News
- Better results: less bot-blocking, more consistent data

Append to every SerpApi URL:
```
&api_key={SERPAPI_KEY}&num=10&hl=en&gl=us
```

Useful SerpApi endpoints with key:
```
Google Search:  engine=google&q={query}
Google Finance: engine=google_finance&q={TICKER}:NASDAQ
Google News:    engine=google_news&q={company}+credit+rating
Yahoo Finance:  engine=yahoo_finance_search&p={company}
```

### With SEC_EDGAR_KEY (valid User-Agent):
Use as User-Agent header on all EDGAR requests:
```
User-Agent: {SEC_EDGAR_KEY}
```

EDGAR endpoints to use:
```
# Full-text search across filings
https://efts.sec.gov/LATEST/search-index?q="{company}"&forms=10-K,10-Q,8-K&dateRange=custom&startdt={year-4}-01-01&enddt={current_year}-12-31

# Company CIK lookup
https://www.sec.gov/cgi-bin/browse-edgar?company={company}&CIK=&type=10-K&action=getcompany

# Direct filing access once CIK known
https://data.sec.gov/submissions/CIK{cik_padded}.json
```

---

## Data Source Notes & Terms of Service

The following sources are used for data collection. Claude should be aware that automated access may be subject to each source's Terms of Service:

| Source | Access Type | Notes |
|---|---|---|
| SEC EDGAR | Official public API | Free; requires User-Agent header per SEC guidelines |
| SerpApi | Paid API | Legitimate API access; rate limits per plan |
| Stock Analysis (stockanalysis.com) | Web scraping | For informational use; verify ToS compliance |
| Macrotrends (macrotrends.net) | Web scraping | For informational use; verify ToS compliance |
| DiscoverCI (discoverci.com) | Web scraping | For informational use; verify ToS compliance |
| Spherical Insights | Web scraping | Market reports; verify ToS compliance |

If your organization requires strict ToS compliance, consider substituting scraping-based sources with licensed data providers (Bloomberg, Refinitiv, FactSet).

---

## Financial Data — Time Period Rules

**ALWAYS collect minimum 3 years. Target 5 years.**

| Data Type | Minimum | Target | Source Priority |
|---|---|---|---|
| Annual Income Statement | 3 years | 5 years | SEC 10-K → Stock Analysis → Macrotrends |
| Annual Balance Sheet | 3 years | 5 years | SEC 10-K → Stock Analysis |
| Annual Cash Flow | 3 years | 5 years | SEC 10-K → Stock Analysis |
| Quarterly Financials | 4 quarters | 8 quarters | SEC 10-Q |
| Credit Ratings History | 2 years | 5 years | Web search |
| News & Events | 12 months | 24 months | SerpApi |

When collecting, always note the year range retrieved: *"Financial data covers FY2019–FY2023 (5 years)."*

---

## Public Company Data Collection

### Phase 1: Identity Resolution
```
Search: "{company name}" stock ticker SEC CIK
→ Extract: Ticker symbol, CIK number, exchange, SIC code, fiscal year end
```

### Phase 2: SEC EDGAR (Primary — most authoritative)
Pull with authenticated header if key available:

**10-K Annual Reports (last 5 years):**
- Income Statement: Revenue, COGS, Gross Profit, EBITDA, EBIT, Net Income, EPS
- Balance Sheet: Assets breakdown, Liabilities breakdown, Equity, Cash, Debt (ST + LT)
- Cash Flow: Operating, Investing, Financing, FCF, CapEx
- MD&A section: Management's own analysis and forward guidance
- Notes: Debt covenants, contingent liabilities, related party transactions

**10-Q Quarterly (last 4 quarters):**
- Latest quarterly snapshot for trend analysis
- Any guidance updates or restatements

**8-K Material Events (last 24 months):**
- Leadership changes, M&A, material litigation, credit amendments, defaults

### Phase 3: Structured Financial Data
Stock Analysis (`https://stockanalysis.com/stocks/{ticker}/financials/`):
- Annual and TTM financial tables
- Key ratios: PE, EV/EBITDA, Debt/Equity, Current Ratio, Quick Ratio, ROE, ROA

Macrotrends (`https://www.macrotrends.net/stocks/charts/{ticker}/`):
- 10-year historical data for trend analysis
- Profit margins history, revenue growth history

### Phase 4: Credit Ratings
SerpApi searches (use Google News endpoint if key available):
```
"{company}" Moody's credit rating 2024 outlook
"{company}" S&P Global rating action 2024
"{company}" Fitch rating downgrade upgrade 2024
"{company}" credit rating history
```
Capture: Agency, rating, outlook, date, rationale, triggers.

### Phase 5: Industry Data
Spherical Insights + SerpApi:
```
"{industry}" market size 2024 billion CAGR forecast
"{industry}" market share leaders 2024
"{company}" market share position 2024
```

### Phase 6: News, Litigation, Management
SerpApi (use Google News if key available):
```
"{company}" lawsuit litigation SEC investigation 2023 2024
"{company}" CEO CFO management change leadership 2024
"{company}" default debt restructuring covenant
"{company}" earnings results revenue guidance 2024
"{company}" acquisition merger strategy 2024
```

---

## Private Company Handling

### Step 1: Ingest Uploaded Documents
For each uploaded file:
- PDF financial statements → extract tables, income/balance/cashflow data
- Excel files → read all sheets, extract financial data
- Word/text documents → extract narrative, management info
- CSV files → parse as financial data

Tag all extracted data: `[FROM UPLOAD — Management Provided]`

### Step 2: Web Fallback for Missing Data
For each data point NOT found in uploads, attempt web search:
```
"{company name}" company overview founded employees headquarters
"{company name}" revenue 2023 2022 annual results
"{industry}" average revenue margins ratios private companies
"{company name}" news 2024
"{company name}" lawsuit litigation court
"{company name}" director CEO background
```

Tag web-sourced data: `[WEB ESTIMATE — Verify independently]`

### Step 3: Data Gap Log
Create a structured gap log (included in Appendix B of output):

| Data Point | Expected | Status | Fallback Used |
|---|---|---|---|
| Revenue FY2021 | $Xm | ⚠️ MISSING | Industry estimate |
| Balance Sheet FY2022 | Full | ✅ FROM UPLOAD | — |
| Credit Rating | Agency rating | ❌ NOT AVAILABLE | Internal only |
| Management Bio CEO | Full bio | 🟡 PARTIAL | LinkedIn/web |

---

## Data Confidence Tagging
Tag every major data point:
```
✅ HIGH    — SEC filing, official agency rating, audited financials
🟡 MEDIUM  — Reputable financial data provider, verified press release
⚠️ LOW     — Web estimate, unaudited management accounts, older than 18 months
❌ MISSING — Not found from any source
[FROM UPLOAD]  — Management-provided, not independently verified
```

**No fabrication rule:** If a data point cannot be found, mark it `❌ MISSING`. Never fill a missing value with a plausible-looking estimate without an explicit `⚠️ LOW` tag and explanation.

---

## Data Freshness Enforcement

**Before finalising collected data, run these checks on every data point:**

### Freshness check protocol:
```
For each data point collected:
  1. Record collected_at = current datetime (ISO 8601)
  2. Record data_as_of = the date the data reflects (e.g. fiscal year end, rating date, article date)
  3. Calculate age = today - data_as_of
  4. Apply freshness rule from table below
  5. Tag accordingly
```

### Freshness rules:
| Data Type | Stale if older than | Action |
|---|---|---|
| Latest quarterly financials | 6 months | ⚠️ STALE — attempt to find updated quarter; flag in output |
| Latest annual financials | 18 months | ⚠️ STALE — flag prominently; note gap year in output |
| Credit ratings | 12 months | ⚠️ POSSIBLY OUTDATED — flag; recommend direct agency check |
| News coverage | 30 days minimum window required | ⚠️ NO RECENT NEWS — note in output |
| Industry market data | 24 months | 🟡 NOTE AS OLDER ESTIMATE in output |
| Management/leadership data | 12 months | 🟡 NOTE; check for recent leadership changes |
| Stock/market data | 1 business day | ⚠️ STALE — always fetch live price/market cap |

### "Latest data" rule — always enforce:
- **ALWAYS** search for the most recent quarter available before using annual-only data
- **ALWAYS** check for any 8-K or press release within the last 30 days that may supersede filed data
- **ALWAYS** check for a rating action or rating watch update within the last 6 months
- **NEVER** use an older data point if a newer one is retrievable — log why if a newer point was unavailable

### Freshness summary object (pass to document generation):
```json
{
  "freshness_summary": {
    "annual_financials_as_of": "FY2025 (Jun 30, 2025)",
    "quarterly_financials_as_of": "Q2 FY2026 (Dec 31, 2025)",
    "credit_ratings_as_of": "Apr 2026",
    "news_coverage_window": "Jan 1, 2026 – Apr 7, 2026",
    "industry_data_as_of": "Q1 2025",
    "management_data_as_of": "Nov 2025",
    "collection_timestamp": "2026-04-07T12:00:00Z",
    "stale_items": ["industry_data"],
    "missing_items": ["fitch_rating", "internal_rating"]
  }
}
```

---

## Output Data Object Structure
```json
{
  "meta": {
    "company": "...",
    "ticker": "...",
    "is_public": true,
    "data_period": "FY2021-FY2025",
    "collection_timestamp": "YYYY-MM-DDTHH:MM:SSZ",
    "api_keys_used": ["serpapi", "sec_edgar"],
    "custom_sources_used": ["bloomberg", "internal_ratings_db"],
    "gaps": ["list of missing data points"],
    "stale_items": ["list of items flagged as stale"],
    "citations": {
      "1": {"source": "Stock Analysis", "url": "https://stockanalysis.com/stocks/msft/financials/", "retrieved": "YYYY-MM-DD"},
      "2": {"source": "S&P Global Ratings", "url": "https://disclosure.spglobal.com/...", "retrieved": "YYYY-MM-DD"}
    }
  },
  "financials": {
    "income_statement": [],
    "balance_sheet": [],
    "cash_flow": [],
    "quarterly": [],
    "ratios": []
  },
  "credit_ratings": {
    "moodys": { "rating": "", "outlook": "", "date": "", "rationale": "" },
    "sp":     { "rating": "", "outlook": "", "date": "", "rationale": "" },
    "fitch":  { "rating": "", "outlook": "", "date": "", "rationale": "" },
    "internal": { "rating": "", "scale": "", "rationale": "", "date": "" }
  },
  "industry": {
    "name": "", "sic_code": "",
    "market_size_usd_bn": 0,
    "cagr_3yr": 0, "cagr_5yr": 0,
    "yoy_growth": 0,
    "top_competitors": [],
    "company_market_share_pct": 0
  },
  "news": {
    "articles": [],
    "sentiment": "positive/neutral/negative",
    "red_flags": []
  },
  "management": {
    "executives": [],
    "board": [],
    "recent_changes": []
  }
}
```
