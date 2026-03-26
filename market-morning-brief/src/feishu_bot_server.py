"""
飞书 Q&A 机器人服务器
支持两种方式与 Claude 进行金融分析问答：

方式一：命令行直接提问（立即生效，无需额外配置）
  python src/main.py --ask "碧桂园利润预期对港股有何影响？"

方式二：飞书群内 @机器人 提问（需要飞书自建应用）
  1. 在飞书开放平台 (open.feishu.cn) 创建自建应用
  2. 开启权限：接收群聊消息 (im:message)
  3. 开启事件订阅 → 配置回调 URL: http://your-ip:5000/webhook
  4. 在 .env 中设置：
       FEISHU_BOT_ENABLED=true
       FEISHU_VERIFICATION_TOKEN=从飞书开发平台事件订阅页面获取
  5. 重启程序，群内 @机器人 即可提问
"""

import json
import logging
import threading
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

logger = logging.getLogger(__name__)
CST = timezone(timedelta(hours=8))

# 防重放：记录已处理的 event_id（内存级，重启清空）
_processed_events: set[str] = set()
_processed_events_lock = threading.Lock()
_MAX_EVENT_CACHE = 5000


def _dedup_event(event_id: str) -> bool:
    """返回 True 表示首次处理，False 表示重复事件"""
    with _processed_events_lock:
        if event_id in _processed_events:
            return False
        _processed_events.add(event_id)
        if len(_processed_events) > _MAX_EVENT_CACHE:
            # 简单清半，保持内存稳定
            to_remove = list(_processed_events)[:_MAX_EVENT_CACHE // 2]
            for e in to_remove:
                _processed_events.discard(e)
        return True


# ══════════════════════════════════════════════════════════════════════
#  Q&A 核心：调用 AI 引擎回答金融问题
# ══════════════════════════════════════════════════════════════════════

class FeishuQABot:
    """
    飞书金融问答机器人
    - 接收用户问题
    - 获取最新新闻作为上下文
    - 调用已配置的 AI 引擎（Claude/OpenAI/Gemini）生成回答
    - 通过飞书 API 推送到群
    """

    def __init__(self, orchestrator, notifier):
        self.orchestrator = orchestrator
        self.notifier = notifier

    def answer_and_push(self, question: str, sender_name: str = "用户") -> bool:
        """
        回答问题并推送到飞书
        返回 True 表示成功
        """
        logger.info(f"[Q&A] 收到问题：{question[:80]}")
        try:
            answer = self._generate_answer(question)
            card = self._build_qa_card(question, answer, sender_name)
            success = self.notifier._send_card(card)
            logger.info(f"[Q&A] 推送{'成功' if success else '失败'}")
            return success
        except Exception as e:
            logger.error(f"[Q&A] 处理失败: {e}")
            # 发送简单错误提示
            try:
                self.notifier.send_alert("Q&A 处理失败", f"问题：{question[:100]}\n错误：{e}", level="error")
            except Exception:
                pass
            return False

    def _generate_answer(self, question: str) -> str:
        """调用已配置的 AI 引擎（Claude/OpenAI/Gemini）生成回答，降级到规则引擎"""
        # 获取最近新闻作为上下文（最多 20 条，4小时内）
        context_parts = []
        try:
            news_items = self.orchestrator.news_fetcher.fetch_all(hours=4)
            if news_items:
                context_parts.append("【最新市场新闻（过去4小时）】")
                for item in news_items[:20]:
                    item_dict = item.to_dict() if hasattr(item, "to_dict") else item
                    context_parts.append(f"- [{item_dict.get('source', '')}] {item_dict.get('title', '')}")
        except Exception as e:
            logger.warning(f"[Q&A] 获取新闻失败: {e}")

        context = "\n".join(context_parts) if context_parts else "（暂无最新新闻数据）"

        # 调用已配置的 AI 引擎
        analyzer = self.orchestrator.analyzer
        if hasattr(analyzer, "answer_question"):
            try:
                return analyzer.answer_question(question, context)
            except Exception as e:
                logger.warning(f"[Q&A] AI 调用失败: {e}，降级到规则引擎")

        # 降级：简单关键词分析
        return self._rule_based_answer(question, context_parts)

    def _rule_based_answer(self, question: str, news_titles: list[str]) -> str:
        """无 Claude 时的简单关键词回答"""
        related = [t for t in news_titles if any(kw in t for kw in question.split() if len(kw) > 1)]
        if related:
            news_part = "\n".join(related[:5])
            return (
                f"根据关键词匹配，与「{question[:30]}」相关的最新消息：\n\n"
                f"{news_part}\n\n"
                "⚠️ 当前使用规则引擎（未配置 ANTHROPIC_API_KEY），无法提供深度分析。\n"
                "请在 .env 文件中配置 ANTHROPIC_API_KEY 以启用 Claude 智能分析。"
            )
        return (
            f"未找到与「{question[:30]}」直接相关的最新新闻。\n\n"
            "建议：\n"
            "1. 尝试换一种提问方式\n"
            "2. 配置 ANTHROPIC_API_KEY 以获得 Claude 智能分析\n\n"
            "⚠️ 当前使用规则引擎，分析能力有限。"
        )

    def _build_qa_card(self, question: str, answer: str, sender_name: str) -> dict:
        """构建飞书消息卡片"""
        now_str = datetime.now(CST).strftime("%m月%d日 %H:%M")
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"💬 市场问答 · {now_str}"},
                "template": "indigo",
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**❓ {sender_name}的问题**\n{question}"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**🤖 Claude 分析**\n{answer}"
                    }
                },
                {"tag": "hr"},
                {
                    "tag": "note",
                    "elements": [{
                        "tag": "plain_text",
                        "content": "⚠️ 以上分析基于公开数据自动生成，仅供参考，不构成投资建议，投资有风险，决策需谨慎"
                    }]
                },
            ],
        }


# ══════════════════════════════════════════════════════════════════════
#  HTTP 服务器：接收飞书事件推送
# ══════════════════════════════════════════════════════════════════════

def _make_handler(qa_bot: FeishuQABot, verification_token: Optional[str]):
    """工厂函数：生成绑定了 qa_bot 的请求处理器"""

    class FeishuEventHandler(BaseHTTPRequestHandler):

        def log_message(self, format, *args):
            logger.debug(f"[Bot HTTP] {format % args}")

        def do_GET(self):
            """健康检查"""
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "feishu-qa-bot"}).encode())

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                payload = json.loads(body.decode("utf-8"))
            except Exception:
                self._respond(400, {"error": "invalid json"})
                return

            # ── v1.0 URL 验证 ────────────────────────────────────────
            if payload.get("type") == "url_verification":
                challenge = payload.get("challenge", "")
                logger.info(f"[Bot] 飞书 URL 验证请求 (v1)")
                self._respond(200, {"challenge": challenge})
                return

            # ── v2.0 URL 验证 ────────────────────────────────────────
            header = payload.get("header", {})
            event_type = header.get("event_type", payload.get("type", ""))
            if event_type == "url_verification":
                challenge = payload.get("event", {}).get("challenge", payload.get("challenge", ""))
                logger.info(f"[Bot] 飞书 URL 验证请求 (v2)")
                self._respond(200, {"challenge": challenge})
                return

            # ── Token 验证 ───────────────────────────────────────────
            if verification_token:
                token = header.get("token", payload.get("token", ""))
                if token != verification_token:
                    logger.warning("[Bot] Token 验证失败，忽略请求")
                    self._respond(403, {"error": "forbidden"})
                    return

            # ── 先回 200，再异步处理（飞书要求3秒内响应）────────────
            self._respond(200, {"code": 0})

            # 在新线程中处理消息，避免阻塞响应
            threading.Thread(
                target=self._process_event,
                args=(payload,),
                daemon=True,
            ).start()

        def _process_event(self, payload: dict):
            """处理飞书事件（在独立线程中运行）"""
            header = payload.get("header", {})
            event_type = header.get("event_type", payload.get("type", ""))
            event_id = header.get("event_id", "")

            # 防重放
            if event_id and not _dedup_event(event_id):
                logger.debug(f"[Bot] 重复事件，跳过: {event_id}")
                return

            # 只处理消息接收事件
            if event_type not in ("im.message.receive_v1", "message"):
                return

            event = payload.get("event", {})
            message = event.get("message", event)
            msg_type = message.get("message_type", message.get("msg_type", ""))

            if msg_type != "text":
                return

            # 提取消息文本
            content_raw = message.get("content", "{}")
            try:
                content_obj = json.loads(content_raw)
                text = content_obj.get("text", "").strip()
            except Exception:
                text = content_raw.strip()

            if not text:
                return

            # 去掉 @mention（飞书格式：<at user_id="xxx">...</at> 或 @名称）
            import re
            text = re.sub(r'<at[^>]*>[^<]*</at>', '', text).strip()
            text = re.sub(r'@\S+', '', text).strip()

            if not text:
                return

            # 获取发送者名称
            sender = event.get("sender", {})
            sender_id = sender.get("sender_id", {})
            sender_name = sender_id.get("user_id", "用户")

            logger.info(f"[Bot] 收到消息 from {sender_name}: {text[:80]}")
            qa_bot.answer_and_push(text, sender_name)

        def _respond(self, code: int, body: dict):
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return FeishuEventHandler


def run_bot_server(
    qa_bot: FeishuQABot,
    port: int = 5000,
    verification_token: Optional[str] = None,
) -> threading.Thread:
    """
    在后台线程启动飞书事件接收服务器
    返回线程对象（daemon=True，主程序退出时自动停止）
    """
    handler_class = _make_handler(qa_bot, verification_token)
    server = ThreadingHTTPServer(("0.0.0.0", port), handler_class)

    def _serve():
        logger.info(f"[Bot] 飞书 Q&A 机器人服务器已启动，监听端口 {port}")
        logger.info(f"[Bot] 事件回调 URL: http://your-server-ip:{port}/webhook")
        logger.info(f"[Bot] 健康检查: http://localhost:{port}/")
        server.serve_forever()

    t = threading.Thread(target=_serve, daemon=True, name="feishu-bot-server")
    t.start()
    return t
