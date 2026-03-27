# Financial Visualization Standards
Ensures all Python-generated charts follow professional financial formatting.

## Standards
- **Palette**: Primary: #003366 (Navy), Secondary: #808080 (Gray), Accent: #CC0000 (Alert).
- **Rules**: 
  - No vertical gridlines; Y-axis only.
  - Labels must include currency and unit (e.g., "USD in Millions").
  - Always add "Source: [MCP Provider]" watermark.

## Implementation
When generating matplotlib/seaborn code, use these color hex codes and formatting rules by default.
