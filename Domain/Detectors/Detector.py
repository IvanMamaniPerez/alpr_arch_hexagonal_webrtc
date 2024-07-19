from Domain.Models.Box import Box
from Domain.Models.Detection import Detection
from Domain.Models.ModelWrapper import ModelWrapper
import numpy as np

class Detector():
    def __init__(self, model_path: str, confidence: float):
        self.model_path:str               = model_path
        self.confidence:float             = confidence
        self.detections : list[Detection] = list()
        
        
    def get_first_detection(self) -> Detection:
        if len(self.detections) == 0:
            raise ValueError("Empty detections list")
        
        return self.detections[0]

    def clear_detections(self) -> None:
        self.detections.clear()

    @staticmethod
    def crop_box_detected(box : Box, image : np.ndarray) -> np.ndarray:
        return image[int(box.y1):int(box.y2), int(box.x1):int(box.x2)]