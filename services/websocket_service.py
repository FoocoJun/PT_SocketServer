import asyncio
import aiohttp
from aiohttp import web
from handlers.client_handler import ClientHandler
from handlers.data_dispatcher import DataDispatcher
from handlers.aws_handler import AWSHandler
import os

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.ping_target = os.getenv("PING_TARGET")  # ✅ 환경 변수로 Ping 대상 서버 설정

    # ✅ Ping 보내는 비동기 함수
    async def ping_target_server(self):
        while True:
            if self.ping_target:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{self.ping_target}/health") as response:
                            print(f"🔗 Ping sent to {self.ping_target}, Status: {response.status}")
                except Exception as e:
                    print(f"⚠️ Ping failed: {e}")
            # ✅ 5~8분(300~480초) 사이의 랜덤 대기 시간
            wait_time = random.randint(300, 480)
            print(f"⏱️ Next ping in {wait_time // 60} minutes {wait_time % 60} seconds")
            await asyncio.sleep(wait_time)

    # ✅ 헬스 체크 엔드포인트
    async def health_check(self, request):
        return web.Response(text="OK")

    async def websocket_handler(self, request):
        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)

        print("✅ New WebSocket client connected!")

        aws_handler = AWSHandler()
        data_dispatcher = DataDispatcher(aws_handler)
        handler = ClientHandler(ws_current, data_dispatcher)

        data_dispatcher.client_handler = handler

        try:
            async for msg in ws_current:
                await handler.process(msg.data)
        except Exception as e:
            print(f"⚠️ Error: {e}")
        finally:
            print("🔒 WebSocket connection closed.")

        return ws_current

    async def start_server(self):
        app = web.Application()
        app.router.add_get("/ws", self.websocket_handler)
        app.router.add_get("/health", self.health_check)  # ✅ 헬스 체크 엔드포인트 추가

        print(f"🚀 Server started at ws://{self.host}:{self.port}")

        # ✅ 서버 구동과 Ping을 병렬로 실행
        await asyncio.gather(
            web._run_app(app, host=self.host, port=self.port),
            self.ping_target_server()  # Ping 기능 활성화
        )

    def start(self):
        asyncio.run(self.start_server())
