import numpy as np
import cv2
from Recognizer.LicensePlateDetector import LicensePlateDetector
from ultralytics import YOLO

analyzer = LicensePlateDetector()
path_image = 'auto_photo.png'


def filter_by_highest_confidence(detections):
    filtered_detections = {}
    for box, confidence, class_id in detections:
        # Convertir coordenadas a enteros antes de usarlas como clave
        box_tuple = tuple(map(int, box))
        if box_tuple not in filtered_detections or filtered_detections[box_tuple][1] < confidence:
            # Almacenar la detección con la mayor confianza para estas coordenadas enteras
            filtered_detections[box_tuple] = (box, confidence, class_id)
    return list(filtered_detections.values())


modelOCR = YOLO("models/ocr_license_plate.pt")
modelOCR.fuse()
# name_image = "crop_cvtcolor_2024-06-07_16:40:40.jpg"
# name_image = "crop_2024-06-07_16:39:38.jpg"
name_image = "auto_rojo.png"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

list_pred = modelOCR.predict(img)

contador = 0

for pred in list_pred:
    detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                    for i, box in enumerate(pred.boxes.xyxy.tolist())]
    detections.sort(key=lambda x: x[0][0])

    detections = filter_by_highest_confidence(detections)
    # Procesar cada detección ordenada
    for box, confidence, class_id in detections:
        x1, y1, x2, y2 = map(int, box)
        class_name = pred.names[class_id]

        print('Class Name:', class_name)
        print('Class Confidence:', confidence)
        print('Box Coordinates:', x1, y1, x2, y2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(str(contador)+ '_resultado_'+ name_image+'.png', img)
