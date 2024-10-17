import json
import os
from typing import Any, Dict

from storage.base_storage import BaseStorage


class LocalStorage(BaseStorage):
    def __init__(self, directory: str):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_assistant(self, assistant_id: str, data: Dict[str, Any]) -> None:
        file_path = os.path.join(self.directory, f"{assistant_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def load_assistant(self, assistant_id: str) -> Dict[str, Any]:
        file_path = os.path.join(self.directory, f"{assistant_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}

    def save_thread(self, thread_id: str, data: Dict[str, Any]) -> None:
        file_path = os.path.join(self.directory, f"{thread_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def load_thread(self, thread_id: str) -> Dict[str, Any]:
        file_path = os.path.join(self.directory, f"{thread_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
