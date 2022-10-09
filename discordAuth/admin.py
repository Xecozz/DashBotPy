from django.contrib import admin
from discordAuth.models import DiscordUser

#add DiscordUser infos to panel admin
admin.site.register(DiscordUser)