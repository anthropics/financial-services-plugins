"""
市场行情数据抓取器
数据源（全部免费/可溯源）：
  - AKShare          https://akshare.akfamily.xyz/  (A股/港股/美股，Python库)
  - yfinance         https://github.com/ranaroussi/yfinance  (美股/港股)  ⚠️ 国内被屏蔽，需代理
  - 东方财富          免费行情接口
  - Alpha Vantage    https://www.alphavantage.co/  (美股板块轮动，免费25次/天，国际网络可直连)
  - CNN Fear&Greed   https://edition.cnn.com/markets/fear-and-greed  ⚠️ 国内被屏蔽，需代理
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

logger = logging.getLogger(__name__)
CST = timezone(timedelta(hours=8))


@dataclass
class IndexSnapshot:
    name: str
    symbol: str
    last_close: float
    prev_close: float
    change_pct: float
    volume: float       # 成交量（万手）
    turnover: float     # 成交额（亿元）
    source: str
    source_url: str
    as_of: datetime

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "last_close": self.last_close,
            "prev_close": self.prev_close,
            "change_pct": round(self.change_pct, 2),
            "volume": self.volume,
            "turnover": self.turnover,
            "source": self.source,
            "source_url": self.source_url,
            "as_of": self.as_of.isoformat(),
        }


@dataclass
class SectorPerformance:
    name: str
    change_pct: float
    leading_stocks: list[str]
    source: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "change_pct": round(self.change_pct, 2),
            "leading_stocks": self.leading_stocks,
            "source": self.source,
        }


class MarketDataFetcher:
    """抓取三地市场指数、板块、北向资金等行情数据"""

    def __init__(self, alpha_vantage_key: str = ""):
        self._akshare_available = self._check_akshare()
        self._yfinance_available = self._check_yfinance()
        self._alpha_vantage_key = alpha_vantage_key

    # ── 主入口 ─────────────────────────────────────────────────────────

    def fetch_market_overview(self, market: str) -> dict:
        """
        market: 'cn'(A股) | 'hk'(港股) | 'us'(美股)
        返回包含指数快照、板块表现、资金流向的字典
        """
        if market == "cn":
            return self._cn_overview()
        elif market == "hk":
            return self._hk_overview()
        elif market == "us":
            return self._us_overview()
        return {}

    # ── A股 ────────────────────────────────────────────────────────────

    def _cn_overview(self) -> dict:
        result = {
            "market": "A股",
            "indices": [],
            "sectors": [],
            "north_flow": None,  # 北向资金
            "limit_up_count": None,
            "limit_down_count": None,
        }
        try:
            import akshare as ak

            # 主要指数
            index_map = {
                "上证指数": "sh000001",
                "深证成指": "sz399001",
                "创业板指": "sz399006",
                "沪深300": "sh000300",
                "科创50":  "sh000688",
                "中证500":  "sh000905",
            }
            for name, symbol in index_map.items():
                try:
                    df = ak.stock_zh_index_daily(symbol=symbol)
                    if df is not None and len(df) >= 2:
                        last = df.iloc[-1]
                        prev = df.iloc[-2]
                        change_pct = (last["close"] - prev["close"]) / prev["close"] * 100
                        result["indices"].append(IndexSnapshot(
                            name=name, symbol=symbol,
                            last_close=float(last["close"]),
                            prev_close=float(prev["close"]),
                            change_pct=change_pct,
                            volume=float(last.get("volume", 0)) / 1e4,
                            turnover=float(last.get("amount", 0)) / 1e8,
                            source="AKShare/东方财富",
                            source_url="https://www.eastmoney.com/",
                            as_of=datetime.now(CST),
                        ).to_dict())
                except Exception as e:
                    logger.debug(f"指数 {name} 获取失败: {e}")

            # 行业板块涨跌
            try:
                sector_df = ak.stock_board_industry_name_em()
                if sector_df is not None:
                    top5 = sector_df.nlargest(5, "涨跌幅")
                    bot5 = sector_df.nsmallest(5, "涨跌幅")
                    for _, row in list(top5.iterrows()) + list(bot5.iterrows()):
                        result["sectors"].append(SectorPerformance(
                            name=str(row.get("板块名称", "")),
                            change_pct=float(row.get("涨跌幅", 0)),
                            leading_stocks=[],
                            source="东方财富",
                        ).to_dict())
            except Exception as e:
                logger.debug(f"行业板块获取失败: {e}")

            # 北向资金
            try:
                north_df = ak.stock_em_hsgt_north_net_flow_in(symbol="全部")
                if north_df is not None and len(north_df) > 0:
                    latest = north_df.iloc[-1]
                    result["north_flow"] = {
                        "date": str(latest.get("日期", "")),
                        "net_inflow_bn": round(float(latest.get("当日成交净买额", 0)) / 1e8, 2),
                        "source": "东方财富",
                        "source_url": "https://data.eastmoney.com/hsgt/",
                    }
            except Exception as e:
                logger.debug(f"北向资金获取失败: {e}")

            # 涨跌停数量
            try:
                zt_df = ak.stock_zt_pool_em(date=datetime.now(CST).strftime("%Y%m%d"))
                dt_df = ak.stock_zt_pool_dtgc_em(date=datetime.now(CST).strftime("%Y%m%d"))
                result["limit_up_count"] = len(zt_df) if zt_df is not None else None
                result["limit_down_count"] = len(dt_df) if dt_df is not None else None
            except Exception as e:
                logger.debug(f"涨跌停数量获取失败: {e}")

        except ImportError:
            logger.warning("AKShare 未安装，使用备用方案")
            result = self._cn_overview_fallback()
        except Exception as e:
            logger.error(f"A股数据获取失败: {e}")
        return result

    def _cn_overview_fallback(self) -> dict:
        """备用：直接调用东方财富接口"""
        import requests
        result = {"market": "A股", "indices": [], "sectors": [], "north_flow": None}
        try:
            url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
            params = {
                "fltt": 2, "invt": 2, "fields": "f1,f2,f3,f4,f12,f14,f15,f16,f17,f18",
                "secids": "1.000001,0.399001,0.399006,1.000300,1.000688,0.399905",
                "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            }
            r = requests.get(url, params=params, timeout=10,
                             headers={"User-Agent": "Mozilla/5.0"})
            data = r.json()
            name_map = {
                "000001": "上证指数", "399001": "深证成指",
                "399006": "创业板指", "000300": "沪深300",
                "000688": "科创50",  "399905": "中证500",
            }
            for item in data.get("data", {}).get("diff", []):
                code = item.get("f12", "")
                name = name_map.get(code, code)
                current = item.get("f2", 0) / 100 if item.get("f2") else 0
                chg = item.get("f3", 0) / 100 if item.get("f3") else 0
                result["indices"].append({
                    "name": name, "symbol": code,
                    "last_close": current, "change_pct": chg,
                    "source": "东方财富", "source_url": "https://www.eastmoney.com/",
                    "as_of": datetime.now(CST).isoformat(),
                })
        except Exception as e:
            logger.error(f"东方财富备用接口失败: {e}")
        return result

    # ── 港股 ────────────────────────────────────────────────────────────

    def _hk_overview(self) -> dict:
        result = {"market": "港股", "indices": [], "sectors": []}
        if self._akshare_available:
            try:
                import akshare as ak
                index_map = {
                    "恒生指数": "^HSI",
                    "恒生科技": "^HSTECH",
                    "恒生中国企业": "^HSCE",
                }
                for name, symbol in index_map.items():
                    try:
                        df = ak.index_investing_global_hist(symbol=symbol.lstrip("^"), period="daily")
                        if df is not None and len(df) >= 2:
                            last = df.iloc[-1]
                            prev = df.iloc[-2]
                            chg = (float(last["收盘"]) - float(prev["收盘"])) / float(prev["收盘"]) * 100
                            result["indices"].append({
                                "name": name, "symbol": symbol,
                                "last_close": float(last["收盘"]),
                                "change_pct": round(chg, 2),
                                "source": "AKShare/Investing",
                                "source_url": "https://hk.investing.com/",
                                "as_of": datetime.now(CST).isoformat(),
                            })
                    except Exception as e:
                        logger.debug(f"港股指数 {name} 失败: {e}")
            except Exception as e:
                logger.debug(f"港股 AKShare 失败: {e}")

        # yfinance 补充
        if self._yfinance_available and not result["indices"]:
            try:
                import yfinance as yf
                hk_indices = {"恒生指数": "^HSI", "恒生科技": "^HSTECH"}
                for name, symbol in hk_indices.items():
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="5d")
                    if len(hist) >= 2:
                        chg = (hist["Close"].iloc[-1] - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2] * 100
                        result["indices"].append({
                            "name": name, "symbol": symbol,
                            "last_close": round(float(hist["Close"].iloc[-1]), 2),
                            "change_pct": round(chg, 2),
                            "source": "Yahoo Finance",
                            "source_url": f"https://finance.yahoo.com/quote/{symbol}",
                            "as_of": datetime.now(CST).isoformat(),
                        })
            except Exception as e:
                logger.debug(f"yfinance 港股失败: {e}")
        return result

    # ── 美股 ────────────────────────────────────────────────────────────

    def _us_overview(self) -> dict:
        result = {"market": "美股", "indices": [], "sectors": [], "fear_greed": None}
        us_indices = {
            "道琼斯": "^DJI",
            "纳斯达克": "^IXIC",
            "标普500": "^GSPC",
            "罗素2000": "^RUT",
            "VIX恐慌指数": "^VIX",
        }

        if self._yfinance_available:
            try:
                import yfinance as yf
                for name, symbol in us_indices.items():
                    try:
                        ticker = yf.Ticker(symbol)
                        hist = ticker.history(period="5d")
                        if len(hist) >= 2:
                            close = float(hist["Close"].iloc[-1])
                            prev  = float(hist["Close"].iloc[-2])
                            chg   = (close - prev) / prev * 100
                            result["indices"].append({
                                "name": name, "symbol": symbol,
                                "last_close": round(close, 2),
                                "change_pct": round(chg, 2),
                                "source": "Yahoo Finance",
                                "source_url": f"https://finance.yahoo.com/quote/{symbol}",
                                "as_of": datetime.now(CST).isoformat(),
                            })
                    except Exception as e:
                        logger.debug(f"美股指数 {name} 失败: {e}")
            except Exception as e:
                logger.debug(f"yfinance 失败: {e}")

        # 恐惧贪婪指数（CNN，需美国网络）
        try:
            import requests
            r = requests.get(
                "https://production.dataviz.cnn.io/index/fearandgreed/graphdata",
                headers={"User-Agent": "Mozilla/5.0"}, timeout=10
            )
            data = r.json()
            score = data.get("fear_and_greed", {}).get("score")
            rating = data.get("fear_and_greed", {}).get("rating", "")
            if score:
                result["fear_greed"] = {
                    "score": round(score, 1),
                    "rating": rating,
                    "source": "CNN Fear & Greed Index",
                    "source_url": "https://edition.cnn.com/markets/fear-and-greed",
                }
        except Exception as e:
            logger.debug(f"恐惧贪婪指数获取失败（国内需代理）: {e}")

        # Alpha Vantage 美股板块轮动（需美国网络或代理，免费 25 次/天）
        if self._alpha_vantage_key and self._alpha_vantage_key != "demo":
            try:
                import requests as _req
                r = _req.get(
                    "https://www.alphavantage.co/query",
                    params={"function": "SECTOR", "apikey": self._alpha_vantage_key},
                    timeout=15,
                )
                data = r.json()
                # 取"1 Day"板块涨跌数据
                day_perf = data.get("Rank A: Real-Time Performance", {})
                if day_perf:
                    for sector_name, change_str in day_perf.items():
                        try:
                            change_pct = float(change_str.strip("%"))
                            result["sectors"].append(SectorPerformance(
                                name=sector_name,
                                change_pct=change_pct,
                                leading_stocks=[],
                                source="Alpha Vantage",
                            ).to_dict())
                        except ValueError:
                            pass
                    logger.debug(f"Alpha Vantage 板块数据：{len(result['sectors'])} 个板块")
            except Exception as e:
                logger.debug(f"Alpha Vantage 板块获取失败: {e}")

        return result

    # ── 工具 ───────────────────────────────────────────────────────────

    @staticmethod
    def _check_akshare() -> bool:
        try:
            import akshare  # noqa
            return True
        except ImportError:
            return False

    @staticmethod
    def _check_yfinance() -> bool:
        try:
            import yfinance  # noqa
            return True
        except ImportError:
            return False
