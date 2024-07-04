from ultralytics import YOLO
from src.Detector.Models.Result import Result
from abc import ABC, abstractmethod
import numpy as np
from src.Detector.Models.Box import Box
class Detector(ABC):
    def __init__(
            self, 
            model_path : str, 
            confidence : float = .5
            ) -> None:
        self.model_path = model_path
        self.model      = YOLO(model_path)
        self.confidence = confidence
        self.model.fuse()

    @property
    def confidence(self) -> float:
        return self.__confidence
    
    @confidence.setter
    def confidence(self, confidence : float) -> None:
        if confidence < 0 or confidence > 1:
            raise ValueError("Confidence must be between 0 and 1")
        self.__confidence = confidence

    @abstractmethod
    def get_detections(self, pred) -> list: 
        pass

    def predict(self, image : np.ndarray) -> Result:
        list_pred = self.model.predict(image)

        if not list_pred or len(list_pred) == 0:
            raise ValueError("Empty prediction")
        
        pred = list_pred[0]

        detections = self.get_detections(pred)

        box, confidence, class_id = detections[0]
        x1, y1, x2, y2 = map(int, box)
        class_name = pred.names[class_id]

        return Result.from_dict({
            "class_name"     : class_name,
            "confidence"     : confidence,
            "box_coordinates": {
                'x1' : x1,
                'y1' : y1,
                'x2' : x2,
                'y2' : y2
            }
        })
    
    @staticmethod
    def crop_box_detected(box : Box, frame : np.ndarray) -> np.ndarray:
        box_dict = box.to_dict()
        y1 = box_dict['y1']
        y2 = box_dict['y2']
        x1 = box_dict['x1']
        x2 = box_dict['x2']

        return frame[int(y1):int(y2), int(x1):int(x2)]
    