from django.db import models


# Create your models here.

class ChannelSetup(models.Model):
    guild_id = models.IntegerField(primary_key=True)
    channel_annonce = models.IntegerField(null=True)
    channel_logs = models.IntegerField(default=None, null=True)
    channel_bienvenue = models.IntegerField(default=None, null=True)

    def __str__(self):
        return self.guild_id
