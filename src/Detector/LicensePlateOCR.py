from ultralytics import YOLO

class LicensePlateOCR: 
    def __init__(
            self, 
            model_path : str = "models/ocr_license_plate.pt", 
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

    def predict(self, image) -> list:
        list_pred = self.model.predict(image)
        results = []
        print('List Pred:', list_pred)
        print('List pred length:', len(list_pred))
        
        for pred in list_pred:
            detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                            for i, box in enumerate(pred.boxes.xyxy.tolist())]
            
            detections.sort(key=lambda x: x[0][0])
            detections = self.filter_by_highest_confidence(detections)
            for box, confidence, class_id in detections:
                x1, y1, x2, y2 = map(int, box)
                class_name = pred.names[class_id]
                print('Class Name into class:', class_name, 'Confidence:', confidence)
                if confidence >= self.confidence:
                    results.append({
                        'class_id'        : class_id,
                        'class_name'      : class_name,
                        'class_confidence': confidence,
                        'box_coordinates' : (x1, y1, x2, y2)
                    })
        return results
    
    def filter_by_highest_confidence(self, detections):
        filtered_detections = {}
        for box, confidence, class_id in detections:
            # Convertir coordenadas a enteros antes de usarlas como clave
            box_tuple = tuple(map(int, box))
            if box_tuple not in filtered_detections or filtered_detections[box_tuple][1] < confidence:
                # Almacenar la detección con la mayor confianza para estas coordenadas enteras
                filtered_detections[box_tuple] = (box, confidence, class_id)
        return list(filtered_detections.values())
    
    def extract_license_plate(self, image) -> str:
        class_names = self.predict(image)
        return  ''.join(map(lambda x: x['class_name'], class_names))
