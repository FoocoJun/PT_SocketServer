from datetime import datetime

class ClientHandler:
    def __init__(self, websocket):
        self.websocket = websocket

    async def process(self, message):
        receive_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print(f"📥 [{receive_time} UTC] Processing message: {message}")

        # ✅ 클라이언트에 확인 메시지 보내기
        confirmation_message = f"✅ 잘 받았어요! ({receive_time} UTC)"
        await self.websocket.send_str(confirmation_message)
