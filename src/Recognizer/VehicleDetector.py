from ultralytics import YOLO

class VehicleDetector: 

    def __init__(
            self, 
            model_path : str = "models/best_vehicles.pt", 
            confidence : float = .5
            ) -> None:
        self.model_path = model_path
        self.model = YOLO(model_path)
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

    def predict(self, image) -> None|dict:
        list_pred = self.model.predict(image)
        result = None
        if len(list_pred) > 0:
            pred = list_pred[0]
            
            detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                    for i, box in enumerate(pred.boxes.xyxy.tolist())]
            
            if detections:

                detections.sort(key=lambda x: (x[0][2] - x[0][0]) * (x[0][3] - x[0][1]), reverse=True)
                # Solo usar el primer resultado, que es el más grande
                box, confidence, class_id = detections[0]

                x1, y1, x2, y2 = map(int, box)

                class_name = pred.names[class_id]

                if confidence >= self.confidence:
                    result = {
                        'class_name': class_name,
                        'class_confidence': confidence,
                        'box_coordinates': (x1, y1, x2, y2)
                    }
        return result

