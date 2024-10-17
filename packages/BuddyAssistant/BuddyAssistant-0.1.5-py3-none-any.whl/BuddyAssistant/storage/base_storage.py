from typing import Any, Dict


class BaseStorage:
    def save_assistant(self, assistant_id: str, data: Dict[str, Any]) -> None:
        """Save the assistant data."""
        raise NotImplementedError()

    def load_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """Load the assistant data."""
        raise NotImplementedError()

    def save_thread(self, thread_id: str, data: Dict[str, Any]) -> None:
        """Save the thread data."""
        raise NotImplementedError()

    def load_thread(self, thread_id: str) -> Dict[str, Any]:
        """Load the thread data."""
        raise NotImplementedError()
