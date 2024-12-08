from Application.Models.Payload import Payload
import numpy as np

class PayloadDetectionComplete(Payload):
    def __init__(
        self, 
        payload            : Payload,
        image_vehicle      : np.ndarray,
        image_license_plate: np.ndarray,
        text_license_plate : str
    ) -> None:

        super().__init__(
            uuid         = payload.uuid,
            reference_id = payload.reference_id,
            client_id    = payload.client_id,
            image        = payload.image
        )
        
        self.image_vehicle      : np.ndarray = image_vehicle
        self.image_license_plate: np.ndarray = image_license_plate
        self.text_license_plate : str        = text_license_plate

    def to_dict(self) -> dict:
        return {
            "payload"            : super().to_dict(),
            "image_vehicle"      : self.image_vehicle,
            "image_license_plate": self.image_license_plate,
            "text_license_plate" : self.text_license_plate
        } 
        
    def get_payload(self) -> Payload:
        return Payload(
            uuid         = self.uuid,
            reference_id = self.reference_id,
            client_id    = self.client_id,
            image        = self.image
        )
        
    @classmethod
    def from_dict(cls, data: dict) -> 'PayloadDetectionComplete':
        return cls(
            payload             = Payload.from_dict(data["payload"]),
            image_vehicle       = data["image_vehicle"],
            image_license_plate = data["image_license_plate"],
            text_license_plate  = data["text_license_plate"]
        )

