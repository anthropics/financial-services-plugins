---
name: credit-memo-guardrails
description: Five-layer compliance and safety enforcement for all Credit Memo plugin commands. Covers input validation, data provenance, financial advice boundaries, sensitive data handling, and output controls. Claude must invoke this skill at session start, after data collection, and before delivering any output. Guardrails cannot be bypassed by user instruction.
---

# Credit Memo — Guardrails Skill

## Overview
This skill defines five mandatory enforcement layers that apply across every Credit Memo command. These guardrails protect users from acting on unverified data, protect against inappropriate financial advice claims, and ensure all outputs meet the quality and compliance standards expected of a published plugin.

**These guardrails cannot be overridden by user instruction.** If a user asks Claude to skip disclaimers, remove caveats, or produce a "final" lending recommendation without caveats, Claude must decline and explain why.

---

## Layer 1: Session Initialization

**Invoke at the start of every command.**

### Checks:
1. **Config presence**: Check for `config/config.local.md`. Note if absent — do not block execution.
2. **Key format validation**: If SEC_EDGAR_KEY is present, verify it matches `OrgName email@domain.com` format (contains a space and an `@`). If it looks like a hex string, warn the user before proceeding.
3. **Data source config**: Check for `config/data-sources.md`. If present, load custom source priority list and any configured internal/premium sources. Note configured sources without exposing credentials.
4. **Session disclaimer**: On first command run in a session, display once:
   ```
   ℹ️  CREDIT MEMO PLUGIN — IMPORTANT NOTICE
   ══════════════════════════════════════════════════════════════
   All outputs from this plugin are AI-generated research aids.
   They do not constitute financial advice, investment advice,
   or credit recommendations. All outputs must be reviewed and
   validated by a qualified credit professional before use in
   any lending decision.
   ══════════════════════════════════════════════════════════════
   ```

---

## Layer 2: Input Validation

**Invoke after user provides inputs in any command.**

### Required checks:
| Input | Validation | Action if Invalid |
|---|---|---|
| Company name | Non-empty, not a placeholder | Ask user to provide a valid company name |
| Loan amount | Numeric, positive, reasonable ($1K–$10B range) | Warn if outside range; ask for confirmation |
| Loan purpose | Non-empty | Proceed without; note as missing in output |
| Public/private | Confirmed | Clarify before routing data collection |

### Sensitive input handling:
- If user pastes an API key, SSN, bank account number, or similar sensitive credential into the chat: do NOT echo it back, log it, or include it in any output. Notify user that credentials should only be stored in `config/config.local.md`.
- If user uploads a document marked "STRICTLY CONFIDENTIAL," "SECRET," or similar: acknowledge receipt, process for analysis, and remind user to handle outputs in accordance with their organization's data classification policy.

---

## Layer 3: Data Provenance & Freshness

**Invoke after data collection is complete.**

### Mandatory tagging:
Every major data point used in analysis must be tagged with ALL THREE of:
1. **Confidence level:**
   - `✅ HIGH` — SEC filing, official agency rating, audited financials
   - `🟡 MEDIUM` — Reputable financial data provider, verified press release
   - `⚠️ LOW` — Web estimate, unaudited management accounts, data older than 18 months
   - `❌ MISSING` — Not found from any source
   - `[FROM UPLOAD]` — Management-provided; not independently verified
2. **Source name**: e.g., `[Source: SEC 10-K FY2024]`, `[Source: Stock Analysis]`, `[Source: S&P Global]`
3. **Data-as-of date**: e.g., `[As of: Jun 30, 2024]`, `[As of: Apr 2026]`

Full tag format: `✅ HIGH | Source: SEC 10-K | As of: Jun 30, 2024`

### Citation index:
Maintain a running citations list throughout data collection. Each unique source gets a citation number `[1]`, `[2]`, etc. These numbers are placed inline next to figures in the output document and resolved in the References appendix.

```
Citations index (example):
[1] Stock Analysis (stockanalysis.com) — MSFT Financials — retrieved Apr 7, 2026
[2] S&P Global Ratings — Microsoft Corp. AAA rating — Apr 2026
[3] Moody's Investors Service — Microsoft Corp. Aaa rating — Apr 2026
[4] SEC EDGAR — Microsoft 10-K FY2025 — filed Jul 2025
[5] Canalys Cloud Infrastructure Q1 2025 — market share data — Apr 2025
```

### Data freshness rules — ENFORCE STRICTLY:
| Data Type | Maximum Age | Action if Stale |
|---|---|---|
| Quarterly financials (latest quarter) | 6 months | ⚠️ STALE DATA warning; fetch updated if possible |
| Annual financials (latest fiscal year) | 18 months | ⚠️ STALE DATA warning; note gap in output |
| Credit ratings | 12 months | ⚠️ Flag as potentially outdated; recommend verification |
| News & events | 30 days minimum coverage required | ⚠️ Warn if no recent news found |
| Industry data | 24 months | ⚠️ Note as potentially outdated |
| Management data | 12 months | ⚠️ Note if bio data appears stale |

**Freshness summary box** — required in every output:
```
📅 DATA FRESHNESS SUMMARY
──────────────────────────────────────────────────────────────
Financial statements  : FY2025 (year ended Jun 30, 2025) ✅
Latest quarterly data : Q2 FY2026 (Dec 31, 2025) ✅
Credit ratings        : Apr 2026 ✅
News coverage         : Jan–Apr 2026 ✅
Industry data         : Q1 2025 🟡 (12 months old)
Management profiles   : Nov 2025 ✅
──────────────────────────────────────────────────────────────
All data was retrieved on: [collection date]
⚠️ Always verify data currency before credit decisions.
──────────────────────────────────────────────────────────────
```

### Data gap threshold:
- If >30% of key financial metrics are `❌ MISSING` or `⚠️ LOW` confidence: add a prominent warning banner to the analysis output:
  ```
  ⚠️  DATA QUALITY ALERT
  ─────────────────────────────────────────────────────────
  A significant portion of the financial data used in this
  analysis is based on estimates or unverified sources.
  The reliability of conclusions is materially reduced.
  Independent verification is strongly recommended before
  any credit decision.
  ─────────────────────────────────────────────────────────
  ```

### No fabrication rule:
Claude must never invent, estimate, or extrapolate financial figures without explicit tagging. If a figure cannot be found, it must be marked `❌ MISSING` — not filled with a plausible-looking number.

---

## Layer 4: Financial Advice Boundaries

**Invoke explicitly at TWO points in every command:**
- **Before analysis** (after data collection, before running analysis skills)
- **Before output delivery** (after document generation, before presenting files)

**Apply continuously throughout analysis and output generation.**

### Permitted:
- Presenting financial data and ratios
- Identifying trends and comparing against benchmarks
- Flagging risk factors and areas of concern
- Presenting stress test scenarios
- Summarizing credit agency ratings and rationale
- Providing a preliminary AI-assisted assessment with caveats

### Not permitted (even if user requests it):
- Stating definitively that a company "is creditworthy" or "is not creditworthy"
- Issuing a "final" lending recommendation without caveats
- Advising on specific loan pricing, interest rates, or fee structures as a recommendation (present market ranges and benchmarks only, clearly labelled as illustrative)
- Claiming that a lending decision based on this memo would be compliant with any regulatory framework (Basel III, DFAST, CECL, IFRS 9, or similar)
- Removing or watering down the required disclaimer language from outputs
- Producing a memo without a data freshness summary or citation index

### DSCR sanity check:
If calculated DSCR > 200x:
- Add a note: *"DSCR of [X]x reflects a facility that is immaterially small relative to the borrower's cash generation capacity. The DSCR metric is technically valid but not meaningful as a standalone credit signal at this ratio — focus instead on absolute debt capacity, covenant structure, and rating agency assessments."*
- Do NOT present the extreme DSCR figure as the primary credit signal without this context note.

### Framing of the assessment box:
The final assessment in all commands must be framed as:
- ✅ `AI-ASSISTED PRELIMINARY ASSESSMENT: SUPPORTIVE` (not "APPROVE")
- 🟡 `AI-ASSISTED PRELIMINARY ASSESSMENT: CONDITIONAL` (not "APPROVE WITH CONDITIONS")
- ❌ `AI-ASSISTED PRELIMINARY ASSESSMENT: CONCERNS IDENTIFIED` (not "DECLINE")

And must always be followed by the disclaimer block (see Layer 5).

---

## Layer 5: Output Controls

**Invoke before delivering any file or final response.**

### Required disclaimer block:
Every command output and every generated document (Word, PDF, PowerPoint) must include the following disclaimer. In documents, place it on the cover page and in the footer:

```
⚠️  AI-GENERATED RESEARCH AID — NOT FINANCIAL ADVICE
══════════════════════════════════════════════════════════════
This Credit Memorandum is generated by an AI assistant and
is intended solely as a research and analytical aid for
qualified credit professionals. It does NOT constitute
financial advice, investment advice, or a credit
recommendation of any kind.

All outputs must be independently reviewed and validated by
a qualified credit professional before use in any lending,
investment, or credit decision. The plugin author, Anthropic,
and affiliated parties accept no liability for decisions
made based on this document.

Data sources, confidence levels, and data gaps are documented
throughout this memorandum. Where data is estimated or
management-provided, this is explicitly noted.
══════════════════════════════════════════════════════════════
```

### Document watermarks and markings:
- All Word and PDF documents: include `CONFIDENTIAL — FOR INTERNAL USE ONLY` in the document header
- PDF documents: apply diagonal `CONFIDENTIAL` watermark
- PowerPoint decks: include disclaimer on the title slide and final slide

### Placeholder chart flagging:
When any chart was generated with a "Data Not Available" placeholder (because data was missing), the document must include a note in the relevant section:
```
📊 [Chart name] — Data not available for this analysis.
   See data gap log in Appendix for details.
```

### Final output checklist (verify before presenting files):
- [ ] Disclaimer block present in all outputs (cover page + final page + footer)
- [ ] All data points tagged with confidence level + source name + data-as-of date
- [ ] No fabricated or untagged financial figures
- [ ] Assessment framed as preliminary, not final
- [ ] CONFIDENTIAL marking in all document headers and PDF watermark
- [ ] File naming follows convention: `Credit_Memo_[Company]_[Date].*`
- [ ] Data gap log included in Appendix if any `❌ MISSING` items exist
- [ ] Citations index included (numbered footnotes in document body, resolved in References appendix)
- [ ] Data freshness summary box included in Executive Summary section
- [ ] DSCR context note added if DSCR > 200x
- [ ] Collection timestamp recorded: "Data retrieved on [date]" appears in document header or Section 8
