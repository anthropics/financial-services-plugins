# Company Research Report Generation Workflow

This document defines the execution workflow for generating a company research report draft.

## Required Order

The workflow must run in this order:

1. Request classification
2. Recency and authority gate
3. Evidence collection
4. Fact Pack
4.5. Analysis Kit Construction
5. Investment View Pack
6. Body Draft
7. Front Page Summary
8. Verification
9. Delivery preparation

Do not generate the front page before the body draft and verification inputs exist.

## Step 1: Request classification

Use the request-classification rules to choose:

- initiating coverage
- earnings review / company update
- general company analysis
- clarification required

## Step 2: Recency and authority gate

Check:

- latest formal reporting period available
- latest disclosure date available
- authority rank of primary sources
- whether the run is still eligible for a current full report

If the run fails this gate:

- switch to degraded mode
- or block the full report and explain the data gap

## Step 3: Evidence collection

Collect the minimum evidence required by the evidence contract.

If the evidence threshold is not met:

- switch to degraded mode
- or ask for clarification

## Step 4: Fact Pack

Build a structured evidence pack containing:

- company identity
- primary disclosures used
- current financial evidence
- key context evidence
- risk evidence
- evidence gaps

## Step 4.5: Analysis Kit Construction

Based on the Fact Pack, the following structured outputs must be completed before drafting. Body Draft (Step 6) must be based on this Kit — direct narrative from Fact Pack is prohibited.

**Gate: Analysis Kit incomplete → must not enter Body Draft.**

### 4.5.1 Financial table pre-fill

- Fill collected financial data into the standard table structure defined in chinese-report-template.md §5.1
- Mark source for each number
- Mark N/A for missing cells
- Minimum: 7 rows × available fiscal years

### 4.5.2 Comparable company screening (Class A required)

- Select 3-5 comparable companies
- Obtain valuation multiples (EV/Revenue, EV/EBITDA, P/E as applicable)
- Document selection rationale (business model similarity, growth stage, market)
- If unavailable: record "无法建立可比框架" with specific data gaps

### 4.5.3 Risk layering

- Classify all identified risk factors by severity (高/中/低)
- Write one-sentence transmission mechanism for each risk
- Identify at least one counter-evidence point against the core thesis

### 4.5.4 Scenario assumptions (Class A required)

- Define Bull/Base/Bear core driver assumption differences
- Assign probability weights
- If insufficient data: record "数据不足以构建情景分析" with specific gaps

### Output format

Structured Analysis Kit (Markdown tables or JSON). This Kit becomes the mandatory input for Step 6 Body Draft.

## Step 5: Investment View Pack

Build a concise analytical pack containing:

- core judgment
- main supporting points
- key risks
- variables that need validation
- valuation state and peer framing (based on Analysis Kit §4.5.2)

## Step 6: Body Draft

Generate the main report body using the Chinese report template.

The body draft must follow the approved section order.

**Mandatory**: Body Draft must be based on the Analysis Kit from Step 4.5. Financial tables, comparable company tables, scenario analysis, and risk matrix must be populated from the Kit, not generated ad hoc during drafting.

## Step 7: Front Page Summary

Only after the body draft exists, generate the top summary:

- key conclusions
- strongest evidence
- uncertainties to track

## Step 8: Verification

Check:

- source hierarchy compliance
- recency and authority compliance
- degraded-mode compliance if applicable
- section completeness
- prohibited-output compliance
- user-message gating compliance

## Step 9: Delivery preparation

Prepare:

- summary message
- Feishu Doc creation and write plan
- Feishu Doc URL
- optional internal markdown artifact reference
- source/scope note

For successful report runs:

- create the Feishu Doc after verification passes
- write the report body into the doc
- verify the resulting doc token or URL is available before replying
- ensure only user-valuable messages are sent outward

## Completion Gate

The workflow is complete only if:

- every prior step has been executed in order
- verification has run
- the output path matches the Feishu delivery contract
- successful report runs return a Feishu Doc URL instead of only a local path
