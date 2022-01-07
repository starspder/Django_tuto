"""
어플리케이션 등록하는 곳, 잘 건들이지 않음

"""

from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
