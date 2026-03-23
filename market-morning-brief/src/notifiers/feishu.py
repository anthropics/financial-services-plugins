"""
飞书通知模块
支持两种发送方式：
  1. 自建应用 API（推荐，可发可收，与 Q&A 机器人统一为一个机器人）
     需要：FEISHU_APP_ID + FEISHU_APP_SECRET + FEISHU_CHAT_IDS
  2. 群自定义机器人 Webhook（仅发送，配置更简单）
     需要：FEISHU_WEBHOOK_URLS

飞书开放平台文档：
  自建应用：https://open.feishu.cn/document/home/develop-a-bot-in-5-minutes/create-an-app
  Webhook：https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
"""

import base64
import hashlib
import hmac
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

logger = logging.getLogger(__name__)
CST = timezone(timedelta(hours=8))

# 飞书开放平台 API 地址
_FEISHU_API_BASE = "https://open.feishu.cn/open-apis"


class FeishuNotifier:
    """
    飞书消息推送器
    自动选择发送方式：
      - 优先使用自建应用 API（需要 app_id + app_secret + chat_ids）
      - 降级使用 Webhook（需要 webhook_urls）
    """

    TIMEOUT = 15

    def __init__(
        self,
        webhook_urls: Optional[list[str]] = None,
        secret: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        chat_ids: Optional[list[str]] = None,
    ):
        self.webhook_urls = webhook_urls or []
        self.secret = secret
        self.app_id = app_id
        self.app_secret = app_secret
        self.chat_ids = chat_ids or []
        self._token_cache: tuple[str, float] = ("", 0.0)  # (token, expire_at)

        if not self.app_mode and not self.webhook_urls:
            raise ValueError("至少需要配置自建应用（app_id+app_secret+chat_ids）或 Webhook URL")

    @property
    def app_mode(self) -> bool:
        """是否使用自建应用模式"""
        return bool(self.app_id and self.app_secret and self.chat_ids)

    # ── tenant_access_token 管理 ────────────────────────────────────

    def _get_tenant_access_token(self) -> str:
        """获取 tenant_access_token，自动缓存（有效期2小时，提前5分钟刷新）"""
        token, expire_at = self._token_cache
        if token and time.time() < expire_at - 300:
            return token

        resp = requests.post(
            f"{_FEISHU_API_BASE}/auth/v3/tenant_access_token/internal",
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=self.TIMEOUT,
        )
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取 tenant_access_token 失败: {data}")

        new_token = data["tenant_access_token"]
        expire_in = data.get("expire", 7200)
        self._token_cache = (new_token, time.time() + expire_in)
        logger.debug("[Feishu] tenant_access_token 已刷新")
        return new_token

    # ── 主发送方法 ─────────────────────────────────────────────────────

    def send_premarket_report(self, analysis, market_label: str):
        """发送开盘前分析报告（飞书消息卡片格式）"""
        card = self._build_premarket_card(analysis, market_label)
        return self._send_card(card)

    def send_postmarket_report(self, analysis, market_label: str):
        """发送收盘复盘报告"""
        card = self._build_postmarket_card(analysis, market_label)
        return self._send_card(card)

    def send_alert(self, title: str, content: str, level: str = "warning"):
        """发送告警消息"""
        color_map = {"info": "blue", "warning": "orange", "error": "red"}
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"⚠️ {title}"},
                "template": color_map.get(level, "orange"),
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": content}}
            ],
        }
        return self._send_card(card)

    # ── 卡片构建：开盘前 ────────────────────────────────────────────────

    def _build_premarket_card(self, analysis, market_label: str) -> dict:
        now_str = datetime.now(CST).strftime("%m月%d日 %H:%M")
        report_type = analysis.report_type

        # 头部
        header_color = "turquoise" if "asia" in report_type else "purple"
        icon = "🌏" if "asia" in report_type else "🗽"

        elements = []

        # 一句话总结
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**📊 市场摘要**\n{analysis.market_summary}"
            }
        })
        elements.append({"tag": "hr"})

        # 重要事件（最多5条）
        key_events = analysis.key_events[:5]
        if key_events:
            event_lines = ["**🔔 关键事件与影响**\n"]
            for ev in key_events:
                direction = ev.get("impact_direction", "neutral")
                dir_icon = {"positive": "📈", "negative": "📉", "neutral": "➡️"}.get(direction, "➡️")
                magnitude = ev.get("impact_magnitude", "medium")
                mag_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(magnitude, "🟡")
                vars_str = "/".join(ev.get("impact_variables", []))
                event_lines.append(
                    f"{dir_icon}{mag_icon} **{ev.get('title', '')}**\n"
                    f"　来源：[{ev.get('source', '')}]({ev.get('source_url', '#')})\n"
                    f"　影响变量：{vars_str} | 传导：{ev.get('transmission_chain', '')[:80]}\n"
                    f"　受影响板块：{', '.join(ev.get('affected_sectors', []))}\n"
                )
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": "\n".join(event_lines)}
            })
            elements.append({"tag": "hr"})

        # 板块展望
        sector_outlook = analysis.sector_outlook[:6]
        if sector_outlook:
            sector_lines = ["**🗂️ 板块展望**\n"]
            for s in sector_outlook:
                direction = s.get("direction", "neutral")
                icon_map = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}
                s_icon = icon_map.get(direction, "➡️")
                picks = "、".join(s.get("top_picks", [])[:3])
                sector_lines.append(
                    f"{s_icon} **{s.get('sector')}** — {s.get('key_driver', '')[:60]}"
                    + (f"\n　关注：{picks}" if picks else "")
                )
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": "\n".join(sector_lines)}
            })
            elements.append({"tag": "hr"})

        # 重点关注标的（表格）
        watchlist = analysis.watchlist[:8]
        if watchlist:
            watch_lines = ["**🎯 重点关注标的**\n"]
            watch_lines.append("| 标的 | 市场 | 操作建议 | 目标价 | 逻辑（第一性原则）| 风险 |")
            watch_lines.append("|------|------|----------|--------|------------------|------|")
            for w in watchlist:
                action = w.get("action", "观望")
                action_icon = {"关注买入": "🟢", "关注卖出": "🔴", "观望": "⚪"}.get(action, "⚪")
                code_name = f"{w.get('name', '')}({w.get('code', '')})"
                watch_lines.append(
                    f"| {code_name} | {w.get('market', '')} | "
                    f"{action_icon}{action} | {w.get('price_target', '-')} | "
                    f"{w.get('rationale', '')[:40]} | {w.get('risk', '')[:30]} |"
                )
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": "\n".join(watch_lines)}
            })
            elements.append({"tag": "hr"})

        # 整体操作建议
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**💡 整体操作建议**\n{analysis.trading_strategy}"
            }
        })

        # 风险提示
        if analysis.risk_warnings:
            risk_text = "\n".join(f"⚠️ {r}" for r in analysis.risk_warnings[:3])
            elements.append({"tag": "hr"})
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": f"**风险提示**\n{risk_text}"}
            })

        # 免责声明 + 数据来源
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "note",
            "elements": [{
                "tag": "plain_text",
                "content": (
                    f"📅 生成时间：{now_str} | "
                    "数据来源：财联社/东方财富/新浪财经/Yahoo Finance/AKShare/美联储/HKEX | "
                    "⚠️ 本报告基于公开数据自动生成，仅供参考，不构成投资建议，投资有风险，决策需谨慎"
                )
            }]
        })

        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{icon} {market_label}开盘前分析 · {now_str}"
                },
                "template": header_color,
            },
            "elements": elements,
        }

    # ── 卡片构建：收盘复盘 ──────────────────────────────────────────────

    def _build_postmarket_card(self, analysis, market_label: str) -> dict:
        now_str = datetime.now(CST).strftime("%m月%d日 %H:%M")
        elements = []

        # 今日总结
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**📊 今日市场复盘**\n{analysis.market_summary}"
            }
        })
        elements.append({"tag": "hr"})

        # 早晨建议回顾
        if analysis.review_of_yesterday:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**🔄 今日建议执行情况回顾**\n{analysis.review_of_yesterday}"
                }
            })
            elements.append({"tag": "hr"})

        # 今日关键事件
        key_events = analysis.key_events[:4]
        if key_events:
            event_lines = ["**🔔 今日关键事件**\n"]
            for ev in key_events:
                direction = ev.get("impact_direction", "neutral")
                dir_icon = {"positive": "📈", "negative": "📉", "neutral": "➡️"}.get(direction, "➡️")
                event_lines.append(
                    f"{dir_icon} **{ev.get('title', '')}**\n"
                    f"　来源：[{ev.get('source', '')}]({ev.get('source_url', '#')})\n"
                    f"　影响：{ev.get('transmission_chain', '')[:80]}"
                )
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": "\n".join(event_lines)}
            })
            elements.append({"tag": "hr"})

        # 明日操作建议
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**💡 明日操作建议**\n{analysis.trading_strategy}"
            }
        })

        # 明日重点关注
        watchlist = analysis.watchlist[:6]
        if watchlist:
            watch_lines = ["\n**🎯 明日重点关注标的**\n"]
            for w in watchlist:
                action = w.get("action", "观望")
                action_icon = {"关注买入": "🟢", "关注卖出": "🔴", "观望": "⚪"}.get(action, "⚪")
                watch_lines.append(
                    f"{action_icon} **{w.get('name')}({w.get('code')})** [{w.get('market')}] "
                    f"— {w.get('rationale', '')[:60]}"
                )
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": "\n".join(watch_lines)}
            })

        # 风险提示
        if analysis.risk_warnings:
            elements.append({"tag": "hr"})
            risk_text = "\n".join(f"⚠️ {r}" for r in analysis.risk_warnings[:3])
            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": f"**风险提示**\n{risk_text}"}
            })

        elements.append({"tag": "hr"})
        elements.append({
            "tag": "note",
            "elements": [{
                "tag": "plain_text",
                "content": (
                    f"📅 复盘时间：{now_str} | "
                    "数据来源：财联社/东方财富/新浪财经/Yahoo Finance/AKShare | "
                    "⚠️ 本报告基于公开数据自动生成，仅供参考，不构成投资建议"
                )
            }]
        })

        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📋 {market_label}收盘复盘 · {now_str}"
                },
                "template": "indigo",
            },
            "elements": elements,
        }

    # ── 发送逻辑 ───────────────────────────────────────────────────────

    def _send_card(self, card: dict) -> bool:
        """发送消息卡片：自建应用模式优先，降级到 Webhook"""
        if self.app_mode:
            return self._send_card_via_api(card)
        return self._send_card_via_webhook(card)

    def _send_card_via_api(self, card: dict) -> bool:
        """通过自建应用 API 发送消息卡片（支持多群）"""
        try:
            token = self._get_tenant_access_token()
        except Exception as e:
            logger.error(f"[Feishu API] 获取 token 失败: {e}，尝试降级到 Webhook")
            if self.webhook_urls:
                return self._send_card_via_webhook(card)
            return False

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        success_count = 0
        for chat_id in self.chat_ids:
            payload = {
                "receive_id": chat_id,
                "msg_type": "interactive",
                "content": json.dumps(card, ensure_ascii=False),
            }
            try:
                r = requests.post(
                    f"{_FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id",
                    headers=headers,
                    json=payload,
                    timeout=self.TIMEOUT,
                )
                data = r.json()
                if data.get("code") == 0:
                    logger.info(f"[Feishu API] 推送成功 → chat_id={chat_id[:12]}...")
                    success_count += 1
                else:
                    logger.error(f"[Feishu API] 推送失败: {data}")
            except Exception as e:
                logger.error(f"[Feishu API] 推送异常: {e}")
        return success_count > 0

    def _send_card_via_webhook(self, card: dict) -> bool:
        """通过 Webhook 发送消息卡片（群自定义机器人）"""
        payload = {
            "msg_type": "interactive",
            "card": card,
        }
        if self.secret:
            ts, sign = self._generate_sign(self.secret)
            payload["timestamp"] = ts
            payload["sign"] = sign

        success_count = 0
        for url in self.webhook_urls:
            try:
                r = requests.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=self.TIMEOUT,
                )
                resp = r.json()
                if resp.get("code") == 0 or resp.get("StatusCode") == 0:
                    logger.info(f"[Webhook] 推送成功: {url[:50]}...")
                    success_count += 1
                else:
                    logger.error(f"[Webhook] 推送失败: {resp}")
            except Exception as e:
                logger.error(f"[Webhook] 推送异常: {e}")
        return success_count > 0

    def _send_text(self, text: str) -> bool:
        """发送纯文本消息（降级方案，仅 Webhook 模式）"""
        if self.app_mode:
            # API 模式走单独文本接口（简化处理，将文本包装为卡片）
            card = {
                "config": {"wide_screen_mode": False},
                "elements": [{"tag": "div", "text": {"tag": "plain_text", "content": text}}],
            }
            return self._send_card_via_api(card)

        payload = {"msg_type": "text", "content": {"text": text}}
        if self.secret:
            ts, sign = self._generate_sign(self.secret)
            payload["timestamp"] = ts
            payload["sign"] = sign

        for url in self.webhook_urls:
            try:
                r = requests.post(url, json=payload, timeout=self.TIMEOUT)
                if r.status_code == 200:
                    return True
            except Exception as e:
                logger.error(f"飞书文本推送失败: {e}")
        return False

    @staticmethod
    def _generate_sign(secret: str) -> tuple[str, str]:
        """飞书签名校验"""
        timestamp = str(int(time.time()))
        string_to_sign = f"{timestamp}\n{secret}"
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        sign = base64.b64encode(hmac_code).decode("utf-8")
        return timestamp, sign
