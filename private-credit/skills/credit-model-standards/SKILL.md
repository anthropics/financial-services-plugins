# Credit Model Standards

This skill fires automatically when building, reviewing, or modifying financial models for private credit transactions — including new deal underwriting models, quarterly monitoring models, and scenario analysis.

---

## Model Structure — Tab Order

The tab structure for a private credit model follows the same foundational architecture as a leveraged buyout model. Start with the LBO model structure as the base and modify for credit-specific needs. Every firm has its own template, but the fundamental structure is consistent.

### Standard Tab Order (Left to Right)

1. **Assumptions / Inputs** — All hardcoded assumptions in one place: revenue growth rates, margin assumptions, working capital assumptions, capex, tax rate, debt terms, pricing. Color-coded as inputs.

2. **Income Statement** — Revenue by segment → COGS → Gross Profit → Operating Expenses by category → EBIT → D&A → EBITDA → Interest → Taxes → Net Income. Historical actuals and projected periods.

3. **Balance Sheet** — Standard format. Working capital detail (AR, inventory, AP, accruals). Debt by tranche. Equity. Ensure debt is shown at face value in the model even if balance sheet reports net of OID.

4. **Cash Flow Statement** — Operating cash flow → Investing → Financing → Net change in cash. Working capital changes flow from the balance sheet. Capex from assumptions.

5. **Debt Schedule** — Beginning balance → draws → repayments → amortization → PIK additions → ending balance. One section per tranche (Revolver, Term Loan A, Term Loan B, any subordinated debt). Interest calculation per tranche (spread + base rate, floors, PIK if applicable). Mandatory amortization schedule. Revolver draw/repay mechanics.

6. **Free Cash Flow Waterfall** — See detailed build below. This is a critical tab for private credit — it shows the business's actual ability to service debt and maintain liquidity.

7. **Credit Statistics** — All key credit ratios calculated from the model outputs. See standard set below.

8. **Covenant Compliance** — Covenant levels by test date, actual levels from the model, headroom calculation, pass/fail, step-down schedule.

9. **Summary Output** — One-page view: high-level P&L flowing into FCF, key credit statistics, leverage trajectory, covenant summary. This is the tab the MD reads.

10. **Cases / Scenarios** — Base, Downside, Stress. Each case has its own assumption set that feeds the model. Output comparison across cases on a summary page.

### Credit-Specific Additions (vs. Standard LBO Model)

- **Do not focus on equity returns.** IRR, MOIC, and equity waterfall tabs are PE-specific. A private credit model focuses on debt service capacity, not equity upside.
- **FCF waterfall must be explicit.** Do not bury free cash flow inside the cash flow statement. Build a dedicated section or tab that clearly shows EBITDA → FCF conversion.
- **Summary output tab is mandatory.** IC members and portfolio managers need a single page that tells the story. They will not flip through five tabs of detail.
- **Cases must be well-developed.** Downside and stress cases require specific, business-relevant assumptions — not just a percentage haircut on the base case.

---

## Free Cash Flow Waterfall — Exact Build

**Start with Reported EBITDA.** This is critical. Do not start with Adjusted EBITDA.

Adjusted EBITDA includes addbacks that are not cash flow items. If you start with Adjusted EBITDA, you must separately subtract the addback amounts to avoid overstating cash flow. Starting with Reported EBITDA avoids this issue entirely.

```
Reported EBITDA
  less: Capital Expenditures
        (split Maintenance vs. Growth if available)
        (split Capitalized Software separately for software companies)
  plus/less: Change in Net Working Capital
        (Change in AR + Change in Inventory - Change in AP - Change in Accrued Liabilities)
  less: Cash Taxes
  less: Cash Interest Expense
  less: Mandatory Amortization Payments
  less: Management Fee (if not already deducted above Reported EBITDA)
  less: One-Time Cash Items (if known — highlight as separate line items in red)
= Free Cash Flow
```

### Common Mistakes

**Synergies and pro forma adjustments.** This is the single most important item to get right in the FCF waterfall. Leverage is set off of pro forma Adjusted EBITDA, which includes projected synergies. But projected synergies are not generating cash until they are realized and appear in the P&L.

When building a model with synergies:
- The covenant compliance section uses Adjusted EBITDA (including synergies) for leverage calculation — this is per the credit agreement
- The FCF waterfall must reflect when synergies actually transition from "projected" to "realized in the P&L"
- Track: In which quarter do specific synergies begin contributing to Reported EBITDA?
- Before that quarter, they are addbacks for covenant purposes but do not generate cash — the FCF waterfall should not include them
- After that quarter, they are part of Reported EBITDA and flow naturally into FCF

**Adjustments double-counting.** If you start from Adjusted EBITDA instead of Reported EBITDA, you must subtract each addback category in the FCF waterfall to get back to actual cash flow. This creates complexity and risk of omission. Starting from Reported EBITDA is cleaner.

**Operating cash flow as sanity check.** Operating Cash Flow from the CFS less CapEx should be a reasonable proxy for FCF. Compare your FCF waterfall output to this simple calculation. If they diverge significantly, investigate.

---

## Case Build Methodology

### Starting Point: Sponsor/Vendor Case

The private equity sponsor provides a base case (sometimes called "management case" or "vendor case"). This is the case used for covenant setting and pricing negotiations.

**Important context:** The sponsor's base case is typically sandbagged — it is a conservative version of their internal realistic case. They present this to lenders because the more conservative the base case, the more covenant cushion they build against their actual expectations. This means the covenant levels are set relative to a case that the sponsor expects to outperform.

### Lender Base Case

Some firms use the sponsor case as-is for their base case. Others build a "lender case" that adjusts the sponsor case around the edges:
- A few percentage points less aggressive on revenue growth
- Slightly less free cash flow generation
- Marginally higher operating expenses

The lender case is not a fundamentally different view — it is the sponsor case with a more conservative tilt to reflect the lender's perspective.

### Downside Case — Business-Specific

**Downside case assumptions must be derived from the specific risk profile of the business.** You cannot reuse a prior deal's downside template. Each downside case must be built from the unique dynamics of the business being analyzed.

| Business Characteristic | Downside Assumption |
|---|---|
| Cyclical business (manufacturing, construction, industrials) | Model a full down-cycle with revenue decline consistent with historical recession performance for this sector |
| High customer concentration (top customer >15-20% of revenue) | Model loss of the top customer: revenue impact, margin impact, working capital impact |
| Supplier-dependent margins (single-source supplier, favorable contract) | Model loss of the favorable supply arrangement: margins compress to industry standard levels |
| Acquisition-dependent growth (roll-up strategy) | Model a pause in acquisitions: organic growth only, no PF EBITDA additions, integration costs continue |
| Discretionary/consumer-facing revenue | Model a demand pullback: revenue decline anchored to 2008-2009 recession performance for comparable businesses |

**Generic downturn scenario:** When business-specific risks do not point to a clear downside driver, model a general economic recession. Anchor to how the business or comparable businesses performed during the 2008-2009 financial crisis. Model a similar decline in revenue and margin, followed by recovery.

### Stress Case

More severe than the downside. The stress case tests whether the structure survives an extreme scenario:
- Combine multiple adverse factors (revenue decline + margin compression + working capital deterioration)
- Test: In what quarter do covenants breach? What is leverage at trough? Does the business generate positive FCF at trough? What is the liquidity runway?

### Recovery Assumptions

Recovery is not always V-shaped:
- **Cyclical downturn:** Typically V-shape or U-shape recovery — revenue declines and then recovers as the cycle turns. Model the recovery period (usually 2-4 quarters from trough to pre-downturn levels).
- **Structural impairment:** If the downside scenario reflects a permanent market shift (e.g., technology disruption, regulatory change), the business may not recover to prior levels. Model a "new normal" at a lower revenue/margin base.
- **Customer loss:** Recovery depends on the business's ability to replace the lost customer. May be partial recovery or full replacement over 4-8 quarters.

Show both the trough and the recovery trajectory in the output. IC needs to evaluate: (1) can the business survive the trough, and (2) what does the recovery path look like?

---

## Debt Schedule

Straightforward roll-forward for each tranche:

```
Beginning Balance
  + Incremental Debt (new draws, add-on terms loans)
  - Mandatory Amortization
  - Voluntary Prepayments (from excess cash flow sweep or optional paydown)
  + PIK Interest (if applicable — interest added to principal balance)
= Ending Balance
```

Each tranche modeled separately: Revolver, Term Loan A, Term Loan B, mezzanine, subordinated notes, etc.

Interest calculation per tranche:
- Base rate (SOFR) + spread
- SOFR floor (if applicable)
- PIK component (if applicable — separate cash pay vs. PIK)
- Commitment fees on undrawn revolver

---

## Credit Statistics — Standard Set

Every private credit model must include:

| Metric | Calculation | Purpose |
|---|---|---|
| **Senior Net Leverage** | Senior Net Debt / LTM EBITDA | Primary leverage metric for senior lenders |
| **Total Net Leverage** | Total Net Debt / LTM EBITDA | Total leverage including subordinated debt |
| **Gross Leverage** | Total Debt (no cash offset) / LTM EBITDA | Leverage without cash benefit — shows structural exposure |
| **Fixed Charge Coverage Ratio (FCCR)** | LTM EBITDA / (Cash Interest + Mandatory Amortization) | Ability to cover required debt service payments |
| **Interest Coverage** | LTM EBITDA / Cash Interest Expense | Variation of FCCR — some agreements test interest only |
| **EBITDA less CapEx Coverage** | (LTM EBITDA - CapEx) / (Cash Interest + Mandatory Amortization) | Tighter coverage metric — accounts for required reinvestment |
| **Loan-to-Value (LTV)** | Total Debt / Enterprise Value | Risk profile relative to business value. Critical to track over time. |

### LTV — Why It Matters

LTV can deteriorate even when leverage is stable. If you originate at 6x leverage on a 10x EV business (60% LTV) and the industry re-rates to 8x EV multiples while leverage stays at 6x, LTV jumps to 75%. The risk profile has changed materially even though the P&L and leverage have not.

Track LTV quarterly using updated comparable company multiples. Include in the credit statistics section and flag when LTV trends higher.

### Deal-Specific Additions

Depending on the business, you may need:
- **Tangible Net Worth** — for asset-heavy or regulated businesses
- **Borrowing Base metrics** — for ABL structures
- **Recurring Revenue coverage** — for software/SaaS businesses
- **Same-store growth** — for multi-location or franchise businesses

---

## Model Hygiene

Follow standard investment banking and private equity modeling best practices. There are no private credit-specific deviations from standard model hygiene rules:

- **Input cells** (hardcoded assumptions): Blue font or yellow fill — consistently applied throughout
- **Formula cells:** Black font, never hardcoded values mixed with formulas
- **Linked cells** (references to other sheets): Green font or consistent indicator
- **Error checks:** Build error check rows at the bottom of each sheet (BS balances, CFS reconciles to BS cash, etc.)
- **No circular references.** If the model requires circularity (e.g., interest expense depends on cash balance which depends on interest expense), use an iterative calculation toggle or break the circularity with a prior-period approximation.
- **Assumptions organized in one place.** All key assumptions on the Assumptions/Inputs tab. Do not bury hardcoded numbers in formula cells throughout the model.
- **Sign convention consistent.** Pick a convention (positive = inflow, negative = outflow) and apply it everywhere. Document it on the first tab.
- **Period labels clear.** Every column header shows the period (Q1 2025, FY 2025, LTM Q3 2025, etc.)
- **Units labeled.** Every table header shows units ($000s, $M, %, x)
