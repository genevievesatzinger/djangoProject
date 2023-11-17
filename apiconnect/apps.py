from django.apps import AppConfig


class ApiconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apiconnect'


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals