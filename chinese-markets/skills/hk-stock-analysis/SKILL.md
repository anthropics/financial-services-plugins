---
name: hk-stock-analysis
description: |
  港股（港交所）全面分析技能。覆盖实时行情、历史数据、财务分析和估值分析。
  使用免费数据源（Yahoo Finance、AKShare）。

  **适用场景：**
  - 港股个股深度分析
  - AH股对比分析
  - 中概股回港分析
  - 港股估值评估

  **触发条件：**
  用户提到"港股"、"港交所"、"恒生"、或提供港股代码（如00700、09988）
---

# 港股分析技能

## 数据源配置

### 主要数据源（全部免费）

**Yahoo Finance（核心数据源）：**
```python
import yfinance as yf

# 港股代码格式: 数字.HK，如 0700.HK
ticker = yf.Ticker("0700.HK")

# 公司信息
info = ticker.info  # 包含市值、PE、PB、行业等

# 历史行情
hist = ticker.history(period="1y")  # 1d/5d/1mo/3mo/6mo/1y/2y/5y/10y/ytd/max

# 财务报表
income_stmt = ticker.financials          # 利润表
balance_sheet = ticker.balance_sheet     # 资产负债表
cash_flow = ticker.cashflow             # 现金流量表

# 季度财报
q_income = ticker.quarterly_financials
q_balance = ticker.quarterly_balance_sheet
q_cashflow = ticker.quarterly_cashflow

# 股息数据
dividends = ticker.dividends

# 机构持仓
holders = ticker.institutional_holders

# 分析师推荐
recommendations = ticker.recommendations
```

**AKShare（补充数据源）：**
```python
import akshare as ak

# 港股实时行情
stock_hk_spot_em = ak.stock_hk_spot_em()  # 港股实时行情

# 港股历史行情
stock_hk_hist = ak.stock_hk_hist(
    symbol="00700",
    period="daily",
    start_date="20230101",
    end_date="20241231",
    adjust="qfq"
)

# AH股数据
stock_a_ah_name_em = ak.stock_a_ah_name_em()  # AH股列表
stock_a_h_spot_em = ak.stock_a_h_spot_em()     # AH股实时比价

# 南向资金（港股通）
stock_hsgt_south_net_flow_in_em = ak.stock_hsgt_south_net_flow_in_em(symbol="南下")

# 港股通持股
stock_hsgt_hold_stock_em = ak.stock_hsgt_hold_stock_em(
    market="港股",
    indicator="今日排行"
)
```

## 分析框架

### 1. 港股基本面分析

**盈利能力（以港币为单位）：**
- ROE / ROA
- 毛利率 / 净利率 / EBITDA利润率
- 考虑汇率影响（人民币收入 vs 港币报价）

**成长性：**
- 营收增速（注意货币换算）
- 用户/客户增长（互联网公司）
- 分部业务增长拆分

**特殊关注：**
- 港股市场流动性（日均成交额）
- 做空比例
- 外资持股比例

### 2. 港股估值特点

**相比A股的折价因素：**
- 流动性折价
- 信息不对称折价
- 外汇风险折价
- 监管风险折价

**港股常用估值方法：**
- PE（TTM）- 适用大多数公司
- PB - 适用银行、地产
- PS - 适用互联网公司
- EV/EBITDA - 适用资本密集型行业
- 股息率 - 适用高分红蓝筹

### 3. AH股对比分析（双重上市公司）

```
AH溢价率 = (A股价格 / (H股价格 × 汇率) - 1) × 100%

解读：
• > 30%: A股显著溢价，H股可能更有价值
• 10-30%: 正常溢价区间
• < 10%: 溢价较低，两地估值趋同
• < 0%: H股溢价（罕见，通常出现在大型蓝筹）
```

### 4. 港股特有风险

- **汇率风险**：港币挂钩美元，但部分公司收入为人民币
- **流动性风险**：部分小盘股日均成交额极低
- **做空风险**：港股允许个股做空
- **除牌风险**：不满足上市条件可能被除牌
- **老千股风险**：频繁合股、供股摊薄散户利益

## 输出模板

```
══════════════════════════════════════════════════════
[公司名称]（港股代码: XXXXX.HK）分析报告
分析日期: YYYY-MM-DD
══════════════════════════════════════════════════════

一、公司概况
• 所属行业: XXXX
• 上市日期: YYYY-MM-DD
• 总市值: HK$XXXX亿 (约¥XXXX亿)

二、行情数据
• 最新价: HK$XX.XX | 涨跌幅: ±X.XX%
• 52周最高: HK$XX.XX | 52周最低: HK$XX.XX
• 日均成交额(20日): HK$XX.XX亿

三、财务分析（以港币/人民币双币种展示关键指标）

四、估值分析
• PE(TTM): XX.X | 5年中位数: XX.X
• PB: X.XX | 5年中位数: X.XX
• 股息率: X.XX%

五、AH股对比（如适用）
• A股价格: ¥XX.XX | H股价格: HK$XX.XX
• AH溢价率: XX.X%

六、综合评价

⚠️ 风险提示
• 港股特有风险提示
• 汇率风险提示
• 本分析不构成投资建议
══════════════════════════════════════════════════════
```

## 依赖

**必需：**
- Python 3.8+
- yfinance >= 0.2.28
- akshare >= 1.10.0
- pandas >= 1.5.0

**可选：**
- matplotlib（图表生成）
