# Formatting Standards Reference

## IB / PE Color Coding Convention

This is the industry-standard color convention used across bulge bracket and elite boutique investment banks. When editing an existing file, first check whether it follows this convention — if it uses a different scheme, match the existing scheme instead.

### Cell Type Colors

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers

# Input cells — values the user can change
INPUT_FONT = Font(name="Calibri", size=10, color="0000FF")  # Blue

# Formula cells — calculated from other cells
FORMULA_FONT = Font(name="Calibri", size=10, color="000000")  # Black

# Cross-sheet links — formulas that reference another sheet
LINK_FONT = Font(name="Calibri", size=10, color="008000")  # Green

# External links — references to other workbooks
EXTERNAL_FONT = Font(name="Calibri", size=10, color="FF0000")  # Red

# Assumption flags — cells flagged for review
FLAG_FILL = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow highlight
```

### Section Headers

```python
SECTION_HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
SECTION_HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
SECTION_HEADER_ALIGNMENT = Alignment(horizontal="left", vertical="center")
```

### Sub-Headers

```python
SUB_HEADER_FONT = Font(name="Calibri", size=10, bold=True, color="1F4E79")
SUB_HEADER_FILL = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
```

### Totals and Subtotals

```python
SUBTOTAL_FONT = Font(name="Calibri", size=10, bold=True, color="000000")
SUBTOTAL_FILL = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
SUBTOTAL_BORDER = Border(top=Side(style="thin"), bottom=Side(style="thin"))

GRAND_TOTAL_FONT = Font(name="Calibri", size=10, bold=True, color="000000")
GRAND_TOTAL_FILL = PatternFill(start_color="B4C6E7", end_color="B4C6E7", fill_type="solid")
GRAND_TOTAL_BORDER = Border(top=Side(style="thin"), bottom=Side(style="double"))
```

---

## Number Formats

### Standard Financial Formats

```python
# Revenue / EBITDA / dollar amounts (in millions)
FORMAT_MILLIONS = '#,##0.0'          # 1,250.3
FORMAT_MILLIONS_NEG = '#,##0.0;(#,##0.0)'  # Negative in parentheses

# Revenue / dollar amounts (in thousands)
FORMAT_THOUSANDS = '#,##0'           # 1,250,300
FORMAT_THOUSANDS_NEG = '#,##0;(#,##0)'

# Percentages
FORMAT_PCT = '0.0%'                  # 12.5%
FORMAT_PCT_PRECISE = '0.00%'         # 12.50%

# Multiples
FORMAT_MULTIPLE = '0.0x'             # 4.5x
FORMAT_MULTIPLE_PRECISE = '0.00x'    # 4.50x

# Years / counts
FORMAT_INTEGER = '#,##0'             # 1,250
FORMAT_YEAR = '0'                    # 2026

# Dates
FORMAT_DATE = 'MM/DD/YYYY'
FORMAT_DATE_SHORT = 'M/D/YY'

# Currency (explicit dollar sign)
FORMAT_CURRENCY = '$#,##0'
FORMAT_CURRENCY_M = '$#,##0.0'       # $1,250.3 (millions)
```

### Applying Number Formats

```python
# Apply format to a cell
ws["D10"].number_format = FORMAT_MILLIONS_NEG

# Apply format to a range
for row in ws.iter_rows(min_row=10, max_row=25, min_col=4, max_col=9):
    for cell in row:
        cell.number_format = FORMAT_MILLIONS_NEG
```

---

## Column Width Standards

```python
# Standard column widths for financial models
COLUMN_WIDTHS = {
    "label": 35,      # Column A — row labels
    "spacer": 2,       # Empty separator columns
    "data": 14,        # Standard data columns (years, quarters)
    "data_wide": 18,   # Wide data columns (with longer numbers)
    "narrow": 8,       # Narrow columns (checkmarks, flags)
}
```

### Applying Column Widths

```python
ws.column_dimensions["A"].width = 35    # Labels
ws.column_dimensions["B"].width = 2     # Spacer
ws.column_dimensions["C"].width = 14    # Year 1
ws.column_dimensions["D"].width = 14    # Year 2
```

---

## Row Height Standards

```python
ROW_HEIGHTS = {
    "header": 25,      # Section headers
    "sub_header": 20,  # Sub-section headers
    "data": 15,        # Standard data rows
    "spacer": 8,       # Empty separator rows
    "total": 18,       # Total / subtotal rows
}
```

---

## Border Patterns

```python
from openpyxl.styles import Border, Side

# Standard borders for financial tables
THIN = Side(style="thin", color="000000")
MEDIUM = Side(style="medium", color="000000")
DOUBLE = Side(style="double", color="000000")
HAIR = Side(style="hair", color="B0B0B0")

# Section separator (above a header)
SECTION_TOP = Border(bottom=MEDIUM)

# Below column headers
HEADER_BOTTOM = Border(bottom=THIN)

# Subtotal row
SUBTOTAL_BORDER = Border(top=THIN, bottom=THIN)

# Grand total row (double bottom line)
TOTAL_BORDER = Border(top=THIN, bottom=DOUBLE)

# Light grid for data cells
DATA_GRID = Border(bottom=HAIR)
```

---

## Detecting Existing Formatting Conventions

Before applying any formatting, detect what the existing file uses. Not every file follows the IB convention.

```python
def detect_formatting_convention(ws, sample_rows=20):
    """Analyze existing formatting to determine the convention in use."""
    convention = {
        "font_name": None,
        "font_size": None,
        "input_color": None,
        "formula_color": None,
        "header_fill": None,
        "uses_ib_convention": False,
    }

    fonts_seen = {}
    fills_seen = {}

    for row in ws.iter_rows(min_row=1, max_row=sample_rows):
        for cell in row:
            if cell.font and cell.font.name:
                fonts_seen[cell.font.name] = fonts_seen.get(cell.font.name, 0) + 1
            if cell.font and cell.font.color and cell.font.color.rgb:
                color = str(cell.font.color.rgb)
                if color.startswith("00"):
                    color = color[2:]  # Strip alpha
                if cell.value and isinstance(cell.value, str) and cell.value.startswith("="):
                    convention["formula_color"] = color
                elif cell.value and isinstance(cell.value, (int, float)):
                    convention["input_color"] = color

    # Most common font
    if fonts_seen:
        convention["font_name"] = max(fonts_seen, key=fonts_seen.get)

    # Check if IB convention (blue inputs, black formulas)
    if convention["input_color"] in ("0000FF", "0070C0"):
        convention["uses_ib_convention"] = True

    return convention
```

**Rule: If the file has an existing convention, match it. Only apply the IB standard to files that already use it or to new sections you are adding to an otherwise unstyled file.**

---

## Sensitivity Table Formatting

Sensitivity tables have specific formatting conventions in financial models:

```python
def format_sensitivity_table(ws, start_row, start_col, rows, cols):
    """Apply standard sensitivity table formatting."""
    # Top-left corner cell (label)
    corner = ws.cell(row=start_row, column=start_col)
    corner.font = Font(bold=True, size=9)
    corner.fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")

    # Column headers (top axis)
    for c in range(start_col + 1, start_col + cols + 1):
        cell = ws.cell(row=start_row, column=c)
        cell.font = Font(bold=True, size=9)
        cell.fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")

    # Row headers (left axis)
    for r in range(start_row + 1, start_row + rows + 1):
        cell = ws.cell(row=r, column=start_col)
        cell.font = Font(bold=True, size=9)
        cell.fill = PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid")

    # Data cells
    for r in range(start_row + 1, start_row + rows + 1):
        for c in range(start_col + 1, start_col + cols + 1):
            cell = ws.cell(row=r, column=c)
            cell.alignment = Alignment(horizontal="center")

    # Center cell (base case) — highlight
    center_r = start_row + 1 + rows // 2
    center_c = start_col + 1 + cols // 2
    base_cell = ws.cell(row=center_r, column=center_c)
    base_cell.fill = PatternFill(start_color="BDD7EE", end_color="BDD7EE", fill_type="solid")
    base_cell.font = Font(bold=True, size=9)
```

---

## Conditional Color Coding for Returns

```python
def color_code_irr(cell, irr_value):
    """Apply traffic-light color coding to IRR cells."""
    if irr_value >= 0.25:
        cell.font = Font(color="006100")  # Dark green
        cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    elif irr_value >= 0.15:
        cell.font = Font(color="9C6500")  # Dark yellow
        cell.fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    else:
        cell.font = Font(color="9C0006")  # Dark red
        cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

def color_code_variance(cell, actual, budget):
    """Apply traffic-light color coding for plan variance."""
    if budget == 0:
        return
    variance = (actual - budget) / abs(budget)
    if variance >= -0.05:
        cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # Green: within 5%
    elif variance >= -0.15:
        cell.fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")  # Yellow: 5-15% below
    else:
        cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")  # Red: >15% below
```

---

## Print Setup

Financial models are frequently printed. Apply these settings when formatting for print:

```python
from openpyxl.worksheet.page import PageMargins

def setup_print(ws, orientation="landscape", fit_to_width=True):
    """Configure print settings for a financial model sheet."""
    ws.page_setup.orientation = orientation
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER

    if fit_to_width:
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0  # 0 = as many pages as needed vertically
        ws.sheet_properties.pageSetUpPr.fitToPage = True

    ws.page_margins = PageMargins(
        left=0.5, right=0.5, top=0.75, bottom=0.75,
        header=0.3, footer=0.3
    )

    # Repeat row 1 (headers) on every printed page
    ws.print_title_rows = "1:1"

    # Print gridlines
    ws.sheet_properties.outlinePr.summaryBelow = False
    ws.print_options.gridLines = False
```
