import asyncio
import base64
import logging
from collections import deque

import numpy as np
import sounddevice as sd

from ticos_agent.core.robot import Robot


logger = logging.getLogger(__name__)


class DesktopRobot(Robot):
    def __init__(self, global_config, robot_config):
        super().__init__(global_config, robot_config)
        self.sample_rate = 24000
        self.channels = 1
        self.dtype = "int16"
        self.chunk_duration_ms = 100
        self.chunk_size = int(self.sample_rate * self.chunk_duration_ms / 1000)
        self.record_queue = asyncio.Queue()
        self.playback_queue = deque()
        self.buffer = np.array([], dtype=self.dtype)
        self.recording = False
        self.playing = False
        self.play_task = None
        self.current_item_id = None

    async def start_audio_stream(self):
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio input status: {status}")
            if self.recording:
                flattened_data = indata.flatten() if indata.ndim > 1 else indata
                self.buffer = np.concatenate((self.buffer, flattened_data))
                while len(self.buffer) >= self.chunk_size:
                    chunk = self.buffer[: self.chunk_size]
                    self.buffer = self.buffer[self.chunk_size :]
                    self.record_queue.put_nowait(chunk)

        self.recording = True
        self.input_stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            callback=audio_callback,
            blocksize=self.chunk_size,
        )
        self.input_stream.start()
        logger.debug(f"Started audio recording with chunk size: {self.chunk_size}")

    async def get_audio_chunk(self):
        try:
            chunk = await self.record_queue.get()
            return self.encode(chunk)
        except Exception as e:
            logger.error(f"Error capturing audio chunk: {e}")
            return None

    def add_audio_to_play(self, audio_data: str, item_id: str):
        audio_array = self.decode(audio_data)
        self.playback_queue.append((item_id, audio_array))

        if not self.play_task or self.play_task.done():
            self.play_task = asyncio.create_task(self._play_audio_loop())

    async def _play_audio_loop(self):
        self.playing = True
        output_stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
        )
        output_stream.start()

        try:
            while self.playback_queue or self.playing:
                if self.playback_queue:
                    item_id, chunk = self.playback_queue.popleft()
                    if item_id != self.current_item_id:
                        if self.current_item_id:
                            logger.info(f"Finished playing audio for item {self.current_item_id}")
                        logger.info(f"Started playing audio for item {item_id}")
                        self.current_item_id = item_id
                    output_stream.write(chunk)
                else:
                    await asyncio.sleep(0.01)
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
        finally:
            output_stream.stop()
            output_stream.close()
            if self.current_item_id:
                logger.info(f"Finished playing audio for item {self.current_item_id}")
            self.current_item_id = None
            self.playing = False

    @staticmethod
    def encode(audio_data):
        return base64.b64encode(audio_data.tobytes()).decode("utf-8")

    @staticmethod
    def decode(audio_string):
        return np.frombuffer(base64.b64decode(audio_string), dtype=np.int16)

    async def run(self):
        await self.start_audio_stream()
        # The streaming will be handled by the RealtimeStreamer

    async def stop(self):
        self.recording = False
        if hasattr(self, "input_stream"):
            self.input_stream.stop()
            self.input_stream.close()
        self.playing = False
        # Wait for play_task to finish if it's running
        if self.play_task and not self.play_task.done():
            await self.play_task
