# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from openai import AzureOpenAI

from config import DefaultConfig

CONFIG = DefaultConfig()

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=CONFIG.ENDPOINT_URL,
    api_key=CONFIG.AZURE_OPENAI_API_KEY,
    api_version="2025-01-01-preview",
)


class EchoBot(ActivityHandler):

    # 当成员加入时的处理逻辑
    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    def ai_chat(self, user_msg:str):
        # Prepare the chat prompt
        chat_prompt = [
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "text",
                            "text": "你是一个帮助用户查找信息的 AI 助手。"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_msg
                        }
                    ]
                },
        ]

        # Include speech result if speech is enabled
        messages = chat_prompt

        # Generate the completion
        completion = client.chat.completions.create(
            model=CONFIG.DEPLOYMENT_NAME,
            messages=messages,
            max_completion_tokens=100000,
            stop=None,
            stream=False
        )
    
        return completion

    # 当收到消息时的处理逻辑
    async def on_message_activity(self, turn_context: TurnContext):
        
        resp = self.ai_chat(turn_context.activity.text)

        return await turn_context.send_activity(
            MessageFactory.text(f"{resp.choices[0].message.content}")
        )
    
