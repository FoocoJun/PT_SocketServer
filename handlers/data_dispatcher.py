class DataDispatcher:
    def __init__(self, aws_handler):
        self.aws_handler = aws_handler
        self.client_handler = None

    async def handle_audio(self, audio_data):
        await self.aws_handler.send_audio(audio_data, self.handle_partial)

    async def handle_partial(self, response):
        # ✅ AWS Transcribe에서 받은 응답을 Unity로 전달
        if "Transcript" in response:
            results = response["Transcript"]["Results"]
            if results:
                transcript = results[0]["Alternatives"][0]["Transcript"]
                is_partial = results[0].get("IsPartial", False)

                # ✅ Partial과 Final 데이터 구분하여 전송
                message_type = "Partial" if is_partial else "Final"
                print(f"📥 {message_type} Result: {transcript}")

                if self.client_handler:
                    await self.client_handler.send_to_unity({
                        "type": message_type,
                        "transcript": transcript
                    })

    async def close(self):
        await self.aws_handler.disconnect()
        print("🔌 AWSHandler disconnected.")
