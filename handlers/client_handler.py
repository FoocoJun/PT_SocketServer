from handlers.aws_handler import AWSHandler

class ClientHandler:
    def __init__(self, client_ws):
        self.client_ws = client_ws
        self.aws_handler = AWSHandler()

    async def process(self):
        async for message in self.client_ws:
            print("🎧 Received from Unity:", message)
            aws_response = await self.aws_handler.send_to_aws(message)
            await self.client_ws.send(aws_response)
