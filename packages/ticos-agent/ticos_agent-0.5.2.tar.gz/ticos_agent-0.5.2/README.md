<img src="https://dash.ticos.ai/logo.svg" alt="Ticos Logo" width="80" height="auto">

# Ticos Agent

## What is Ticos?

Ticos is an advanced Embodied AI platform for Humanoid Robotics. It provides a comprehensive suite of tools and frameworks for developing, deploying, and managing intelligent systems for humanoid robots. The Ticos Agent is a crucial component of this ecosystem, responsible for managing real-time audio streaming and interaction between robotic systems and the Ticos cloud infrastructure.

## Overview

The Ticos Agent is an efficient and secure system designed for real-time audio streaming and interaction in robotic applications, with a focus on humanoid robotics. It serves as the bridge between the physical robot and the Ticos cloud platform, enabling real-time audio communication and AI-driven interactions.

## Features

- Real-time audio streaming from robot to cloud
- Real-time audio playback from cloud to robot
- Extensible architecture for custom robot implementations
- Secure WebSocket-based communication
- Configurable audio parameters
- Easy-to-use command-line interface

## Installation

To install the Ticos Agent, you can clone the repository and install using Poetry:

```bash
git clone https://github.com/tiwater/ticos-agent.git
cd ticos-agent
poetry install
```

## Configuration

The Ticos Agent uses a YAML configuration file. By default, it looks for `examples/conf/default.yaml`. Here's an example configuration:

```yaml
# Agent configuration
agent_id: "your_agent_id_here"

# Robot configuration
robot:
  name: desktop_robot
  type: builtin
  module: desktop
  class_name: DesktopRobot
  config:
    # Any parameters specific to the robot can be set here

# Streaming configuration
streaming:
  ws_url: wss://api.ticos.ai/v1/realtime # WebSocket URL for real-time streaming
```

## Usage

To run the Ticos Agent:

```bash
poetry run start-dev
```

It will use the default configuration file.

## Extending the Ticos Agent

The Ticos Agent supports custom robot implementations. To create a custom robot:

1. Create a Python file in the `src/ticos_agent/robots` directory.
2. Implement a class that inherits from the `Robot` abstract base class.

```python
from ticos_agent.core.robot import Robot

class CustomRobot(Robot):
    async def start_audio_stream(self):
        # Implement audio stream initialization

    async def get_audio_chunk(self):
        # Implement audio chunk capture logic

    def add_audio_to_play(self, audio_data: str, item_id: str):
        # Implement audio playback logic

    async def stop(self):
        # Implement cleanup logic
```

You can look into the `src/ticos_agent/robots/desktop/robot.py` file for a built-in robot example.

## Project Structure

- `src/ticos_agent/`: Main package directory
  - `core/`: Core components (Agent, Robot base class, RealtimeStreamer)
  - `robots/`: Robot implementations
  - `utils/`: Utility functions and classes
  - `__main__.py`: Entry point for the application

## Contributing

We welcome contributions to the Ticos Agent! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

The Ticos Agent is released under the [MIT License](LICENSE).

## Support

For support, please open an issue on our [GitHub repository](https://github.com/tiwater/ticos-agent) or contact our support team at support@ticos.ai.

## Acknowledgements

The Ticos Agent is developed and maintained by the Tiwater team. We thank all our contributors and the open-source community for their valuable input and support.
