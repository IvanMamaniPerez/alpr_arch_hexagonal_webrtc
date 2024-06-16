import numpy as np
import cv2
from src.Recognizer.LicensePlateOCR import LicensePlateOCR
from src.Recognizer.VehicleDetector import VehicleDetector

vehicle_detector = VehicleDetector()
name_image = "auto_photo.png"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
vehicle_detected = vehicle_detector.predict(img)
box_coordinates = vehicle_detected['box_coordinates']

image_croped = img[box_coordinates['y1']:box_coordinates['y2'], box_coordinates['x1']:box_coordinates['x2']]


# cv2.imwrite('auto_cerca_gerar.png', image_croped)

""" ocr = LicensePlateOCR(confidence=0.4);
name_image = "crop_2024-06-07_16:39:38.jpg"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

result = ocr.extract_license_plate(img)
print(result)  """

