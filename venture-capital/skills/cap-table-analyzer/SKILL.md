---
name: cap-table-analyzer
description: Professional capitalization table analysis for venture capital. Analyzes equity ownership, liquidation preferences, dilution from new rounds, and exit scenarios. Use when users need to understand ownership stakes, model a new funding round (Pre-Seed to Series E), or calculate exit proceeds for founders and investors.
---

# Cap Table Analyzer

## Overview

This skill provides comprehensive analysis of a company's capitalization table. It helps investors and founders understand the impact of new financing, option pool increases, and liquidation waterfalls.

## Critical Constraints

- **Ownership Accuracy**: Always account for fully diluted shares, including all outstanding options, warrants, and convertible notes.
- **Liquidation Preference**: Correctly model 1x, 2x, or higher non-participating and participating preferences.
- **Dilution Logic**: Ensure the "Option Pool Shuffle" (new options coming out of pre-money valuation) is modeled correctly if requested.
- **Exit Math**: Zero errors in exit proceeds calculations. Total proceeds must equal Exit Value minus Transaction Expenses.

## Workflow

### Step 1: Data Ingestion
- Extract share counts by class (Common, Series Seed, Series A, etc.) from provided documents or user input.
- Identify outstanding convertible notes (SAFE, KISS, traditional notes) and their terms (Cap, Discount).

### Step 2: Ownership Analysis
- Calculate current ownership % for all key stakeholders.
- Visualize the cap table in a clean table format.

### Step 3: Funding Round Modeling
- Model new investment amount, pre-money valuation, and post-money valuation.
- Calculate price per share for the new round.
- Show dilution impact on existing shareholders.

### Step 4: Exit Waterfall
- Model exit scenarios (M&A, IPO).
- Calculate proceeds for each share class based on liquidation preferences and participation rights.
- Identify the "Conversion Point" where preferred shares choose to convert to common for higher proceeds.
