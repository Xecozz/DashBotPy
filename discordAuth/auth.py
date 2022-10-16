import logging

from django.contrib.auth.backends import BaseBackend

from .models import DiscordUser


class DiscordAuthentificationBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) != 0:
            return find_user

        logging.info(f"{user['username']} ({user['id']}) : User was not found => saving...")
        DiscordUser.objects.create_new_discord_user(user)

        return DiscordUser.objects.filter(id=user['id'])

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None



