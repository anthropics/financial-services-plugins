# Company Research Feishu Delivery Specification

This document defines how the company research agent should return results to Feishu in V1.

The goal is a reliable first experience, not a feature-complete messaging workflow.

## V1 Delivery Principle

Keep delivery simple:

- short summary in the Feishu message
- full report written to a Feishu Doc first
- local markdown kept only as an internal artifact
- optional docx later

Do not block launch on rich cards or complex approval interaction.

## Hard Requirement

For any successful full-report delivery:

- the agent must create a Feishu Doc
- the agent must write the report body into that doc
- the agent must read or otherwise confirm the resulting doc token or URL
- the final reply must include the Feishu Doc URL
- the body must be verified to exist; a title-only doc does not count

A local file path alone does not count as successful user delivery.

## V1 Response Types

### Type 1: Full report success

Return:

- a concise summary message
- the Feishu Doc URL
- data/source note

Internal markdown may still be written for audit or debugging, but it must not be the only user-facing artifact.

Message should include:

- company name
- report type
- completion status
- top 3-5 findings
- note on evidence scope

### Type 2: Degraded analysis success

Return:

- short analysis summary
- explicit missing-data disclosure
- Feishu Doc URL if a degraded note was generated and delivered successfully

### Type 3: Clarification required

Return:

- why the task cannot proceed
- what user input is needed next

## Summary Message Structure

Use this order:

1. task completion line
2. report type and company
3. top findings
4. source or scope disclosure
5. Feishu Doc link

## V1 Message Template

```text
已完成：{company} {report_type} 初稿

核心结论：
1. {finding_1}
2. {finding_2}
3. {finding_3}

说明：
- 本稿为研究初稿，默认不含正式评级和目标价
- 主要依据：{source_summary}

飞书文档：
- {document_url}

本地留档：
- {artifact_reference}
```

## Artifact Rules

V1 artifact priority:

1. Feishu Doc
2. markdown
3. docx
4. pdf

Use deterministic file names:

- `{company}_{report_type}_{YYYYMMDD}.md`
- `{company}_{report_type}_{YYYYMMDD}.docx`

Feishu Doc title should be deterministic:

- `{company} {report_type} {YYYY-MM-DD}`

## Feishu Doc Write Sequence

The delivery path must follow this sequence:

1. create Feishu Doc
2. write report body into Feishu Doc
3. verify that the doc contains body content, not just a title block
4. return the URL in the final message

Preferred runtime path:

- use a deterministic report-to-Feishu writer script when available
- do not rely on free-form tool chatter to decide whether the body was written

Do not assume `create` writes the body.
Do not return success if only a local markdown file exists.
Do not return success if the document only contains the title page.

## Failure And Timeout Messaging

If the run fails or times out, return:

- failure reason in plain language
- whether partial work exists
- whether the user should retry or provide more data

Do not return raw stack traces or tool noise.

## Compliance Rules For Delivery

Before sending a success message:

- confirm whether the artifact passed the compliance checklist
- confirm whether the artifact passed the quality checklist
- confirm whether a Feishu Doc URL exists and is usable as the primary user-facing artifact
- confirm that the Feishu Doc has body content, not just a title block

If not, do not present the run as complete.
