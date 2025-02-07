class ClientHandler:
    def __init__(self, websocket, data_dispatcher):
        self.websocket = websocket
        self.data_dispatcher = data_dispatcher
        self.data_dispatcher.client_handler = self  # DataDispatcher가 ClientHandler를 참조할 수 있도록 설정

    async def process(self, audio_data):
        # DataDispatcher로 음성 데이터 전달
        await self.data_dispatcher.handle_audio(audio_data)

    async def send_to_unity(self, partial_result):
        # Unity로 Partial 데이터 전송
        await self.websocket.send_str(f"📝 Partial Result: {partial_result}")
