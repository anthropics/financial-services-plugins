---
description: Analyze a stock using Wind data (A-shares, HK, US-listed Chinese companies)
argument-hint: "[stock code or company name, e.g. 600519.SH or 贵州茅台]"
---

# Wind Equity Analysis Command

Build a comprehensive equity analysis using Wind Financial Terminal data.

## Workflow

### Step 1: Identify the Security

If a stock code or company name is provided, use it. Otherwise ask:
- "What company would you like to analyze? Please provide a Wind code (e.g. 600519.SH) or company name."

### Step 2: Load Wind Equity Analysis Skill

Use `skill: "wind-equity-analysis"` to perform the analysis:

1. **Company Profile** — Use `wind_wss` for latest snapshot:
   - Name, sector (申万), listing date, market cap
   - Valuation multiples: PE, PB, PS, EV/EBITDA
   - Latest financials: revenue, profit, margins, ROE
   - Growth rates: revenue YoY, profit YoY

2. **Historical Trends** — Use `wind_wsd` for 3-year history:
   - Quarterly revenue and profit trend
   - Valuation band (PE/PB range)
   - Price performance vs sector index

3. **Peer Comparison** — Use `wind_wss` with peer codes:
   - Identify 4-6 peers in same 申万二级行业
   - Compare valuation, growth, profitability
   - Statistical summary (median, quartiles)

### Step 3: Create Output

Generate:
1. **Excel file** with company profile, historical data, and peer comparison tabs
2. **Summary** with key findings: valuation position vs peers, growth trajectory, key risks

### Step 4: Additional Context (Optional)

If relevant, add macro context using `wind_edb`:
- Industry-relevant macro indicators
- Policy rate environment
- Sector-specific drivers
