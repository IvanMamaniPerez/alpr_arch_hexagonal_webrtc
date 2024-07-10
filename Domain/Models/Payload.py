class Payload:
    
    def __init__(self, uuid: str ,reference_id:str, data: dict) -> None:
        self.uuid         = uuid
        self.reference_id = reference_id
        self.data         = data
        
    def to_dict(self) -> dict:
        return {
            "uuid"         : self.uuid,
            "reference_id" : self.reference_id,
            "data"         : self.data
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Payload':
        return cls(
            uuid         = data["uuid"],
            reference_id = data["reference_id"],
            data         = data["data"]
        )