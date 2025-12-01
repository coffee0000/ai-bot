import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from botbuilder.core import TurnContext
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes

from bots import EchoBot
from config import DefaultConfig

CONFIG = DefaultConfig()

# 创建 FastAPI 应用
app = FastAPI(title="AI Chat Bot", version="1.0.0")

# 创建 Bot Framework 适配器
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))

# 错误处理回调
async def on_error(context: TurnContext, error: Exception):
    """处理 Bot Framework 错误"""
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # 发送错误消息给用户
    await context.send_activity("抱歉，机器人遇到了一个错误。")
    await context.send_activity("请稍后重试。")
    
    # 在模拟器中发送追踪信息
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

# 创建 Bot 实例
BOT = EchoBot()

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok"}

# Bot Framework 消息处理端点
@app.post("/api/messages")
async def messages(req: Request):
    """处理来自 Bot Framework 的消息

    注意：当应用在容器内运行且本地使用 Bot Framework Emulator 时，Activity 中的
    `serviceUrl` 可能指向 `localhost:<port>`（即宿主机的地址）。容器内的 `localhost`
    指向容器自身，导致容器内代码尝试连接 `localhost:<port>` 时被拒绝。

    解决方法：在传入请求进入 Adapter 之前，把 `serviceUrl` 中的 `localhost` 替换为
    `host.docker.internal`（或由环境变量 `HOST_ALIAS` 指定的主机别名），这样容器
    内的进程能正确访问宿主机上的 Emulator。
    """
    from starlette.requests import Request as StarletteRequest
    import json
    import os

    try:
        # 读取原始请求体并尝试替换 serviceUrl 中的 localhost
        body_bytes = await req.body()
        if body_bytes:
            try:
                payload = json.loads(body_bytes)
            except Exception:
                payload = None

            if isinstance(payload, dict):
                # 只有在本地开发模式（设置了 HOST_ALIAS）时才替换 localhost
                host_alias = os.environ.get("HOST_ALIAS", None)

                if host_alias:
                    svc = payload.get("serviceUrl")
                    if isinstance(svc, str) and "localhost" in svc:
                        payload["serviceUrl"] = svc.replace("localhost", host_alias)

                        # 重新构造一个 Starlette Request，传给 Adapter
                        modified_body = json.dumps(payload).encode("utf-8")
                        scope = req.scope

                        async def receive() -> dict:
                            return {"type": "http.request", "body": modified_body, "more_body": False}

                        new_req = StarletteRequest(scope, receive)
                        response = await ADAPTER.process(new_req, BOT)
                        if response is None:
                            return JSONResponse(status_code=HTTPStatus.OK, content={"status": "ok"})
                        return response
                
                # 生产环境或未设置 HOST_ALIAS 时，直接用原始 Request（不替换）
                    response = await ADAPTER.process(new_req, BOT)
                    if response is None:
                        return JSONResponse(status_code=HTTPStatus.OK, content={"status": "ok"})
                    return response

        # 默认路径：直接传入原始 Request
        response = await ADAPTER.process(req, BOT)
        if response is None:
            return JSONResponse(status_code=HTTPStatus.OK, content={"status": "ok"})
        return response
    except Exception as e:
        print(f"Error in /api/messages: {e}", file=sys.stderr)
        traceback.print_exc()
        return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content={"error": str(e)})

# 运行 FastAPI 应用
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=CONFIG.PORT,
        log_level="info"
    )
