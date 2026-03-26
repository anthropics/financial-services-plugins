"""
Claude 分析引擎
"""

import logging

import anthropic

from .base_analyzer import BaseAnalyzer, AnalysisResult, FIRST_PRINCIPLES_SYSTEM_PROMPT, QA_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ClaudeAnalyzer(BaseAnalyzer):
    """使用 Claude API 进行市场分析"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def _call_api(self, prompt: str, report_type: str) -> AnalysisResult:
        logger.info(f"[Claude] 调用 {self.model}: {report_type}")
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=FIRST_PRINCIPLES_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        return self._parse_result(raw, report_type)

    def answer_question(self, question: str, context: str) -> str:
        prompt = f"以下是当前市场最新动态：\n\n{context}\n\n---\n用户问题：{question}\n\n请基于以上信息和你的金融专业知识回答。"
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=QA_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
