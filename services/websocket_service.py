import asyncio
import websockets
from aiohttp import web  # 추가: HTTP 서버 처리를 위한 aiohttp
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
        return web.Response(text="OK")  # Render의 헬스 체크 요청에 OK 반환

    async def run_server(self):
        print(f"🚀 Server started at ws://{self.host}:{self.port}")

        # HTTP 서버와 WebSocket 서버 동시 실행
        app = web.Application()
        app.router.add_get("/", self.health_check)  # 헬스 체크 엔드포인트 추가

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        # WebSocket 서버 시작
        async with websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            origins=["*"]  # 모든 출처 허용
        ):
            await asyncio.Future()  # 서버가 종료되지 않도록 유지

    def start(self):
        asyncio.run(self.run_server())
