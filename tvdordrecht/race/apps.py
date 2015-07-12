from django.apps import AppConfig

class RaceConfig(AppConfig):
    name = 'race'

    def ready(self):
        import signals