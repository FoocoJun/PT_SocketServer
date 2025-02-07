class DataDispatcher:
    def __init__(self, aws_handler):
        self.aws_handler = aws_handler
        self.client_handler = None

    async def handle_audio(self, audio_data):
        # ✅ 더미 연결 호출
        await self.aws_handler.connect("wss://dummy-aws-transcribe")
        
        # ✅ AWSHandler로 데이터 전송 (더미 데이터 반환)
        await self.aws_handler.send_audio(audio_data, self.handle_partial)

    async def handle_partial(self, partial_result):
        print(f"📝 Partial Result: {partial_result}")
        
        # ✅ Unity로 Partial 결과 전송
        if self.client_handler:
            await self.client_handler.send_to_unity(partial_result)
