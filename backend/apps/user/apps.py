from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Renamed from AccountsConfig to match the app name 'apps.user'.

    The ready() method is called once when Django starts up.  Importing
    the signals module here is what activates the @receiver decorators
    inside it — without this, the signal never fires.
    """
    name = 'apps.user'

    def ready(self):
        import apps.user.signals  # noqa: F401 — import is for side-effect (registering signals)