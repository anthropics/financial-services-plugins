---
name: refresh
description: Re-fetch the latest data for a previously analyzed company, compare against the prior Credit Memo baseline, and flag material changes. Useful for loan renewals, annual reviews, or when significant events occur.
---

# Command: /credit-memo:refresh

## Purpose
Re-fetch the latest data for a previously analyzed company and flag what has changed since the last Credit Memo was generated. Useful for loan renewals, annual reviews, or when significant events occur.

---

## Trigger
- `/credit-memo:refresh`
- "Refresh the data for [Company]"
- "What's changed for [Company] since our last memo?"
- "Annual review update for [Company]"
- "Update the credit memo for [Company]"

---

## Required Inputs
- Company Name
- [Optional] Date of previous Credit Memo (for comparison baseline)
- [Optional] Specific sections to refresh (all sections by default)

---

## Execution Steps

### STEP 0 — Invoke Guardrails
Invoke `guardrails` skill (Layer 1: Session Initialization) before any data collection.
Check `config/config.local.md` for API keys; load custom source priorities from `config/data-sources.md` if present.

### STEP 1 — Establish Baseline
Ask user: *"Do you have a previous Credit Memo date to compare against? (e.g., June 2023)"*
- If yes → use that date as the comparison baseline
- If no → compare against 12 months ago as default

### STEP 2 — Targeted Data Refresh
Invoke `guardrails` skill (Layer 3: Data Provenance & Freshness) after data collection — enforce date-of-collection stamps and freshness rules on all updated data points.
Pull only recently changed or newly published data:
- Latest 10-Q or 10-K filed since baseline date
- New credit rating actions (upgrades, downgrades, outlook changes)
- Material news events (M&A, litigation, leadership changes, earnings)
- Updated financial ratios from latest available period
- Industry data refresh (market size updates, new CAGR estimates)

### STEP 3 — Change Assessment Logic

For each data category, apply this significance test before flagging:

**Financial Metrics — Flag if:**
- Revenue change YoY > ±10%
- EBITDA margin change > ±3 percentage points
- Net Debt/EBITDA change > ±0.5x
- Current Ratio falls below 1.0 or rises above 3.0
- Free Cash Flow turns negative for 2+ quarters

**Credit Ratings — Flag if:**
- Any agency changes rating by ≥1 notch
- Any agency changes outlook (Stable → Negative, Positive → Watch, etc.)
- New rating action issued by any agency

**News & Events — Flag if:**
- Litigation filed or judgment >$10M (or >5% of annual revenue)
- M&A announced or completed
- C-suite leadership change (CEO, CFO, COO)
- Earnings miss vs. guidance >10%
- Regulatory investigation or enforcement action
- Default, covenant breach, or debt restructuring

**Overall Change Severity:**
- 🟢 No material changes — informational refresh only
- 🟡 Moderate changes — recommend review of affected sections
- 🔴 Material changes — recommend full Credit Memo update

### STEP 4 — Change Summary Output

```
📊 DATA REFRESH — [Company Name]
Baseline: [Previous Date] → Current: [Today's Date]
══════════════════════════════════════════════════════

📈 FINANCIAL CHANGES
  Revenue     : $X.Xbn → $X.Xbn  (+X.X% YoY)  ✅ Improved
  EBITDA Mgn  : X.X%  → X.X%    (-X.Xpp)      ⚠️ Declined
  Net Debt    : $X.Xbn → $X.Xbn  (Stable)      ✅ Stable
  DSCR        : X.Xx  → X.Xx    (Stable)       ✅ Stable

📊 RATING CHANGES
  S&P         : BBB    → BBB+    (Upgraded ↑)   ✅ Positive
  Moody's     : Baa2   → Baa2    (No change)    ✅ Stable
  Fitch       : BBB-   → BBB-    (No change)    ✅ Stable

📰 KEY EVENTS SINCE LAST MEMO
  ⚠️ [Date] — Filed $Xm lawsuit in [jurisdiction]
  ✅ [Date] — Completed acquisition of [Company]
  ⚠️ [Date] — CFO resigned; replacement appointed

🔄 OVERALL CHANGE SEVERITY: 🟡 MODERATE
   → Recommend: Review Risk Assessment and Management sections

══════════════════════════════════════════════════════
Run /credit-memo:generate to produce a full updated memo
```

### STEP 5 — Optional: Generate Amendment Memo
If changes are significant (🔴 Material), offer:
*"Would you like me to generate an amendment memo showing only the changed sections?"*

If yes → generate a delta document:
- Filename: `Credit_Memo_[Company]_REFRESH_[Date].docx`
- Include only sections with material changes
- Side-by-side comparison tables where applicable (Old → New)
- Executive summary of what changed and credit impact

> ⚠️ Refresh outputs are AI-generated and based on publicly available data. All changes and credit implications require review by a qualified credit professional before any lending decision.
