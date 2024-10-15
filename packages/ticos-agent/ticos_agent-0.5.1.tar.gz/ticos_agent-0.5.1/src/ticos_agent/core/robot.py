import asyncio
import importlib
import logging
from abc import ABC, abstractmethod
from pathlib import Path

from .realtime_streamer import RealtimeStreamer
from .telemetry import TelemetryManager


logger = logging.getLogger(__name__)


class Robot(ABC):
    def __init__(self, config, robot_config):
        self.config = config
        self.robot_config = robot_config
        self.name = robot_config["name"]
        self.telemetry_manager = TelemetryManager()

        # Make ws_url optional
        ws_url = config.get("streaming", {}).get("ws_url")
        agent_id = config.get("agent_id")  # Get the agent_id from the config
        if ws_url:
            if agent_id is None:
                logger.warning(f"No agent_id provided for robot {self.name}. Using default value 0.")
                agent_id = 0
            self.realtime_streamer = RealtimeStreamer(ws_url, agent_id)
        else:
            logger.warning(f"No WebSocket URL provided for robot {self.name}. Real-time streaming will be disabled.")
            self.realtime_streamer = None

    async def run(self):
        tasks = [self.collect_and_send_telemetry()]
        if self.realtime_streamer:
            tasks.append(self.stream_realtime_data())
        await asyncio.gather(*tasks)

    async def collect_and_send_telemetry(self):
        while True:
            telemetry_data = await self.get_telemetry()
            if self.realtime_streamer:
                await self.realtime_streamer.send_telemetry(telemetry_data)
            await asyncio.sleep(self.config.get("telemetry", {}).get("send_interval", 5))

    async def stream_realtime_data(self):
        if self.realtime_streamer:
            await self.realtime_streamer.start_streaming(self.get_video_frame, self.get_audio_chunk)
        else:
            logger.warning(f"Real-time streaming is disabled for robot {self.name}")

    async def execute_command(self, command):
        # Implement command execution logic here
        pass

    async def stop(self):
        # Implement any necessary cleanup here
        pass

    # @abstractmethod
    # async def get_telemetry(self):
    #     """Get telemetry data from the robot."""
    #     pass

    # @abstractmethod
    # def get_video_frame(self):
    #     """Get a video frame from the robot."""
    #     pass

    @abstractmethod
    def get_audio_chunk(self):
        """Get an audio chunk from the robot."""
        pass


def get_robot_class(robot_type):
    try:
        module = importlib.import_module(f"ticos_agent.robots.{robot_type}.robot")
        return getattr(module, f"{robot_type.capitalize()}Robot")
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Failed to load robot type '{robot_type}': {str(e)}")


def list_available_robots():
    robot_dir = Path(__file__).parent.parent / "robots"
    return [d.name for d in robot_dir.iterdir() if d.is_dir() and (d / "robot.py").exists()]


def initialize_robot(config):
    robot_config = config.get("robot", {})
    robot_name = robot_config.get("name")
    robot_class_name = robot_config.get("class_name")
    robot_module = robot_config.get("module")
    robot_type = robot_config.get("type")

    if not all([robot_name, robot_class_name, robot_type]):
        raise ValueError(f"Robot config missing required fields: {robot_config}")

    try:
        if robot_type == "builtin":
            robot_module_path = "ticos_agent.robots"
            full_module_path = f"{robot_module_path}.{robot_module}.robot"
            robot_module = importlib.import_module(full_module_path)
            robot_class = getattr(robot_module, robot_class_name)
        else:
            raise ValueError(f"Unsupported robot type: {robot_type}")

        logger.info(f"Initializing robot: {robot_name} with class: {robot_class}")
        logger.debug(f"Config: {config}")
        logger.debug(f"Robot config: {robot_config}")

        # Initialize the robot with the config
        robot = robot_class(config, robot_config)
        logger.info(f"Initialized robot: {robot_name}")
        return robot
    except ImportError:
        logger.exception(f"Failed to import robot module for class: {robot_module}.{robot_class_name}")
    except AttributeError:
        logger.error(f"Failed to find robot class: {robot_class_name}")
    except Exception as e:
        logger.error(f"Error initializing robot {robot_name}: {str(e)}")
        logger.exception("Detailed error:")

    raise RuntimeError(f"Failed to initialize robot: {robot_name}")
