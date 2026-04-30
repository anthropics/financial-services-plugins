---
name: credit-memo-document-generation
description: Compiles all analyzed sections and charts into professional Word (.docx), PDF, and PowerPoint (.pptx) output files. Reads chart PNGs from the visuals skill, embeds them with captions, and generates all three formats. Claude uses this skill as the final step in Credit Memo generation.
---

# Document Generation Skill

## Overview
Generate three output files from the underlying data and analysis:
- **Word (.docx)** — Full detailed memo (25–45 pages), all tables, embedded charts
- **PDF** — Converted from Word; CONFIDENTIAL watermark; locked for editing
- **PowerPoint (.pptx)** — Executive summary deck (15–20 slides), visual-first

---

## WORD DOCUMENT (.docx)

### Setup
```bash
npm install -g docx
```

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
        WidthType, ShadingType, VerticalAlign, PageNumber, PageBreak,
        LevelFormat } = require('docx');
const fs = require('fs');
```

### Document Structure
```
1. Cover Page (Company name, date, loan amount, CONFIDENTIAL marking, disclaimer)
2. Deal Snapshot (key metrics one-pager)
3. Table of Contents
4. Executive Summary
5. Company Overview
6. Financial Analysis
   6.1 Income Statement (+ chart_revenue_ebitda.png, chart_margins.png)
   6.2 Balance Sheet (+ chart_balance_sheet.png)
   6.3 Cash Flow (+ chart_cashflow_waterfall.png)
7. Industry Analysis (+ chart_industry.png, chart_swot.png)
8. Risk Assessment (+ chart_ratios_dashboard.png, chart_credit_ratings.png)
9. Repayment Analysis (+ chart_dscr_stress.png)
10. Management Assessment (+ chart_mgmt_tenure.png)
11. Credit Opinion & AI-Assisted Preliminary Assessment
12. Appendix A: Data Sources & Confidence Levels
13. Appendix B: Data Gap Log (if any MISSING items)
14. Disclaimer Page (full text — required)
```

### Page Setup (US Letter)
```javascript
sections: [{
  properties: {
    page: {
      size: { width: 12240, height: 15840 },
      margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
    }
  },
  headers: {
    default: new Header({
      children: [
        new Table({
          width: { size: 10080, type: WidthType.DXA },
          columnWidths: [5040, 5040],
          borders: { bottom: { style: BorderStyle.SINGLE, size: 1, color: '2E75B6' },
                     top: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE },
                     right: { style: BorderStyle.NONE }, insideH: { style: BorderStyle.NONE },
                     insideV: { style: BorderStyle.NONE } },
          rows: [new TableRow({ children: [
            new TableCell({ children: [new Paragraph({ children: [
              new TextRun({ text: company_name, bold: true, color: '1F3864', size: 18 })
            ]})]}),
            new TableCell({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
              new TextRun({ text: 'CONFIDENTIAL — FOR INTERNAL USE ONLY', color: '808080', size: 14, italics: true })
            ]})]}),
          ]})]
        })
      ]
    })
  },
  footers: {
    default: new Footer({
      children: [
        new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({ text: `Credit Memorandum | ${company_name} | ${date} | Page `, size: 16, color: '808080' }),
          new PageNumber()
        ]}),
        new Paragraph({ alignment: AlignmentType.CENTER, children: [
          new TextRun({
            text: 'AI-generated research aid — not financial advice. Requires review by a qualified credit professional.',
            size: 12, color: 'A0A0A0', italics: true
          })
        ]})
      ]
    })
  }
}]
```

### Embedding Charts
```javascript
function embedChart(chartPath, width = 600, height = 350, caption = '') {
  // Check for placeholder chart first
  const isPlaceholder = chartPath.includes('placeholder') ||
                        !fs.existsSync(chartPath);
  if (isPlaceholder) {
    return [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 100 },
        children: [new TextRun({
          text: `📊 ${caption} — Data not available for this analysis. See Appendix B.`,
          italics: true, size: 18, color: 'A0A0A0'
        })]
      })
    ];
  }
  const imageData = fs.readFileSync(chartPath);
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new ImageRun({
        type: 'png',
        data: imageData,
        transformation: { width, height },
        altText: { title: caption, description: caption, name: caption }
      })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [new TextRun({ text: caption, italics: true, size: 18, color: '808080' })]
    })
  ];
}
```

### Section Header Style
```javascript
function sectionBanner(number, title) {
  return new Table({
    width: { size: 10080, type: WidthType.DXA },
    columnWidths: [10080],
    rows: [new TableRow({ children: [
      new TableCell({
        shading: { fill: '1F3864', type: ShadingType.CLEAR },
        margins: { top: 120, bottom: 120, left: 240, right: 240 },
        children: [new Paragraph({ children: [
          new TextRun({ text: `${number}  ${title.toUpperCase()}`,
                        bold: true, color: 'FFFFFF', size: 28 })
        ]})]
      })
    ]})]
  });
}
```

### Disclaimer Page (Required — must be last page before appendices)
```javascript
function disclaimerPage() {
  return [
    new Paragraph({ pageBreakBefore: true }),
    new Table({
      width: { size: 10080, type: WidthType.DXA },
      rows: [new TableRow({ children: [new TableCell({
        shading: { fill: 'FFF3CD', type: ShadingType.CLEAR },
        margins: { top: 300, bottom: 300, left: 300, right: 300 },
        children: [
          new Paragraph({ children: [new TextRun({
            text: '⚠️  AI-GENERATED RESEARCH AID — NOT FINANCIAL ADVICE',
            bold: true, size: 24, color: '856404'
          })]}),
          new Paragraph({ spacing: { before: 200 }, children: [new TextRun({
            text: 'This Credit Memorandum is generated by an AI assistant and is intended solely as a research and analytical aid for qualified credit professionals. It does NOT constitute financial advice, investment advice, or a credit recommendation of any kind.',
            size: 18, color: '495057'
          })]}),
          new Paragraph({ spacing: { before: 150 }, children: [new TextRun({
            text: 'All outputs must be independently reviewed and validated by a qualified credit professional before use in any lending, investment, or credit decision. The plugin author, Anthropic, and affiliated parties accept no liability for decisions made based on this document.',
            size: 18, color: '495057'
          })]}),
          new Paragraph({ spacing: { before: 150 }, children: [new TextRun({
            text: 'Data sources, confidence levels, and data gaps are documented in Appendices A and B. Where data is estimated or management-provided, this is explicitly noted throughout the document.',
            size: 18, color: '495057'
          })]})
        ]
      })})]
    })
  ];
}
```

---

## PDF GENERATION

### Method: docx2pdf (preferred — highest fidelity)
```bash
pip install docx2pdf --break-system-packages
```

```python
from docx2pdf import convert
import subprocess, sys

docx_path = f'Credit_Memo_{company}_{date}.docx'
pdf_path  = f'Credit_Memo_{company}_{date}.pdf'

try:
    convert(docx_path, pdf_path)
    print(f"PDF generated: {pdf_path}")
except Exception as e:
    # Fallback: LibreOffice headless
    subprocess.run([
        'libreoffice', '--headless', '--convert-to', 'pdf',
        '--outdir', '/tmp/', docx_path
    ], check=True)
    print(f"PDF generated via LibreOffice: {pdf_path}")
```

### Add CONFIDENTIAL Watermark to PDF
```python
pip install PyMuPDF --break-system-packages
```

```python
import fitz  # PyMuPDF

def add_watermark(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        # Diagonal CONFIDENTIAL watermark
        page.insert_text(
            (page.rect.width * 0.15, page.rect.height * 0.55),
            "CONFIDENTIAL",
            fontsize=72,
            color=(0.85, 0.85, 0.85),
            rotate=45,
            overlay=False
        )
    doc.save(output_path)
    doc.close()

add_watermark(pdf_path, pdf_path)
```

---

## POWERPOINT DECK (.pptx)

### Setup
```bash
pip install python-pptx --break-system-packages
```

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import datetime

NAVY  = RGBColor(0x1F, 0x38, 0x64)
BLUE  = RGBColor(0x2E, 0x75, 0xB6)
GOLD  = RGBColor(0xC9, 0xA8, 0x4C)
GREEN = RGBColor(0x70, 0xAD, 0x47)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LGRAY = RGBColor(0xF2, 0xF2, 0xF2)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]  # Blank layout
```

### Slide Structure (15–20 slides)
```
Slide 1:  Title — Company name, loan amount, date, CONFIDENTIAL
Slide 2:  Disclaimer (required — AI-generated research aid)
Slide 3:  Deal Snapshot — Key metrics at a glance
Slide 4:  Company Overview — Business description, revenue mix
Slide 5:  Financial Highlights — Revenue, EBITDA, FCF summary
Slide 6:  Revenue & EBITDA Trend (chart_revenue_ebitda.png)
Slide 7:  Profit Margin Trends (chart_margins.png)
Slide 8:  Balance Sheet Composition (chart_balance_sheet.png)
Slide 9:  Cash Flow Waterfall (chart_cashflow_waterfall.png)
Slide 10: Key Ratio Dashboard (chart_ratios_dashboard.png)
Slide 11: Credit Ratings (chart_credit_ratings.png)
Slide 12: Industry Overview (chart_industry.png)
Slide 13: SWOT Analysis (chart_swot.png)
Slide 14: Repayment & DSCR Stress Test (chart_dscr_stress.png)
Slide 15: Management Team (chart_mgmt_tenure.png)
Slide 16: Risk Summary — Heat map table
Slide 17: AI-Assisted Preliminary Assessment + Conditions
Slide 18: Appendix — Data sources and confidence levels
```

### Title Slide
```python
def add_title_slide(prs, company, loan_amount, date):
    slide = prs.slides.add_slide(blank_layout)
    # Navy background
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = NAVY

    # Company name
    txb = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(1.5))
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = company
    p.font.bold = True
    p.font.size = Pt(44)
    p.font.color.rgb = WHITE

    # Subtitle
    txb2 = slide.shapes.add_textbox(Inches(1), Inches(3.2), Inches(11), Inches(0.8))
    tf2 = txb2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = f"Credit Memorandum  |  Loan Request: {loan_amount}  |  {date}"
    p2.font.size = Pt(20)
    p2.font.color.rgb = GOLD

    # CONFIDENTIAL tag
    txb3 = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(11), Inches(0.5))
    tf3 = txb3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "CONFIDENTIAL — FOR INTERNAL USE ONLY  |  AI-generated research aid — not financial advice"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
    p3.font.italic = True
```

### Chart Slide Helper
```python
def add_chart_slide(prs, title, chart_path, note=''):
    slide = prs.slides.add_slide(blank_layout)
    # Light gray background
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = LGRAY

    # Title bar
    txb = slide.shapes.add_textbox(Inches(0.3), Inches(0.2), Inches(12.7), Inches(0.7))
    tf = txb.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(22)
    p.font.color.rgb = NAVY

    # Chart image (or placeholder)
    import os
    if chart_path and os.path.exists(chart_path):
        slide.shapes.add_picture(chart_path, Inches(0.5), Inches(1.0),
                                  Inches(12.3), Inches(5.8))
    else:
        txb_ph = slide.shapes.add_textbox(Inches(2), Inches(3), Inches(9), Inches(1))
        tf_ph = txb_ph.text_frame
        p_ph = tf_ph.paragraphs[0]
        p_ph.text = f"📊 {title} — Data not available. See Appendix."
        p_ph.font.size = Pt(16)
        p_ph.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
        p_ph.font.italic = True
        p_ph.alignment = PP_ALIGN.CENTER

    # Bottom note
    if note:
        txb_n = slide.shapes.add_textbox(Inches(0.3), Inches(7.0), Inches(12.7), Inches(0.35))
        tf_n = txb_n.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = note
        p_n.font.size = Pt(9)
        p_n.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
        p_n.font.italic = True
```

### Save PowerPoint
```python
pptx_path = f'Credit_Memo_{company}_{date}_Deck.pptx'
prs.save(pptx_path)
print(f"PowerPoint saved: {pptx_path}")
```

---

## Final Output Checklist
Before presenting files to the user, verify:
- [ ] Word file opens without errors
- [ ] All 10 charts embedded in Word (placeholder note if any are missing)
- [ ] Disclaimer page present in Word document
- [ ] PDF generated with CONFIDENTIAL watermark
- [ ] PowerPoint has disclaimer on slide 2 and assessment slide
- [ ] All files named consistently: `Credit_Memo_[Company]_[Date].*`
- [ ] File sizes are reasonable (Word: 2–15MB, PDF: similar, PPT: 5–20MB)
- [ ] Data gap appendix included if any items were marked MISSING

## File Delivery
Present all three files with download links. Guardrails Layer 5 must be invoked before presenting.
