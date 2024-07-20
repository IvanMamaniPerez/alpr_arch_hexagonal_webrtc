from Application.Ports.DetectorPort import DetectorPort
from Application.Ports.UseCasePort import UseCasePort
from Domain.Detectors.VehicleDetector import VehicleDetector
from Domain.Detectors.LicensePlateDetector import LicensePlateDetector
from Application.Models.ResultUseCase import ResultUseCase
from Domain.Payloads.Payload import Payload
import cv2

class DetectVehicleAndLicensePlateUseCase(UseCasePort):
    def __init__(
            self, 
            vehicle_detector_port: DetectorPort, 
            license_plate_detector_port: DetectorPort, 
            vehicle_detector: VehicleDetector,
            license_plate_detector: LicensePlateDetector
        ) -> None:

        if vehicle_detector_port == license_plate_detector_port:
            raise ValueError("The vehicle and license plate detector ports must be different instances")
                
        self.vehicle_detector_port       : DetectorPort = vehicle_detector_port
        self.license_plate_detector_port : DetectorPort = license_plate_detector_port

        self.vehicle_detector : VehicleDetector = vehicle_detector
        self.license_plate_detector : LicensePlateDetector = license_plate_detector
        
        self.vehicle_detector_port.load_model(vehicle_detector)
        self.license_plate_detector_port.load_model(license_plate_detector)
        
        

    def execute(self, payload: Payload) -> ResultUseCase:
        # TODO[epic=events] implement the management of the events
        try: 
            self.vehicle_detector.detections = self.vehicle_detector_port.detect(payload.image)
            self.vehicle_detector.sort_by_area()
            first_detection = self.vehicle_detector.get_first_detection()
            vehicle_image = self.vehicle_detector.crop_box_detected(
                box = first_detection.box, 
                image = payload.image
            )
            
            self.license_plate_detector.detections = self.license_plate_detector_port.detect(vehicle_image)

            """ For test """
            license_plate_img = self.license_plate_detector.get_first_detection()
            img_cropped = self.license_plate_detector.crop_box_detected(license_plate_img.box, vehicle_image)

            cv2.imwrite('storage/cropped_ivan_stbks.png', img_cropped)
            """ For test """


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