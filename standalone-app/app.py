#!/usr/bin/env python3
"""
中国股市分析工具 - 独立运行版
支持 A股（上交所/深交所）和 港股（港交所）
数据来源：AKShare（免费）、Yahoo Finance（免费）、BaoStock（免费）

运行方式：
  python app.py              # 开发模式（默认端口 8888）
  python app.py --port 9999  # 指定端口
  python app.py --host 0.0.0.0  # 允许局域网访问（手机访问）
"""

import argparse
import json
import os
import sys
import webbrowser
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from data_fetcher import (
    get_a_stock_financial,
    get_a_stock_history,
    get_a_stock_realtime,
    get_ah_comparison,
    get_hk_stock_financial,
    get_hk_stock_history,
    get_hk_stock_realtime,
    get_industry_boards,
    get_market_overview,
    screen_stocks,
)

app = Flask(__name__)
app.json.ensure_ascii = False

VERSION = "1.0.0"
APP_NAME = "中国股市分析工具"


# ============================================================
# 页面路由
# ============================================================


@app.route("/")
def index():
    """主页"""
    return render_template("index.html", version=VERSION, app_name=APP_NAME)


# ============================================================
# API 路由 - A股
# ============================================================


@app.route("/api/a-stock/realtime/<symbol>")
def api_a_stock_realtime(symbol):
    """A股实时行情"""
    return jsonify(get_a_stock_realtime(symbol))


@app.route("/api/a-stock/history/<symbol>")
def api_a_stock_history(symbol):
    """A股历史行情"""
    period = request.args.get("period", "daily")
    days = int(request.args.get("days", 365))
    return jsonify(get_a_stock_history(symbol, period, days))


@app.route("/api/a-stock/financial/<symbol>")
def api_a_stock_financial(symbol):
    """A股财务数据"""
    return jsonify(get_a_stock_financial(symbol))


# ============================================================
# API 路由 - 港股
# ============================================================


@app.route("/api/hk-stock/realtime/<symbol>")
def api_hk_stock_realtime(symbol):
    """港股实时行情"""
    return jsonify(get_hk_stock_realtime(symbol))


@app.route("/api/hk-stock/history/<symbol>")
def api_hk_stock_history(symbol):
    """港股历史行情"""
    period = request.args.get("period", "1y")
    return jsonify(get_hk_stock_history(symbol, period))


@app.route("/api/hk-stock/financial/<symbol>")
def api_hk_stock_financial(symbol):
    """港股财务数据"""
    return jsonify(get_hk_stock_financial(symbol))


# ============================================================
# API 路由 - 市场概览
# ============================================================


@app.route("/api/market/overview")
def api_market_overview():
    """市场概览"""
    return jsonify(get_market_overview())


@app.route("/api/market/industries")
def api_market_industries():
    """行业板块"""
    return jsonify(get_industry_boards())


@app.route("/api/market/ah-comparison")
def api_ah_comparison():
    """AH股对比"""
    return jsonify(get_ah_comparison())


# ============================================================
# API 路由 - 股票筛选
# ============================================================


@app.route("/api/screener", methods=["POST"])
def api_screener():
    """股票筛选"""
    filters = request.get_json() or {}
    return jsonify(screen_stocks(filters))


# ============================================================
# API 路由 - 系统
# ============================================================


@app.route("/api/status")
def api_status():
    """系统状态"""
    return jsonify({
        "status": "running",
        "version": VERSION,
        "app_name": APP_NAME,
        "timestamp": datetime.now().isoformat(),
        "data_sources": {
            "akshare": "免费 - A股/港股实时和历史数据",
            "yfinance": "免费 - 港股/美股数据",
            "baostock": "免费 - A股历史数据",
        },
    })


# ============================================================
# 主入口
# ============================================================


def main():
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--host", default="127.0.0.1",
                        help="监听地址（默认127.0.0.1，使用0.0.0.0允许局域网访问）")
    parser.add_argument("--port", type=int, default=8888,
                        help="监听端口（默认8888）")
    parser.add_argument("--no-browser", action="store_true",
                        help="不自动打开浏览器")
    parser.add_argument("--production", action="store_true",
                        help="使用生产模式（waitress服务器）")
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════╗
║           {APP_NAME} v{VERSION}                ║
║                                                      ║
║  数据源: AKShare + Yahoo Finance + BaoStock（全免费） ║
║  覆盖: A股(上交所/深交所) + 港股(港交所)              ║
║                                                      ║
║  访问地址: http://{args.host}:{args.port}             ║
║  手机访问: http://[电脑IP]:{args.port}                ║
╚══════════════════════════════════════════════════════╝
    """)

    if not args.no_browser:
        url = f"http://{'localhost' if args.host == '0.0.0.0' else args.host}:{args.port}"
        webbrowser.open(url)

    if args.production:
        try:
            from waitress import serve
            print(f"[生产模式] 使用 waitress 服务器...")
            serve(app, host=args.host, port=args.port)
        except ImportError:
            print("[警告] waitress 未安装，回退到 Flask 开发服务器")
            app.run(host=args.host, port=args.port, debug=False)
    else:
        app.run(host=args.host, port=args.port, debug=True)


if __name__ == "__main__":
    main()
