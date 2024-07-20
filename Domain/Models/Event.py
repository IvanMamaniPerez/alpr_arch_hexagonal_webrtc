from Domain.Enums.EventChannelEnum import EventChannelEnum
from datetime import datetime
from Domain.Payloads.Payload import Payload
class Event:
    def __init__(self, event_id: str, channel: EventChannelEnum, created_at: datetime, payload: Payload) -> None:
        self.event_id   = event_id
        self.channel    = channel
        self.created_at = created_at
        self.payload    = payload

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        return cls(
            event_id   = data["event_id"],
            channel    = EventChannelEnum(data["channel"]),
            created_at = datetime.fromisoformat(data["created_at"]),
            payload    = Payload.from_dict(data["payload"])
        )