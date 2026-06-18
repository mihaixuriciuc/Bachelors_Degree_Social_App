from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.user'

    def ready(self):
        import apps.user.signals  # noqa: F401 — import is for side-effect (registering signals)