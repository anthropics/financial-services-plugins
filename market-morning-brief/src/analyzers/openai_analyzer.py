"""
OpenAI (ChatGPT) 分析引擎
"""

import logging

from .base_analyzer import BaseAnalyzer, AnalysisResult, FIRST_PRINCIPLES_SYSTEM_PROMPT, QA_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class OpenAIAnalyzer(BaseAnalyzer):
    """使用 OpenAI API (GPT-4o 等) 进行市场分析"""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def _call_api(self, prompt: str, report_type: str) -> AnalysisResult:
        logger.info(f"[OpenAI] 调用 {self.model}: {report_type}")
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": FIRST_PRINCIPLES_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content.strip()
        return self._parse_result(raw, report_type)

    def answer_question(self, question: str, context: str) -> str:
        prompt = f"以下是当前市场最新动态：\n\n{context}\n\n---\n用户问题：{question}\n\n请基于以上信息和你的金融专业知识回答。"
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": QA_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
