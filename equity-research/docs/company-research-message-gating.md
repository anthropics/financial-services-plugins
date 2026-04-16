# Company Research User Message Gating

This document defines what the agent may and may not send to the end user during report generation.

The purpose is to stop internal process chatter from leaking into Feishu.

## Core Rule

Only send a user-facing message if it changes the user's next decision or gives the user the final result.

If a message does not change the user's next decision, do not send it.

## Allowed User-Facing Message Types

### Type 1: Intake acknowledgement

Allowed once near the start of the run.

Use for:

- confirming the request was accepted
- confirming the intended report type
- confirming the agent will use current official and high-value sources first

Good example:

- `已开始生成泡泡玛特公司分析报告，将优先使用最新披露、业绩材料和可复核市场信息。`

### Type 2: Clarification request

Allowed only if a blocking ambiguity exists.

Use for:

- company identity ambiguity
- missing market/ticker when multiple listed entities match
- missing user choice that materially changes the report path

Rule:

- ask one concise question
- do not ask multiple speculative follow-ups

### Type 3: Blocking data warning

Allowed only if the agent cannot continue to a valid full report.

Use for:

- latest disclosure unavailable
- current financial evidence unavailable
- only stale or low-authority evidence found

Good example:

- `目前未取到泡泡玛特最新正式披露期的核心财务资料，不能按当前深度报告标准完成。`

### Type 4: Final result

Allowed once the run is complete.

Must contain:

- completion status
- report type
- 3-5 key findings
- scope/source disclosure
- Feishu Doc URL

### Type 5: Final failure

Allowed if the run cannot produce a compliant output.

Must contain:

- plain-language failure reason
- whether partial work exists
- what the user should do next, if anything

## Prohibited User-Facing Messages

Never send these to the user:

- `我现在需要收集更多信息`
- `让我继续收集`
- `我需要读取文件`
- `我现在创建报告文件`
- `我现在创建飞书文档`
- `我现在写入飞书文档`
- any tool-by-tool progress chatter
- any chain-of-thought style narration

These are internal execution steps, not user value.

## Message Filtering Test

Before sending a message, ask:

1. Does this change what the user should do next?
2. Does this provide the final result?
3. Does this explain a real blocking failure?

If the answer to all three is no, do not send the message.

## Completion Gate

Message gating is satisfied only if:

- no internal process chatter is sent to the user
- only allowed message types appear in the user-visible transcript
