---
name: quick-risk
description: Run a rapid 2-minute preliminary risk screen on a company. Returns a risk scorecard for initial deal screening — not a substitute for a full Credit Memo or professional credit review.
---

# Command: /credit-memo:quick-risk

## Purpose
Run a rapid preliminary risk screen on a company — takes approximately 2 minutes. Returns a risk scorecard without generating the full Credit Memo. Intended for initial deal screening before committing to full analysis.

> ⚠️ This is a screening tool only. It is not a creditworthiness determination and cannot substitute for a full Credit Memo or qualified professional credit review.

---

## Trigger
- `/credit-memo:quick-risk`
- "Quick risk screen on [Company]"
- "Preliminary check on [Company]"
- "Do a fast screening for [Company]"
- "Should I proceed with a full memo on [Company]?"

---

## Required Inputs
- Company Name
- [Optional] Loan Amount

---

## Execution Steps

### STEP 1 — Invoke Guardrails (Layer 1)
Invoke `guardrails` skill before data collection.

### STEP 2 — Rapid Data Pull
Collect in parallel (lightweight):
- Latest credit ratings (Moody's, S&P, Fitch) via web search
- Most recent quarterly financials (1 source — Stock Analysis or SEC)
- Top 5 recent news headlines
- Any default, litigation, or distress flags

### STEP 3 — Score & Flag
Calculate a quick Risk Score across 5 dimensions (score each 1–5):

| Dimension | Score (1=High Risk, 5=Low Risk) | Key Signal |
|---|---|---|
| Credit Rating | — | External agency rating |
| Financial Health | — | Debt/Equity, Current Ratio |
| News Sentiment | — | Recent negative news |
| Industry Risk | — | Sector cyclicality |
| Litigation / Default | — | Legal flags |

**Overall Score**: Average of 5 dimensions
- 4.0–5.0 → 🟢 Low preliminary risk — consider full Credit Memo
- 2.5–3.9 → 🟡 Moderate preliminary risk — full memo required before proceeding
- 1.0–2.4 → 🔴 Elevated preliminary risk — flag for senior review before full memo

### STEP 4 — Output
Return a formatted risk screen card in chat (no document generated):

```
⚡ PRELIMINARY RISK SCREEN — [Company Name]
════════════════════════════════════════════
Credit Rating    : BBB (S&P) | Baa2 (Moody's)
Revenue (Latest) : $X.Xbn
Net Debt/EBITDA  : X.Xx
Current Ratio    : X.X
Recent News      : [Positive / Neutral / Negative]
Legal Flags      : [None found / ⚠️ See below]
────────────────────────────────────────────
SCREEN SCORE     : X.X/5.0 — 🟢 LOW PRELIMINARY RISK
────────────────────────────────────────────
Next Step: Run /credit-memo:generate for full analysis

⚠️  IMPORTANT
This screen is an AI-assisted preliminary indicator only.
It is based on limited data and does NOT constitute a
creditworthiness assessment or financial advice.
A full Credit Memo and qualified professional review are
required before any credit decision.
════════════════════════════════════════════
```

---

## Notes
- If any red flags are found, list them explicitly below the main card
- Always recommend full analysis before any credit approval
- Score thresholds are indicative only — not calibrated to any specific credit policy
