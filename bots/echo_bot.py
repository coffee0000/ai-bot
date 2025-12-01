# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from openai import AzureOpenAI

from config import DefaultConfig

CONFIG = DefaultConfig()

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=CONFIG.ENDPOINT_URL,
    api_key=CONFIG.AZURE_OPENAI_API_KEY,
    api_version=CONFIG.AZURE_OPENAI_API_VERSION,
)


class EchoBot(ActivityHandler):
    """Bot Framework ActivityHandler 的实现"""

    def __init__(self):
        """初始化机器人"""
        self.system_prompt = "你是一个帮助用户查找信息的 AI 助手。请用简洁清晰的方式回答用户的问题。"

    # 当成员加入时的处理逻辑
    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ):
        """处理成员加入事件"""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text("你好！我是 AI 助手，很高兴为您服务。")
                )

    async def ai_chat(self, user_msg: str) -> str:
        """
        与 Azure OpenAI 进行聊天
        
        Args:
            user_msg: 用户消息
            
        Returns:
            AI响应的消息内容
        """
        import traceback
        try:
            # 打印诊断信息
            print(f"Azure OpenAI endpoint: {CONFIG.ENDPOINT_URL}")
            print(f"Azure OpenAI deployment: {CONFIG.DEPLOYMENT_NAME}")

            # 准备聊天消息
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_msg
                },
            ]

            # 调用 Azure OpenAI 生成响应
            completion = client.chat.completions.create(
                model=CONFIG.DEPLOYMENT_NAME,
                messages=messages,
                max_completion_tokens=1000,
                temperature=1,
                stop=None,
                stream=False
            )
            
            # 提取并返回响应内容
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error in ai_chat: {e}")
            traceback.print_exc()
            return "抱歉，我无法处理您的请求。请稍后重试。"

    # 当收到消息时的处理逻辑
    async def on_message_activity(self, turn_context: TurnContext):
        """处理消息活动"""
        user_message = turn_context.activity.text
        
        # 调用 AI 聊天方法获取响应
        response_text = await self.ai_chat(user_message)
        
        # 发送响应给用户
        await turn_context.send_activity(
            MessageFactory.text(response_text)
        )
