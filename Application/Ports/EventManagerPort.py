from abc import ABC, abstractmethod
from Application.Models.Payload import Payload

class EventManagerPort(ABC):
    @abstractmethod
    def send_event(self, event: str, payload: Payload) -> None:
        pass