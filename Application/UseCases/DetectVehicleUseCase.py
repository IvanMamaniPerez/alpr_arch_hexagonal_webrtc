from Application.Ports.DetectorPort import DetectorPort
from Application.Ports.UseCasePort import UseCasePort
from Domain.Detectors.VehicleDetector import VehicleDetector
from Application.Models.ResultUseCase import ResultUseCase
from Domain.Payloads.Payload import Payload
import numpy as np

class DetectVehicleUseCase(UseCasePort):
    def __init__(self, detector_port: DetectorPort, vehicle_detector: VehicleDetector) -> None:
        self.detector_port    : DetectorPort    = detector_port
        self.vehicle_detector : VehicleDetector = vehicle_detector
        self.detector_port.load_model(vehicle_detector)

    def execute(self, payload: Payload) -> ResultUseCase:
        # TODO[epic=events] implement the management of the events
        try: 
            self.vehicle_detector.detections = self.detector_port.detect(payload.image)
            self.vehicle_detector.sort_by_area()
            
            return ResultUseCase(
                success = True,
                payload = payload,
                metadata = {}
            )
            
        except Exception as e:
            return ResultUseCase(
                success = False,
                payload = payload,
                metadata = {'error': str(e)}
            )