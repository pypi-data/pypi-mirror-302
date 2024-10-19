import os

import yaml


class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_dir = os.path.dirname(os.path.abspath(config_path))
        self._config = {}
        self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as file:
            self._config = yaml.safe_load(file)

        # Update these attributes to match the new configuration structure
        self.robot = self._config.get("robot", {})
        self.telemetry = self._config.get("telemetry", {})
        self.custom_robots_path = self._config.get("custom_robots_path", "examples/custom_robots")
        self.streaming = self._config.get("streaming", {})

        # Process the custom_robots_path
        if not os.path.isabs(self.custom_robots_path):
            self.custom_robots_path = os.path.join(self.config_dir, self.custom_robots_path)
        self.custom_robots_path = os.path.normpath(self.custom_robots_path)

        # Extract commonly used values for convenience
        self.telemetry_interval = self.telemetry.get("send_interval", 5)
        self.telemetry_exporter = self.telemetry.get("exporter", "console")
        self.otlp_endpoint = self.telemetry.get("otlp_endpoint", "http://localhost:4318/v1/traces")

        self.agent_id = self._config.get("agent_id")

    def get(self, key, default=None):
        return self._config.get(key, default)

    def __getitem__(self, key):
        return self._config[key]

    def __contains__(self, key):
        return key in self._config

    def __str__(self):
        return str(self._config)

    def __repr__(self):
        return f"Config({self.config_path})"
