import websockets
import asyncio
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

class AWSHandler:
    def __init__(self):
        self.aws_endpoint = "wss://transcribestreaming.ap-northeast-2.amazonaws.com"

    async def send_to_aws(self, data):
        headers = {"Authorization": "Bearer ${AWS_SECRET_KEY}"}

        async with websockets.connect(self.aws_endpoint, extra_headers=headers) as aws_ws:
            await aws_ws.send(data)  # Unity에서 받은 데이터 전송
            response = await aws_ws.recv()  # AWS로부터 partial 응답 받기
            return response
