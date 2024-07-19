from Domain.Detectors.Detector import Detector
from Domain.Models.Detection import Detection
from Domain.Models.ModelWrapper import ModelWrapper
import numpy as np
class LicensePlateOCR(Detector): 
    def __init__(
            self, 
            model_path   : str,
            confidence   : float,
            model_wrapper: ModelWrapper
            ) -> None:
        super().__init__(
            model_path    = model_path,
            confidence    = confidence,
            model_wrapper = model_wrapper
            )

    def filter_by_highest_confidence(self, detections : list[Detection]) -> list[Detection]:
        filtered_detections: dict = {}
        
        for detection  in detections:
            box        = detection.box
            box_tuple  = box.to_tuple()
            confidence = detection.confidence
            class_id   = detection.class_id
            class_name = detection.class_name
            
            if box_tuple not in filtered_detections or filtered_detections[box_tuple][1] < confidence:
                filtered_detections[box_tuple] = (box, confidence, class_id, class_name)
                
        return [
            Detection(
                class_id   = class_id,
                class_name = class_name,
                confidence = confidence,
                box        = box
                )
            for box, confidence, class_id in filtered_detections.values()
            ]
    
    def extract_license_plate(self, detections:  list[Detection]) -> str:
        detections = self.filter_by_highest_confidence(detections)
        if len(detections) == 0:
            raise ValueError("No ocr detections found")
        return ''.join(map(lambda x: x.class_name, detections))
