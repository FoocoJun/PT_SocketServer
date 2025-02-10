import asyncio
from handlers.aws_event_formatter import create_audio_event, decode_event

class DataDispatcher:
    def __init__(self, aws_handler):
        self.aws_handler = aws_handler
        self.client_handler = None
        self.is_streaming = False  # ✅ 스트리밍 상태 관리

    async def start_streaming(self):
        if not self.is_streaming:
            print("🎙️ Starting AWS Transcribe stream")
            await self.aws_handler.start_transcribe_stream(self.handle_aws_response)
            self.is_streaming = True

    async def stop_streaming(self):
        if self.is_streaming:
            print("🛑 Stopping AWS Transcribe stream")
            
            # ✅ Final 응답 플래그 초기화
            self.final_response_received = False
            
            # ✅ 빈 오디오 데이터 전송 (스트림 종료 신호)
            await self.aws_handler.send_audio(create_audio_event(b''), self.handle_aws_response)

            # ✅ Final 응답 수신 대기
            try:
                await asyncio.wait_for(self.await_final_response(), timeout=5)
            except asyncio.TimeoutError:
                print("⚠️ Final response timeout. Proceeding to close connection.")

            await self.aws_handler.disconnect()
            self.is_streaming = False

    async def handle_audio(self, raw_audio_data):
        if self.is_streaming:
            # ✅ 오디오 데이터 포맷 변환 및 전송
            formatted_audio = create_audio_event(raw_audio_data)
            print(f"🎯 Audio data formatted for AWS")
            await self.aws_handler.send_audio(formatted_audio, self.handle_aws_response)

    async def handle_aws_response(self, aws_message):
        try:
            headers, transcript_payload = decode_event(aws_message)
            print(f"📝 Decoded AWS Response: {transcript_payload}")

            # ✅ Final 응답 도착 시 플래그 설정
            results = transcript_payload.get('Transcript', {}).get('Results', [])
            if results and not results[0].get('IsPartial', True):
                self.final_response_received = True

            if self.client_handler:
                await self.client_handler.send_to_unity(transcript_payload)

        except Exception as e:
            print(f"⚠️ Failed to handle AWS response: {e}")

    async def await_final_response(self):
        print("⏳ Waiting for Final AWS response...")

        for _ in range(50):  # 50 x 0.1초 = 최대 5초 대기
            if self.final_response_received:
                print("✅ Final response received.")
                break
            await asyncio.sleep(0.1)

    async def close(self):
        if self.is_streaming:
            await self.stop_streaming()  # ✅ 스트리밍 종료 처리

        if hasattr(self.aws_handler, "disconnect"):
            await self.aws_handler.disconnect()
            print("🔌 AWSHandler disconnected")
