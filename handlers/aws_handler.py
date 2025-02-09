import asyncio
import boto3
import json
import websockets
import os
from dotenv import load_dotenv
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from urllib.parse import urlencode

# ✅ 환경 변수 로드
load_dotenv()
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
        session = boto3.Session()
        credentials = session.get_credentials()
        region = AWS_REGION
        service = 'transcribe'

        host = f'transcribestreaming.{region}.amazonaws.com:8443'
        endpoint = f'wss://{host}/stream-transcription-websocket'

        params = {
            "language-code": "en-US",
            "media-encoding": "pcm",
            "sample-rate": "16000"
        }

        request = AWSRequest(
            method='GET',
            url=f"{endpoint}?{urlencode(params)}",
            headers={"host": host}
        )

        # ✅ 서명 추가
        SigV4Auth(credentials, service, region).add_auth(request)

        return request.url

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
    async def send_audio(self, audio_data, callback):
        if not self.connection:
            await self.start_transcribe_stream(callback)

        try:
            await self.connection.send(audio_data)  # ✅ Binary 데이터 전송
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
                try:
                    response = json.loads(message)
                    await callback(response)
                except json.JSONDecodeError:
                    print(f"⚠️ Failed to decode AWS response: {message}")
        except websockets.ConnectionClosed as e:
            print(f"🔌 AWS Transcribe connection closed: {e}")

    # ✅ 연결 종료
    async def disconnect(self):
        if self.connection and not self.connection.closed:
            await self.connection.close()
            print("🔌 AWS Transcribe connection closed.")
        else:
            print("⚠️ No active connection to close.")
