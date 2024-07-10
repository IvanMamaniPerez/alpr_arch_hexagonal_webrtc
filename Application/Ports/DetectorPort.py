from abc import ABC, abstractmethod
from Domain.Models.Result import Result
import numpy as np
from Domain.Models.Box import Box

class DetectorPort(ABC):
    @abstractmethod
    def predict(self, image : np.ndarray) -> Result:
        """ Predict the image"""
        pass

    @staticmethod
    @abstractmethod
    def crop_box_detected(box : Box, frame : np.ndarray) -> np.ndarray:
        """ Crop box detected, it needs a box and a frame"""
        pass

    @property
    @abstractmethod
    def confidence(self) -> float:
        """ Return the confidence"""
        pass

    @confidence.setter
    @abstractmethod
    def confidence(self, confidence : float) -> None:
        """ Set the confidence"""
        pass

    @abstractmethod
    def get_detections(self, pred) -> list: 
        """ This method returns the detections of the image prosessed 
        by the model and the use case in the diferent types of detectors """
        pass