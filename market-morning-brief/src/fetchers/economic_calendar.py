"""
经济日历抓取器
数据源（免费/公开）：
  - AKShare macro 接口     ak.macro_china_cpi_yearly() 等
  - Investing.com 经济日历  https://cn.investing.com/economic-calendar/
  - 美联储 FRED             https://fred.stlouisfed.org/
  - 财联社财经日历          https://www.cls.cn/
"""

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import requests

logger = logging.getLogger(__name__)
CST = timezone(timedelta(hours=8))
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MarketBriefBot/1.0)"}


@dataclass
class EconomicEvent:
    name: str               # 事件名称
    country: str            # CN / US / EU / JP / HK
    scheduled_at: datetime  # 发布时间
    period: str             # 统计期（如 "2024年12月"）
    forecast: Optional[str] # 预期值
    previous: Optional[str] # 前值
    actual: Optional[str]   # 实际值（已公布）
    importance: str         # high / medium / low
    source: str
    source_url: str

    @property
    def is_released(self) -> bool:
        return self.actual is not None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "country": self.country,
            "scheduled_at": self.scheduled_at.isoformat(),
            "period": self.period,
            "forecast": self.forecast,
            "previous": self.previous,
            "actual": self.actual,
            "importance": self.importance,
            "is_released": self.is_released,
            "source": self.source,
            "source_url": self.source_url,
        }


class EconomicCalendarFetcher:
    """抓取未来 3 天及昨天的重要经济事件"""

    def fetch_upcoming(self, days_ahead: int = 3) -> list[EconomicEvent]:
        events = []
        today = datetime.now(CST).date()

        for fetch_fn in [self._fetch_akshare_macro, self._fetch_investing_calendar]:
            try:
                items = fetch_fn(today, days_ahead)
                events.extend(items)
            except Exception as e:
                logger.warning(f"[{fetch_fn.__name__}] 经济日历抓取失败: {e}")

        # 按时间排序，去重
        seen = set()
        unique = []
        for ev in sorted(events, key=lambda x: x.scheduled_at):
            key = f"{ev.name}_{ev.scheduled_at.date()}"
            if key not in seen:
                seen.add(key)
                unique.append(ev)

        logger.info(f"共获取 {len(unique)} 条经济事件")
        return unique

    # ── AKShare 宏观数据 ───────────────────────────────────────────────

    def _fetch_akshare_macro(self, today: date, days_ahead: int) -> list[EconomicEvent]:
        """从 AKShare 获取最新宏观数据发布信息"""
        try:
            import akshare as ak
        except ImportError:
            return []

        events = []
        now_cst = datetime.now(CST)

        # 中国 CPI / PPI
        macro_tasks = [
            ("中国CPI同比", "CN", "high", lambda: ak.macro_china_cpi_yearly()),
            ("中国PPI同比", "CN", "high", lambda: ak.macro_china_ppi_yearly()),
            ("中国PMI制造业", "CN", "high", lambda: ak.macro_china_pmi()),
            ("中国社会消费品零售", "CN", "medium", lambda: ak.macro_china_retail_sales()),
            ("美国CPI同比", "US", "high", lambda: ak.macro_usa_cpi_monthly()),
            ("美国非农就业", "US", "high", lambda: ak.macro_usa_non_farm()),
            ("美国GDP", "US", "high", lambda: ak.macro_usa_gdp()),
            ("美联储利率决议", "US", "high", lambda: ak.macro_usa_interest_rate()),
        ]

        for name, country, importance, fetch_fn in macro_tasks:
            try:
                df = fetch_fn()
                if df is not None and len(df) > 0:
                    latest = df.iloc[-1]
                    # 估算发布时间（取最新数据期对应月份）
                    date_col = [c for c in df.columns if "日期" in c or "date" in c.lower()]
                    if date_col:
                        raw_date = str(latest[date_col[0]])
                        try:
                            pub_date = datetime.strptime(raw_date[:10], "%Y-%m-%d").replace(tzinfo=CST)
                        except Exception:
                            pub_date = now_cst
                    else:
                        pub_date = now_cst

                    # 值列
                    val_cols = [c for c in df.columns if c not in date_col]
                    actual = str(latest[val_cols[0]]) if val_cols else None
                    previous = str(df.iloc[-2][val_cols[0]]) if len(df) > 1 and val_cols else None

                    events.append(EconomicEvent(
                        name=name,
                        country=country,
                        scheduled_at=pub_date,
                        period=raw_date[:7] if date_col else "",
                        forecast=None,
                        previous=previous,
                        actual=actual,
                        importance=importance,
                        source="AKShare/国家统计局",
                        source_url="https://data.stats.gov.cn/",
                    ))
            except Exception as e:
                logger.debug(f"AKShare {name} 失败: {e}")

        return events

    # ── Investing.com 经济日历 ─────────────────────────────────────────

    def _fetch_investing_calendar(self, today: date, days_ahead: int) -> list[EconomicEvent]:
        """
        Investing.com 经济日历 API（非官方，公开可用）
        数据溯源: https://cn.investing.com/economic-calendar/
        """
        events = []
        try:
            end_date = today + timedelta(days=days_ahead)
            url = "https://sbcharts.investing.com/events_charts/us/calendar_1.json"
            r = requests.get(url, headers=HEADERS, timeout=15)
            data = r.json()

            importance_map = {1: "low", 2: "medium", 3: "high"}
            country_map = {
                "美国": "US", "中国": "CN", "欧盟": "EU",
                "日本": "JP", "英国": "UK", "澳大利亚": "AU",
            }

            for item in data.get("data", []):
                try:
                    ts = item.get("timestamp")
                    if not ts:
                        continue
                    ev_date = datetime.fromtimestamp(ts, tz=CST)
                    if not (today <= ev_date.date() <= end_date):
                        continue

                    country_raw = item.get("country", "")
                    country = country_map.get(country_raw, country_raw[:2].upper())
                    importance_raw = item.get("importance", 1)
                    importance = importance_map.get(int(importance_raw), "low")

                    events.append(EconomicEvent(
                        name=item.get("event", ""),
                        country=country,
                        scheduled_at=ev_date,
                        period=item.get("period", ""),
                        forecast=item.get("forecast"),
                        previous=item.get("previous"),
                        actual=item.get("actual"),
                        importance=importance,
                        source="Investing.com经济日历",
                        source_url="https://cn.investing.com/economic-calendar/",
                    ))
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"Investing.com 日历抓取失败: {e}")

        # 备用：财联社财经日历
        if not events:
            events = self._fetch_cls_calendar(today, days_ahead)

        return events

    def _fetch_cls_calendar(self, today: date, days_ahead: int) -> list[EconomicEvent]:
        """财联社财经日历（备用）"""
        events = []
        try:
            url = "https://www.cls.cn/api/schedule"
            params = {
                "date": today.strftime("%Y-%m-%d"),
                "days": days_ahead + 1,
            }
            r = requests.get(url, params=params, headers=HEADERS, timeout=10)
            data = r.json()
            for item in data.get("data", []):
                title = item.get("title", "")
                date_str = item.get("date", "")
                try:
                    ev_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=CST)
                except Exception:
                    ev_date = datetime.now(CST)
                events.append(EconomicEvent(
                    name=title,
                    country="CN",
                    scheduled_at=ev_date,
                    period="",
                    forecast=None, previous=None, actual=None,
                    importance="medium",
                    source="财联社财经日历",
                    source_url="https://www.cls.cn/",
                ))
        except Exception as e:
            logger.debug(f"财联社日历失败: {e}")
        return events
