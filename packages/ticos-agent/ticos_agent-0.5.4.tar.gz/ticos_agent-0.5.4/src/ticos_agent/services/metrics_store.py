import threading
from typing import Any, Dict


class MetricsStore:
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()

    def add_metric(self, key: str, value: Any):
        with self.lock:
            self.metrics[key] = value

    def remove_metric(self, key: str):
        with self.lock:
            self.metrics.pop(key, None)

    def get_metrics(self) -> Dict[str, Any]:
        with self.lock:
            return self.metrics.copy()

    def clear_metrics(self):
        with self.lock:
            self.metrics.clear()

    def store_metrics(self, device_info: Dict[str, Any], data: Dict[str, Any]):
        with self.lock:
            identifier = device_info.get("identifier", "unknown_device")
            if identifier not in self.metrics:
                self.metrics[identifier] = {}
            self.metrics[identifier].update(data)

    def __str__(self):
        return f"MetricsStore(metrics={self.get_metrics()})"

    def __repr__(self):
        return self.__str__()
