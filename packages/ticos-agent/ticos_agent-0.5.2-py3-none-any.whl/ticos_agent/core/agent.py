import asyncio
import logging
import signal

from ticos_agent.core.realtime_streamer import RealtimeStreamer
from ticos_agent.core.robot import initialize_robot


logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, config):
        self.config = config
        self.agent_id = config.agent_id
        self.robot = initialize_robot(config)
        self.running = False
        self.shutdown_event = asyncio.Event()
        self.tasks = []

        ws_url = config.get("streaming", {}).get("ws_url", "wss://api.ticos.ai/v1/realtime")
        self.realtime_streamer = RealtimeStreamer(ws_url, self.agent_id)

    async def run(self):
        self.running = True
        try:
            # Start the robot's audio stream
            await self.robot.start_audio_stream()

            # Start the realtime streaming
            streaming_task = asyncio.create_task(
                self.realtime_streamer.start_streaming(self.robot.get_audio_chunk, self.robot.add_audio_to_play)
            )
            self.tasks.append(streaming_task)

            # Wait for the shutdown event
            await self.shutdown_event.wait()

        except asyncio.CancelledError:
            logger.info("Agent run cancelled")
        except Exception as e:
            logger.error(f"Unexpected error in Agent.run: {e}", exc_info=True)
        finally:
            await self.shutdown()

    async def shutdown(self):
        if not self.running:
            return

        logger.info("Shutting down agent...")
        self.running = False
        self.shutdown_event.set()

        # Cancel all tasks
        for task in self.tasks:
            task.cancel()

        # Wait for all tasks to complete with a timeout
        await asyncio.wait(self.tasks, timeout=5)

        await self.realtime_streamer.stop()
        await self.robot.stop()

        logger.info("Agent shutdown completed")

    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}. Initiating shutdown...")
        asyncio.create_task(self.shutdown())
