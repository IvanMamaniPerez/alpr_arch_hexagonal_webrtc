from Domain.Enums.EventTypeEnum import EventTypeEnum
from datetime import datetime
from Domain.Models.Payload import Payload
class Event:
    def __init__(self, event_id: str, type: EventTypeEnum, created_at: datetime, payload: Payload) -> None:
        self.event_id   = event_id
        self.type       = type
        self.created_at = created_at
        self.payload    = payload
        
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        return cls(
            event_id   = data["event_id"],
            type       = EventTypeEnum(data["type"]),
            created_at = datetime.fromisoformat(data["created_at"]),
            payload    = Payload.from_dict(data["payload"])
        )