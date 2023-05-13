from django.apps import AppConfig


class TablesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Tables'

    def ready(self):
        import apps.Tables.signals