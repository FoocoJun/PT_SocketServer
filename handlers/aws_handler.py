import asyncio
import random

class AWSHandler:
    def __init__(self):
        self.connection = None
        self.audio_counter = 0  # ✅ send_audio 호출 횟수 카운트

    async def connect(self, aws_ws_url):
        # # 실제 AWS 연결 (비활성화 상태)
        # self.connection = await websockets.connect(aws_ws_url)

        # ✅ 실제 연결 대신 더미 연결 처리
        self.connection = True
        print(f"🔗 [Dummy Mode] Pretending to connect to {aws_ws_url}")

    async def send_audio(self, audio_data, callback):
        if self.connection:
            # ✅ send_audio 호출 카운트 증가
            self.audio_counter += 1
            print(f"📤 [Dummy Mode] Sending audio data #{self.audio_counter}")

            # ✅ 3~5번 호출마다 Partial 데이터 전송
            if self.audio_counter % random.randint(3, 5) == 0:
                await self.send_mocked_partial_data(callback)

            # ✅ 7~10번 호출마다 Final 데이터 전송 (랜덤)
            if self.audio_counter % random.randint(7, 10) == 0:
                await self.send_mocked_final_data(callback)
        else:
            print("⚠️ No active connection (Dummy Mode)")

    async def send_mocked_partial_data(self, callback):
        dummy_partial = {
            "Transcript": {
                "Results": [
                    {
                        "Alternatives": [
                            {"Transcript": f"Mocked partial result #{self.audio_counter}"}
                        ],
                        "IsPartial": True
                    }
                ]
            }
        }
        await asyncio.sleep(0.5)  # ✅ 약간의 지연 시뮬레이션
        print(f"📥 [Dummy Mode] Sending Partial: {dummy_partial['Transcript']['Results'][0]['Alternatives'][0]['Transcript']}")
        await callback(dummy_partial)

    async def send_mocked_final_data(self, callback):
        dummy_final = {
            "Transcript": {
                "Results": [
                    {
                        "Alternatives": [
                            {"Transcript": "This is the final mocked result"}
                        ],
                        "IsPartial": False
                    }
                ]
            }
        }
        await asyncio.sleep(1)  # ✅ Final 데이터 지연
        print(f"🏁 [Dummy Mode] Sending Final: {dummy_final['Transcript']['Results'][0]['Alternatives'][0]['Transcript']}")
        await callback(dummy_final)

    async def disconnect(self):
        if self.connection:
            self.connection = None
            print("🔌 AWSHandler connection closed.")
