---
name: check-model
description: Debug and audit financial models for errors — circular references, broken formulas, hardcoded overrides, balance sheet imbalances, cash flow mismatches, and logic gaps. Use when a model isn't tying, producing unexpected results, or before sending to a client or IC. Triggers on "debug model", "model check", "audit model", "model won't balance", "something's off in my model", "check my model", "QA model", or "model review".
---

# Model Checker

## Workflow

### Step 1: Ingest the Model

- Accept the user's Excel model (.xlsx or .xlsm)
- Identify model type: DCF, LBO, merger, 3-statement, comps, returns, or custom
- Map the structure: which tabs exist, how they're linked, where inputs vs. outputs live

### Step 2: Structural Checks

**Tab & Layout Review:**
- Are inputs clearly separated from calculations?
- Is there a consistent color-coding convention? (blue = input, black = formula, green = link)
- Are there hidden tabs or rows that could contain overrides?
- Is the model flow logical? (assumptions → IS → BS → CF → valuation)

**Formula Consistency:**
- Check for hardcoded numbers inside formulas (partial hardcodes)
- Check for inconsistent formulas across row/column ranges (should be the same formula dragged across)
- Identify any #REF!, #VALUE!, #N/A, #DIV/0! errors
- Flag cells that are formatted as formulas but contain hardcoded values

### Step 3: Integrity Checks

**Balance Sheet:**
- Total Assets = Total Liabilities + Equity (every period)
- If imbalanced, quantify the gap and trace where it breaks
- Check that retained earnings rolls forward correctly: Prior RE + Net Income - Dividends = Current RE
- Verify goodwill and intangibles flow from acquisition assumptions (if M&A model)

**Cash Flow Statement:**
- Ending cash from CF = Cash on BS (every period)
- Operating CF + Investing CF + Financing CF = Change in Cash
- D&A on CF matches D&A on IS
- Capex on CF matches PP&E rollforward on BS
- Working capital changes on CF match BS movements (AR, AP, inventory)

**Income Statement:**
- Revenue builds tie to segment/product detail
- COGS and gross margin are consistent with assumptions
- Tax expense = Pre-tax income × tax rate (check for deferred tax adjustments)
- Share count ties to dilution schedule (options, converts, buybacks)

**Circular References:**
- Check for circular references (interest expense → debt balance → cash → interest)
- If intentional (common in LBO/3-statement models), verify the iteration toggle works
- If unintentional, trace the loop and suggest how to break it

### Step 4: Logic Checks

**Reasonableness:**
- Do growth rates make sense? (100%+ revenue growth without explanation = red flag)
- Are margins within industry norms? Flag outliers
- Does terminal value dominate the DCF? (>75% of EV from TV is a yellow flag)
- Are projections hockey-sticking unrealistically?
- Does EBITDA growth compound to an absurd number by Year 10?

**Sensitivity & Edge Cases:**
- What happens at 0% growth? Negative growth?
- Does the model break with negative EBITDA?
- Do leverage ratios go negative or exceed realistic bounds?
- Are there any divide-by-zero risks?

**Cross-Tab Consistency:**
- Do linked cells actually match their source? (copy-paste errors are common)
- Are date headers consistent across all tabs?
- Do units match (thousands vs. millions vs. actuals)?

### Step 5: Common Bugs by Model Type

**DCF:**
- Discount rate applied to wrong period (mid-year vs. end-of-year convention)
- Terminal value not discounted back correctly
- WACC uses book values instead of market values
- FCF includes interest expense (should be unlevered)
- Tax shield double-counted

**LBO:**
- Debt paydown doesn't match cash sweep mechanics
- PIK interest not accruing to debt balance
- Management rollover not reflected in returns
- Exit multiple applied to wrong EBITDA (LTM vs. NTM)
- Fees and expenses not deducted from Day 1 equity

**Merger Model:**
- Accretion/dilution uses wrong share count (pre- vs. post-deal)
- Synergies not phased in correctly
- Purchase price allocation doesn't balance
- Foregone interest on cash not included
- Transaction fees not in sources & uses

**3-Statement:**
- Working capital changes have wrong sign convention
- Depreciation doesn't match PP&E schedule
- Debt maturity schedule doesn't match principal payments
- Dividends paid exceed net income without explanation

### Step 6: Report

Generate a model audit report:

**Summary:**
- Model type and overall assessment (Clean / Minor Issues / Major Issues)
- Number of issues found by severity

**Issue Log:**

| # | Tab | Cell/Range | Severity | Category | Description | Suggested Fix |
|---|-----|-----------|----------|----------|-------------|--------------|
| 1 | | | Critical/Warning/Info | Formula/Logic/Balance/Hardcode | | |

**Severity Definitions:**
- **Critical**: Model produces wrong output (BS doesn't balance, formulas broken)
- **Warning**: Model works but has risks (hardcodes, inconsistent formulas, edge case failures)
- **Info**: Style and best practice suggestions (color coding, layout, naming)

### Step 7: Output

- Issue log table (in chat or Excel)
- Annotated model with comments on flagged cells (if user provides the file)
- Summary assessment with fix priority

## Important Notes

- Always check the BS balance first — if it doesn't balance, nothing else matters until it does
- Hardcoded overrides are the #1 source of model errors — search aggressively for them
- Sign convention errors (positive vs. negative for cash outflows) are extremely common
- Models that "work" can still be wrong — sanity-check outputs against industry benchmarks
- If the model uses VBA macros, note any macro-driven calculations that can't be audited from formulas alone
- Don't change the model without asking — report issues and let the user decide how to fix
