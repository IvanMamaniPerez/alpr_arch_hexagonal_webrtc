from Domain.Models.Box import Box

class Detection:
    def __init__(self, id_class : int, confidence : float, box : Box) -> None:
        self.id_class   = id_class
        self.confidence = confidence
        self.box        = box
        
    def to_dict(self) -> dict:
        return {
            "id_class"  : self.id_class,
            "confidence": self.confidence,
            "box"       : self.box.to_dict()
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Detection':
        return cls(
            id_class   = data["id_class"],
            confidence = data["confidence"],
            box        = Box.from_dict(data["box"])
        )