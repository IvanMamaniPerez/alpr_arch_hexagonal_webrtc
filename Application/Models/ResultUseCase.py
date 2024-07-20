from Domain.Payloads.Payload import Payload
class ResultUseCase:
    def __init__(self, success : bool, payload: Payload, metadata : dict) -> None:
        self.success  : bool    = success
        self.payload  : Payload = payload
        self.metadata : dict    = metadata
        