import json
from handlers.aws_event_formatter import create_audio_event, decode_event

class DataDispatcher:
    def __init__(self, aws_handler):
        self.aws_handler = aws_handler
        self.client_handler = None

    async def handle_audio(self, raw_audio_data):
        # ✅ 1. 클라이언트에서 받은 원시 오디오 데이터를 AWS 포맷으로 가공
        formatted_audio = create_audio_event(raw_audio_data)
        print(f"🎯 Audio data formatted for AWS")

        # ✅ 2. 가공된 데이터를 AWS로 전송
        await self.aws_handler.send_audio(formatted_audio, self.handle_aws_response)

    async def handle_aws_response(self, aws_message):
        try:
            # ✅ 3. AWS 응답 디코딩
            headers, transcript_payload = decode_event(aws_message)
            print(f"📝 Decoded AWS Response: {transcript_payload}")

            # ✅ 4. JSON 데이터 변환
            # 작은따옴표 → 큰따옴표, 대문자 → 소문자 변환은 json 모듈로 처리
            try:
                # 문자열이 JSON 형식이 아닌 경우 예외 처리
                transcript_payload = json.loads(transcript_payload)
            except json.JSONDecodeError as json_error:
                print(f"⚠️ JSON 디코딩 오류: {json_error}")
                return

            # ✅ 5. Unity 클라이언트로 전송
            if self.client_handler:
                await self.client_handler.send_to_unity(json.dumps(transcript_payload))

        except Exception as e:
            print(f"⚠️ Failed to handle AWS response: {e}")

    async def close(self):
        if hasattr(self.aws_handler, "disconnect"):
            await self.aws_handler.disconnect()
            print("🔌 AWSHandler disconnected")
