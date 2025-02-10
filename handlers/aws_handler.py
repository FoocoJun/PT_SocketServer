import asyncio
import boto3
import websockets
import os
from handlers.presigned_url_generator import AWSTranscribePresignedURL

# ✅ 환경 변수 로드
AWS_REGION = os.getenv("AWS_REGION")
AWS_SERVICE = "transcribe"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

class AWSHandler:
    def __init__(self):
        self.connection = None
        self.transcribe_client = boto3.client('transcribe', region_name=AWS_REGION)

    # ✅ Presigned URL 생성
    def generate_presigned_url(self):
        access_key = AWS_ACCESS_KEY
        secret_key = AWS_SECRET_KEY
        session_token = os.getenv("AWS_SESSION_TOKEN", "")  # 세션 토큰이 없는 경우 빈 문자열 처리
        region = AWS_REGION

        # ✅ Presigned URL 생성
        presigner = AWSTranscribePresignedURL(access_key, secret_key, session_token, region)
        presigned_url = presigner.get_request_url(sample_rate=16000, language_code="en-US")
        
        print(f"Generated Presigned URL: {presigned_url}")
        return presigned_url

    # ✅ AWS 연결 확인
    async def connect(self):
        try:
            response = self.transcribe_client.list_transcription_jobs(MaxResults=1)
            print("✅ Successfully connected to AWS Transcribe!")
        except Exception as e:
            print(f"❌ Failed to connect to AWS Transcribe: {e}")
            return False
        return True

    # ✅ 오디오 데이터 전송
    async def send_audio(self, formatted_audio, callback):
        if not self.connection:
            await self.start_transcribe_stream(callback)

        try:
            await self.connection.send(formatted_audio)  # ✅ 포맷된 데이터 전송
            print(f"📤 Sent formatted audio data to AWS")
        except Exception as e:
            print(f"⚠️ Error sending audio data: {e}")

    # ✅ AWS Transcribe 스트리밍 시작
    async def start_transcribe_stream(self, callback):
        try:
            presigned_url = self.generate_presigned_url()
            self.connection = await websockets.connect(presigned_url)
            print("🎙️ AWS Transcribe streaming started!")

            # ✅ AWS 데이터 수신 비동기 처리
            asyncio.create_task(self.receive_transcribe_data(callback))

        except Exception as e:
            print(f"❌ Failed to start AWS Transcribe stream: {e}")

    # ✅ AWS 데이터 수신
    async def receive_transcribe_data(self, callback):
        try:
            async for message in self.connection:
                callback(message);
        except websockets.ConnectionClosed:
            print("🔌 AWS Transcribe connection closed.")

    # ✅ 연결 종료
    async def disconnect(self):
        if self.connection and not self.connection.closed:
            await self.connection.close()
            print("🔌 AWS Transcribe connection closed.")
        else:
            print("⚠️ No active connection to close.")
