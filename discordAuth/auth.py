from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser
from django.contrib.auth.models import User


class DiscordAuthentificationBackend(BaseBackend):
    def authenticate(self, request, user, guilds) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) == 0:
            print("User was not found => saving...")
            new_user = DiscordUser.objects.create_new_discord_user(user, guilds)
            print(user)
        return find_user

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None