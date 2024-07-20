import numpy as np
from abc import ABC, abstractmethod
class Payload(ABC):
    
    def __init__(self, uuid: str, reference_id:str, client_id:str, image: np.ndarray) -> None:
        self.uuid         : str        = uuid
        self.reference_id : str        = reference_id
        self.client_id    : str        = client_id
        self.image        : np.ndarray = image

    def to_dict(self) -> dict:
        return {
            "uuid"         : self.uuid,
            "reference_id" : self.reference_id,
            "client_id"    : self.client_id,
            "image"        : self.image.tolist()
        }
        
        
    @classmethod
    def from_dict(cls, payload_dict: dict) -> 'Payload':
        return cls(
            payload_dict["uuid"],
            payload_dict["reference_id"],
            payload_dict["client_id"],
            np.array(payload_dict["image"])
        )
