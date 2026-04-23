---
description: "Full covenant compliance snapshot with headroom analysis"
argument-hint: "<attached compliance cert or financials>"
---

# /private-credit:covenant-check

Produces a comprehensive covenant compliance snapshot: financial maintenance covenants with headroom, incurrence test levels, restricted covenant baskets, step-down schedule, and cure rights summary.

---

## Trigger

User invokes `/private-credit:covenant-check` with a borrower's compliance certificate and/or credit model. Optionally, the credit agreement or summary of key terms for incurrence and basket details.

---

## Required Inputs

| Input | Required? | Notes |
|---|---|---|
| Compliance certificate (current quarter) | **Yes** | Source of truth for actual covenant levels |
| Credit agreement or term sheet summary | **Yes** | For covenant definitions, step-down schedules, incurrence levels, baskets |
| Credit model (for historical quarters) | Recommended | Enables trend analysis across multiple quarters |

---

## Calculation Approach

### Financial Maintenance Covenants

**Use the compliance certificate number directly.** The compliance cert is signed by the CFO or company officer and is the authoritative source for covenant calculations.

Do NOT independently recalculate and substitute a different number. The cert number is the covenant test result.

**Verification exercise:** Separately attempt to calculate the covenant metrics from the financial statements to verify you can reach the same number. If you cannot reconcile:
- For net debt: investigate OID treatment, lease classification, letter of credit inclusion — this should almost always be bridgeable
- For EBITDA: investigate addback detail, PF adjustments, retroactive adjustments — bridgeability depends on reporting quality
- If the gap cannot be explained, flag it as a question. Do not override the cert.

---

## Output Structure

### Section 1: Financial Maintenance Covenant Table

| | Q1 2025 | Q2 2025 | Q3 2025 | Q4 2025 | Q1 2026 | Q2 2026 |
|---|---|---|---|---|---|---|
| **Net Leverage** | | | | | | |
| Covenant Threshold | 5.00x | 5.00x | 5.00x | 4.75x | 4.75x | 4.50x |
| Actual | 4.52x | 4.38x | 4.15x | 4.02x | — | — |
| Cushion | 9.6% | 12.4% | 17.0% | 15.4% | — | — |
| Status | ⚠️ Tight | ✅ | ✅ | ✅ | *step-down* | *step-down* |
| **FCCR** | | | | | | |
| Covenant Threshold | 1.10x | 1.10x | 1.10x | 1.10x | 1.15x | 1.15x |
| Actual | 1.18x | 1.22x | 1.28x | 1.31x | — | — |
| Cushion | 7.3% | 10.9% | 16.4% | 19.1% | — | — |
| Status | ⚠️ Tight | ✅ | ✅ | ✅ | *step-down* | — |

**Key formatting rules:**
- Columns: quarterly progression left to right (oldest to newest, then 2-4 future quarters)
- Future quarters: show covenant threshold only (actuals blank). Reader sees upcoming step-downs visually.
- Cushion: positive = in compliance. Flag per headroom framework:
  - ≥ 20%: no flag
  - 10-20%: "⚡ Elevated attention"
  - < 10%: "⚠️ Tight — flag to IC"
- Note trajectory in a summary line: "Leverage headroom: improving (9.6% → 17.0% over 3 quarters)" or "FCCR headroom: stable at 10-12%"

### Section 2: Incurrence Test Levels

| Incurrence Test | Trigger | Leverage Level |
|---|---|---|
| Additional Senior Debt | Incurrence of new pari passu debt | ≤ 4.00x Total Net Leverage |
| Additional Junior Debt | Incurrence of subordinated debt | ≤ 5.50x Total Net Leverage |
| Restricted Payments / Dividends | Distributions to equity holders | ≤ 3.50x Total Net Leverage |
| Junior Debt Payments | Payments on subordinated obligations | ≤ 4.00x Total Net Leverage |

**Include current actual leverage for context:** "Current Total Net Leverage: 4.02x — restricted payment incurrence test (3.50x) is not currently available."

### Section 3: Key Restricted Baskets

Summarize the most important baskets from the credit agreement:

| Basket | Limit | Current Utilization | Available |
|---|---|---|---|
| CapEx | $5.0M annually | $3.2M YTD | $1.8M remaining |
| Restricted Payments (general) | $2.0M per year + leverage-based | $0 used | $2.0M available |
| Permitted Investments | $3.0M in aggregate | $1.5M used | $1.5M available |
| Debt Incurrence (incremental) | $10.0M | $0 drawn | $10.0M available |

Populate with actual figures if available from the compliance cert or credit agreement tracking. If utilization data is not available, show the limit and note "utilization not reported."

### Section 4: Equity Cure Rights

| Item | Detail |
|---|---|
| Total cures permitted | [X] over the life of the facility |
| Consecutive quarter limit | No more than [X] in any [Y] consecutive quarters |
| Cures exercised to date | [X] |
| Cures remaining | [X] |

Present as a factual reference footnote. No analysis unless headroom is tight enough that cure exercise is a realistic near-term possibility.

---

## Summary Statement

Close with a 2-3 sentence summary:
- Overall compliance status
- Headroom trajectory (improving, stable, deteriorating)
- Any upcoming step-downs that will tighten headroom
- Any incurrence tests currently unavailable due to leverage levels

Example: "Company X is in compliance with all financial maintenance covenants as of Q4 2025. Leverage headroom improved from 9.6% in Q1 to 15.4% in Q4, driven by EBITDA growth and modest deleveraging. Note: the 4.50x step-down in Q2 2026 will compress headroom to an estimated 10-11% at current run-rate — monitor closely."

---

## Value of This Command

This command eliminates the need to manually open the credit agreement, look up step-down schedules, cross-check compliance cert numbers, calculate headroom, and compile incurrence levels. One command produces the full covenant picture: current levels, cushion, trend, upcoming changes, incurrence availability, and cure rights — everything needed to assess the covenant position at a glance.
