import json
import psutil
from typing import TypedDict

class LattaSystemInfo(TypedDict):
    cpu_usage: float
    total_memory: int
    free_memory: int

def safe_serialize_environ(environ):
    """Tries to safely serialize environment variables"""
    safe_environ = {}
    
    for key, value in environ.items():
        try:
            json.dumps({key: value})
            safe_environ[key] = value
        except (TypeError, ValueError):
            safe_environ[key] = str(value)
    
    return safe_environ

def get_system_info() -> LattaSystemInfo:
    """Get current system info"""
    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()

    return {
        'cpu_usage': cpu_usage,
        'total_memory': memory.total,
        'free_memory': memory.free
    }