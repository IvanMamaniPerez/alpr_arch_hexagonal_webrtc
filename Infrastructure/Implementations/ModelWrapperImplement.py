from numpy import ndarray
from Domain.Models.ModelWrapper import ModelWrapper
from ultralytics import YOLO
class ModelWrapperImplement(ModelWrapper):
    def __init__(self, model_path:str = '', confidence:float = 0) -> None:
        super().__init__(model_path, confidence)
    
    def load_model(self) -> YOLO:
        model = YOLO(self.model_path)
        model.fuse()
        return model
    
    def detect(self, image: ndarray):
        return self.model.predict(image)