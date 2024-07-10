from enum import Enum

class EventTypeEnum(Enum):
    DATACHANNEL = 'datachannel'
    WEBHOOK     = 'webhook'
    QUEUE       = 'queue'