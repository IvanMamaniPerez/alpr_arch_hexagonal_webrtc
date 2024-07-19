from Domain.Detectors.Detector import Detector
from Domain.Models.Detection import Detection
from Domain.Models.ModelWrapper import ModelWrapper
class VehicleDetector(Detector): 
    def __init__(
            self,
            model_path : str ,
            confidence : float,
            model_wrapper: ModelWrapper
            ) -> None:
        super().__init__(
            model_path    = model_path,
            confidence    = confidence,
            model_wrapper = model_wrapper
        )
    def sort_by_area(self, detections : list[Detection]) -> list:
        return sorted(
            detections, 
            key=lambda x: (x.box.x2 - x.box.x1) * (x.box.y2 - x.box.y1), 
            reverse=True
        )