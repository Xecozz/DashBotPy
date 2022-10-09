from django.db import models

from .managers import DiscordUserOauth2Manager
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


#model Discord USer
class DiscordUser(models.Model):
    objects = DiscordUserOauth2Manager()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True)
    locale = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True)
    tag = models.CharField(max_length=100, null=True)
    premium_type = models.IntegerField(max_length=100, null=True)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    guilds = models.JSONField(null=True)

    @staticmethod
    def is_authenticated(self, request):
        return True

    def __str__(self):
        if  self.last_login != None:
            date = self.last_login.strftime('%A, %d %b %Y %H:%M:%S')
            return f"{self.discord_tag}: {self.id} [{date}]"
        return f"{self.discord_tag}: {self.id}"

#Model refresh Token
class RefreshToken(models.Model):
    objects = DiscordUserOauth2Manager()

    id = models.BigIntegerField(primary_key=True)
    token = models.TextField()
    last_date = models.DateTimeField(null=True)
