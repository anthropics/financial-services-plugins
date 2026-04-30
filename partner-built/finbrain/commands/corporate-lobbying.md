---
description: Quarterly corporate lobbying filings for a ticker — registrants, income, expenses, issue codes, and targeted government entities
argument-hint: "<ticker> [quarters]"
---

# Corporate Lobbying Analysis

> This command uses FinBrain's corporate lobbying tool. See [CONNECTORS.md](../CONNECTORS.md) for the full tool reference.

Analyze a company's lobbying footprint using filings under the Lobbying Disclosure Act: who it hires, how much it spends, on which issues, and which agencies it targets.

See the **corporate-lobbying** skill for interpretation of registrant concentration and issue-code taxonomy.

## Workflow

### 1. Gather Inputs

Ask the user for:
- Ticker (required)
- Optional number of quarters to look back (default 8)

### 2. Pull Lobbying Filings

Call `corporate_lobbying_by_ticker` with the ticker and `date_from` set to today minus (quarters × ~92 days). Use `limit` of 500 to avoid truncation for heavy lobbyists.

### 3. Aggregate by Quarter

For each quarter present in the data:
- Total income (dollars paid to outside lobbying firms)
- Total expenses (company's internal lobbying spend, if disclosed)
- Number of distinct filings
- Unique registrants
- Unique issue codes

### 4. Registrant Concentration

Rank the top 5 registrants (lobbying firms) by total income across the window. Flag if a single firm represents >60% of spend (concentration risk or strategic relationship).

### 5. Issue-Code Themes

Count issue-code frequency across all filings. Present the top 10 with a plain-English label (the codes themselves are short mnemonics like `TAX`, `HCR`, `DEF`; expand them inline if known).

### 6. Agency Targeting

Aggregate `government_entities` across filings; rank the top 10 agencies/bodies by filing count. This reveals where the company focuses its advocacy (e.g., FDA for pharma, DoD for defense, Treasury + House Ways & Means for tax).

### 7. Synthesize

Present quarterly spend trend, registrant table, issue-code table, and agency table. Close with a one-paragraph read-out: which policy areas the company is actively influencing, whether spend is rising or falling, and any recent pivots.

## Output Format

Four tables (Quarterly spend, Top registrants, Top issue codes, Top agencies) plus a 2–3 sentence interpretation. Dollar amounts in USD millions with one decimal.
