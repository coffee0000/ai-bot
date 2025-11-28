import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from botbuilder.core import TurnContext
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes

from bots import EchoBot
from config import DefaultConfig

CONFIG = DefaultConfig()

# 创建 FastAPI 应用
APP = FastAPI()

# 创建适配器
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))

# 错误处理函数
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # 发送错误消息
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity("To continue to run this bot, please fix the bot source code.")
    
    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)

ADAPTER.on_turn_error = on_error

# 创建Bot实例
BOT = EchoBot()

# 处理请求的路由
@APP.post("/api/messages")
async def messages(req: Request):
    return await ADAPTER.process(req, BOT)

# 运行 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=CONFIG.PORT)
