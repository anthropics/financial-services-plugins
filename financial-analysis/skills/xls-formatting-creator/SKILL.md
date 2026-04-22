---
name: xls-formatting-creator
description: Creates self-contained XLS formatting SKILLS (not workbooks) from user-provided representative Excel files. Use ONLY when a user wants to create a reusable skill that encodes their spreadsheet formatting conventions (fonts, colors, borders, number formats, color coding). For creating or editing actual workbooks, use the xlsx / clean-data-xls / audit-xls skills instead.
---

# XLS Formatting Creator

**This skill creates SKILLS, not workbooks.** Use this when a user wants to turn one or more representative Excel files into a reusable skill that enforces their formatting conventions on future models. If the user just wants to build or edit a workbook, use `xlsx`, `clean-data-xls`, or `audit-xls`.

Unlike PowerPoint, Excel has no slide layouts or placeholders — formatting conventions are *inferred patterns* distributed across cells. The meta-skill's job is to extract those patterns and encode them in the generated skill.

The generated skill includes:
- `assets/reference.xlsx` — the representative workbook (or one of them, if multiple)
- `SKILL.md` — complete formatting conventions + code to apply them (self-contained, no external references)

**For general skill-building best practices**, refer to the `skill-creator` skill. This skill focuses on XLS-specific patterns.

## Workflow

1. **User provides one or more representative Excel files** (.xlsx). Multiple examples yield a better pattern inference — ask for at least one, ideally two or three.
2. **Analyze the file(s)** — extract theme, fonts, fills, borders, number formats, column widths, color coding.
3. **Initialize the skill** — use `skill-creator` to set up the directory.
4. **Bundle a reference workbook** — copy the cleanest example to `assets/reference.xlsx`.
5. **Write SKILL.md** — follow the template below with the extracted patterns.
6. **Create an example output** — generate a tiny sample workbook to validate the skill applies formatting correctly.
7. **Package** — use `skill-creator` to package into a `.skill` file.

## Step 2: Analyze the Workbook(s)

**CRITICAL:** Excel formatting patterns are inferred, not declared. You are reverse-engineering the house style.

Use `openpyxl` (preferred for introspection; `xlsx` package retains theme + style tables):

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from collections import Counter

wb = load_workbook(path, data_only=False)

for ws in wb.worksheets:
    print(f"\n=== Sheet: {ws.title} ({ws.max_row} rows x {ws.max_column} cols) ===")

    # Column widths
    widths = {get_column_letter(i): ws.column_dimensions[get_column_letter(i)].width
              for i in range(1, ws.max_column + 1)}
    print("Column widths:", widths)

    # Profile cell formatting
    fonts = Counter()
    fills = Counter()
    num_formats = Counter()
    borders = Counter()
    font_color_by_type = {
        "numeric_input": Counter(),  # hardcoded number — this is what "input color" refers to
        "text_label":    Counter(),  # text constant (labels, headers)
        "formula":       Counter(),
        "intra_link":    Counter(),  # cross-sheet, same workbook (has !)
        "external_link": Counter(),  # external workbook (has [)
    }

    def side_style(s): return s.style if s is not None else None

    def classify(cell):
        v = cell.value
        if isinstance(v, str) and v.startswith("="):
            if "[" in v: return "external_link"
            if "!" in v: return "intra_link"
            return "formula"
        if isinstance(v, (int, float)): return "numeric_input"
        return "text_label"

    for row in ws.iter_rows():
        for cell in row:
            if cell.value is None:
                continue
            f = cell.font
            fonts[(f.name, f.size, f.bold, f.italic, str(f.color.rgb) if f.color else None)] += 1
            if cell.fill.fill_type == "solid":
                fills[str(cell.fill.fgColor.rgb)] += 1
            if cell.number_format and cell.number_format != "General":
                num_formats[cell.number_format] += 1
            b = cell.border
            borders[(side_style(b.top), side_style(b.bottom), side_style(b.left), side_style(b.right))] += 1

            color = str(f.color.rgb) if f.color else None
            font_color_by_type[classify(cell)][color] += 1

    print("Top fonts:", fonts.most_common(5))
    print("Top fills:", fills.most_common(5))
    print("Top number formats (excluding General):", num_formats.most_common(10))
    print("Top border combos:", borders.most_common(5))
    print("Color-coding by cell type:")
    for k, v in font_color_by_type.items():
        print(f"  {k}: {v.most_common(3)}")

# Named styles (openpyxl exposes these as a list of strings)
print("\nNamed styles:", list(wb.named_styles))

# Theme colors (resolved from theme XML)
import re
from openpyxl.xml.functions import fromstring
theme_xml = wb.loaded_theme
if theme_xml:
    root = fromstring(theme_xml)
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    scheme = root.find(".//a:clrScheme", ns)
    print("Theme colors:")
    for child in scheme:
        tag = child.tag.split("}")[-1]
        srgb = child.find(".//a:srgbClr", ns)
        sys = child.find(".//a:sysClr", ns)
        color = srgb.get("val") if srgb is not None else (sys.get("lastClr") if sys is not None else None)
        print(f"  {tag}: #{color}")
```

### What to extract and document

| Dimension | What to capture |
|---|---|
| **Theme** | The 12 theme colors (2 backgrounds, 2 texts, 6 accents, 2 hyperlinks) + theme font names |
| **Fonts** | (family, size, bold, italic, color) per role: section-header, subheader, body, total, footer |
| **Color coding** | The inferred mapping — e.g. blue (`#0000FF`) = hardcoded input, black (`#000000`) = formula, green (`#008000`) = link/cross-sheet reference |
| **Number formats** | Currency (`"$#,##0"`, `"$#,##0;(#,##0)"`), percent (`"0.0%"`), multiple (`"0.0x"`), date (`"mmm-yy"`), multiples/thousands toggle |
| **Fills** | Header fill colors, alternating row fills, highlight colors for assumptions |
| **Borders** | Top/bottom line weights for section breaks, totals (single-top, double-bottom is the classic "total" border) |
| **Column widths** | Label column (wide), data columns (narrow, often equal), spacer columns |
| **Named styles** | Any `Input`, `Calculation`, `Heading`, `Total` styles already defined in the workbook |
| **Layout conventions** | Title row position, sub-title rows, units row (`($ in millions)`), period header row, first data row, section spacing |

### Inferring color-coding conventions

This is the highest-value and most non-obvious extraction. The classic banker convention is:

- **Blue font** = hardcoded input (a number the user typed)
- **Black font** = formula operating within the sheet
- **Green font** = link to another sheet (intra-workbook)
- **Red font** = link to another workbook (external reference)

The user's house style may differ — you must infer it. The classification heuristic used above splits on formula text:

- `constant` — cell value is not a formula
- `formula` — formula with no `!` and no `[` (purely in-sheet math)
- `intra_link` — formula contains `!` but no `[` (cross-sheet reference like `=Assumptions!B10`)
- `external_link` — formula contains `[` (external-workbook reference like `=[Other.xlsx]Sheet!A1`)

A mixed formula like `=A1+Assumptions!B5` gets bucketed as `intra_link` because the heuristic prioritizes the strongest lineage signal. Report the resulting mapping back to the user before encoding it in the generated skill — if their convention differs (e.g., they use red for intra-workbook), they'll catch it here.

### Inferring section-header / subheader / total conventions

Sort unique font tuples by (bold desc, size desc). Typical patterns:

- Section header: bold, 12pt, often with a fill
- Subheader: bold, 11pt, no fill
- Body: regular, 10–11pt
- Total: bold, top border (thin), bottom border (double)
- Footer/source: italic, 8–9pt, muted gray

## Step 5: Write SKILL.md

Generated skill structure:
```
[company]-xls-formatting/
├── SKILL.md
└── assets/
    └── reference.xlsx
```

### Generated SKILL.md Template

The generated SKILL.md must be **self-contained** with all conventions and code embedded. Fill in bracketed values from your analysis.

````markdown
---
name: [company]-xls-formatting
description: [Company] Excel formatting conventions. Use when building or styling [Company]-branded financial models, output schedules, or client-facing spreadsheets. Applies house fonts, colors, number formats, color-coding rules, and border conventions.
---

# [Company] XLS Formatting

Reference workbook: `assets/reference.xlsx` — open this to eyeball the intended look when in doubt.

## Environment

- **Inside Excel (Office Add-in / Office JS):** use `Excel.run` with `range.format.*` APIs.
- **Standalone .xlsx file:** use `openpyxl` with `Font`, `PatternFill`, `Border`, `Side`, `Alignment`, and `numFormat` objects.

## Theme

| Role | Color |
|---|---|
| Background 1 | `#[HEX]` |
| Background 2 | `#[HEX]` |
| Text 1 | `#[HEX]` |
| Text 2 | `#[HEX]` |
| Accent 1 | `#[HEX]` |
| Accent 2 | `#[HEX]` |
| Hyperlink | `#[HEX]` |

Theme fonts: heading = `[FONT]`, body = `[FONT]`.

## Color-Coding Convention

**Every cell's font color encodes its data lineage.** This is the most important rule.

| Font color | Hex | Meaning |
|---|---|---|
| [Color name] | `#[HEX]` | Hardcoded input (a number someone typed) |
| [Color name] | `#[HEX]` | In-sheet formula |
| [Color name] | `#[HEX]` | Link to another sheet in the same workbook |
| [Color name] | `#[HEX]` | External link (different workbook) |

Never apply a color that contradicts the lineage — a hardcoded input in black looks like a formula and will silently mislead reviewers.

## Fonts

| Role | Font | Size | Weight | Style | Color |
|---|---|---|---|---|---|
| Section header | [FONT] | [pt] | Bold | — | `#[HEX]` |
| Subheader | [FONT] | [pt] | Bold | — | `#[HEX]` |
| Body | [FONT] | [pt] | Regular | — | per color-coding rule |
| Total | [FONT] | [pt] | Bold | — | per color-coding rule |
| Footer/source | [FONT] | [pt] | Regular | Italic | `#[HEX]` |

## Number Formats

| Data kind | Format string |
|---|---|
| Currency, whole | `[$#,##0;(#,##0)]` |
| Currency, 1dp | `[$#,##0.0;($#,##0.0)]` |
| Percent, 1dp | `[0.0%;(0.0%)]` |
| Multiple | `[0.0"x"]` |
| Basis points | `[0" bps"]` |
| Date (month) | `[mmm-yy]` |
| Date (full) | `[m/d/yyyy]` |
| Count / shares | `[#,##0;(#,##0)]` |
| Zero display | `[#,##0;(#,##0);"—"]` (em-dash for zero) |

## Fills

| Role | Color |
|---|---|
| Section header fill | `#[HEX]` |
| Assumption highlight | `#[HEX]` |
| Alternating row (light) | `#[HEX]` |

## Borders

| Role | Top | Bottom | Left | Right |
|---|---|---|---|---|
| Section divider | thin | — | — | — |
| Subtotal row | thin | — | — | — |
| Total row | thin | double | — | — |
| Data block outline | thin | thin | thin | thin |

## Column Widths

| Column | Width |
|---|---|
| Label column (A) | [N] |
| Data columns (B–?) | [N] |
| Spacer column | [N] |

## Layout Conventions

- Row 1: Title (sheet name, e.g. "DCF Summary")
- Row 2: Sub-title (e.g. company name + period)
- Row 3: Units row (e.g. `$ in millions, except per share data`)
- Row [N]: Period headers (FY24A, FY25E, …)
- Row [N+1]: First data row
- Freeze pane below period-header row and right of label column

## Applying Formatting — openpyxl

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, NamedStyle

# House constants (from extraction)
BLUE_INPUT    = "[HEX]"
BLACK_FORMULA = "[HEX]"
GREEN_LINK    = "[HEX]"
HEADER_FILL   = "[HEX]"
ACCENT_1      = "[HEX]"
BODY_FONT     = "[FONT]"

def input_font(size=11):
    return Font(name=BODY_FONT, size=size, color=BLUE_INPUT)

def formula_font(size=11, bold=False):
    return Font(name=BODY_FONT, size=size, bold=bold, color=BLACK_FORMULA)

def header_style():
    return NamedStyle(
        name="SectionHeader",
        font=Font(name=BODY_FONT, size=12, bold=True, color="FFFFFF"),
        fill=PatternFill("solid", fgColor=HEADER_FILL),
        alignment=Alignment(horizontal="left", vertical="center"),
    )

def total_border():
    thin = Side(style="thin", color="000000")
    double = Side(style="double", color="000000")
    return Border(top=thin, bottom=double)

CURRENCY_WHOLE = '_($* #,##0_);_($* (#,##0);_($* "-"_);_(@_)'
PERCENT_1DP    = '0.0%;(0.0%)'
MULTIPLE       = '0.0"x"'
```

## Applying Formatting — Office JS

```javascript
await Excel.run(async (context) => {
  const sheet = context.workbook.worksheets.getActiveWorksheet();

  // Section header
  const header = sheet.getRange("A1:F1");
  header.format.font.name = "[FONT]";
  header.format.font.size = 12;
  header.format.font.bold = true;
  header.format.font.color = "#FFFFFF";
  header.format.fill.color = "#[HEADER_FILL]";

  // Input cell (blue font, house convention)
  sheet.getRange("B5").format.font.color = "#[BLUE_INPUT]";
  sheet.getRange("B5").numberFormat = [["$#,##0;($#,##0)"]];

  // Total row (thin top, double bottom)
  const total = sheet.getRange("A20:F20");
  total.format.font.bold = true;
  total.format.borders.getItem("EdgeTop").style = "Continuous";
  total.format.borders.getItem("EdgeBottom").style = "Double";

  await context.sync();
});
```

## Quick Recipes

### Style a hardcoded assumption cell
- Font: body family, size [N], color `[BLUE_INPUT]`
- Fill: none (or assumption highlight if part of an inputs block)
- Number format: appropriate to the unit

### Style a total row
- Font: bold, color per lineage rule
- Border: thin top, double bottom
- Blank row above for visual spacing

### Style a section header
- Font: bold, size [N], color [HEX]
- Fill: `[HEADER_FILL]`
- Merge across the data block if the house pattern does this

## Rules

1. **Never override the color-coding rule** — font color encodes lineage. Apply it last if other formatting has overwritten it.
2. **Use named styles where possible** — `Input`, `Calculation`, `Total`, `Heading 1` — they propagate changes cleanly.
3. **Don't hardcode values with a formula color** — a pasted-over formula looks fine but breaks audits. If unsure, check `cell.value` / `cell.data_type`.
4. **Anchor to the reference workbook** — when ambiguous, open `assets/reference.xlsx` and match what you see.
````

## Step 6: Create an Example Output

Produce a tiny sample — e.g. a 10-row mini-schedule with inputs (blue), formulas (black), a total row, and one external link (green). Save it next to the skill for validation. This is the skill's smoke test.

## XLS-Specific Rules for Generated Skills

1. **Reference workbook in `assets/`** — always bundle at least one real example.
2. **Self-contained SKILL.md** — embed all hex codes, font names, number format strings. No "see the reference" in place of the actual rule.
3. **Document color coding first** — it's the single most load-bearing convention and easiest to silently violate.
4. **Cover both environments** — Office JS and openpyxl. Models get built in both.
5. **Give applied examples, not just rules** — the Quick Recipes section is where the skill earns its keep.
