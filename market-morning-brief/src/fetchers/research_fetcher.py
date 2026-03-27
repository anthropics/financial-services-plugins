"""
研究报告摘要抓取器
数据源（免费/公开）：
  - 东方财富研报中心    https://data.eastmoney.com/report/
  - 新浪财经研报        https://finance.sina.com.cn/stock/stockzmt.shtml
  - AKShare 研报接口    ak.stock_research_report_em()
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
CST = timezone(timedelta(hours=8))

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MarketBriefBot/1.0)"}


@dataclass
class ResearchReport:
    title: str
    institution: str       # 机构名（华泰证券、中金公司等）
    rating: str            # 买入/增持/中性/减持
    target_price: Optional[float]
    stock_name: str
    stock_code: str
    summary: str           # 摘要（300字以内）
    source: str
    source_url: str
    published_at: datetime

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "institution": self.institution,
            "rating": self.rating,
            "target_price": self.target_price,
            "stock_name": self.stock_name,
            "stock_code": self.stock_code,
            "summary": self.summary[:300],
            "source": self.source,
            "source_url": self.source_url,
            "published_at": self.published_at.isoformat(),
        }


class ResearchFetcher:
    """抓取最新研报摘要（开盘前 24h 内发布的）"""

    def fetch_recent(self, hours: int = 24, max_count: int = 20) -> list[ResearchReport]:
        reports = []
        cutoff = datetime.now(CST) - timedelta(hours=hours)

        for fetch_fn in [self._fetch_eastmoney, self._fetch_akshare]:
            try:
                items = fetch_fn()
                for item in items:
                    if item.published_at >= cutoff:
                        reports.append(item)
                    if len(reports) >= max_count:
                        break
            except Exception as e:
                logger.warning(f"[{fetch_fn.__name__}] 研报抓取失败: {e}")
            if len(reports) >= max_count:
                break

        # 按时间倒序，取 max_count 条
        reports.sort(key=lambda x: x.published_at, reverse=True)
        logger.info(f"共获取 {len(reports)} 条研报")
        return reports[:max_count]

    # ── 东方财富研报中心 ───────────────────────────────────────────────

    def _fetch_eastmoney(self) -> list[ResearchReport]:
        """
        东方财富研报中心接口
        https://data.eastmoney.com/report/stock.jshtml
        """
        url = "https://reportapi.eastmoney.com/report/list"
        params = {
            "cb": "datatable",
            "industryCode": "*",
            "pageSize": 50,
            "industry": "*",
            "rating": "*",
            "ratingChange": "*",
            "beginTime": (datetime.now(CST) - timedelta(days=2)).strftime("%Y-%m-%d"),
            "endTime": datetime.now(CST).strftime("%Y-%m-%d"),
            "pageNo": 1,
            "fields": "",
            "qType": 0,
            "orgCode": "",
            "_": int(datetime.now().timestamp() * 1000),
        }
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        text = r.text
        # 去掉 JSONP 包装
        if text.startswith("datatable("):
            text = text[10:-1]
        import json
        data = json.loads(text)

        items = []
        for report in data.get("data", []):
            pub_str = report.get("publishDate", "")
            try:
                pub = datetime.strptime(pub_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=CST)
            except Exception:
                try:
                    pub = datetime.strptime(pub_str[:10], "%Y-%m-%d").replace(tzinfo=CST)
                except Exception:
                    pub = datetime.now(CST)

            # 评级映射
            rating_raw = report.get("rating", "")
            rating = self._normalize_rating(rating_raw)

            # 目标价
            tp_str = report.get("minPrice", "")
            try:
                target_price = float(tp_str) if tp_str else None
            except Exception:
                target_price = None

            items.append(ResearchReport(
                title=report.get("title", "")[:200],
                institution=report.get("orgSName", ""),
                rating=rating,
                target_price=target_price,
                stock_name=report.get("stockName", ""),
                stock_code=report.get("stockCode", ""),
                summary=report.get("infoCode", "")[:300],
                source="东方财富研报中心",
                source_url=(
                    f"https://data.eastmoney.com/report/zw_stock.jshtml?"
                    f"infocode={report.get('infoCode', '')}"
                ),
                published_at=pub,
            ))
        return items

    # ── AKShare 研报接口 ────────────────────────────────────────────────

    def _fetch_akshare(self) -> list[ResearchReport]:
        try:
            import akshare as ak
            df = ak.stock_research_report_em()
            if df is None or df.empty:
                return []
            items = []
            for _, row in df.iterrows():
                pub_str = str(row.get("日期", ""))
                try:
                    pub = datetime.strptime(pub_str, "%Y-%m-%d").replace(tzinfo=CST)
                except Exception:
                    pub = datetime.now(CST)
                items.append(ResearchReport(
                    title=str(row.get("报告名称", ""))[:200],
                    institution=str(row.get("机构名称", "")),
                    rating=self._normalize_rating(str(row.get("评级", ""))),
                    target_price=None,
                    stock_name=str(row.get("股票简称", "")),
                    stock_code=str(row.get("股票代码", "")),
                    summary=str(row.get("报告名称", ""))[:300],
                    source="AKShare/东方财富研报",
                    source_url="https://data.eastmoney.com/report/",
                    published_at=pub,
                ))
            return items
        except ImportError:
            logger.debug("AKShare 未安装")
            return []
        except Exception as e:
            logger.debug(f"AKShare 研报接口失败: {e}")
            return []

    # ── 评级标准化 ─────────────────────────────────────────────────────

    @staticmethod
    def _normalize_rating(raw: str) -> str:
        mapping = {
            "买入": "买入", "强烈推荐": "买入", "强推": "买入",
            "推荐": "增持", "增持": "增持", "跑赢行业": "增持",
            "中性": "中性", "持有": "中性", "与大市持平": "中性",
            "减持": "减持", "低于行业": "减持",
            "卖出": "卖出", "回避": "卖出",
        }
        raw = raw.strip()
        return mapping.get(raw, raw or "未评级")
