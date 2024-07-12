from Domain.Detectors.VehicleDetector import VehicleDetector 
from Domain.Detectors.LicensePlateDetector import LicensePlateDetector 
from Domain.Detectors.LicensePlateOCR import LicensePlateOCR 
from infrastructure.Adapters.YOLODetectorAdapter import YOLODetectorAdapter as Detector
import numpy as np
import cv2
import traceback
import datetime

#Testing old code for OCR
from src.Detector.LicensePlateOCR import LicensePlateOCR as LicensePlateOCROld

vehicle_detector = VehicleDetector()
license_plate_detector = LicensePlateDetector()
license_plate_ocr = LicensePlateOCROld(
    confidence=.4
)
start = datetime.datetime.now()

name_image = "auto_photo"
extension = ".png"
path_image = 'storage/'+ name_image + extension

nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

print(start)

# result = vehicle_detector.predict(img)
try:

    img_cropped = Detector.crop_box_detected(result.box_coordinates, img)
    img_license_plate = license_plate_detector.predict(img)

    print(img_license_plate.to_dict())

    img_license_plate_cropped = Detector.crop_box_detected(img_license_plate.box_coordinates, img)
    final_license_plate = license_plate_ocr.extract_license_plate(img_license_plate_cropped)
    
    cv2.imwrite('storage/results/'+name_image+'_vehicle.png', img_cropped)
    cv2.imwrite('storage/results/'+name_image+'_license_plate.png', img_license_plate_cropped)

    print(final_license_plate)
    print(datetime.datetime.now())
    print("Time total:", datetime.datetime.now() - start)
    
except Exception as e:
    print(e)
    print(traceback.format_exc())
