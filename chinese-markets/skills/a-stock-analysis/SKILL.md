---
name: a-stock-analysis
description: |
  A股（上交所/深交所）全面分析技能。覆盖实时行情、历史数据、财务分析、技术分析和估值分析。
  使用免费数据源（AKShare、BaoStock）。

  **适用场景：**
  - A股个股深度分析
  - A股行业板块分析
  - A股技术面/基本面综合分析
  - A股估值评估

  **触发条件：**
  用户提到"A股分析"、"沪市/深市分析"、"上交所/深交所"、
  或提供6位A股代码（如600519、000001、300750）
---

# A股分析技能

## 数据源配置

### 主要数据源（全部免费）

**AKShare（核心数据源）：**
```python
import akshare as ak

# 实时行情
stock_zh_a_spot_em = ak.stock_zh_a_spot_em()  # A股实时行情（东方财富）

# 历史行情
stock_zh_a_hist = ak.stock_zh_a_hist(
    symbol="600519",
    period="daily",     # daily/weekly/monthly
    start_date="20230101",
    end_date="20241231",
    adjust="qfq"        # qfq前复权/hfq后复权/空不复权
)

# 财务数据
stock_financial_report = ak.stock_financial_report_sina(
    stock="600519",
    symbol="资产负债表"  # 资产负债表/利润表/现金流量表
)

# 财务指标
stock_financial_abstract = ak.stock_financial_abstract_ths(
    symbol="600519",
    indicator="按年度"  # 按年度/按单季度
)

# 行业数据
stock_board_industry_name_em = ak.stock_board_industry_name_em()  # 行业板块
stock_board_industry_cons_em = ak.stock_board_industry_cons_em(symbol="白酒")  # 行业成分股

# 资金流向
stock_individual_fund_flow = ak.stock_individual_fund_flow(
    stock="600519",
    market="sh"
)

# 北向资金
stock_hsgt_north_net_flow_in_em = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")

# 龙虎榜
stock_lhb_detail_em = ak.stock_lhb_detail_em(
    start_date="20241201",
    end_date="20241231"
)
```

**BaoStock（历史数据补充）：**
```python
import baostock as bs

# 登录
lg = bs.login()

# 日K线数据
rs = bs.query_history_k_data_plus(
    "sh.600519",
    "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
    start_date='2023-01-01',
    end_date='2024-12-31',
    frequency="d",      # d=日, w=周, m=月
    adjustflag="2"       # 1=后复权, 2=前复权, 3=不复权
)

# 季频财务指标
rs_profit = bs.query_profit_data(code="sh.600519", year=2024, quarter=3)
rs_operation = bs.query_operation_data(code="sh.600519", year=2024, quarter=3)
rs_growth = bs.query_growth_data(code="sh.600519", year=2024, quarter=3)
rs_balance = bs.query_balance_data(code="sh.600519", year=2024, quarter=3)
rs_cash = bs.query_cash_flow_data(code="sh.600519", year=2024, quarter=3)

# 登出
bs.logout()
```

## 分析框架

### 1. 基本面分析

**盈利能力：**
- ROE（净资产收益率）：> 15% 为优秀
- 毛利率趋势：稳定或上升为佳
- 净利率趋势：关注费用控制能力
- ROIC（投入资本回报率）

**成长性：**
- 营收增速：与行业平均对比
- 净利润增速：是否高于营收增速（经营杠杆）
- 扣非净利增速：排除一次性损益

**财务健康度：**
- 资产负债率：< 60% 为一般安全线（行业不同）
- 流动比率：> 1.5 为健康
- 速动比率：> 1.0 为健康
- 经营现金流/净利润：> 1.0 为优质

**分红能力：**
- 股息率
- 分红比例
- 连续分红年限

### 2. 技术分析

**均线系统：**
- MA5/MA10/MA20/MA60/MA120/MA250
- 多头排列：短期均线在上方，看涨信号
- 空头排列：短期均线在下方，看跌信号
- 金叉/死叉判断

**量价关系：**
- 放量上涨：主力资金进场
- 缩量回调：正常调整
- 放量下跌：主力出货信号
- 地量地价：可能见底

**关键价位：**
- 前高压力位
- 前低支撑位
- 整数关口心理价位
- 缺口位置

### 3. 估值分析

**绝对估值：**
- DCF（现金流折现）
- DDM（股利折现模型，适合高分红股）

**相对估值：**
- PE（TTM）vs 历史中位数
- PB vs 历史中位数
- PS vs 行业对比
- PEG = PE / 净利增速

**估值百分位：**
- 近5年PE百分位
- 近5年PB百分位
- < 20% 为低估区间
- > 80% 为高估区间

### 4. A股特色分析

**股东分析：**
- 前十大股东变化
- 机构持仓比例变化
- 沪深港通持股变化

**资金面分析：**
- 主力资金净流入/流出
- 北向资金动向
- 融资买入额变化

**政策面关注：**
- 行业政策变化
- 监管动态
- 国家战略方向

## 输出模板

```
══════════════════════════════════════════════════════
[公司名称]（代码: XXXXXX）深度分析报告
分析日期: YYYY-MM-DD
══════════════════════════════════════════════════════

一、公司概况
• 所属行业: XXXX
• 上市日期: YYYY-MM-DD
• 总市值: XXXX亿元
• 流通市值: XXXX亿元

二、行情数据
• 最新价: ¥XX.XX | 涨跌幅: ±X.XX%
• 今日成交额: XX.XX亿元
• 换手率: X.XX%

三、财务分析
[详细财务指标和趋势分析]

四、技术分析
[均线、量价、关键价位分析]

五、估值分析
[PE/PB/PS 当前值与历史对比]

六、综合评价
[综合以上分析的结论]

⚠️ 风险提示
• 本分析基于公开数据，仅供参考
• 不构成任何投资建议
• 投资有风险，决策需谨慎
══════════════════════════════════════════════════════
```

## 依赖

**必需：**
- Python 3.8+
- akshare >= 1.10.0
- baostock >= 0.8.8
- pandas >= 1.5.0

**可选：**
- matplotlib（图表生成）
- mplfinance（K线图）
