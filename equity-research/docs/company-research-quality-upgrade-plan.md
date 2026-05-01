# Company Research Report Quality Upgrade Plan

本文档是报告质量升级的总体方案，定义优化步骤、功能点清单和验收标准。

## 问题诊断

### 现状

MiniMax 报告实测暴露以下质量缺陷：

| 缺陷 | 根因文件 | 根因描述 |
|------|---------|---------|
| 无估值逻辑（DCF/可比/目标价区间） | chinese-report-template.md §7 | "若证据允许，可加入估值状态和情景讨论"——可选=不做 |
| 无财务表格/指标趋势 | chinese-report-template.md §5 | 只列指标名称，不要求表格结构 |
| 无风险分层（财务/运营/宏观） | chinese-report-template.md §8 | 列了4类风险但不要求按严重性分层 |
| 无 Bull/Base/Bear 情景 | 全链路无要求 | 模板、workflow、quality-checklist 均未提及 |
| 无行内引用 | source-hierarchy.md 有规则但模板无占位符 | LLM 不在模板中看到引用格式就会忽略 |
| 财务数据浅表 | evidence-contract.md | 门槛太低："至少一个财务来源"即可开写 |
| 质量检查形同虚设 | quality-checklist.md | 只检查"章节是否存在"，不检查分析深度 |
| 散文叙事而非分析框架 | workflow.md Step 4→6 | Fact Pack 直接到 Body Draft，缺少"分析框架构建"中间步骤 |

### 根因总结

模板定义了"写什么章节"但未定义"每个章节必须包含什么分析结构"。LLM 用叙事性散文填充章节，产出"商业记者综述"而非"分析师研报"。

---

## 优化步骤总览

共 4 个 Phase，按依赖顺序执行。

| Phase | 名称 | 核心产出 | 优先级 |
|-------|------|---------|--------|
| 1 | 模板结构升级 | 新版 chinese-report-template.md + 估值框架章节 | P0 |
| 2 | 证据门槛与流程升级 | 新版 evidence-contract + workflow 插入分析框架构建步骤 | P0 |
| 3 | 质量门禁升级 | 新版 quality-checklist + compliance-checklist 深度检查项 | P1 |
| 4 | Few-shot 示范与模型策略 | 示范报告片段 + 模型分层建议 | P2 |

---

## Phase 1: 模板结构升级

### 目标

将 chinese-report-template.md 从"章节大纲"升级为"分析结构模板"，每个章节包含必填的结构化产出要求。

### 涉及文件

| 文件 | 操作 |
|------|------|
| `equity-research/skills/initiating-coverage/assets/chinese-report-template.md` | 重写 |
| `equity-research/docs/company-research-output-contract.md` | 更新，增加估值章节要求 |
| `equity-research/docs/company-research-request-classification.md` | 更新，Class A 关联估值必填 |

### 功能点 1.1: 财务章节结构化（§5）

**当前状态**：§5 只列指标名称，无表格要求。

**目标产出**：

```
§5.1 核心财务摘要表（必填）
- 标准表格：指标 × (FY-2, FY-1, FY(E), FY+1(E), 来源)
- 必填行：营收、营收YoY%、毛利率、净利润、净利率、经营现金流、自由现金流
- 空格填 N/A 并在口径说明中解释
- 预测列仅在有明确依据时填写

§5.2 财务趋势分析（必填）
- 至少分析收入增速、利润率、现金流三个维度
- 每个关键数字必须行内引用来源

§5.3 单位经济/运营 KPI（按行业必填）
- 引用 sector-kpis-{sector}.md 中定义的必填 KPI
- 至少给出 2 个核心 KPI 的历史数据
```

**验收标准**：
- 模板中 §5 包含表格结构定义
- 表格至少 7 行必填指标
- 每行要求来源列

### 功能点 1.2: 新增估值框架章节（§7.5）

**当前状态**：整个 prompt chain 无估值章节。

**目标产出**：

在 §7（未来展望）和 §8（风险提示）之间插入独立估值章节：

```
§7.5 估值框架

§7.5.1 可比公司法（首次覆盖必填）
- 标准表格：公司 × (市值, EV/Revenue, EV/EBITDA, P/E, 增速, 来源)
- 至少 3 家可比公司 + 行业中位数
- 必须说明可比选择理由
- 必须说明标的溢价/折价及原因

§7.5.2 DCF/简化现金流分析（首次覆盖推荐）
- 关键假设清单
- 敏感性分析 2×2 矩阵（增速 × 折现率）

§7.5.3 情景分析（必填）
- Bull/Base/Bear 表格：情景 × (概率权重, 核心假设, 隐含估值/市值)
- 数据不足时必须写"当前证据不足以给出估值区间"并说明缺什么
```

**验收标准**：
- 模板包含 §7.5 及三个子节
- 可比公司表格结构完整
- 情景分析表格结构完整
- 数据不足降级路径已定义

### 功能点 1.3: 风险章节分层（§8）

**当前状态**：§8 列了 4 类风险但无分层要求。

**目标产出**：

```
§8 风险提示

§8.1 风险矩阵（必填）
- 按"影响程度 × 发生概率"分三档：高/中/低
- 每个风险写一句传导机制说明
- 表格：风险项 × (类别, 严重性, 概率, 传导机制)

§8.2 反证与下行风险（必填）
- 至少一条与核心结论相反的反证线索
- 如果结论乐观，必须写出最可能导致结论失败的场景
```

**验收标准**：
- §8 包含风险矩阵表格定义
- 要求反证/下行风险子节

### 功能点 1.4: 行内引用格式强制嵌入

**当前状态**：source-hierarchy.md 定义了引用规则，但模板中未嵌入格式示范。

**目标产出**：

在模板每个章节的产出要求中增加引用格式示范：

```
每个事实性断言必须行内引用，格式：
- `（来源：公司2024年年报 p.XX）`
- `（来源：SEC 10-K, 2025-02-18）`
- `（来源：2024Q4业绩会纪要）`

§9 数据来源与口径说明 不再是"引用集中地"，
而是对全文引用的汇总索引 + 口径差异说明。
```

**验收标准**：
- 模板中至少 3 个章节包含行内引用格式示范
- §9 角色从"唯一引用位置"变为"汇总索引"

### 功能点 1.5: 首页摘要增加定量要素

**当前状态**：首页只要求"先结论→再证据→再不确定性"。

**目标产出**：

```
首页摘要必须包含：
1. 3-5 条核心结论（已有）
2. 关键财务指标快照：最新营收、增速、利润率、估值倍数（新增）
3. Bull/Base/Bear 一行摘要（新增）
4. 最大风险一句话（新增）
```

**验收标准**：
- 首页摘要要求列表包含定量要素

---

## Phase 2: 证据门槛与流程升级

### 目标

提高起草前的证据门槛，并在 workflow 中插入"分析框架构建"中间步骤，防止从散装事实直接叙事。

### 涉及文件

| 文件 | 操作 |
|------|------|
| `equity-research/docs/company-research-evidence-contract.md` | 重写证据门槛 |
| `equity-research/docs/company-research-workflow.md` | 插入 Step 4.5 |
| `equity-research/docs/company-research-degraded-mode.md` | 更新降级触发条件 |

### 功能点 2.1: 升级首次覆盖证据门槛

**当前状态**：
- "at least one official disclosure source"
- "at least one current financial evidence source"

一篇新闻稿就能满足。

**目标产出**：

```
首次覆盖最低证据门槛（升级版）

财务数据（必须）：
- 至少 2 个完整财年的收入、利润、现金流数据
- 最新一期（季度或半年）的关键指标
- 若未上市，至少有招股书或融资轮次披露的财务摘要

业务数据（必须）：
- 收入拆分（按业务线/地区/客户类型）
- 至少 2 个核心运营 KPI 的历史数据

可比公司（首次覆盖必须）：
- 至少识别 3 家可比公司
- 至少获取可比公司的核心估值倍数

不满足时的降级规则：
- 只有 1 年财务数据 → Level B（分析笔记），明确标注
- 无收入拆分 → §4 标注"收入结构未披露"
- 无可比数据 → 估值章节写"无法建立可比框架"而非跳过
```

**验收标准**：
- evidence-contract.md 包含升级后的门槛
- 每个不满足条件有明确降级路径

### 功能点 2.2: Workflow 插入 Step 4.5 "分析框架构建"

**当前状态**：Fact Pack → Investment View Pack → Body Draft，中间缺少结构化分析步骤。

**目标产出**：

在 workflow.md Step 4（Fact Pack）和 Step 5（Investment View Pack）之间插入：

```
Step 4.5: 分析框架构建（Analysis Kit）

基于 Fact Pack，必须在起草前完成以下结构化产出：

1. 财务表格预填
   - 把收集到的财务数据填入标准表格结构
   - 标注每个数字的来源
   - 空格标 N/A

2. 可比公司筛选
   - 选出 3-5 家可比公司
   - 获取估值倍数
   - 说明筛选逻辑

3. 风险分层
   - 按高/中/低分类所有风险因素
   - 每个风险写一句传导机制

4. 情景假设
   - 列出 Bull/Base/Bear 的核心驱动假设差异

产出格式：结构化 Analysis Kit（JSON 或 Markdown 表格）
Body Draft 必须基于此 Kit 填充，不得从 Fact Pack 直接叙事。

Gate：Analysis Kit 不完整则不得进入 Body Draft。
```

**验收标准**：
- workflow.md 包含 Step 4.5
- Step 4.5 定义了 4 项必填产出
- Step 6（Body Draft）要求基于 Analysis Kit

### 功能点 2.3: 降级模式增加估值相关触发条件

**当前状态**：降级触发不包含估值数据缺失。

**目标产出**：

在 degraded-mode.md 的触发条件中增加：

```
新增降级触发条件：
- 无法获取可比公司估值数据（首次覆盖场景）
- 财务数据不足 2 个完整财年（首次覆盖场景）
- 收入拆分数据不可得

对应降级行为：
- 估值章节标注"数据不足，无法进行可比分析"
- 报告整体仍可为 Level A，但估值章节降为 Level B 标注
```

**验收标准**：
- degraded-mode.md 包含估值相关触发条件
- 支持"章节级降级"而非只有"整体降级"

---

## Phase 3: 质量门禁升级

### 目标

从"检查章节存在"升级为"检查分析深度"，让质量检查真正能拦截低质量报告。

### 涉及文件

| 文件 | 操作 |
|------|------|
| `equity-research/docs/company-research-quality-checklist.md` | 重写，增加深度检查项 |
| `equity-research/docs/company-research-compliance-checklist.md` | 增加引用密度检查 |
| `equity-research/docs/company-research-regression-suite.md` | 增加质量相关回归用例 |

### 功能点 3.1: Quality Checklist 增加分析深度检查

**当前状态**：
- "all required report sections are present"
- "key claims are evidence-backed"

**目标产出**：

```
分析深度检查（Must Pass）

财务部分：
- [ ] 核心财务摘要表存在且至少有 2 年数据
- [ ] 至少 3 个关键指标有 YoY 变化率
- [ ] 至少 2 个运营 KPI 有历史趋势

估值部分（首次覆盖）：
- [ ] 可比公司表存在且至少 3 家
- [ ] 可比选择理由已说明
- [ ] Bull/Base/Bear 三情景已给出
- [ ] 若无法估值，已明确说明原因和缺失数据

风险部分：
- [ ] 风险按严重程度分层（高/中/低）
- [ ] 至少有一条与核心结论相反的反证

引用部分：
- [ ] 每个财务数字有行内引用
- [ ] §9 数据来源具体到文件名/页码，非泛泛"公司公告"

新增 Fail 条件：
- 财务摘要表不存在 → Fail
- Bull/Base/Bear 缺失且无解释 → Fail
- 超过 3 个财务断言无来源 → Fail
- 可比公司表缺失（首次覆盖）且无解释 → Fail
```

**验收标准**：
- quality-checklist.md 包含上述所有检查项
- Fail 条件可被 LLM 自检执行

### 功能点 3.2: Compliance Checklist 增加引用密度要求

**当前状态**：只检查"source or scope disclosure is present"。

**目标产出**：

```
新增合规项：
- [ ] 报告正文中行内引用数量 >= 10（首次覆盖）/ >= 5（更新报告）
- [ ] 每个财务表格中的来源列无空白
- [ ] 估值可比公司数据有来源标注
```

**验收标准**：
- compliance-checklist.md 包含引用密度要求

### 功能点 3.3: 回归测试增加质量用例

**目标产出**：

在 regression-suite.md 中增加：

```
质量回归用例：

Case Q1: 财务表格完整性
- 输入：生成一份首次覆盖报告
- 预期：§5 包含标准财务摘要表，至少 7 行指标
- Fail：表格不存在或少于 5 行

Case Q2: 估值框架完整性
- 输入：生成一份首次覆盖报告
- 预期：§7.5 包含可比公司表（≥3家）和情景分析表
- Fail：两个表格均不存在

Case Q3: 风险分层
- 输入：生成一份报告
- 预期：§8 按高/中/低分层
- Fail：风险仅为无层级列表

Case Q4: 行内引用密度
- 输入：生成一份首次覆盖报告
- 预期：正文行内引用 ≥ 10 处
- Fail：引用 < 5 处

Case Q5: Bull/Base/Bear 降级路径
- 输入：数据不足时生成报告
- 预期：估值章节标注"数据不足"而非跳过
- Fail：估值章节完全缺失
```

**验收标准**：
- regression-suite.md 包含 Q1-Q5 用例

---

## Phase 4: Few-shot 示范与模型策略

### 目标

通过示范和模型配置进一步提高输出质量。

### 涉及文件

| 文件 | 操作 |
|------|------|
| `equity-research/skills/initiating-coverage/assets/example-report-excerpt.md` | 新建 |
| `equity-research/skills/initiating-coverage/assets/chinese-report-template.md` | 引用示例 |
| `agents/company-research/agent/BOOTSTRAP.md`（目标运行环境） | 更新引用 |
| `agents/company-research/agent/models.json`（目标运行环境） | 模型策略更新 |

### 功能点 4.1: 创建 Few-shot 示范报告片段

**目标产出**：

创建一个 2-3 页的示范报告片段（用虚构公司或已公开数据的公司），展示：

1. 财务摘要表的正确格式
2. 可比公司表的正确格式
3. Bull/Base/Bear 情景表的正确格式
4. 风险矩阵表的正确格式
5. 行内引用的正确用法
6. 首页摘要的正确写法

**注意**：不是完整报告，是"关键结构的示范片段"，控制 token 消耗。

**验收标准**：
- 示例文件存在
- 模板文件引用示例文件
- 示例覆盖 5 种核心结构

### 功能点 4.2: 模型分层策略建议

**目标产出**：

在 BOOTSTRAP.md 或独立文档中记录模型使用建议：

```
模型分层建议

Step 1-3（检索、分类、证据收集）：
- 当前模型即可（Qwen3-Max / Kimi K2.5）
- 重点是工具调用准确性，不需要强推理

Step 4.5（分析框架构建）：
- 建议使用 reasoning 模型（DeepSeek-R1 / Kimi K2.5 thinking）
- 这一步需要财务建模和逻辑推理能力

Step 5-7（Investment View + Body Draft + Front Page）：
- 建议使用强写作模型
- 需要在结构化要求下保持表达质量

Step 8（Verification）：
- 可用当前模型
- 主要是 checklist 比对
```

**验收标准**：
- 模型策略文档存在
- 每个 workflow step 有模型建议

### 功能点 4.3: Sector KPI 扩展

**当前状态**：只有 consumer 和 SaaS 两个行业 KPI 文件。

**目标产出**：

为 MiniMax 等 AI 公司覆盖的场景，增加：

```
sector-kpis-ai-platform.md
必填 KPI：
- MAU/DAU 及趋势
- ARPU
- 用户留存率（D1/D7/D30）
- API 调用量/收入
- 训练成本/推理成本趋势
- 模型性能基准得分
- 现金消耗速率（burn rate）
- 现金 runway
```

**验收标准**：
- 新增 sector KPI 文件
- 文件被 §5.3 引用路径覆盖

---

## 完整功能点清单

| ID | 功能点 | Phase | 优先级 | 涉及文件 | 操作 |
|----|--------|-------|--------|---------|------|
| 1.1 | 财务章节结构化 | 1 | P0 | chinese-report-template.md | 重写 §5 |
| 1.2 | 新增估值框架章节 | 1 | P0 | chinese-report-template.md | 新增 §7.5 |
| 1.3 | 风险章节分层 | 1 | P0 | chinese-report-template.md | 重写 §8 |
| 1.4 | 行内引用格式强制嵌入 | 1 | P0 | chinese-report-template.md | 全文更新 |
| 1.5 | 首页摘要增加定量要素 | 1 | P0 | chinese-report-template.md | 重写首页部分 |
| 1.6 | Output Contract 更新 | 1 | P0 | company-research-output-contract.md | 增加估值要求 |
| 1.7 | Request Classification 更新 | 1 | P1 | company-research-request-classification.md | Class A 关联估值必填 |
| 2.1 | 升级证据门槛 | 2 | P0 | company-research-evidence-contract.md | 重写门槛 |
| 2.2 | Workflow 插入分析框架构建 | 2 | P0 | company-research-workflow.md | 插入 Step 4.5 |
| 2.3 | 降级模式增加估值触发 | 2 | P1 | company-research-degraded-mode.md | 增加触发条件 |
| 3.1 | Quality Checklist 深度检查 | 3 | P1 | company-research-quality-checklist.md | 重写 |
| 3.2 | Compliance Checklist 引用密度 | 3 | P1 | company-research-compliance-checklist.md | 增加检查项 |
| 3.3 | 回归测试质量用例 | 3 | P1 | company-research-regression-suite.md | 增加 Q1-Q5 |
| 4.1 | Few-shot 示范报告片段 | 4 | P2 | example-report-excerpt.md | 新建 |
| 4.2 | 模型分层策略 | 4 | P2 | BOOTSTRAP.md 或独立文档 | 新建/更新 |
| 4.3 | AI Platform Sector KPI | 4 | P2 | sector-kpis-ai-platform.md | 新建 |

---

## 执行依赖关系

```
Phase 1 (模板升级)
  ├── 1.1 财务结构化
  ├── 1.2 估值章节 ──→ 依赖 1.1（表格格式一致）
  ├── 1.3 风险分层
  ├── 1.4 行内引用 ──→ 依赖 1.1-1.3（嵌入到各章节）
  ├── 1.5 首页定量 ──→ 依赖 1.2（引用估值结论）
  ├── 1.6 Output Contract ──→ 依赖 1.2
  └── 1.7 Request Classification ──→ 依赖 1.2

Phase 2 (证据与流程)  ──→ 依赖 Phase 1 完成
  ├── 2.1 证据门槛 ──→ 依赖 1.2（可比公司要求）
  ├── 2.2 Workflow Step 4.5 ──→ 依赖 2.1
  └── 2.3 降级模式 ──→ 依赖 2.1

Phase 3 (质量门禁)  ──→ 依赖 Phase 1+2 完成
  ├── 3.1 Quality Checklist ──→ 依赖 1.1-1.3 的结构定义
  ├── 3.2 Compliance Checklist ──→ 依赖 1.4 的引用格式
  └── 3.3 回归测试 ──→ 依赖 3.1+3.2

Phase 4 (示范与策略)  ──→ 可与 Phase 3 并行
  ├── 4.1 Few-shot 示例 ──→ 依赖 Phase 1 模板定稿
  ├── 4.2 模型策略 ──→ 依赖 2.2 Step 4.5 定义
  └── 4.3 Sector KPI ──→ 独立
```

---

## 部署计划

每个 Phase 完成后：

1. 更新本地 repo 文件
2. 同步到目标运行环境 workspace：`<workspace_root>/`
3. 更新 BOOTSTRAP.md（如涉及）：`<agent_runtime_root>/BOOTSTRAP.md`
4. 用一个测试公司（建议用 MiniMax）跑一次端到端验证
5. 与上一版 MiniMax 报告对比，检查新增结构是否出现

### 验收标准（E2E）

新报告必须满足以下全部条件才算优化成功：

- [ ] §5 包含财务摘要表，至少 7 行指标 × 2 年数据
- [ ] §7.5 包含可比公司表（≥3 家）或明确标注"数据不足"
- [ ] §7.5 包含 Bull/Base/Bear 情景表或降级说明
- [ ] §8 风险按高/中/低分层，含反证子节
- [ ] 正文行内引用 ≥ 10 处
- [ ] 首页摘要包含关键指标快照
- [ ] §9 数据来源具体到文件名/日期

---

## 与现有 Implementation Plan 的关系

本方案是对 `company-research-report-agent-implementation-plan.md` 中以下 Function 的升级补丁：

| 原 Function | 本方案对应 |
|-------------|-----------|
| Function 2: Chinese Report Template | Phase 1 全部 |
| Function 8: Evidence Collection Contract | Phase 2: 2.1 |
| Function 10: Report Generation Workflow | Phase 2: 2.2 |
| Function 5: Degraded Mode Behavior | Phase 2: 2.3 |
| Function 15: Compliance Checklist | Phase 3: 3.2 |
| Function 16: Quality Checklist | Phase 3: 3.1 |
| Function 17: Regression Suite | Phase 3: 3.3 |
| Function 4: Sector KPI Checklist | Phase 4: 4.3 |

原 implementation plan 的 function-by-function 交付模型和回归测试要求保持不变。本方案是在原框架内升级具体文档内容，不改变架构。
