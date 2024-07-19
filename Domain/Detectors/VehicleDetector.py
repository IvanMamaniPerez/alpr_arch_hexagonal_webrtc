from Domain.Detectors.Detector import Detector
from Domain.Models.Detection import Detection
class VehicleDetector(Detector): 
    def __init__(
            self,
            model_path : str ,
            confidence : float
            ) -> None:
        super().__init__(
            model_path    = model_path,
            confidence    = confidence
        )
    def sort_by_area(self) -> list[Detection]:
        return sorted(
            self.detections, 
            key=lambda x: (x.box.x2 - x.box.x1) * (x.box.y2 - x.box.y1), 
            reverse=True
        )