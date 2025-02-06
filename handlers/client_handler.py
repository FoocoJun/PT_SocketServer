class ClientHandler:
    def __init__(self, websocket):
        self.websocket = websocket

    async def process(self, message):  # message 인자 추가
        print(f"📥 Processing message: {message}")
        await self.websocket.send(f"Echo: {message}")  # 받은 메시지 그대로 반환
