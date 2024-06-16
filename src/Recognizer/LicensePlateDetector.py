import numpy as np
import cv2
from ultralytics import YOLO
import pytesseract
import re
import os
from datetime import datetime

class LicensePlateDetector:
    
    def __init__(
            self, 
            model_path = "runs/detect/train/weights/best.pt", 
        ):
        
        self.model = YOLO(model_path)

    
    def predict(self, image) ->None|dict:
        list_pred = self.model.predict(image)
        result = None

        if len(list_pred) > 0:
            pred = list_pred[0]

            # Filtrar las detecciones por la de mayor confianza 
            detections = [(box, pred.boxes.conf[i].item(), int(pred.boxes.cls[i].item()))
                            for i, box in enumerate(pred.boxes.xyxy.tolist())]
            
            if detections:
                first_detection = detections[0]
                result = {
                    'box': first_detection[0],
                    'confidence': first_detection[1],
                    'class_id': first_detection[2]
                }

        return result

    def crop_box(self, box, frame):
        x1, y1, x2, y2 = box    
        return frame[int(y1):int(y2), int(x1):int(x2)]                    
