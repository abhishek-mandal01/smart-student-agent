from typing import Dict, Any
import time
import logging

logger = logging.getLogger(__name__)

class MemoryBank:
    """
    Simple in-memory memory for demo.
    Replace with persistent storage for production.
    """
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}

    def read(self, user_id: str) -> Dict[str, Any]:
        return self.users.get(user_id, {})

    def write(self, user_id: str, data: Dict[str, Any]) -> None:
        self.users.setdefault(user_id, {}).update({
            **data,
            "_last_update": time.time()
        })
        logger.info("MemoryBank.write user=%s keys=%s", user_id, list(data.keys()))

memory = MemoryBank()
