from Infrastructure.Adapters.DetectorAdapter import DetectorAdapter
from Domain.Detectors.VehicleDetector import VehicleDetector
from Domain.Detectors.LicensePlateDetector import LicensePlateDetector
from Application.UseCases.DetectVehicleAndLicensePlateUseCase import DetectVehicleAndLicensePlateUseCase
from Domain.Detectors.VehicleDetector import VehicleDetector
from Domain.Detectors.Detector import Detector
from Domain.Payloads.Payload import Payload
import cv2
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

vehicle_detector_adapter = DetectorAdapter()
license_plate_detector_adapter = DetectorAdapter()

vehicle_detector = VehicleDetector(
    model_path    = os.getenv("VEHICLE_MODEL_PATH", ''),
    confidence    = float(os.getenv("VEHICLE_CONFIDENCE", .5))
)

license_plate_detector = LicensePlateDetector(
    model_path    = os.getenv("LICENSE_PLATE_MODEL_PATH", ''),
    confidence    = float(os.getenv("LICENSE_PLATE_CONFIDENCE", .5))
)

use_case = DetectVehicleAndLicensePlateUseCase(
    vehicle_detector_port = vehicle_detector_adapter,
    license_plate_detector_port = license_plate_detector_adapter,
    vehicle_detector = vehicle_detector,
    license_plate_detector = license_plate_detector
)



name_image = "auto_photo"
extension = ".png"
path_image = 'storage/'+ name_image + extension

nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

payload = Payload('asdfasdfasdfsd', 'asdfa', '2134', img)

detection = use_case.execute(payload)

print(detection)

""" img_cropped = Detector.crop_box_detected(detection.box, img)

cv2.imwrite('storage/cropped_ivan.png', img_cropped) """