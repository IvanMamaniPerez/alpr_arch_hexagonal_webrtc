from Application.Adapters.YOLODetectorAdapter import YOLODetectorAdapter



class VehicleDetector(YOLODetectorAdapter): 

    def __init__(
            self, 
            model_path : str = "models/best_vehicles.pt", 
            confidence : float = .5
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
        
        return sorted(detections, key=lambda x: (x[0][2] - x[0][0]) * (x[0][3] - x[0][1]), reverse=True)

    def sort_by_area(self, detections : list) -> list:
        return sorted(detections, key=lambda x: (x[0][2] - x[0][0]) * (x[0][3] - x[0][1]), reverse=True)