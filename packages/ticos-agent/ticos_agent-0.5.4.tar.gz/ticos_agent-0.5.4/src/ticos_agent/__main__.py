import argparse
import asyncio
import os
import signal
from pathlib import Path

from ticos_agent.core.agent import Agent
from ticos_agent.core.config import Config
from ticos_agent.utils.logger import setup_logger


logger = setup_logger("ticos_agent")

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Default config path
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "examples" / "conf" / "default.yaml"


async def main():
    parser = argparse.ArgumentParser(description="Ticos Agent")
    parser.add_argument("--config", help="Path to configuration file", default=str(DEFAULT_CONFIG_PATH))
    args = parser.parse_args()

    config_path = args.config

    if not os.path.isfile(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        return

    config = Config(config_path)
    agent = Agent(config)

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}. Shutting down...")
        asyncio.create_task(agent.shutdown())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info(f"Starting agent... {agent}")

    try:
        await agent.run()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        await agent.shutdown()


def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
