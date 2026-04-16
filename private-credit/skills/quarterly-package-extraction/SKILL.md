# Quarterly Package Extraction

This skill fires automatically when extracting financial data from borrower quarterly packages, compliance certificates, or any borrower-provided financial reporting for the purpose of updating a credit model.

---

## Extraction Order

Extract financial data top-down, following the natural order of the financial statements:

### Step 1: Income Statement / P&L

Start at the top of the P&L and work down:
- Revenue (by segment or line of business if provided)
- Cost of goods sold / Cost of revenue (if provided — many borrowers report gross profit only)
- Gross profit
- Operating expenses (by category if provided: SG&A, R&D, sales & marketing, G&A)
- Operating income / EBIT
- Depreciation & Amortization (may be embedded above or shown separately)
- EBITDA (reported)
- Adjustments (if shown on the P&L)
- Adjusted EBITDA (if shown)
- Interest expense
- Tax expense
- Net income

Extract whatever the borrower provides. If they report only Revenue → Gross Profit → Adjusted EBITDA, extract those three lines and note the gaps.

### Step 2: Balance Sheet

- Cash and cash equivalents
- Accounts receivable
- Inventory (if applicable)
- Other current assets
- Total current assets
- Property, plant & equipment
- Goodwill and intangibles
- Other long-term assets
- Total assets
- Accounts payable
- Accrued liabilities
- Current portion of long-term debt
- Other current liabilities
- Total current liabilities
- Long-term debt (by tranche if provided)
- Other long-term liabilities
- Total liabilities
- Total equity

Pay attention to how debt is reported — net of OID on the balance sheet vs. face value on the compliance certificate. Note any lease obligations, sale-leaseback financing, or other off-balance-sheet items that may count as debt for covenant purposes.

### Step 3: Cash Flow Statement

- Net income
- D&A add-back
- Stock-based compensation
- Changes in working capital (AR, inventory, AP, accrued liabilities, other)
- Operating cash flow
- Capital expenditures (split maintenance vs. growth if provided)
- Capitalized software (for software companies)
- Other investing activities
- Debt draws / repayments
- Equity contributions / distributions
- Other financing activities
- Net change in cash

### Step 4: Compliance Certificate

- Extract all covenant tests: covenant name, actual level, threshold, pass/fail
- Extract the compliance EBITDA calculation if provided (build-up from net income or reported EBITDA with each addback category)
- Extract net debt as calculated for covenant purposes
- Note any items where the cert calculation differs from what you would expect based on the financial statements

---

## Excel vs. PDF — Same Workflow

The workflow is identical regardless of whether the source is Excel or PDF:
1. Open the source document
2. Review the financials
3. Type the numbers into your own credit model

Even when the borrower provides an Excel file, it is safer and cleaner to type the numbers manually rather than copy-paste. Copy-paste can introduce hidden formatting issues, linked references to the source file, or misaligned rows. Manually entering the numbers forces the analyst to look at each line item and consider how it maps to the model.

---

## Label Matching and Template Customization

Borrower financials almost never use the same labels as your credit model template. The correct approach is to customize the template to match the borrower's reporting, not to force the borrower's data into rigid template labels.

### First-Time Setup (New Borrower)

When building a quarterly model for a new borrower for the first time:
- Start from your firm's base template (general structure, standard sections)
- Modify line item labels to match the borrower's actual reporting
- Add line items as needed — if the borrower has 10 revenue segments and your template has 2, add the additional segments and bucket the remainder into "Other"
- Apply the same customization to every section: revenue, cost structure, margins, operating expenses, EBITDA adjustments, balance sheet, cash flow
- This first-time setup is the heaviest lift in the monitoring workflow

### Subsequent Quarters

After the first quarter is set up:
- The template already matches the borrower's reporting structure
- Each subsequent quarter, you repeat the same mapping and input process
- Much faster and lighter — you already know where every line item goes
- Only adjust if the borrower changes their reporting format (new segments, reclassifications, restatements)

### Unmapped Line Items

When a borrower introduces a new line item or label you have not seen before:
- Do not guess where it maps
- Flag it: "New line item — [label] — $X.X — requires mapping decision"
- Determine whether it is a reclassification of an existing item, a genuinely new item, or an acquisition-related addition
- Add to the template once the mapping is confirmed

---

## Handling Discrepancies Between Financials and Compliance Certificate

### Rule: The Compliance Certificate Is the Source of Truth

The compliance certificate is a signed PDF document, executed by the CFO or another company officer. It is the authoritative source for covenant calculations. The Excel financial package is less formal.

### Discrepancies Are Not Errors

When numbers in the financial package differ from the compliance certificate, this almost always reflects a reporting difference, not an error:
- Debt reported net of OID on the balance sheet vs. face value on the cert
- Lease or financing obligations included in covenant debt per the credit agreement but classified differently on the balance sheet
- Letters of credit included or excluded based on credit agreement definition
- EBITDA adjustments visible in the cert but not separately identifiable in the P&L

**The analyst's job:** Identify the discrepancy, attempt to bridge it using the credit agreement definitions, and if the bridge is not possible with available information, raise the question with the management team or agent. Do not assume the cert is wrong. Do not assume the financials are wrong. Understand why the numbers differ.

### Debt Should Always Be Bridgeable

An analyst should almost always be able to reconcile the debt number between the balance sheet, the compliance certificate, and the credit agreement terms. The ingredients are: balance sheet debt, OID adjustment, lease/financing treatment per the agreement, and letter of credit inclusion. If you cannot bridge the debt, something is missing — escalate.

### EBITDA May Not Be Fully Bridgeable

The ability to reconcile EBITDA depends entirely on the quality of the borrower's reporting. With detailed reporting (full P&L down to net income, itemized adjustments), you can bridge. With minimal reporting (Revenue → Gross Profit → Adjusted EBITDA), you cannot — flag the limitation and work with what is available.

---

## Common Data Quality Issues

### Minimal Reporting

The most common issue is not data errors but **insufficient data.** Borrowers report the bare minimum required by the credit agreement:
- No historical comparisons unless required
- No budget comparison unless required
- No segment detail unless required
- Summary-level financials with limited line item granularity

**Analyst response:** Assess what you can build with the data provided. Identify what additional information would be needed for a complete credit assessment. Frame questions to management or the agent to fill the gaps.

### Acquisitions Embedded in Reporting

For acquisition-active borrowers, a common trap is that acquired company financials are folded into the reporting without restatement of prior periods. This means:
- Revenue and EBITDA jump significantly from one quarter to the next
- The increase is not labeled as acquisition-driven — it just appears as growth
- QoQ and YoY comparisons become misleading because prior periods do not include the acquired business

**Analyst response:**
- Track all acquisitions with close dates
- When financials show a material jump, check whether an acquisition closed during the period
- Ask for organic vs. inorganic breakdowns if not provided
- Adjust your QoQ and YoY analysis to separate organic growth from acquisition contribution where possible
- Note in your quarterly review when comparisons are distorted by acquisitions

### Other Issues (Rare but Worth Noting)

- **Mixed units:** Thousands vs. actuals vs. millions. Should be obvious from table headers and labels. Almost never an issue in practice.
- **Missing quarters:** If the borrower simply does not report a quarter, there is nothing to extract. Flag the gap and note it in the quarterly review.
- **Restated numbers:** Rare. If prior period numbers change without explanation, flag and investigate. This could indicate a restatement, a reclassification, or an error in the prior period reporting.

---

## Monthly to Quarterly / LTM Aggregation

When borrowers report monthly:
- Aggregate monthly figures into quarterly totals (3 months per quarter)
- Aggregate quarterly totals into LTM figures (4 quarters)
- No special adjustments or gotchas in the aggregation itself
- Consolidate, aggregate, and analyze — straightforward mechanical exercise
