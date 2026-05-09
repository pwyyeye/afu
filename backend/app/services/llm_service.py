from typing import List, Dict
from app.config import settings

# Mock responses for development when no API key is configured
MOCK_RESPONSES = {
    "头疼": "头疼是很常见的症状，可能由多种原因引起：\n\n**常见原因：**\n1. 紧张性头疼：压力大、睡眠不足、长时间用眼\n2. 偏头疼：一侧搏动性疼痛，可能伴有恶心\n3. 颈椎问题：长期伏案工作导致\n\n**建议：**\n- 保证充足睡眠（7-8小时）\n- 适当休息，每工作1小时活动5分钟\n- 多喝水，保持身体水分充足\n- 如果持续3天以上或加重，建议就医\n\n以上内容仅供参考，不构成医疗建议。如有不适，请及时前往正规医疗机构就诊。",
    "default": "感谢您的提问！作为AI健康助手，我会尽力为您提供有用的健康建议。\n\n不过，目前我需要更详细的信息才能给出更准确的建议。请您描述一下：\n\n1. 症状的具体表现\n2. 持续了多长时间\n3. 是否有其他伴随症状\n\n以上内容仅供参考，不构成医疗建议。如有不适，请及时前往正规医疗机构就诊。"
}


class LLMService:
    def __init__(self):
        self._client = None
        self._vl_client = None
        self._mock_mode = not settings.DASHSCOPE_API_KEY

    @property
    def client(self):
        if self._mock_mode:
            return None
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                api_key=settings.DASHSCOPE_API_KEY,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        return self._client

    @property
    def vl_client(self):
        if self._mock_mode:
            return None
        if self._vl_client is None:
            from openai import OpenAI
            self._vl_client = OpenAI(
                api_key=settings.DASHSCOPE_API_KEY,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        return self._vl_client

    def _get_mock_response(self, content: str) -> str:
        for keyword, response in MOCK_RESPONSES.items():
            if keyword in content and keyword != "default":
                return response
        return MOCK_RESPONSES["default"]

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        if self._mock_mode:
            user_content = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    user_content = msg["content"]
                    break
            return self._get_mock_response(user_content)

        model = model or settings.QWEN_MODEL
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        if self._mock_mode:
            user_content = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    user_content = msg["content"]
                    break
            response = self._get_mock_response(user_content)
            # Simulate streaming by yielding characters
            for i in range(0, len(response), 5):
                yield response[i:i+5]
            return

        model = model or settings.QWEN_MODEL
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def analyze_image(
        self,
        image_base64: str,
        prompt: str,
        model: str = None,
        temperature: float = 0.3,
    ) -> str:
        if self._mock_mode:
            return "这是一张图片。在开发模式下，AI视觉分析功能需要配置DASHSCOPE_API_KEY才能使用。请在.env文件中设置您的API密钥。"

        model = model or settings.QWEN_VL_MODEL
        response = self.vl_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.3,
    ) -> str:
        if self._mock_mode:
            return '{"indicators": [], "overall_light": "green", "summary": "开发模式下需要配置API密钥才能分析报告", "action_plan": []}'

        model = model or settings.QWEN_MODEL
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content


llm_service = LLMService()
