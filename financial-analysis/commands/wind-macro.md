---
description: Build a China macro economic dashboard using Wind EDB data
argument-hint: "[focus area, e.g. 'growth', 'inflation', 'monetary policy', or blank for full overview]"
---

# Wind Macro Dashboard Command

Build a macroeconomic dashboard using Wind Economic Database.

## Workflow

### Step 1: Determine Focus

If a focus area is provided, narrow the dashboard. Otherwise build a full overview:
- **Full overview**: Growth + Inflation + Monetary + Trade + Real Estate
- **Growth**: GDP, PMI, Industrial VA, FAI, Retail Sales
- **Inflation**: CPI, Core CPI, PPI
- **Monetary policy**: LPR, SHIBOR, M1/M2, New Loans, TSF
- **Trade**: Exports, Imports, Trade Balance, USD/CNY
- **Real estate**: Property investment, sales, new starts
- **China vs US**: Side-by-side macro comparison

### Step 2: Load Wind Macro Dashboard Skill

Use `skill: "wind-macro-dashboard"` to build the analysis:

1. **Pull data** — Use `wind_edb` with relevant indicator codes
   - Default lookback: 2 years for monthly data, 5 years for quarterly
   - Use `Fill=Previous` option to handle missing data points

2. **Build dashboard** with:
   - Latest readings table (indicator, latest value, prior period, YoY change)
   - Time-series data for trend analysis
   - Notable inflection points and commentary

### Step 3: Create Output

Generate:
1. **Excel file** with dashboard data (chart-ready layout)
2. **Summary** highlighting:
   - Current macro regime (expansion/contraction)
   - Key trends and inflection points
   - Policy stance assessment
   - Implications for equity/bond markets

### Step 4: Sector Implications (Optional)

If the user has a specific sector focus, map macro indicators to sector drivers and provide implications.
