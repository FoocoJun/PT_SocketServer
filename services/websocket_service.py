import asyncio
from aiohttp import web
from handlers.client_handler import ClientHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def websocket_handler(self, request):
        print("📡 Incoming WebSocket connection...")  # 핸드셰이크 직후 로그 추가
        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)

        print("✅ WebSocket client connected!")  # 핸드셰이크 성공 직후 로그

        handler = ClientHandler(ws_current)
        try:
            async for msg in ws_current:
                print(f"📥 Received: {msg.data}")  # 메시지 수신 확인
                await handler.process(msg.data)
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
        finally:
            print("🔒 WebSocket connection closed.")
        return ws_current

    async def health_check(self, request):
        print("💓 Health check received")
        return web.Response(text="OK")

    def start(self):
        app = web.Application()
        app.router.add_get("/", self.health_check)
        app.router.add_get("/ws", self.websocket_handler)

        print(f"🚀 Server started at ws://{self.host}:{self.port}")
        web.run_app(app, host=self.host, port=self.port)
