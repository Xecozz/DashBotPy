import datetime

from django.db import models
from .managers import DiscordUserOauth2Manager
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


# Create your models here.

class DiscordUser(models.Model):
    objects = DiscordUserOauth2Manager()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    guilds = models.JSONField(null=True)

    def is_authenticated(self, request):
        return True

    def __str__(self):
        if  self.last_login != None:
            date = self.last_login.strftime('%A, %d %b %Y %H:%M:%S')
            return f"{self.discord_tag}: {self.id} [{date}]"
        return f"{self.discord_tag}: {self.id}"
