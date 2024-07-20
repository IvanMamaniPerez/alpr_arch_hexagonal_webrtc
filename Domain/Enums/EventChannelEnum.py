from enum import Enum

class EventChannelEnum(Enum):
    WEBRTC_DATACHANNEL = 'webrtc_datachannel'
    WEBHOOK     = 'webhook'
    QUEUE       = 'queue'