from abc import ABC, abstractmethod
from Domain.Payloads.Payload import Payload
from Application.Ports.PayloadPort import PayloadPort
class UseCasePort(ABC):
    @abstractmethod
    def execute(self, payload : Payload):
        pass