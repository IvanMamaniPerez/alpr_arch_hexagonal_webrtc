from abc import ABC, abstractmethod
from Domain.Models.Detection import Detection
from Domain.Detectors.Detector import Detector
import numpy as np

class DetectorPort(ABC):
    @abstractmethod
    def load_model(self, detector: Detector) -> None:
        """ Load the model"""
        pass
    
    @abstractmethod
    def detect(self, image : np.ndarray) -> list[Detection]:
        """ Predict the image"""
        pass
    