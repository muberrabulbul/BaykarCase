from django.apps import AppConfig


class BaykarAccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "baykaraccounts"

    def ready(self):
        import baykaraccounts.signals
