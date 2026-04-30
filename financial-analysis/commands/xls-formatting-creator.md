---
description: Create a reusable XLS formatting skill from one or more representative Excel files
argument-hint: "[path(s) to .xlsx file(s)]"
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# XLS Formatting Creator Command

Create a self-contained XLS formatting skill from user-provided representative Excel files.

## Instructions

1. **Ask for the representative file(s)** if not provided:
   - "Please provide one or more representative Excel files (.xlsx) whose formatting conventions you want to capture. Two or three examples produce a cleaner inference than one."
   - The files should be finished, house-style-compliant workbooks — outputs you'd be happy to send a client.

2. **Load the xls-formatting-creator skill**:
   - Use the `skill: "xls-formatting-creator"` tool to load the full skill instructions.
   - Follow the workflow in the skill to analyze the file(s) and generate a new skill.

3. **Gather additional info**:
   - Company / house-style name (for naming the generated skill).
   - Primary use cases (operating models, LBO outputs, DCF summaries, client-facing schedules, etc.).
   - Any conventions the user knows off the top of their head that might not be obvious from the files (e.g. "we always use green for external links, not cross-sheet").

4. **Execute the skill workflow**:
   - Analyze workbook(s) (theme, fonts, color coding, number formats, borders, column widths, named styles).
   - Report the inferred color-coding rule back to the user and confirm before encoding it.
   - Generate skill directory with `assets/reference.xlsx` and `SKILL.md`.
   - Create a small example output to validate the skill applies formatting correctly.
   - Package the skill.

5. **Deliver the packaged skill** to the user.
