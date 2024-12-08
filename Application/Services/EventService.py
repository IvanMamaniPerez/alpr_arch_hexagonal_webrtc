from typing import Callable, Dict, List
from Application.Models.Event import Event

class EventService:
    def __init__(self) -> None:
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, listener: Callable[[Event], None]) -> None:
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def emit(self, event_name: str, data: dict) -> None:
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(data)
