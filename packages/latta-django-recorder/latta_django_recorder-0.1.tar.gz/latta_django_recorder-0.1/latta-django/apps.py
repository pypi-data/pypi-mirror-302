import os
import logging
from .api import LattaApi
from django.apps import AppConfig
from .consts import LattaProperties
from django.core.cache import cache

class LattaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'latta'
    logger = logging.getLogger(__name__)

    def ready(self):
        """
        Acquire Latta instance id on startup
        """
        if not os.environ.get('RUN_MAIN'):
            return
            
        if cache.get(LattaProperties.LATTA_INSTANCE_CACHE_KEY.value):
            return
        try:
            LattaApi().put_instance()
        except Exception as err:
            self.logger.warning(err)
        
        

        