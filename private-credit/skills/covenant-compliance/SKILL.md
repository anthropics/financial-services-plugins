# Covenant Compliance

This skill fires automatically when working with financial covenants, compliance certificates, headroom analysis, or covenant testing for private credit borrowers.

---

## Source of Truth

The compliance certificate is always the source of truth for covenant calculations. The compliance certificate is a PDF document signed by the CFO or another company officer. Because it is executed by a company officer, it has been reviewed and is authoritative.

When the borrower provides LTM Compliance EBITDA on the cert, use that number directly for covenant testing. Do not substitute your own independently calculated number.

However, always attempt to reconcile the cert number by spreading quarterly financials and building up to the LTM figure independently. This reconciliation is a verification exercise, not a replacement. If you cannot bridge to the cert number, that is a question to raise — not an error to correct.

---

## Reconciliation: Why the Numbers Often Don't Tie

The reconciliation between your independent quarterly build-up and the compliance cert's LTM number is rarely straightforward. The following are the primary sources of discrepancy:

### EBITDA Discrepancies

1. **M&A during the LTM period.** When a borrower acquires a company mid-period, the compliance cert pro forma's the acquired company's EBITDA for the pre-acquisition portion of the LTM window. You will not have the acquired company's standalone quarterly financials to spread, so the PF adjustment appears as a plug. This is expected — not an error.

2. **New adjustment initiatives.** The borrower may introduce new EBITDA addbacks that apply retroactively to the full LTM period but were not present in your prior quarterly spreads. A restructuring program started in Q3 may produce an addback applied to Q1-Q4 on the LTM cert.

3. **Unclear reported-to-adjusted bridge.** Some borrowers report only Revenue → Gross Profit → Adjusted EBITDA with no detail in between. When the quarterly P&L does not show the full waterfall, you must make assumptions about D&A, pro forma adjustments, and addback allocations across quarters. These assumptions will introduce variance.

4. **COGS-level adjustments.** Some addback categories include amounts embedded in cost of goods sold. The borrower reports gross profit as a single line (netting these out), then separately lists the full addback category on the compliance cert. A portion of the cert addback is already reflected in gross profit, causing an apparent double-count if you are not careful.

### Net Debt Discrepancies

1. **OID treatment.** The balance sheet reports debt net of original issue discount. The compliance certificate reports debt at face value. This difference is mechanical and explainable — not a flag.

2. **Lease and financing treatment.** The credit agreement defines which obligations count as debt for covenant purposes. Equipment leases, capital leases, sale-leasebacks, and other financing arrangements may be included or excluded depending on the agreement. The balance sheet may classify these differently than the credit agreement.

3. **Letters of credit.** Drawn and undrawn letters of credit may or may not be included in the covenant debt calculation depending on the credit agreement.

4. **Revolver balance.** The compliance cert tests as of quarter-end. The revolver balance at quarter-end may differ from average or month-end balances shown elsewhere in the reporting.

**Rule:** An analyst should almost always be able to bridge net debt between the audited financials, quarterly reporting, and the credit agreement. If you cannot bridge the debt number, something is wrong or missing — escalate. For EBITDA, the ability to bridge depends on the quality and detail of the borrower's reporting.

---

## Headroom Framework

Calculate covenant headroom as the percentage difference between the actual level and the covenant threshold.

| Headroom Level | Classification | Action |
|---|---|---|
| ≥ 20% | Comfortable | Standard monitoring. No escalation required. |
| 10% – 20% | Elevated attention | Monitor closely. Note in quarterly review. Track trajectory. |
| < 10% | Tight — flag to IC | High priority. Flag in quarterly review as approaching breach territory. Prioritize management call questions around drivers. |

### Trajectory Matters

Headroom assessment must always be read in context of the trend:

- **Improving** (e.g., 5% → 10% → 15%): Still flag if below 20%, but note the positive trajectory. IC needs to know the direction, not just the level.
- **Deteriorating** (e.g., 18% → 12% → 9%): Escalate early. Do not wait until sub-10% to flag. If the trend line points to sub-10% within one or two quarters, flag now.
- **Stable at tight levels** (e.g., 11% → 12% → 11%): The company is operating near the threshold consistently. Flag and assess whether this is structural or temporary.

---

## Maintenance vs. Incurrence Covenants

### Financial Maintenance Covenants

Tested quarterly (or as specified in the credit agreement) based on the most recent LTM period. The compliance certificate reports the results. The borrower must remain in compliance at each test date.

Standard maintenance covenants in mid-market private credit:
- **Net leverage** (Total Net Debt / LTM Adjusted EBITDA) — most common, usually the binding constraint
- **Fixed charge coverage ratio (FCCR)** (LTM EBITDA / (Cash Interest + Required Amortization)) — second most common
- **Minimum liquidity** (Cash + Revolver Availability ≥ threshold) — unusual; when present, it signals credit stress and is the highest priority covenant

### Incurrence Covenants

Not tested periodically. Triggered only when the borrower takes a specific action (incurring new debt, making a restricted payment, paying a dividend, making a junior debt payment). The borrower must demonstrate pro forma compliance with the incurrence level before taking the action.

**What the analyst must do at close and maintain ongoing:**
- Extract all incurrence test levels from the credit agreement
- Build a reference table: what action is restricted, at what leverage level does the restriction lift, and what baskets are available
- Key incurrence levels to track:
  - **Additional debt capacity:** At what leverage level can the borrower incur additional senior, junior, or pari passu debt?
  - **Restricted payments / dividends:** At what leverage level can the borrower make distributions, pay dividends, or make junior payments?
- Monitor actual leverage against incurrence levels on a quarterly basis — even though the test is not periodic, you need to know if the borrower is approaching a level where they could take action

---

## Step-Down Schedules

Covenant step-downs almost always align with quarter-end reporting dates. A step-down effective January 1 applies to the test period ending March 31, with results due approximately 45 days after quarter-end. Mid-quarter step-downs are extremely rare (well under 1% of deals).

### How to Apply Step-Downs

Always look up the applicable covenant threshold by test date. Walk the step-down schedule and return the threshold from the most recent effective date that is on or before the test date. Never hardcode a single threshold — always reference the schedule.

### Revolver Window Dressing

The most relevant operational consideration for step-downs and covenant testing is **revolver manipulation at quarter-end.**

Because covenants test as of quarter-end only, borrowers can:
- Draw up the revolver balance significantly during the quarter (increasing net debt) and repay it 1-2 days before quarter-end to reduce net leverage at the test date
- Withhold cash payments (vendor payments, discretionary spending) in the final weeks of the quarter so the cash balance is artificially high at quarter-end, reducing net leverage

**Watch for this pattern when:**
- Headroom is tight (sub-15%)
- Revolver utilization shows sharp quarter-end drops followed by immediate re-draws
- Cash balances spike at quarter-end and immediately decline in the following month (if monthly reporting is available)

---

## Covenant Severity Hierarchy

When a borrower is tight on multiple covenants, prioritize in this order:

1. **Minimum liquidity** — If present, this is the top priority. Minimum liquidity covenants are unusual in mid-market private credit. Their presence signals that lenders had specific concerns about cash flow or liquidity at origination. A liquidity covenant breach can trigger immediate acceleration — there is no cure through operational performance.

2. **Net leverage** — The binding constraint in the vast majority of mid-market direct lending deals. Whether it is cov-lite (springing leverage on the revolver only) or a full maintenance covenant, leverage is the metric that drives most credit decisions.

3. **Fixed charge coverage ratio (FCCR)** — Typically tested alongside leverage. Important, but leverage usually trips first because EBITDA declines hit the leverage numerator (debt is relatively fixed in the near term) before they flow through to fixed charge shortfalls.

4. **Maximum capex** — Second-tier covenant. Relevant for capital-intensive businesses. Rarely the binding constraint but can catch borrowers who are investing through a downturn.

**General principle:** Lower credit quality borrowers carry higher leverage and tighter covenant packages. The further down the credit spectrum, the more covenants you see and the tighter the thresholds. Many mid-market deals are cov-lite (leverage maintenance only, or springing). When covenants exist, net leverage is almost always the one that matters most.

---

## Equity Cure Rights

When documenting a covenant check, note the equity cure provision as a factual reference:
- How many cures are permitted under the credit agreement (typically 2-3 over the life of the facility, sometimes limited to 1-2 per 4-quarter period)
- How many have been used to date
- How many remain available

Present this as a footnote or side note. Do not build cure mechanics into the covenant check output unless headroom is tight enough that a cure is a realistic near-term possibility.
