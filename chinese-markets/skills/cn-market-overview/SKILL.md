---
name: cn-market-overview
description: |
  中国股市（A股+港股）市场全景概览技能。提供主要指数行情、板块轮动、资金流向、市场情绪等综合市场信息。

  **触发条件：**
  用户提到"市场概览"、"大盘怎么样"、"今日行情"、"市场总结"、"板块分析"
---

# 中国股市概览技能

## 数据获取

### 指数数据
```python
import akshare as ak

# A股主要指数
index_zh_a_hist = ak.index_zh_a_hist(
    symbol="000001",  # 上证指数
    period="daily",
    start_date="20240101",
    end_date="20241231"
)

# 实时指数
stock_zh_index_spot_em = ak.stock_zh_index_spot_em(symbol="沪深重要指数")

# 港股指数
index_hk_spot_em = ak.stock_hk_index_spot_em()
```

### 板块数据
```python
# 行业板块
stock_board_industry_name_em = ak.stock_board_industry_name_em()

# 概念板块
stock_board_concept_name_em = ak.stock_board_concept_name_em()
```

### 资金数据
```python
# 北向资金
stock_hsgt_north_net_flow_in_em = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")

# 南向资金
stock_hsgt_south_net_flow_in_em = ak.stock_hsgt_south_net_flow_in_em(symbol="南下")

# 两市成交额
stock_zh_a_spot_em = ak.stock_zh_a_spot_em()  # 汇总计算

# 融资融券
stock_margin_sse = ak.stock_margin_sse(
    start_date="20241201",
    end_date="20241231"
)
```

### 市场情绪
```python
# 涨跌统计
stock_market_activity_legu = ak.stock_market_activity_legu()

# 涨停分析
stock_zt_pool_em = ak.stock_zt_pool_em(date="20241220")  # 涨停池
stock_zt_pool_dtgc_em = ak.stock_zt_pool_dtgc_em(date="20241220")  # 跌停池
```

## 分析维度

### 1. 宏观市场状态

**多空判断框架：**
- 指数位置：相对于 MA20/MA60/MA250 的位置
- 成交量：与近20日均量对比
- 资金流向：北向资金连续流入/流出天数
- 情绪指标：涨跌家数比

### 2. 板块轮动分析

**轮动规律：**
- 金融→周期→消费→科技→防御
- 关注连续领涨板块的持续性
- 主线板块 vs 轮动补涨

### 3. 资金流向解读

**北向资金：**
- 单日净流入 > 50亿：强烈看多信号
- 单日净流出 > 50亿：短期风险信号
- 连续5日以上同向流动：趋势信号

**融资余额：**
- 持续增加：市场做多情绪升温
- 快速下降：杠杆资金撤退

### 4. 港股联动

**AH联动：**
- AH溢价指数走势
- 南向资金流向
- 港股通成交占比

## 免责声明

市场分析基于公开数据和历史规律，不构成投资建议。
