"""
Google Gemini 分析引擎
"""

import logging

from .base_analyzer import BaseAnalyzer, AnalysisResult, FIRST_PRINCIPLES_SYSTEM_PROMPT, QA_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class GeminiAnalyzer(BaseAnalyzer):
    """使用 Google Gemini API 进行市场分析"""

    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model_name = model
        self.genai = genai

    def _call_api(self, prompt: str, report_type: str) -> AnalysisResult:
        logger.info(f"[Gemini] 调用 {self.model_name}: {report_type}")
        model = self.genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=FIRST_PRINCIPLES_SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json", "max_output_tokens": 4096},
        )
        response = model.generate_content(prompt)
        raw = response.text.strip()
        return self._parse_result(raw, report_type)

    def answer_question(self, question: str, context: str) -> str:
        prompt = f"以下是当前市场最新动态：\n\n{context}\n\n---\n用户问题：{question}\n\n请基于以上信息和你的金融专业知识回答。"
        model = self.genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=QA_SYSTEM_PROMPT,
            generation_config={"max_output_tokens": 1024},
        )
        response = model.generate_content(prompt)
        return response.text.strip()
