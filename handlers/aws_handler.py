import boto3
import os
from dotenv import load_dotenv
import asyncio
import websockets
import json

# ✅ 환경 변수 로드
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

class AWSHandler:
    def __init__(self):
        self.transcribe_client = boto3.client(
            'transcribe',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        self.connection = None

    async def connect(self):
        try:
            # ✅ Transcribe 연결 테스트
            response = self.transcribe_client.list_transcription_jobs(MaxResults=1)
            print("✅ Successfully connected to AWS Transcribe!")
        except Exception as e:
            print(f"❌ Failed to connect to AWS Transcribe: {e}")

    async def send_audio(self, audio_data, callback):
        # ✅ AWS로 데이터 전송 (추후 스트리밍 로직 추가)
        await asyncio.sleep(1)  # 더미 지연
        print(f"📤 Sending audio data to AWS: {audio_data[:10]}...")

        # ✅ 더미 Partial 데이터 반환
        dummy_partial = {
            "Transcript": {
                "Results": [
                    {
                        "Alternatives": [
                            {"Transcript": "Mocked partial result"}
                        ],
                        "IsPartial": True
                    }
                ]
            }
        }
        await callback(dummy_partial)

    async def disconnect(self):
        print("🔌 AWS Transcribe connection closed.")
