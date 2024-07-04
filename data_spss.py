""" import numpy as np
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
 """

""" import asyncio

async def task(name, delay):
    print(f"Task {name} started, will take {delay} seconds.")
    await asyncio.sleep(delay)
    print(f"Task {name} completed.")

async def main():
    # Ejecutar las tareas concurrentemente
    await asyncio.gather(
        task("A", 3),
        task("B", 1)
    )

# Ejecutar la función principal
asyncio.run(main())
"""

import src.Detector.VehicleDetector as VehicleDetector
import src.Detector.LicensePlateDetector as LicensePlateDetector
from src.Detector.Detector import Detector
import numpy as np
import cv2
import traceback
import datetime


vehicle_detector = VehicleDetector.VehicleDetector()
license_plate_detector = LicensePlateDetector.LicensePlateDetector()
start = datetime.datetime.now()
name_image = "auto_multiple.png"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

print(start)
# result = vehicle_detector.predict(img)
try:
    # img_cropped = Detector.crop_box_detected(result.box_coordinates, img)
    img_license_plate = license_plate_detector.predict(img)
    print(img_license_plate.to_dict())
    img_license_plate_cropped = Detector.crop_box_detected(img_license_plate.box_coordinates, img)
    
    #cv2.imwrite('auto_cerca_gerar.png', img_cropped)
    cv2.imwrite('auto_cerca_gerar_license_plate2.png', img_license_plate_cropped)
    print(datetime.datetime.now())
    print("Time total:", datetime.datetime.now() - start)
except Exception as e:
    print(e)
    print(traceback.format_exc())
