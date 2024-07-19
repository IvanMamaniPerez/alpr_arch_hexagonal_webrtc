from Infrastructure.Adapters.DetectorAdapter import DetectorAdapter
from Domain.Detectors.VehicleDetector import VehicleDetector
from Application.UseCases.DetectVehicleUseCase import DetectVehicleUseCase
from Domain.Detectors.VehicleDetector import VehicleDetector
from Domain.Detectors.Detector import Detector

import cv2
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

detector_adapter = DetectorAdapter()

vehicle_detector = VehicleDetector(
    model_path    = os.getenv("VEHICLE_MODEL_PATH", ''),
    confidence    = float(os.getenv("VEHICLE_CONFIDENCE", .5))
)

use_case = DetectVehicleUseCase(
    detector_port = detector_adapter,
    vehicle_detector = vehicle_detector
)

name_image = "auto_photo"
extension = ".png"
path_image = 'storage/'+ name_image + extension

nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

detection = use_case.execute(image=img)

print(detection.to_dict())

img_cropped = Detector.crop_box_detected(detection.box, img)

cv2.imwrite('storage/cropped_ivan.png', img_cropped)