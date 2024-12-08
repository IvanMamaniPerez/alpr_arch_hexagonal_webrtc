from enum import Enum

class DetectionStatusEnum(Enum):
    IN_PROGRESS = 'in_progress'
    COMPLETED   = 'completed'
    FAILED      = 'failed'
    CANCELLED   = 'cancelled'