from Application.Ports.DetectorPort import DetectorPort
from Domain.Detectors.Detector import Detector
from Domain.Models.Detection import Detection
from ultralytics import YOLO
import numpy as np

class DetectorAdapter(DetectorPort):
    def __init__(
            self
            ) -> None:
        self.model:YOLO = None
        self.confidence:float = 0
    
    def load_model(self, detector: Detector) -> None:
        
        model = YOLO(detector.model_path)
        model.fuse()
        
        self.confidence = detector.confidence
        self.model      = model
        

    def detect(self, image: np.ndarray) -> list[Detection]:

        detections = self.model.predict(image)
        
        if not detections or len(detections) == 0:
            raise ValueError("Empty prediction")
        
        return [
            Detection.from_dict({
                'class_id'  : int(pred.boxes.cls[i].item()),
                'class_name': pred.names[int(pred.boxes.cls[i].item())],
                'confidence': pred.boxes.conf[i].item(),
                'box': {
                    'x1': int(box[0]),
                    'y1': int(box[1]),
                    'x2': int(box[2]),
                    'y2': int(box[3])
                }
            })
            for pred in detections
            for i, box in enumerate(pred.boxes.xyxy.tolist())
            if pred.boxes.conf[i].item() >= self.confidence
        ]