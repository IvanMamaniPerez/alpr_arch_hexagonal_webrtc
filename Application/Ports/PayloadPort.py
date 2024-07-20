from abc import ABC, abstractmethod
from Domain.Payloads.Payload import Payload

class PayloadPort(ABC):
    @abstractmethod
    def save_image(self, payload: Payload) -> None:
        pass
    
    