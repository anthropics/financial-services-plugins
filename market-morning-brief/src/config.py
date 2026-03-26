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
    # 模式一：群自定义机器人 Webhook（只能发，不能收）
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

    # 模式二：自建应用（可发可收，与 Q&A 机器人统一为一个机器人）
    # 在飞书开放平台 (open.feishu.cn) 创建自建应用后获取
    feishu_app_id: Optional[str] = field(
        default_factory=lambda: os.environ.get("FEISHU_APP_ID")
    )
    feishu_app_secret: Optional[str] = field(
        default_factory=lambda: os.environ.get("FEISHU_APP_SECRET")
    )
    # 要推送消息的群 chat_id，逗号分隔（在群设置中获取，或通过 API 查询）
    feishu_chat_ids: list = field(
        default_factory=lambda: [
            c.strip()
            for c in os.environ.get("FEISHU_CHAT_IDS", "").split(",")
            if c.strip()
        ]
    )

    # ── AI 分析引擎（三选一，未配置对应 Key 时自动跳过）──────────────
    # AI_PROVIDER 可手动指定：claude | openai | gemini
    # 不填时按优先级自动选择：claude → openai → gemini → 规则引擎
    ai_provider: str = field(
        default_factory=lambda: os.environ.get("AI_PROVIDER", "auto")
    )

    # Claude（Anthropic）
    # 申请地址：https://console.anthropic.com/
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY")
    )
    claude_model: str = field(
        default_factory=lambda: os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
    )

    # OpenAI（ChatGPT）
    # 申请地址：https://platform.openai.com/api-keys
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("OPENAI_API_KEY")
    )
    openai_model: str = field(
        default_factory=lambda: os.environ.get("OPENAI_MODEL", "gpt-4o")
    )

    # Google Gemini
    # 申请地址：https://aistudio.google.com/app/apikey
    gemini_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("GEMINI_API_KEY")
    )
    gemini_model: str = field(
        default_factory=lambda: os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
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

    @property
    def feishu_app_mode(self) -> bool:
        """是否使用自建应用模式（app_id + app_secret + chat_id）"""
        return bool(self.feishu_app_id and self.feishu_app_secret and self.feishu_chat_ids)

    def validate(self):
        errors = []
        if not self.feishu_app_mode and not self.feishu_webhooks:
            errors.append(
                "请配置飞书发送方式（二选一）：\n"
                "    方式一（自建应用，可收发）：FEISHU_APP_ID + FEISHU_APP_SECRET + FEISHU_CHAT_IDS\n"
                "    方式二（Webhook，仅发送）：FEISHU_WEBHOOK_URLS"
            )
        if errors:
            raise ValueError("配置错误：\n" + "\n".join(f"  - {e}" for e in errors))
        return self


# 全局单例
config = Config()
