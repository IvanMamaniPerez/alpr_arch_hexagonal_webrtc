import numpy as np
import cv2
from src.Recognizer.LicensePlateOCR import LicensePlateOCR
from src.Recognizer.VehicleDetector import VehicleDetector

vehicle_detector = VehicleDetector()
name_image = "auto_frontal.png"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
vehicle_detected = vehicle_detector.predict(img)
box_coordinates = vehicle_detected['box_coordinates']
image_croped = img[box_coordinates[1]:box_coordinates[3], box_coordinates[0]:box_coordinates[2]]

cv2.imwrite('moto_cerca_process.png', image_croped)



""" ocr = LicensePlateOCR(confidence=0.4);
name_image = "crop_2024-06-07_16:39:38.jpg"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

result = ocr.extract_license_plate(img)
print(result) """

