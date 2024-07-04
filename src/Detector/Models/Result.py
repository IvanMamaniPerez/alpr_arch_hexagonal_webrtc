from src.Detector.Models.Box import Box

class Result:
    def __init__(self, class_name: str, confidence: float, box_coordinates: dict) -> None:
        self.class_name      = class_name
        self.confidence      = confidence
        self.box_coordinates = Box.from_dict(box_coordinates)

    def to_dict(self) -> dict:
        return {
            "class_name"     : self.class_name,
            "confidence"     : self.confidence,
            "box_coordinates": self.box_coordinates.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Result':
        
        return cls(
            class_name      = data["class_name"],
            confidence      = data["confidence"],
            box_coordinates = data["box_coordinates"]
        )