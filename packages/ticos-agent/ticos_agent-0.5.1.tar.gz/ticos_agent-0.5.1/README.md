<img src="https://dash.ticos.ai/logo.svg" alt="Ticos Logo" width="80" height="auto">

# Ticos Agent

## What is Ticos?

Ticos is an advanced Embodied AI platform for Humanoid Robotics. It provides a comprehensive suite of tools and frameworks for developing, deploying, and managing intelligent systems for humanoid robots. The Ticos Agent is a crucial component of this ecosystem, responsible for collecting and transmitting data from robotic systems to the Ticos cloud infrastructure.

## Overview

The Ticos Agent is an extensible, efficient, and secure data collection and transmission system designed for robotic applications, with a focus on humanoid robotics. It serves as the bridge between the physical robot and the Ticos cloud platform, enabling real-time monitoring, analytics, and AI-driven decision making.

## Features

- Real-time system information collection
- Extensible architecture for custom robot implementations
- Secure and efficient data transmission
- Configurable telemetry collection and sending intervals
- Support for real-time streaming of video and audio data
- Easy-to-use command-line interface

## Installation

To install the Ticos Agent, you can use pip:

```bash
pip install ticos-agent
```

Or clone the repository and install using Poetry:

```bash
git clone https://github.com/tiwater/ticos-agent.git
cd ticos-agent
poetry install
```

## Configuration

The Ticos Agent uses a YAML configuration file. By default, it looks for `examples/conf/default.yaml`. Here's an example configuration:

```yaml
# General configuration
api_url: http://localhost:8765
api_key: ti_25e364c8dcb91d0bfd0524ce13759bfd
custom_robots_path: examples/custom_robots

# Telemetry configuration
telemetry:
  exporter: console # Options: otlp, logging, file
  # otlp_endpoint: http://localhost:4318/v1/traces  # Only used if exporter is otlp
  send_interval: 5

# Robot configuration
robot:
  name: desktop_robot
  type: builtin
  module: desktop
  class_name: DesktopRobot
  config:
    # Any parameters specific to the robot can be set here

# Optional: Global device ID (if not provided, MAC address will be used)
# device_id: 1

# Streaming configuration
streaming:
  ws_url: wss://api.ticos.ai/v1/realtime # WebSocket URL for real-time streaming
```

## Usage

To run the Ticos Agent:

```bash
poetry run ticos --config /path/to/config.yaml
```

If no config file is specified, it will use the default configuration file.

## Extending the Ticos Agent

The Ticos Agent supports custom robot implementations. To create a custom robot:

1. Create a Python file in the `custom_robots_path` specified in your config.
2. Implement a class that inherits from the `Robot` abstract base class.

```python
from ticos_agent.core.robot import Robot

class CustomRobot(Robot):
    async def get_telemetry(self):
        # Implement telemetry collection logic
        pass

    async def get_video_frame(self):
        # Implement video frame capture logic
        pass

    async def get_audio_chunk(self):
        # Implement audio chunk capture logic
        pass

    async def execute_command(self, command):
        # Implement command execution logic
        pass
```

You can look into the `src/ticos_agent/robots` folder for built-in robot examples.

## Contributing

We welcome contributions to the Ticos Agent! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

The Ticos Agent is released under the [MIT License](LICENSE).

## Support

For support, please open an issue on our [GitHub repository](https://github.com/tiwater/ticos-agent) or contact our support team at support@ticos.ai.

## Acknowledgements

The Ticos Agent is developed and maintained by the Tiwater team. We thank all our contributors and the open-source community for their valuable input and support.
