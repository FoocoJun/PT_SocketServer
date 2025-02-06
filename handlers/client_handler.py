class ClientHandler:
    def __init__(self, websocket):
        self.websocket = websocket

    async def process(self):
        async for message in self.websocket:
            print(f"📥 Received from client: {message}")
            await self.websocket.send(f"Echo: {message}")
