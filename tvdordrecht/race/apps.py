from django.apps import AppConfig

class RaceConfig(AppConfig):
    name = 'race'
    verbose_name = "Wedstrijd"

    def ready(self):
        import signals
