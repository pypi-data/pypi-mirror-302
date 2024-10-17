import sys
import logging
import traceback
from threading import local
from typing import TypedDict
from django.conf import settings

from latta.latta.api import LattaApi
from .consts import LattaProperties
from rest_framework.views import APIView
from django.utils.deprecation import MiddlewareMixin
from .logging import LattaLogEntry, RequestLoggingHandler, thread_local


local = local()

class LattaExceptionData(TypedDict):
    name: str
    message: str
    stack: list[str]

class LattaMiddleware(MiddlewareMixin):
    api = LattaApi()

    def __init__(self, get_response):
        super().__init__(get_response)
        self.handler = RequestLoggingHandler()


    def process_request(self, request):
        thread_local.request_logs = []
        logging.getLogger().addHandler(self.handler)
        # Store the original _handle_exception method
        if hasattr(request, 'resolver_match') and request.resolver_match:
            if hasattr(request.resolver_match, 'func') and hasattr(request.resolver_match.func, 'view_class'):
                view_class = request.resolver_match.func.view_class
                if issubclass(view_class, APIView):
                    self.original_handle_exception = view_class.handle_exception
                    view_class.handle_exception = self.custom_handle_exception

    def process_response(self, request, response):
        # Restore the original _handle_exception method
        if hasattr(self, 'original_handle_exception'):
            if hasattr(request, 'resolver_match') and request.resolver_match:
                if hasattr(request.resolver_match, 'func') and hasattr(request.resolver_match.func, 'view_class'):
                    request.resolver_match.func.view_class.handle_exception = self.original_handle_exception

        logging.getLogger().removeHandler(self.handler)
        exception = getattr(local, 'error_data', None)
        
        if exception:
            relation_id = self.save_snapshot(request, response, exception, getattr(thread_local, 'request_logs', None))
            if relation_id: 
                response.set_cookie(
                    'Latta-Recording-Relation-Id', 
                    relation_id,
                    secure=True,
                    httponly=False
                )

        return response

    def process_exception(self, request, exception):
        self.store_exception()
        return None

    def custom_handle_exception(self, exc):
        response = self.original_handle_exception(exc)
        self.store_exception()
        return response

    def store_exception(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

        error_data: LattaExceptionData = {
            'name': str(exc_type.__name__),
            'message': str(exc_value),
            'stack': stack_trace,
        }

        setattr(local, 'error_data', error_data)

    def get_response_content(self, response):
        if hasattr(response, 'rendered_content'):
            return response.rendered_content.decode('utf-8')
        elif hasattr(response, 'content'):
            return response.content.decode('utf-8')
        else:
            return str(response)

    def save_snapshot(self, request, response, exception: LattaExceptionData, logs: list[LattaLogEntry] | None) -> str | None:
        latta_relation_id: str | None = getattr(request, 'Latta-Recording-Relation-Id', None) or request.COOKIES.get('Latta-Recording-Relation-Id')
        data = self.api.put_snapshot(exception['message'], latta_relation_id)
        if not data:
            return None
        self.api.put_snapshot_data(data[0], request, response, exception, logs)
        return data[1]
