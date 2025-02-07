import asyncio

class AWSHandler:
    def __init__(self):
        self.connection = None

    async def connect(self, aws_ws_url):
        # # AWS 컨넥넥
        # self.connection = await websockets.connect(aws_ws_url)

        # ✅ 실제 연결 대신 더미 연결 처리
        self.connection = True  # 더미 연결 상태 유지
        print(f"🔗 [Dummy Mode] Pretending to connect to {aws_ws_url}")

    async def send_audio(self, audio_data, callback):
        if self.connection:
            # # AWS로 데이터 전송
            # await self.connection.send(audio_data)

            # ✅ 실제 전송 대신 더미 Partial 데이터 반환
            print(f"📤 [Dummy Mode] Sending audio data: {audio_data}")
            await self.receive_partial(callback)
        else:
            print("⚠️ No active connection (Dummy Mode)")

    async def receive_partial(self, callback):
        # # Partial 결과를 DataDispatcher로 전달
        # async for message in self.connection:
        #     await callback(message)

        # ✅ 더미 Partial 데이터 생성
        dummy_partial = {"transcript": "This is a dummy partial result"}
        
        # ✅ 지연 시간 시뮬레이션
        await asyncio.sleep(1)
        
        # ✅ 콜백 호출로 더미 데이터 전달
        await callback(dummy_partial)
