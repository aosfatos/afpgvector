from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class AFPGVectorConfig(AppConfig):
    name = "afpgvector"

    def ready(self):
        if "vector" not in settings.DATABASES:
            raise ImproperlyConfigured("must set 'vector database' in DATABASES")
