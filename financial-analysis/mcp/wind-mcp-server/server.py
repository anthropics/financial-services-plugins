"""
Wind Financial Terminal MCP Server

A stdio-based MCP server that wraps Wind's Python API (WindPy),
exposing Wind data as MCP tools for Claude to use in financial analysis.

Requirements:
- Wind Financial Terminal installed locally
- WindPy Python package (bundled with Wind Terminal)
- Python 3.8+
- mcp package: pip install mcp
"""

import json
import sys
import logging
from datetime import datetime, timedelta
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "Wind Financial Terminal",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Wind connection management
# ---------------------------------------------------------------------------

_wind_started = False


def _ensure_wind():
    """Lazily start Wind connection on first tool call."""
    global _wind_started
    if _wind_started:
        return

    from WindPy import w  # noqa: N813

    result = w.start()
    if result.ErrorCode != 0:
        raise RuntimeError(f"Wind start failed: ErrorCode={result.ErrorCode}")
    _wind_started = True


def _wind():
    """Return the Wind w object, ensuring it's started."""
    _ensure_wind()
    from WindPy import w  # noqa: N813

    return w


def _format_wind_data(raw) -> dict[str, Any]:
    """Convert WindData object to a JSON-serializable dict."""
    if raw.ErrorCode != 0:
        return {"error": True, "error_code": raw.ErrorCode, "error_message": str(raw.Data)}

    result: dict[str, Any] = {
        "error": False,
        "codes": raw.Codes,
        "fields": raw.Fields,
        "times": [t.strftime("%Y-%m-%d") if hasattr(t, "strftime") else str(t) for t in raw.Times],
    }

    data = []
    for row in raw.Data:
        formatted_row = []
        for val in row:
            if val is None:
                formatted_row.append(None)
            elif hasattr(val, "strftime"):
                formatted_row.append(val.strftime("%Y-%m-%d"))
            elif isinstance(val, float) and val != val:  # NaN check
                formatted_row.append(None)
            else:
                formatted_row.append(val)
        data.append(formatted_row)
    result["data"] = data
    return result


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def wind_wsd(
    codes: str,
    fields: str,
    begin_date: str,
    end_date: str,
    options: str = "",
) -> str:
    """Retrieve historical time-series data from Wind (日期序列数据).

    Use this for historical stock prices, financial metrics over a date range,
    trading volume, technical indicators, etc.

    Args:
        codes: Security codes, comma-separated. Examples:
            - A-shares: "600519.SH" (Kweichow Moutai), "000858.SZ"
            - HK stocks: "00700.HK" (Tencent)
            - US stocks: "AAPL.O" (NASDAQ), "MSFT.N" (NYSE)
            - Indices: "000300.SH" (CSI 300), "HSI.HI" (Hang Seng)
            - Bonds: "019672.SH"
            - Futures: "IF2403.CFE"
        fields: Data fields, comma-separated. Common fields:
            - Prices: "open,high,low,close,volume,amt,pct_chg"
            - Valuation: "pe_ttm,pb_lf,ps_ttm,ev_ebitda"
            - Financials: "tot_oper_rev,oper_profit,net_profit_is"
            - Per-share: "eps_basic,bps,cfps"
        begin_date: Start date in "YYYY-MM-DD" format
        end_date: End date in "YYYY-MM-DD" format
        options: Optional Wind parameters, e.g. "PriceAdj=F" for forward-adjusted prices,
            "Period=W" for weekly, "Period=M" for monthly
    """
    w = _wind()
    raw = w.wsd(codes, fields, begin_date, end_date, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_wss(
    codes: str,
    fields: str,
    options: str = "",
) -> str:
    """Retrieve cross-sectional snapshot data from Wind (截面数据).

    Use this for current/latest financial data for one or more securities:
    latest valuation multiples, financial statement items, company info, etc.

    Args:
        codes: Security codes, comma-separated. Can query multiple securities at once.
            Example: "600519.SH,000858.SZ,000568.SZ" for comparing Baijiu stocks.
        fields: Data fields, comma-separated. Common fields:
            - Valuation: "pe_ttm,pb_lf,ps_ttm,pcf_ocf_ttm,ev_ebitda,mkt_cap_ard"
            - Income: "tot_oper_rev,oper_profit,net_profit_is,grossprofitmargin"
            - Balance: "tot_assets,tot_liab,tot_shrhldr_eqy_excl_min_int"
            - Cash flow: "net_cash_flows_oper_act,net_cash_flows_inv_act"
            - Growth: "yoy_or,yoy_np,qfa_yoy_or"
            - Company: "sec_name,industry_sw,province,listdate"
        options: Optional parameters, e.g.
            "rptDate=20231231" for specific reporting period,
            "unit=1" for units in yuan (default: 10k yuan)
    """
    w = _wind()
    raw = w.wss(codes, fields, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_wset(
    report_name: str,
    options: str = "",
) -> str:
    """Query Wind dataset tables (数据集).

    Use this for structured queries like index constituents, sector lists,
    IPO calendars, margin trading data, stock connect flows, etc.

    Args:
        report_name: Dataset name. Common datasets:
            - "sectorconstituent": Index/sector constituents
            - "indexconstituent": Index constituent weights
            - "ipo": IPO listing data
            - "margintrading": Margin trading data
            - "sharebuyback": Share buyback records
            - "topholderdata": Top shareholder data
            - "stockconnectsummary": Stock Connect (沪深港通) summary
        options: Query parameters as semicolon-separated key=value pairs.
            Examples:
            - "date=2024-01-15;sectorid=a]001010100000000" (CSI 300 constituents)
            - "date=2024-01-15;sectorid=1000008892000000" (沪深300)
            - "startdate=2024-01-01;enddate=2024-03-01" (date range filters)
    """
    w = _wind()
    raw = w.wset(report_name, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_edb(
    codes: str,
    begin_date: str,
    end_date: str,
    options: str = "",
) -> str:
    """Query Wind Economic Database for macro indicators (宏观经济数据库).

    Use this for macroeconomic data: GDP, CPI, PPI, PMI, monetary supply,
    interest rates, exchange rates, trade data, etc.

    Args:
        codes: EDB indicator codes, comma-separated. Common indicators:
            - GDP: "M0001228" (GDP current price), "M0001227" (GDP YoY)
            - CPI: "M0000612" (CPI YoY), "M0000616" (Core CPI YoY)
            - PPI: "M0001227" (PPI YoY)
            - PMI: "M0017126" (Manufacturing PMI), "M0017127" (Non-mfg PMI)
            - Money: "M0001385" (M2 YoY), "M0001387" (M1 YoY)
            - Rates: "M0009808" (LPR 1Y), "M0009809" (LPR 5Y)
            - Trade: "M0000607" (Exports YoY USD), "M0000608" (Imports YoY USD)
            - FX: "M0290205" (USD/CNY central parity)
            - US: "G0000891" (US CPI YoY), "G0000876" (US GDP QoQ SAAR)
        begin_date: Start date in "YYYY-MM-DD" format
        end_date: End date in "YYYY-MM-DD" format
        options: Optional parameters, e.g. "Fill=Previous" to fill missing data
    """
    w = _wind()
    raw = w.edb(codes, begin_date, end_date, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_wsi(
    codes: str,
    fields: str,
    begin_time: str,
    end_time: str,
    options: str = "",
) -> str:
    """Retrieve intraday minute-bar data from Wind (分钟线数据).

    Use this for intraday analysis: minute-level OHLCV, VWAP, etc.

    Args:
        codes: Single security code. Example: "600519.SH"
        fields: Data fields, comma-separated.
            Common: "open,high,low,close,volume,amt"
        begin_time: Start datetime in "YYYY-MM-DD HH:MM:SS" format
        end_time: End datetime in "YYYY-MM-DD HH:MM:SS" format
        options: Optional parameters, e.g. "BarSize=5" for 5-min bars (default 1-min)
    """
    w = _wind()
    raw = w.wsi(codes, fields, begin_time, end_time, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_wst(
    codes: str,
    fields: str,
    begin_time: str,
    end_time: str,
    options: str = "",
) -> str:
    """Retrieve intraday tick data from Wind (逐笔成交数据).

    Use this for tick-level analysis: individual trades, order flow, etc.

    Args:
        codes: Single security code. Example: "600519.SH"
        fields: Data fields, comma-separated.
            Common: "last,volume,amt,bid1,ask1,bsize1,asize1"
        begin_time: Start datetime in "YYYY-MM-DD HH:MM:SS" format
        end_time: End datetime in "YYYY-MM-DD HH:MM:SS" format
        options: Optional parameters
    """
    w = _wind()
    raw = w.wst(codes, fields, begin_time, end_time, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_wsq(
    codes: str,
    fields: str,
    options: str = "",
) -> str:
    """Retrieve real-time quote snapshot from Wind (实时行情数据).

    Use this for live/latest market data: current price, bid/ask, volume,
    turnover, limit up/down, VWAP, etc. Returns the most recent quote
    as a one-time snapshot (not a streaming subscription).

    Args:
        codes: Security codes, comma-separated. Can query multiple securities.
            Examples: "600519.SH,000858.SZ" or "00700.HK" or "AAPL.O"
        fields: Real-time quote fields, comma-separated. Common fields:
            - Price: "rt_last,rt_open,rt_high,rt_low,rt_pre_close"
            - Change: "rt_pct_chg,rt_chg,rt_swing"
            - Volume: "rt_vol,rt_amt,rt_turn"
            - Bid/Ask: "rt_bid1,rt_ask1,rt_bsize1,rt_asize1"
            - Extended: "rt_bid2,rt_bid3,rt_ask2,rt_ask3" (multi-level quotes)
            - Limit: "rt_uplimit,rt_downlimit"
            - VWAP: "rt_vwap"
            - Market cap: "rt_mkt_cap,rt_float_mkt_cap"
            - Status: "rt_trade_status,rt_susp_reason"
        options: Optional parameters
    """
    w = _wind()
    raw = w.wsq(codes, fields, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


@mcp.tool()
def wind_wpf(
    portfolio_name: str,
    fields: str,
    options: str = "",
) -> str:
    """Query Wind Portfolio data (组合数据).

    Use this to retrieve portfolio holdings, NAV, returns from Wind Portfolio Manager.

    Args:
        portfolio_name: Portfolio name as registered in Wind
        fields: Data fields. Common: "wind_code,sec_name,weight,mkt_value"
        options: Optional parameters, e.g. "view=LastDay" for latest holdings
    """
    w = _wind()
    raw = w.wpf(portfolio_name, fields, options)
    return json.dumps(_format_wind_data(raw), ensure_ascii=False)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
