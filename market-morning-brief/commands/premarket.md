---
description: 立即生成三地股市开盘前分析报告并推送飞书
argument-hint: "[asia|us] 例如: asia 或 us（默认 asia）"
---

# 开盘前分析命令

立即触发市场开盘前分析，抓取最新新闻、研报、经济数据，用第一性原则进行分析，推送到飞书。

## 工作流程

### 第一步：解析参数

- `asia`（默认）：生成 A股+港股 开盘前分析
- `us`：生成 美股 开盘前分析
- 无参数：默认生成 A股+港股 分析

### 第二步：执行分析

运行以下命令：

**Docker 环境：**
```bash
docker-compose exec market-brief python src/main.py --now premarket_asia
# 或
docker-compose exec market-brief python src/main.py --now premarket_us
```

**本地 Python 环境：**
```bash
python src/main.py --now premarket_asia
python src/main.py --now premarket_us
```

### 第三步：数据来源说明

本命令抓取以下可溯源数据源：

| 数据类型 | 来源 | 接口类型 |
|---------|------|---------|
| A股行情 | 东方财富/AKShare | 免费API |
| 港股行情 | Yahoo Finance/AKShare | 免费API |
| 美股行情 | Yahoo Finance | 免费API |
| 财经新闻 | 财联社、东方财富 | 免费RSS/API |
| 政策动态 | 新华社、人民日报 | 免费RSS |
| 监管公告 | 证监会、央行 | 官网抓取 |
| 港交所公告 | HKEX官网 | 官网抓取 |
| 美联储公告 | 美联储官网 | 免费RSS |
| 机构研报 | 东方财富研报中心 | 免费API |
| 经济日历 | Investing.com/AKShare | 免费API |
| 恐惧贪婪 | CNN Fear & Greed | 免费API |

### 第四步：输出结果

分析报告将推送到飞书群，包含：

1. **市场摘要** - 一句话概括当前市场环境
2. **关键事件** - 重大事件、影响变量（E/r/L/ρ）、传导链条
3. **板块展望** - 涨跌方向和核心驱动因素
4. **重点标的** - 附操作建议（买入/卖出/观望）和价格区间
5. **整体策略** - 基于第一性原则的操作建议
6. **风险提示** - 主要不确定性因素

### 第一性原则分析框架

所有分析基于以下框架：

```
市场价格 = f(盈利预期E × 利率折现r × 流动性L × 风险情绪ρ)

对每个事件：
  1. 它影响了哪个变量？(E/r/L/ρ)
  2. 影响方向？(正/负/中性)
  3. 影响幅度？(高/中/低)
  4. 传导链条？(事件→变量→行业→个股)
  5. 时间维度？(短期<1周 / 中期1-3个月)
```

## 使用示例

```
/market-morning-brief:premarket asia
/market-morning-brief:premarket us
```
