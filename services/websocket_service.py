import asyncio
import os
import websockets
from aiohttp import web
from handlers.client_handler import ClientHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def handle_client(self, websocket, path):
        print("✅ Client connected!")
        handler = ClientHandler(websocket)
        try:
            await handler.process()
        except websockets.ConnectionClosed as e:
            print(f"❌ Connection closed: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")

    async def health_check(self, request):
        return web.Response(text="OK")  # Render 헬스 체크용

    async def run_server(self):
        print(f"🚀 Server started at ws://{self.host}:{self.port}")

        # HTTP 서버 설정 (헬스 체크 용도)
        app = web.Application()
        app.router.add_get("/", self.health_check)  # 헬스 체크 엔드포인트 추가

        # WebSocket과 HTTP 서버를 같은 포트에서 처리
        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        # WebSocket 서버를 같은 포트에서 실행
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            origins=["*"]  # CORS 허용
        )

        await asyncio.Future()  # 서버 유지

    def start(self):
        asyncio.run(self.run_server())
