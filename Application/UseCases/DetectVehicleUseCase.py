from Application.Ports.DetectorPort import DetectorPort
from Domain.Detectors.VehicleDetector import VehicleDetector
from Domain.Models.Detection import Detection
import numpy as np

class DetectVehicleUseCase:
    def __init__(self, detector_port: DetectorPort, vehicle_detector: VehicleDetector) -> None:
        self.detector_port    : DetectorPort    = detector_port
        self.vehicle_detector : VehicleDetector = vehicle_detector
        self.detector_port.load_model(vehicle_detector)

    def execute(self, image: np.ndarray) -> Detection:
        # TODO[epic=events] implement the management of the events
        
        self.vehicle_detector.detections = self.detector_port.detect(image)
        self.vehicle_detector.sort_by_area()
        
        return self.vehicle_detector.get_first_detection()