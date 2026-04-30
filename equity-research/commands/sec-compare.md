# /sec-compare [ticker] [period1] [period2]
Compare specific sections of two SEC filings to identify narrative shifts.

## Arguments
- `ticker`: Stock symbol (e.g., AAPL)
- `period1`: Base filing (e.g., 2024-10K)
- `period2`: Target filing (e.g., 2025-Q1)

## Instructions
1. Use the **SEC EDGAR MCP** to fetch both filings.
2. Isolate the "Management's Discussion and Analysis" (MD&A) sections.
3. Perform a semantic diff to highlight:
   - New risks added.
   - Deletions of previous guidance.
   - Changes in specific numerical targets (e.g., CAPEX guidance).
4. Summarize "The Delta" in 3 bullet points.
