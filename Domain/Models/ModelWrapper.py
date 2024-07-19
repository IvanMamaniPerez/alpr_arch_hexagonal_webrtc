from abc import ABC, abstractmethod
import numpy as np

class ModelWrapper(ABC):
    def __init__(self, model_path:str = '', confidence:float = 0) -> None:
        self.model_path:str   = model_path
        self.confidence:float = confidence
        self.model            = self.load_model()
    
    @classmethod
    def from_implementation(cls, model_path:str, confidence:float) -> 'ModelWrapper':
        return cls(model_path, confidence)
    
    @abstractmethod
    def load_model(self):
        pass
    
    @abstractmethod
    def detect(self, image: np.ndarray) -> list:
        pass
