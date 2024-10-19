import asyncio
import json
import logging

import websockets


logger = logging.getLogger(__name__)


class RealtimeStreamer:
    def __init__(self, ws_url, agent_id):
        self.ws_url = ws_url
        self.agent_id = agent_id
        self.websocket = None
        self.running = False
        self.get_audio_chunk = None
        self.add_audio_to_play = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.ws_url)
            init_message = {"type": "init", "agent_id": self.agent_id}
            await self.websocket.send(json.dumps(init_message))
            init_response = await self.websocket.recv()
            logger.info(f"Init response: {init_response}")

            response_data = json.loads(init_response)
            if response_data.get("type") == "error":
                logger.error(f"Initialization error: {response_data.get('message')}")
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            return False

    async def start_streaming(self, get_audio_chunk, add_audio_to_play):
        self.running = True
        self.get_audio_chunk = get_audio_chunk
        self.add_audio_to_play = add_audio_to_play

        if not await self.connect():
            logger.error("Failed to initialize the connection. Exiting.")
            return

        send_task = asyncio.create_task(self._send_audio())
        receive_task = asyncio.create_task(self._receive_messages())

        try:
            await asyncio.gather(send_task, receive_task)
        except asyncio.CancelledError:
            logger.info("Streaming tasks cancelled")
        finally:
            self.running = False

    async def _send_audio(self):
        while self.running:
            try:
                audio_chunk = await self.get_audio_chunk()
                if audio_chunk:
                    message = {
                        "type": "message",
                        "content": {"type": "audio", "audio": audio_chunk},
                    }
                    await self.websocket.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending audio: {str(e)}")
                await asyncio.sleep(1)

    async def _receive_messages(self):
        try:
            async for message in self.websocket:
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
            self.running = False

    async def handle_message(self, message):
        try:
            data = json.loads(message)
            if data.get("type") == "conversation_updated":
                event = data.get("event", {})
                item = event.get("item", {})
                delta = event.get("delta", {})

                if delta and delta.get("audio"):
                    if self.add_audio_to_play:
                        self.add_audio_to_play(delta["audio"], item.get("id"))

                if item.get("status") == "completed":
                    if item.get("role") == "assistant":
                        print(f"Assistant: {item.get('formatted', {}).get('transcript', '[Empty]')}")
                    elif item.get("role") == "user":
                        print(f"User: {item.get('formatted', {}).get('transcript', '[Empty]')}")
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")

    async def stop(self):
        self.running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
