"""
免费金融数据获取模块
支持 A股（AKShare + BaoStock）和 港股（Yahoo Finance + AKShare）
"""

import json
import traceback
from datetime import datetime, timedelta

import pandas as pd

# ============================================================
# A股数据获取
# ============================================================


def get_a_stock_realtime(symbol: str) -> dict:
    """获取A股实时行情数据"""
    import akshare as ak

    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df["代码"] == symbol]
        if row.empty:
            row = df[df["名称"].str.contains(symbol, na=False)]
        if row.empty:
            return {"error": f"未找到股票: {symbol}"}
        row = row.iloc[0]
        return {
            "code": str(row.get("代码", "")),
            "name": str(row.get("名称", "")),
            "price": float(row.get("最新价", 0) or 0),
            "change_pct": float(row.get("涨跌幅", 0) or 0),
            "change_amt": float(row.get("涨跌额", 0) or 0),
            "volume": float(row.get("成交量", 0) or 0),
            "amount": float(row.get("成交额", 0) or 0),
            "high": float(row.get("最高", 0) or 0),
            "low": float(row.get("最低", 0) or 0),
            "open": float(row.get("今开", 0) or 0),
            "prev_close": float(row.get("昨收", 0) or 0),
            "turnover_rate": float(row.get("换手率", 0) or 0),
            "pe": float(row.get("市盈率-动态", 0) or 0),
            "pb": float(row.get("市净率", 0) or 0),
            "total_mv": float(row.get("总市值", 0) or 0),
            "circ_mv": float(row.get("流通市值", 0) or 0),
            "amplitude": float(row.get("振幅", 0) or 0),
            "volume_ratio": float(row.get("量比", 0) or 0),
            "chg_60d": float(row.get("60日涨跌幅", 0) or 0),
            "chg_ytd": float(row.get("年初至今涨跌幅", 0) or 0),
        }
    except Exception as e:
        return {"error": f"获取A股实时数据失败: {str(e)}"}


def get_a_stock_history(symbol: str, period: str = "daily",
                        days: int = 365) -> dict:
    """获取A股历史行情数据"""
    import akshare as ak

    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust="qfq",
        )
        if df.empty:
            return {"error": "未获取到历史数据"}
        records = []
        for _, row in df.iterrows():
            records.append({
                "date": str(row.get("日期", "")),
                "open": float(row.get("开盘", 0) or 0),
                "close": float(row.get("收盘", 0) or 0),
                "high": float(row.get("最高", 0) or 0),
                "low": float(row.get("最低", 0) or 0),
                "volume": float(row.get("成交量", 0) or 0),
                "amount": float(row.get("成交额", 0) or 0),
                "change_pct": float(row.get("涨跌幅", 0) or 0),
            })
        return {
            "symbol": symbol,
            "period": period,
            "count": len(records),
            "data": records,
        }
    except Exception as e:
        return {"error": f"获取历史数据失败: {str(e)}"}


def get_a_stock_financial(symbol: str) -> dict:
    """获取A股财务指标"""
    import akshare as ak

    try:
        df = ak.stock_financial_abstract_ths(symbol=symbol, indicator="按年度")
        if df is None or df.empty:
            return {"error": "未获取到财务数据"}
        records = []
        for _, row in df.head(5).iterrows():
            record = {}
            for col in df.columns:
                val = row[col]
                if pd.isna(val):
                    record[col] = None
                elif isinstance(val, (int, float)):
                    record[col] = float(val)
                else:
                    record[col] = str(val)
            records.append(record)
        return {"symbol": symbol, "data": records}
    except Exception as e:
        return {"error": f"获取财务数据失败: {str(e)}"}


def get_a_stock_list() -> dict:
    """获取A股市场全部股票列表（精简版）"""
    import akshare as ak

    try:
        df = ak.stock_zh_a_spot_em()
        stocks = []
        for _, row in df.iterrows():
            stocks.append({
                "code": str(row.get("代码", "")),
                "name": str(row.get("名称", "")),
                "price": float(row.get("最新价", 0) or 0),
                "change_pct": float(row.get("涨跌幅", 0) or 0),
                "pe": float(row.get("市盈率-动态", 0) or 0),
                "pb": float(row.get("市净率", 0) or 0),
                "total_mv": float(row.get("总市值", 0) or 0),
            })
        return {"count": len(stocks), "data": stocks}
    except Exception as e:
        return {"error": f"获取股票列表失败: {str(e)}"}


# ============================================================
# 港股数据获取
# ============================================================


def get_hk_stock_realtime(symbol: str) -> dict:
    """获取港股实时行情数据"""
    try:
        import yfinance as yf

        # 格式化代码
        code = symbol.lstrip("0")
        ticker = yf.Ticker(f"{code}.HK")
        info = ticker.info
        if not info or "regularMarketPrice" not in info:
            return {"error": f"未找到港股: {symbol}"}
        return {
            "code": symbol,
            "name": info.get("longName", info.get("shortName", "")),
            "price": info.get("regularMarketPrice", 0),
            "prev_close": info.get("regularMarketPreviousClose", 0),
            "open": info.get("regularMarketOpen", 0),
            "high": info.get("regularMarketDayHigh", 0),
            "low": info.get("regularMarketDayLow", 0),
            "volume": info.get("regularMarketVolume", 0),
            "market_cap": info.get("marketCap", 0),
            "pe": info.get("trailingPE", 0),
            "pb": info.get("priceToBook", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
            "beta": info.get("beta", 0),
            "currency": "HKD",
        }
    except Exception as e:
        return {"error": f"获取港股数据失败: {str(e)}"}


def get_hk_stock_history(symbol: str, period: str = "1y") -> dict:
    """获取港股历史行情"""
    try:
        import yfinance as yf

        code = symbol.lstrip("0")
        ticker = yf.Ticker(f"{code}.HK")
        df = ticker.history(period=period)
        if df.empty:
            return {"error": "未获取到港股历史数据"}
        records = []
        for date, row in df.iterrows():
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(float(row.get("Open", 0)), 2),
                "close": round(float(row.get("Close", 0)), 2),
                "high": round(float(row.get("High", 0)), 2),
                "low": round(float(row.get("Low", 0)), 2),
                "volume": int(row.get("Volume", 0)),
            })
        return {"symbol": symbol, "count": len(records), "data": records}
    except Exception as e:
        return {"error": f"获取港股历史数据失败: {str(e)}"}


def get_hk_stock_financial(symbol: str) -> dict:
    """获取港股财务数据"""
    try:
        import yfinance as yf

        code = symbol.lstrip("0")
        ticker = yf.Ticker(f"{code}.HK")
        income = ticker.financials
        balance = ticker.balance_sheet
        if income is None or income.empty:
            return {"error": "未获取到港股财务数据"}
        result = {"symbol": symbol, "income_statement": {}, "balance_sheet": {}}
        for col in income.columns[:4]:
            period = col.strftime("%Y-%m-%d")
            data = {}
            for idx in income.index:
                val = income.loc[idx, col]
                data[idx] = None if pd.isna(val) else float(val)
            result["income_statement"][period] = data
        if balance is not None and not balance.empty:
            for col in balance.columns[:4]:
                period = col.strftime("%Y-%m-%d")
                data = {}
                for idx in balance.index:
                    val = balance.loc[idx, col]
                    data[idx] = None if pd.isna(val) else float(val)
                result["balance_sheet"][period] = data
        return result
    except Exception as e:
        return {"error": f"获取港股财务数据失败: {str(e)}"}


# ============================================================
# 市场概览
# ============================================================


def get_market_overview() -> dict:
    """获取市场概览数据"""
    import akshare as ak

    result = {"indices": [], "north_flow": None, "south_flow": None}
    try:
        idx_df = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
        if idx_df is not None and not idx_df.empty:
            for _, row in idx_df.head(10).iterrows():
                result["indices"].append({
                    "code": str(row.get("代码", "")),
                    "name": str(row.get("名称", "")),
                    "price": float(row.get("最新价", 0) or 0),
                    "change_pct": float(row.get("涨跌幅", 0) or 0),
                    "amount": float(row.get("成交额", 0) or 0),
                })
    except Exception:
        pass
    try:
        north_df = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")
        if north_df is not None and not north_df.empty:
            latest = north_df.iloc[-1]
            result["north_flow"] = {
                "date": str(latest.iloc[0]) if len(latest) > 0 else "",
                "value": float(latest.iloc[1]) if len(latest) > 1 else 0,
            }
    except Exception:
        pass
    return result


def get_industry_boards() -> dict:
    """获取行业板块数据"""
    import akshare as ak

    try:
        df = ak.stock_board_industry_name_em()
        if df is None or df.empty:
            return {"error": "未获取到行业板块数据"}
        boards = []
        for _, row in df.iterrows():
            boards.append({
                "name": str(row.get("板块名称", "")),
                "change_pct": float(row.get("涨跌幅", 0) or 0),
                "total_mv": float(row.get("总市值", 0) or 0),
                "turnover_rate": float(row.get("换手率", 0) or 0),
                "leader": str(row.get("领涨股票", "")),
                "leader_pct": float(row.get("领涨股票-涨跌幅", 0) or 0),
            })
        return {"count": len(boards), "data": boards}
    except Exception as e:
        return {"error": f"获取板块数据失败: {str(e)}"}


# ============================================================
# 股票筛选
# ============================================================


def screen_stocks(filters: dict) -> dict:
    """根据条件筛选A股"""
    import akshare as ak

    try:
        df = ak.stock_zh_a_spot_em()
        if df is None or df.empty:
            return {"error": "未获取到市场数据"}

        # 应用筛选条件
        if "pe_min" in filters and filters["pe_min"]:
            df = df[df["市盈率-动态"].astype(float, errors="ignore") >= float(filters["pe_min"])]
        if "pe_max" in filters and filters["pe_max"]:
            df = df[df["市盈率-动态"].astype(float, errors="ignore") <= float(filters["pe_max"])]
            df = df[df["市盈率-动态"].astype(float, errors="ignore") > 0]
        if "pb_max" in filters and filters["pb_max"]:
            df = df[df["市净率"].astype(float, errors="ignore") <= float(filters["pb_max"])]
            df = df[df["市净率"].astype(float, errors="ignore") > 0]
        if "mv_min" in filters and filters["mv_min"]:
            min_val = float(filters["mv_min"]) * 1e8  # 亿转元
            df = df[df["总市值"].astype(float, errors="ignore") >= min_val]
        if "mv_max" in filters and filters["mv_max"]:
            max_val = float(filters["mv_max"]) * 1e8
            df = df[df["总市值"].astype(float, errors="ignore") <= max_val]

        # 排序
        sort_by = filters.get("sort_by", "总市值")
        sort_asc = filters.get("sort_asc", False)
        if sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=sort_asc)

        # 取前30条
        df = df.head(30)
        results = []
        for _, row in df.iterrows():
            results.append({
                "code": str(row.get("代码", "")),
                "name": str(row.get("名称", "")),
                "price": float(row.get("最新价", 0) or 0),
                "change_pct": float(row.get("涨跌幅", 0) or 0),
                "pe": float(row.get("市盈率-动态", 0) or 0),
                "pb": float(row.get("市净率", 0) or 0),
                "total_mv": float(row.get("总市值", 0) or 0),
                "turnover_rate": float(row.get("换手率", 0) or 0),
            })
        return {"count": len(results), "data": results}
    except Exception as e:
        return {"error": f"筛选失败: {str(e)}"}


# ============================================================
# AH股对比
# ============================================================


def get_ah_comparison() -> dict:
    """获取AH股对比数据"""
    import akshare as ak

    try:
        df = ak.stock_a_h_spot_em()
        if df is None or df.empty:
            return {"error": "未获取到AH股数据"}
        records = []
        for _, row in df.iterrows():
            records.append({
                "name": str(row.get("名称", "")),
                "a_code": str(row.get("A股代码", "")),
                "h_code": str(row.get("H股代码", "")),
                "a_price": float(row.get("A股价格", 0) or 0),
                "h_price": float(row.get("H股价格", 0) or 0),
                "premium": float(row.get("比价(A/H)", 0) or 0),
            })
        return {"count": len(records), "data": records}
    except Exception as e:
        return {"error": f"获取AH股数据失败: {str(e)}"}
