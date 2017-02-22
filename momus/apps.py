from django.apps import AppConfig


class MomusConfig(AppConfig):
    name = 'momus'

    def ready(self):
        import momus.signals
