import asyncio
import websockets
from handlers.client_handler import ClientHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def handle_client(self, websocket, path):
        handler = ClientHandler(websocket)
        await handler.process()

    async def run_server(self):
        print(f"🚀 Server started at ws://{self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # 서버가 종료되지 않도록 대기

    def start(self):
        asyncio.run(self.run_server())  # 수정된 부분
