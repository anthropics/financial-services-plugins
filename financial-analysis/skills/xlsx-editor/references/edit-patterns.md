# Edit Patterns Reference

Common patterns for modifying existing Excel workbooks safely with openpyxl.

---

## Pattern 1: Updating Cell Values

The simplest and safest edit — change specific cell values without touching anything else.

```python
import openpyxl

wb = openpyxl.load_workbook("model.xlsx")
ws = wb["Assumptions"]

# Update individual cells
ws["C5"] = 0.08         # Numeric input
ws["C6"] = "Q1 2026"    # Text label
ws["C7"] = "=C5*C6"     # Formula

# Update a block of cells
updates = {
    "C5": 0.08,
    "C6": 0.22,
    "C7": 4.5,
    "C8": 3.5,
}
for cell_ref, value in updates.items():
    ws[cell_ref] = value

wb.save("model_updated.xlsx")
```

**When to use:** Changing assumptions, updating inputs, correcting typos, fixing formulas.

---

## Pattern 2: Batch Update a Column or Row

```python
# Update an entire column of values (e.g., updating actuals for a new quarter)
new_actuals = [125.3, 42.1, 33.7, 18.5, 23.6, 8.2, 15.3]
start_row = 5
col = 7  # Column G

for i, value in enumerate(new_actuals):
    ws.cell(row=start_row + i, column=col, value=value)
    # Preserve input formatting (blue font for actuals)
    ws.cell(row=start_row + i, column=col).font = Font(color="0000FF")
```

---

## Pattern 3: Inserting Line Items

Adding a new row to a financial model while preserving structure and formulas.

```python
from copy import copy
from openpyxl.styles import Font

def insert_line_item(ws, insert_at, label, source_row=None):
    """
    Insert a new line item row into a financial model.

    Args:
        ws: Worksheet
        insert_at: Row number where the new row will be inserted
        label: Label for column A
        source_row: Row to copy formatting from (defaults to insert_at - 1, pre-insertion)
    """
    if source_row is None:
        source_row = insert_at  # Will become insert_at + 1 after insertion

    # Step 1: Insert the row
    ws.insert_rows(insert_at)

    # Step 2: The source row has shifted down by 1
    actual_source = source_row + 1 if source_row >= insert_at else source_row

    # Step 3: Copy formatting from source row
    for col in range(1, ws.max_column + 1):
        src_cell = ws.cell(row=actual_source, column=col)
        tgt_cell = ws.cell(row=insert_at, column=col)
        tgt_cell.font = copy(src_cell.font)
        tgt_cell.fill = copy(src_cell.fill)
        tgt_cell.border = copy(src_cell.border)
        tgt_cell.alignment = copy(src_cell.alignment)
        tgt_cell.number_format = src_cell.number_format

    # Step 4: Set the label
    ws.cell(row=insert_at, column=1, value=label)

    return insert_at


# Example: Add "Other Revenue" line item above the Total Revenue row
# Suppose Total Revenue is at row 12 and sums rows 8:11
total_row = 12
new_row = insert_line_item(ws, insert_at=total_row, label="  Other Revenue")

# Write formulas for the new row (matching pattern from adjacent rows)
for col in range(3, 9):  # Columns C through H (years)
    ws.cell(row=new_row, column=col, value=0)  # Placeholder input
    ws.cell(row=new_row, column=col).font = Font(color="0000FF")  # Blue = input
```

### Updating SUM Ranges After Insertion

**Critical:** After inserting a row, any SUM formula that should include the new row must be updated manually. openpyxl does NOT auto-expand SUM ranges.

```python
# Before insertion: =SUM(C8:C11) at row 12
# After inserting at row 12: Total is now at row 13, new row is 12
# The SUM is still =SUM(C8:C11) — it did NOT expand to include row 12

# Fix: Update the SUM formula
for col in range(3, 9):
    col_letter = chr(64 + col)  # C, D, E, ...
    ws.cell(row=13, column=col).value = f"=SUM({col_letter}8:{col_letter}12)"
```

**Best practice:** When possible, structure SUM ranges to include a blank row as a buffer. `=SUM(C8:C12)` where row 12 is blank — inserting at row 12 pushes the blank to 13 and the SUM auto-expands to include the new row 12.

---

## Pattern 4: Deleting Rows Safely

```python
def delete_row_safe(ws, row_idx, check_references=True):
    """
    Delete a row after checking for formula references to it.

    Args:
        ws: Worksheet
        row_idx: Row to delete
        check_references: If True, scan for formulas referencing this row
    """
    if check_references:
        # Scan all cells for formulas referencing this row
        row_refs = []
        for row in ws.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str) and cell.value.startswith("="):
                    # Simple check — look for row number in formula
                    if f"${row_idx}" in cell.value or f"{row_idx})" in cell.value or f"{row_idx}:" in cell.value:
                        row_refs.append(f"{cell.coordinate}: {cell.value}")

        if row_refs:
            print(f"WARNING: {len(row_refs)} formulas reference row {row_idx}:")
            for ref in row_refs[:10]:
                print(f"  {ref}")
            return False  # Do not delete — return False to signal

    ws.delete_rows(row_idx)
    return True
```

---

## Pattern 5: Adding a New Column (e.g., New Year)

```python
def add_year_column(ws, insert_col, year_label, source_col):
    """
    Add a new year column to a financial model by copying structure from an existing year.

    Args:
        ws: Worksheet
        insert_col: Column index where the new column will be inserted
        year_label: Header label (e.g., "2027E")
        source_col: Column index to copy formatting and formula patterns from
    """
    ws.insert_cols(insert_col)

    # Copy formatting from source column
    for row in range(1, ws.max_row + 1):
        src_cell = ws.cell(row=row, column=source_col + 1)  # Source shifted right
        tgt_cell = ws.cell(row=row, column=insert_col)
        tgt_cell.font = copy(src_cell.font)
        tgt_cell.fill = copy(src_cell.fill)
        tgt_cell.border = copy(src_cell.border)
        tgt_cell.alignment = copy(src_cell.alignment)
        tgt_cell.number_format = src_cell.number_format

    # Set header
    ws.cell(row=1, column=insert_col, value=year_label)

    # Copy column width
    from openpyxl.utils import get_column_letter
    src_letter = get_column_letter(source_col + 1)
    tgt_letter = get_column_letter(insert_col)
    ws.column_dimensions[tgt_letter].width = ws.column_dimensions[src_letter].width
```

---

## Pattern 6: Reformatting an Existing Table

Apply consistent formatting to a table without changing any values or formulas.

```python
def reformat_table(ws, start_row, end_row, start_col, end_col,
                   header_row=True, total_row=False):
    """Apply clean financial table formatting to an existing range."""

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            cell = ws.cell(row=row, column=col)

            # Header row
            if header_row and row == start_row:
                cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
                cell.fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = Border(bottom=Side(style="thin"))

            # Total row
            elif total_row and row == end_row:
                cell.font = Font(name="Calibri", size=10, bold=True)
                cell.border = Border(top=Side(style="thin"), bottom=Side(style="double"))

            # Data rows
            else:
                cell.font = Font(name="Calibri", size=10)
                # Alternate row shading
                if (row - start_row) % 2 == 0:
                    cell.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

            # Right-align numbers, left-align text (column A)
            if col == start_col:
                cell.alignment = Alignment(horizontal="left", indent=1)
            else:
                cell.alignment = Alignment(horizontal="right")
```

---

## Pattern 7: Merging/Unmerging Cells

```python
# Check merged cells before writing
def safe_write(ws, cell_ref, value):
    """Write to a cell, handling merged regions."""
    from openpyxl.utils import coordinate_to_tuple

    row, col = coordinate_to_tuple(cell_ref)

    # Check if this cell is in a merged region
    for merged_range in ws.merged_cells.ranges:
        if cell_ref in merged_range:
            # Can only write to the top-left cell of a merged region
            top_left = str(merged_range).split(":")[0]
            if cell_ref != top_left:
                print(f"WARNING: {cell_ref} is in merged range {merged_range}. Writing to {top_left} instead.")
                ws[top_left] = value
                return
    ws[cell_ref] = value
```

---

## Pattern 8: Copying a Sheet Within the Same Workbook

```python
def copy_sheet(wb, source_name, target_name):
    """Copy a sheet within the same workbook."""
    source = wb[source_name]
    target = wb.copy_worksheet(source)
    target.title = target_name
    return target
```

**Limitation:** `copy_worksheet` copies values, formulas, and formatting but does NOT copy:
- Charts
- Images
- Pivot tables
- Print areas (sometimes)

---

## Pattern 9: Find and Replace in Formulas

```python
def find_replace_in_formulas(ws, old_text, new_text, sheet_ref=False):
    """
    Find and replace text within formulas across a sheet.
    Useful when renaming sheets or fixing broken references.

    Args:
        ws: Worksheet
        old_text: Text to find
        new_text: Replacement text
        sheet_ref: If True, only replace within sheet references (e.g., 'OldName'!A1)
    """
    changes = []
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith("="):
                if old_text in cell.value:
                    original = cell.value
                    cell.value = cell.value.replace(old_text, new_text)
                    changes.append(f"{cell.coordinate}: {original} -> {cell.value}")

    return changes
```

---

## Pattern 10: Applying Conditional Number Formatting

```python
def apply_financial_number_format(ws, start_row, end_row, start_col, end_col, format_type="millions"):
    """Apply appropriate number formatting based on the data type."""

    FORMAT_MAP = {
        "millions": '#,##0.0;(#,##0.0)',
        "thousands": '#,##0;(#,##0)',
        "percent": '0.0%',
        "multiple": '0.0x',
        "integer": '#,##0',
        "currency": '$#,##0.0',
    }

    fmt = FORMAT_MAP.get(format_type, '#,##0.0')

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            ws.cell(row=row, column=col).number_format = fmt
```

---

## Anti-Patterns — What NOT to Do

### 1. Don't rebuild the workbook from scratch

```python
# WRONG — destroys all formatting, charts, named ranges, etc.
wb_old = openpyxl.load_workbook("model.xlsx")
wb_new = openpyxl.Workbook()
ws_new = wb_new.active
for row in wb_old.active.iter_rows(values_only=True):
    ws_new.append(row)
wb_new.save("model.xlsx")
```

### 2. Don't iterate and re-apply all formatting

```python
# WRONG — slow, error-prone, and may not capture all style properties
for row in ws.iter_rows():
    for cell in row:
        cell.font = Font(name="Calibri", size=10)  # Overwrites existing formatting
```

### 3. Don't use ws.append() for inserting rows mid-sheet

```python
# WRONG — append() adds to the bottom, does not insert
ws.append(["New Line Item", 100, 200, 300])  # Goes to the end, not where you want it
```

### 4. Don't delete and recreate sheets

```python
# WRONG — loses charts, named ranges, conditional formatting
del wb["Returns"]
ws_new = wb.create_sheet("Returns")
# ... rebuild everything from scratch
```

### 5. Don't open with data_only=True and save

```python
# WRONG — replaces all formulas with their last-cached values (PERMANENTLY)
wb = openpyxl.load_workbook("model.xlsx", data_only=True)
wb.save("model.xlsx")
```
