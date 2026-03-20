"""
规则引擎分析器 - 无需任何大模型
基于关键词匹配 + 模板生成，零API成本
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

logger = logging.getLogger(__name__)
CST = timezone(timedelta(hours=8))


@dataclass
class AnalysisResult:
    report_type: str
    generated_at: datetime
    market_summary: str
    key_events: list[dict]
    sector_outlook: list[dict]
    watchlist: list[dict]
    trading_strategy: str
    risk_warnings: list[str]
    review_of_yesterday: Optional[str]
    raw_response: str

    def to_dict(self) -> dict:
        return {
            "report_type": self.report_type,
            "generated_at": self.generated_at.isoformat(),
            "market_summary": self.market_summary,
            "key_events": self.key_events,
            "sector_outlook": self.sector_outlook,
            "watchlist": self.watchlist,
            "trading_strategy": self.trading_strategy,
            "risk_warnings": self.risk_warnings,
            "review_of_yesterday": self.review_of_yesterday,
        }


# ── 关键词 → 影响变量映射 ─────────────────────────────────────────────

KEYWORD_RULES = [
    # (关键词列表, 影响变量, 影响方向, 影响幅度, 受影响板块)
    # 利率相关
    (["加息", "升息", "利率上调", "鹰派", "缩表"], ["r"], "negative", "high", ["科技", "成长股", "房地产"]),
    (["降息", "降准", "利率下调", "鸽派", "扩表"], ["r", "L"], "positive", "high", ["科技", "成长股", "房地产"]),
    (["MLF", "逆回购", "公开市场操作"], ["L"], "neutral", "medium", ["金融", "银行"]),

    # 流动性相关
    (["放水", "宽松", "流动性充裕", "净投放"], ["L"], "positive", "medium", ["金融", "房地产"]),
    (["收紧", "流动性紧张", "净回笼", "钱荒"], ["L"], "negative", "medium", ["金融", "房地产"]),
    (["北向资金流入", "外资买入", "陆股通净买入"], ["L", "ρ"], "positive", "medium", ["消费", "金融"]),
    (["北向资金流出", "外资卖出", "陆股通净卖出"], ["L", "ρ"], "negative", "medium", ["消费", "金融"]),

    # 盈利预期相关
    (["业绩超预期", "盈利增长", "利润大增", "营收增长"], ["E"], "positive", "high", []),
    (["业绩下滑", "亏损", "利润下降", "营收下降", "业绩暴雷"], ["E"], "negative", "high", []),
    (["GDP增长", "经济复苏", "PMI回升", "制造业扩张"], ["E"], "positive", "medium", ["消费", "工业"]),
    (["GDP下降", "经济放缓", "PMI下降", "制造业收缩"], ["E"], "negative", "medium", ["消费", "工业"]),

    # 风险情绪相关
    (["VIX飙升", "恐慌", "暴跌", "崩盘", "黑天鹅", "战争", "冲突", "制裁"], ["ρ"], "negative", "high", []),
    (["VIX下降", "风险偏好回升", "大涨", "突破新高"], ["ρ"], "positive", "medium", []),

    # 行业政策
    (["芯片", "半导体", "光刻机", "集成电路", "国产替代"], ["E"], "positive", "medium", ["半导体", "科技"]),
    (["人工智能", "AI", "大模型", "ChatGPT", "算力", "GPU"], ["E"], "positive", "high", ["人工智能", "科技"]),
    (["新能源", "光伏", "风电", "储能", "碳中和"], ["E"], "positive", "medium", ["新能源"]),
    (["电动车", "新能源车", "动力电池", "充电桩"], ["E"], "positive", "medium", ["新能源", "汽车"]),
    (["医药", "创新药", "医疗器械", "集采"], ["E"], "neutral", "medium", ["医药"]),
    (["消费升级", "零售数据", "社零"], ["E"], "positive", "medium", ["消费"]),
    (["房地产调控", "限购", "限贷"], ["E", "L"], "negative", "medium", ["房地产"]),
    (["房地产松绑", "取消限购", "降低首付"], ["E", "L"], "positive", "medium", ["房地产"]),
    (["军工", "国防", "军事", "军费"], ["E"], "positive", "medium", ["军工"]),
    (["金融监管", "反垄断", "罚款"], ["E", "ρ"], "negative", "medium", ["金融", "互联网"]),
]

# ── 板块关键词映射 ───────────────────────────────────────────────────

SECTOR_KEYWORDS = {
    "科技": ["科技", "互联网", "软件", "云计算", "SaaS", "数字经济"],
    "半导体": ["芯片", "半导体", "光刻机", "集成电路", "封装", "晶圆"],
    "人工智能": ["AI", "人工智能", "大模型", "算力", "GPU", "机器人"],
    "新能源": ["新能源", "光伏", "风电", "储能", "氢能", "碳中和", "电动车", "动力电池"],
    "消费": ["消费", "零售", "白酒", "食品", "旅游", "免税"],
    "医药": ["医药", "创新药", "医疗", "生物", "疫苗", "集采"],
    "金融": ["银行", "保险", "券商", "金融", "信贷"],
    "房地产": ["房地产", "地产", "楼市", "房价", "限购"],
    "军工": ["军工", "国防", "军事", "航天", "军费"],
}


class RuleAnalyzer:
    """基于规则的市场分析引擎，零API成本"""

    def analyze_premarket(
        self,
        market_type: str,
        news_items: list,
        market_data: dict,
        research_reports: list,
        economic_events: list,
        focus_sectors: list[str],
        watchlist: list[str],
        yesterday_strategy: Optional[str] = None,
    ) -> AnalysisResult:
        """生成开盘前分析报告"""
        report_type = f"premarket_{market_type}"
        market_label = "A股+港股" if market_type == "asia" else "美股"

        # 1. 分析新闻事件
        key_events = self._analyze_news(news_items)

        # 2. 生成板块展望
        sector_outlook = self._generate_sector_outlook(
            news_items, market_data, research_reports, focus_sectors
        )

        # 3. 生成关注标的
        watchlist_items = self._generate_watchlist(
            research_reports, watchlist, market_type
        )

        # 4. 生成市场摘要
        market_summary = self._generate_summary(
            market_data, key_events, market_label
        )

        # 5. 生成操作建议
        trading_strategy = self._generate_strategy(
            key_events, sector_outlook, market_data, economic_events, market_label
        )

        # 6. 风险提示
        risk_warnings = self._generate_risks(
            news_items, economic_events, market_data
        )

        return AnalysisResult(
            report_type=report_type,
            generated_at=datetime.now(CST),
            market_summary=market_summary,
            key_events=key_events[:5],
            sector_outlook=sector_outlook[:6],
            watchlist=watchlist_items[:8],
            trading_strategy=trading_strategy,
            risk_warnings=risk_warnings[:5],
            review_of_yesterday=None,
            raw_response="rule-based",
        )

    def analyze_postmarket(
        self,
        market_type: str,
        market_data: dict,
        news_items: list,
        morning_strategy: Optional[str] = None,
        focus_sectors: list[str] = None,
    ) -> AnalysisResult:
        """生成收盘复盘报告"""
        market_label = {"cn": "A股", "hk": "港股", "us": "美股", "asia": "A股+港股"}.get(
            market_type, market_type
        )

        key_events = self._analyze_news(news_items)
        sector_outlook = self._generate_sector_outlook(
            news_items, market_data, [], focus_sectors or []
        )
        market_summary = self._generate_postmarket_summary(market_data, market_label)
        trading_strategy = self._generate_strategy(
            key_events, sector_outlook, market_data, [], f"明日{market_label}"
        )
        risk_warnings = self._generate_risks(news_items, [], market_data)

        review = None
        if morning_strategy:
            review = f"今日开盘前建议：{morning_strategy[:200]}。请结合实际走势自行评估。"

        return AnalysisResult(
            report_type="postmarket",
            generated_at=datetime.now(CST),
            market_summary=market_summary,
            key_events=key_events[:4],
            sector_outlook=sector_outlook[:6],
            watchlist=[],
            trading_strategy=trading_strategy,
            risk_warnings=risk_warnings[:3],
            review_of_yesterday=review,
            raw_response="rule-based",
        )

    # ── 新闻分析 ─────────────────────────────────────────────────────

    def _analyze_news(self, news_items: list) -> list[dict]:
        """对新闻进行关键词匹配分析"""
        analyzed = []
        seen_titles = set()

        for item in news_items:
            item_dict = item.to_dict() if hasattr(item, "to_dict") else item
            title = item_dict.get("title", "")
            summary = item_dict.get("summary", "")
            text = f"{title} {summary}"

            if title in seen_titles:
                continue
            seen_titles.add(title)

            match = self._match_keywords(text)
            if not match:
                continue

            variables, direction, magnitude, sectors = match
            transmission = self._build_transmission(title, variables, sectors)

            analyzed.append({
                "title": title,
                "source": item_dict.get("source", ""),
                "source_url": item_dict.get("source_url", ""),
                "impact_variables": variables,
                "impact_direction": direction,
                "impact_magnitude": magnitude,
                "transmission_chain": transmission,
                "affected_sectors": sectors,
                "affected_stocks": [],
                "time_horizon": "short",
            })

        # 按影响幅度排序: high > medium > low
        mag_order = {"high": 0, "medium": 1, "low": 2}
        analyzed.sort(key=lambda x: mag_order.get(x["impact_magnitude"], 2))
        return analyzed

    def _match_keywords(self, text: str) -> Optional[tuple]:
        """匹配文本中的关键词，返回 (变量, 方向, 幅度, 板块)"""
        best_match = None
        best_priority = 999

        for keywords, variables, direction, magnitude, sectors in KEYWORD_RULES:
            for kw in keywords:
                if kw in text:
                    priority = {"high": 0, "medium": 1, "low": 2}.get(magnitude, 2)
                    if priority < best_priority:
                        best_priority = priority
                        best_match = (variables, direction, magnitude, sectors)
                    break

        return best_match

    def _build_transmission(self, title: str, variables: list, sectors: list) -> str:
        """生成传导链条描述"""
        var_names = {"E": "盈利预期", "r": "利率", "L": "流动性", "ρ": "风险情绪"}
        var_str = "/".join(var_names.get(v, v) for v in variables)
        sector_str = "、".join(sectors[:3]) if sectors else "市场整体"
        return f"{title[:30]} → {var_str}变动 → 影响{sector_str}"

    # ── 板块展望 ─────────────────────────────────────────────────────

    def _generate_sector_outlook(
        self, news_items, market_data, research_reports, focus_sectors
    ) -> list[dict]:
        """基于新闻频次和研报生成板块展望"""
        sector_signals = {}

        # 统计各板块新闻提及次数和方向
        for item in news_items:
            item_dict = item.to_dict() if hasattr(item, "to_dict") else item
            text = f"{item_dict.get('title', '')} {item_dict.get('summary', '')}"

            for sector, keywords in SECTOR_KEYWORDS.items():
                if sector not in focus_sectors:
                    continue
                for kw in keywords:
                    if kw in text:
                        if sector not in sector_signals:
                            sector_signals[sector] = {"positive": 0, "negative": 0, "drivers": []}
                        match = self._match_keywords(text)
                        if match:
                            _, direction, _, _ = match
                            if direction == "positive":
                                sector_signals[sector]["positive"] += 1
                            elif direction == "negative":
                                sector_signals[sector]["negative"] += 1
                            sector_signals[sector]["drivers"].append(
                                item_dict.get("title", "")[:40]
                            )
                        break

        # 从研报中提取板块信号
        for report in research_reports:
            r = report.to_dict() if hasattr(report, "to_dict") else report
            rating = r.get("rating", "")
            stock_name = r.get("stock_name", "")
            for sector, keywords in SECTOR_KEYWORDS.items():
                if sector not in focus_sectors:
                    continue
                for kw in keywords:
                    if kw in stock_name or kw in r.get("title", ""):
                        if sector not in sector_signals:
                            sector_signals[sector] = {"positive": 0, "negative": 0, "drivers": []}
                        if "买入" in rating or "增持" in rating or "推荐" in rating:
                            sector_signals[sector]["positive"] += 1
                        elif "卖出" in rating or "减持" in rating:
                            sector_signals[sector]["negative"] += 1
                        break

        # 生成板块展望列表
        outlook = []
        for sector in focus_sectors:
            if sector not in sector_signals:
                outlook.append({
                    "sector": sector,
                    "direction": "neutral",
                    "key_driver": "暂无显著驱动事件",
                    "top_picks": [],
                })
                continue

            sig = sector_signals[sector]
            if sig["positive"] > sig["negative"] + 1:
                direction = "bullish"
            elif sig["negative"] > sig["positive"] + 1:
                direction = "bearish"
            else:
                direction = "neutral"

            # 取最新的驱动因素
            drivers = sig["drivers"][:3]
            driver_text = "；".join(dict.fromkeys(drivers)) if drivers else "综合信号"

            # 从研报中提取top picks
            top_picks = []
            for report in research_reports:
                r = report.to_dict() if hasattr(report, "to_dict") else report
                for kw in SECTOR_KEYWORDS.get(sector, []):
                    if kw in r.get("stock_name", "") or kw in r.get("title", ""):
                        code = r.get("stock_code", "")
                        name = r.get("stock_name", "")
                        if name and name not in top_picks:
                            top_picks.append(f"{name}({code})" if code else name)
                        break
                if len(top_picks) >= 3:
                    break

            outlook.append({
                "sector": sector,
                "direction": direction,
                "key_driver": driver_text[:80],
                "top_picks": top_picks,
            })

        # 有信号的板块排前面
        outlook.sort(key=lambda x: 0 if x["direction"] != "neutral" else 1)
        return outlook

    # ── 关注标的 ─────────────────────────────────────────────────────

    def _generate_watchlist(
        self, research_reports, watchlist_codes, market_type
    ) -> list[dict]:
        """从研报中提取关注标的"""
        items = []

        for report in research_reports:
            r = report.to_dict() if hasattr(report, "to_dict") else report
            code = r.get("stock_code", "")
            name = r.get("stock_name", "")
            rating = r.get("rating", "")
            institution = r.get("institution", "")
            target_price = r.get("target_price")

            if not code or not name:
                continue

            # 判断市场
            if code.startswith(("6", "0", "3")):
                market = "A股"
            elif code.startswith("0") and len(code) == 5:
                market = "港股"
            else:
                market = "美股" if code.isalpha() else "A股"

            # 操作建议映射
            if "买入" in rating or "推荐" in rating or "增持" in rating:
                action = "关注买入"
            elif "卖出" in rating or "减持" in rating:
                action = "关注卖出"
            else:
                action = "观望"

            tp_str = f"¥{target_price}" if target_price else "-"

            items.append({
                "code": code,
                "name": name,
                "market": market,
                "action": action,
                "price_target": tp_str,
                "rationale": f"{institution}评级{rating}",
                "catalyst": r.get("title", "")[:40],
                "risk": "研报观点仅供参考",
            })

            if len(items) >= 8:
                break

        return items

    # ── 市场摘要 ─────────────────────────────────────────────────────

    def _generate_summary(self, market_data, key_events, market_label) -> str:
        """根据市场数据生成一句话摘要"""
        parts = []

        # 提取指数涨跌幅
        for market_key, label in [("cn", "沪指"), ("hk", "恒指"), ("us", "标普500"),
                                   ("us_overnight", "标普500")]:
            data = market_data.get(market_key, {})
            if not data:
                continue
            indices = data.get("indices", {})
            for idx_name, idx_data in indices.items():
                if isinstance(idx_data, dict):
                    change_pct = idx_data.get("change_pct")
                    if change_pct is not None:
                        direction = "涨" if change_pct > 0 else "跌"
                        parts.append(f"{idx_name}{direction}{abs(change_pct):.2f}%")
                        break

        if parts:
            return f"{market_label}盘前：{'; '.join(parts[:4])}。" + (
                f"今日有{len(key_events)}条重要事件值得关注。" if key_events else ""
            )
        return f"{market_label}盘前概览：数据采集中，请关注各项指标变化。"

    def _generate_postmarket_summary(self, market_data, market_label) -> str:
        """收盘复盘摘要"""
        parts = []
        for market_key in ["cn", "hk", "us"]:
            data = market_data.get(market_key, {})
            if not data:
                continue
            indices = data.get("indices", {})
            for idx_name, idx_data in indices.items():
                if isinstance(idx_data, dict):
                    change_pct = idx_data.get("change_pct")
                    if change_pct is not None:
                        direction = "涨" if change_pct > 0 else "跌"
                        parts.append(f"{idx_name}{direction}{abs(change_pct):.2f}%")
                        break

        if parts:
            return f"{market_label}收盘：{'; '.join(parts[:4])}。"
        return f"{market_label}收盘数据采集中。"

    # ── 操作建议 ─────────────────────────────────────────────────────

    def _generate_strategy(
        self, key_events, sector_outlook, market_data, economic_events, market_label
    ) -> str:
        """基于信号强度生成模板化操作建议"""
        positive_count = sum(
            1 for e in key_events if e.get("impact_direction") == "positive"
        )
        negative_count = sum(
            1 for e in key_events if e.get("impact_direction") == "negative"
        )
        high_impact = sum(
            1 for e in key_events if e.get("impact_magnitude") == "high"
        )

        bullish_sectors = [s["sector"] for s in sector_outlook if s["direction"] == "bullish"]
        bearish_sectors = [s["sector"] for s in sector_outlook if s["direction"] == "bearish"]

        parts = []

        # 整体判断
        if positive_count > negative_count + 2:
            parts.append(f"{market_label}多头信号偏多，市场情绪偏暖。")
        elif negative_count > positive_count + 2:
            parts.append(f"{market_label}空头信号偏多，建议谨慎操作。")
        else:
            parts.append(f"{market_label}多空信号交织，建议以观望为主。")

        # 板块建议
        if bullish_sectors:
            parts.append(f"偏多板块：{'、'.join(bullish_sectors[:3])}，可适当关注。")
        if bearish_sectors:
            parts.append(f"偏空板块：{'、'.join(bearish_sectors[:3])}，注意规避。")

        # 经济事件提醒
        high_events = [
            e for e in (economic_events or [])
            if (e.to_dict() if hasattr(e, "to_dict") else e).get("importance") == "high"
        ]
        if high_events:
            ev = (high_events[0].to_dict() if hasattr(high_events[0], "to_dict") else high_events[0])
            parts.append(f"近期关注：{ev.get('name', '')}数据公布，可能引发波动。")

        # 风险等级
        if high_impact >= 2:
            parts.append("今日高影响事件较多，建议控制仓位，避免追涨杀跌。")

        return "".join(parts)[:300]

    # ── 风险提示 ─────────────────────────────────────────────────────

    def _generate_risks(self, news_items, economic_events, market_data) -> list[str]:
        """从新闻中提取风险相关内容"""
        risks = []
        risk_keywords = [
            "暴跌", "崩盘", "黑天鹅", "战争", "冲突", "制裁", "违约",
            "爆雷", "退市", "跌停", "熔断", "危机", "衰退",
        ]

        seen = set()
        for item in news_items:
            item_dict = item.to_dict() if hasattr(item, "to_dict") else item
            title = item_dict.get("title", "")
            for kw in risk_keywords:
                if kw in title and kw not in seen:
                    risks.append(f"{title[:50]}（来源：{item_dict.get('source', '')}）")
                    seen.add(kw)
                    break
            if len(risks) >= 3:
                break

        # 默认风险提示
        if not risks:
            risks.append("市场存在不确定性，投资需谨慎")

        risks.append("本报告基于公开数据自动生成，不构成投资建议")
        return risks
