#!/usr/bin/env python3
"""
市场晨报/晚报系统 - 主入口
三地市场（A股/港股/美股）定时分析推送
无需任何大模型，基于规则引擎自动分析

调度时间表（CST, UTC+8）：
  09:00  →  A股+港股 开盘前分析（推送飞书）
  15:30  →  A股+港股 收盘复盘（推送飞书）
  21:00  →  美股 开盘前分析（推送飞书）

运行方式：
  python main.py                    # 定时模式（生产）
  python main.py --now premarket_asia   # 立即执行亚洲盘前
  python main.py --now premarket_us     # 立即执行美股盘前
  python main.py --now postmarket_asia  # 立即执行亚洲复盘
  python main.py --test             # 测试飞书连接
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
from analyzers.rule_analyzer import RuleAnalyzer
from notifiers.feishu import FeishuNotifier

# ── 日志配置 ───────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, config.log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            Path(config.cache_dir) / "market_brief.log",
            encoding="utf-8",
        ) if Path(config.cache_dir).exists() else logging.StreamHandler(),
    ],
)
logger = logging.getLogger("market_brief")
CST = timezone(timedelta(hours=8))


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
        self.market_fetcher = MarketDataFetcher()
        self.research_fetcher = ResearchFetcher()
        self.calendar_fetcher = EconomicCalendarFetcher()
        self.analyzer = RuleAnalyzer()
        self.notifier = FeishuNotifier(
            webhook_urls=config.feishu_webhooks,
            secret=config.feishu_secret,
        )
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

            # 2. 规则引擎分析
            logger.info("正在进行规则引擎分析...")
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

            analysis = self.analyzer.analyze_postmarket(
                market_type="asia",
                market_data=market_data,
                news_items=news,
                morning_strategy=self._last_strategy.get("asia_premarket"),
                focus_sectors=config.focus_sectors,
            )

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
#  调度器
# ══════════════════════════════════════════════════════════════════════

def run_scheduler(orchestrator: MarketBriefOrchestrator):
    """使用 APScheduler 按时间表执行任务"""
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger

    scheduler = BlockingScheduler(timezone="Asia/Shanghai")

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
        misfire_grace_time=300,
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
        misfire_grace_time=300,
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
        misfire_grace_time=300,
    )

    now = datetime.now(CST)
    logger.info(f"调度器启动 (当前时间: {now.strftime('%Y-%m-%d %H:%M CST')})")
    logger.info(f"  A股+港股 开盘前: 每周一至五 {config.asia_premarket_hour:02d}:{config.asia_premarket_minute:02d} CST")
    logger.info(f"  A股+港股 收盘复盘: 每周一至五 {config.asia_postmarket_hour:02d}:{config.asia_postmarket_minute:02d} CST")
    logger.info(f"  美股 开盘前: 每周一至五 {config.us_premarket_hour:02d}:{config.us_premarket_minute:02d} CST")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("调度器已停止")


# ══════════════════════════════════════════════════════════════════════
#  CLI 入口
# ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="三地股市智能晨报/晚报系统（规则引擎版，无需大模型）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py                         # 启动定时调度（生产模式）
  python main.py --now premarket_asia    # 立即生成亚洲盘前报告
  python main.py --now postmarket_asia   # 立即生成亚洲收盘复盘
  python main.py --now premarket_us      # 立即生成美股盘前报告
  python main.py --test                  # 发送测试消息到飞书
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
    args = parser.parse_args()

    # 配置校验
    try:
        config.validate()
        logger.info("配置校验通过")
        logger.info(f"  分析引擎: 规则引擎（无需大模型）")
        logger.info(f"  飞书 Webhook 数量: {len(config.feishu_webhooks)}")
        logger.info(f"  关注板块: {', '.join(config.focus_sectors)}")
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    if args.validate:
        return

    orchestrator = MarketBriefOrchestrator()

    if args.test:
        logger.info("发送测试消息...")
        success = orchestrator.notifier.send_alert(
            title="市场晨报系统测试",
            content=(
                "飞书推送配置正常！\n\n"
                f"系统信息：\n"
                f"- 分析引擎：规则引擎（零API成本）\n"
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

    # 默认：定时调度模式
    if config.run_mode == "scheduler":
        run_scheduler(orchestrator)
    else:
        logger.info("RUN_MODE=manual，退出（使用 --now 手动触发任务）")


if __name__ == "__main__":
    main()
