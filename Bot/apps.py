from django.apps import AppConfig
from Bot.main import bot


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bot'

    def ready(self):
        bot()


