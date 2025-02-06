import asyncio
import websockets
from handlers.client_handler import ClientHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def handle_client(self, websocket, path):
        print("✅ Client connected!")  # 연결 성공 시 출력
        handler = ClientHandler(websocket)
        try:
            await handler.process()
        except websockets.ConnectionClosed as e:
            print(f"❌ Connection closed: {e}")  # 연결 종료 시 출력
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")   # 기타 오류 처리

    async def run_server(self):
        print(f"🚀 Server started at ws://{self.host}:{self.port}")
        async with websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            origins=["*"]  # CORS 허용
        ):
            await asyncio.Future()  # 서버가 종료되지 않도록 유지

    def start(self):
        asyncio.run(self.run_server())
