# Connectors

This plugin connects to multiple MCP data providers. The **Wind Financial Terminal** MCP server runs locally and wraps Wind's Python API (WindPy) for direct access to Chinese and global market data.

## Wind MCP Server (Local)

The Wind MCP server is a stdio-based local server that requires Wind Financial Terminal to be installed and logged in. It provides the following tools:

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| Historical Data | `wind_wsd` | Time-series data: prices, financials, technicals over date ranges |
| Snapshot Data | `wind_wss` | Cross-sectional data: latest multiples, fundamentals for multiple securities |
| Dataset Queries | `wind_wset` | Structured datasets: index constituents, IPO data, sector lists |
| Macro Economics | `wind_edb` | Economic database: GDP, CPI, PMI, monetary policy, trade, FX |
| Intraday Bars | `wind_wsi` | Minute-level OHLCV bars for intraday analysis |
| Tick Data | `wind_wst` | Tick-by-tick trade data for microstructure analysis |
| Portfolio | `wind_wpf` | Portfolio holdings, NAV, and return data |

## Complete Tool Reference

### Historical Time-Series — `wind_wsd`
Query historical data over a date range for one or more securities. Supports daily, weekly, monthly frequency. Covers prices (OHLCV), valuation multiples (PE, PB, PS, EV/EBITDA), financial statement items, per-share metrics, technical indicators, and more. Supports price adjustment (forward/backward).

**Key parameters:**
- `codes`: Security codes (e.g., "600519.SH,000858.SZ")
- `fields`: Data fields (e.g., "close,pe_ttm,pb_lf,volume")
- `begin_date` / `end_date`: Date range in "YYYY-MM-DD"
- `options`: "PriceAdj=F" (forward adjust), "Period=W" (weekly), "Period=M" (monthly)

### Cross-Sectional Snapshot — `wind_wss`
Retrieve the latest data point for one or many securities simultaneously. Ideal for building comparable company tables, screening, and benchmarking.

**Key parameters:**
- `codes`: One or more security codes
- `fields`: Data fields for the snapshot
- `options`: "rptDate=20231231" for specific report date, "unit=1" for yuan units

### Dataset Queries — `wind_wset`
Access structured reference datasets from Wind. Covers index/sector membership, IPO calendars, margin trading, stock connect flows, share buybacks, and more.

**Key parameters:**
- `report_name`: Dataset identifier (e.g., "sectorconstituent", "indexconstituent", "ipo")
- `options`: Filter parameters as semicolon-separated key=value pairs

### Economic Database — `wind_edb`
Access China and global macroeconomic indicators. Covers national accounts (GDP), prices (CPI, PPI), PMI surveys, monetary aggregates (M1, M2), interest rates (LPR, SHIBOR), exchange rates, trade data, and global economy indicators.

**Key parameters:**
- `codes`: EDB indicator codes (e.g., "M0001228" for GDP, "M0000612" for CPI)
- `begin_date` / `end_date`: Date range

### Intraday Minute Bars — `wind_wsi`
Retrieve intraday bar data at configurable intervals (1, 3, 5, 15, 30, 60 min). Useful for intraday pattern analysis and VWAP calculations.

### Intraday Tick Data — `wind_wst`
Retrieve individual trade records with price, volume, and order book snapshots. For microstructure analysis and execution quality assessment.

### Portfolio Data — `wind_wpf`
Query portfolio data from Wind Portfolio Manager. Retrieve holdings, weights, market values, and NAV history.

## Security Code Format

| Market | Format | Example |
|--------|--------|---------|
| Shanghai A-shares | XXXXXX.SH | 600519.SH (贵州茅台) |
| Shenzhen A-shares | XXXXXX.SZ | 000858.SZ (五粮液) |
| ChiNext (创业板) | 3XXXXX.SZ | 300750.SZ (宁德时代) |
| STAR Market (科创板) | 68XXXX.SH | 688981.SH |
| Hong Kong | XXXXX.HK | 00700.HK (腾讯) |
| US NASDAQ | XXXX.O | AAPL.O |
| US NYSE | XXXX.N | MSFT.N |
| CSI Indices | XXXXXX.SH | 000300.SH (沪深300) |
| Hang Seng Index | HSI.HI | HSI.HI |
| Government Bonds | XXXXXX.SH/IB | 019672.SH |
| Futures | XXXXXX.CFE/SHF/DCE/ZCE | IF2403.CFE |
| Options | XXXXXX.SH/SZ | 10007081.SH |

## Common EDB Indicator Codes

| Category | Code | Description |
|----------|------|-------------|
| GDP | M0001228 | GDP (current price, 100M CNY) |
| GDP Growth | M0001227 | GDP YoY (%) |
| CPI | M0000612 | CPI YoY (%) |
| Core CPI | M0000616 | Core CPI YoY (%) |
| PPI | M0001227 | PPI YoY (%) |
| PMI Mfg | M0017126 | Manufacturing PMI |
| PMI Non-Mfg | M0017127 | Non-manufacturing PMI |
| M2 | M0001385 | M2 YoY (%) |
| M1 | M0001387 | M1 YoY (%) |
| LPR 1Y | M0009808 | LPR 1-year (%) |
| LPR 5Y | M0009809 | LPR 5-year (%) |
| USD/CNY | M0290205 | Central parity rate |
| Exports | M0000607 | Exports YoY (USD) |
| Imports | M0000608 | Imports YoY (USD) |
| US CPI | G0000891 | US CPI YoY (%) |
| US GDP | G0000876 | US GDP QoQ SAAR (%) |
