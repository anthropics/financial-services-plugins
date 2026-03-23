"""
新闻与政策公告抓取器
数据源（全部免费/公开，可溯源）：
  1. 财联社电报 RSS          https://www.cls.cn/
  2. 新浪财经 RSS            https://finance.sina.com.cn/
  3. 东方财富 快讯 API       https://www.eastmoney.com/
  4. 新华社 RSS              http://www.xinhuanet.com/
  5. 人民日报 RSS            http://www.people.com.cn/
  6. 美联储公告              https://www.federalreserve.gov/feeds/
  7. 中国人民银行公告        http://www.pbc.gov.cn/
  8. 证监会公告              http://www.csrc.gov.cn/
  9. NewsAPI（可选）         https://newsapi.org/
  10. HKEX 公告              https://www.hkex.com.hk/
  11. Reuters 商业新闻 RSS   https://feeds.reuters.com/  ⚠️ 需美国网络
  12. CNBC 市场新闻 RSS      https://www.cnbc.com/        ⚠️ 需美国网络
  13. SEC EDGAR 8-K 公告     https://www.sec.gov/          ⚠️ 需美国网络
"""

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

CST = timezone(timedelta(hours=8))


@dataclass
class NewsItem:
    title: str
    summary: str
    source: str
    source_url: str
    published_at: datetime
    category: str          # policy / market / macro / company
    importance: str        # high / medium / low (pre-filled, overridden by AI)
    raw_content: str = ""

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "summary": self.summary,
            "source": self.source,
            "source_url": self.source_url,
            "published_at": self.published_at.isoformat(),
            "category": self.category,
            "importance": self.importance,
        }

    @property
    def dedup_key(self) -> str:
        return hashlib.md5(self.title.encode()).hexdigest()[:12]


class NewsFetcher:
    """聚合多路新闻源，去重后返回最近 N 小时的新闻"""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; MarketBriefBot/1.0; "
            "+https://github.com/anthropics/financial-services-plugins)"
        )
    }
    TIMEOUT = 15

    def __init__(self, cache_dir: str = "/tmp/market_cache", newsapi_key: str = ""):
        self.cache_dir = cache_dir
        self.newsapi_key = newsapi_key
        os.makedirs(cache_dir, exist_ok=True)
        self._seen_keys: set = set()

    # ── Public ────────────────────────────────────────────────────────

    def fetch_all(self, hours: int = 12) -> list[NewsItem]:
        """抓取过去 hours 小时的所有新闻，去重后返回"""
        cutoff = datetime.now(CST) - timedelta(hours=hours)
        all_items: list[NewsItem] = []

        sources = [
            self._fetch_cls_telegraph,
            self._fetch_eastmoney_news,
            self._fetch_sina_finance_rss,
            self._fetch_xinhua_rss,
            self._fetch_fed_rss,
            self._fetch_pbc_news,
            self._fetch_csrc_news,
            self._fetch_hkex_news,
            # 以下需美国网络（配置 HTTP_PROXY/HTTPS_PROXY 后生效，无代理时自动跳过）
            self._fetch_reuters_rss,
            self._fetch_cnbc_rss,
            self._fetch_sec_edgar_rss,
        ]
        if self.newsapi_key:
            sources.append(self._fetch_newsapi)

        for fetch_fn in sources:
            try:
                items = fetch_fn()
                for item in items:
                    if item.published_at >= cutoff and item.dedup_key not in self._seen_keys:
                        self._seen_keys.add(item.dedup_key)
                        all_items.append(item)
            except Exception as e:
                logger.warning(f"[{fetch_fn.__name__}] 抓取失败: {e}")

        all_items.sort(key=lambda x: x.published_at, reverse=True)
        logger.info(f"共抓取 {len(all_items)} 条新闻（{hours}h内）")
        return all_items

    # ── 财联社电报 ─────────────────────────────────────────────────────

    def _fetch_cls_telegraph(self) -> list[NewsItem]:
        """财联社实时电报 - 使用东方财富代理接口（免费）"""
        url = "https://www.cls.cn/nodeapi/updateTelegraphList"
        params = {"app": "CLS", "os": "web", "sv": "7.7.5", "rn": 40}
        r = requests.get(url, params=params, headers=self.HEADERS, timeout=self.TIMEOUT)
        data = r.json()
        items = []
        for item in data.get("data", {}).get("roll_data", []):
            ts = item.get("ctime", 0)
            pub = datetime.fromtimestamp(ts, tz=CST) if ts else datetime.now(CST)
            items.append(NewsItem(
                title=item.get("title", "")[:200],
                summary=item.get("content", "")[:500],
                source="财联社",
                source_url=f"https://www.cls.cn/detail/{item.get('id', '')}",
                published_at=pub,
                category=self._classify(item.get("content", "")),
                importance="medium",
                raw_content=item.get("content", ""),
            ))
        return items

    # ── 东方财富快讯 ───────────────────────────────────────────────────

    def _fetch_eastmoney_news(self) -> list[NewsItem]:
        """东方财富 7x24 快讯（免费 JSON 接口）"""
        url = "https://np-listapi.eastmoney.com/comm/web/getNPNewsList"
        params = {
            "client": "web",
            "type": 0,
            "mTypeAndId": "1:182,2:247,2:249,",
            "pageSize": 50,
            "pageIndex": 1,
        }
        r = requests.get(url, params=params, headers=self.HEADERS, timeout=self.TIMEOUT)
        data = r.json()
        items = []
        for article in data.get("data", {}).get("list", []):
            pub_str = article.get("ShowTime", "")
            try:
                pub = datetime.strptime(pub_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=CST)
            except Exception:
                pub = datetime.now(CST)
            items.append(NewsItem(
                title=article.get("Title", "")[:200],
                summary=article.get("Content", "")[:500],
                source="东方财富",
                source_url=article.get("NewsUrl", "https://www.eastmoney.com/"),
                published_at=pub,
                category=self._classify(article.get("Content", "")),
                importance="medium",
            ))
        return items

    # ── 新浪财经 RSS ───────────────────────────────────────────────────

    def _fetch_sina_finance_rss(self) -> list[NewsItem]:
        feeds = [
            ("https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&num=50&page=1", "新浪财经-宏观"),
            ("https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2521&num=50&page=1", "新浪财经-A股"),
        ]
        items = []
        for url, source_name in feeds:
            try:
                r = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
                data = r.json()
                for article in data.get("result", {}).get("data", []):
                    ts = int(article.get("ctime", 0))
                    pub = datetime.fromtimestamp(ts, tz=CST) if ts else datetime.now(CST)
                    items.append(NewsItem(
                        title=article.get("title", "")[:200],
                        summary=article.get("intro", "")[:500],
                        source=source_name,
                        source_url=article.get("url", "https://finance.sina.com.cn/"),
                        published_at=pub,
                        category=self._classify(article.get("intro", "")),
                        importance="medium",
                    ))
            except Exception as e:
                logger.debug(f"新浪财经 {url} 失败: {e}")
        return items

    # ── 新华社 RSS ──────────────────────────────────────────────────────

    def _fetch_xinhua_rss(self) -> list[NewsItem]:
        rss_urls = [
            "http://www.xinhuanet.com/politics/rss/zhengcijiedu.xml",
            "http://www.xinhuanet.com/fortune/rss/index.xml",
        ]
        items = []
        for url in rss_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:20]:
                    pub = self._parse_rss_date(entry)
                    items.append(NewsItem(
                        title=entry.get("title", "")[:200],
                        summary=entry.get("summary", "")[:500],
                        source="新华社",
                        source_url=entry.get("link", "http://www.xinhuanet.com/"),
                        published_at=pub,
                        category="policy",
                        importance="high",
                    ))
            except Exception as e:
                logger.debug(f"新华社 RSS {url} 失败: {e}")
        return items

    # ── 美联储公告 RSS ─────────────────────────────────────────────────

    def _fetch_fed_rss(self) -> list[NewsItem]:
        rss_url = "https://www.federalreserve.gov/feeds/press_monetary.xml"
        try:
            feed = feedparser.parse(rss_url)
            items = []
            for entry in feed.entries[:10]:
                pub = self._parse_rss_date(entry)
                items.append(NewsItem(
                    title=entry.get("title", "")[:200],
                    summary=entry.get("summary", "")[:500],
                    source="美联储",
                    source_url=entry.get("link", "https://www.federalreserve.gov/"),
                    published_at=pub,
                    category="policy",
                    importance="high",
                ))
            return items
        except Exception as e:
            logger.debug(f"美联储 RSS 失败: {e}")
            return []

    # ── 中国人民银行公告 ────────────────────────────────────────────────

    def _fetch_pbc_news(self) -> list[NewsItem]:
        """央行货币政策公告"""
        url = "http://www.pbc.gov.cn/rmyh/index.html"
        try:
            r = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            items = []
            for li in soup.select(".news_list li")[:10]:
                a = li.find("a")
                if not a:
                    continue
                title = a.get_text(strip=True)
                href = a.get("href", "")
                if href and not href.startswith("http"):
                    href = "http://www.pbc.gov.cn" + href
                span = li.find("span")
                date_str = span.get_text(strip=True) if span else ""
                try:
                    pub = datetime.strptime(date_str, "%Y-%m-%d").replace(
                        hour=9, tzinfo=CST
                    )
                except Exception:
                    pub = datetime.now(CST)
                items.append(NewsItem(
                    title=title[:200],
                    summary=title[:200],
                    source="中国人民银行",
                    source_url=href or "http://www.pbc.gov.cn/",
                    published_at=pub,
                    category="policy",
                    importance="high",
                ))
            return items
        except Exception as e:
            logger.debug(f"央行公告抓取失败: {e}")
            return []

    # ── 证监会公告 ────────────────────────────────────────────────────

    def _fetch_csrc_news(self) -> list[NewsItem]:
        url = "http://www.csrc.gov.cn/csrc/c100028/common_list.shtml"
        try:
            r = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            items = []
            for li in soup.select(".newslist li")[:10]:
                a = li.find("a")
                if not a:
                    continue
                title = a.get_text(strip=True)
                href = a.get("href", "")
                if href and not href.startswith("http"):
                    href = "http://www.csrc.gov.cn" + href
                span = li.find("span", class_="date")
                date_str = span.get_text(strip=True) if span else ""
                try:
                    pub = datetime.strptime(date_str, "%Y-%m-%d").replace(
                        hour=9, tzinfo=CST
                    )
                except Exception:
                    pub = datetime.now(CST)
                items.append(NewsItem(
                    title=title[:200],
                    summary=title[:200],
                    source="中国证监会",
                    source_url=href or "http://www.csrc.gov.cn/",
                    published_at=pub,
                    category="policy",
                    importance="high",
                ))
            return items
        except Exception as e:
            logger.debug(f"证监会公告抓取失败: {e}")
            return []

    # ── 港交所公告 ────────────────────────────────────────────────────

    def _fetch_hkex_news(self) -> list[NewsItem]:
        """港交所市场公告 RSS"""
        url = "https://www.hkex.com.hk/News/News-Release/News-Release-Listing?sc_lang=zh-HK"
        try:
            r = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            items = []
            for row in soup.select(".table-striped tr")[:15]:
                cols = row.find_all("td")
                if len(cols) < 2:
                    continue
                title = cols[0].get_text(strip=True)
                date_str = cols[-1].get_text(strip=True)
                a = cols[0].find("a")
                href = "https://www.hkex.com.hk" + a["href"] if a else "https://www.hkex.com.hk/"
                try:
                    pub = datetime.strptime(date_str, "%d/%m/%Y").replace(
                        hour=9, tzinfo=CST
                    )
                except Exception:
                    pub = datetime.now(CST)
                items.append(NewsItem(
                    title=title[:200],
                    summary=title[:200],
                    source="港交所",
                    source_url=href,
                    published_at=pub,
                    category="market",
                    importance="medium",
                ))
            return items
        except Exception as e:
            logger.debug(f"港交所公告抓取失败: {e}")
            return []

    # ── Reuters RSS（需美国网络）─────────────────────────────────────

    def _fetch_reuters_rss(self) -> list[NewsItem]:
        """Reuters 商业/市场新闻 RSS（需美国网络或代理）"""
        feeds = [
            ("https://feeds.reuters.com/reuters/businessNews", "Reuters-商业"),
            ("https://feeds.reuters.com/reuters/companyNews",  "Reuters-公司"),
        ]
        items = []
        for url, source_name in feeds:
            try:
                feed = feedparser.parse(url)
                if not feed.entries:
                    continue
                for entry in feed.entries[:15]:
                    pub = self._parse_rss_date(entry)
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    items.append(NewsItem(
                        title=title[:200],
                        summary=summary[:500],
                        source=source_name,
                        source_url=entry.get("link", "https://www.reuters.com/"),
                        published_at=pub,
                        category=self._classify(title + " " + summary),
                        importance="high",
                    ))
            except Exception as e:
                logger.debug(f"Reuters RSS {url} 失败（可能需要代理）: {e}")
        return items

    # ── CNBC RSS（需美国网络）────────────────────────────────────────

    def _fetch_cnbc_rss(self) -> list[NewsItem]:
        """CNBC 市场/经济新闻 RSS（需美国网络或代理）"""
        feeds = [
            ("https://www.cnbc.com/id/100003114/device/rss/rss.html", "CNBC-美股"),
            ("https://www.cnbc.com/id/20409666/device/rss/rss.html",  "CNBC-全球经济"),
        ]
        items = []
        for url, source_name in feeds:
            try:
                feed = feedparser.parse(url)
                if not feed.entries:
                    continue
                for entry in feed.entries[:15]:
                    pub = self._parse_rss_date(entry)
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    # 去掉 CNBC summary 中的 HTML 标签
                    if summary:
                        try:
                            summary = BeautifulSoup(summary, "html.parser").get_text()[:500]
                        except Exception:
                            summary = summary[:500]
                    items.append(NewsItem(
                        title=title[:200],
                        summary=summary,
                        source=source_name,
                        source_url=entry.get("link", "https://www.cnbc.com/"),
                        published_at=pub,
                        category=self._classify(title + " " + summary),
                        importance="medium",
                    ))
            except Exception as e:
                logger.debug(f"CNBC RSS {url} 失败（可能需要代理）: {e}")
        return items

    # ── SEC EDGAR 8-K 公告（需美国网络）─────────────────────────────

    def _fetch_sec_edgar_rss(self) -> list[NewsItem]:
        """SEC EDGAR 重大事件公告（8-K）RSS，仅抓头部大公司（需美国网络或代理）"""
        # 8-K = 重大事件披露，对市场影响最直接
        url = (
            "https://www.sec.gov/cgi-bin/browse-edgar"
            "?action=getcurrent&type=8-K&dateb=&owner=include&count=20&output=atom"
        )
        try:
            feed = feedparser.parse(url)
            items = []
            for entry in feed.entries[:10]:
                pub = self._parse_rss_date(entry)
                title = entry.get("title", "")
                items.append(NewsItem(
                    title=title[:200],
                    summary=entry.get("summary", title)[:500],
                    source="SEC EDGAR",
                    source_url=entry.get("link", "https://www.sec.gov/"),
                    published_at=pub,
                    category="company",
                    importance="high",
                ))
            return items
        except Exception as e:
            logger.debug(f"SEC EDGAR RSS 失败（可能需要代理）: {e}")
            return []

    # ── NewsAPI（可选增强）────────────────────────────────────────────

    def _fetch_newsapi(self) -> list[NewsItem]:
        if not self.newsapi_key:
            return []
        queries = [
            ("China economy policy", "macro"),
            ("Federal Reserve interest rate", "policy"),
            ("Hong Kong stock market", "market"),
        ]
        items = []
        for query, category in queries:
            try:
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": query,
                    "sortBy": "publishedAt",
                    "pageSize": 10,
                    "language": "en",
                    "apiKey": self.newsapi_key,
                }
                r = requests.get(url, params=params, headers=self.HEADERS, timeout=self.TIMEOUT)
                for article in r.json().get("articles", []):
                    pub_str = article.get("publishedAt", "")
                    try:
                        pub = datetime.fromisoformat(pub_str.replace("Z", "+00:00")).astimezone(CST)
                    except Exception:
                        pub = datetime.now(CST)
                    items.append(NewsItem(
                        title=article.get("title", "")[:200],
                        summary=article.get("description", "")[:500],
                        source=f"NewsAPI-{article.get('source', {}).get('name', 'Unknown')}",
                        source_url=article.get("url", "https://newsapi.org/"),
                        published_at=pub,
                        category=category,
                        importance="medium",
                    ))
            except Exception as e:
                logger.debug(f"NewsAPI {query} 失败: {e}")
        return items

    # ── 工具方法 ──────────────────────────────────────────────────────

    @staticmethod
    def _parse_rss_date(entry) -> datetime:
        import email.utils
        published = entry.get("published", "") or entry.get("updated", "")
        if published:
            try:
                tt = email.utils.parsedate_to_datetime(published)
                return tt.astimezone(CST)
            except Exception:
                pass
        return datetime.now(CST)

    @staticmethod
    def _classify(text: str) -> str:
        text = text.lower()
        if any(k in text for k in ["政策", "央行", "利率", "美联储", "监管", "法规", "规定"]):
            return "policy"
        if any(k in text for k in ["gdp", "cpi", "ppi", "就业", "通胀", "经济", "贸易"]):
            return "macro"
        if any(k in text for k in ["个股", "业绩", "财报", "并购", "增发", "回购"]):
            return "company"
        return "market"
