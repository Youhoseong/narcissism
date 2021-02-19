from django.apps import AppConfig


class AlarmsConfig(AppConfig):
    name = 'alarms'
    verbose_name='Alarms Configuration for msg'
    def ready(self):
        import alarms.signals