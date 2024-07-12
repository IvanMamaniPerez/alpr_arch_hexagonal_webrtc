from Domain.Models.Box import Box

class Detection:
    def __init__(self, class_id : int, class_name: str, confidence : float, box : Box) -> None:
        self.class_id   : int   = class_id
        self.class_name : str   = class_name
        self.confidence : float = confidence
        self.box        : Box   = box

    def to_dict(self) -> dict:
        return {
            "class_id"  : self.class_id,
            "class_name": self.class_name,
            "confidence": self.confidence,
            "box"       : self.box.to_dict()
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Detection':
        return cls(
            class_id   = data["class_id"],
            class_name = data["class_name"],
            confidence = data["confidence"],
            box        = Box.from_dict(data["box"])
        )