---
name: credit-memo-visuals
description: Generates all charts, graphs, infographics, and visual assets for the Credit Memo. Creates Python matplotlib/plotly charts as PNG images that get embedded into Word, PDF, and PowerPoint outputs. Claude draws on this skill automatically when financial data has been collected and analysis is ready to be visualized.
---

# Credit Memo — Visuals Skill

## Overview
Numbers without visuals don't communicate well in credit presentations. This skill defines every chart to generate, the data it needs, the chart type, and exact styling. All charts are produced as high-resolution PNG files, then embedded into Word/PDF/PPT outputs by the document-generation skill.

---

## Chart Generation Setup

```bash
pip install matplotlib plotly kaleido pandas numpy --break-system-packages
```

### Standard Chart Template:
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Brand colors
NAVY    = '#1F3864'
BLUE    = '#2E75B6'
GOLD    = '#C9A84C'
GREEN   = '#70AD47'
AMBER   = '#ED7D31'
RED     = '#C00000'
LGRAY   = '#F2F2F2'
DGRAY   = '#404040'

fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(colors=DGRAY)
plt.tight_layout()
plt.savefig('chart_name.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
```

---

## Placeholder Chart Protocol

**When data is unavailable for any chart**, generate a clearly marked placeholder PNG instead of skipping the file. This ensures the document-generation skill always finds a file by the expected name, and readers can clearly see that data is missing — rather than seeing a confusing broken image or blank space.

```python
def generate_placeholder(filename, chart_title, reason='Data not available for this analysis'):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Dashed border
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_linestyle('--')
        ax.spines[spine].set_color('#AAAAAA')

    # Icon and message
    ax.text(0.5, 0.65, '📊', fontsize=48, ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.45, chart_title, fontsize=14, fontweight='bold',
            ha='center', va='center', color='#555555', transform=ax.transAxes)
    ax.text(0.5, 0.30, reason, fontsize=11, ha='center', va='center',
            color='#888888', style='italic', transform=ax.transAxes)
    ax.text(0.5, 0.15, 'See Appendix B — Data Gap Log for details.',
            fontsize=10, ha='center', va='center', color='#AAAAAA', transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close()
    print(f"[PLACEHOLDER] Generated: {filename}")
```

Call this function whenever the required data for a chart is `❌ MISSING` or confidence is too low to render meaningful values.

---

## Required Charts — All 10

### CHART 1: Revenue & EBITDA Trend (5-Year)
**File:** `chart_revenue_ebitda.png`
**Type:** Grouped bar (Revenue) + Line overlay (EBITDA Margin %)
**Data:** Annual Revenue ($M) and EBITDA Margin (%) for 5 years

```python
fig, ax1 = plt.subplots(figsize=(10, 5), dpi=150)
ax2 = ax1.twinx()

years = ['FY2019', 'FY2020', 'FY2021', 'FY2022', 'FY2023']
revenue = [/* from data */]
ebitda_margin = [/* from data */]

bars = ax1.bar(years, revenue, color=BLUE, alpha=0.85, width=0.5, label='Revenue ($M)')
ax1.bar_label(bars, fmt='$%.0fM', padding=3, fontsize=9, color=DGRAY)
ax1.set_ylabel('Revenue ($M)', color=NAVY, fontweight='bold')
ax1.set_ylim(0, max(revenue) * 1.2)

line = ax2.plot(years, ebitda_margin, color=GOLD, marker='o',
                linewidth=2.5, markersize=8, label='EBITDA Margin %')
for i, v in enumerate(ebitda_margin):
    ax2.annotate(f'{v:.1f}%', (years[i], v), textcoords='offset points',
                 xytext=(0, 10), ha='center', fontsize=9, color=GOLD)
ax2.set_ylabel('EBITDA Margin (%)', color=GOLD, fontweight='bold')
ax2.set_ylim(0, max(ebitda_margin) * 2)

ax1.set_title(f'{company} — Revenue & EBITDA Margin (5-Year)',
              fontsize=13, fontweight='bold', color=NAVY, pad=15)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
```

---

### CHART 2: Profit Margins Trend
**File:** `chart_margins.png`
**Type:** Multi-line chart
**Data:** Gross Margin %, Operating Margin %, Net Margin % for 5 years

```python
fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
ax.plot(years, gross_margins, color=GREEN, marker='s', lw=2.5, ms=8, label='Gross Margin')
ax.plot(years, op_margins, color=BLUE, marker='o', lw=2.5, ms=8, label='Operating Margin')
ax.plot(years, net_margins, color=GOLD, marker='^', lw=2.5, ms=8, label='Net Margin')
# Industry average reference line (if available)
if industry_avg_net_margin:
    ax.axhline(y=industry_avg_net_margin, color=RED, linestyle='--', lw=1.5,
               label=f'Industry Avg Net Margin ({industry_avg_net_margin:.1f}%)')
ax.fill_between(years, net_margins, alpha=0.1, color=GOLD)
ax.set_ylabel('Margin (%)', fontweight='bold', color=NAVY)
ax.set_title(f'{company} — Profit Margin Trends vs. Industry',
             fontsize=13, fontweight='bold', color=NAVY, pad=15)
ax.legend(framealpha=0.9)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
```

---

### CHART 3: Cash Flow Waterfall
**File:** `chart_cashflow_waterfall.png`
**Type:** Horizontal waterfall chart
**Data:** OCF, CapEx, FCF, Financing Activities, Net Change (latest year)

```python
categories = ['Operating\nCash Flow', 'Capital\nExpenditure', 'Free Cash\nFlow',
              'Financing\nActivities', 'Net Cash\nChange']
values = [ocf, -capex, fcf, financing, net_change]
colors = [GREEN if v >= 0 else RED for v in values]
colors[2] = BLUE  # FCF always in blue

bars = ax.barh(categories, values, color=colors, height=0.5, edgecolor='white', lw=0.5)
ax.axvline(x=0, color=DGRAY, lw=1)
for bar, val in zip(bars, values):
    label = f'${abs(val):.0f}M'
    xpos = val + (max(abs(v) for v in values) * 0.02) if val >= 0 else val - (max(abs(v) for v in values) * 0.02)
    ha = 'left' if val >= 0 else 'right'
    ax.text(xpos, bar.get_y() + bar.get_height()/2, label,
            va='center', ha=ha, fontsize=10, fontweight='bold', color=DGRAY)
ax.set_title(f'{company} — Cash Flow Waterfall ({latest_year})',
             fontsize=13, fontweight='bold', color=NAVY, pad=15)
```

---

### CHART 4: Balance Sheet Composition
**File:** `chart_balance_sheet.png`
**Type:** Side-by-side stacked bar — Assets AND Liabilities/Equity

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=150)

# Assets side
ax1.bar(years_3, current_assets, color='#AED6F1', label='Current Assets')
ax1.bar(years_3, noncurrent_assets, bottom=current_assets, color=BLUE, label='Non-Current Assets')
ax1.set_title('Asset Composition', fontweight='bold', color=NAVY)
ax1.legend(loc='upper left', fontsize=9)

# Liabilities + Equity side
ax2.bar(years_3, current_liab, color='#F1948A', label='Current Liabilities')
ax2.bar(years_3, lt_debt, bottom=current_liab, color=RED, label='Long-Term Debt')
bottom2 = [c + l for c, l in zip(current_liab, lt_debt)]
ax2.bar(years_3, equity, bottom=bottom2, color=GREEN, label="Shareholders' Equity")
ax2.set_title("Liabilities & Equity Composition", fontweight='bold', color=NAVY)
ax2.legend(loc='upper left', fontsize=9)

fig.suptitle(f'{company} — Balance Sheet Composition (3-Year)',
             fontsize=13, fontweight='bold', color=NAVY)
```

---

### CHART 5: Key Financial Ratios Dashboard (Traffic Light)
**File:** `chart_ratios_dashboard.png`
**Type:** Horizontal bar chart with color-coded thresholds
**Data:** Current Ratio, Quick Ratio, Debt/Equity, Net Debt/EBITDA, Interest Coverage, DSCR

```python
# Note: thresholds below are defaults — use sector-specific values from financial-analysis skill
ratios = {
    'Current Ratio':     {'value': cr,   'good': 2.0, 'warn': 1.0, 'fmt': '{:.2f}x', 'higher_better': True},
    'Quick Ratio':       {'value': qr,   'good': 1.0, 'warn': 0.5, 'fmt': '{:.2f}x', 'higher_better': True},
    'Debt / Equity':     {'value': de,   'good': 1.0, 'warn': 2.0, 'fmt': '{:.2f}x', 'higher_better': False},
    'Net Debt / EBITDA': {'value': nde,  'good': 2.0, 'warn': 3.5, 'fmt': '{:.2f}x', 'higher_better': False},
    'Interest Coverage': {'value': ic,   'good': 5.0, 'warn': 2.0, 'fmt': '{:.1f}x', 'higher_better': True},
    'DSCR':              {'value': dscr, 'good': 1.5, 'warn': 1.1, 'fmt': '{:.2f}x', 'higher_better': True},
}

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
labels, values, colors_bar = [], [], []
for name, r in ratios.items():
    labels.append(name)
    values.append(r['value'])
    if r['higher_better']:
        c = GREEN if r['value'] >= r['good'] else (AMBER if r['value'] >= r['warn'] else RED)
    else:
        c = GREEN if r['value'] <= r['good'] else (AMBER if r['value'] <= r['warn'] else RED)
    colors_bar.append(c)

bars = ax.barh(labels, values, color=colors_bar, height=0.55, edgecolor='white')
for bar, r in zip(bars, ratios.values()):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
            r['fmt'].format(r['value']), va='center', fontsize=11, fontweight='bold')

legend_patches = [
    mpatches.Patch(color=GREEN, label='Strong ✅'),
    mpatches.Patch(color=AMBER, label='Watch 🟡'),
    mpatches.Patch(color=RED,   label='Risk ❌')
]
ax.legend(handles=legend_patches, loc='lower right')
ax.set_title(f'{company} — Key Ratio Dashboard', fontsize=13, fontweight='bold', color=NAVY, pad=15)
ax.set_xlabel('Ratio Value', color=NAVY)
```

---

### CHART 6: Credit Rating Scale Visual
**File:** `chart_credit_ratings.png`
**Type:** Custom horizontal rating scale with agency markers
**Data:** Moody's, S&P, Fitch ratings + internal rating if available

```python
scale = ['AAA','AA+','AA','AA-','A+','A','A-','BBB+','BBB','BBB-',
         'BB+','BB','BB-','B+','B','B-','CCC','CC','C','D']

# Color zones: investment grade (green shades) vs speculative (amber/red)
zone_colors = []
for i in range(len(scale)):
    if i < 3:   zone_colors.append('#1a7741')   # AAA–AA: dark green
    elif i < 6: zone_colors.append('#70AD47')   # A: green
    elif i < 10: zone_colors.append('#A9D18E')  # BBB: light green
    elif i < 13: zone_colors.append('#ED7D31')  # BB: amber
    else:        zone_colors.append('#C00000')  # B and below: red

fig, ax = plt.subplots(figsize=(12, 3), dpi=150)
for i, (rating, color) in enumerate(zip(scale, zone_colors)):
    ax.bar(i, 1, color=color, edgecolor='white', width=0.9)
    ax.text(i, 0.5, rating, ha='center', va='center', fontsize=8,
            fontweight='bold', color='white')

# Investment grade dividing line
ax.axvline(x=9.5, color='black', lw=2, linestyle='--')
ax.text(4.5, 1.08, 'INVESTMENT GRADE', ha='center', fontsize=10,
        fontweight='bold', color='#1a7741', transform=ax.transAxes)
ax.text(0.78, 1.08, 'SPECULATIVE', ha='center', fontsize=10,
        fontweight='bold', color='#C00000', transform=ax.transAxes)

# Mark each agency's rating with a pin
for agency, rating_str, marker, color in [
    ('Moody\'s', moodys_rating, 'v', NAVY),
    ('S&P', sp_rating, '^', BLUE),
    ('Fitch', fitch_rating, 's', GOLD),
]:
    if rating_str in scale:
        idx = scale.index(rating_str)
        ax.plot(idx, 1.3, marker=marker, ms=12, color=color, label=f'{agency}: {rating_str}')

ax.set_xlim(-0.5, len(scale) - 0.5)
ax.set_ylim(0, 1.8)
ax.axis('off')
ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax.set_title(f'{company} — Credit Rating Position', fontsize=13, fontweight='bold',
             color=NAVY, pad=20)
```

---

### CHART 7: Industry Market Size & Growth
**File:** `chart_industry.png`
**Type:** Grouped bar (market size, USD bn) + Line (growth rate %)
**Data:** Market size last 5 years + CAGR projection

```python
fig, ax1 = plt.subplots(figsize=(10, 5), dpi=150)
ax2 = ax1.twinx()
bars = ax1.bar(years, market_size, color=BLUE, alpha=0.8, width=0.5, label='Market Size ($bn)')
ax1.bar_label(bars, fmt='$%.0fbn', padding=3, fontsize=9, color=DGRAY)
ax1.set_ylabel('Market Size (USD bn)', color=NAVY, fontweight='bold')
ax2.plot(years, growth_rate, color=GOLD, marker='o', lw=2.5, ms=8, label='YoY Growth %')
ax2.set_ylabel('Growth Rate (%)', color=GOLD, fontweight='bold')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
ax1.set_title(f'{industry} — Market Size & Growth', fontsize=13, fontweight='bold', color=NAVY, pad=15)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)
```

---

### CHART 8: SWOT Matrix
**File:** `chart_swot.png`
**Type:** 2×2 colored quadrant diagram

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8), dpi=150)
configs = [
    ('STRENGTHS',     strengths,     '#D5E8D4', '#82B366', 0, 0),
    ('WEAKNESSES',    weaknesses,    '#FFE6CC', '#D6B656', 0, 1),
    ('OPPORTUNITIES', opportunities, '#DAE8FC', '#6C8EBF', 1, 0),
    ('THREATS',       threats,       '#F8CECC', '#B85450', 1, 1),
]
for title, items, bg, border, r, c in configs:
    ax = axes[r][c]
    ax.set_facecolor(bg)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor(border); spine.set_linewidth(2)
    ax.text(0.5, 0.92, title, transform=ax.transAxes, fontsize=13,
            fontweight='bold', ha='center', color=border)
    for i, item in enumerate(items[:4]):
        ax.text(0.08, 0.75 - i * 0.18, f'• {item}', transform=ax.transAxes,
                fontsize=10, va='top', wrap=True)
fig.suptitle('Industry SWOT Analysis', fontsize=16, fontweight='bold', color=NAVY)
plt.tight_layout(rect=[0, 0, 1, 0.95])
```

---

### CHART 9: DSCR Stress Test
**File:** `chart_dscr_stress.png`
**Type:** Grouped bar chart (Base, Downside, Severe)
**Data:** DSCR under 3 scenarios

```python
scenarios = ['Base Case\n(Revenue flat)', 'Downside\n(-15% Revenue)', 'Severe Stress\n(-30% Revenue)']
dscr_values = [base_dscr, downside_dscr, severe_dscr]
threshold = 1.25
colors_s = [GREEN if v >= threshold else (AMBER if v >= 1.0 else RED) for v in dscr_values]

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
bars = ax.bar(scenarios, dscr_values, color=colors_s, width=0.4, edgecolor='white')
ax.axhline(y=threshold, color=RED, linestyle='--', lw=2, label=f'Min. DSCR Threshold ({threshold}x)')
ax.axhline(y=1.0, color=AMBER, linestyle=':', lw=1.5, label='Break-even (1.0x)')
ax.bar_label(bars, fmt='{:.2f}x', padding=4, fontsize=11, fontweight='bold')
ax.set_ylabel('Debt Service Coverage Ratio', fontweight='bold', color=NAVY)
ax.set_title(f'{company} — DSCR Stress Test Scenarios', fontsize=13, fontweight='bold',
             color=NAVY, pad=15)
ax.legend()
```

---

### CHART 10: Management Tenure Timeline
**File:** `chart_mgmt_tenure.png`
**Type:** Horizontal Gantt-style bar chart
**Data:** Each C-suite exec — join year, current year, role

```python
fig, ax = plt.subplots(figsize=(10, max(4, len(executives) * 0.7)), dpi=150)
current_year = 2024

for i, exec in enumerate(executives):
    tenure = current_year - exec['join_year']
    color = GREEN if tenure >= 5 else (AMBER if tenure >= 2 else RED)
    ax.barh(i, tenure, left=exec['join_year'], color=color, height=0.5,
            edgecolor='white', alpha=0.85)
    ax.text(exec['join_year'] + tenure + 0.1, i,
            f"{exec['name']} — {exec['title']} ({tenure}y)",
            va='center', fontsize=9, color=DGRAY)

ax.set_yticks(range(len(executives)))
ax.set_yticklabels([e['title'] for e in executives], fontsize=9)
ax.set_xlabel('Year', color=NAVY, fontweight='bold')
ax.set_title(f'{company} — C-Suite Tenure', fontsize=13, fontweight='bold',
             color=NAVY, pad=15)
legend_patches = [
    mpatches.Patch(color=GREEN, label='>5 years — Stable'),
    mpatches.Patch(color=AMBER, label='2–5 years — Watch'),
    mpatches.Patch(color=RED,   label='<2 years — New')
]
ax.legend(handles=legend_patches, loc='lower right')
ax.invert_yaxis()
```

---

## Chart Output Protocol
1. Generate all charts as PNG at 150 DPI minimum
2. Save to temp folder: `/tmp/credit_memo_charts/`
3. Name exactly as specified (document-generation skill reads them by name)
4. After generation, verify all 10 chart files exist
5. **If any chart fails due to missing data → call `generate_placeholder()` with the chart filename and reason**
6. Log all placeholders: add them to the data gap log (Appendix B)

## Chart Quality Checklist
Before embedding, verify each chart:
- [ ] No overlapping labels
- [ ] All axes labeled with units
- [ ] Legend present and readable
- [ ] Title includes company name and metric
- [ ] Source line at bottom if data source is known
- [ ] White or light-gray background (no transparency)
- [ ] Minimum 150 DPI
- [ ] Placeholder charts clearly distinguishable from real data charts
