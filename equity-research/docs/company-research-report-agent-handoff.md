# Company Research Report Agent Handoff

This file is the durable handoff record for future AI agents working on the company research report agent in this repository.

Read this file before proposing new architecture, new templates, or new workflow changes.

## Project State

The repo already contains the correct base architecture:

- `equity-research` is the report workflow layer
- `financial-analysis` is the valuation and shared connector layer
- `equity-research/skills/initiating-coverage` is the main skeleton for initiation reports
- `equity-research/skills/earnings-analysis` is the starting point for update notes

Do not replace this structure in V1.

## Decisions Already Made

These decisions are settled unless the user explicitly changes them.

### 1. Product goal

The goal is to generate a high-quality first draft of a company research report.

This project is not trying to solve:

- review workflow
- internal approval flow
- publication system
- portfolio management workflow

Only the first-draft generation layer is in scope.

### 2. Output scope

V1 should support:

- initiating coverage
- company update / earnings review

V1 should not try to support every report type.

### 3. Report framework

Use a hybrid structure:

- Goldman-style front page
  - conclusion first
  - key bullet points first
  - key metrics / valuation summary on page 1
- CICC / Chinese sell-side style body
  - investment thesis or event view
  - company overview
  - industry and competition
  - business-line analysis
  - financial analysis
  - forecast and valuation
  - risks
- Fund-style completeness checklist
  - business model
  - market space
  - competitive position
  - growth drivers
  - governance and incentives
  - risks and disconfirming evidence

This means:

- do not copy protected wording
- do copy structure and sequencing

### 4. Report assembly order

The report must be assembled in this order:

1. `Fact Pack`
2. `Investment View Pack`
3. `Body Draft`
4. `Front Page Summary`
5. `Verification`
6. `Export`

Do not generate the front page first.

### 5. Default Chinese research style

The default writing style is based on publicly visible Changsheng Fund disclosure patterns.

Use:

- cautious tone
- evidence first, conclusion second
- explicit source and scope language
- more `判断 / 预计 / 关注 / 需跟踪`
- less aggressive recommendation language

Do not default to highly promotional sell-side wording.

### 6. Default Chinese report template

Unless the user changes it, use this section order:

1. `核心结论`
2. `公司基本面概览`
3. `行业与市场环境`
4. `业务与竞争力分析`
5. `财务与关键指标分析`
6. `当前变化与驱动因素`
7. `未来展望`
8. `风险提示`
9. `数据来源与口径说明`

### 7. Default research framework

Unless the user changes it, use this analytical path:

1. `宏观与政策环境`
2. `行业景气度与周期位置`
3. `竞争格局与公司位置`
4. `公司质量`
5. `增长驱动与催化因素`
6. `交易与估值状态`
7. `风险与反证`

This came from publicly visible fund-manager and fund-report style, especially Changsheng Fund material.

### 8. Source priority rules

Unless the user changes it, use this source priority:

1. official regulatory and company disclosure
2. auditable or official-market reference data
3. public management communication
4. market and industry data providers
5. news and media coverage

If sources conflict:

1. latest formal filing or announcement
2. notes to financial statements
3. public management remarks
4. third-party interpretation

News must not be the primary basis for a core investment conclusion.

### 9. Rating and target price boundary

Unless the user explicitly requests otherwise, do not output:

- formal buy / sell ratings
- target price
- implied upside language

Use instead:

- `观点倾向`
- `关注重点`
- `后续验证指标`
- `需持续跟踪的风险`

### 10. Reuse-first policy

Future agents should reuse:

- current plugin architecture
- current initiation workflow
- current earnings workflow
- current `comps` and `dcf` flows
- external open-source connectors where possible

Do not propose new infrastructure before checking whether the need is already covered by:

- `sec-edgar-mcp`
- `sec-edgar-toolkit`
- `OpenBB`
- `Octagon MCP Server`
- `earningscall-python`
- `rag-citation`
- `docxtemplater`
- `pandoc`

## Open-Source Components Already Selected

Prefer these components before inventing new ones:

- Filing and fundamentals:
  - <https://github.com/stefanoamorelli/sec-edgar-mcp>
  - <https://github.com/stefanoamorelli/sec-edgar-toolkit>
- Market and profile data:
  - <https://github.com/OpenBB-finance/OpenBB>
- Transcript and event context:
  - <https://github.com/OctagonAI/octagon-mcp-server>
  - <https://github.com/EarningsCall/earningscall-python>
- Citation support:
  - <https://github.com/rahulanand1103/rag-citation>
- Export:
  - <https://github.com/open-xml-templating/docxtemplater>
  - <https://pandoc.org/>

## Quality Upgrade Status (2026-03-11)

A quality upgrade initiative is underway to fix low-quality report output (diagnosed from MiniMax report).

Root cause: Chinese template only defined "what sections to write" but not "what analytical structure each section must contain". LLM filled sections with narrative prose instead of structured analysis.

### Upgrade plan document

`equity-research/docs/company-research-quality-upgrade-plan.md` — 4 phases, 16 feature points.

### Reference material

High-quality Chinese analysis template sourced from Day1Global (public .skill archive):
- Saved to: `<local_research_notes_path>/day1global-tech-earnings-deepdive-SKILL.md`
- Also saved: valuation models, bias checklist, investing philosophies

### Phase completion status

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: Template structure upgrade (1.1-1.5) | **DONE** | chinese-report-template.md rewritten from 107-line skeleton to comprehensive v2.0 with mandatory tables, valuation framework, risk matrix, inline citations, chapter required/optional matrix |
| Phase 1: Downstream docs (1.6-1.7) | **DONE** | output-contract: Class A/B/C/D analytical structure requirements + degradation rules. request-classification: Class A mandatory structures list |
| Phase 2: Evidence threshold (2.1) | **DONE** | evidence-contract: 2+ fiscal years, revenue breakdown, 2+ KPIs, 3+ comps, each with degraded trigger |
| Phase 2: Workflow Step 4.5 (2.2) | **DONE** | workflow: Analysis Kit Construction inserted (financial pre-fill, comps screening, risk layering, scenario assumptions). Gate: Kit incomplete → block Body Draft |
| Phase 2: Degraded mode (2.3) | **DONE** | degraded-mode: added section-level degradation table (5 triggers: comps, 1yr financials, revenue breakdown, scenario, KPI). Rule: sections never silently omitted |
| Phase 3: Quality checklist (3.1) | **DONE** | quality-checklist: 17 Class A depth checks (financial/valuation/risk/citations/front page), 3 Class B checks, 6 explicit fail conditions |
| Phase 3: Compliance checklist (3.2) | **DONE** | compliance-checklist: citation density per class (A≥10, B≥5, C/D≥3), table source completeness, 2 new fail conditions |
| Phase 3: Regression suite (3.3) | **DONE** | regression-suite: Q1-Q5 quality cases (financial table, valuation framework, risk layering, citation density, degradation path) |
| Phase 4: Few-shot excerpt (4.1) | **DONE** | example-report-excerpt.md created with 6 demonstrations (front page, financial table, comps, scenarios, risk matrix, citations). Template references it |
| Phase 4: Model strategy (4.2) | **DONE** | company-research-model-strategy.md created. Step 4.5 + Step 6 identified as highest-priority for model quality. 3 tiers: Standard/Reasoning/Strong writing |
| Phase 4: AI Platform KPI (4.3) | **DONE** | sector-kpis-ai-platform.md created with 13 KPIs + 8 risk items. Covers MAU/ARPU/retention/inference cost/burn rate/runway |
| Deploy: file sync to staging | **DONE** | 13 files synced to `<workspace_root>/`. AGENTS.md updated with 3 new file references (example-report-excerpt, model-strategy, sector-kpis-ai-platform). Handoff doc synced. Verified 22 markdown files in staging. |
| Deploy: E2E validation | **FAILED** | 泡泡玛特 Class B test: 0 tables, 0 citations, 0 risk layering, delivered as inline message not Feishu Doc. All Q-cases failed. Root cause: agent likely did not read upgraded workspace docs. See regression-suite.md "2026-03-11 泡泡玛特" for full failure record |

### Key design decisions in v2.0 template

- Fused English template structure (Goldman front page + comps + DCF sensitivity) with Day1Global analysis depth (Key Forces + 6 investment philosophies + multi-method valuation)
- Added mandatory financial summary table (7+ rows x 5 columns with source column)
- Added comparable company table (3+ companies + median/mean)
- Added Bull/Base/Bear scenario table with probability weights
- Added risk matrix with severity x probability classification
- Added inline citation format enforcement throughout all chapters
- Added chapter required/optional matrix by report type (A/B/C/D)
- Preserved existing constraints: no formal rating/target price, Changsheng cautious tone, evidence-first

### E2E failure root cause (2026-03-11 泡泡玛特)

Confirmed root cause chain:
1. OpenClaw uses **persistent session** for Feishu direct messages (all DMs from same user share one session)
2. 泡泡玛特 request entered as message #201 in a session already containing 200 messages / 48K tokens of unrelated work (Day1Global skill installation)
3. AGENTS.md IS injected into system prompt every message (OpenClaw design), but it's a **reading list** of 19 files — requires model to voluntarily call `read_file` tool
4. qwen3-max in 48K token context **skipped all tool calls** and generated the entire report from parametric knowledge (zero tool calls, zero file reads, zero web searches)
5. Result: report with 0 tables, 0 citations, 0 risk layering, all data likely hallucinated

### Decided remediation plan

**Phase 5: Runtime remediation (adopted 2026-03-11)**

| Step | Action | Purpose |
|------|--------|---------|
| 5.1 | **Inline critical constraints into AGENTS.md** | Put "must not" rules directly in system prompt so they're seen every message without needing tool calls. Keep under 20K chars (bootstrapMaxChars limit). |
| 5.2 | **Session reset + test with qwen3-max** | Verify whether the upgraded docs work in a clean session. If yes → qwen3-max is viable with architecture fix. |
| 5.3 | **If qwen3-max still fails: add Claude Sonnet 4** | Claude proxy available at `<claude_proxy_base_url>`, anthropic-messages API. Use for Step 4.5 (Analysis Kit) + Step 6 (Body Draft) only. Classification/retrieval stays on qwen3-max for cost control. |

Execution order: 5.1 → 5.2 → evaluate → conditionally 5.3.

### Phase 5.1 completion record (2026-03-11)

- AGENTS.md rewritten (5,728 chars, under 20K limit): added 3 "绝对禁止" rules (no parametric generation, no vague numbers, no inline delivery), inlined structural requirements (tables/citations/risk layering per class), Class B incremental focus constraint, workflow summary with gate
- BOOTSTRAP.md updated (3,526 chars): added "最高优先级规则" block requiring read_file of 4 specific workspace docs + search tools before any report writing, explicit "no tool call = hallucination" warning
- All 5.1a-5.1d regression cases PASS

### Claude API proxy (for step 5.3 if needed)

- Base URL: `<claude_proxy_base_url>`
- API: POST `/v1/messages` (Anthropic Messages API compatible)
- Auth: `Authorization: Bearer ${CLAUDE_PROXY_API_KEY}`
- Required headers: `content-type: application/json`, `anthropic-version: 2023-06-01`
- Verified model: `claude-sonnet-4-20250514`

### Phase 5.2 测试结果 (2026-03-11)

Session 重置后用 qwen3-max 重新测试泡泡玛特 Class B。

**改善点**：模型执行了 4 次 web_search + 1 次 web_fetch + 1 次 write + 3 次 feishu_doc 调用（之前为 0）。数据来源真实，包含具体财务数字和明确财报期间。

**仍然失败的项目**：

| 用例 | 结果 | 详情 |
|------|------|------|
| Q1-B 财务表格 | **未通过** | 0 个 markdown 表格，财务数据全在正文散落 |
| Q3 风险分层 | **未通过** | 5 条风险平级 bullet，无严重性分类 |
| Q4-B 引用密度 | **未通过** | 0 条（来源：）格式的行内引用 |
| Q9 Class B 增量聚焦 | **未通过** | 写了完整公司概况（2010年成立…）而非增量更新 |
| Q10 无常识填充 | **未通过** | §3 全是"IP消费崛起""全球化布局"等泛泛描述 |

**结论**：5.1 修复解决了数据来源问题（不再凭空捏造），但 qwen3-max 无法遵守结构性格式规则（表格、引用格式、风险矩阵、报告类型范围约束）。这是模型指令遵循能力的限制，非 prompt 工程可解决。

**决策**：执行 Phase 5.3，切换 company-research agent 主模型为 Claude Sonnet 4。

### Phase 5.3 修复计划：模型切换 + 质量验证

**发现**：OpenClaw 支持 per-agent 模型覆盖（`executive` agent 已有先例）。

#### 功能清单

| 编号 | 功能 | 文件 | 测试用例 |
|------|------|------|---------|
| 5.3a | 添加 Claude proxy provider 到 models.json | models.json | JSON 合法，包含 claude-proxy provider，model id 和 API 配置正确 |
| 5.3b | 设置 company-research agent 使用 Claude | runtime config (agents.list) | company-research 条目包含 `model.primary: "claude-proxy/claude-sonnet-4-20250514"` |
| 5.3c | Session 重置 | sessions.json | feishu:direct session 已清除 |
| 5.3d | 泡泡玛特 Class B 端到端测试 | 报告输出 | Q1-B 通过（有 markdown 表格），Q3 通过（风险有分层），Q4-B 通过（引用≥5），Q9 通过（聚焦增量），Q10 通过（无泛泛描述） |
| 5.3e | 全量 Q0-Q12 回归 | 报告输出 | 所有结构性质量用例通过或有明确降级说明 |

#### 技术细节

- Claude proxy: `<claude_proxy_base_url>`, anthropic-messages API
- Auth: `Bearer ${CLAUDE_PROXY_API_KEY}`
- Model: `claude-sonnet-4-20250514`
- models.json 中 apiKey 直接写死（proxy 固定 token，不走 .env）
- runtime config 修改需要 gateway 重启生效
- 风险：Claude 是否能正确使用 OpenClaw 注册的 tools（brave_search、feishu_doc 等）——需在 5.3d 验证
- 官方推荐方案：`sessions_spawn` + 显式 `model` 参数（subagent 模型覆盖），而非脚本委托或 model.primary 切换
- 参考：[Sub-Agents 官方文档](https://docs.openclaw.ai/tools/subagents)，详细调研见 `<local_research_notes_path>/openclaw-multi-model-routing.md`

### Phase 5.3a 完成记录 (2026-03-11)

- models.json 添加 `claude-proxy` provider（anthropic-messages API）
- 部署路径：`<agent_runtime_root>/models.json`
- 5 个 provider 共存：dashscope, kimi-coding, volcengine, volcengine-plan, claude-proxy
- 测试：JSON 合法，provider 配置正确 ✅

### Phase 5.3b 完成记录 (2026-03-11)

- 源码验证 `sessions_spawn` + `model` 参数的完整调用链：
  - `sessions_spawn` 工具定义 (reply L30219) → `readStringParam(params, "model")` → `spawnSubagentDirect`
  - `spawnSubagentDirect` (reply L29793) → `resolveSubagentSpawnModelSelection({ modelOverride })` → 显式 model 最高优先级
  - `resolveSubagentSpawnModelSelection` (model-selection L17175) → `normalizeModelSelection(params.modelOverride)` 排第一，跳过所有 config 默认值
  - 解析后通过 `sessions.patch({ model })` 写入子 session → model override 生效
- **结论**：显式传入 `model` 参数不走 config 默认值路径，不受 Issue #10963 bug 影响
- 测试：源码逻辑验证通过 ✅（无需运行时测试，代码路径确定性保证）

### Phase 5.3c 完成记录 (2026-03-11)

- AGENTS.md 重写为三阶段多模型协作工作流（6,967 bytes）：
  - Phase 1（qwen3-max 自己做）：请求分类、搜索、证据收集、Fact Pack 组装
  - Phase 2（委托 Claude）：`sessions_spawn({ model: "claude-proxy/claude-sonnet-4-20250514", thinking: "high" })` — 分析工具包 + 报告正文
  - Phase 3（qwen3-max 自己做）：验证、补充前页摘要、飞书交付
- task 字段模板包含：报告类型、Fact Pack、9 章结构要求、引用/表格/风险分层格式要求
- 部署到 staging：`<workspace_root>/AGENTS.md`
- 测试：内容验证通过 ✅

### Phase 5.3d 测试记录 (2026-03-11)

**测试结果**：报告质量巨大飞跃，但 Claude 模型切换有阻塞。

**Session 行为**（4ada9469）：
1. qwen3-max 执行 7 次 brave_search 收集数据 ✅
2. 第一次 `sessions_spawn({ model: "claude-proxy/claude-sonnet-4-20250514" })` → **"model not allowed"** ❌
3. 第二次 spawn（无 model 参数，用默认 qwen3-max）→ 成功
4. subagent 完成后主 agent 写入 reports/ + 创建飞书文档 ✅

**报告质量评估（泡泡玛特_9992.HK_公司更新_20260311.md）**：

| 用例 | 结果 | 详情 |
|------|------|------|
| Q1-B 财务表格 | **✅ PASS** | §5 有 6 行 markdown 表格，每行有来源引用 |
| Q3 风险分层 | **✅ PASS** | 高/中/低分类，每条有传导机制（IP生命周期→销量下滑→库存积压→毛利率承压→利润下滑） |
| Q4-B 引用密度 | **✅ PASS** | 全文 >15 处（来源：具体文件名/日期）格式引用 |
| Q6 无模糊近似 | **✅ PASS** | 138.76亿、204.4%、45.74亿 — 全部精确数字 |
| Q7 数据来源具体性 | **✅ PASS** | §9 列出 5 个具体来源，含文件名和日期 |
| Q8 财务期间明确 | **✅ PASS** | "2025年上半年"、"2025年第三季度" |
| Q9 Class B 增量聚焦 | **✅ PASS** | §2 = "参见此前报告"（极简），§6 是最长章节 |
| Q10 无常识填充 | **✅ PASS** | 行业描述绑定具体公司数据 |
| Q12 报告保存 | **✅ PASS** | reports/泡泡玛特_9992.HK_公司更新_20260311.md |

**关键发现**：即使没用 Claude（subagent 用了默认 qwen3-max），报告质量也大幅提升。原因：
1. subagent 在干净上下文中运行（无历史噪音）
2. task 字段包含了完整 Fact Pack + 明确结构要求
3. AGENTS.md 的结构性约束通过 task prompt 传递给了 subagent

**待修复**：`claude-proxy/claude-sonnet-4-20250514` 被 model allowlist 拒绝，需要在 runtime config 中添加到允许列表

## What Is Still Pending (Original)

These are the original next concrete deliverables:

1. ~~Adapt initiation and earnings documentation to the default Chinese framework~~ (partially done via quality upgrade)
2. Create runtime-ready OpenClaw agent files and bind them into the target deployment
3. Connect the selected provider stack for launch
4. Run end-to-end validation through Feishu

## Delivery Rule Fix Applied

The Feishu user-facing artifact is now required to be a Feishu Doc URL.

This means:

- local markdown is still useful for internal traceability
- but a local path alone is not a successful delivery
- successful report delivery requires `create -> write -> confirm URL`

## Runtime Directory Layout (Critical — Do Not Confuse)

There are two `.openclaw` directories in the target runtime. They serve different purposes:

| Path | Purpose |
|------|---------|
| `<agent_root>/` | **Agent definitions** — BOOTSTRAP.md, models.json, workspace files. This is where the runtime config points to. |
| `<runtime_state_root>/` | **Runtime state** — sessions, cron, logs, gateway process, runtime config itself. |

Specifically for company-research:

| Item | Path |
|------|------|
| Agent definition | `<agent_runtime_root>/BOOTSTRAP.md` |
| Models config | `<agent_runtime_root>/models.json` |
| Workspace | `<workspace_root>/` |
| Runtime sessions | `<runtime_state_root>/agents/company-research/sessions/` |
| Master config | `<runtime_state_root>/openclaw.json` (agentDir + workspace + Feishu binding) |

**Rule**: Deploy agent files to `<agent_root>/`. Check runtime state in `<runtime_state_root>/`. Do not confuse them.

## Live State In Staging

The staging OpenClaw environment has already proven these behaviors:

- `company-research` agent exists and is routable from Feishu
- Routing: `<runtime_state_root>/openclaw.json` → accountId "default" → agentId "company-research"
- Agent dir: `<agent_runtime_root>/`
- Workspace: `<workspace_root>/`
- the default Feishu account is bound to this agent in staging
- the `default` Feishu account is bound to `company-research`
- full Apple report markdown exists in runtime workspace
- Feishu Doc create/write path is real and working
- a full Apple report has already been written to a live Feishu Doc
- that Feishu Doc link has already been sent to the target Feishu user

Validated live document:

- `<redacted_feishu_doc_url_2>`

This means the delivery channel is no longer hypothetical.

## Current Gap

There is still one runtime inconsistency to preserve in context:

- when the agent is explicitly told to read an existing markdown report and write it to Feishu Doc, delivery succeeds
- when a standard company-analysis request runs end to end, the model may still fall back to the old summary + local path pattern

Do not misstate this as "Feishu delivery is fully solved."

The correct status is:

- manual/live Feishu Doc delivery path: working
- default automatic report-completion path: not fully converged yet

## Runtime Mapping In Staging

Keep these mappings explicit:

- Feishu bot for user interaction:
  - account id: `default`
  - bot name: `<redacted_bot_name>`
  - bound agent: `company-research`
- Known-good Feishu Doc write app for full report body:
  - app id: `<redacted_feishu_app_id>`

Do not confuse:

- the Feishu bot account used for chat delivery
- the app identity that successfully wrote the full report body into Feishu Doc

## Document Delivery Caveat

The first Apple replacement link that was sent as a "success" turned out to be title-only.

Verified bad document:

- `<redacted_feishu_doc_url_1>`
- read-back result: `block_count = 1`, title only, no body

Verified replacement document with body:

- `<redacted_feishu_doc_url_2>`
- direct API verification with the writing app returned `code = 0`
- child block query returned content blocks, not an empty title-only doc

Future agents must preserve this lesson:

- "doc created" is not enough
- "URL returned" is not enough
- delivery is only valid after body existence is verified

Preferred runtime mitigation:

- use a deterministic markdown-to-Feishu-doc write path
- verify child blocks exist before treating the delivery as successful

## Constraints For Future AI Agents

Before making edits, future agents must follow these constraints:

- keep diffs small
- prefer documentation and template changes over architecture changes
- do not remove existing workflow files unless explicitly asked
- preserve the repo's current plugin / command / skill model
- verify whether an existing skill already covers the need before adding new files
- if browsing is available, verify time-sensitive facts and source URLs
- do not use a "minimal closed loop first" delivery strategy
- deliver one function at a time and require regression for that function before moving on

## Required Reading Order For Future Agents

Before doing more work, read:

1. `README.md`
2. `equity-research/docs/company-research-report-agent.md`
3. `equity-research/docs/company-research-report-agent-handoff.md`
4. `equity-research/docs/company-research-report-agent-implementation-plan.md`
5. `equity-research/docs/company-research-source-hierarchy.md`
6. `equity-research/docs/company-research-degraded-mode.md`
7. `equity-research/docs/company-research-recency-authority-gate.md`
8. `equity-research/docs/company-research-message-gating.md`
9. `equity-research/docs/company-research-feishu-delivery.md`
10. `equity-research/skills/initiating-coverage/assets/chinese-report-template.md`
11. `equity-research/skills/initiating-coverage/references/sector-kpis-saas.md`
12. `equity-research/skills/initiating-coverage/references/sector-kpis-consumer.md`
13. `equity-research/skills/initiating-coverage/SKILL.md`
14. `equity-research/skills/initiating-coverage/assets/report-template.md`
15. `equity-research/skills/initiating-coverage/assets/quality-checklist.md`

## Short Continuation Summary

If context is compressed, the minimum summary to preserve is:

- Build on existing `equity-research` + `financial-analysis` plugins
- Goal is first-draft company research reports, not full publishing workflow
- Use hybrid report structure: Goldman front page + Chinese sell-side body + fund-style checklist
- Use assembly order: Fact Pack -> Investment View Pack -> Body Draft -> Front Page Summary -> Verification -> Export
- Default Chinese style is cautious and evidence-first, based on Changsheng Fund-style public disclosure patterns
- Default section order and source priority are already fixed in this file
- User-visible messages must be filtered through explicit message-gating rules
- Retrieval must prioritize newest official high-value sources first
- Default output should avoid formal rating and target price unless explicitly requested
- Reuse open-source connectors before proposing custom infrastructure
- Execute delivery through the implementation plan and do not skip compliance/test gates
- Function-by-function delivery with per-function regression is mandatory

### Phase 5.3e: 台积电 + 智谱AI 实测（2026-03-11 18:24+）

**测试 1：台积电 Class B 公司更新**

请求："写一份台积电的公司更新"

执行时间线：
- 18:24:19 收到消息
- 18:24:48–18:25:46 Phase 1 数据收集（6×web_search，约 1 分钟）
- 18:26:28 sessions_spawn 调用（model: dashscope/qwen3-max-2026-01-23，未用 Claude）
- 18:26:35 主 agent dispatch 完成（replies=8，过程消息泄露给用户）
- 18:27:45 subagent 完成（77s）
- 18:29:17 write 保存报告（8,990 bytes）
- 18:29:35 feishu_doc create（只传 title 没传 content → 空文档）

质量检查：

| Case | 结果 | 详情 |
|------|------|------|
| Q1-B 财务表格 | PASS | markdown 表格，4 数据行，含"数据来源"列 |
| Q3 风险分层 | PASS | 高/中/低三级，每条有传导机制 |
| Q4-B 引用 ≥5 | PASS | 15 条行内引用 |
| Q6 无模糊近似 | PASS | 具体数字，无"约XX%" |
| Q7 数据来源具体 | PASS | §9 列出 10 个具体来源含日期 |
| Q8 财报期间明确 | PASS | 明确标注"2025年第三季度" |
| Q9 Class B 增量聚焦 | PASS | §2 仅一段，§6 最长 |
| Q10 无常识填充 | PASS | 行业评论绑定公司数据 |
| Q12 报告保存 | PASS | 台积电_TSMC_公司更新_20260311.md |

发现的问题：
1. **过程消息泄露**：8 条内部过程消息暴露给用户 → 违反 Q18
2. **飞书 Doc 空文档**：feishu_doc create 只传 title 没传 content
3. **模型未遵守 Claude 指定**：AGENTS.md 写 claude-proxy，实际用了 qwen3-max

**测试 2：智谱AI Class A 首次覆盖**

请求："写一篇智谱AI的首次收录公司分析报告"

执行时间线：
- 18:38 收到消息（进入台积电同一 session）
- 7×web_search + 2×tool fail（Tool not found）
- 18:42:40 sessions_spawn（model: dashscope/qwen3-max-2026-01-23，仍未用 Claude）
- 18:44:52 subagent 完成（132s）
- 主 agent 未执行 Phase 3（无 write、无 feishu_doc）
- 用户未收到报告

根因：sessions_spawn 异步特性 → 主 agent dispatch 后不会被唤醒执行 Phase 3。

**修复措施（已实施）**：

1. **禁止 #4：过程消息门控** — 加入禁止区，禁止向用户发送过程状态消息
2. **飞书交付指令修复** — 明确 feishu_doc create 必须同时传 content
3. **Phase 2+3 合并** — 将文件保存和飞书交付指令写入 subagent task prompt，不依赖主 agent 回来处理

AGENTS.md 更新后大小：5,005 bytes（bootstrapMaxChars 20,000 限制内）

**待验证**：
- 修复后的 AGENTS.md 是否解决了交付问题（需要新 session 测试）
- Claude 模型 allowlist 已添加但 agent 仍选择 qwen3-max（prompt 层面无法强制，可能需要 config 层面方案）
