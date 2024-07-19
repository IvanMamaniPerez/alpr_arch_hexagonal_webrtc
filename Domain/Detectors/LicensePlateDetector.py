from Domain.Detectors.Detector import Detector
from Domain.Models.Detection import Detection

class LicensePlateDetector(Detector):
    
    def __init__(
            self, 
            model_path   : str,
            confidence   : float
        ) -> None:
            super().__init__(
                model_path    = model_path,
                confidence    = confidence
            )

    def sort_by_confidence(self, detections : list[Detection]) -> list:
        return sorted(detections, key=lambda x: x.confidence, reverse=True)

