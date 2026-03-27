#!/usr/bin/env python3
"""
市场晨报/晚报系统 - 主入口
三地市场（A股/港股/美股）定时分析推送
优先使用 Claude 大模型深度分析，未配置 API Key 时自动降级为规则引擎

调度时间表（CST, UTC+8）：
  09:00  →  A股+港股 开盘前分析（推送飞书）
  16:30  →  A股+港股 收盘复盘（港股16:00收盘，推送飞书）
  21:00  →  美股 开盘前分析（推送飞书）

运行方式：
  python main.py                           # 定时模式（生产）
  python main.py --now premarket_asia      # 立即执行亚洲盘前
  python main.py --now premarket_us        # 立即执行美股盘前
  python main.py --now postmarket_asia     # 立即执行亚洲复盘
  python main.py --test                    # 测试飞书连接
  python main.py --ask "你的问题"          # 向 Claude 提问，结果推送到飞书
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── 项目根路径 ─────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from config import config
from fetchers.news_fetcher import NewsFetcher
from fetchers.market_data import MarketDataFetcher
from fetchers.research_fetcher import ResearchFetcher
from fetchers.economic_calendar import EconomicCalendarFetcher
from analyzers.base_analyzer import BaseAnalyzer
from analyzers.claude_analyzer import ClaudeAnalyzer
from analyzers.openai_analyzer import OpenAIAnalyzer
from analyzers.gemini_analyzer import GeminiAnalyzer
from analyzers.rule_analyzer import RuleAnalyzer
from notifiers.feishu import FeishuNotifier
from feishu_bot_server import FeishuQABot, run_bot_server

# ── 日志配置 ───────────────────────────────────────────────────────────
# 确保 cache 目录在写日志前存在（Windows 首次运行时 /app/cache 不存在）
Path(config.cache_dir).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, config.log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            Path(config.cache_dir) / "market_brief.log",
            encoding="utf-8",
        ),
    ],
)
logger = logging.getLogger("market_brief")
CST = timezone(timedelta(hours=8))


# ══════════════════════════════════════════════════════════════════════
#  分析引擎工厂
# ══════════════════════════════════════════════════════════════════════

def _build_analyzer(cfg) -> BaseAnalyzer:
    """根据配置选择分析引擎，支持手动指定或自动选择"""
    provider = cfg.ai_provider.lower()

    def try_claude():
        if cfg.anthropic_api_key:
            return ClaudeAnalyzer(api_key=cfg.anthropic_api_key, model=cfg.claude_model)
        return None

    def try_openai():
        if cfg.openai_api_key:
            return OpenAIAnalyzer(api_key=cfg.openai_api_key, model=cfg.openai_model)
        return None

    def try_gemini():
        if cfg.gemini_api_key:
            return GeminiAnalyzer(api_key=cfg.gemini_api_key, model=cfg.gemini_model)
        return None

    if provider == "claude":
        analyzer = try_claude()
        if not analyzer:
            raise ValueError("AI_PROVIDER=claude 但未配置 ANTHROPIC_API_KEY")
    elif provider == "openai":
        analyzer = try_openai()
        if not analyzer:
            raise ValueError("AI_PROVIDER=openai 但未配置 OPENAI_API_KEY")
    elif provider == "gemini":
        analyzer = try_gemini()
        if not analyzer:
            raise ValueError("AI_PROVIDER=gemini 但未配置 GEMINI_API_KEY")
    else:
        # auto：按优先级自动选择
        analyzer = try_claude() or try_openai() or try_gemini()

    if analyzer is None:
        logger.warning("未配置任何 AI API Key，降级使用规则引擎（分析质量较低）")
        return RuleAnalyzer()

    return analyzer


def _analyzer_label(analyzer) -> str:
    name_map = {
        "ClaudeAnalyzer": f"Claude（{getattr(analyzer, 'model', '')}）",
        "OpenAIAnalyzer": f"OpenAI ChatGPT（{getattr(analyzer, 'model', '')}）",
        "GeminiAnalyzer": f"Google Gemini（{getattr(analyzer, 'model_name', '')}）",
        "RuleAnalyzer": "规则引擎（无 AI Key，分析质量较低）",
    }
    return name_map.get(type(analyzer).__name__, type(analyzer).__name__)


# ══════════════════════════════════════════════════════════════════════
#  核心任务
# ══════════════════════════════════════════════════════════════════════

class MarketBriefOrchestrator:
    """编排数据抓取、分析、推送的完整流程"""

    def __init__(self):
        config.validate()
        os.makedirs(config.cache_dir, exist_ok=True)

        self.news_fetcher = NewsFetcher(
            cache_dir=config.cache_dir,
            newsapi_key=config.newsapi_key or "",
        )
        self.market_fetcher = MarketDataFetcher(
            alpha_vantage_key=config.alpha_vantage_key,
        )
        self.research_fetcher = ResearchFetcher()
        self.calendar_fetcher = EconomicCalendarFetcher()
        self.analyzer = _build_analyzer(config)
        logger.info(f"分析引擎：{_analyzer_label(self.analyzer)}")
        self.notifier = FeishuNotifier(
            webhook_urls=config.feishu_webhooks,
            secret=config.feishu_secret,
            app_id=config.feishu_app_id,
            app_secret=config.feishu_app_secret,
            chat_ids=config.feishu_chat_ids,
        )
        mode = "自建应用 API（可收发）" if config.feishu_app_mode else "Webhook（仅发送）"
        logger.info(f"飞书发送模式：{mode}")
        self._last_strategy: dict = self._load_last_strategy()

    # ── 任务1：亚洲盘前分析 ─────────────────────────────────────────────

    def run_premarket_asia(self):
        logger.info("=== 开始执行 A股+港股 开盘前分析 ===")
        try:
            # 1. 数据抓取
            logger.info("正在抓取新闻...")
            news = self.news_fetcher.fetch_all(hours=12)

            logger.info("正在获取市场数据...")
            cn_data = self.market_fetcher.fetch_market_overview("cn")
            hk_data = self.market_fetcher.fetch_market_overview("hk")
            us_data = self.market_fetcher.fetch_market_overview("us")  # 美股隔夜数据
            market_data = {"cn": cn_data, "hk": hk_data, "us_overnight": us_data}

            logger.info("正在获取研报...")
            reports = self.research_fetcher.fetch_recent(hours=24)

            logger.info("正在获取经济日历...")
            events = self.calendar_fetcher.fetch_upcoming(days_ahead=3)

            # 2. 分析（Claude 失败时自动降级到规则引擎）
            logger.info("正在进行分析...")
            try:
                analysis = self.analyzer.analyze_premarket(
                    market_type="asia",
                    news_items=news,
                    market_data=market_data,
                    research_reports=reports,
                    economic_events=events,
                    focus_sectors=config.focus_sectors,
                    watchlist=config.watchlist,
                    yesterday_strategy=self._last_strategy.get("asia_postmarket"),
                )
            except Exception as e:
                if isinstance(self.analyzer, ClaudeAnalyzer):
                    logger.warning(f"Claude 分析失败（{e}），降级到规则引擎")
                    analysis = RuleAnalyzer().analyze_premarket(
                        market_type="asia",
                        news_items=news,
                        market_data=market_data,
                        research_reports=reports,
                        economic_events=events,
                        focus_sectors=config.focus_sectors,
                        watchlist=config.watchlist,
                        yesterday_strategy=self._last_strategy.get("asia_postmarket"),
                    )
                else:
                    raise

            # 3. 推送飞书
            logger.info("正在推送飞书...")
            success = self.notifier.send_premarket_report(analysis, "A股+港股")

            # 4. 保存策略（供复盘对比）
            self._save_strategy("asia_premarket", analysis.trading_strategy)

            logger.info(f"A股+港股 开盘前推送{'成功' if success else '失败'}")
            return analysis

        except Exception as e:
            logger.exception(f"亚洲盘前分析失败: {e}")
            self.notifier.send_alert("亚洲盘前分析失败", str(e), level="error")

    # ── 任务2：亚洲收盘复盘 ─────────────────────────────────────────────

    def run_postmarket_asia(self):
        logger.info("=== 开始执行 A股+港股 收盘复盘 ===")
        try:
            news = self.news_fetcher.fetch_all(hours=8)
            cn_data = self.market_fetcher.fetch_market_overview("cn")
            hk_data = self.market_fetcher.fetch_market_overview("hk")
            market_data = {"cn": cn_data, "hk": hk_data}

            try:
                analysis = self.analyzer.analyze_postmarket(
                    market_type="asia",
                    market_data=market_data,
                    news_items=news,
                    morning_strategy=self._last_strategy.get("asia_premarket"),
                    focus_sectors=config.focus_sectors,
                )
            except Exception as e:
                if isinstance(self.analyzer, ClaudeAnalyzer):
                    logger.warning(f"Claude 分析失败（{e}），降级到规则引擎")
                    analysis = RuleAnalyzer().analyze_postmarket(
                        market_type="asia",
                        market_data=market_data,
                        news_items=news,
                        morning_strategy=self._last_strategy.get("asia_premarket"),
                        focus_sectors=config.focus_sectors,
                    )
                else:
                    raise

            success = self.notifier.send_postmarket_report(analysis, "A股+港股")
            self._save_strategy("asia_postmarket", analysis.trading_strategy)

            logger.info(f"A股+港股 收盘复盘推送{'成功' if success else '失败'}")
            return analysis

        except Exception as e:
            logger.exception(f"亚洲收盘复盘失败: {e}")
            self.notifier.send_alert("亚洲收盘复盘失败", str(e), level="error")

    # ── 任务3：美股盘前分析 ─────────────────────────────────────────────

    def run_premarket_us(self):
        logger.info("=== 开始执行 美股 开盘前分析 ===")
        try:
            news = self.news_fetcher.fetch_all(hours=12)
            us_data = self.market_fetcher.fetch_market_overview("us")
            cn_data = self.market_fetcher.fetch_market_overview("cn")
            hk_data = self.market_fetcher.fetch_market_overview("hk")
            market_data = {
                "us": us_data,
                "cn_today": cn_data,
                "hk_today": hk_data,
            }

            reports = self.research_fetcher.fetch_recent(hours=12)
            events = self.calendar_fetcher.fetch_upcoming(days_ahead=2)

            try:
                analysis = self.analyzer.analyze_premarket(
                    market_type="us",
                    news_items=news,
                    market_data=market_data,
                    research_reports=reports,
                    economic_events=events,
                    focus_sectors=config.focus_sectors,
                    watchlist=config.watchlist,
                    yesterday_strategy=self._last_strategy.get("us_premarket"),
                )
            except Exception as e:
                if isinstance(self.analyzer, ClaudeAnalyzer):
                    logger.warning(f"Claude 分析失败（{e}），降级到规则引擎")
                    analysis = RuleAnalyzer().analyze_premarket(
                        market_type="us",
                        news_items=news,
                        market_data=market_data,
                        research_reports=reports,
                        economic_events=events,
                        focus_sectors=config.focus_sectors,
                        watchlist=config.watchlist,
                        yesterday_strategy=self._last_strategy.get("us_premarket"),
                    )
                else:
                    raise

            success = self.notifier.send_premarket_report(analysis, "美股")
            self._save_strategy("us_premarket", analysis.trading_strategy)

            logger.info(f"美股 开盘前推送{'成功' if success else '失败'}")
            return analysis

        except Exception as e:
            logger.exception(f"美股盘前分析失败: {e}")
            self.notifier.send_alert("美股盘前分析失败", str(e), level="error")

    # ── 策略持久化 ────────────────────────────────────────────────────

    def _save_strategy(self, key: str, strategy: str):
        self._last_strategy[key] = strategy
        try:
            cache_file = Path(config.cache_dir) / "last_strategy.json"
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(self._last_strategy, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"策略保存失败: {e}")

    def _load_last_strategy(self) -> dict:
        try:
            cache_file = Path(config.cache_dir) / "last_strategy.json"
            if cache_file.exists():
                with open(cache_file, encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.debug(f"读取策略缓存失败: {e}")
        return {}


# ══════════════════════════════════════════════════════════════════════
#  启动补跑：程序晚启动时立即执行今日已错过的任务
# ══════════════════════════════════════════════════════════════════════

def _catchup_missed_jobs(orchestrator: MarketBriefOrchestrator, now: datetime):
    """
    调度器启动时检查今日是否有任务在过去 2 小时内被错过。
    若是工作日且当前时间落在 [scheduled_time, scheduled_time+2h] 区间，则立即补跑一次。
    这解决了电脑晚开机 / 从睡眠唤醒 / 程序晚启动导致的漏推问题。
    """
    if now.weekday() >= 5:   # 周六/日不补跑
        return

    GRACE_HOURS = 5  # 收盘后5小时内均可补跑

    jobs = [
        # (计划小时, 计划分钟, 任务函数, 任务名)
        (config.asia_premarket_hour,  config.asia_premarket_minute,  orchestrator.run_premarket_asia,  "A股+港股开盘前分析"),
        (config.asia_postmarket_hour, config.asia_postmarket_minute, orchestrator.run_postmarket_asia, "A股+港股收盘复盘"),
        (config.us_premarket_hour,    config.us_premarket_minute,    orchestrator.run_premarket_us,    "美股开盘前分析"),
    ]

    for hour, minute, func, name in jobs:
        scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        delta_minutes = (now - scheduled).total_seconds() / 60
        if 0 < delta_minutes <= GRACE_HOURS * 60:
            logger.info(f"[补跑] {name} 计划 {hour:02d}:{minute:02d}，已过 {delta_minutes:.0f} 分钟，立即执行")
            try:
                func()
            except Exception as e:
                logger.error(f"[补跑] {name} 执行失败: {e}")


# ══════════════════════════════════════════════════════════════════════
#  调度器
# ══════════════════════════════════════════════════════════════════════

def run_scheduler(orchestrator: MarketBriefOrchestrator):
    """使用 APScheduler 按时间表执行任务"""
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger

    scheduler = BlockingScheduler(timezone="Asia/Shanghai")

    # misfire_grace_time=18000：容忍最多 5 小时的延迟
    # 解决：电脑晚开机、从睡眠唤醒、程序晚启动等场景下任务被跳过的问题
    # coalesce=True：多次积压的 misfire 只补跑一次，防止重复推送
    GRACE = 18000

    # A股+港股 开盘前（默认 09:00 CST，周一至周五）
    scheduler.add_job(
        orchestrator.run_premarket_asia,
        CronTrigger(
            day_of_week="mon-fri",
            hour=config.asia_premarket_hour,
            minute=config.asia_premarket_minute,
            timezone="Asia/Shanghai",
        ),
        id="premarket_asia",
        name="A股+港股开盘前分析",
        replace_existing=True,
        misfire_grace_time=GRACE,
        coalesce=True,
    )

    # A股+港股 收盘复盘（默认 15:30 CST，周一至周五）
    scheduler.add_job(
        orchestrator.run_postmarket_asia,
        CronTrigger(
            day_of_week="mon-fri",
            hour=config.asia_postmarket_hour,
            minute=config.asia_postmarket_minute,
            timezone="Asia/Shanghai",
        ),
        id="postmarket_asia",
        name="A股+港股收盘复盘",
        replace_existing=True,
        misfire_grace_time=GRACE,
        coalesce=True,
    )

    # 美股 开盘前（默认 21:00 CST，周一至周五）
    scheduler.add_job(
        orchestrator.run_premarket_us,
        CronTrigger(
            day_of_week="mon-fri",
            hour=config.us_premarket_hour,
            minute=config.us_premarket_minute,
            timezone="Asia/Shanghai",
        ),
        id="premarket_us",
        name="美股开盘前分析",
        replace_existing=True,
        misfire_grace_time=GRACE,
        coalesce=True,
    )

    now = datetime.now(CST)
    logger.info(f"调度器启动 (当前时间: {now.strftime('%Y-%m-%d %H:%M CST')})")
    logger.info(f"  A股+港股 开盘前: 每周一至五 {config.asia_premarket_hour:02d}:{config.asia_premarket_minute:02d} CST")
    logger.info(f"  A股+港股 收盘复盘: 每周一至五 {config.asia_postmarket_hour:02d}:{config.asia_postmarket_minute:02d} CST")
    logger.info(f"  美股 开盘前: 每周一至五 {config.us_premarket_hour:02d}:{config.us_premarket_minute:02d} CST")

    # 启动时补跑：检查今日是否有任务在 2 小时内被错过，有则立即执行
    _catchup_missed_jobs(orchestrator, now)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("调度器已停止")


# ══════════════════════════════════════════════════════════════════════
#  CLI 入口
# ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="三地股市智能晨报/晚报系统（Claude 大模型分析，无 Key 时降级为规则引擎）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                              # 启动定时调度（生产模式）
  python main.py --now premarket_asia         # 立即生成亚洲盘前报告
  python main.py --now postmarket_asia        # 立即生成亚洲收盘复盘
  python main.py --now premarket_us           # 立即生成美股盘前报告
  python main.py --test                       # 发送测试消息到飞书
  python main.py --ask "碧桂园利润预期的影响"  # 向 Claude 提问，结果推送到飞书
        """,
    )
    parser.add_argument(
        "--now",
        choices=["premarket_asia", "postmarket_asia", "premarket_us"],
        help="立即执行指定任务（不启动调度器）",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="发送测试消息到飞书（验证 Webhook 配置）",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="仅验证配置，不运行任务",
    )
    parser.add_argument(
        "--ask",
        metavar="QUESTION",
        help="向 Claude 提问金融问题，分析结果推送到飞书（例：--ask '碧桂园利润预期对港股有何影响？'）",
    )
    args = parser.parse_args()

    # 配置校验
    try:
        config.validate()
        logger.info("配置校验通过")
        analyzer_preview = _build_analyzer(config)
        logger.info(f"  分析引擎: {_analyzer_label(analyzer_preview)}")
        if config.feishu_app_mode:
            logger.info(f"  飞书模式: 自建应用（app_id={config.feishu_app_id[:8]}...，推送 {len(config.feishu_chat_ids)} 个群）")
        else:
            logger.info(f"  飞书模式: Webhook（{len(config.feishu_webhooks)} 个）")
        logger.info(f"  关注板块: {', '.join(config.focus_sectors)}")
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    if args.validate:
        return

    orchestrator = MarketBriefOrchestrator()

    if args.test:
        logger.info("发送测试消息...")
        engine_label = (
            f"Claude 大模型（{config.claude_model}）"
            if config.anthropic_api_key
            else "规则引擎（未配置 ANTHROPIC_API_KEY，分析质量较低）"
        )
        success = orchestrator.notifier.send_alert(
            title="市场晨报系统测试",
            content=(
                "飞书推送配置正常！\n\n"
                f"系统信息：\n"
                f"- 分析引擎：{engine_label}\n"
                f"- 关注板块：{', '.join(config.focus_sectors)}\n"
                f"- 调度时间：亚洲 {config.asia_premarket_hour:02d}:{config.asia_premarket_minute:02d} / "
                f"复盘 {config.asia_postmarket_hour:02d}:{config.asia_postmarket_minute:02d} / "
                f"美股 {config.us_premarket_hour:02d}:{config.us_premarket_minute:02d} CST\n"
                f"- 当前时间：{datetime.now(CST).strftime('%Y-%m-%d %H:%M CST')}"
            ),
            level="info",
        )
        sys.exit(0 if success else 1)

    if args.now:
        task_map = {
            "premarket_asia":  orchestrator.run_premarket_asia,
            "postmarket_asia": orchestrator.run_postmarket_asia,
            "premarket_us":    orchestrator.run_premarket_us,
        }
        task_map[args.now]()
        return

    if args.ask:
        qa_bot = FeishuQABot(orchestrator, orchestrator.notifier)
        success = qa_bot.answer_and_push(args.ask, sender_name="命令行")
        sys.exit(0 if success else 1)

    # 默认：定时调度模式
    if config.run_mode == "scheduler":
        # 若启用了飞书 Q&A 机器人，先在后台启动 HTTP 服务器
        if config.feishu_bot_enabled:
            qa_bot = FeishuQABot(orchestrator, orchestrator.notifier)
            run_bot_server(
                qa_bot=qa_bot,
                port=config.feishu_bot_port,
                verification_token=config.feishu_verification_token,
            )
            logger.info(
                f"飞书 Q&A 机器人已启动（端口 {config.feishu_bot_port}）"
                "，群内 @机器人 即可提问"
            )
        run_scheduler(orchestrator)
    else:
        logger.info("RUN_MODE=manual，退出（使用 --now 手动触发任务）")


if __name__ == "__main__":
    main()
