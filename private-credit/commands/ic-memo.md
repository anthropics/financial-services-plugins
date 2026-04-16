---
description: "Generate a full IC memo from deal inputs (CIM + model + term sheet)"
argument-hint: "<attached deal materials>"
---

# /private-credit:ic-memo

Produces a full investment committee memo in private credit format from deal inputs. The memo is written in advocacy tone — the team is recommending approval to proceed.

---

## Trigger

User invokes `/private-credit:ic-memo` with deal materials attached or referenced.

---

## Minimum Required Inputs

| Input | Required? | Notes |
|---|---|---|
| CIM or lender presentation | **Yes** | Foundation for business description and deal context |
| Financial model with base case and downside case | **Yes** | Must be the analyst's own model, not just the sponsor's case |
| Term sheet or summary of key credit terms | **Yes** | Can be 1-2 pages — detailed credit agreement is often post-IC |

**Without a model and your own case analysis, do not produce an IC memo.** A memo built from the CIM alone is a reorganization of sell-side materials without independent analytical input. Inform the user that a model is required and offer to help build one using `/private-credit:scenario-analysis` first.

## Inputs That Improve Quality

| Input | Impact |
|---|---|
| Management call notes | Adds narrative depth, addresses risk mitigants, provides forward-looking context |
| Expert call findings | Industry validation, competitive positioning verification |
| Data cuts (customer, product, vendor, historical) | Deal-specific analysis beyond CIM |
| Comps analysis (public and private) | Valuation context, market positioning |
| Precedent deals (same industry or sponsor) | Structural benchmarking |
| Q&A responses from borrower or sponsor | Answers to diligence questions |

If these additional inputs are available, incorporate them throughout the memo — not in a separate section.

---

## Output Structure

The IC memo follows the section order defined in the credit-memo-standards skill. Produce each section with the following specific guidance:

### Section 1: Executive Summary / Deal Setup (1-2 slides equivalent)

Write this section **last** — after all other sections are complete. It is a distillation of the entire memo.

Must answer in the first few sentences:
- What is the business? (one sentence: sector, product/service, revenue scale)
- What is the opportunity? (new deal, refinancing, add-on — amount and structure)
- What are the headline terms? (leverage, spread, maturity)
- Why is this attractive? (2-3 strongest merits from Section 4)
- What are the key risks? (2-3 most important risks from Section 5)

**Do not** open with company history. Do not spend the first paragraph on industry background. Lead with the deal.

### Section 2: Sources & Uses + Capital Structure (1 slide equivalent)

Two tables:

**Sources & Uses:**
Pull directly from the CIM, lender presentation, or term sheet. If not explicitly provided, construct from available information:
- Sources: each debt tranche (committed amount), equity contribution, rollover equity, seller note, other
- Uses: enterprise value / purchase price, debt refinancing, transaction fees, OID, working capital, cash to balance sheet

**Capital Structure:**
Each tranche with: facility type, committed amount, drawn amount, spread, OID, maturity, amortization schedule. Calculate and show:
- Senior leverage, total leverage (gross and net)
- LTV at entry (if enterprise value is available)

### Section 3: Term Sheet Summary (1-2 slides equivalent)

Summarize from the term sheet or CIM term sheet section:
- Financial maintenance covenants with levels and step-down schedule
- Key incurrence tests (leverage levels for restricted payments, additional debt)
- Important baskets (CapEx, restricted payments, investments, debt incurrence)
- Reporting requirements
- Equity cure rights
- Call protection and prepayment terms
- Change of control

### Section 4: Investment Merits (multiple slides equivalent)

4-6 merits. The first 1-3 are the strongest arguments for the deal.

For each merit:
- Clear heading stating the merit
- 2-4 sentences of narrative explanation with specific evidence from the CIM, data cuts, or model
- Supporting data point, chart description, or table reference where applicable

Draw from these categories as applicable:
- **Business strengths:** Market position, industry growth, switching costs, customer stickiness, recurring revenue, retention rates
- **Financial strengths:** Revenue CAGR, margin profile, FCF generation, low leverage relative to cash flow, asset coverage
- **Other:** Management quality, sponsor reputation, familiarity with industry or sponsor, attractive structure, clear deleveraging path

**Always include a merit on FCF and deleveraging.** IC must see the path from entry leverage to a lower level over the projection period. State the base case deleveraging trajectory explicitly: "Base case projects deleveraging from X.Xx at close to Y.Yx by Year 3 through $ZM of cumulative FCF generation."

### Section 5: Key Risks & Mitigants (multiple slides equivalent)

3-5 risks specific to this deal. **Every risk must have a mitigant paired with it.**

For each risk:
- Clear heading stating the risk
- 2-4 sentences explaining why this is a risk for this specific business and this specific structure (not generic platitudes)
- Mitigant: how the risk is addressed — structurally (covenant, basket, collateral), contractually (credit agreement provision), or by the business's characteristics

**Do not include generic risks.** "An economic downturn could impact revenue" without deal-specific context is not useful. "Revenue concentration: top 3 customers represent 45% of revenue, and loss of the largest (22%) would reduce EBITDA by an estimated $4M, compressing covenant headroom from 18% to 6%" — that is a useful risk statement.

**This section determines whether the deal survives IC.** If IC identifies a risk the team did not address, it signals insufficient diligence. Identify every risk IC is likely to raise and address it proactively.

### Section 6: Historical Financials (1 slide equivalent)

Table: 3 years of historical financials, quarterly if available.
- Revenue by segment (if provided)
- Gross profit and gross margin
- EBITDA and EBITDA margin
- Key balance sheet items (cash, debt, net debt)
- Key credit ratios (leverage, coverage)

Narrative alongside the table: what drove performance changes, one-time events, trend context.

### Section 7: EBITDA Adjustments Detail (1 slide equivalent)

Bridge: Reported EBITDA → each adjustment category → Adjusted EBITDA.
- Show dollar amounts per category
- Show total adjustments as a percentage of Reported EBITDA
- Flag any category that appears recurring (3+ consecutive quarters at similar levels)
- Flag any category exceeding 5% of EBITDA
- Note cash vs. non-cash nature of each adjustment

### Section 8: Model Output — Base Case and Downside Case (2-4 slides equivalent)

**Base Case (1-2 slides):**
Key model outputs in table form:
- Revenue, EBITDA, EBITDA margin (3-year projection)
- FCF and cumulative FCF
- Leverage trajectory (entry → Year 1 → Year 2 → Year 3)
- Covenant compliance with headroom at each test date
- Liquidity position (cash + revolver availability)

Narrative alongside: key assumptions, what drives the case, why the assumptions are reasonable.

**Downside Case (1-2 slides):**
Same metrics as base case. Plus:
- Specific assumptions and why they are appropriate for this business
- The quarter where covenants breach (if they do) and the leverage at that point
- FCF at trough — positive or negative? Magnitude?
- Liquidity runway at trough
- Recovery trajectory: what does the path back look like? How many quarters to return to base case levels?

Present the downside factually and descriptively. State the assumptions, state the outcomes, describe how the company is positioned to manage through the trough. IC evaluates whether the structure survives the downside — give them the facts to make that judgment.

### Section 9: Appendix

Include as applicable:
- Detailed company and business description
- Industry analysis and market sizing
- Deal-specific analysis: retention metrics, KPI deep-dives, fixed vs. variable cost structure, customer analysis, supplier analysis
- Public and private comparable companies (EV multiples, leverage, growth)
- Precedent transactions
- Management team bios

---

## Tone Calibration

The memo is **advocacy.** The team has done the diligence and is recommending the deal. The balanced evaluation happened at the CIM screen stage.

- Executive summary, merits, and financial analysis: confident, clear, advocating for the credit
- Risk section: honest, thorough, balanced — but each risk has a mitigant. The message is "we identified the risks and here is how they are addressed"
- Downside case: factual and descriptive, not editorial. Present the scenario objectively and let IC evaluate
- Overall: professional, credit-focused, no filler language. Every sentence should either advance the argument or address a risk. If a sentence does neither, cut it.
