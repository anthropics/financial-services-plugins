"""
配置模块 - 从环境变量读取所有配置
无需任何大模型API Key
"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    # ── 飞书 Feishu ──────────────────────────────────────────────────
    # 支持多个 webhook，逗号分隔
    feishu_webhooks: list = field(
        default_factory=lambda: [
            w.strip()
            for w in os.environ.get("FEISHU_WEBHOOK_URLS", "").split(",")
            if w.strip()
        ]
    )
    feishu_secret: Optional[str] = field(
        default_factory=lambda: os.environ.get("FEISHU_SECRET")
    )

    # ── 可选数据源 API Key（有免费替代方案）──────────────────────────
    # Alpha Vantage: https://www.alphavantage.co/support/#api-key (免费)
    alpha_vantage_key: str = field(
        default_factory=lambda: os.environ.get("ALPHA_VANTAGE_KEY", "demo")
    )
    # NewsAPI: https://newsapi.org/register (免费100次/天)
    newsapi_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("NEWSAPI_KEY")
    )

    # ── 调度时间（CST, UTC+8）────────────────────────────────────────
    # A股+港股 开盘前30分钟推送
    asia_premarket_hour: int = field(
        default_factory=lambda: int(os.environ.get("ASIA_PREMARKET_HOUR", "9"))
    )
    asia_premarket_minute: int = field(
        default_factory=lambda: int(os.environ.get("ASIA_PREMARKET_MINUTE", "0"))
    )
    # A股+港股 收盘后30分钟复盘
    asia_postmarket_hour: int = field(
        default_factory=lambda: int(os.environ.get("ASIA_POSTMARKET_HOUR", "15"))
    )
    asia_postmarket_minute: int = field(
        default_factory=lambda: int(os.environ.get("ASIA_POSTMARKET_MINUTE", "30"))
    )
    # 美股 开盘前30分钟推送 (9:30 PM CST winter / 8:30 PM CST summer)
    us_premarket_hour: int = field(
        default_factory=lambda: int(os.environ.get("US_PREMARKET_HOUR", "21"))
    )
    us_premarket_minute: int = field(
        default_factory=lambda: int(os.environ.get("US_PREMARKET_MINUTE", "0"))
    )

    # ── 代理设置（可选）────────────────────────────────────────────────
    http_proxy: Optional[str] = field(
        default_factory=lambda: os.environ.get("HTTP_PROXY")
    )
    https_proxy: Optional[str] = field(
        default_factory=lambda: os.environ.get("HTTPS_PROXY")
    )

    # ── 重点关注板块（逗号分隔）────────────────────────────────────────
    focus_sectors: list = field(
        default_factory=lambda: [
            s.strip()
            for s in os.environ.get(
                "FOCUS_SECTORS",
                "科技,新能源,半导体,消费,医药,金融,房地产,人工智能"
            ).split(",")
            if s.strip()
        ]
    )

    # ── 重点关注标的（可选，逗号分隔股票代码）──────────────────────────
    watchlist: list = field(
        default_factory=lambda: [
            s.strip()
            for s in os.environ.get("WATCHLIST", "").split(",")
            if s.strip()
        ]
    )

    # ── 运行模式 ────────────────────────────────────────────────────
    # "scheduler" = 定时运行（生产）| "manual" = 手动触发（测试）
    run_mode: str = field(
        default_factory=lambda: os.environ.get("RUN_MODE", "scheduler")
    )
    log_level: str = field(
        default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO")
    )
    # 数据缓存目录
    cache_dir: str = field(
        default_factory=lambda: os.environ.get("CACHE_DIR", "/app/cache")
    )

    def validate(self):
        errors = []
        if not self.feishu_webhooks:
            errors.append("FEISHU_WEBHOOK_URLS 未设置（至少一个）")
        if errors:
            raise ValueError("配置错误：\n" + "\n".join(f"  - {e}" for e in errors))
        return self


# 全局单例
config = Config()
