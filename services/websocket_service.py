import asyncio
from aiohttp import web
import websockets
from handlers.client_handler import ClientHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def websocket_handler(self, request):
        # WebSocket 핸드셰이크 처리
        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)

        print("✅ WebSocket client connected!")
        handler = ClientHandler(ws_current)
        try:
            async for msg in ws_current:
                if msg.type == web.WSMsgType.TEXT:
                    await handler.process(msg.data)
                elif msg.type == web.WSMsgType.ERROR:
                    print(f"❌ WebSocket error: {ws_current.exception()}")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
        finally:
            print("🔒 WebSocket connection closed.")
        return ws_current

    async def health_check(self, request):
        # Render 헬스 체크를 위한 엔드포인트
        return web.Response(text="OK")

    def start(self):
        app = web.Application()
        app.router.add_get("/", self.health_check)            # 헬스 체크 엔드포인트
        app.router.add_get("/ws", self.websocket_handler)     # WebSocket 엔드포인트

        print(f"🚀 Server started at ws://{self.host}:{self.port}")
        web.run_app(app, host=self.host, port=self.port)
