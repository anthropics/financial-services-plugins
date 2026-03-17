---
name: xlsx-editor
description: "Edit existing Excel (.xlsx) workbooks while preserving formatting, formulas, styles, and structure. Handles cell updates, row/column insertion, formula repair, style-matched additions, and structural modifications without corrupting the file. Use when users say 'update this spreadsheet,' 'change these numbers,' 'add rows to this model,' 'fix this Excel file,' 'edit my workbook,' 'modify this sheet,' 'update the assumptions,' 'insert a new section,' 'reformat this table,' or any task that modifies an existing .xlsx file rather than creating one from scratch. Also triggers on 'edit xlsx,' 'update Excel,' 'change spreadsheet values,' 'add columns,' 'fix formatting,' 'match the style,' or 'preserve formatting.'"
---

# Excel Workbook Editor

## Overview

This skill edits **existing** Excel workbooks while preserving their formatting, formulas, structure, and design integrity. It is the complement to the xlsx creation skill — use this skill whenever the user provides an existing `.xlsx` file and wants modifications, not a blank-slate build.

**Core principle:** Leave everything you did not intentionally change exactly as it was.

---

## Environment Detection

- **If running inside Excel (Office Add-in / Office JS):** Use Office JS directly. Read via `range.values`, write via `range.values` or `range.formulas`. Formatting via `range.format.*`. Excel handles recalc natively.
- **If editing a standalone .xlsx file (Claude Code / Claude Web):** Use Python with openpyxl. Run `recalc.py` after edits to validate formulas.

The rest of this skill uses openpyxl examples. Translate to Office JS when in that environment — all principles apply identically.

---

## Critical Rules — Read Before Every Edit

### 1. Never Open with `data_only=True` and Save

```python
# WRONG — permanently destroys all formulas, replacing them with cached values
wb = openpyxl.load_workbook("model.xlsx", data_only=True)
# ... any edits ...
wb.save("model.xlsx")  # Every formula is now a hardcoded number. Unrecoverable.

# CORRECT — preserves formulas as strings
wb = openpyxl.load_workbook("model.xlsx")
```

Opening with `data_only=True` is only safe for **reading** computed values. Never save a workbook opened this way.

### 2. Preserve What You Don't Touch

When editing a workbook:
- Do NOT iterate over all cells and re-apply formatting
- Do NOT delete and recreate sheets
- Do NOT copy data to a new workbook
- Only write to the specific cells you intend to change
- Access cells directly by address: `ws["B5"] = new_value`

### 3. Formulas Over Hardcodes

When updating a cell that feeds other formulas, write a formula — not a computed value:

```python
# If B5 is an assumption that C5:G5 reference
ws["B5"] = 0.08  # OK — this is an input cell (blue)

# If D10 should be Revenue * Margin
ws["D10"] = "=D5*D8"  # CORRECT — formula
ws["D10"] = 1250000    # WRONG — breaks the model's flexibility
```

### 4. Style-Match New Content

When adding new rows, columns, or cells, match the surrounding formatting exactly. See the [Formatting Standards reference](references/formatting-standards.md) for the conventions.

### 5. Known openpyxl Limitations When Editing

openpyxl can silently corrupt complex workbooks. Be aware of these risks:

| Feature | Risk | Mitigation |
|---------|------|------------|
| Named ranges | May be silently dropped on save | Check `wb.defined_names` before and after; warn user if count changes |
| Conditional formatting | Complex rules may be stripped | Read `ws.conditional_formatting` before edit; verify after |
| Data validation | Dropdowns may be lost | Check `ws.data_validations` before and after |
| Charts | Chart data ranges may break if rows are inserted | Avoid inserting rows within a chart's data range |
| Pivot tables | Will be corrupted | Never edit workbooks with pivot tables using openpyxl — warn the user |
| Macros (.xlsm) | VBA code will be stripped | Refuse to edit .xlsm files; tell user to save as .xlsx first or use a different tool |
| Merged cells | May cause write errors | Check `ws.merged_cells.ranges` before writing to any cell in a merged region |
| Images/shapes | May shift if rows/columns are inserted | Warn user before structural changes to sheets with images |
| Sparklines | Will be removed | Warn user before saving |

**Pre-edit safety check** — run this before any modification:

```python
import openpyxl

def pre_edit_audit(filepath):
    """Audit workbook for features that openpyxl may corrupt."""
    wb = openpyxl.load_workbook(filepath)
    warnings = []

    # Check for macros
    if filepath.endswith('.xlsm'):
        warnings.append("BLOCKING: File contains macros (.xlsm). openpyxl will strip VBA code. Cannot safely edit.")

    # Check named ranges
    named_count = len(list(wb.defined_names.definedName))
    if named_count > 0:
        warnings.append(f"WARNING: {named_count} named ranges detected. Will verify preservation after edit.")

    for ws in wb.worksheets:
        # Conditional formatting
        if ws.conditional_formatting:
            warnings.append(f"WARNING: Sheet '{ws.title}' has {len(list(ws.conditional_formatting))} conditional formatting rules.")

        # Data validations
        if ws.data_validations and ws.data_validations.dataValidation:
            warnings.append(f"WARNING: Sheet '{ws.title}' has {len(ws.data_validations.dataValidation)} data validation rules.")

        # Merged cells
        if ws.merged_cells.ranges:
            warnings.append(f"INFO: Sheet '{ws.title}' has {len(ws.merged_cells.ranges)} merged cell regions.")

        # Charts
        if ws._charts:
            warnings.append(f"WARNING: Sheet '{ws.title}' has {len(ws._charts)} charts. Row/column insertion may break chart ranges.")

    wb.close()
    return warnings
```

**If any BLOCKING warning is raised, stop and inform the user.** For WARNING items, inform the user and proceed with caution. For INFO items, proceed normally but remain aware.

---

## Workflow

### Step 1: Understand the File

Before making any changes, read the workbook and understand its structure:

```python
wb = openpyxl.load_workbook("model.xlsx")

# Survey all sheets
for ws in wb.worksheets:
    print(f"Sheet: {ws.title}, Dimensions: {ws.dimensions}")

# Identify the layout of the target sheet
ws = wb["Sheet1"]
# Read headers, identify input cells vs formula cells, note formatting patterns
```

Report to the user:
- Sheet names and their apparent purpose
- The area you plan to modify
- Any risks from the pre-edit audit

### Step 2: Run the Pre-Edit Audit

Run `pre_edit_audit()` and present findings to the user. If there are BLOCKING issues, stop. If there are WARNINGs, explain the risk and ask whether to proceed.

### Step 3: Snapshot Key Metadata

Before editing, capture metadata you will verify after saving:

```python
# Capture before-state
before_named_ranges = len(list(wb.defined_names.definedName))
before_cf_rules = {}
before_dv_rules = {}
for ws in wb.worksheets:
    before_cf_rules[ws.title] = len(list(ws.conditional_formatting))
    if ws.data_validations and ws.data_validations.dataValidation:
        before_dv_rules[ws.title] = len(ws.data_validations.dataValidation)
```

### Step 4: Make the Edits

Apply the requested changes using the patterns in the [Edit Patterns reference](references/edit-patterns.md). Key principles:

**Updating cell values:**
```python
# Direct cell access — preserves all other cells
ws["B5"] = 0.12          # Update an input
ws["C3"] = "Q1 2026"     # Update a label
ws["D10"] = "=D5*D8"     # Update a formula
```

**Matching existing formatting when writing new content:**
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from copy import copy

def copy_style(source_cell, target_cell):
    """Copy all formatting from source to target cell."""
    target_cell.font = copy(source_cell.font)
    target_cell.fill = copy(source_cell.fill)
    target_cell.border = copy(source_cell.border)
    target_cell.alignment = copy(source_cell.alignment)
    target_cell.number_format = source_cell.number_format
    target_cell.protection = copy(source_cell.protection)
```

**Inserting rows while preserving formatting:**
```python
def insert_row_with_style(ws, row_idx, source_row_idx=None):
    """Insert a row and copy formatting from a source row."""
    ws.insert_rows(row_idx)
    if source_row_idx:
        # After insertion, source_row has shifted down by 1 if it was at or below row_idx
        actual_source = source_row_idx + 1 if source_row_idx >= row_idx else source_row_idx
        for col in range(1, ws.max_column + 1):
            source_cell = ws.cell(row=actual_source, column=col)
            target_cell = ws.cell(row=row_idx, column=col)
            copy_style(source_cell, target_cell)
```

**Updating formulas that reference shifted rows:**
After inserting or deleting rows, openpyxl does NOT automatically update formula references. You must:
1. Identify formulas that reference rows at or below the insertion point
2. Manually adjust the row numbers in those formulas
3. Or, better: use named ranges or table references that are position-independent

### Step 5: Post-Edit Validation

After saving, verify that nothing was silently corrupted:

```python
wb.save("model_edited.xlsx")

# Reload and verify
wb_check = openpyxl.load_workbook("model_edited.xlsx")

after_named_ranges = len(list(wb_check.defined_names.definedName))
if after_named_ranges != before_named_ranges:
    print(f"WARNING: Named ranges changed: {before_named_ranges} -> {after_named_ranges}")

for ws in wb_check.worksheets:
    after_cf = len(list(ws.conditional_formatting))
    if after_cf != before_cf_rules.get(ws.title, 0):
        print(f"WARNING: Conditional formatting on '{ws.title}' changed: {before_cf_rules[ws.title]} -> {after_cf}")
```

### Step 6: Formula Recalculation (Standalone Files Only)

If editing a standalone .xlsx (not inside Excel), run the recalculation script to validate all formulas compute correctly:

```python
# recalc.py uses LibreOffice headless to recalculate and check for errors
# python recalc.py model_edited.xlsx 30
```

If `recalc.py` is not available, warn the user:
> The edited file has been saved. Formula values shown in Excel may be stale until you open the file and press Ctrl+Alt+F9 (full recalc). I was unable to run automated recalculation — please verify formula outputs manually.

### Step 7: Save Strategy

**Always save to a new filename first**, then let the user decide whether to overwrite:

```python
import os

original = "model.xlsx"
edited = "model_edited.xlsx"
wb.save(edited)

# Report to user
print(f"Saved edited file as '{edited}'. Original '{original}' is unchanged.")
print("Rename or overwrite when you've verified the edits.")
```

If the user explicitly asks to overwrite the original, do so — but always confirm first.

---

## Common Edit Scenarios

### Scenario 1: Update Assumptions / Inputs

The simplest and safest edit. Change input cells (typically blue-formatted), let formulas recalculate.

```python
wb = openpyxl.load_workbook("lbo_model.xlsx")
ws = wb["Assumptions"]

# Update specific inputs
ws["C5"] = 0.08    # Revenue growth rate
ws["C6"] = 0.22    # EBITDA margin
ws["C7"] = 4.5     # Entry multiple

wb.save("lbo_model_updated.xlsx")
```

### Scenario 2: Add New Line Items to a Financial Model

When inserting rows into a model (e.g., adding a new revenue line), you must:
1. Insert the row
2. Copy formatting from adjacent rows
3. Write formulas for the new row
4. Update any SUM ranges that should include the new row

See [Edit Patterns: Inserting Line Items](references/edit-patterns.md#inserting-line-items) for the full pattern.

### Scenario 3: Reformat an Existing Table

When the user wants consistent formatting applied across a table:
1. Identify the table boundaries
2. Read the desired style (from user instructions or from a "model" row)
3. Apply formatting without changing values or formulas

See [Formatting Standards](references/formatting-standards.md) for IB/PE conventions.

### Scenario 4: Add a New Sheet to an Existing Workbook

```python
# Add a new sheet without disturbing existing sheets
ws_new = wb.create_sheet("Sensitivity", index=len(wb.sheetnames))

# Copy header formatting from an existing sheet for consistency
ws_source = wb["Returns"]
for col in range(1, ws_source.max_column + 1):
    source_cell = ws_source.cell(row=1, column=col)
    target_cell = ws_new.cell(row=1, column=col)
    copy_style(source_cell, target_cell)
    target_cell.value = source_cell.value  # Copy headers
```

### Scenario 5: Fix Broken Formulas

When formulas show errors (#REF!, #DIV/0!, etc.):
1. Open with `data_only=False` (default)
2. Read the formula string from the cell
3. Diagnose the issue (missing sheet reference, shifted rows, division by zero)
4. Write the corrected formula
5. Run recalc to verify

---

## Financial Services Formatting Conventions

When editing financial models, match these conventions unless the existing file uses a different standard. See [Formatting Standards](references/formatting-standards.md) for the complete reference.

**Quick reference:**

| Element | Font Color | Fill | Number Format |
|---------|-----------|------|---------------|
| Hardcoded inputs | Blue (`#0000FF`) | None or light yellow | Varies by type |
| Formulas | Black (`#000000`) | None | Varies by type |
| Cross-sheet links | Green (`#008000`) | None | Match source |
| Section headers | White (`#FFFFFF`) | Dark blue (`#1F4E79`) | Text |
| Subtotals | Black, **bold** | Light gray (`#D9E2F3`) | Match column |
| Grand totals | Black, **bold** | Medium gray (`#B4C6E7`) | Match column |
| Negative numbers | Red or `(parentheses)` | None | `#,##0;(#,##0)` |
| Percentages | Match cell type | None | `0.0%` |
| Currency (millions) | Match cell type | None | `#,##0.0` with "($M)" header |

---

## Error Recovery

If an edit goes wrong:

1. **You saved to a new file (recommended):** The original is untouched. Discard the edited file and retry.
2. **You overwrote the original:** Check if the user has version control, a backup, or if the file was recently saved in a cloud service with version history.
3. **openpyxl corrupted the file:** The file may not open in Excel. This is a known limitation with complex workbooks. Inform the user and suggest restoring from the original.

**Prevention is better than recovery.** Always:
- Save to a new filename first
- Run the pre-edit audit
- Verify metadata after saving
