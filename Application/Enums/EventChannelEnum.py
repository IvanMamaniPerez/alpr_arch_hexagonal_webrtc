from enum import Enum

class EventChannelEnum(Enum):
    WEBRTC_DATACHANNEL = 'webrtc_datachannel'
    WEBHOOK            = 'webhook'
    WEBHOOK_QUEUE      = 'webhook_queue'