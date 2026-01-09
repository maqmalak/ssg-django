from django.apps import AppConfig


class HangerlineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hangerline'

    def ready(self):
        import hangerline.signals  # noqa
