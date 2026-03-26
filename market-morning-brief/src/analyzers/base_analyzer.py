"""
分析引擎基类
- 定义 AnalysisResult 数据结构
- 定义第一性原则分析框架的系统提示
- 封装 Prompt 构建和 JSON 解析逻辑（所有 LLM 通用）
- 子类只需实现 _call_api() 和 answer_question()
"""

import json
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


FIRST_PRINCIPLES_SYSTEM_PROMPT = """你是一名专业的金融分析师，具备以下核心能力：

【第一性原则分析框架】
市场价格由4个核心变量决定：
1. **盈利预期（E）**：企业/经济体未来盈利能力
2. **无风险利率（r）**：美联储/央行政策利率影响折现率
3. **流动性（L）**：货币供给、信贷条件、市场资金面
4. **风险情绪（ρ）**：VIX、北向资金、两融余额等情绪指标

对每条新闻/事件，必须回答：
- 它影响了哪个核心变量？（E/r/L/ρ，可多选）
- 影响方向（正/负）和幅度（高/中/低）
- 传导链条（1→2→3步）
- 受影响的板块和个股

【分析原则】
- 数据必须有来源（新闻标题+媒体名）
- 区分短期冲击（<1周）和中期趋势（1-3个月）
- 给出具体的操作建议：涨/跌/观望，以及价格区间
- 明确指出不确定性和尾部风险

【输出格式】
必须严格返回合法的 JSON 格式（下方定义）。不要在 JSON 外添加任何 markdown 代码块标记。

JSON Schema:
{
  "market_summary": "string（不超过100字）",
  "key_events": [
    {
      "title": "事件标题",
      "source": "数据来源",
      "source_url": "URL",
      "impact_variables": ["E", "r", "L", "ρ"],
      "impact_direction": "positive|negative|neutral",
      "impact_magnitude": "high|medium|low",
      "transmission_chain": "string（传导链条描述）",
      "affected_sectors": ["string"],
      "affected_stocks": [{"code": "string", "name": "string", "reason": "string"}],
      "time_horizon": "short|medium|long"
    }
  ],
  "sector_outlook": [
    {
      "sector": "板块名",
      "direction": "bullish|bearish|neutral",
      "key_driver": "string",
      "top_picks": ["股票代码/名称"]
    }
  ],
  "watchlist": [
    {
      "code": "string",
      "name": "string",
      "market": "A股|港股|美股",
      "action": "关注买入|关注卖出|观望",
      "price_target": "string（价格区间或空）",
      "rationale": "string（50字以内，基于第一性原则）",
      "catalyst": "string（触发因素）",
      "risk": "string（主要风险）"
    }
  ],
  "trading_strategy": "string（300字以内的整体操作建议）",
  "risk_warnings": ["string"]
}"""

QA_SYSTEM_PROMPT = """你是一位专业的金融分析师，专注于A股、港股和美股市场分析。

分析框架：基于第一性原则，将市场价格拆解为 P = f(E × r / L × ρ)：
- E（盈利预期）：企业未来盈利能力
- r（利率）：无风险利率 → 折现因子
- L（流动性）：货币供应、信贷、资金流向
- ρ（风险情绪）：VIX、北向资金、市场情绪

回答要求：
1. 直接回答问题，结论在前
2. 说明影响的变量（E/r/L/ρ）及传导链条
3. 指出受影响的行业/板块
4. 给出具体操作建议（买入/观望/回避）
5. 回答控制在 300 字以内，简明精准
6. 最后注明：本分析仅供参考，不构成投资建议"""


class BaseAnalyzer:
    """所有 LLM 分析引擎的基类，封装 Prompt 构建和结果解析"""

    # ── 主入口（子类无需覆盖）──────────────────────────────────────────

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
        prompt = self._build_premarket_prompt(
            market_type, news_items, market_data, research_reports,
            economic_events, focus_sectors, watchlist, yesterday_strategy,
        )
        return self._call_api(prompt, f"premarket_{market_type}")

    def analyze_postmarket(
        self,
        market_type: str,
        market_data: dict,
        news_items: list,
        morning_strategy: Optional[str] = None,
        focus_sectors: list[str] = None,
    ) -> AnalysisResult:
        prompt = self._build_postmarket_prompt(
            market_type, market_data, news_items, morning_strategy, focus_sectors or []
        )
        return self._call_api(prompt, "postmarket")

    # ── 子类必须实现 ───────────────────────────────────────────────────

    def _call_api(self, prompt: str, report_type: str) -> AnalysisResult:
        raise NotImplementedError

    def answer_question(self, question: str, context: str) -> str:
        """回答单个金融问题（用于 Q&A 机器人），子类实现"""
        raise NotImplementedError

    # ── Prompt 构建（所有 LLM 共用）───────────────────────────────────

    def _build_premarket_prompt(
        self, market_type, news_items, market_data, research_reports,
        economic_events, focus_sectors, watchlist, yesterday_strategy,
    ) -> str:
        now_str = datetime.now(CST).strftime("%Y-%m-%d %H:%M CST")
        market_label = "A股+港股" if market_type == "asia" else "美股"

        parts = [
            f"【{market_label}开盘前分析】 生成时间：{now_str}",
            f"重点关注板块：{', '.join(focus_sectors)}",
            f"自选标的：{', '.join(watchlist) if watchlist else '无'}",
            "",
        ]

        parts.append("=== 最新市场数据 ===")
        if market_data:
            parts.append(json.dumps(market_data, ensure_ascii=False, indent=2))

        if economic_events:
            parts.append("\n=== 近期重要经济事件（含时间表）===")
            for ev in economic_events[:15]:
                ev_dict = ev.to_dict() if hasattr(ev, "to_dict") else ev
                importance_label = "🔴" if ev_dict.get("importance") == "high" else "🟡"
                parts.append(
                    f"{importance_label} {ev_dict.get('name')} | "
                    f"{ev_dict.get('country')} | "
                    f"{ev_dict.get('scheduled_at', '')[:16]} | "
                    f"预期: {ev_dict.get('forecast', 'N/A')} | "
                    f"前值: {ev_dict.get('previous', 'N/A')} | "
                    f"实际: {ev_dict.get('actual', '待公布')} | "
                    f"来源: {ev_dict.get('source')}"
                )

        parts.append("\n=== 市场关键新闻（过去12小时）===")
        categorized = {"policy": [], "macro": [], "market": [], "company": []}
        for item in news_items:
            item_dict = item.to_dict() if hasattr(item, "to_dict") else item
            cat = item_dict.get("category", "market")
            if cat in categorized:
                categorized[cat].append(item_dict)

        cat_labels = {"policy": "政策监管", "macro": "宏观经济", "market": "市场动态", "company": "公司事件"}
        for cat, label in cat_labels.items():
            items_in_cat = categorized[cat][:8]
            if items_in_cat:
                parts.append(f"\n--- {label} ---")
                for item in items_in_cat:
                    parts.append(
                        f"• [{item.get('source')}] {item.get('title')} "
                        f"({item.get('published_at', '')[:16]}) "
                        f"链接: {item.get('source_url')}"
                    )
                    if item.get("summary"):
                        parts.append(f"  摘要: {item.get('summary')[:150]}")

        if research_reports:
            parts.append("\n=== 机构研报摘要（近24小时）===")
            for report in research_reports[:12]:
                r = report.to_dict() if hasattr(report, "to_dict") else report
                tp_str = f"目标价 ¥{r.get('target_price')}" if r.get("target_price") else ""
                parts.append(
                    f"• [{r.get('institution')}] {r.get('stock_name')}({r.get('stock_code')}) "
                    f"评级:{r.get('rating')} {tp_str} | {r.get('title')} "
                    f"| 来源: {r.get('source_url')}"
                )

        if yesterday_strategy:
            parts.append(f"\n=== 昨日操作建议（供参考对比）===\n{yesterday_strategy}")

        parts.append(
            "\n请基于上述数据，运用第一性原则框架，生成今日开盘前分析报告。"
            "所有结论必须有数据来源支撑。严格按照系统提示中定义的 JSON 格式输出。"
        )
        return "\n".join(parts)

    def _build_postmarket_prompt(
        self, market_type, market_data, news_items, morning_strategy, focus_sectors,
    ) -> str:
        now_str = datetime.now(CST).strftime("%Y-%m-%d %H:%M CST")
        market_label = {"cn": "A股", "hk": "港股", "us": "美股", "asia": "A股+港股"}.get(
            market_type, market_type
        )

        parts = [f"【{market_label}收盘复盘】 生成时间：{now_str}", ""]
        parts.append("=== 今日收盘数据 ===")
        parts.append(json.dumps(market_data, ensure_ascii=False, indent=2))

        if news_items:
            parts.append("\n=== 今日重要新闻 ===")
            for item in news_items[:20]:
                item_dict = item.to_dict() if hasattr(item, "to_dict") else item
                parts.append(
                    f"• [{item_dict.get('source')}] {item_dict.get('title')} "
                    f"({item_dict.get('published_at', '')[:16]}) "
                    f"链接: {item_dict.get('source_url')}"
                )

        if morning_strategy:
            parts.append(f"\n=== 今日开盘前操作建议（复盘对比）===\n{morning_strategy}")

        parts.append(
            "\n请对今日市场进行全面复盘："
            "1) 市场今日走势是否符合第一性原则预期？"
            "2) 今日建议是否正确？原因是什么？"
            "3) 明日需要重点关注哪些变量？"
            "4) 给出明日操作建议。"
            "严格按照系统提示中定义的 JSON 格式输出，review_of_yesterday 字段填写对今日建议的回顾。"
        )
        return "\n".join(parts)

    # ── 结果解析（所有 LLM 共用）──────────────────────────────────────

    def _parse_result(self, raw: str, report_type: str) -> AnalysisResult:
        data = self._extract_json(raw)
        return AnalysisResult(
            report_type=report_type,
            generated_at=datetime.now(CST),
            market_summary=data.get("market_summary", ""),
            key_events=data.get("key_events", []),
            sector_outlook=data.get("sector_outlook", []),
            watchlist=data.get("watchlist", []),
            trading_strategy=data.get("trading_strategy", ""),
            risk_warnings=data.get("risk_warnings", []),
            review_of_yesterday=data.get("review_of_yesterday"),
            raw_response=raw,
        )

    @staticmethod
    def _extract_json(text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        logger.warning("无法解析 LLM 返回的 JSON，返回原始文本")
        return {"market_summary": text[:200], "raw": text}
