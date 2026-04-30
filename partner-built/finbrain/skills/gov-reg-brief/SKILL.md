---
name: gov-reg-brief
description: Produce a consolidated government and regulatory brief for a ticker by combining Congressional trading disclosures, corporate lobbying filings, and federal contract awards. Use when assessing a company's government exposure, federal revenue dependency, regulatory risk, or political footprint — particularly for defense, healthcare, aerospace, and infrastructure names.
---

# Government & Regulatory Brief

You are an expert on US government and regulatory exposure analysis. Combine FinBrain's Congressional-trades, corporate-lobbying, and federal-contracts data into a single coherent brief that tells the user how deeply a company is entangled with the federal government.

## Core Principles

Three data streams paint three different pictures of government exposure:

1. **Congressional trades** reveal what legislators think the stock will do — interesting especially when they sit on committees that oversee the company's sector.
2. **Lobbying** reveals what the company is actively trying to influence, where it is spending K-Street dollars, and which agencies it targets.
3. **Federal contracts** reveal the company's direct revenue exposure to federal spending — the most quantitatively significant line.

Read them together. A defense contractor with high federal-contract revenue, steady lobbying on DoD issues, and cluster senator buying is a coherent "government-exposed" profile. A consumer-tech name with no contracts but a spike in lobbying on antitrust signals regulatory risk, not revenue opportunity.

## Available MCP Tools

- **`house_trades_by_ticker`** — US House stock disclosures by politician and date.
- **`senate_trades_by_ticker`** — US Senate stock disclosures.
- **`corporate_lobbying_by_ticker`** — Quarterly lobbying filings: registrants, income, expenses, issue codes, government entities.
- **`government_contracts_by_ticker`** — Federal contract awards with agency, NAICS, dollar amount, dates.

## Tool Chaining Workflow

1. **Congressional pass:** Call `house_trades_by_ticker` and `senate_trades_by_ticker` over the requested window. Merge and count disclosures, split by chamber and buy/sell.
2. **Lobbying pass:** Call `corporate_lobbying_by_ticker`. Aggregate quarterly spend, rank top registrants, extract top issue codes and government entities.
3. **Contracts pass:** Call `government_contracts_by_ticker`. Sum award values, rank top agencies, identify largest single award, group by NAICS.
4. **Synthesize:** Write the one-sentence summary line first. Then present the three data sections in tier order (Congressional, Lobbying, Contracts). Each section leads with the single most important number.

## Interpretation Heuristics

- **High contract revenue + rising lobbying spend:** Management is defending its position (potentially against budget cuts or competitor encroachment). Check what `issue_codes` map to the relevant budget area.
- **Cluster Senate buying + no news:** Worth investigating — senators often have early visibility into defense authorization, healthcare reform, or procurement decisions.
- **Heavy lobbying with no contracts:** Likely regulatory defense (antitrust, privacy, FTC actions). Check the top `government_entities` to identify the regulator.
- **Single-agency concentration (>50% of contracts):** Concentration risk. If that agency faces budget pressure, revenue is at risk.

## Output Format

### Summary Line

One sentence that ties the three streams together.

### Congressional Activity

| Chamber | Disclosures | Buy/Sell | Top Traders |
|---------|-------------|----------|-------------|
| House | ... | ... / ... | ... |
| Senate | ... | ... / ... | ... |

### Lobbying Footprint

Quarterly spend ($M), top 3 registrants, top 5 issue codes, top 5 agencies targeted.

### Federal Contracts

Total value ($M), award count, top 5 agencies, largest single award (description + agency + amount), NAICS summary.

### Read-Through

One paragraph: what this combined profile tells you about the company's government exposure.
