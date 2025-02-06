import os
from services.websocket_service import WebSocketServer

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", 8765))  # Render 포트 사용, 기본값 8765
    server = WebSocketServer(host=host, port=port)
    server.start()