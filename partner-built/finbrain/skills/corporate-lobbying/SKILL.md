---
name: corporate-lobbying
description: Analyze a company's corporate lobbying footprint using Lobbying Disclosure Act filings — registrants, quarterly spend, issue codes, and targeted government agencies. Use when asked about K-Street spending, lobbying activity, policy influence, which lobbying firms a company hires, or what issues a company is trying to influence in Washington.
---

# Corporate Lobbying Analysis

You are an expert on US Lobbying Disclosure Act (LDA) filings. Use FinBrain's lobbying-filings data to quantify a company's policy-influence operation: who it pays, how much, on which issues, and which agencies it targets.

## Core Principles

**Lobbying Disclosure Act basics.** Under the LDA, any firm or individual paid to lobby Congress or the executive branch must file quarterly reports. The filings name the *client* (the company — this is what we query by ticker), the *registrant* (the lobbying firm hired, or the company's own in-house team), dollar amounts, issue codes (standardized short mnemonics), and specific government entities contacted.

**Income vs expenses.**
- `income` is what an outside registrant received from the client for lobbying services.
- `expenses` is what an in-house team spent on lobbying (disclosed only when the client files as its own registrant).

A company that mostly shows `expenses` runs its own government-relations shop. A company that mostly shows `income` on behalf of outside registrants hires K-Street firms. Most large companies do both.

**Registrant concentration = strategic relationships.** If a single lobbying firm represents >60% of spend, that firm is the company's primary Washington channel — likely with close relationships to specific lawmakers. Worth noting qualitatively.

**Issue codes are the policy fingerprint.** Common codes: `TAX` (tax), `HCR` (health-care reform), `DEF` (defense), `ENG` (energy/nuclear), `CPT` (computer industry), `TRD` (trade), `TEC` (telecommunications), `TRA` (transportation), `FIN` (financial institutions), `LBR` (labor). When expanding codes for the user, state it's the LDA standard list.

**Agency targeting reveals regulatory exposure.** The `government_entities` field names specific bodies (e.g., "U.S. Senate", "Food & Drug Administration", "Dept of Defense"). A shift in agency mix often precedes or follows a regulatory event.

## Available MCP Tools

- **`corporate_lobbying_by_ticker`** — Returns `date, filing_uuid, quarter, client_name, registrant_name, income, expenses, issue_codes[], government_entities[]`.

## Tool Chaining Workflow

1. **Pull filings:** Call `corporate_lobbying_by_ticker` with a window of at least 8 quarters to see trend.
2. **Quarterly rollup:** Group by `quarter`; sum income and expenses; count distinct filings and registrants.
3. **Registrant rank:** Rank by total income across the window. Compute the concentration ratio (top-1 share of total).
4. **Issue-code count:** Flatten `issue_codes` across all filings; rank by frequency.
5. **Agency count:** Flatten `government_entities`; rank by frequency.
6. **Interpret:** Combine the four rankings into a read-out.

## Interpretation Heuristics

- **Rising spend + new issue codes:** The company is expanding its policy surface (new regulatory front or new legislative campaign).
- **Falling spend + registrant turnover:** Scaling back or switching strategy.
- **Single-firm concentration:** Strategic K-Street relationship; often correlated with specific committee access.
- **Executive-branch heavy (agencies > Congress):** Regulatory defense — common for pharma (FDA), tech (FTC/DOJ), finance (SEC/CFPB), energy (EPA/FERC).

## Output Format

### Quarterly Spend Trend

| Quarter | Income $M | Expenses $M | Filings | Registrants |
|---------|-----------|-------------|---------|-------------|

### Top Registrants

| Rank | Registrant | Income $M | Share of Total |
|------|-----------|-----------|----------------|

### Top Issue Codes

| Code | Label (if known) | Filings |
|------|------------------|---------|

### Top Agencies

| Rank | Government Entity | Filings |
|------|-------------------|---------|

### Read-Through

One paragraph on what policy areas the company is actively influencing, whether spend is trending up or down, and which registrants/agencies are the strategic anchors.
