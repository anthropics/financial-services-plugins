---
name: wind-macro-dashboard
description: |
  Build macroeconomic dashboards and analysis using Wind Economic Database (EDB).
  Covers China macro indicators, global economy data, monetary policy, and cross-country comparisons.

  **Perfect for:**
  - China macro economic overview and trend analysis
  - Monetary policy and interest rate environment assessment
  - Cross-country macro comparison (China vs US vs EU)
  - Industry and sector macro drivers analysis
  - Investment strategy macro backdrop reports
  - Economic indicator forecasting context

  **Not ideal for:**
  - Real-time market data (use wind_wsd/wind_wsi instead)
  - Company-level financial data (use wind-equity-analysis)
---

# Wind Macro Dashboard

## Overview

This skill uses Wind's Economic Database (`wind_edb`) to build macroeconomic dashboards and analysis reports. Wind EDB is one of the most comprehensive macro databases for China economic data, with extensive coverage of global indicators.

## Core EDB Indicator Codes

### China — Growth & Output
| Code | Indicator | Frequency |
|------|-----------|-----------|
| M0001228 | GDP (current price, 亿元) | Quarterly |
| M0001227 | GDP YoY (%) | Quarterly |
| M6193292 | GDP QoQ SAAR (%) | Quarterly |
| M0017126 | Manufacturing PMI (official) | Monthly |
| M0017127 | Non-manufacturing PMI (official) | Monthly |
| M0061603 | Caixin Manufacturing PMI | Monthly |
| M0000545 | Industrial Value Added YoY (%) | Monthly |
| M0000011 | Fixed Asset Investment YTD YoY (%) | Monthly |
| M0001428 | Retail Sales YoY (%) | Monthly |

### China — Prices
| Code | Indicator | Frequency |
|------|-----------|-----------|
| M0000612 | CPI YoY (%) | Monthly |
| M0000616 | Core CPI YoY (%) | Monthly |
| M0000613 | CPI MoM (%) | Monthly |
| M0061626 | PPI YoY (%) | Monthly |

### China — Monetary & Credit
| Code | Indicator | Frequency |
|------|-----------|-----------|
| M0001385 | M2 YoY (%) | Monthly |
| M0001387 | M1 YoY (%) | Monthly |
| M0001389 | M0 YoY (%) | Monthly |
| M0001411 | New CNY Loans (亿元) | Monthly |
| M5206730 | Total Social Financing (亿元) | Monthly |
| M0009808 | LPR 1Y (%) | Monthly |
| M0009809 | LPR 5Y (%) | Monthly |
| M0017139 | SHIBOR Overnight (%) | Daily |
| M0017141 | SHIBOR 3M (%) | Daily |

### China — Trade & FX
| Code | Indicator | Frequency |
|------|-----------|-----------|
| M0000607 | Exports YoY (%, USD) | Monthly |
| M0000608 | Imports YoY (%, USD) | Monthly |
| M0000609 | Trade Balance (亿美元) | Monthly |
| M0290205 | USD/CNY Central Parity | Daily |
| M0067855 | Foreign Exchange Reserves (亿美元) | Monthly |

### China — Real Estate
| Code | Indicator | Frequency |
|------|-----------|-----------|
| M0000531 | Real Estate Investment YTD YoY (%) | Monthly |
| M0000536 | Commercial Property Sales Area YTD YoY (%) | Monthly |
| M0000537 | Commercial Property Sales Value YTD YoY (%) | Monthly |
| M0000542 | New Construction Starts YTD YoY (%) | Monthly |

### US — Key Indicators
| Code | Indicator | Frequency |
|------|-----------|-----------|
| G0000876 | US GDP QoQ SAAR (%) | Quarterly |
| G0000891 | US CPI YoY (%) | Monthly |
| G0000900 | US Core CPI YoY (%) | Monthly |
| G0000911 | US PPI YoY (%) | Monthly |
| G0005394 | US Non-farm Payrolls Change (K) | Monthly |
| G0005396 | US Unemployment Rate (%) | Monthly |
| G0000886 | US ISM Manufacturing PMI | Monthly |
| G1120619 | Fed Funds Target Upper (%) | As-needed |

## Workflow Templates

### 1. China Macro Overview Dashboard

**Objective:** Comprehensive snapshot of China's economic health.

**Steps:**
1. Pull growth indicators with `wind_edb`:
   ```
   codes: "M0001227,M0017126,M0017127,M0000545,M0000011,M0001428"
   begin_date: [2 years ago]
   end_date: [today]
   ```

2. Pull price and monetary data:
   ```
   codes: "M0000612,M0000616,M0061626,M0001385,M0001387,M0009808"
   begin_date: [2 years ago]
   end_date: [today]
   ```

3. Pull trade data:
   ```
   codes: "M0000607,M0000608,M0000609,M0290205"
   begin_date: [2 years ago]
   end_date: [today]
   ```

4. Compile into dashboard with trend charts and latest readings

### 2. China vs US Macro Comparison

**Objective:** Side-by-side comparison of China and US economic cycles.

**Steps:**
1. Growth comparison: China GDP YoY vs US GDP QoQ SAAR
2. Inflation: China CPI vs US CPI
3. Policy rates: LPR vs Fed Funds Rate
4. PMI: China official PMI vs US ISM PMI
5. Employment: China surveyed unemployment vs US unemployment

### 3. Monetary Policy & Liquidity Monitor

**Objective:** Track PBoC monetary policy stance and liquidity conditions.

**Steps:**
1. Pull rate data: LPR, SHIBOR, MLF rate
2. Pull money supply: M0, M1, M2 YoY
3. Pull credit data: New loans, total social financing
4. Analyze: Rate trends, M1-M2 scissors gap, credit impulse

### 4. Sector Macro Drivers

**Objective:** Identify macro drivers for specific sectors.

**Steps:**
1. Map sector to relevant indicators:
   - Consumer: Retail sales, CPI, consumer confidence
   - Real estate: Property investment, sales area, new starts
   - Manufacturing: PMI, industrial VA, fixed asset investment
   - Banking: LPR, M2, new loans, NIM proxy
   - Export-oriented: Trade data, USD/CNY, global demand

2. Pull relevant indicators with `wind_edb`
3. Overlay with sector index performance from `wind_wsd`

## Output Standards

- Time series data presented as tables with date index
- Include latest reading, prior period, and YoY change
- Flag notable inflection points or trend breaks
- All data attributed: "Source: Wind EDB, as of [date]"
- For Excel output: include chart-ready data layout with dates in column A
