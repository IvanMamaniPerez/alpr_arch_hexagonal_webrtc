from abc import ABC, abstractmethod
from Application.Models.Payload import Payload

class PayloadManagerPort(ABC):
    
    @abstractmethod
    def get_storage_path(self) -> str:
        pass
    
    @abstractmethod
    def save_image(self, payload: Payload) -> None:
        pass
    
    @abstractmethod
    def load_payload(self, uuid: str) -> Payload:
        pass
    
"""     @abstractmethod
    def load_image(self, Payload: Payload, Detection) ->  """