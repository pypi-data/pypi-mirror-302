import logging
from threading import local
from typing import TypedDict

thread_local = local()

class LattaLogEntry(TypedDict):
    timestamp: int
    level: str
    message: str

class RequestLoggingHandler(logging.Handler):
    def emit(self, record):
        if hasattr(thread_local, 'request_logs'):
            log: LattaLogEntry = {
                "timestamp": int(record.created*1000),
                "level": record.levelname,
                "message": record.getMessage()
            }
            thread_local.request_logs.append(log)