from Domain.Detectors.Detector import Detector
from Domain.Models.Detection import Detection
from Domain.Models.ModelWrapper import ModelWrapper

class LicensePlateDetector(Detector):
    
    def __init__(
            self, 
            model_path   : str,
            confidence   : float,
            model_wrapper: ModelWrapper
        ) -> None:
            super().__init__(
                model_path    = model_path,
                confidence    = confidence,
                model_wrapper = model_wrapper
            )

    def sort_by_confidence(self, detections : list[Detection]) -> list:
        return sorted(detections, key=lambda x: x.confidence, reverse=True)

