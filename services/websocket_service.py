import asyncio
from aiohttp import web
from handlers.client_handler import ClientHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    # ✅ 모든 요청을 로깅하는 함수
    async def request_logger(self, request):
        print(f"🌐 Received {request.method} request for {request.path}")
        return web.Response(text="Request received")

    async def websocket_handler(self, request):
        print("📡 Incoming WebSocket connection...")
        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)

        print("✅ WebSocket client connected!")
        handler = ClientHandler(ws_current)
        try:
            async for msg in ws_current:
                print(f"📥 Received: {msg.data}")
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

        # 헬스 체크 및 WebSocket 라우팅
        app.router.add_get("/", self.health_check)
        app.router.add_get("/ws", self.websocket_handler)

        # ✅ 모든 요청 로깅 (404 에러 방지 및 디버깅용)
        app.router.add_route('*', '/{tail:.*}', self.request_logger)

        print(f"🚀 Server started at ws://{self.host}:{self.port}")
        web.run_app(app, host=self.host, port=self.port)
