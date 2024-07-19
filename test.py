from Domain.Detectors.VehicleDetector import VehicleDetector 
from Domain.Detectors.LicensePlateDetector import LicensePlateDetector 
from Domain.Detectors.LicensePlateOCR import LicensePlateOCR 
from Infrastructure.Adapters.YOLODetectorAdapter import YOLODetectorAdapter as Detector
import numpy as np
import cv2
import traceback
import datetime

#Testing old code for OCR
from src.Detector.LicensePlateOCR import LicensePlateOCR as LicensePlateOCROld
from dotenv import load_dotenv
import os
from ultralytics import YOLO
load_dotenv()
# get implement for the model wrapper
from Infrastructure.Implementations.ModelWrapperImplement import ModelWrapperImplement 

model_wrapper = ModelWrapperImplement()

vehicle_detector = VehicleDetector(
    model_path    = os.getenv("VEHICLE_MODEL_PATH", ''),
    confidence    = float(os.getenv("VEHICLE_CONFIDENCE", .5)),
    model_wrapper = model_wrapper
)

license_plate_detector = LicensePlateDetector(
    model_path    = os.getenv("LICENSE_PLATE_MODEL_PATH", ''),
    confidence    = float(os.getenv("LICENSE_PLATE_CONFIDENCE", .5)),
    model_wrapper = model_wrapper
)

license_plate_ocr = LicensePlateOCR(
    model_path    = os.getenv("OCR_MODEL_PATH", ''),
    confidence    = float(os.getenv("OCR_CONFIDENCE", .4)),
    model_wrapper = model_wrapper
)




# license_plate_ocr = LicensePlateOCROld(
#     confidence=.4
# )
start = datetime.datetime.now()

name_image = "auto_photo"
extension = ".png"
path_image = 'storage/'+ name_image + extension

nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

print(start)
try:
    result = vehicle_detector.model.detect(img)
    img_cropped = Detector.crop_box_detected(result.box_coordinates, img)
    img_license_plate = license_plate_detector.model_wrapper.model.predict(img)

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
