from Application.Adapters.YOLODetectorAdapter import YOLODetectorAdapter
class LicensePlateOCR(YOLODetectorAdapter): 
    def __init__(
            self, 
            model_path : str = "models/ocr_license_plate.pt", 
            confidence : float = .5
            ) -> None:
        super().__init__(
            model_path = model_path, 
            confidence = confidence
            )

    def get_detections(self, pred) -> list:
        detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                            for i, box in enumerate(pred.boxes.xyxy.tolist())]
        detections.sort(key=lambda x: x[0][0])
        return self.filter_by_highest_confidence(detections)

    def filter_by_highest_confidence(self, detections : list) -> list:
        filtered_detections: dict = {}
        for box, confidence, class_id in detections:
            
            box_tuple = tuple(map(int, box))
            if box_tuple not in filtered_detections or filtered_detections[box_tuple][1] < confidence:
                
                filtered_detections[box_tuple] = (box, confidence, class_id)
                
        return list(filtered_detections.values())
    
    def extract_license_plate(self, image) -> str:
        result = self.predict(image)
        if not result:
            raise ValueError("No ocr detections found")
        print("OCR")
        print(result.to_dict())
        
        return  ''.join(map(lambda x: x['class_name'], result.to_dict()))
