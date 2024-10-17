from enum import Enum

class LattaProperties(Enum):
    LATTA_API_URI = 'https://recording.latta.ai/v1'
    LATTA_INSTANCE_CACHE_KEY = 'latta_instance_id'

class LattaEndpoints(Enum):
    LATTA_PUT_INSTANCE = 'instance/backend'
    LATTA_PUT_SNAPSHOT = 'snapshot/%s'
    LATTA_PUT_SNAPSHOT_ATTACHMENT = 'snapshot/%s/attachment'

class LattaRecordLevels(Enum):
    LATTA_ERROR = 'ERROR'
    LATTA_WARN = 'WARN'
    LATTA_FATAL = 'FATAL'
    