
from Application.Adapters.YOLODetectorAdapter import YOLODetectorAdapter

class LicensePlateDetector(YOLODetectorAdapter):
    
    def __init__(
            self, 
            model_path = "models/best_licences_detector.pt",  
            confidence = .5
        ) -> None:
            super().__init__(
                model_path = model_path, 
                confidence = confidence
            )

    def get_detections(self, pred) -> list:
        detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                            for i, box in enumerate(pred.boxes.xyxy.tolist())]
        
        if not detections:
            raise ValueError("No detections found")
        
        return sorted(detections, key=lambda x: x[1], reverse=True)
