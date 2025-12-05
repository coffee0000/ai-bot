# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from ai.AIService import AIService

class EchoBot(ActivityHandler):
    def __init__(self):
        self.ai_service = AIService()

    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        ai_response = self.ai_service.ai_chat(user_message)

        return await turn_context.send_activity(
            MessageFactory.text(f"{ai_response}")
        )
