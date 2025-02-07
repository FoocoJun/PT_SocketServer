import asyncio
from aiohttp import web
from handlers.client_handler import ClientHandler
from handlers.data_dispatcher import DataDispatcher
from handlers.aws_handler import AWSHandler

class WebSocketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    # ✅ 모든 요청을 로깅하는 함수
    async def request_logger(self, request):
        print(f"🌐 Received {request.method} request for {request.path}")
        return web.Response(text="Request received")

    # ✅ WebSocket 핸들러 (클라이언트 연결 처리)
    async def websocket_handler(self, request):
        ws_current = web.WebSocketResponse()
        await ws_current.prepare(request)

        print("✅ New WebSocket client connected!")

        # ✅ 클라이언트마다 독립적인 인스턴스 생성
        aws_handler = AWSHandler()                      # 각 클라이언트 전용 AWSHandler
        data_dispatcher = DataDispatcher(aws_handler)   # 각 클라이언트 전용 DataDispatcher
        handler = ClientHandler(ws_current, data_dispatcher)  # 각 클라이언트 전용 ClientHandler

        # ✅ 상호 참조 설정
        data_dispatcher.client_handler = handler

        try:
            async for msg in ws_current:
                await handler.process(msg.data)
        except Exception as e:
            print(f"⚠️ Error: {e}")
        finally:
            print("🔒 WebSocket connection closed.")

        return ws_current

    # ✅ 헬스 체크용 엔드포인트
    async def health_check(self, request):
        return web.Response(text="OK")

    # ✅ 서버 시작
    def start(self):
        app = web.Application()

        # 헬스 체크 및 WebSocket 라우팅
        app.router.add_get("/", self.health_check)
        app.router.add_get("/ws", self.websocket_handler)

        # ✅ 모든 요청 로깅 (404 에러 방지 및 디버깅용)
        app.router.add_route('*', '/{tail:.*}', self.request_logger)

        print(f"🚀 Server started at ws://{self.host}:{self.port}")
        web.run_app(app, host=self.host, port=self.port)
