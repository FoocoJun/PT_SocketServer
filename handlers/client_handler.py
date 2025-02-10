import json

class ClientHandler:
    def __init__(self, websocket, data_dispatcher):
        self.websocket = websocket
        self.data_dispatcher = data_dispatcher
        self.data_dispatcher.client_handler = self  # DataDispatcher가 ClientHandler를 참조할 수 있도록 설정
        self.is_streaming = False  # ✅ 스트리밍 상태 관리

    async def process(self, message):
        try:
            # ✅ 메시지가 JSON인지 확인하여 제어 메시지 처리
            data = json.loads(message)
            event = data.get("event")

            if event == "start_streaming":
                print("🎙️ Start Streaming Event Received")
                if not self.is_streaming:
                    await self.data_dispatcher.start_streaming()
                    self.is_streaming = True

            elif event == "stop_streaming":
                print("🛑 Stop Streaming Event Received")
                if self.is_streaming:
                    await self.data_dispatcher.stop_streaming()
                    self.is_streaming = False

        except json.JSONDecodeError:
            # ✅ JSON이 아닌 경우 오디오 데이터로 처리
            if self.is_streaming:
                await self.data_dispatcher.handle_audio(message)

    async def send_to_unity(self, partial_result):
        # ✅ 연결 상태 확인 후 데이터 전송
        if not self.websocket.closed:
            await self.websocket.send_str(f"📝 Partial Result: {partial_result}")
        else:
            print("⚠️ WebSocket is already closed. Skipping message.")

    async def close(self):
        # ✅ WebSocket 연결 종료
        if not self.websocket.closed:
            await self.websocket.close()
            print("🔒 WebSocket connection closed by ClientHandler.")

        # ✅ DataDispatcher를 통해 AWSHandler 연결 종료
        await self.data_dispatcher.close()

        print("✅ ClientHandler resources cleaned up.")
