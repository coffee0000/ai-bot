from langchain_openai import AzureChatOpenAI, AzureOpenAI
from config import DefaultConfig

CONFIG = DefaultConfig()

class AIService:
    def __init__(self):
        self.model = self.__create_azure_openai_model()

    def __create_azure_openai_model(self):
        llm_model = AzureChatOpenAI(
            azure_endpoint=CONFIG.ENDPOINT_URL,
            azure_deployment=CONFIG.DEPLOYMENT_NAME,
            openai_api_version=CONFIG.AZURE_OPENAI_API_VERSION,
            api_key=CONFIG.AZURE_OPENAI_API_KEY,
            temperature=1,
            max_tokens=1000,
        )
        return llm_model
          

    def ai_chat(self, prompt: str) -> str:
        if not prompt:
            return "请输入有效的问题。"
        messages = [
            ("system", "你是一个帮助用户查找信息的 AI 助手。请用简洁清晰的方式回答用户的问题。"),
            ("human", prompt)
        ]
        response = self.model.invoke(messages)
        content = response.content if response else "内容为空。"
        return content