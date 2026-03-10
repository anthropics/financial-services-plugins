---
name: wind-equity-analysis
description: |
  Equity analysis using Wind Financial Terminal data. Build company profiles, valuation analyses, peer comparisons,
  and financial deep-dives for A-shares, Hong Kong, and US-listed Chinese companies.

  **Perfect for:**
  - A-share company valuation and peer comparison
  - Hong Kong / US-listed Chinese company analysis
  - Cross-market (A+H) premium/discount analysis
  - Industry chain and sector analysis
  - Financial statement deep-dives for Chinese companies
  - IPO and secondary offering analysis

  **Not ideal for:**
  - Companies with no Wind coverage
  - Pure US/European companies (use other MCP providers)
---

# Wind Equity Analysis

## Overview

This skill uses Wind MCP tools to perform equity analysis on Chinese and Asian market securities. Wind provides the most comprehensive coverage of A-shares, Hong Kong stocks, and US-listed Chinese ADRs.

## Data Source Priority

1. **Wind MCP** — Primary source for all China/HK/Asian market data
2. **Other MCP providers** — Supplement with S&P Kensho, FactSet for global comparisons
3. **Never use web search** when Wind MCP is available

## Core Workflows

### 1. Single Company Profile

**Objective:** Build a comprehensive company snapshot with financials, valuation, and trading data.

**Steps:**
1. Use `wind_wss` to get latest snapshot data:
   - Company info: `sec_name,industry_sw,industry_sw_lv2,province,listdate,mkt_cap_ard`
   - Valuation: `pe_ttm,pb_lf,ps_ttm,pcf_ocf_ttm,ev_ebitda`
   - Financials: `tot_oper_rev,oper_profit,net_profit_is,grossprofitmargin,roe_avg`
   - Growth: `yoy_or,yoy_np,qfa_yoy_or,qfa_yoy_np`
   - Per-share: `eps_basic,bps,cfps,dividendyield2`

2. Use `wind_wsd` for historical trends (3-5 years):
   - Revenue and profit trends: `tot_oper_rev,net_profit_is`
   - Valuation history: `pe_ttm,pb_lf`
   - Price performance: `close,pct_chg` with `PriceAdj=F`

3. Use `wind_wset("sectorconstituent")` to identify sector peers

### 2. Peer Comparison (Comps Table)

**Objective:** Build a comparable company table for A-share/HK peers.

**Steps:**
1. Identify peer group:
   - Use `wind_wset("sectorconstituent")` to get sector constituents
   - Or use `wind_wss` with user-specified codes

2. Pull snapshot data with `wind_wss` for all peers at once:
   ```
   codes: "600519.SH,000858.SZ,000568.SZ,603369.SH,002304.SZ"
   fields: "sec_name,mkt_cap_ard,pe_ttm,pb_lf,ps_ttm,ev_ebitda,tot_oper_rev,yoy_or,grossprofitmargin,roe_avg"
   ```

3. Build comparison table with median/quartile statistics

4. Output as Excel following comps-analysis skill format

### 3. Financial Statement Deep-Dive

**Objective:** Analyze 3-5 years of financial statements for trend analysis.

**Steps:**
1. Use `wind_wsd` for annual data:
   - Income statement: `tot_oper_rev,oper_cost,selling_dist_exp,gerl_admin_exp,rd_exp,oper_profit,net_profit_is`
   - Balance sheet: `tot_assets,tot_liab,tot_shrhldr_eqy_excl_min_int,monetary_cap,inventories,acct_rcv`
   - Cash flow: `net_cash_flows_oper_act,net_cash_flows_inv_act,net_cash_flows_fnc_act,free_cash_flow`
   - Set `options: "Period=Y;rptType=1"` for annual reports

2. Calculate key ratios:
   - Profitability: gross margin, operating margin, net margin, ROE, ROA
   - Efficiency: asset turnover, inventory days, receivable days
   - Leverage: debt/equity, interest coverage
   - Growth: revenue CAGR, profit CAGR

### 4. Index Constituent Analysis

**Objective:** Analyze an index (CSI 300, CSI 500, etc.) for sector allocation and top holdings.

**Steps:**
1. Use `wind_wset("indexconstituent")` with index sector ID
2. Use `wind_wss` for valuation data of all constituents
3. Aggregate by sector (申万行业分类) for sector allocation breakdown
4. Identify top holdings by weight and valuation outliers

## Wind Code Quick Reference

| Type | Format | Example |
|------|--------|---------|
| Shanghai A | XXXXXX.SH | 600519.SH (贵州茅台) |
| Shenzhen A | XXXXXX.SZ | 000858.SZ (五粮液) |
| ChiNext | 3XXXXX.SZ | 300750.SZ (宁德时代) |
| STAR Market | 68XXXX.SH | 688981.SH (中芯国际) |
| Hong Kong | XXXXX.HK | 00700.HK (腾讯) |
| US ADR | XXXX.O / XXXX.N | BABA.N (阿里巴巴) |

## Common Wind Fields Reference

### Valuation
| Field | Description |
|-------|-------------|
| pe_ttm | P/E (TTM) |
| pb_lf | P/B (LF) |
| ps_ttm | P/S (TTM) |
| pcf_ocf_ttm | P/CF (TTM) |
| ev_ebitda | EV/EBITDA |
| mkt_cap_ard | Market Cap (元) |
| ev2 | Enterprise Value (元) |

### Financials
| Field | Description |
|-------|-------------|
| tot_oper_rev | Total Revenue |
| oper_profit | Operating Profit |
| net_profit_is | Net Profit |
| grossprofitmargin | Gross Margin (%) |
| roe_avg | ROE (average) |
| eps_basic | Basic EPS |

### Growth
| Field | Description |
|-------|-------------|
| yoy_or | Revenue YoY (%) |
| yoy_np | Net Profit YoY (%) |
| qfa_yoy_or | Single Quarter Revenue YoY (%) |
| qfa_yoy_np | Single Quarter Net Profit YoY (%) |

## Output Standards

- All monetary values in appropriate units (亿元 for large-cap, 万元 for small-cap) with clear labels
- Percentage values to 1 decimal place
- Multiples to 1 decimal place
- Include data source attribution: "Source: Wind Financial Terminal, as of [date]"
- For Excel output, follow the formatting conventions in comps-analysis skill
