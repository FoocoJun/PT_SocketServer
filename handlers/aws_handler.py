import asyncio
import boto3
import json
import websockets
import os
from dotenv import load_dotenv

# ✅ 환경 변수 로드
load_dotenv()
AWS_REGION = os.getenv("AWS_REGION")

class AWSHandler:
    def __init__(self):
        self.connection = None
        self.transcribe_client = boto3.client('transcribe', region_name=AWS_REGION)

    async def connect(self):
        try:
            response = self.transcribe_client.list_transcription_jobs(MaxResults=1)
            print("✅ Successfully connected to AWS Transcribe!")
        except Exception as e:
            print(f"❌ Failed to connect to AWS Transcribe: {e}")
            return False
        return True

    async def send_audio(self, audio_data, callback):
        if not self.connection:
            await self.start_transcribe_stream(callback)

        await self.connection.send(audio_data)

    async def start_transcribe_stream(self, callback):
        try:
            url = "wss://transcribestreaming.{region}.amazonaws.com:8443/stream-transcription-websocket" \
                  "?language-code=en-US&media-encoding=pcm&sample-rate=16000".format(region=AWS_REGION)

            self.connection = await websockets.connect(url)
            print("🎙️ AWS Transcribe streaming started!")

            asyncio.create_task(self.receive_transcribe_data(callback))

        except Exception as e:
            print(f"❌ Failed to start AWS Transcribe stream: {e}")

    async def receive_transcribe_data(self, callback):
        try:
            async for message in self.connection:
                response = json.loads(message)
                await callback(response)  # ✅ Unity로 전달
        except websockets.ConnectionClosed:
            print("🔌 AWS Transcribe connection closed.")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            print("🔌 AWS Transcribe connection closed.")
