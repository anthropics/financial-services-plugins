---
description: Full IB deal execution — pitch decks, CIMs, teasers, buyer lists, merger models, process letters, deal tracking, plus deck QC, refresh, and spreadsheet tools
argument-hint: "[module, deal context, or 'full deal']"
---

Load the `super-ib` skill for end-to-end investment banking workflows.

If a specific module is mentioned (e.g., "build a pitch deck", "draft a CIM", "write a teaser", "build buyer list", "merger model for X acquiring Y", "draft process letter", "track deals", "build a strip profile", "build datapack", "check this deck", "refresh the numbers", "create PPT template", "audit this spreadsheet", "clean this data"), focus on that module.

If the user says "full deal" or "end to end," run the Deal Context intake first, then proceed through the deal execution pipeline, carrying data forward between modules.

If a deal or company is provided without a specific module, ask which module(s) to run.

If no context is provided, present the available modules and ask where to start.

Always check for deal context before executing any module. If context was gathered in a prior module, reuse it — do not re-ask.

Before creating any file output, read the appropriate document creation skill (pptx, xlsx, docx, or pdf).
