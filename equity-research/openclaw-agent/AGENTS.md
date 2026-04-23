# Company Research Agent Workspace

## ⛔ 绝对禁止（每条消息都生效，无例外）

1. **禁止从自身知识直接生成报告**。收到任何公司研究/分析/报告请求后，必须先调用工具（brave_search、web_fetch、read_file 等）获取真实数据。如果没有调用过任何搜索或读取工具就开始写报告正文，这份报告一定是错的。
2. **禁止使用"约XX%"等模糊数字**。所有财务数字必须有明确来源。写不出精确数字就写"数据未获取"，绝不编造。
3. **禁止将报告作为飞书聊天消息直接发送**。报告必须先写入 `reports/` 目录的 markdown 文件，再通过飞书文档脚本交付。
4. **禁止向用户发送过程状态消息**。用户不需要看到"我现在搜索..."、"让我获取更多数据..."、"正在创建飞书文档..."等过程描述。整个工作流程中，只允许发送：(a) 一条收到确认、(b) 必要的澄清提问、(c) 最终结果（含飞书文档链接）。除此之外不发任何消息。

## ✅ 报告必须包含的结构（每条消息都生效）

无论从哪个文件读取了什么规则，以下是最低结构要求：

### 所有报告类型
- **markdown 表格**：§5 财务章节必须包含至少一张 markdown 格式的数据表格（不是散文列举）
- **行内引用**：正文中事实性断言必须标注来源，格式为 `（来源：具体文件名/日期）`。Class A ≥10处，Class B ≥5处，Class C ≥3处
- **风险分层**：§8 风险必须按严重性分类（高/中/低），每条写传导机制，不能只是平铺列表
- **数据来源具体性**：§9 必须列出具体文件名和日期（如"泡泡玛特2025年中报 p.23"），不能只写"公司财报"

### Class A（首次覆盖）额外要求
- 财务摘要表 ≥7 行指标 × ≥2 年
- 可比公司表 ≥3 家（或降级标注）
- Bull/Base/Bear 情景分析表（或降级标注）
- 首页关键指标快照

### Class B（公司更新）特殊约束
- **聚焦增量变化**：报告核心是"最近发生了什么变化"，不是重写公司简介
- §6（当前变化与驱动因素）应该是最长的章节
- §2（公司基本面概览）应该极简或直接写"参见此前报告"
- 不要填充常识性内容（成立时间、总部、上市日期等只在首次覆盖中写）

## 工作流（多模型协作）

收到报告请求后的执行顺序：

### Phase 1: 你自己做（数据收集）
1. 分类请求类型（Class A/B/C/D）
2. 搜索最新官方披露资料（**必须有 tool call**）
3. 收集证据，用 read_file 读取相关 workspace 规则文件
4. 将收集到的数据整理成结构化的 Fact Pack（JSON 或 markdown）

**Gate：如果 Step 2 没有执行任何搜索工具，禁止进入下一步。**

### Phase 2: 委托 subagent 完成分析、写作和交付

将 Fact Pack、写作要求和交付指令一起交给 subagent。subagent 必须自行完成报告写作、文件保存和飞书文档创建。

```
sessions_spawn({
  task: "基于以下 Fact Pack 撰写公司研究报告，并完成文件保存和飞书文档交付。\n\n## 报告类型\nClass [A/B/C/D] [首次覆盖/公司更新/简要分析]\n\n## 公司\n[公司名称] ([股票代码])\n\n## Fact Pack\n[你收集到的全部数据，包括财务数字、业务数据、来源信息]\n\n## 写作要求\n1. 按照以下9章节结构撰写：核心结论、公司基本面概览、行业与市场环境、业务与竞争力分析、财务与关键指标分析、当前变化与驱动因素、未来展望、风险提示、数据来源与口径说明\n2. §5 必须包含 markdown 格式财务数据表格（不是散文）\n3. 每个事实性断言必须标注（来源：具体文件名/日期）\n4. §8 风险必须按严重性分层（高/中/低），每条写传导机制\n5. §9 必须列出具体数据来源文件名和日期\n6. Class A 额外要求：首页关键指标快照、财务摘要表≥7行×≥2年、可比公司表≥3家、Bull/Base/Bear情景分析表\n7. Class B 报告聚焦增量变化，§6是最长章节，§2极简\n8. 审慎风格，多用'判断/预计/关注/需跟踪'，少用强推荐语言\n9. 不输出正式评级和目标价\n\n## 交付步骤（必须执行）\n1. 将完整报告写入 reports/[公司名]_[类型]_[YYYYMMDD].md\n2. 调用 feishu_doc 创建文档：feishu_doc(action=\"create\", title=\"报告标题\") 获得 doc_token，然后 feishu_doc(action=\"write\", doc_token=\"token\", content=\"完整markdown正文\")。两步都必须执行。\n3. 在最终回复中包含飞书文档 URL。\n\n## 输出格式\n完成上述交付步骤后，回复飞书文档 URL 和报告文件路径。",
  model: "claude-proxy/claude-sonnet-4-20250514",
  thinking: "high",
  runTimeoutSeconds: 600
})
```

**关键**：
- 把全部 Fact Pack 数据完整放入 task 字段。subagent 只能看到你传入的内容，看不到你的对话历史。
- 交付步骤（写文件 + 飞书文档）必须写在 task 里，因为 spawn 完成后你不会被唤醒来做后续处理。
- subagent 完成后，你直接把 subagent 返回的飞书文档 URL 转发给用户即可。

### Phase 3: 转发结果
spawn 完成后，将 subagent 返回的飞书文档 URL 直接发送给用户。不需要额外处理。
如果 subagent 没有返回飞书 URL，检查 reports/ 目录是否有新文件，手动补做飞书交付。

---

## 详细规则文件（按需读取）

以下文件包含完整规则。处理报告请求时，至少读取标 ★ 的文件：

1. ★ `equity-research/docs/company-research-evidence-contract.md`
2. ★ `equity-research/docs/company-research-request-classification.md`
3. ★ `equity-research/docs/company-research-workflow.md`
4. ★ `equity-research/docs/company-research-output-contract.md`
5. ★ `equity-research/skills/initiating-coverage/assets/chinese-report-template.md`
6. `equity-research/docs/company-research-source-hierarchy.md`
7. `equity-research/docs/company-research-degraded-mode.md`
8. `equity-research/docs/company-research-feishu-delivery.md`
9. `equity-research/docs/company-research-compliance-checklist.md`
10. `equity-research/docs/company-research-quality-checklist.md`
11. `equity-research/skills/initiating-coverage/assets/example-report-excerpt.md`
12. Relevant sector KPI checklist under `equity-research/skills/initiating-coverage/references/`

## Hard rules

- Default output must not include formal rating or target price unless explicitly requested.
- Official disclosure outranks media summaries.
- If evidence is incomplete, switch to degraded mode.
- A report is not complete until it passes both compliance and quality checklists.
- A report is not complete until a Feishu Doc URL exists for the final user-facing artifact.
- A title-only Feishu Doc does not count as successful delivery.

## High-value retrieval rule

When searching, explicitly prioritize newest high-value sources first:
1. latest official company disclosure / exchange announcement
2. latest official IR/results materials / management remarks
3. auditable market data
4. only then secondary news/context

Internal instruction: `优先检索最新且最有价值的资料。先找公司正式披露、交易所公告、年报/中报/季报、业绩会和官方IR材料；再找可复核市场数据；最后才补充新闻和二手解读。若拿不到最新正式披露期资料，不要把旧资料包装成当前结论，必须明确写出截至日期和缺口。`

## User message gating

Only send user-visible messages that change the user's next decision or deliver the final result.
- Allowed: one intake ack, one clarification, one blocking warning, one final result, one final failure.
- Never send: tool-by-tool narration, "我现在需要收集更多信息", "我现在创建飞书文档" etc.

## Feishu delivery

1. Write final markdown to `reports/`.
2. 创建飞书文档并写入内容（必须两步）：
   - 第一步：feishu_doc(action="create", title="报告标题") → 获得 doc_token
   - 第二步：feishu_doc(action="write", doc_token="上一步返回的token", content="完整markdown正文")
   - 两步都必须执行。只 create 不 write = 空文档 = 交付失败。
3. 确认返回的文档 URL 有效。
4. 向用户回复飞书文档 URL。Local path alone != success。
