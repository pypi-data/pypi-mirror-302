import json
import uuid
import django
import logging
import datetime
import platform
import requests
from django.conf import settings
from django.core.cache import cache

from latta.latta.logging import LattaLogEntry
from .consts import LattaEndpoints, LattaProperties, LattaRecordLevels
from .utils import get_system_info, safe_serialize_environ

class LattaApi:
    logger = logging.getLogger(__name__)
    headers = {'content-type': 'application/json', 'Authorization': f"Bearer {settings.LATTA_API_KEY}"}

    def put_instance(self) -> str | None:
        
        body = {
            'os_version': platform.version(),
            'os': platform.system().lower(),
            'lang': settings.LANGUAGE_CODE,
            'device':'server',
            "framework":"django",
            "framework_version": django.get_version()
        }
        uri = f"{LattaProperties.LATTA_API_URI.value}/{LattaEndpoints.LATTA_PUT_INSTANCE.value}"

        try:
            response = requests.put(uri, headers=self.headers, data=json.dumps(body))
        except Exception as e:
            return None
        if not response.ok:
            raise Exception("Latta responded with error, check your API key")

        data = response.json()
        cache.set(LattaProperties.LATTA_INSTANCE_CACHE_KEY.value, data['id'], timeout=None)
        

    def put_snapshot(self, message: str, related_to_relation_id: str | None ) -> list[str] | None:
        latta_instance:str | None = cache.get(LattaProperties.LATTA_INSTANCE_CACHE_KEY.value)
        if not latta_instance:
            return None

        uri = f"{LattaProperties.LATTA_API_URI.value}/{LattaEndpoints.LATTA_PUT_SNAPSHOT.value%(latta_instance)}"
        relation_id = str(uuid.uuid4())

        data = {
            'message': message,
            'relation_id': None if related_to_relation_id else relation_id,
            'related_to_relation_id': related_to_relation_id
        }

        try:
            snapshot_response = requests.put(uri, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            return None

        if not snapshot_response.ok:
            self.logger.warning("Creation of Latta snapshot did not succeed")
            return None
        
        return [snapshot_response.json()['id'], relation_id]

    def put_snapshot_data(self, snapshot_id: str, request, response, exception, logs: list[LattaLogEntry] | None):
        timestamp = int(datetime.datetime.now().timestamp()*1000)
        attachment = {
            "type":"record",
            "data":{
                "type":"request",
                "timestamp":timestamp,
                "level": LattaRecordLevels.LATTA_ERROR.value,
                "request": {
                    "method": request.method,
                    "url": f"{request._current_scheme_host}{request.path}",
                    "route": request.path,
                    "query":dict(request.GET.items()),
                    "headers": dict(request.headers.items()),
                    "body": request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body,
                },
                "response": {
                    "status_code": response.status_code,
                    "body": response.content.decode('utf-8') if isinstance(response.content, bytes) else response.content,
                    "headers": dict(response.headers.items()) 
                },
                "name": exception["name"],
                "message": exception["message"],
                "stack": "\n".join(exception["stack"]) ,
                "environment_variables": safe_serialize_environ(request.environ),
                "system_info": get_system_info(),
                "logs": {
                    "entries": logs if logs else []
                }
            }
        }

        uri = f"{LattaProperties.LATTA_API_URI.value}/{LattaEndpoints.LATTA_PUT_SNAPSHOT_ATTACHMENT.value%(snapshot_id)}"
        try:
            data_response = requests.put(uri, headers=self.headers, data=json.dumps(attachment))
        except Exception as e:
            self.logger.exception(e)
            return False

        return data_response.ok
