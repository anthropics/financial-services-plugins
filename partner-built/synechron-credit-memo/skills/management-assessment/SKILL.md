---
name: credit-memo-management-assessment
description: Assesses the quality, experience, governance, and strategic execution of a borrower's management team and board of directors for credit purposes. Covers executive biographies, tenure, track record, governance structure, board composition, strategic initiatives, and risk management approach. Claude uses this skill automatically when evaluating management quality in Credit Memo generation.
---

# Credit Memo — Management Assessment Skill

## Overview
Management quality is a qualitative credit factor — but one of the most important. Poor management has destroyed sound businesses. Strong management has navigated companies through crises. The credit analyst's job is to form an informed view on whether this team can execute through the loan period.

---

## Data Collection Requirements
Gather from the following sources before running analysis:
- Company website (About/Leadership/Governance pages)
- SEC DEF 14A (Proxy Statement) — most detailed source of executive bios and compensation
- SEC 10-K (Part I — Business; Part III — Directors and Executive Officers)
- LinkedIn profiles of C-suite executives
- News search: `"{Executive name}" "{Company}" track record achievement`
- Glassdoor ratings (culture/management signals)
- Board composition databases

---

## Section 1: Key Management Profiles

### Questions to Answer:
- Who are the key management personnel and what is their background?
- What is the track record of the team at this company and previously?
- How long have key executives been in their roles?
- Have there been recent leadership changes and what was the impact?

> 📊 *[Embed: chart_mgmt_tenure.png — C-Suite Tenure Timeline]*

### Executive Summary Table:
| Role | Name | Tenure at Company | Total Industry Experience | Prior Company / Role |
|---|---|---|---|---|
| CEO | [Name] | X years | X years | [Previous role] |
| CFO | [Name] | X years | X years | [Previous role] |
| COO | [Name] | X years | X years | [Previous role] |
| CTO/CIO | [Name] | X years | X years | [Previous role] |

### Detailed Profiles (CEO and CFO — required; others if material):

**[Name] — [Title]**
- **Tenure:** X years (joined [year])
- **Education:** [Degree, Institution]
- **Prior Experience:** [Previous 2–3 roles in reverse chronological order]
- **Track Record at Company:** [Key achievements — revenue milestones, turnarounds, acquisitions completed, strategic pivots executed]
- **Industry Standing:** [Awards, board memberships, public recognition]
- **Adverse Findings:** [Any litigation, forced departures elsewhere, regulatory actions — note "None found" if clean]

### Leadership Stability Assessment:
| Indicator | Value | Signal |
|---|---|---|
| Average C-suite tenure | X years | >5y = Stable 🟢 / 2–5y = Watch 🟡 / <2y = Risk 🔴 |
| C-suite changes in last 24 months | X | 0–1 = Normal / 2–3 = Watch / >3 = Elevated |
| CEO/CFO both present >2 years | Yes/No | Both stable = 🟢 |
| Planned succession in place | Yes/No | Yes = 🟢 |
| Leadership vacuum in critical role | Yes/No | Yes = 🔴 |

---

## Section 2: Board of Directors Analysis

### Questions to Answer:
- What is the governance and organizational structure?
- How independent and qualified is the board?
- Does the governance structure protect creditors' interests?

### Board Composition Table:
| Director | Independent? | Committee | Primary Expertise | Tenure |
|---|---|---|---|---|
| [Name] — Chair | Yes/No | Audit, Comp | Finance | X yrs |
| [Name] | Yes/No | Risk | Industry | X yrs |
| [Name] (CEO) | No | — | Operations | X yrs |

### Governance Quality Scorecard:
Score each dimension (1–5, where 5 = best practice):
| Governance Dimension | Score | Observation |
|---|---|---|
| Board independence (>50% independent = best practice) | /5 | X% independent |
| Audit committee — all members financially literate | /5 | [Big 4 auditor / clean opinion] |
| Separate risk committee | /5 | [Present / Absent] |
| Executive compensation aligned with long-term performance | /5 | [LTI plan / vesting structure] |
| Shareholder rights (no classified board / dual-class shares) | /5 | [Notes] |
| ESG/sustainability oversight | /5 | [Dedicated committee / None] |
| Frequency of board meetings | /5 | [Quarterly or more = best] |
| **Overall Governance Score** | **/5** | |

### Governance Red Flags — Check Explicitly:
- [ ] Audit committee members without financial expertise
- [ ] CEO also serving as Board Chairman (concentration of power)
- [ ] Multiple undisclosed or inadequately disclosed related-party transactions
- [ ] Frequent auditor changes (>1 change in 5 years without explanation)
- [ ] Material weaknesses in internal controls disclosed in 10-K
- [ ] Dominant founding family with voting control but poor performance track record
- [ ] Lack of independent directors on audit or compensation committee

---

## Section 3: Strategic Execution Assessment

### Questions to Answer:
- What are the firm's stated strategic priorities?
- How well has management executed against past targets?
- What is the track record on financial guidance accuracy?

### Top Strategic Priorities (from CEO letters, investor presentations, 10-K):
1. [Strategic Priority 1]
2. [Strategic Priority 2]
3. [Strategic Priority 3]

### Guidance vs. Actual Performance (last 3 years):
| Year | Revenue Guidance | Actual Revenue | Variance | EBITDA Guidance | Actual EBITDA | Variance |
|---|---|---|---|---|---|---|
| FY2021 | $Xm | $Xm | +/- X% | $Xm | $Xm | +/- X% |
| FY2022 | $Xm | $Xm | +/- X% | $Xm | $Xm | +/- X% |
| FY2023 | $Xm | $Xm | +/- X% | $Xm | $Xm | +/- X% |

**Assessment:** *"Management has [consistently/mostly/rarely] met its financial guidance over the past three years. [Interpret what this means for the credibility of projections underpinning the repayment analysis.]*"

---

## Section 4: Financial Reporting Quality

### Reporting Quality Checklist:
| Factor | Status | Credit Risk |
|---|---|---|
| Big 4 / reputable auditor | Yes/No | Low/Medium |
| Clean audit opinion (last 3 years) | Yes/No | Low/High |
| Material weaknesses disclosed | None/Present | Low/High |
| Financial restatements (past 5 years) | None/X | Low/High |
| Related party transactions — adequate disclosure | Yes/No | Low/Medium |
| Segment reporting granularity | Detailed/Limited | Low/Medium |
| ESG/sustainability reporting published | Yes/No | — |
| On-time SEC filing history | Consistent/Late | Low/High |

---

## Section 5: Risk Management Culture

### Assessment Points:
- Does the company have a formal Enterprise Risk Management (ERM) framework?
- Is there a dedicated Chief Risk Officer (CRO) or equivalent role?
- How frequently does the board formally review risk?
- Has management's response to past risks (operational, financial, reputational) been effective? Reference specific examples.
- Is there a documented Business Continuity Plan (BCP)?
- How has management addressed technology/cybersecurity risk?

---

## Section 6: Management Assessment Summary

### Management Quality Score:
| Dimension | Score (1–5) | Rationale |
|---|---|---|
| Leadership experience & depth | /5 | |
| Leadership stability & succession planning | /5 | |
| Strategic execution track record | /5 | |
| Corporate governance quality | /5 | |
| Financial reporting quality & transparency | /5 | |
| Risk management maturity | /5 | |
| **Overall Management Score** | **/5** | |

**Score interpretation:**
- 4.0–5.0: Strong management — positive credit factor
- 2.5–3.9: Adequate management — neutral credit factor
- 1.0–2.4: Weak management — negative credit factor; consider as a risk condition in loan structure

### Management Credit Opinion (2 paragraphs):
**Paragraph 1:** Overall quality of management and governance — what stands out positively and negatively, and why.

**Paragraph 2:** Whether management quality strengthens or weakens the overall credit case, and any management-related conditions recommended for the loan structure. Examples:
- *"Key person life insurance on CEO and CFO recommended given their central role in the business."*
- *"Requirement to maintain a CFO with minimum X years of relevant industry experience."*
- *"Quarterly financial reporting covenant recommended given recent leadership transition."*
- *"No material change in senior management without lender notification within 5 business days."*
