from abc import ABC, abstractmethod
from Application.Models.Payload import Payload
from Application.Ports.PayloadManagerPort import PayloadPort
class UseCasePort(ABC):
    @abstractmethod
    def execute(self, payload : Payload):
        pass