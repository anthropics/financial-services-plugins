---
description: "Screen a CIM or teaser for credit fit: Pass / Pursue / More Info"
argument-hint: "<attached CIM or teaser>"
---

# /private-credit:cim-screen

Produces a credit fit assessment from a CIM, teaser, or lender presentation. Output: **Pass / Pursue / More Info** with supporting analysis.

---

## Trigger

User invokes `/private-credit:cim-screen` with a CIM, teaser, or lender presentation attached or pasted.

---

## Required Context

Before running the screen, Claude must know the firm's credit box. If not already provided, ask for:
1. **Structure mandate:** Senior only? Unitranche? Mezzanine? Second lien?
2. **Size range:** Minimum and maximum hold size (or EBITDA range)
3. **Excluded industries:** Tobacco, firearms, cannabis, etc.
4. **Known IC preferences:** Customer concentration thresholds, geography restrictions, business type preferences or aversions (e.g., "IC does not like software," "IC prefers asset-heavy businesses")
5. **Leverage comfort:** Maximum leverage the firm will consider

If the credit box has been established in a prior conversation or configuration, use it without re-asking.

---

## Screening Workflow

### Step 1: Quick Read (Simulate the First 5-10 Minutes)

Read the document end to end. Identify:
- What is the business? (sector, product/service, scale, geography)
- What is the opportunity? (new financing, refinancing, add-on, dividend recap, acquisition financing)
- What capital is being sought? (amount, structure, position in cap stack)
- Who is the sponsor? (if PE-backed)

### Step 2: Hard Pass Check

Check the opportunity against the firm's credit box for hard disqualifiers:
- Structure mismatch (e.g., seeking junior capital, firm only offers senior)
- Excluded industry
- Size outside mandate (EBITDA too small or too large)
- Known IC dealbreaker (customer concentration above threshold, geography exclusion)
- ESG restriction

If any hard pass criteria are triggered, output **PASS** immediately with the specific reason. Do not continue the analysis.

### Step 3: Soft Pass Check

Check for soft disqualifiers — items that are not formal mandate exclusions but pattern-match to known IC aversions:
- Business type that IC has historically rejected
- Characteristics that raise well-known credit concerns for the firm
- Structural features that do not fit the firm's typical deal profile

If soft pass criteria are triggered, note them but continue the analysis. These influence the final recommendation but do not automatically result in a PASS.

### Step 4: Credit Assessment

Analyze the opportunity across these dimensions:

**Business quality:**
- Market position and competitive dynamics
- Revenue model (recurring vs. project vs. transactional)
- Customer concentration and diversification
- Growth trajectory and drivers
- Margin profile and stability

**Financial profile (from whatever data is available):**
- Revenue scale and trajectory
- EBITDA and margins
- Free cash flow generation capacity
- Working capital dynamics
- Capex requirements

**Leverage and structure (if provided, or build back-of-envelope):**
If capital structure and leverage are provided in the CIM, analyze them directly. If not, build a quick back-of-envelope model:
- Project EBITDA forward 3 years with reasonable assumptions for this type of business
- Plug in the proposed debt quantum and estimated market pricing
- Calculate cash interest expense and basic FCF
- Assess whether the business generates positive FCF at the proposed leverage
- If at market leverage the business does not generate positive FCF for the first 3 years, leverage is too high for this business
- Factor in business type: capital-intensive businesses with reinvestment requirements cannot support as much leverage even if near-term FCF looks acceptable

**Risk identification (at this stage):**
- Top 3-5 risks visible from the CIM
- Potential mitigants if identifiable
- Open questions that would need answers before making a full credit decision

### Step 5: Determine Output

| Recommendation | When to Use |
|---|---|
| **PASS** | Hard pass criteria triggered, OR the credit assessment reveals fundamental issues that make the opportunity unattractive regardless of terms (unsustainable leverage, structural mismatch with the firm's lending philosophy, critical business risk with no visible mitigant) |
| **PURSUE** | No hard or soft pass criteria triggered. Business quality, financial profile, and proposed leverage are within acceptable parameters. Risks are identifiable and appear mitigable. The opportunity fits the firm's credit box and appears attractive. |
| **MORE INFO** | Cannot make a definitive call with the information provided. This is the default for teasers (2-5 pages) where you can check hard criteria but cannot assess the full credit picture. For full CIMs, this applies only if 2-3 critical gating questions remain unanswered. |

**Bias toward PURSUE or MORE INFO.** Analysts should be biased toward learning more and spending time, not toward clearing opportunities quickly. Unless hard-no criteria are hit, lean toward continued evaluation.

---

## Output Format

Produce a 1-2 page narrative memo structured as follows:

### 1. Summary (3-5 sentences)
What the business is, what the opportunity is, and the recommendation (Pass / Pursue / More Info) with the primary reason.

### 2. What's Attractive (3-5 bullet points)
Business and financial merits identified from the CIM. Focus on characteristics that would resonate with a private credit IC: recurring revenue, strong margins, market leadership, low customer concentration, asset coverage, clear FCF generation.

### 3. Key Risks (3-5 bullet points)
Risks identified at this stage. Pair with mitigants where possible. Acknowledge where mitigants are unknown pending further diligence.

### 4. Financial Overview
Back-of-envelope summary tying the merits and risks to actual numbers:
- Revenue and EBITDA (current and trajectory)
- Proposed leverage and structure
- FCF assessment (positive/negative, magnitude)
- Covenant cushion estimate (if enough data)
- Sources & Uses if available

### 5. Open Questions / Next Steps
If PURSUE: What are the next steps? (management call, data room access, model build)
If MORE INFO: What specific information is needed to make a decision? Frame these as specific asks to the broker or sponsor — not vague requests.
If PASS: State the reason clearly. No further analysis needed.

---

## Calibration Notes

- For a **teaser** (2-5 pages): You can only check hard criteria and form a very preliminary view. Default output is MORE INFO unless a hard pass is triggered. Frame the "More Info" as "this fits our mandate on the surface — requesting the full CIM to evaluate further."
- For a **full CIM** (50-100+ pages): You should be able to make a PURSUE or PASS call. MORE INFO is only appropriate if 2-3 truly critical questions cannot be answered from the materials provided. Even then, the default approach is to PURSUE and flag the gating items rather than wait.
- The output is a **mini investment memo** — it should be clean, concise, and useful enough to share with the IC or deal team to align on whether to proceed.
