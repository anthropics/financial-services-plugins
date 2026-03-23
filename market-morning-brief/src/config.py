"""
配置模块 - 从环境变量读取所有配置
"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# 项目根目录（market-morning-brief/）
_ROOT = Path(__file__).parent.parent


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

    # ── Anthropic API Key（用于 Claude 大模型分析）────────────────────
    # 申请地址：https://console.anthropic.com/
    # 未设置时自动降级为规则引擎（分析质量较低，仅作兜底）
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY")
    )
    # Claude 模型版本（默认使用 claude-sonnet-4-6）
    claude_model: str = field(
        default_factory=lambda: os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
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
    # A股+港股 收盘复盘（港股16:00收盘，默认16:30推送）
    asia_postmarket_hour: int = field(
        default_factory=lambda: int(os.environ.get("ASIA_POSTMARKET_HOUR", "16"))
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

    # ── 飞书 Q&A 机器人（可选）──────────────────────────────────────
    # 开启后启动 HTTP 服务器接收飞书群消息，群内 @机器人 即可与 Claude 对话
    # 需要在飞书开放平台创建自建应用并配置事件订阅
    feishu_bot_enabled: bool = field(
        default_factory=lambda: os.environ.get("FEISHU_BOT_ENABLED", "false").lower() == "true"
    )
    feishu_bot_port: int = field(
        default_factory=lambda: int(os.environ.get("FEISHU_BOT_PORT", "5000"))
    )
    # 飞书事件订阅验证 Token（在飞书开放平台 → 事件订阅 → Verification Token 获取）
    feishu_verification_token: Optional[str] = field(
        default_factory=lambda: os.environ.get("FEISHU_VERIFICATION_TOKEN")
    )

    # ── 运行模式 ────────────────────────────────────────────────────
    # "scheduler" = 定时运行（生产）| "manual" = 手动触发（测试）
    run_mode: str = field(
        default_factory=lambda: os.environ.get("RUN_MODE", "scheduler")
    )
    log_level: str = field(
        default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO")
    )
    # 数据缓存目录（Windows/Linux 跨平台：默认与项目同级的 cache 文件夹）
    cache_dir: str = field(
        default_factory=lambda: os.environ.get(
            "CACHE_DIR", str(_ROOT / "cache")
        )
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
