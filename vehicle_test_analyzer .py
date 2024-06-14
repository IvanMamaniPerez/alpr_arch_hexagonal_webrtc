import numpy as np
import cv2
from src.Recognizer.LicensePlateAnalyzer import LicensePlateAnalyzer
from ultralytics import YOLO

analyzer = LicensePlateAnalyzer()
path_image = 'moto.png'

def filter_by_highest_confidence(detections):
    filtered_detections = {}
    for box, confidence, class_id in detections:
        # Convertir coordenadas a enteros antes de usarlas como clave
        box_tuple = tuple(map(int, box))
        if box_tuple not in filtered_detections or filtered_detections[box_tuple][1] < confidence:
            # Almacenar la detección con la mayor confianza para estas coordenadas enteras
            filtered_detections[box_tuple] = (box, confidence, class_id)
    return list(filtered_detections.values())


modelOCR = YOLO("models/best_vehicles.pt")
modelOCR.fuse()
name_image = "moto_cerca.png"
path_image = 'storage/'+ name_image
nparr = np.fromfile(path_image, np.uint8)
img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

list_pred = modelOCR.predict(img)

contador = 0

pred = list_pred[0]
detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                for i, box in enumerate(pred.boxes.xyxy.tolist())]

detections.sort(key=lambda x: (x[0][2] - x[0][0]) * (x[0][3] - x[0][1]), reverse=True)


if detections:
    # Solo usar el primer resultado, que es el más grande
    box, confidence, class_id = detections[0]

    x1, y1, x2, y2 = map(int, box)
    class_name = pred.names[class_id]
    if(confidence >= 0.5):
        print('Class Name:', class_name)
        print('Class Confidence:', confidence)
        print('Box Coordinates:', x1, y1, x2, y2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imwrite(str(contador)+ '_resultado_'+ name_image+'.png', img)
